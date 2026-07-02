/**
 * Trade History — AI Journal Summary Error States
 * TEST-GAP-EPIC-01 (v6.4, EPIC-03, ST-12)
 *
 * Covers observable UI error-state ACs introduced by v6.3 ST-01 that were
 * cleared by code review only (staging sign-off deferred — reproducibility
 * condition unmet; see verification_report.md §6, cycle 2026-06-26__release-v6.3,
 * TSG-v63-01) and had no prior Playwright coverage.
 *
 * Covers: SC-TH-AI-01, SC-TH-AI-02, SC-TH-AI-03
 *
 * Component: src/pages/TradeHistory.js — "AI Journal Summary" section
 * (data-testid="ai-journal-summary-section" and children, added in this story).
 *
 * ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/TradeHistory').
 * No live backend required — all API calls intercepted via page.route().
 */

'use strict';

const { test, expect } = require('@playwright/test');

// ---------------------------------------------------------------------------
// Seed data
// ---------------------------------------------------------------------------

const TRADE = {
  id: 'th-ai-t1',
  ticker: 'AAPL',
  market: 'US',
  entry_date: '2026-03-01',
  exit_date: '2026-03-15',
  entry_price: 200.0,
  exit_price: 220.0,
  shares: 10,
  pnl: 199.5,
  pnl_pct: 9.95,
  fee_drag_pct: null,
  slippage_pct: null,
  exit_reason: 'Target Reached',
  tags: [],
};

const TRADES_RESPONSE = {
  status: 'ok',
  trades: [TRADE],
  avg_fee_drag_pct: null,
  avg_slippage_pct: null,
  total_pnl: 199.5,
  total_trades: 1,
  win_rate: 100,
};

const ANALYTICS_STUB = { status: 'ok', data: { trades_for_charts: [] } };

// ---------------------------------------------------------------------------
// Shared mock setup
// ---------------------------------------------------------------------------

async function mockBaseEndpoints(page) {
  // Catch-all registered FIRST — Playwright routes are LIFO (last-registered
  // wins), so registering the catch-all first ensures specific mocks below
  // take precedence (same convention as fee-drag-trade-history.spec.js).
  await page.route(/\/analytics\//, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(/\/trades$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TRADES_RESPONSE) })
  );
  await page.route(/\/analytics\/metrics/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ANALYTICS_STUB) })
  );
}

async function openAiJournalSummary(page) {
  await page.goto('/#/TradeHistory');
  await page.waitForSelector('h1', { timeout: 10000 });
  await page.getByTestId('ai-journal-summary-toggle').click();
  await expect(page.getByTestId('ai-journal-summary-generate-btn')).toBeVisible({ timeout: 5000 });
}

// ---------------------------------------------------------------------------
// SC-TH-AI-01 — Server-error message on non-2xx response
// ---------------------------------------------------------------------------

test.describe('SC-TH-AI-01 — AI journal summary server-error state', () => {
  test('SC-TH-AI-01a: specific error message displayed when POST /ai/journal-summary returns non-2xx', async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.route(/\/ai\/journal-summary$/, (route) =>
      route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ detail: 'Internal error' }) })
    );

    await openAiJournalSummary(page);
    await page.getByTestId('ai-journal-summary-generate-btn').click();

    const errorEl = page.getByTestId('ai-journal-summary-error');
    await expect(errorEl).toBeVisible({ timeout: 8000 });
    await expect(errorEl).toHaveText('Journal summary request failed. Please try again.');
  });
});

// ---------------------------------------------------------------------------
// SC-TH-AI-02 — Network-error message on request failure (no response)
// ---------------------------------------------------------------------------

test.describe('SC-TH-AI-02 — AI journal summary network-error state', () => {
  test('SC-TH-AI-02a: network-error message displayed when POST /ai/journal-summary fails to reach the server', async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.route(/\/ai\/journal-summary$/, (route) => route.abort('failed'));

    await openAiJournalSummary(page);
    await page.getByTestId('ai-journal-summary-generate-btn').click();

    const errorEl = page.getByTestId('ai-journal-summary-error');
    await expect(errorEl).toBeVisible({ timeout: 8000 });
    await expect(errorEl).toHaveText('Unable to reach the server. Please check your connection.');
  });
});

// ---------------------------------------------------------------------------
// SC-TH-AI-03 — Success path renders the summary content (regression guard,
// ensures the error-state tests above are meaningfully distinct from success)
// ---------------------------------------------------------------------------

test.describe('SC-TH-AI-03 — AI journal summary success state', () => {
  test('SC-TH-AI-03a: summary content renders on a 200 response with a summary field', async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.route(/\/ai\/journal-summary$/, (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ summary: 'You tend to exit winners early on high-volatility days.' }),
      })
    );

    await openAiJournalSummary(page);
    await page.getByTestId('ai-journal-summary-generate-btn').click();

    const contentEl = page.getByTestId('ai-journal-summary-content');
    await expect(contentEl).toBeVisible({ timeout: 8000 });
    await expect(contentEl).toContainText('exit winners early');
    await expect(page.getByTestId('ai-journal-summary-error')).not.toBeVisible();
  });
});
