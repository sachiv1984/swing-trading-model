/**
 * Trade Entry — Pre-Entry Checks on every route
 * ST-01 (BLG-FE-244, EPIC-01, v9.15)
 *
 * Design source: docs/design/2026-11-03__release-v9.15/trade-entry-pre-entry-checks/decision_record.md
 * Frontend spec: docs/specs/frontend/components/position_form.md v1.13 §Pre-Entry Checks
 * Ruling: ESC-EXEC-20261104-01, Branch A (acknowledge to proceed); strategy_rules.md §4.2.6 / §4.2.1 v1.23
 *
 * Coverage:
 *   SC-TEPC-01  Sidebar route: the panel shows the check results before save (AC 1)
 *   SC-TEPC-02  Positions "New Position" route: the panel shows (AC 1)
 *   SC-TEPC-03  `n` shortcut from Positions: the panel shows (AC 1)
 *   SC-TEPC-04  Risk-off regime FAIL: Submit disabled with the helper line until acknowledged;
 *               the save then sends pre_entry_override_acknowledged: true (AC 2)
 *   SC-TEPC-05  Unknown regime FAILs (never a pass) and needs the acknowledgement (AC 2)
 *   SC-TEPC-06  Before Shares, the panel shows the waiting line
 *   SC-TEPC-07  Linked plan with stored checks: the panel is not shown; the on-plan line shows once (AC 3)
 *   SC-TEPC-08  Linked plan without stored checks: the panel shows exactly once (AC 3)
 *   SC-TEPC-09  Endpoint failure never disables Submit
 *   SC-TEPC-10  All checks pass: no acknowledgement, Submit enabled, no override flag sent
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradeEntry').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const PASS_CHECKS = [
  { rule: 'regime_gate', status: 'pass', detail: 'UK market is risk-on' },
  { rule: 'cash_constraint', status: 'pass', detail: 'Sufficient cash' },
];
const RISK_OFF_CHECKS = [
  { rule: 'regime_gate', status: 'fail', detail: 'UK market is risk-off (FTSE below 200-day MA)' },
  { rule: 'cash_constraint', status: 'pass', detail: 'Sufficient cash' },
];
const UNKNOWN_CHECKS = [
  { rule: 'regime_gate', status: 'fail', detail: 'UK market regime is unknown: index data unavailable' },
  { rule: 'cash_constraint', status: 'pass', detail: 'Sufficient cash' },
];

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockValidation(page, { checks, advisory, fail = false }) {
  await page.route(new RegExp(`${API}/portfolio/pre-entry-validation`), (route) => {
    if (fail) {
      route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'boom' }) });
      return;
    }
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { advisory_status: advisory, checks } }),
    });
  });
}

async function mockAddPosition(page, onRequest) {
  await page.route(`${API}/portfolio/position`, (route) => {
    const body = route.request().postDataJSON();
    if (onRequest) onRequest(body);
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: { ticker: body.ticker, total_cost: 1000, fees_paid: 5, entry_price: body.entry_price, trade_plan_linked: false, initial_stop: 90, remaining_cash: 5000, position_id: 'new-pos-tepc' },
      }),
    });
  });
}

async function mockPlans(page, plan) {
  await page.route(`${API}/trade-plans`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [plan] }) })
  );
  await page.route(`${API}/trade-plans/${plan.id}`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plan }) })
  );
}

// The Positions page needs a market-status shape and a bare positions array
// (same stubs as exit-condition-surfacing.spec.js); the generic fallback crashes it.
async function mockPositionsPage(page) {
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { spy: { price: 500, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7600, is_risk_on: true }, fx_rate: 1.27 } }) })
  );
  await page.route(`${API}/positions**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(`${API}/positions/grace-period-alerts`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

const tickerInput = (page) => page.getByPlaceholder('e.g., AAPL or VOD.L');
const submit = (page) => page.getByRole('button', { name: /create position/i });

async function fillUkEntry(page, { shares = '10' } = {}) {
  await tickerInput(page).fill('LGEN');
  await page.getByPlaceholder('0.00').first().fill('100');
  await page.getByPlaceholder('Fetched automatically if blank').fill('2');
  if (shares !== null) await page.getByPlaceholder('0', { exact: true }).fill(shares);
}

async function expectPanelResults(page) {
  const panel = page.getByTestId('pre-entry-checks-panel');
  await expect(panel).toBeVisible({ timeout: 10000 });
  await expect(panel.getByTestId('pre-entry-check-regime_gate')).toBeVisible({ timeout: 10000 });
}

test('SC-TEPC-01: the sidebar route shows the pre-entry check results before save', async ({ page }) => {
  await mockFallback(page);
  await mockValidation(page, { checks: PASS_CHECKS, advisory: 'pass' });
  await mockPositionsPage(page);
  await page.goto('/#/Positions');
  await page.getByRole('link', { name: 'Trade Entry' }).first().click();
  await expect(page).toHaveURL(/#\/TradeEntry/);
  await expect(tickerInput(page)).toBeVisible({ timeout: 10000 });
  await fillUkEntry(page);
  await expectPanelResults(page);
});

test('SC-TEPC-02: the Positions "New Position" route shows the pre-entry checks', async ({ page }) => {
  await mockFallback(page);
  await mockValidation(page, { checks: PASS_CHECKS, advisory: 'pass' });
  await mockPositionsPage(page);
  await page.goto('/#/Positions');
  await page.getByRole('button', { name: /new position/i }).first().click();
  await expect(page).toHaveURL(/#\/TradeEntry/);
  await expect(tickerInput(page)).toBeVisible({ timeout: 10000 });
  await fillUkEntry(page);
  await expectPanelResults(page);
});

test('SC-TEPC-03: the n shortcut from Positions shows the pre-entry checks', async ({ page }) => {
  await mockFallback(page);
  await mockValidation(page, { checks: PASS_CHECKS, advisory: 'pass' });
  await mockPositionsPage(page);
  await page.goto('/#/Positions');
  await expect(page.getByRole('button', { name: /new position/i }).first()).toBeVisible({ timeout: 10000 });
  await page.keyboard.press('n');
  await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });
  await expect(tickerInput(page)).toBeVisible({ timeout: 10000 });
  await fillUkEntry(page);
  await expectPanelResults(page);
});

test('SC-TEPC-04: a risk-off FAIL disables Submit until acknowledged, and the save records the override', async ({ page }) => {
  let body = null;
  await mockFallback(page);
  await mockValidation(page, { checks: RISK_OFF_CHECKS, advisory: 'fail' });
  await mockAddPosition(page, (b) => { body = b; });
  await page.goto('/#/TradeEntry');
  await fillUkEntry(page);

  const regime = page.getByTestId('pre-entry-check-regime_gate');
  await expect(regime).toHaveAttribute('data-status', 'fail', { timeout: 10000 });
  await expect(regime).toContainText('✗');

  await expect(submit(page)).toBeDisabled();
  const helper = page.getByTestId('pre-entry-ack-required');
  await expect(helper).toHaveText('Tick the acknowledgement in Pre-Entry Checks to save.');
  await expect(submit(page)).toHaveAttribute('aria-describedby', 'pre-entry-ack-required');

  await page.getByTestId('override-acknowledgement-checkbox').check();
  await expect(helper).toHaveCount(0);
  await expect(submit(page)).toBeEnabled();

  await submit(page).click();
  await expect.poll(() => body).not.toBeNull();
  expect(body.pre_entry_override_acknowledged).toBe(true);
});

test('SC-TEPC-05: an unknown regime FAILs, is never shown as a pass, and needs the acknowledgement', async ({ page }) => {
  await mockFallback(page);
  await mockValidation(page, { checks: UNKNOWN_CHECKS, advisory: 'fail' });
  await page.goto('/#/TradeEntry');
  await fillUkEntry(page);

  const regime = page.getByTestId('pre-entry-check-regime_gate');
  await expect(regime).toHaveAttribute('data-status', 'fail', { timeout: 10000 });
  await expect(regime).toContainText('unknown');
  await expect(regime).not.toContainText('✓');
  await expect(submit(page)).toBeDisabled();
  await expect(page.getByTestId('pre-entry-ack-required')).toBeVisible();

  await page.getByTestId('override-acknowledgement-checkbox').check();
  await expect(submit(page)).toBeEnabled();
});

test('SC-TEPC-06: before Shares is entered, the panel shows the waiting line', async ({ page }) => {
  await mockFallback(page);
  await mockValidation(page, { checks: RISK_OFF_CHECKS, advisory: 'fail' });
  await page.goto('/#/TradeEntry');
  await fillUkEntry(page, { shares: null });
  await expect(page.getByTestId('pre-entry-checks-panel')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('pre-entry-checks-waiting')).toHaveText('Enter shares to run the pre-entry checks.');
});

const PLAN_BASE = {
  ticker: 'LGEN', market: 'UK', status: 'draft', position_id: null, r_target: 2,
  setup_thesis: 'Breakout', updated_at: '2026-11-01T10:00:00Z',
  planned_entry_price: 100, planned_stop_price: 90, planned_quantity: 10,
};

async function linkPlan(page, plan) {
  await page.getByTestId('link-trade-plan-select').click();
  await page.getByRole('option', { name: new RegExp(plan.ticker) }).click();
}

test('SC-TEPC-07: a linked plan with stored checks hides the panel and shows the on-plan line once', async ({ page }) => {
  const plan = { ...PLAN_BASE, id: 'plan-tepc-snap', pre_entry_validation_snapshot: { advisory_status: 'pass', checks: PASS_CHECKS } };
  await mockFallback(page);
  await mockValidation(page, { checks: RISK_OFF_CHECKS, advisory: 'fail' });
  await mockPlans(page, plan);
  await page.goto('/#/TradeEntry');
  await expect(page.getByTestId('link-trade-plan-select')).toBeVisible({ timeout: 10000 });
  await fillUkEntry(page);
  await expect(page.getByTestId('pre-entry-checks-panel')).toHaveCount(1, { timeout: 10000 });

  await linkPlan(page, plan);
  await expect(page.getByTestId('pre-entry-checks-on-plan')).toHaveCount(1, { timeout: 10000 });
  await expect(page.getByTestId('pre-entry-checks-on-plan')).toHaveText('Pre-entry checks were run on the linked plan.');
  await expect(page.getByTestId('pre-entry-checks-panel')).toHaveCount(0);
  await expect(submit(page)).toBeEnabled();
  // Form state survives the switch.
  await expect(page.getByPlaceholder('0', { exact: true })).toHaveValue('10');
});

test('SC-TEPC-08: a linked plan without stored checks shows the panel exactly once', async ({ page }) => {
  const plan = { ...PLAN_BASE, id: 'plan-tepc-nosnap', pre_entry_validation_snapshot: null };
  await mockFallback(page);
  await mockValidation(page, { checks: PASS_CHECKS, advisory: 'pass' });
  await mockPlans(page, plan);
  await page.goto('/#/TradeEntry');
  await expect(page.getByTestId('link-trade-plan-select')).toBeVisible({ timeout: 10000 });
  await fillUkEntry(page);
  await linkPlan(page, plan);
  await expect(page.getByTestId('pre-entry-check-regime_gate')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('pre-entry-checks-panel')).toHaveCount(1);
  await expect(page.getByTestId('pre-entry-checks-on-plan')).toHaveCount(0);
});

test('SC-TEPC-09: a validation endpoint failure never disables Submit', async ({ page }) => {
  await mockFallback(page);
  await mockValidation(page, { fail: true });
  await page.goto('/#/TradeEntry');
  await fillUkEntry(page);
  await expect(page.getByText('Validation unavailable — proceed with manual checks')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('pre-entry-ack-required')).toHaveCount(0);
  await expect(submit(page)).toBeEnabled();
});

test('SC-TEPC-10: when every check passes there is no acknowledgement and no override flag', async ({ page }) => {
  let body = null;
  await mockFallback(page);
  await mockValidation(page, { checks: PASS_CHECKS, advisory: 'pass' });
  await mockAddPosition(page, (b) => { body = b; });
  await page.goto('/#/TradeEntry');
  await fillUkEntry(page);
  await expect(page.getByTestId('pre-entry-check-regime_gate')).toHaveAttribute('data-status', 'pass', { timeout: 10000 });
  await expect(page.getByTestId('override-acknowledgement-checkbox')).toHaveCount(0);
  await expect(submit(page)).toBeEnabled();
  await submit(page).click();
  await expect.poll(() => body).not.toBeNull();
  expect(body.pre_entry_override_acknowledged).toBeUndefined();
});
