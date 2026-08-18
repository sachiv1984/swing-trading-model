/**
 * Position Sizing — Concentration-Aware Sizing Display (V-SIZE-01, V-SIZE-02)
 * ST-04 (BLG-BE-104, EPIC-02, v8.9) — Correlation/sector-concentration-aware
 * position sizing.
 *
 * AC-02: "Sizing output includes a visible reason when reduced or flagged
 * for concentration." Covers the frontend-visible concentration_reason
 * display added to PositionSizingWidget.js per
 * docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md
 * (AlertTriangle icon, amber text, directly beneath the Suggested Shares
 * result line; hidden entirely when concentration_reason is null).
 *
 * Spec ref: docs/specs/frontend/pages/trade_plan.md §10.7
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');
const { SMOKE_SETTINGS, SMOKE_POSITIONS, SMOKE_PORTFOLIO } = require('./mocks/smoke-mock-data');

async function mockCommon(page) {
  await page.route(/\/settings/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SMOKE_SETTINGS) });
    } else {
      route.continue();
    }
  });
  await page.route(/\/positions(\?.*)?$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SMOKE_POSITIONS) });
    } else {
      route.continue();
    }
  });
  await page.route(/\/portfolio$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SMOKE_PORTFOLIO) });
    } else {
      route.continue();
    }
  });
  await page.route(/\/trade-plans(\?.*)?$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    } else {
      route.continue();
    }
  });
}

/** Mock POST /portfolio/size with a caller-supplied data payload. */
async function mockPortfolioSize(page, data) {
  await page.route(/\/portfolio\/size/, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data }),
    });
  });
}

async function fillSizingInputs(page, { ticker = 'MSFT', entry = '100.00', stop = '90.00' } = {}) {
  const tickerInput = page.getByPlaceholder('e.g., AAPL or VOD.L');
  await expect(tickerInput).toBeVisible({ timeout: 10000 });
  await tickerInput.fill(ticker);

  const entryPriceInput = page.getByPlaceholder('0.00').first();
  await entryPriceInput.fill(entry);

  const stopPriceInput = page.getByPlaceholder('0.00').last();
  await stopPriceInput.fill(stop);
}

test.describe('Position Sizing — Concentration Display (V-SIZE-01, V-SIZE-02)', () => {
  test('V-SIZE-01 — reduced size shows amber concentration reason beneath Suggested Shares', { tag: ['@smoke'] }, async ({ page }) => {
    await mockCommon(page);
    await mockPortfolioSize(page, {
      valid: true,
      suggested_shares: 10.0,
      risk_amount: 200.0,
      stop_distance: 10.0,
      estimated_cost: 1000.0,
      estimated_fees: 0.0,
      fx_rate_used: 1.0,
      cash_sufficient: true,
      available_cash: 20000.0,
      concentration_adjusted: true,
      concentration_reason: 'Reduced 50% — 2 open positions already in Technology (25.0% of portfolio heat).',
    });

    await page.goto('/#/TradeEntry');
    await fillSizingInputs(page);

    await page.waitForResponse(/\/portfolio\/size/, { timeout: 5000 });

    const reasonText = 'Reduced 50% — 2 open positions already in Technology (25.0% of portfolio heat).';
    await expect(page.getByText(reasonText)).toBeVisible({ timeout: 5000 });

    // Amber styling per decision_record.md §2 — not a StandingAlert, no dismiss affordance.
    // The text renders inside a <span> nested in the styled <p> — assert the class on the <p> ancestor.
    const reasonContainer = page.locator('p.text-amber-600', { hasText: reasonText });
    await expect(reasonContainer).toBeVisible();
    // AlertTriangle (lucide-react aliases to triangle-alert) renders beside the text.
    await expect(reasonContainer.locator('svg.lucide-triangle-alert')).toBeVisible();
  });

  test('V-SIZE-02 — no concentration issue: reason text is absent entirely', { tag: ['@smoke'] }, async ({ page }) => {
    await mockCommon(page);
    await mockPortfolioSize(page, {
      valid: true,
      suggested_shares: 20.0,
      risk_amount: 200.0,
      stop_distance: 10.0,
      estimated_cost: 2000.0,
      estimated_fees: 0.0,
      fx_rate_used: 1.0,
      cash_sufficient: true,
      available_cash: 20000.0,
      concentration_adjusted: false,
      concentration_reason: null,
    });

    await page.goto('/#/TradeEntry');
    await fillSizingInputs(page, { ticker: 'JNJ' });

    await page.waitForResponse(/\/portfolio\/size/, { timeout: 5000 });
    // Give the widget's render pass a moment to settle before asserting absence.
    await page.waitForTimeout(300);

    await expect(page.getByText(/open position.*already in/)).toHaveCount(0);
    await expect(page.locator('svg.lucide-triangle-alert')).toHaveCount(0);
  });

  test('V-SIZE-03 — flagged-not-reduced: amber note renders without a shares reduction', { tag: ['@smoke'] }, async ({ page }) => {
    await mockCommon(page);
    await mockPortfolioSize(page, {
      valid: true,
      suggested_shares: 20.0,
      risk_amount: 200.0,
      stop_distance: 10.0,
      estimated_cost: 2000.0,
      estimated_fees: 0.0,
      fx_rate_used: 1.0,
      cash_sufficient: true,
      available_cash: 20000.0,
      concentration_adjusted: false,
      concentration_reason: '2 open positions already in Technology (10.0% of portfolio heat) — approaching 30% concentration limit.',
    });

    await page.goto('/#/TradeEntry');
    await fillSizingInputs(page);

    await page.waitForResponse(/\/portfolio\/size/, { timeout: 5000 });

    const reason = page.getByText('2 open positions already in Technology (10.0% of portfolio heat) — approaching 30% concentration limit.');
    await expect(reason).toBeVisible({ timeout: 5000 });

    // Suggested Shares value itself is unchanged (20.0000) — this is a flag, not a reduction.
    await expect(page.getByText('20.0000')).toBeVisible();
  });
});
