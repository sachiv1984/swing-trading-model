/**
 * v9.10 ST-12 (BLG-FE-196, EPIC-03) — lifecycle badge agrees with the §6 grace
 * window, in calendar days.
 *
 * Design source: docs/design/2026-10-06__release-v9.10/lifecycle-badge-grace-calendar-days/decision_record.md §5
 * Spec: docs/specs/frontend/pages/positions.md §Grace Precedence and UNKNOWN Reasons
 *
 *   SC-LBG-01  In-grace position more than 0.5 ATR below entry shows "GRACE — 4d left"
 *              (the backend's grace-first classification is unit-tested in
 *              tests/test_position_lifecycle.py; this asserts the rendering)
 *   SC-LBG-02  GRACE tooltip and aria-label use calendar days
 *   SC-LBG-03  No element or tooltip on the page says "trading day"
 *   SC-LBG-04  Each UNKNOWN lifecycle_reason renders its own tooltip
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation via page.goto('/#/Positions')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function stubCommon(page) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/alerts/history`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { spy: { price: 500, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7600, is_risk_on: true }, fx_rate: 1.27 } }) })
  );
  await page.route(`${API}/portfolio**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: { total_value: 10000, positions: [] } }) })
  );
  await page.route(`${API}/metrics**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: {} }) })
  );
  await page.route(`${API}/notifications**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );
}

function makePosition(overrides = {}) {
  return {
    id: 'pos-001',
    ticker: 'NVDA',
    market: 'US',
    entry_price: 800.0,
    current_price: 700.0,
    current_price_native: 700.0, // well over 0.5 ATR below entry
    atr_value: 20.0,
    stop_price: 0,
    stop_price_native: 0,
    shares: 10,
    pnl: -1000.0,
    pnl_percent: -12.5,
    holding_days: 6,
    grace_period: true,
    grace_days_remaining: 4,
    status: 'open',
    entry_date: '2026-04-01',
    lifecycle_state: 'GRACE',
    position_state: 'GRACE',
    days_in_state: 6,
    lifecycle_reason: null,
    ...overrides,
  };
}

async function setup(page, positions, alerts = []) {
  await stubCommon(page);
  await page.route(`${API}/positions**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) })
  );
  await page.route(`${API}/positions/grace-period-alerts`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: alerts }) })
  );
  await page.goto('/#/Positions');
  await page.waitForLoadState('domcontentloaded');
  const tableBtn = page.locator('[aria-label="Table view"]');
  if (await tableBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    await tableBtn.click();
  }
  await expect(page.getByText('NVDA').first()).toBeVisible({ timeout: 8000 });
}

test.describe('ST-12 — lifecycle badge grace window in calendar days', () => {
  test('SC-LBG-01: in-grace position below entry shows "GRACE — 4d left"', async ({ page }) => {
    await setup(page, [makePosition()]);
    const badge = page.getByTestId('lifecycle-badge');
    await expect(badge).toHaveText('GRACE — 4d left');
    await expect(page.getByTestId('lifecycle-badge').filter({ hasText: 'LOSING' })).toHaveCount(0);
  });

  test('SC-LBG-02: GRACE tooltip and aria-label use calendar days', async ({ page }) => {
    await setup(page, [makePosition()]);
    const badge = page.getByTestId('lifecycle-badge');
    await expect(badge).toHaveAttribute(
      'title',
      'Grace period: 4 calendar days left. The stop is tracked but not enforced until the grace period ends (10 calendar days, §6).'
    );
    await expect(badge).toHaveAttribute('aria-label', 'Position state: GRACE, 4 calendar days of grace left');
  });

  test('SC-LBG-03: no "trading day" wording for the grace period', async ({ page }) => {
    const alert = {
      position_id: 'pos-001', ticker: 'NVDA', market: 'US', days_in_state: 8,
      grace_days_remaining: 2, trade_plan_id: null, trade_plan_summary: null,
    };
    await setup(page, [makePosition({ grace_days_remaining: 2, days_in_state: 8, holding_days: 8 })], [alert]);
    await expect(page.getByText(/grace period ends in 2 days\./i)).toBeVisible();
    await expect(page.getByText(/trading day/i)).toHaveCount(0);
    await expect(page.locator('[title*="trading day" i]')).toHaveCount(0);
    await expect(page.locator('[aria-label*="trading day" i]')).toHaveCount(0);
  });

  const unknownCases = [
    ['missing_data', 'No lifecycle state: ATR or price data is missing for this position.'],
    ['flat_after_grace', 'No lifecycle state: the grace period has ended and the price is within 0.5 ATR of entry.'],
    [null, 'No lifecycle state is available for this position.'],
  ];
  for (const [reason, tip] of unknownCases) {
    test(`SC-LBG-04: UNKNOWN tooltip for lifecycle_reason=${reason}`, async ({ page }) => {
      await setup(page, [makePosition({
        lifecycle_state: 'UNKNOWN', position_state: 'UNKNOWN', lifecycle_reason: reason,
        grace_period: false, grace_days_remaining: null, holding_days: 20,
      })]);
      const badge = page.getByTestId('lifecycle-badge');
      await expect(badge).toHaveText('UNKNOWN');
      await expect(badge).toHaveAttribute('title', tip);
    });
  }
});
