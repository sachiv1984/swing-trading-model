/**
 * Risk Dashboard and Dashboard price integrity — Playwright E2E Tests
 * EPIC-02, v9.11. Design: docs/design/2026-10-08__release-v9.11/risk-price-integrity/decision_record.md
 * Spec refs: docs/specs/frontend/pages/risk_dashboard.md §6, docs/specs/frontend/pages/dashboard.md §4 Card 2
 *
 * Covers:
 *   SC-RPI-01: ST-10 (BLG-BE-154) — a position with price_is_stale=true shows the stale marker on the
 *              Risk Dashboard and the stale notice on the Dashboard; price_is_stale=false shows neither
 *   SC-RPI-02: ST-11 (BLG-FE-206) — a US row's Entry renders "£" with the GET /portfolio GBP value; a GRACE
 *              row shows "Not enforced (grace)" in Stop and Stop Dist % with no rose/amber colour
 *   SC-RPI-03: ST-13 (BLG-BE-155) — the Stop Dist % cell shows the API's stop_distance_pct, not a value
 *              derived in the browser from GBP figures
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

function position(overrides = {}) {
  return {
    id: 'pos-1', ticker: 'MU', market: 'US', entry_date: '2026-09-10', entry_price: 78.74, shares: 10,
    current_price: 88.89, current_value: 888.9, pnl: 101.5, pnl_pct: 12.9, current_stop: 72.44,
    holding_days: 28, status: 'open', display_status: 'PROFITABLE', fx_rate: 1.27, grace_period: false,
    grace_days_remaining: null, live_fx_rate: 1.35, price_is_stale: false,
    ...overrides,
  };
}

function portfolio(positions) {
  return {
    cash: 5000, cash_balance: 5000, total_value: 10000, open_positions_value: 5000, total_pnl: 0,
    current_drawdown_percent: 0, peak_portfolio_value: 10000, portfolio_heat_percent: 8.5,
    position_risks: positions.map((p) => ({ ticker: p.ticker, position_risk_gbp: 100 })),
    positions,
  };
}

async function mockAll(page, positions) {
  // Fallback first: later routes take precedence in Playwright.
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(`${API}/portfolio`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(portfolio(positions)) })
  );
}

async function gotoRisk(page) {
  await page.goto('/#/RiskDashboard');
  await expect(page.locator('h1').filter({ hasText: 'Risk Dashboard' })).toBeVisible({ timeout: 15000 });
  await expect(page.getByText('Position Risk')).toBeVisible({ timeout: 15000 });
}

test.describe('SC-RPI-01 — Stale price marker (ST-10, BLG-BE-154)', () => {
  test('SC-RPI-01a: a stale position shows the marker on the Risk Dashboard', async ({ page }) => {
    await mockAll(page, [position({ id: 'a', ticker: 'MU', price_is_stale: true }), position({ id: 'b', ticker: 'WDC' })]);
    await gotoRisk(page);
    const markers = page.getByTestId('price-stale-marker');
    await expect(markers).toHaveCount(1);
    const row = page.locator('tr', { hasText: 'MU' });
    await expect(row.getByTestId('price-stale-marker')).toBeVisible();
    await expect(row.getByTestId('price-stale-marker')).toHaveAttribute(
      'aria-label', "Live price unavailable. Showing the last stored price converted at today's FX rate."
    );
    await expect(page.locator('tr', { hasText: 'WDC' }).getByTestId('price-stale-marker')).toHaveCount(0);
  });

  test('SC-RPI-01b: no marker when price_is_stale is false or missing', async ({ page }) => {
    const missing = position({ id: 'c', ticker: 'DELL' });
    delete missing.price_is_stale;
    await mockAll(page, [position({ id: 'a', ticker: 'MU' }), missing]);
    await gotoRisk(page);
    await expect(page.locator('tr', { hasText: 'DELL' })).toBeVisible();
    await expect(page.getByTestId('price-stale-marker')).toHaveCount(0);
  });

  test('SC-RPI-01c: the Dashboard Portfolio Heat card shows the stale notice with the count', async ({ page }) => {
    await mockAll(page, [
      position({ id: 'a', ticker: 'MU', price_is_stale: true }),
      position({ id: 'b', ticker: 'WDC', price_is_stale: true }),
      position({ id: 'c', ticker: 'DELL' }),
    ]);
    await page.goto('/#/');
    const notice = page.getByTestId('dashboard-price-stale-notice');
    await expect(notice).toBeVisible({ timeout: 15000 });
    await expect(notice).toHaveText('⚠ 2 position prices stale');
  });

  test('SC-RPI-01d: the Dashboard shows no stale notice when every price is live', async ({ page }) => {
    await mockAll(page, [position({ id: 'a', ticker: 'MU' })]);
    await page.goto('/#/');
    await expect(page.getByText('Portfolio Heat')).toBeVisible({ timeout: 15000 });
    await expect(page.getByText('8.5%').first()).toBeVisible({ timeout: 15000 });
    await expect(page.getByTestId('dashboard-price-stale-notice')).toHaveCount(0);
  });
});

test.describe('SC-RPI-02 — GBP entry prices and grace stops (ST-11, BLG-FE-206)', () => {
  test('SC-RPI-02a: a US row\'s Entry cell shows the GBP value from GET /portfolio', async ({ page }) => {
    await mockAll(page, [position({ id: 'a', ticker: 'MU', market: 'US', entry_price: 78.74 })]);
    await gotoRisk(page);
    await expect(page.locator('th', { hasText: 'Entry (GBP)' })).toBeVisible();
    await expect(page.locator('th', { hasText: 'Stop (GBP)' })).toBeVisible();
    const entryCell = page.locator('tr', { hasText: 'MU' }).locator('td').nth(2);
    await expect(entryCell).toHaveText('£78.74');
  });

  test('SC-RPI-02b: a GRACE row shows "Not enforced (grace)" in Stop and Stop Dist % with no distance colour', async ({ page }) => {
    await mockAll(page, [
      position({ id: 'g', ticker: 'SNDK', display_status: 'GRACE', grace_period: true, grace_days_remaining: 4,
        holding_days: 6, current_price: 50.0, current_stop: 49.5 }),
      position({ id: 'p', ticker: 'MU' }),
    ]);
    await gotoRisk(page);
    const row = page.locator('tr', { hasText: 'SNDK' });
    const cells = row.getByTestId('stop-not-enforced');
    await expect(cells).toHaveCount(2);
    await expect(cells.first()).toHaveText('Not enforced (grace)');
    await expect(cells.first()).toHaveAttribute('title', 'Stops are not enforced during the 10-day grace period. See strategy rules §6.');
    // Stop Dist % cell (6th column) carries no rose/amber distance colour.
    const distCell = row.locator('td').nth(5);
    await expect(distCell).not.toHaveClass(/text-rose-400|text-amber-400/);
    await expect(distCell.locator('.text-rose-400, .text-amber-400')).toHaveCount(0);
    // A post-grace row still shows its stop price.
    await expect(page.locator('tr', { hasText: 'MU' }).getByTestId('stop-not-enforced')).toHaveCount(0);
  });

  test('SC-RPI-02c: GRACE rows sort by grace days remaining, fewest first', async ({ page }) => {
    await mockAll(page, [
      position({ id: 'g1', ticker: 'AAA', display_status: 'GRACE', grace_period: true, grace_days_remaining: 7 }),
      position({ id: 'g2', ticker: 'BBB', display_status: 'GRACE', grace_period: true, grace_days_remaining: 2 }),
    ]);
    await gotoRisk(page);
    const tickers = page.locator('tbody tr td:first-child');
    await expect(tickers).toHaveText(['BBB', 'AAA']);
  });
});

test.describe('SC-RPI-03 — Stop Dist % from the API (ST-13, BLG-BE-155)', () => {
  test('SC-RPI-03a: the table shows the API stop_distance_pct, not a browser-derived value', async ({ page }) => {
    // GBP figures alone would give (74.07 - 72.44) / 74.07 = 2.2%; the API's native value is 8.0%.
    await mockAll(page, [
      position({ id: 'a', ticker: 'MU', current_price: 74.07, current_stop: 72.44, stop_distance_pct: 8.0 }),
      position({ id: 'b', ticker: 'WDC', current_price: 50, current_stop: 49, stop_distance_pct: 4.2 }),
      position({ id: 'c', ticker: 'DELL', current_price: 50, current_stop: 40, stop_distance_pct: null }),
    ]);
    await gotoRisk(page);
    const distOf = (t) => page.locator('tr', { hasText: t }).locator('td').nth(5);
    await expect(distOf('MU')).toHaveText('8.0%');
    await expect(distOf('MU')).toHaveClass(/text-amber-400/);
    await expect(distOf('WDC')).toHaveText('4.2%');
    await expect(distOf('WDC')).toHaveClass(/text-rose-400/);
    await expect(distOf('DELL')).toHaveText('—');
    // Within PROFITABLE, smallest API distance first.
    await expect(page.locator('tbody tr td:first-child')).toHaveText(['WDC', 'MU', 'DELL']);
  });
});
