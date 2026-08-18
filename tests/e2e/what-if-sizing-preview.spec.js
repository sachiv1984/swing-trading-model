/**
 * What-If Sizing Preview — Acceptance Tests (V-WHATIF-01..03)
 * ST-05 (BLG-FEAT-91, EPIC-02, v8.9) — Pre-commit "what-if" sizing/risk
 * simulator on the trade-plan form.
 *
 * AC-01: User can adjust stop distance/entry price on the trade-plan form
 *        and see position size, R at risk, and portfolio heat impact update
 *        live, before saving.
 * AC-03: No DB write occurs from interacting with the preview alone.
 *
 * (AC-02 — preview value matches what is actually saved — holds by
 * construction: the panel calls the identical POST /portfolio/size endpoint
 * PositionSizingWidget uses at order entry; covered by code reuse, not a
 * separate E2E assertion here.)
 *
 * Spec ref: docs/specs/frontend/pages/trade_plan.md §5d
 * Design source: docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMarketStatus(page) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { spy: { is_risk_on: true }, ftse: { is_risk_on: true } } }),
    })
  );
}

async function mockSettings(page) {
  await page.route(`${API}/settings`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: [{ id: 'settings-1', default_risk_percent: 1.0 }] }),
      });
    } else {
      route.continue();
    }
  });
}

/** Mock POST /portfolio/size with a caller-supplied data payload. */
async function mockPortfolioSize(page, data) {
  await page.route(new RegExp(`${API}/portfolio/size`), (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data }) });
  });
}

async function gotoTradePlan(page, params = { ticker: 'AAPL', market: 'US' }) {
  const qs = new URLSearchParams(params).toString();
  await page.goto(`/#/TradePlan?${qs}`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

test.describe('What-If Sizing Preview (V-WHATIF-01..03)', () => {
  test('V-WHATIF-01 — panel hidden until Stop Level is set', { tag: ['@smoke'] }, async ({ page }) => {
    await mockFallback(page);
    await mockMarketStatus(page);
    await mockSettings(page);

    await gotoTradePlan(page);

    await expect(page.getByTestId('what-if-sizing-preview-panel')).toHaveCount(0);

    // Setting a stop price reveals the panel (empty Planned Entry Price input).
    const stopInput = page.getByTestId('planned-stop-price-input');
    await stopInput.fill('142.00');

    await expect(page.getByTestId('what-if-sizing-preview-panel')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('what-if-entry-price-input')).toBeVisible();
  });

  test('V-WHATIF-02 — entering planned entry price shows live size/R/heat', { tag: ['@smoke'] }, async ({ page }) => {
    await mockFallback(page);
    await mockMarketStatus(page);
    await mockSettings(page);
    await mockPortfolioSize(page, {
      valid: true,
      suggested_shares: 17.8571,
      risk_amount: 125.0,
      stop_distance: 70.0,
      estimated_cost: 15178.57,
      estimated_fees: 0.0,
      fx_rate_used: 1.3642,
      cash_sufficient: true,
      available_cash: 20000.0,
      concentration_adjusted: false,
      concentration_reason: null,
      heat_impact_percent: 0.8,
    });

    await gotoTradePlan(page);

    await page.getByTestId('planned-stop-price-input').fill('780.00');
    await expect(page.getByTestId('what-if-sizing-preview-panel')).toBeVisible({ timeout: 5000 });

    await page.getByTestId('what-if-entry-price-input').fill('850.00');

    await page.waitForResponse(/\/portfolio\/size/, { timeout: 5000 });

    await expect(page.getByTestId('what-if-suggested-shares')).toHaveText('17.8571 shares', { timeout: 5000 });
    await expect(page.getByTestId('what-if-r-at-risk')).toHaveText('1250.00'); // (850-780)*17.8571
    await expect(page.getByTestId('what-if-heat-impact')).toHaveText('+0.8% heat');
  });

  test('V-WHATIF-03 — interacting with the preview never fires a trade-plan write', { tag: ['@smoke'] }, async ({ page }) => {
    await mockFallback(page);
    await mockMarketStatus(page);
    await mockSettings(page);
    await mockPortfolioSize(page, {
      valid: true,
      suggested_shares: 10.0,
      risk_amount: 100.0,
      stop_distance: 10.0,
      estimated_cost: 1000.0,
      estimated_fees: 0.0,
      fx_rate_used: 1.0,
      cash_sufficient: true,
      available_cash: 20000.0,
      concentration_adjusted: false,
      concentration_reason: null,
      heat_impact_percent: 0.2,
    });

    let tradePlanWriteFired = false;
    await page.route(`${API}/trade-plans`, (route) => {
      if (route.request().method() === 'POST' || route.request().method() === 'PUT') {
        tradePlanWriteFired = true;
      }
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    });

    await gotoTradePlan(page);

    await page.getByTestId('planned-stop-price-input').fill('90.00');
    await expect(page.getByTestId('what-if-sizing-preview-panel')).toBeVisible({ timeout: 5000 });
    await page.getByTestId('what-if-entry-price-input').fill('100.00');
    await page.waitForResponse(/\/portfolio\/size/, { timeout: 5000 });

    // Also adjust Risk % within the panel — still no write.
    await page.getByTestId('what-if-risk-percent-input').fill('2.0');
    await page.waitForTimeout(500); // debounce window + margin

    expect(tradePlanWriteFired).toBe(false);
  });
});
