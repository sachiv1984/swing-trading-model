/**
 * Stale price marker on Positions, and its accessible explanation — Playwright E2E Tests
 * ST-07 / ST-08 (EPIC-01, v9.14, BLG-BE-168 / BLG-FE-214)
 * Design: docs/design/2026-10-29__release-v9.14/stale-price-marker/decision_record.md
 *
 *   SC-SPM-01: the Positions table and grid show price-stale-marker on the stale row only (ST-07 AC 3)
 *   SC-SPM-02: on /risk and on Positions the marker is reachable by Tab, its accessible description is the
 *              decision record §2.3 text for that surface, and focus or a tap opens the tooltip (ST-08 AC 2, AC 3)
 *   SC-SPM-03: axe finds no serious or critical violation on /risk with a stale row (ST-08 AC 1)
 *   SC-SPM-04: Dashboard Card 2's link carries the /risk explanation as its accessible description
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const RISK_TEXT =
  'Live price unavailable, so the last stored price is shown. Value, P&L and heat use this price until a live price is fetched. Reload the page to try again.';
const POSITIONS_TEXT =
  'Live price unavailable, so the last stored price is shown. Value and P&L use this price until a live price is fetched. Reload the page to try again.';

function position(overrides = {}) {
  return {
    id: 'pos-1', ticker: 'MU', market: 'US', entry_date: '2026-09-10', entry_price: 78.74, shares: 10,
    current_price: 88.89, current_price_native: 120.0, current_value: 888.9, pnl: 101.5, pnl_pct: 12.9,
    pnl_percent: 12.9, current_stop: 72.44, stop_price: 72.44, stop_price_native: 97.8, holding_days: 28,
    status: 'open', display_status: 'PROFITABLE', fx_rate: 1.27, grace_period: false, grace_days_remaining: null,
    live_fx_rate: 1.35, fx_rate_source: 'live', price_is_stale: false, initial_stop: 70.0, tags: [],
    ...overrides,
  };
}

const POSITIONS = [position({ id: 'a', ticker: 'MU', price_is_stale: true }), position({ id: 'b', ticker: 'WDC' })];

async function mockAll(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(POSITIONS) })
  );
  await page.route(`${API}/portfolio`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        cash: 5000, cash_balance: 5000, total_value: 10000, open_positions_value: 5000, total_pnl: 0,
        current_drawdown_percent: 0, peak_portfolio_value: 10000, portfolio_heat_percent: 8.5,
        live_fx_rate: 1.35, fx_rate_source: 'live', position_risks: [], positions: POSITIONS,
      }),
    })
  );
}

async function gotoPositions(page, view) {
  await page.goto('/#/Positions');
  const toggle = page.locator(`[aria-label="${view} view"]`);
  await toggle.waitFor({ state: 'visible', timeout: 15000 });
  await toggle.click();
}

test('SC-SPM-01a: the Positions table marks the stale row only', async ({ page }) => {
  await mockAll(page);
  await gotoPositions(page, 'Table');
  await expect(page.getByRole('row').filter({ hasText: 'WDC' })).toBeVisible({ timeout: 15000 });
  await expect(page.getByTestId('price-stale-marker')).toHaveCount(1);
  await expect(page.getByRole('row').filter({ hasText: 'MU' }).getByTestId('price-stale-marker')).toBeVisible();
  await expect(page.getByRole('row').filter({ hasText: 'WDC' }).getByTestId('price-stale-marker')).toHaveCount(0);
});

test('SC-SPM-01b: the Positions grid marks the stale card only', async ({ page }) => {
  await mockAll(page);
  await gotoPositions(page, 'Grid');
  await expect(page.getByText('WDC').first()).toBeVisible({ timeout: 15000 });
  await expect(page.getByTestId('price-stale-marker')).toHaveCount(1);
});

test('SC-SPM-02a: the /risk marker is reachable by Tab and described', async ({ page }) => {
  await mockAll(page);
  await page.goto('/#/RiskDashboard');
  const marker = page.locator('tr', { hasText: 'MU' }).getByTestId('price-stale-marker');
  await expect(marker).toBeVisible({ timeout: 15000 });
  await expect(marker).toHaveAccessibleName('Price stale');
  await expect(marker).toHaveAccessibleDescription(RISK_TEXT);
  await expect(marker).not.toHaveAttribute('title', /.*/);
  for (let i = 0; i < 60 && !(await marker.evaluate((el) => el === document.activeElement)); i += 1) {
    await page.keyboard.press('Tab');
  }
  await expect(marker).toBeFocused();
  await expect(page.getByRole('tooltip')).toContainText('Value, P&L and heat use this price');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('tooltip')).toHaveCount(0);
});

test('SC-SPM-02b: the Positions marker uses the Positions text and opens on tap', async ({ page }) => {
  await mockAll(page);
  await gotoPositions(page, 'Table');
  const marker = page.getByRole('row').filter({ hasText: 'MU' }).getByTestId('price-stale-marker');
  await expect(marker).toBeVisible({ timeout: 15000 });
  await expect(marker).toHaveAccessibleDescription(POSITIONS_TEXT);
  await marker.click();
  await expect(page.getByRole('tooltip')).toContainText('Value and P&L use this price');
});

test('SC-SPM-03: axe finds no serious or critical violation on /risk with a stale row', async ({ page }) => {
  await mockAll(page);
  await page.goto('/#/RiskDashboard');
  await expect(page.getByTestId('price-stale-marker')).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(1000);
  const results = await new AxeBuilder({ page }).analyze();
  const serious = results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
  expect(serious.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).join(', ')}`)).toEqual([]);
});

test('SC-SPM-04: Dashboard Card 2 link carries the /risk explanation', async ({ page }) => {
  await mockAll(page);
  await page.goto('/#/');
  const notice = page.getByTestId('dashboard-price-stale-notice');
  await expect(notice).toHaveText('⚠ 1 position price stale', { timeout: 15000 });
  await expect(notice).not.toHaveAttribute('title', /.*/);
  await expect(page.getByRole('link').filter({ has: notice })).toHaveAccessibleDescription(RISK_TEXT);
});
