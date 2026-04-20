/**
 * Market Correlation Acceptance Tests — EPIC-01 (ST-01, v2.8)
 *
 * Covers AC-1 through AC-6 of MarketCorrelationSection (§18, analytics.md v1.7)
 * mapped to scenarios SC-CORR-FE-01 through SC-CORR-FE-08.
 * Spec: docs/testing/analytics_scenarios.md §4 (SC-CORR-01–04)
 *       docs/specs/frontend/pages/analytics.md §18
 *
 * ── AC coverage ──────────────────────────────────────────────────────────────
 *   AC-1  Section renders on Analytics page (heading + subtitle)
 *   AC-2  Severity badge Tailwind colour tokens (text-rose-400 / text-amber-400 / text-emerald-400)
 *   AC-3  Portfolio-level weighted average block renders with value + badge
 *   AC-4  Null correlation renders "N/A" and sorts below all non-null rows
 *   AC-5  Data sourced exclusively from GET /analytics/market-correlation
 *   AC-6  No regression — existing Analytics page sections still render
 *
 * ── Scope constraints ────────────────────────────────────────────────────────
 *   - Playwright PASS is primary evidence for non-visual AC.
 *   - Visual AC (exact colour rendering in browser) remain DoQ manual review.
 *   - Flaky failures are advisory — MUST NOT block the PR.
 *   - This suite does NOT replace DoQ human sign-off.
 *
 * ── Infrastructure ────────────────────────────────────────────────────────────
 *   - Playwright page.route() network interception. No live backend required.
 *   - ROUTING NOTE: App uses HashRouter. ALL navigation must use
 *     page.goto('/#/PageKey') — NOT page.goto('/path'). Path-based navigation
 *     silently loads the Dashboard without a 404. This comment must be
 *     preserved in all future Playwright spec files.
 *   - Run time target: < 5 minutes.
 *
 * ── Data access note ─────────────────────────────────────────────────────────
 *   doFetch (base44Client.js line 73-74) unwraps the {status, data} envelope,
 *   returning json.data directly. MarketCorrelationSection therefore receives
 *   data = { correlations, portfolio_correlation } — not data.data.*.
 *   The component uses data?.correlations (post-fix). Mocks return the full
 *   HTTP envelope; doFetch unwrapping is transparent to Playwright.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const {
  CORRELATION_RESPONSE,
  CORRELATION_ERROR_RESPONSE,
  CORRELATION_EMPTY_RESPONSE,
} = require('./mocks/analytics-correlation-mock-data');

const API_BASE = 'http://localhost:8000';
const CORR_URL = `${API_BASE}/analytics/market-correlation`;

// ---------------------------------------------------------------------------
// Shared setup helper
// ---------------------------------------------------------------------------

/**
 * Register all mocks, navigate, and wait for the market-correlation response.
 *
 * Route registration order: catch-all FIRST (lowest LIFO priority), specific
 * mocks LAST (highest priority). The most-recently-registered route wins.
 *
 * Explicit waitForResponse on /analytics/market-correlation is used rather
 * than relying on the animate-spin heuristic alone, because the spinner may
 * briefly read zero before MarketCorrelationSection mounts.
 */
async function setupAnalyticsPage(page, correlationPayload = CORRELATION_RESPONSE) {
  // Catch-all: prevents unmocked endpoints from hanging (lowest priority)
  await page.route(new RegExp(`${API_BASE}/`), (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    });
  });

  // /trades — required by PerformanceAnalytics data pipeline
  await page.route(`${API_BASE}/trades`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ trades: [] }),
    });
  });

  // /settings — min_trades_for_analytics:0 so hasEnoughTrades gate passes
  // with an empty trades list (avoids the "need N closed trades" early-return).
  await page.route(`${API_BASE}/settings`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [{ min_trades_for_analytics: 0 }] }),
    });
  });

  // /analytics/market-correlation — the endpoint under test (highest priority)
  await page.route(CORR_URL, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(correlationPayload),
    });
  });

  // Start waiting for the correlation response BEFORE navigation to avoid races
  const corrResponsePromise = page.waitForResponse(
    (resp) => resp.url().includes('/analytics/market-correlation'),
    { timeout: 15000 }
  );

  await page.goto('/#/PerformanceAnalytics');

  // Wait for the correlation endpoint to have responded
  await corrResponsePromise;

  // Wait for all loading spinners to clear (including MarketCorrelationSection's)
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-CORR-FE-01 — AC-1: Section renders on Analytics page
// ---------------------------------------------------------------------------

test('SC-CORR-FE-01: MarketCorrelationSection renders heading and subtitle', async ({ page }) => {
  await setupAnalyticsPage(page);

  // Panel heading as specified in §18
  await expect(
    page.locator('h3').filter({ hasText: 'Market Correlation' })
  ).toBeVisible({ timeout: 5000 });

  // Subtitle
  await expect(
    page.getByText('Per-position Pearson correlation vs benchmark')
  ).toBeVisible({ timeout: 5000 });

  // Position rows from mock data
  await expect(page.getByText('LGEN').first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('BARC').first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('SHEL').first()).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-02 — AC-2: Severity badge colour tokens
//
// SeverityBadge applies Tailwind classes from SEVERITY_STYLES:
//   high:     bg-rose-500/20  text-rose-400  border-rose-500/30
//   moderate: bg-amber-500/20 text-amber-400 border-amber-500/30
//   low:      bg-emerald-500/20 text-emerald-400 border-emerald-500/30
// ---------------------------------------------------------------------------

test('SC-CORR-FE-02: severity badges carry correct Tailwind colour tokens', async ({ page }) => {
  await setupAnalyticsPage(page);

  // Scope to the correlation table to avoid matching badges in other components
  const corrTable = page.locator('table').filter({ has: page.locator('td').filter({ hasText: 'LGEN' }) });

  const highBadge = corrTable.locator('span').filter({ hasText: /^High$/ });
  await expect(highBadge).toBeVisible({ timeout: 5000 });
  await expect(highBadge).toHaveClass(/text-rose-400/);

  const moderateBadge = corrTable.locator('span').filter({ hasText: /^Moderate$/ }).first();
  await expect(moderateBadge).toBeVisible({ timeout: 5000 });
  await expect(moderateBadge).toHaveClass(/text-amber-400/);

  const lowBadge = corrTable.locator('span').filter({ hasText: /^Low$/ });
  await expect(lowBadge).toBeVisible({ timeout: 5000 });
  await expect(lowBadge).toHaveClass(/text-emerald-400/);
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-03 — AC-3: Portfolio-level weighted average block renders
// ---------------------------------------------------------------------------

test('SC-CORR-FE-03: portfolio weighted average block renders with value and badge', async ({ page }) => {
  await setupAnalyticsPage(page);

  await expect(
    page.getByText('Portfolio Weighted Average')
  ).toBeVisible({ timeout: 5000 });

  // Value from mock: portfolio_correlation.value = 0.52 → "0.52"
  // Scope to the portfolio block to avoid collision with the BARC row (also 0.52)
  const portfolioBlock = page.locator('p').filter({ hasText: 'Portfolio Weighted Average' }).locator('..');
  await expect(portfolioBlock.getByText('0.52')).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-04 — AC-4: Null correlation renders "N/A" and sorts last
// ---------------------------------------------------------------------------

test('SC-CORR-FE-04: null correlation row renders "N/A", dash in severity, and sorts last', async ({ page }) => {
  await setupAnalyticsPage(page);

  // Scope all assertions to the correlation table to avoid matching N/A in
  // other Analytics components (there can be multiple N/A values on the page).
  const corrTable = page.locator('table').filter({
    has: page.locator('td').filter({ hasText: 'LGEN' }),
  });

  // HSBA row must be present with N/A correlation
  const hsbaRow = corrTable.locator('tr').filter({ hasText: 'HSBA' });
  await expect(hsbaRow).toBeVisible({ timeout: 5000 });
  await expect(hsbaRow.getByText('N/A')).toBeVisible({ timeout: 5000 });

  // The null row must appear last (4 rows total, HSBA is last)
  const rows = corrTable.locator('tbody tr');
  await expect(rows).toHaveCount(4, { timeout: 5000 });
  const lastRowText = await rows.last().textContent();
  expect(lastRowText).toContain('HSBA');
  expect(lastRowText).toContain('N/A');

  // No SeverityBadge for null row — severity cell shows a dash, not a badge
  const lastRowSeverityCell = rows.last().locator('td').nth(2);
  await expect(lastRowSeverityCell).not.toContainText('High');
  await expect(lastRowSeverityCell).not.toContainText('Moderate');
  await expect(lastRowSeverityCell).not.toContainText('Low');
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-05 — AC-5: Data sourced from GET /analytics/market-correlation
// ---------------------------------------------------------------------------

test('SC-CORR-FE-05: data loaded from GET /analytics/market-correlation', async ({ page }) => {
  let correlationCallCount = 0;

  await page.route(new RegExp(`${API_BASE}/`), (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    });
  });

  await page.route(`${API_BASE}/trades`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ trades: [] }),
    });
  });

  await page.route(`${API_BASE}/settings`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [{ min_trades_for_analytics: 0 }] }),
    });
  });

  await page.route(CORR_URL, (route) => {
    correlationCallCount++;
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(CORRELATION_RESPONSE),
    });
  });

  const corrResponsePromise = page.waitForResponse(
    (resp) => resp.url().includes('/analytics/market-correlation'),
    { timeout: 15000 }
  );

  await page.goto('/#/PerformanceAnalytics');
  await corrResponsePromise;
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 10000 });

  // Endpoint must have been called at least once on mount
  expect(correlationCallCount).toBeGreaterThanOrEqual(1);

  // Values in table must match the mock payload exactly
  await expect(page.getByText('LGEN').first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('0.85')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('0.18')).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-06 — AC-6: No regression to existing Analytics page sections
//
// Checks that adding MarketCorrelationSection has not displaced or broken
// RMultipleAnalysis (confirmed to render without trade data).
// WinRateByMonth is excluded — it returns null when monthlyData is empty.
// ---------------------------------------------------------------------------

test('SC-CORR-FE-06: existing Analytics sections still render after adding Market Correlation', async ({ page }) => {
  await setupAnalyticsPage(page);

  // Market Correlation section present (new §18)
  await expect(
    page.locator('h3').filter({ hasText: 'Market Correlation' })
  ).toBeVisible({ timeout: 5000 });

  // R-Multiple Analysis section still present (renders without trade data)
  await expect(
    page.locator('h3').filter({ hasText: 'R-Multiple Analysis' })
  ).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-07 — Error state: section shows error message, not blank screen
// ---------------------------------------------------------------------------

test('SC-CORR-FE-07: error state renders graceful message when endpoint fails', async ({ page }) => {
  // CORRELATION_ERROR_RESPONSE has status:'error' — doFetch throws, useQuery
  // sets error, component renders the error message branch.
  await setupAnalyticsPage(page, CORRELATION_ERROR_RESPONSE);

  await expect(
    page.getByText('Unable to load correlation data. Please try again later.')
  ).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-08 — Empty state: no positions shows appropriate message
// ---------------------------------------------------------------------------

test('SC-CORR-FE-08: empty state renders when no open positions', async ({ page }) => {
  await setupAnalyticsPage(page, CORRELATION_EMPTY_RESPONSE);

  await expect(
    page.getByText('No open positions to correlate.')
  ).toBeVisible({ timeout: 5000 });
});
