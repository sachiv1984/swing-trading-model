/**
 * Market Correlation Acceptance Tests — EPIC-01 (ST-01, v2.8)
 *
 * Covers AC-1 through AC-6 of MarketCorrelationSection (§18, analytics.md v1.7)
 * mapped to scenarios SC-CORR-FE-01 through SC-CORR-FE-06.
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
 */

'use strict';

const { test, expect } = require('@playwright/test');
const {
  CORRELATION_RESPONSE,
  CORRELATION_ERROR_RESPONSE,
  CORRELATION_EMPTY_RESPONSE,
} = require('./mocks/analytics-correlation-mock-data');

const API_BASE = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Shared setup helper
// ---------------------------------------------------------------------------

/**
 * Register all mocks needed for the Analytics page and navigate to it.
 *
 * Route registration order matters — Playwright uses LIFO matching, so the
 * catch-all is registered FIRST and specific overrides are registered AFTER.
 * The most-specific match registered last wins.
 */
async function setupAnalyticsPage(page, correlationPayload = CORRELATION_RESPONSE) {
  // Catch-all: prevents unmocked endpoints from hanging
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
      body: JSON.stringify({ status: 'ok', data: [] }),
    });
  });

  // /settings — required by PerformanceAnalytics on mount
  await page.route(`${API_BASE}/settings`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [{ min_trades_for_analytics: 10 }] }),
    });
  });

  // /analytics/market-correlation — the endpoint under test
  await page.route(`${API_BASE}/analytics/market-correlation`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(correlationPayload),
    });
  });

  await page.goto('/#/PerformanceAnalytics');

  // Wait for React to finish initial renders (spinner disappears)
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 15000 });
}

// ---------------------------------------------------------------------------
// SC-CORR-FE-01 — AC-1: Section renders on Analytics page
// ---------------------------------------------------------------------------

test('SC-CORR-FE-01: MarketCorrelationSection renders heading and subtitle', async ({ page }) => {
  await setupAnalyticsPage(page);

  // Panel heading as specified in §18
  await expect(page.getByText('Market Correlation')).toBeVisible({ timeout: 10000 });

  // Subtitle (descriptive copy confirming correct panel)
  await expect(
    page.getByText('Per-position Pearson correlation vs benchmark')
  ).toBeVisible({ timeout: 5000 });

  // Position rows are visible (LGEN, BARC, SHEL from mock)
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
//
// Playwright toHaveClass checks the class attribute of the element.
// We assert on the text colour token (most discriminating signal).
// ---------------------------------------------------------------------------

test('SC-CORR-FE-02: severity badges carry correct Tailwind colour tokens', async ({ page }) => {
  await setupAnalyticsPage(page);

  // Locate the "High" badge by its text content, then check parent span classes
  const highBadge = page.locator('span').filter({ hasText: /^High$/ }).first();
  await expect(highBadge).toBeVisible({ timeout: 10000 });
  await expect(highBadge).toHaveClass(/text-rose-400/);

  const moderateBadge = page.locator('span').filter({ hasText: /^Moderate$/ }).first();
  await expect(moderateBadge).toBeVisible({ timeout: 5000 });
  await expect(moderateBadge).toHaveClass(/text-amber-400/);

  const lowBadge = page.locator('span').filter({ hasText: /^Low$/ }).first();
  await expect(lowBadge).toBeVisible({ timeout: 5000 });
  await expect(lowBadge).toHaveClass(/text-emerald-400/);
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-03 — AC-3: Portfolio-level weighted average block renders
// ---------------------------------------------------------------------------

test('SC-CORR-FE-03: portfolio weighted average block renders with value and badge', async ({ page }) => {
  await setupAnalyticsPage(page);

  // Label text as rendered in the component
  await expect(
    page.getByText('Portfolio Weighted Average')
  ).toBeVisible({ timeout: 10000 });

  // Value from mock: portfolio_correlation.value = 0.52 → "0.52"
  await expect(page.getByText('0.52')).toBeVisible({ timeout: 5000 });

  // Badge for portfolio severity (moderate)
  // There are multiple "Moderate" badges (one portfolio + one BARC row);
  // the portfolio one is in the dedicated block — just verify at least one exists
  await expect(
    page.locator('span').filter({ hasText: /^Moderate$/ }).first()
  ).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-04 — AC-4: Null correlation renders "N/A" and sorts to bottom
//
// The component renders correlation=null as "N/A" in the Correlation column
// and a "—" placeholder in the Severity column (no badge).
// SEVERITY_ORDER maps null/unknown to 3 — always last in sortedCorrelations.
// ---------------------------------------------------------------------------

test('SC-CORR-FE-04: null correlation row renders "N/A", dash in severity, and sorts last', async ({ page }) => {
  await setupAnalyticsPage(page);

  // "N/A" must be visible for the null-correlation row
  await expect(page.getByText('N/A')).toBeVisible({ timeout: 10000 });

  // HSBA ticker must be present
  await expect(page.getByText('HSBA')).toBeVisible({ timeout: 5000 });

  // The null row must appear after the three rows with valid correlations.
  // Strategy: verify row order by checking each ticker's position in the DOM.
  const rows = page.locator('table tbody tr');
  const rowCount = await rows.count();
  expect(rowCount).toBe(4); // LGEN, BARC, SHEL, HSBA

  // Last row should be HSBA (null severity → sorts bottom)
  const lastRowText = await rows.last().textContent();
  expect(lastRowText).toContain('HSBA');
  expect(lastRowText).toContain('N/A');

  // No SeverityBadge for the null row — severity cell shows dash placeholder
  // (The component renders <span className="text-slate-500 text-xs">—</span>)
  const lastRowSeverityCell = rows.last().locator('td').nth(2);
  await expect(lastRowSeverityCell).not.toContainText('High');
  await expect(lastRowSeverityCell).not.toContainText('Moderate');
  await expect(lastRowSeverityCell).not.toContainText('Low');
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-05 — AC-5: Data sourced exclusively from GET /analytics/market-correlation
// ---------------------------------------------------------------------------

test('SC-CORR-FE-05: data loaded from GET /analytics/market-correlation', async ({ page }) => {
  let correlationCallCount = 0;

  // Catch-all first (LIFO — lowest priority)
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
      body: JSON.stringify({ status: 'ok', data: [] }),
    });
  });

  await page.route(`${API_BASE}/settings`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [{ min_trades_for_analytics: 10 }] }),
    });
  });

  // Count calls to the market-correlation endpoint
  await page.route(`${API_BASE}/analytics/market-correlation`, (route) => {
    correlationCallCount++;
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(CORRELATION_RESPONSE),
    });
  });

  await page.goto('/#/PerformanceAnalytics');
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 15000 });

  // Component must have called the endpoint at least once on mount
  expect(correlationCallCount).toBeGreaterThanOrEqual(1);

  // Data rendered in the table must match the mock payload — not fabricated
  await expect(page.getByText('LGEN').first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('0.85')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('0.18')).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-06 — AC-6: No regression to existing Analytics page sections
//
// Verifies that adding MarketCorrelationSection has not displaced or broken
// other established Analytics components. Checks for known headings from
// RMultipleAnalysis and WinRateByMonth (both present in PerformanceAnalytics).
// ---------------------------------------------------------------------------

test('SC-CORR-FE-06: existing Analytics sections still render after adding Market Correlation', async ({ page }) => {
  await setupAnalyticsPage(page);

  // Market Correlation section present (new §18)
  await expect(page.getByText('Market Correlation')).toBeVisible({ timeout: 10000 });

  // Existing sections from prior releases must still be present
  await expect(page.getByText('R-Multiple Analysis')).toBeVisible({ timeout: 10000 });
  await expect(page.getByText('Win Rate by Month')).toBeVisible({ timeout: 10000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-07 — Error state: section shows error message, not blank screen
// ---------------------------------------------------------------------------

test('SC-CORR-FE-07: error state renders graceful message when endpoint fails', async ({ page }) => {
  // Serve an error response for the correlation endpoint
  await setupAnalyticsPage(page, CORRELATION_ERROR_RESPONSE);

  // Component error state text (from MarketCorrelationSection render path)
  await expect(
    page.getByText('Unable to load correlation data. Please try again later.')
  ).toBeVisible({ timeout: 10000 });
});

// ---------------------------------------------------------------------------
// SC-CORR-FE-08 — Empty state: no positions shows appropriate message
// ---------------------------------------------------------------------------

test('SC-CORR-FE-08: empty state renders when no open positions', async ({ page }) => {
  await setupAnalyticsPage(page, CORRELATION_EMPTY_RESPONSE);

  await expect(
    page.getByText('No open positions to correlate.')
  ).toBeVisible({ timeout: 10000 });
});
