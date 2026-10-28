/**
 * Position Sizing Calculator — §4.1.7 UI behaviours
 * ST-19 (BLG-QA-206, EPIC-03, v9.12)
 *
 * Canonical rules: claude/strategy/strategy_rules.md §4.1.7
 * Frontend spec:   docs/specs/frontend/components/position_form.md §Position Sizing Calculator
 * Matrix:          docs/testing/strategy_rule_test_traceability_matrix.md (C4.1.7-*)
 *
 * Coverage (one scenario per clause; C4.1.7-04 is already asserted by smoke-critical-paths PATH-1):
 *   SC-PSW-01  C4.1.7-01  Calculator is visible on load with no toggle or activation control
 *   SC-PSW-02  C4.1.7-02  Recalculates on entry / stop / risk % change, 300 ms after typing stops
 *   SC-PSW-03  C4.1.7-03  Loading state shows between the debounce firing and the response
 *   SC-PSW-05  C4.1.7-05  A manually entered share count is not overwritten; "Use suggested shares" applies it
 *   SC-PSW-06  C4.1.7-06  Insufficient cash: no auto-fill; max affordable shares shown as information
 *   SC-PSW-07  C4.1.7-07  Invalid result: no auto-fill; inline plain-language message
 *   SC-PSW-08  C4.1.7-08  Invalid or cash-constrained results do not block submission
 *
 * POST /portfolio/size is mocked with the canonical response shape (openapi.yaml OkPositionSize).
 * The stop is the system stop, entry − 5× ATR (position_form.md §Initial Stop); typing an ATR
 * means the ST-17 ATR preview (GET /market/atr) is not called, but it is mocked to null anyway.
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradeEntry').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const VALID = {
  valid: true, suggested_shares: 10.0, risk_amount: 100.0, stop_distance: 10.0,
  estimated_cost: 1000.0, estimated_fees: 0.0, fx_rate_used: 1.0, cash_sufficient: true,
  available_cash: 20000.0, concentration_adjusted: false, concentration_reason: null,
};

async function mockCommon(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(/\/market\/atr\//, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { ticker: 'LGEN', market: 'UK', atr: null, atr_period: 14, as_of: '2026-10-13T09:00:00+00:00' } }),
    })
  );
}

/**
 * Mocks POST /portfolio/size. `data` may be a function of the request body.
 * Records each call's body and arrival time.
 */
async function mockSize(page, data, { delayMs = 0 } = {}) {
  const calls = [];
  await page.route(/\/portfolio\/size/, async (route) => {
    const body = route.request().postDataJSON();
    calls.push({ body, at: Date.now() });
    if (delayMs) await new Promise((r) => setTimeout(r, delayMs));
    const payload = typeof data === 'function' ? data(body) : data;
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: payload }) });
  });
  return calls;
}

async function gotoTradeEntry(page) {
  await page.goto('/#/TradeEntry');
  await expect(page.getByPlaceholder('e.g., AAPL or VOD.L')).toBeVisible({ timeout: 10000 });
}

const ticker = (page) => page.getByPlaceholder('e.g., AAPL or VOD.L');
const entry = (page) => page.getByPlaceholder('0.00').first();
const atr = (page) => page.getByPlaceholder('Fetched automatically if blank');
const shares = (page) => page.getByPlaceholder('0', { exact: true });
const riskPercent = (page) => page.locator('input[type="number"][min="0.01"][max="100"]');
const submit = (page) => page.getByRole('button', { name: /create position/i });

// UK ticker, entry 100, ATR 2 → system stop 90.
async function fillSizingInputs(page, { entryPrice = '100', atrValue = '2' } = {}) {
  await ticker(page).fill('LGEN');
  await entry(page).fill(entryPrice);
  await atr(page).fill(atrValue);
}

test('SC-PSW-01 (C4.1.7-01): the calculator is visible on load with no toggle', async ({ page }) => {
  await mockCommon(page);
  await gotoTradeEntry(page);

  const heading = page.getByText('Position Sizing', { exact: true });
  await expect(heading).toBeVisible();
  await expect(riskPercent(page)).toBeVisible();
  await expect(page.getByTestId('sizing-empty-hint')).toBeVisible();
  // No activation control of any kind on the page.
  await expect(page.getByRole('switch')).toHaveCount(0);
  await expect(page.getByRole('checkbox')).toHaveCount(0);
  await expect(page.getByRole('button', { name: /sizing|calculator/i })).toHaveCount(0);
});

test('SC-PSW-02 (C4.1.7-02): recalculates on entry, stop and risk % change, 300 ms after typing stops', async ({ page }) => {
  await mockCommon(page);
  const calls = await mockSize(page, VALID);
  // A controlled clock makes the 300 ms debounce deterministic.
  await page.clock.install();
  await gotoTradeEntry(page);
  await ticker(page).fill('LGEN');
  await atr(page).fill('2');
  // Freeze time (running any pending timers first), so only runFor() advances it.
  await page.clock.pauseAt(Date.now() + 10_000);

  // Typing the entry price key by key, 60 ms apart (under the debounce), makes no call yet.
  for (const key of '100') {
    await entry(page).press(key);
    await page.clock.runFor(60);
  }
  await page.clock.runFor(180); // 240 ms after the last keystroke
  await page.waitForTimeout(200);
  expect(calls.length).toBe(0);

  // At 300 ms after the last keystroke, one call fires with the final values.
  await page.clock.runFor(70);
  await expect.poll(() => calls.length, { timeout: 5000 }).toBe(1);
  expect(calls[0].body).toMatchObject({ entry_price: 100, stop_price: 90 });

  // Stop change (via ATR): 100 − 5 × 3 = 85.
  await atr(page).fill('3');
  await page.clock.runFor(310);
  await expect.poll(() => calls.length).toBe(2);
  expect(calls[1].body.stop_price).toBe(85);

  // Risk % change.
  await riskPercent(page).fill('2');
  await page.clock.runFor(310);
  await expect.poll(() => calls.length).toBe(3);
  expect(calls[2].body.risk_percent).toBe(2);
});

test('SC-PSW-03 (C4.1.7-03): a loading state shows until the response returns', async ({ page }) => {
  await mockCommon(page);
  await mockSize(page, VALID, { delayMs: 1500 });
  await gotoTradeEntry(page);
  await fillSizingInputs(page);

  await expect(page.locator('svg.animate-spin')).toBeVisible();
  await expect(page.getByText('10.0000')).toBeVisible({ timeout: 5000 });
  await expect(page.locator('svg.animate-spin')).toHaveCount(0);
});

test('SC-PSW-05 (C4.1.7-05): a manually entered share count is not overwritten', async ({ page }) => {
  await mockCommon(page);
  const calls = await mockSize(page, VALID);
  await gotoTradeEntry(page);
  await shares(page).fill('7');
  await fillSizingInputs(page);

  await expect.poll(() => calls.length).toBeGreaterThan(0);
  await expect(page.getByText('10.0000')).toBeVisible();
  await expect(shares(page)).toHaveValue('7');

  const useButton = page.getByRole('button', { name: 'Use suggested shares' });
  await expect(useButton).toBeVisible();
  await useButton.click();
  await expect(shares(page)).toHaveValue('10');
  await expect(useButton).toHaveCount(0);
});

test('SC-PSW-06 (C4.1.7-06): insufficient cash does not auto-fill and shows max affordable as information', async ({ page }) => {
  await mockCommon(page);
  const calls = await mockSize(page, { ...VALID, cash_sufficient: false, available_cash: 450.0, max_affordable_shares: 4.5 });
  await gotoTradeEntry(page);
  await fillSizingInputs(page);

  await expect.poll(() => calls.length).toBeGreaterThan(0);
  const info = page.getByText('Max affordable: 4.5000 shares');
  await expect(info).toBeVisible();
  await expect(info).not.toHaveClass(/amber|rose|red/);
  await expect(shares(page)).toHaveValue('');
  await expect(page.getByRole('button', { name: 'Use suggested shares' })).toHaveCount(0);
});

test('SC-PSW-07 (C4.1.7-07): an invalid result does not auto-fill and shows an inline message', async ({ page }) => {
  await mockCommon(page);
  const calls = await mockSize(page, { valid: false, reason: 'INVALID_RISK_PERCENT', suggested_shares: null });
  await gotoTradeEntry(page);
  await fillSizingInputs(page);

  await expect.poll(() => calls.length).toBeGreaterThan(0);
  await expect(page.getByText('Risk % must be greater than 0')).toBeVisible();
  await expect(shares(page)).toHaveValue('');
});

for (const [label, result] of [
  ['invalid', { valid: false, reason: 'INVALID_RISK_PERCENT', suggested_shares: null }],
  ['cash-constrained', { ...VALID, cash_sufficient: false, max_affordable_shares: 4.5 }],
]) {
  test(`SC-PSW-08 (C4.1.7-08): a ${label} sizing result does not block submission`, async ({ page }) => {
    await mockCommon(page);
    const calls = await mockSize(page, result);
    let posted = null;
    await page.route(`${API}/portfolio/position`, (route) => {
      posted = route.request().postDataJSON();
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { ticker: 'LGEN', initial_stop: 90, trade_plan_linked: false, position_id: 'p-psw' } }),
      });
    });
    await gotoTradeEntry(page);
    await fillSizingInputs(page);
    await expect.poll(() => calls.length).toBeGreaterThan(0);

    await shares(page).fill('3');
    await expect(submit(page)).toBeEnabled();
    await submit(page).click();
    await expect.poll(() => posted).not.toBeNull();
    expect(posted.shares).toBe(3);
  });
}
