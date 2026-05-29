/**
 * Reports Page — Performance Tab Playwright Tests
 * ST-16 (v2.6 EPIC-01 test gap closure)
 *
 * Covers the frontend behaviour introduced by EPIC-01 (ST-01):
 *   SC-REP-01: Performance tab renders summary stats from /analytics/metrics
 *   SC-REP-02: Period selector change re-fetches with correct backend period param
 *   SC-REP-03: Loading state shown while /analytics/metrics is in flight
 *   SC-REP-04: Zero/empty state rendered when analyticsData returns no trades
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports').
 * - api.analytics.metrics(period) → GET /analytics/metrics?period=<param>
 *   doFetch returns response.data; analyticsData = data object directly.
 * - Period selector maps: "month" → "last_month", "week" → "last_7_days", etc.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

/** Full analytics response with summary, executive_metrics, and trades_for_charts */
const ANALYTICS_FULL = {
  status: 'ok',
  data: {
    summary: {
      total_pnl: 1250.50,
      win_rate: 62.5,
      total_trades: 8,
      total_closed_trades: 8,
      total_gross_profit: 3200.00,
      total_gross_loss: 1949.50,
      total_realised_pnl: 1250.50,
    },
    executive_metrics: {
      profit_factor: 1.64,
    },
    trades_for_charts: [
      {
        id: 'rep-t1', ticker: 'LGEN', market: 'UK',
        entry_date: '2026-03-01', exit_date: '2026-03-15',
        pnl: 800.00, pnl_pct: 12.5, fees: 9.95, stop_price: 190.00,
      },
      {
        id: 'rep-t2', ticker: 'BARC', market: 'UK',
        entry_date: '2026-03-05', exit_date: '2026-03-20',
        pnl: -320.00, pnl_pct: -5.2, fees: 9.95, stop_price: 145.00,
      },
    ],
  },
};

/** Empty analytics response — no trades for the selected period */
const ANALYTICS_EMPTY = {
  status: 'ok',
  data: {
    summary: {
      total_pnl: 0,
      win_rate: 0,
      total_trades: 0,
      total_closed_trades: 0,
      total_gross_profit: 0,
      total_gross_loss: 0,
      total_realised_pnl: 0,
    },
    executive_metrics: {
      profit_factor: 0,
    },
    trades_for_charts: [],
  },
};

// ---------------------------------------------------------------------------
// Shared setup helpers
// ---------------------------------------------------------------------------

/**
 * Mock /analytics/metrics to return the given payload.
 * Matches both plain /analytics/metrics and /analytics/metrics?period=...
 */
async function mockAnalyticsMetrics(page, payload = ANALYTICS_FULL) {
  await page.route(/\/analytics\/metrics/, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    })
  );
}

/** Mock /positions to return an empty list (open positions count = 0) */
async function mockPositions(page, positions = []) {
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(positions),
    })
  );
}

/** Catch-all: prevent unmocked endpoints from hanging tests */
async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

// ---------------------------------------------------------------------------
// SC-REP-01 — Performance tab renders summary stats from /analytics/metrics
// ---------------------------------------------------------------------------

test.describe('SC-REP-01 — Performance tab summary stats', () => {
  test.beforeEach(async ({ page }) => {
    // Catch-all first — Playwright routes are LIFO, so registering catch-all first
    // ensures the specific mocks below take precedence.
    await mockFallback(page);
    await mockAnalyticsMetrics(page, ANALYTICS_FULL);
    await mockPositions(page, []);
    await page.goto('/#/Reports');
    // Wait for all API calls to settle before asserting
  });

  test('SC-REP-01a: Total P&L StatsCard renders value from analytics summary', async ({ page }) => {
    // metrics.totalPnL = analyticsData.summary.total_pnl = 1250.50
    // Rendered as "+£1,250.50"
    await expect(page.getByText(/\+£1,250\.50/)).toBeVisible({ timeout: 8000 });
  });

  test('SC-REP-01b: Win Rate StatsCard renders value from analytics summary', async ({ page }) => {
    // metrics.winRate = analyticsData.summary.win_rate = 62.5 → "62.5%"
    await expect(page.getByText('62.5%')).toBeVisible({ timeout: 8000 });
  });

  test('SC-REP-01c: Total Trades StatsCard renders value from analytics summary', async ({ page }) => {
    // metrics.totalTrades = analyticsData.summary.total_trades = 8
    // Use exact:true + first() to avoid strict-mode violation: getByText('8') does substring
    // matching and would also match chart axis labels like "08 Apr" or values like "£800".
    await expect(page.getByText('8', { exact: true }).first()).toBeVisible({ timeout: 8000 });
  });

  test('SC-REP-01d: Profit Factor StatsCard renders value from executive_metrics', async ({ page }) => {
    // metrics.profitFactor = analyticsData.executive_metrics.profit_factor = 1.64
    await expect(page.getByText('1.64')).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-REP-02 — Period selector triggers re-fetch with correct backend period param
// ---------------------------------------------------------------------------

test.describe('SC-REP-02 — Period selector maps to correct backend period param', () => {
  test('SC-REP-02a: Default period "month" fetches with period=last_month', async ({ page }) => {
    const requests = [];
    page.on('request', (req) => {
      if (req.url().includes('/analytics/metrics')) requests.push(req.url());
    });

    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await mockFallback(page);
    await mockAnalyticsMetrics(page, ANALYTICS_FULL);
    await mockPositions(page, []);
    await page.goto('/#/Reports');
    // Allow request to fire
    await page.waitForTimeout(500);

    const analyticsRequests = requests.filter(u => u.includes('/analytics/metrics'));
    expect(analyticsRequests.length).toBeGreaterThan(0);
    expect(analyticsRequests[0]).toContain('period=last_month');
  });

  test('SC-REP-02b: Selecting "Last 7 Days" re-fetches with period=last_7_days', async ({ page }) => {
    const requests = [];
    page.on('request', (req) => {
      if (req.url().includes('/analytics/metrics')) requests.push(req.url());
    });

    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await mockFallback(page);
    await mockAnalyticsMetrics(page, ANALYTICS_FULL);
    await mockPositions(page, []);
    await page.goto('/#/Reports');
    await page.waitForTimeout(300);

    // Clear captured requests to isolate the selector change
    requests.length = 0;

    // Open the period selector (Select component — click the trigger)
    const selectTrigger = page.locator('[role="combobox"]').first();
    await selectTrigger.click();
    await page.getByRole('option', { name: 'Last 7 Days' }).click();

    await page.waitForTimeout(500);

    const afterChange = requests.filter(u => u.includes('/analytics/metrics'));
    expect(afterChange.length).toBeGreaterThan(0);
    expect(afterChange[afterChange.length - 1]).toContain('period=last_7_days');
  });

  test('SC-REP-02c: Selecting "All Time" re-fetches with period=all_time', async ({ page }) => {
    const requests = [];
    page.on('request', (req) => {
      if (req.url().includes('/analytics/metrics')) requests.push(req.url());
    });

    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await mockFallback(page);
    await mockAnalyticsMetrics(page, ANALYTICS_FULL);
    await mockPositions(page, []);
    await page.goto('/#/Reports');
    await page.waitForTimeout(300);

    requests.length = 0;

    const selectTrigger = page.locator('[role="combobox"]').first();
    await selectTrigger.click();
    await page.getByRole('option', { name: 'All Time' }).click();

    await page.waitForTimeout(500);

    const afterChange = requests.filter(u => u.includes('/analytics/metrics'));
    expect(afterChange.length).toBeGreaterThan(0);
    expect(afterChange[afterChange.length - 1]).toContain('period=all_time');
  });
});

// ---------------------------------------------------------------------------
// SC-REP-03 — Loading state shown while /analytics/metrics is in-flight
// ---------------------------------------------------------------------------

test.describe('SC-REP-03 — Loading state during fetch', () => {
  test('SC-REP-03a: Loading spinner visible while /analytics/metrics is pending', async ({ page }) => {
    // Catch-all first — LIFO: checked last, so specific mocks below take precedence.
    await mockFallback(page);
    await mockPositions(page, []);
    // Delay the analytics response by 1 second to observe loading state.
    // Registered LAST so it takes precedence (LIFO) over the catch-all above.
    await page.route(/\/analytics\/metrics/, async (route) => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(ANALYTICS_FULL),
      });
    });
    await page.goto('/#/Reports');

    // Loading spinner should be visible before data arrives
    // The page renders <Loader2 className="animate-spin"> during isLoading
    await expect(page.locator('.animate-spin')).toBeVisible({ timeout: 3000 });

    // After load completes, stats should appear
    await expect(page.getByText(/\+£1,250\.50/)).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-REP-04 — Zero/empty state when no trades for selected period
// ---------------------------------------------------------------------------

test.describe('SC-REP-04 — Empty state (no trades for period)', () => {
  test.beforeEach(async ({ page }) => {
    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await mockFallback(page);
    await mockAnalyticsMetrics(page, ANALYTICS_EMPTY);
    await mockPositions(page, []);
    await page.goto('/#/Reports');
  });

  test('SC-REP-04a: Total P&L shows £0.00 when no trades', async ({ page }) => {
    // metrics.totalPnL = 0 → "+£0.00"
    await expect(page.getByText(/\+£0\.00/)).toBeVisible({ timeout: 8000 });
  });

  test('SC-REP-04b: Win Rate shows 0.0% when no trades', async ({ page }) => {
    await expect(page.getByText('0.0%')).toBeVisible({ timeout: 8000 });
  });

  test('SC-REP-04c: Profit Factor shows 0.00 when no trades', async ({ page }) => {
    // Scope to the Profit Factor card to avoid strict-mode violation: multiple StatsCards
    // show "0.00" when there are no trades. The value <p> is the immediate sibling of the
    // label <p>Profit Factor</p>, so use XPath following-sibling to target it precisely.
    const profitFactorLabel = page.locator('p').filter({ hasText: /^Profit Factor$/ });
    await expect(profitFactorLabel.locator('xpath=following-sibling::p[1]')).toHaveText('0.00', { timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// ST-18 — Strategy Compliance section in Monthly P&L tab (Arc 5, v4.3)
// SC-REP-05: Strategy Compliance section visible with metric fields
// ---------------------------------------------------------------------------

const MONTHLY_PNL_WITH_COMPLIANCE = {
  status: 'ok',
  data: [
    { year: 2026, month: 5, realised_pnl_gbp: 320.50, trade_count: 3 },
  ],
  strategy_compliance: {
    period_days: 30,
    validation_pass_rate: 0.82,
    override_count: 2,
    red_flag_events_count: 5,
    most_frequent_rule_breach: 'sector_concentration',
  },
};

test.describe('SC-REP-05: Monthly P&L — Strategy Compliance section', () => {
  test.beforeEach(async ({ page }) => {
    // Fallback registered FIRST (lowest priority — Playwright uses LIFO route evaluation).
    await page.route(new RegExp(`${API}/`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
    );
    // Specific mocks registered LAST (highest priority — override the fallback).
    await page.route(`${API}/analytics/metrics*`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
    );
    await page.route(`${API}/reports/monthly-pnl`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MONTHLY_PNL_WITH_COMPLIANCE) })
    );
    await page.goto('/#/Reports');
    // Navigate to Monthly P&L tab
    await page.getByRole('button', { name: /Monthly P&L/i }).click();
  });

  test('SC-REP-05a: Strategy Compliance heading visible in Monthly P&L tab', async ({ page }) => {
    await expect(page.getByTestId('strategy-compliance-section')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('Strategy Compliance')).toBeVisible({ timeout: 5000 });
  });

  test('SC-REP-05b: Validation Pass Rate and Override Count metric fields visible', async ({ page }) => {
    await expect(page.getByTestId('compliance-pass-rate')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('compliance-override-count')).toBeVisible({ timeout: 5000 });
  });
});
