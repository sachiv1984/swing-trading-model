/**
 * v9.14 ST-11 (BLG-FE-231, EPIC-02) — the Daily Position Monitor's suggestions follow the grace period.
 *
 * Design source: docs/design/2026-10-29__release-v9.14/monitor-grace-aware-suggestions/decision_record.md §6
 * Spec: positions.md §Daily Position Monitor Exit Queue → §Monitor Suggestions
 *
 *   SC-MGS-01  An in-grace position priced below its trailing stop is not suggested; its row reads
 *              "In grace: stop not enforced" and the footer counts no suggestion (AC 2)
 *   SC-MGS-02  A post-grace breach is suggested with "Stop price hit", a risk_off_exit position with
 *              "Market risk off", and a position with both reads "Market risk off" (AC 3)
 *   SC-MGS-03  Risk-off comes from the position's risk_off_exit flag, not the regime list: a
 *              risk_off regime with risk_off_exit false suggests nothing (decision record §2.1)
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

function makePosition(overrides = {}) {
  return {
    id: 'pos-1', ticker: 'POST', market: 'US', status: 'open',
    entry_price: 100, current_price: 85, current_price_native: 85,
    stop_price: 90, stop_price_native: 90, current_trailing_stop: 90, current_trailing_stop_native: 90,
    shares: 10, fx_rate: 1.27, live_fx_rate: 1.27,
    holding_days: 20, grace_period: false, grace_days_remaining: null,
    risk_off_exit: false, entry_date: '2026-09-01', pnl: -150, pnl_percent: -15,
    ...overrides,
  };
}

const IN_GRACE_BREACH = makePosition({
  id: 'pos-grace', ticker: 'GRACE', holding_days: 4, grace_period: true, grace_days_remaining: 6, stop_price: 0,
});
const POST_GRACE_BREACH = makePosition({ id: 'pos-stop', ticker: 'STOP' });
const RISK_OFF = makePosition({ id: 'pos-ro', ticker: 'RISKOFF', current_price: 120, current_price_native: 120, risk_off_exit: true });
const BOTH = makePosition({ id: 'pos-both', ticker: 'BOTH', risk_off_exit: true });
const HEALTHY = makePosition({ id: 'pos-ok', ticker: 'OK', current_price: 120, current_price_native: 120 });

async function stubDashboard(page, positions, regimes = []) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/market/regime**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: regimes }) })
  );
  await page.route(new RegExp(`${API}/positions$`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) })
  );
}

async function openMonitor(page) {
  // The "Daily Monitor" quick action is a plain onClick <div>: click its heading.
  await page.getByRole('heading', { name: 'Daily Monitor' }).click();
  await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible({ timeout: 10000 });
}

function row(page, ticker) {
  return page.locator(`[data-testid="monitor-row"][data-ticker="${ticker}"]`);
}

test.describe('Daily Position Monitor grace-aware suggestions (ST-11)', () => {
  test('SC-MGS-01: an in-grace breach is not suggested and says why', async ({ page }) => {
    await stubDashboard(page, [IN_GRACE_BREACH]);
    await page.goto('/#/Dashboard');
    await openMonitor(page);

    const grace = row(page, 'GRACE');
    await expect(grace).toHaveAttribute('data-suggestion', 'hold');
    await expect(grace).toContainText('In grace: stop not enforced');
    await expect(grace).not.toContainText('Stop price hit');
    await expect(page.getByRole('dialog')).toContainText('All positions healthy');

    // Clicking a hold row selects nothing, so no exit can be queued for it.
    await grace.click();
    await expect(page.getByRole('button', { name: 'Exit Selected' })).toHaveCount(0);
  });

  test('SC-MGS-02: post-grace breach and risk-off are suggested; risk-off wins when both apply', async ({ page }) => {
    await stubDashboard(page, [POST_GRACE_BREACH, RISK_OFF, BOTH, HEALTHY]);
    await page.goto('/#/Dashboard');
    await openMonitor(page);

    await expect(row(page, 'STOP')).toHaveAttribute('data-suggestion', 'exit');
    await expect(row(page, 'STOP')).toContainText('Stop price hit');
    await expect(row(page, 'RISKOFF')).toHaveAttribute('data-suggestion', 'exit');
    await expect(row(page, 'RISKOFF')).toContainText('Market risk off');
    await expect(row(page, 'BOTH')).toHaveAttribute('data-suggestion', 'exit');
    await expect(row(page, 'BOTH')).toContainText('Market risk off');
    await expect(row(page, 'BOTH')).not.toContainText('Stop price hit');
    await expect(row(page, 'OK')).toHaveAttribute('data-suggestion', 'hold');
    await expect(row(page, 'OK')).toContainText('Position OK');
    await expect(page.getByRole('dialog')).toContainText('3 exit suggestions');

    // BOTH queues with "Risk-Off Signal", the same reason the Positions exit dialog pre-selects.
    await row(page, 'BOTH').click();
    await page.getByRole('button', { name: 'Exit Selected' }).click();
    await expect(page.getByTestId('exit-reason-select')).toContainText('Risk-Off Signal');
  });

  test('SC-MGS-03: a risk-off regime alone, without risk_off_exit, suggests nothing', async ({ page }) => {
    await stubDashboard(page, [HEALTHY], [{ market: 'US', status: 'risk_off' }]);
    await page.goto('/#/Dashboard');
    await openMonitor(page);

    await expect(row(page, 'OK')).toHaveAttribute('data-suggestion', 'hold');
    await expect(row(page, 'OK')).toContainText('Position OK');
  });
});
