/**
 * Metrics Staleness Indicator — Acceptance Tests
 * ST-02 (BLG-FEAT-09, v2.3)
 * Covers: SC-STALE-01 through SC-STALE-05
 *
 * Spec refs:
 *   docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md
 *   docs/specs/frontend/pages/analytics.md §Metrics Staleness Indicator
 *
 * What these tests cover (non-visual AC only):
 *   SC-STALE-01  Analytics page: fresh indicator present and stale badge absent
 *   SC-STALE-02  Analytics page: stale badge present when last_sync_at ≥ 4h ago
 *   SC-STALE-03  Analytics page: indicator hidden when last_sync_at is null
 *   SC-STALE-04  Positions page: fresh indicator present
 *   SC-STALE-05  Hover tooltip shows absolute UTC timestamp in both pages
 *
 * What requires DoQ manual visual verification (not covered here):
 *   - Actual colour rendering: grey for fresh, amber for stale
 *   - ⚠ icon renders correctly in stale badge
 *   - Tooltip dark background, readable text
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');
const {
  ANALYTICS_FRESH,
  ANALYTICS_STALE,
  ANALYTICS_NO_SYNC_AT,
  ANALYTICS_FIXED_TS,
  FIXED_SYNC_AT,
  TEN_TRADES,
  SETTINGS_DEFAULT,
  COHORT_EMPTY,
  R_MULTIPLE_EMPTY,
  COMPLIANCE_EMPTY,
  POSITIONS_EMPTY,
} = require('./mocks/staleness-mock-data');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Shared mock helpers
// ---------------------------------------------------------------------------

/**
 * Mock GET /analytics/metrics with a controlled response.
 * The MetricsStalenessIndicator fetches this endpoint directly.
 * Route regex matches both plain /analytics/metrics and /analytics/metrics?period=...
 */
async function mockAnalyticsMetrics(page, payload) {
  await page.route(/\/analytics\/metrics(\?|$)/, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    });
  });
}

/** Mock GET /trades — provides enough trades for the analytics page main render path. */
async function mockTrades(page, payload = TEN_TRADES) {
  await page.route(/\/trades(\?|$)/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(payload),
      });
    } else {
      route.continue();
    }
  });
}

/** Mock GET /settings. */
async function mockSettings(page) {
  await page.route(/\/settings(\?|$)/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SETTINGS_DEFAULT),
      });
    } else {
      route.continue();
    }
  });
}

/** Mock analytics sub-endpoints used by CohortAnalysis, RMultipleDistribution, DisciplineComplianceSection. */
async function mockAnalyticsSubEndpoints(page) {
  await page.route(/\/analytics\/cohort/, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(COHORT_EMPTY) });
  });
  await page.route(/\/analytics\/r-multiple-distribution/, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(R_MULTIPLE_EMPTY) });
  });
  await page.route(/\/analytics\/compliance-metrics/, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(COMPLIANCE_EMPTY) });
  });
}

/** Mock GET /positions — used by Positions page. Returns empty array to avoid entity fetch errors. */
async function mockPositions(page) {
  await page.route(/\/positions(\?|$)/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(POSITIONS_EMPTY),
      });
    } else {
      route.continue();
    }
  });
}

/** Set up all mocks needed for the PerformanceAnalytics page to reach the main render path. */
async function setupAnalyticsPage(page, metricsPayload) {
  await mockAnalyticsMetrics(page, metricsPayload);
  await mockTrades(page);
  await mockSettings(page);
  await mockAnalyticsSubEndpoints(page);
}

/** Set up all mocks needed for the Positions page. */
async function setupPositionsPage(page, metricsPayload) {
  await mockAnalyticsMetrics(page, metricsPayload);
  await mockPositions(page);
}

// ---------------------------------------------------------------------------
// SC-STALE-01 — Analytics page: fresh indicator present, stale badge absent
// ---------------------------------------------------------------------------

test('SC-STALE-01: analytics page shows fresh staleness indicator when data is recent', async ({ page }) => {
  await setupAnalyticsPage(page, ANALYTICS_FRESH);

  await page.goto('/#/PerformanceAnalytics');
  await page.waitForLoadState('networkidle');

  // Fresh indicator present: "Data as of N mins ago" (no "may be outdated")
  const freshIndicator = page.getByText(/Data as of/i).first();
  await expect(freshIndicator).toBeVisible({ timeout: 5000 });

  // Stale badge absent
  await expect(page.getByText(/may be outdated/i)).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-STALE-02 — Analytics page: stale badge present when data is ≥ 4h old
// ---------------------------------------------------------------------------

test('SC-STALE-02: analytics page shows stale badge when last_sync_at is 5 hours ago', async ({ page }) => {
  await setupAnalyticsPage(page, ANALYTICS_STALE);

  await page.goto('/#/PerformanceAnalytics');
  await page.waitForLoadState('networkidle');

  // Stale badge visible: "⚠ Data as of Nh ago — may be outdated"
  const staleBadge = page.getByText(/may be outdated/i).first();
  await expect(staleBadge).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-STALE-03 — Analytics page: indicator hidden when last_sync_at is null
// ---------------------------------------------------------------------------

test('SC-STALE-03: analytics page hides indicator when last_sync_at is null', async ({ page }) => {
  await setupAnalyticsPage(page, ANALYTICS_NO_SYNC_AT);

  await page.goto('/#/PerformanceAnalytics');
  await page.waitForLoadState('networkidle');

  // Indicator must not appear at all
  await expect(page.getByText(/Data as of/i)).not.toBeVisible({ timeout: 5000 });
  await expect(page.getByText(/may be outdated/i)).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-STALE-04 — Positions page: fresh indicator present
// ---------------------------------------------------------------------------

test('SC-STALE-04: positions page shows staleness indicator', async ({ page }) => {
  await setupPositionsPage(page, ANALYTICS_FRESH);

  await page.goto('/#/Positions');
  await page.waitForLoadState('networkidle');

  // Fresh indicator visible on positions page
  const freshIndicator = page.getByText(/Data as of/i).first();
  await expect(freshIndicator).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-STALE-05 — Hover tooltip shows absolute UTC timestamp
// ---------------------------------------------------------------------------

test('SC-STALE-05: hover tooltip shows absolute UTC timestamp', async ({ page }) => {
  await setupAnalyticsPage(page, ANALYTICS_FIXED_TS);

  await page.goto('/#/PerformanceAnalytics');
  await page.waitForLoadState('networkidle');

  // Wait for indicator to appear
  const indicator = page.getByText(/Data as of/i).first();
  await expect(indicator).toBeVisible({ timeout: 5000 });

  // Hover over the indicator to trigger tooltip
  await indicator.hover();

  // Tooltip must contain the absolute timestamp
  // FIXED_SYNC_AT = '2026-03-29T09:41:00.000000+00:00' → "Updated: 2026-03-29 09:41 UTC"
  const tooltip = page.getByText(/Updated: 2026-03-29 09:41 UTC/i);
  await expect(tooltip).toBeVisible({ timeout: 3000 });
});
