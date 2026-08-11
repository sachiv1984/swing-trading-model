/**
 * TradePlanCompletionRateSection — Playwright Acceptance Tests
 * ST-01 (EPIC-01, v8.6) — BLG-FEAT-32
 *
 * Covers observable ACs for the Trade Plan Completion Rate section on the
 * Performance Analytics page (analytics.md §21):
 *
 *   SC-TPCR-01  Heading "Trade Plan Completion Rate" is visible
 *   SC-TPCR-02  Three summary cards visible when data is loaded: "Plans
 *               Created", "Completion Rate", "Plans Abandoned"
 *   SC-TPCR-03  Loading skeleton shown when data is pending
 *   SC-TPCR-04  Empty state ("No trade plans created yet.") shown when
 *               plans_created is 0 — not a 0% completion rate
 *   SC-TPCR-05  Error state shown when the API call fails
 *   SC-TPCR-06  Summary line "{plans_completed} of {plans_created} plans
 *               completed" renders with correct values
 *   SC-TPCR-07  Completion rate colour convention (green >=60%, amber
 *               40-59%, red <40%) mirrors §13 Win Rate Consistency
 *
 * Spec ref: docs/specs/frontend/pages/analytics.md §21
 * Design source: docs/design/2026-08-11__release-v8.6/trade-plan-completion-rate-metric/decision_record.md
 * API contract: docs/specs/api_contracts/analytics_endpoints.md
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

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock payloads
// ---------------------------------------------------------------------------

const COMPLETION_RATE_OK = {
  status: 'ok',
  data: { plans_created: 24, plans_completed: 15, plans_abandoned: 4, completion_rate: 62.5 },
};

const COMPLETION_RATE_AMBER = {
  status: 'ok',
  data: { plans_created: 10, plans_completed: 5, plans_abandoned: 1, completion_rate: 50.0 },
};

const COMPLETION_RATE_RED = {
  status: 'ok',
  data: { plans_created: 10, plans_completed: 3, plans_abandoned: 5, completion_rate: 30.0 },
};

const COMPLETION_RATE_EMPTY = {
  status: 'ok',
  data: { plans_created: 0, plans_completed: 0, plans_abandoned: 0, completion_rate: null },
};

const COMPLETION_RATE_ERROR = {
  status: 'error',
  detail: 'Internal server error',
};

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

/**
 * PerformanceAnalytics gates all sections behind a minimum-trades check
 * (settingsData.min_trades_for_analytics, default 10). Without at least 10
 * closed trades in the selected period, the page shows "Not enough trades"
 * and none of the analytics sections (including TradePlanCompletionRateSection)
 * render at all. Same helper as arc5-compliance-section.spec.js.
 */
function buildMockTrades(count = 12) {
  const now = new Date();
  return Array.from({ length: count }, (_, i) => ({
    id: `trade-${i}`,
    ticker: 'AAPL',
    market: 'US',
    entry_date: new Date(now.getTime() - (i + 5) * 86400000).toISOString(),
    exit_date: new Date(now.getTime() - i * 86400000).toISOString(),
    entry_price: 100,
    exit_price: 105,
    pnl: 50,
    shares: 10,
  }));
}

/** Mock all API calls not explicitly set to return empty 200s to prevent hangs. */
async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route(new RegExp(`${API}/trades$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: buildMockTrades() }) })
  );
}

/** Mock GET /analytics/trade-plan-completion-rate with the given payload and status. */
async function mockCompletionRate(page, payload = COMPLETION_RATE_OK, status = 200) {
  await page.route(new RegExp(`${API}/analytics/trade-plan-completion-rate`), (route) =>
    route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

/** Navigate to the Performance Analytics page and wait for it to mount. */
async function gotoAnalytics(page) {
  await page.goto('/#/PerformanceAnalytics');
  await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-TPCR-01 — Heading visible
// ---------------------------------------------------------------------------

test.describe('SC-TPCR-01 — Trade Plan Completion Rate heading', () => {
  test('SC-TPCR-01: Heading "Trade Plan Completion Rate" is visible on the analytics page', async ({ page }) => {
    await mockFallback(page);
    await mockCompletionRate(page, COMPLETION_RATE_OK);
    await gotoAnalytics(page);

    await expect(page.getByText('Trade Plan Completion Rate')).toBeVisible({ timeout: 10000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TPCR-02 — Three summary cards visible
// ---------------------------------------------------------------------------

test.describe('SC-TPCR-02 — Three summary cards', () => {
  test('SC-TPCR-02: All three summary card titles are visible when data is loaded', async ({ page }) => {
    await mockFallback(page);
    await mockCompletionRate(page, COMPLETION_RATE_OK);
    await gotoAnalytics(page);

    await expect(page.getByText('Trade Plan Completion Rate')).toBeVisible({ timeout: 10000 });

    await expect(page.getByText('Plans Created')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Completion Rate')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Plans Abandoned')).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TPCR-03 — Loading skeleton shown while pending
// ---------------------------------------------------------------------------

test.describe('SC-TPCR-03 — Loading skeleton state', () => {
  test('SC-TPCR-03: Loading skeleton shown while completion-rate data is pending', async ({ page }) => {
    let resolveRoute;
    const routePromise = new Promise((resolve) => { resolveRoute = resolve; });

    // mockFallback must be registered FIRST: Playwright evaluates page.route()
    // handlers in reverse registration order (most-recently-registered first).
    await mockFallback(page);

    await page.route(new RegExp(`${API}/analytics/trade-plan-completion-rate`), async (route) => {
      await routePromise;
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(COMPLETION_RATE_OK) });
    });

    await gotoAnalytics(page);

    await expect(page.getByText('Trade Plan Completion Rate')).toBeVisible({ timeout: 10000 });

    const skeletons = page.locator('.animate-pulse');
    await expect(skeletons.first()).toBeVisible({ timeout: 5000 });

    resolveRoute();
  });
});

// ---------------------------------------------------------------------------
// SC-TPCR-04 — Empty state when plans_created is 0
// ---------------------------------------------------------------------------

test.describe('SC-TPCR-04 — Empty state', () => {
  test('SC-TPCR-04: "No trade plans created yet." shown when plans_created is 0, not a 0% rate', async ({ page }) => {
    await mockFallback(page);
    await mockCompletionRate(page, COMPLETION_RATE_EMPTY);
    await gotoAnalytics(page);

    await expect(page.getByText('Trade Plan Completion Rate')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('No trade plans created yet.')).toBeVisible({ timeout: 8000 });

    // Must not render the summary cards or a misleading 0% in the empty state.
    await expect(page.getByText('Plans Created')).not.toBeVisible();
    await expect(page.getByText('0.0%')).not.toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// SC-TPCR-05 — Error state
// ---------------------------------------------------------------------------

test.describe('SC-TPCR-05 — Error state', () => {
  test('SC-TPCR-05: Error card with retry shown when API returns error', async ({ page }) => {
    await mockFallback(page);
    await mockCompletionRate(page, COMPLETION_RATE_ERROR, 500);
    await gotoAnalytics(page);

    await expect(page.getByText('Trade Plan Completion Rate')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Something went wrong')).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TPCR-06 — Summary line
// ---------------------------------------------------------------------------

test.describe('SC-TPCR-06 — Summary line', () => {
  test('SC-TPCR-06: "15 of 24 plans completed" summary line renders', async ({ page }) => {
    await mockFallback(page);
    await mockCompletionRate(page, COMPLETION_RATE_OK);
    await gotoAnalytics(page);

    await expect(page.getByText('Trade Plan Completion Rate')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('15 of 24 plans completed')).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TPCR-07 — Completion rate colour convention
// ---------------------------------------------------------------------------

test.describe('SC-TPCR-07 — Completion rate colour convention', () => {
  test('SC-TPCR-07a: Rate >=60% renders in the green (emerald) colour class', async ({ page }) => {
    await mockFallback(page);
    await mockCompletionRate(page, COMPLETION_RATE_OK); // 62.5%
    await gotoAnalytics(page);

    const rate = page.getByText('62.5%');
    await expect(rate).toBeVisible({ timeout: 8000 });
    await expect(rate).toHaveClass(/text-emerald-400/);
  });

  test('SC-TPCR-07b: Rate 40-59% renders in the amber colour class', async ({ page }) => {
    await mockFallback(page);
    await mockCompletionRate(page, COMPLETION_RATE_AMBER); // 50.0%
    await gotoAnalytics(page);

    const rate = page.getByText('50.0%');
    await expect(rate).toBeVisible({ timeout: 8000 });
    await expect(rate).toHaveClass(/text-amber-400/);
  });

  test('SC-TPCR-07c: Rate <40% renders in the red (rose) colour class', async ({ page }) => {
    await mockFallback(page);
    await mockCompletionRate(page, COMPLETION_RATE_RED); // 30.0%
    await gotoAnalytics(page);

    const rate = page.getByText('30.0%');
    await expect(rate).toBeVisible({ timeout: 8000 });
    await expect(rate).toHaveClass(/text-rose-400/);
  });
});
