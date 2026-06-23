/**
 * Setup Quality Score — Playwright Tests
 * ST-09 (EPIC-04, v6.1): SetupQualityScorePanel
 *
 * Covers:
 *   SC-SQS-01: Score panel renders in Pre-Trade Research View
 *   SC-SQS-02: Score badge shows numeric value and qualitative label
 *   SC-SQS-03: Gate-not-met message renders when insufficient trade history
 *   SC-SQS-04: Expanded detail shows matching_trades, win_rate, average return
 *   SC-SQS-05: Score updates when ticker changes (no stale data)
 *   SC-SQS-06: Score panel renders in Trade Plan form when ticker is entered
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - HashRouter: navigate via page.goto('/#/Research/AAPL') or '/#/TradePlan?ticker=AAPL'.
 * - GET /trade-plans/setup-quality-score?ticker=AAPL → { status, data }
 * - LIFO ordering: catch-all registered FIRST so specific mocks take precedence.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

const SCORE_MET_AAPL = {
  status: 'ok',
  data: {
    gate_not_met: false,
    ticker: 'AAPL',
    score: 82,
    matching_trades: 25,
    win_rate: 72.0,
    average_pnl_pct: 4.5,
    score_explanation: 'Based on 25 closed trades.',
  },
};

const SCORE_MET_TSLA = {
  status: 'ok',
  data: {
    gate_not_met: false,
    ticker: 'TSLA',
    score: 45,
    matching_trades: 22,
    win_rate: 50.0,
    average_pnl_pct: 1.2,
    score_explanation: 'Based on 22 closed trades.',
  },
};

const SCORE_GATE_NOT_MET = {
  status: 'ok',
  data: {
    gate_not_met: true,
    min_trades_required: 20,
    current_trades: 12,
  },
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: {} }),
    })
  );
}

async function mockSetupQualityScore(page, ticker, payload) {
  await page.route(
    new RegExp(`${API}/trade-plans/setup-quality-score\\?ticker=${ticker}`),
    (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(payload),
      })
  );
}

async function mockResearchBase(page) {
  await page.route(`${API}/research/AAPL`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: { price: 182.5, price_change_pct: 0.015, signal: { status: 'active', signal_type: 'Breakout' } },
      }),
    })
  );
  await page.route(new RegExp(`${API}/trade-plans\\?ticker=AAPL`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

// ---------------------------------------------------------------------------
// SC-SQS-01 — Panel renders in Pre-Trade Research View
// ---------------------------------------------------------------------------

test.describe('SC-SQS-01 — Panel renders in Pre-Trade Research View', () => {
  test('SC-SQS-01a: setup-quality-score-panel is visible on Research page', async ({ page }) => {
    await mockFallback(page);
    await mockResearchBase(page);
    await mockSetupQualityScore(page, 'AAPL', SCORE_MET_AAPL);

    await page.goto('/#/Research/AAPL');
    await expect(page.getByTestId('setup-quality-score-panel')).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SQS-02 — Score badge shows numeric value and qualitative label
// ---------------------------------------------------------------------------

test.describe('SC-SQS-02 — Score badge with value and label', () => {
  test.beforeEach(async ({ page }) => {
    await mockFallback(page);
    await mockResearchBase(page);
    await mockSetupQualityScore(page, 'AAPL', SCORE_MET_AAPL);
    await page.goto('/#/Research/AAPL');
    await page.waitForSelector('[data-testid="setup-quality-score-value"]', { timeout: 8000 });
  });

  test('SC-SQS-02a: Numeric score is displayed', async ({ page }) => {
    await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82', { timeout: 8000 });
  });

  test('SC-SQS-02b: Qualitative label is displayed for score ≥ 80 (Excellent)', async ({ page }) => {
    await expect(page.getByTestId('setup-quality-score-label')).toHaveText('Excellent', { timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SQS-03 — Gate-not-met message renders
// ---------------------------------------------------------------------------

test.describe('SC-SQS-03 — Gate-not-met message', () => {
  test('SC-SQS-03a: Insufficient trade history message shown when gate not met', async ({ page }) => {
    await mockFallback(page);
    await mockResearchBase(page);
    await mockSetupQualityScore(page, 'AAPL', SCORE_GATE_NOT_MET);

    await page.goto('/#/Research/AAPL');
    await expect(page.getByTestId('setup-quality-gate-not-met')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('setup-quality-gate-not-met')).toContainText('Insufficient trade history', { timeout: 8000 });
  });

  test('SC-SQS-03b: Score badge is absent when gate not met', async ({ page }) => {
    await mockFallback(page);
    await mockResearchBase(page);
    await mockSetupQualityScore(page, 'AAPL', SCORE_GATE_NOT_MET);

    await page.goto('/#/Research/AAPL');
    await expect(page.getByTestId('setup-quality-gate-not-met')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('setup-quality-score-value')).not.toBeVisible({ timeout: 3000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SQS-04 — Expanded detail shows matching_trades, win_rate, average return
// ---------------------------------------------------------------------------

test.describe('SC-SQS-04 — Expanded detail view', () => {
  test('SC-SQS-04a: Expanding detail section shows matching_trades, win_rate, avg return', async ({ page }) => {
    await mockFallback(page);
    await mockResearchBase(page);
    await mockSetupQualityScore(page, 'AAPL', SCORE_MET_AAPL);

    await page.goto('/#/Research/AAPL');
    await page.waitForSelector('[data-testid="setup-quality-score-value"]', { timeout: 8000 });

    // Click expand button
    await page.locator('[data-testid="setup-quality-score-panel"] button[aria-label="Expand details"]').click();

    const detail = page.getByTestId('setup-quality-score-detail');
    await expect(detail).toBeVisible({ timeout: 5000 });

    // Verify detail values
    await expect(detail).toContainText('25', { timeout: 5000 }); // matching_trades
    await expect(detail).toContainText('72%', { timeout: 5000 }); // win_rate
    await expect(detail).toContainText('4.5%', { timeout: 5000 }); // average_pnl_pct
  });
});

// ---------------------------------------------------------------------------
// SC-SQS-05 — Score updates when ticker changes
// ---------------------------------------------------------------------------

test.describe('SC-SQS-05 — Score updates on ticker change', () => {
  test('SC-SQS-05a: Navigating to a different ticker shows updated score', async ({ page }) => {
    // Setup AAPL mock
    await mockFallback(page);
    await mockResearchBase(page);
    await mockSetupQualityScore(page, 'AAPL', SCORE_MET_AAPL);

    // Setup TSLA mocks
    await page.route(`${API}/research/TSLA`, (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: { price: 248.0, price_change_pct: -0.02, signal: { status: 'watch' } },
        }),
      })
    );
    await page.route(new RegExp(`${API}/trade-plans\\?ticker=TSLA`), (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: [] }),
      })
    );
    await mockSetupQualityScore(page, 'TSLA', SCORE_MET_TSLA);

    await page.goto('/#/Research/AAPL');
    await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82', { timeout: 8000 });

    await page.goto('/#/Research/TSLA');
    await expect(page.getByTestId('setup-quality-score-value')).toHaveText('45', { timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SQS-06 — Panel renders in Trade Plan form
// ---------------------------------------------------------------------------

test.describe('SC-SQS-06 — Panel renders in Trade Plan form', () => {
  test('SC-SQS-06a: setup-quality-score-panel appears in Trade Plan form when ticker is set', async ({ page }) => {
    await mockFallback(page);
    await mockSetupQualityScore(page, 'AAPL', SCORE_MET_AAPL);

    await page.goto('/#/TradePlan?ticker=AAPL');
    await expect(page.getByTestId('setup-quality-score-panel')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SQS-06b: Panel shows score value in Trade Plan form', async ({ page }) => {
    await mockFallback(page);
    await mockSetupQualityScore(page, 'AAPL', SCORE_MET_AAPL);

    await page.goto('/#/TradePlan?ticker=AAPL');
    await expect(page.getByTestId('setup-quality-score-value')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82', { timeout: 8000 });
  });
});
