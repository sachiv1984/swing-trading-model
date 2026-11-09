/**
 * Trade Plan — suggested size before shares — ST-08 (BLG-FE-256, EPIC-02, v9.16)
 *
 * Design: docs/design/2026-11-06__release-v9.16/signal-to-plan-flow/decision_record.md §2.2, §6
 * Spec: docs/specs/frontend/pages/trade_plan.md v1.22 §5f
 *
 *   SC-TPS-01  Field order Entry | Stop → suggested size → Planned Shares; with entry and stop
 *              entered, Planned Shares pre-fills with the floored §4.1 suggestion (light and dark)
 *   SC-TPS-02  Before entry and stop are both valid there is no line and no placeholder
 *   SC-TPS-03  A typed shares value is not overwritten; "Use suggested size" copies the suggestion in
 *   SC-TPS-04  After the user edits a pre-filled value, a new suggestion no longer writes to it
 *   SC-TPS-05  Cash-insufficient and invalid results show the §10.6a messages and do not pre-fill
 *   SC-TPS-06  Edit mode: a stored planned_quantity counts as typed
 *   SC-TPS-07  "Plan this" (entry pre-filled): entering the stop alone pre-fills shares
 *
 * Infrastructure: page.route() network interception — no live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const VALID = (suggested = 10.7) => ({
  valid: true, suggested_shares: suggested, risk_amount: 100, stop_distance: 10,
  estimated_cost: 1500, estimated_fees: 0, fx_rate_used: 1.27, cash_sufficient: true,
  available_cash: 20000, concentration_adjusted: false, concentration_reason: null,
});

const ok = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });

async function mockCommon(page) {
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(ok({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(ok({ status: 'ok', data: { spy: { price: 521, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7200, is_risk_on: true }, fx_rate: 1.27 } }))
  );
}

/** Mocks POST /portfolio/size; `data` may be a function of the request body. Returns the call log. */
async function mockSize(page, data) {
  const calls = [];
  await page.route(/\/portfolio\/size/, async (route) => {
    const body = route.request().postDataJSON();
    calls.push(body);
    const payload = typeof data === 'function' ? data(body) : data;
    await route.fulfill(ok({ status: 'ok', data: payload }));
  });
  return calls;
}

const entry = (page) => page.getByTestId('planned-entry-price-input');
const stop = (page) => page.getByTestId('planned-stop-price-input');
const shares = (page) => page.getByTestId('planned-quantity-input');
const line = (page) => page.getByTestId('plan-suggested-size');

async function gotoNewPlan(page, query = 'ticker=AAPL&market=US') {
  await page.goto(`/#/TradePlan?${query}`);
  await expect(entry(page)).toBeVisible({ timeout: 10000 });
}

for (const theme of ['dark', 'light']) {
  test(`SC-TPS-01 (${theme}): with entry and stop, Planned Shares pre-fills with the floored §4.1 suggestion`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await mockCommon(page);
    const calls = await mockSize(page, VALID(10.7));
    await gotoNewPlan(page);

    // §5f field order: Entry | Stop above the suggested line, which is above Planned Shares.
    await entry(page).fill('150');
    await stop(page).fill('140');
    await expect(line(page)).toHaveText('Suggested size: 10 shares (§4.1, 1% risk)', { timeout: 5000 });
    await expect(shares(page)).toHaveValue('10');
    const tops = await Promise.all([entry(page), line(page), shares(page)].map((l) => l.evaluate((e) => e.getBoundingClientRect().top)));
    expect(tops[0]).toBeLessThan(tops[1]);
    expect(tops[1]).toBeLessThan(tops[2]);
    await expect(page.getByTestId('plan-use-suggested-size')).toHaveCount(0);

    // The request uses the default risk %, no fx_rate (live rate for US), and the plan's inputs.
    const last = calls[calls.length - 1];
    expect(last).toMatchObject({ entry_price: 150, stop_price: 140, risk_percent: 1, market: 'US', ticker: 'AAPL' });
    expect(last.fx_rate).toBeUndefined();
  });
}

test('SC-TPS-02: before entry and stop are both valid there is no suggested-size line', async ({ page }) => {
  await mockCommon(page);
  await mockSize(page, VALID());
  await gotoNewPlan(page);
  await entry(page).fill('150');
  await page.waitForTimeout(600);
  await expect(line(page)).toHaveCount(0);
  await expect(page.getByTestId('plan-suggested-size-loading')).toHaveCount(0);
  await expect(shares(page)).toHaveValue('');
});

test('SC-TPS-03: a typed shares value is not overwritten, and "Use suggested size" restores the suggestion', async ({ page }) => {
  await mockCommon(page);
  await mockSize(page, VALID(12));
  await gotoNewPlan(page);
  await shares(page).fill('25');
  await entry(page).fill('150');
  await stop(page).fill('140');
  await expect(line(page)).toHaveText('Suggested size: 12 shares (§4.1, 1% risk)', { timeout: 5000 });
  await expect(shares(page)).toHaveValue('25');
  const use = page.getByTestId('plan-use-suggested-size');
  await expect(use).toBeVisible();
  await use.click();
  await expect(shares(page)).toHaveValue('12');
  await expect(use).toHaveCount(0);
});

test('SC-TPS-04: after the user edits a pre-filled value, a new suggestion does not write to it', async ({ page }) => {
  await mockCommon(page);
  await mockSize(page, (body) => VALID(body.stop_price === 140 ? 10 : 20));
  await gotoNewPlan(page);
  await entry(page).fill('150');
  await stop(page).fill('140');
  await expect(shares(page)).toHaveValue('10', { timeout: 5000 });
  await shares(page).fill('7');
  await stop(page).fill('145');
  await expect(line(page)).toHaveText('Suggested size: 20 shares (§4.1, 1% risk)', { timeout: 5000 });
  await expect(shares(page)).toHaveValue('7');
});

test('SC-TPS-05: cash-insufficient and invalid results show their messages and do not pre-fill', async ({ page }) => {
  await mockCommon(page);
  await mockSize(page, (body) =>
    body.stop_price < body.entry_price
      ? { ...VALID(10), cash_sufficient: false, max_affordable_shares: 3.5 }
      : { valid: false, reason: 'INVALID_STOP_DISTANCE' }
  );
  await gotoNewPlan(page);
  await entry(page).fill('150');
  await stop(page).fill('140');
  await expect(line(page)).toHaveText('Max affordable: 3.5000 shares', { timeout: 5000 });
  await expect(shares(page)).toHaveValue('');
  await stop(page).fill('160');
  await expect(line(page)).toHaveText('Stop price must be below entry price', { timeout: 5000 });
  await expect(shares(page)).toHaveValue('');
});

test('SC-TPS-06: in edit mode a stored planned_quantity counts as typed', async ({ page }) => {
  const plan = {
    id: 'plan-tps-edit', ticker: 'AAPL', market: 'US', status: 'draft', position_id: null,
    planned_quantity: 30, planned_entry_price: 150, planned_stop_price: 140, checklist_items: [],
  };
  await mockCommon(page);
  await page.route(`${API}/trade-plans/${plan.id}`, (r) => r.fulfill(ok({ status: 'ok', data: plan })));
  await mockSize(page, VALID(10));
  await page.goto(`/#/TradePlan?edit=${plan.id}`);
  await expect(line(page)).toHaveText('Suggested size: 10 shares (§4.1, 1% risk)', { timeout: 10000 });
  await expect(shares(page)).toHaveValue('30');
  await expect(page.getByTestId('plan-use-suggested-size')).toBeVisible();
});

test('SC-TPS-07: from "Plan this" (entry pre-filled), entering the stop pre-fills shares', async ({ page }) => {
  await mockCommon(page);
  await mockSize(page, VALID(8.9));
  await gotoNewPlan(page, 'ticker=MSFT&market=US&entry_price=410.25');
  await expect(entry(page)).toHaveValue('410.25');
  await stop(page).fill('390');
  await expect(shares(page)).toHaveValue('8', { timeout: 5000 });
});
