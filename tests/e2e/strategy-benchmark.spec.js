/**
 * Strategy Benchmark Page — Scenario Coverage
 * TEST-GAP-EPIC-03 (v6.4, EPIC-03, ST-13); Panel 0 gap closed by
 * TEST-GAP-EPIC-03-v64 (v6.5, EPIC-02, ST-05).
 *
 * v6.3 ST-11 shipped the Strategy Benchmark page with test_scenarios: "pending"
 * (per LL-v2.0-P4-2) — zero Playwright coverage for its 3 panels, sticky
 * filters, toggle modes, and exit reason badges. See verification_report.md §6
 * (cycle 2026-06-26__release-v6.3, TSG-v63-02).
 *
 * Panel 0 (Open Positions, v6.4 EPIC-03 BLG-FEAT-54) was deferred to this
 * sprint per the v6.4 QA evidence log (code review only, backlog item filed).
 * Covered here: conditional rendering (SC-SB-05), Market-filter-only
 * interaction with no Year dependency (SC-SB-06), and the API-error state
 * (SC-SB-07). See docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md.
 *
 * Covers: SC-SB-01, SC-SB-02, SC-SB-03, SC-SB-04, SC-SB-05, SC-SB-06, SC-SB-07
 *
 * Component: src/pages/StrategyBenchmark.js
 * ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/StrategyBenchmark')
 * or via the sidebar nav link (SC-SB-01).
 */

'use strict';

const { test, expect } = require('@playwright/test');

// ---------------------------------------------------------------------------
// Seed data
// ---------------------------------------------------------------------------

const SUMMARY_WITH_ACTUAL = {
  filters: { year: null, market: 'ALL' },
  last_imported_at: '2026-06-30T10:15:00Z',
  available_years: [2023, 2024, 2025, 2026],
  backtest_stats: {
    total_trades: 40,
    win_rate_pct: 62.5,
    avg_pnl_gbp: 210.5,
    total_pnl_gbp: 8420.0,
    avg_hold_days: 14.2,
  },
  actual_stats: {
    total_trades: 6,
    win_rate_pct: 66.7,
    avg_pnl_gbp: 180.3,
    total_pnl_gbp: 1081.8,
    avg_hold_days: 11.5,
  },
  yearly_breakdown: [
    { entry_year: 2025, num_trades: 20, avg_pnl_gbp: 200.0, total_pnl_gbp: 4000.0, avg_hold_days: 13.0, win_rate_pct: 60.0 },
  ],
};

// actual_stats: null — no live trades match the filter (AC-03: frontend renders "—")
const SUMMARY_NO_ACTUAL = {
  ...SUMMARY_WITH_ACTUAL,
  actual_stats: null,
};

const TRADES_RESPONSE = {
  filters: { year: null, market: 'ALL' },
  backtest_trades: [
    { id: 1, ticker: 'NVDA', entry_date: '2023-02-28', exit_date: '2023-03-20', holding_days: 20, entry_price: 234.5, exit_price: 268.1, pnl_gbp: 425.3, pnl_pct: 14.33, market: 'US', exit_reason: 'Stop', was_profitable: true, entry_year: 2023 },
    { id: 2, ticker: 'BARC', entry_date: '2023-04-10', exit_date: '2023-04-25', holding_days: 15, entry_price: 150.0, exit_price: 145.0, pnl_gbp: -75.0, pnl_pct: -3.33, market: 'UK', exit_reason: 'Risk-Off', was_profitable: false, entry_year: 2023 },
    { id: 3, ticker: 'MSFT', entry_date: '2023-05-01', exit_date: '2023-05-20', holding_days: 19, entry_price: 300.0, exit_price: 320.0, pnl_gbp: 200.0, pnl_pct: 6.67, market: 'US', exit_reason: 'Rebalance', was_profitable: true, entry_year: 2023 },
  ],
  actual_trades: [
    { ticker: 'AAPL', entry_date: '2024-03-01', exit_date: '2024-03-22', holding_days: 21, entry_price: 175.4, exit_price: 182.1, pnl_gbp: 312.5, pnl_pct: 3.82, market: 'US', exit_reason: 'trailing_stop', was_profitable: true, entry_year: 2024 },
  ],
};

const OPEN_POSITIONS_EMPTY = {
  filters: { market: 'ALL' },
  open_positions: [],
  summary: { count: 0, total_unrealized_pnl_gbp: null },
};

const OPEN_POSITIONS_WITH_DATA = {
  filters: { market: 'ALL' },
  open_positions: [
    {
      ticker: 'TSLA',
      market: 'US',
      entry_date: '2026-06-01',
      entry_price: 210.0,
      current_price: 228.5,
      unrealized_pnl_gbp: 18.5,
      unrealized_pnl_pct: 8.81,
      days_held: 32,
    },
  ],
  summary: { count: 1, total_unrealized_pnl_gbp: 18.5 },
};

// ---------------------------------------------------------------------------
// Shared mock setup
// ---------------------------------------------------------------------------

async function mockBaseEndpoints(page, { summary = SUMMARY_WITH_ACTUAL, trades = TRADES_RESPONSE, openPositions = OPEN_POSITIONS_EMPTY } = {}) {
  await page.route(/\/strategy\/benchmark\/open-positions/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(openPositions) })
  );
  await page.route(/\/strategy\/benchmark\/summary/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(summary) })
  );
  await page.route(/\/strategy\/benchmark\/trades/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(trades) })
  );
}

// Minimal Positions-page route set (same shape as the proven-in-CI
// stubPositionsRoutes helper in epic02-v62-ai-briefing-chat.spec.js) — used
// as the navigation origin for SC-SB-01a instead of DashboardHome, which
// requires a much larger stub surface (market/status, signals, ai/*,
// red-flag-journal, etc.) that this spec has no reason to duplicate.
async function mockPositionsOrigin(page) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance') || url.includes('/grace-period-alerts')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) });
  });
  await page.route('**/portfolio**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null }) })
  );
}

// ---------------------------------------------------------------------------
// SC-SB-01 — Page accessible from navigation
// ---------------------------------------------------------------------------

test.describe('SC-SB-01 — Strategy Benchmark page accessible from navigation', () => {
  test('SC-SB-01a: clicking the sidebar "Strategy Benchmark" link navigates to the page', async ({ page }) => {
    await mockPositionsOrigin(page);
    await mockBaseEndpoints(page);
    await page.goto('/#/Positions');
    await page.waitForSelector('h1', { timeout: 10000 });

    // The sidebar groups items under collapsible sections (Trading, Analytics,
    // Tools, System — see Layout.js NAV_GROUPS). Only the group containing the
    // *current* page starts expanded; "Strategy Benchmark" lives in the
    // "Analytics" group, which is collapsed by default when navigating from
    // Positions (in the "Trading" group). Expand it before clicking the link.
    await page.getByRole('button', { name: 'Analytics' }).click();

    await page.getByRole('link', { name: 'Strategy Benchmark' }).first().click();

    await expect(page).toHaveURL(/#\/StrategyBenchmark/);
    await expect(page.getByTestId('strategy-benchmark-page')).toBeVisible({ timeout: 10000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SB-02 — Year + Market filters apply to all panels simultaneously
// ---------------------------------------------------------------------------

test.describe('SC-SB-02 — Year and Market filters apply simultaneously', () => {
  test('SC-SB-02a: selecting a year re-requests summary and trades with the year query param', async ({ page }) => {
    await mockBaseEndpoints(page);

    let summaryUrl = null;
    let tradesUrl = null;
    await page.route(/\/strategy\/benchmark\/summary/, (route) => {
      summaryUrl = route.request().url();
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SUMMARY_WITH_ACTUAL) });
    });
    await page.route(/\/strategy\/benchmark\/trades/, (route) => {
      tradesUrl = route.request().url();
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TRADES_RESPONSE) });
    });

    await page.goto('/#/StrategyBenchmark');
    await expect(page.getByTestId('benchmark-year-filter')).toBeVisible({ timeout: 10000 });

    await page.getByTestId('benchmark-year-filter').selectOption('2023');
    await page.waitForTimeout(500);

    expect(summaryUrl).toContain('year=2023');
    expect(tradesUrl).toContain('year=2023');
  });

  test('SC-SB-02b: selecting a market re-requests summary and trades with the market query param', async ({ page }) => {
    await mockBaseEndpoints(page);

    let summaryUrl = null;
    let tradesUrl = null;
    await page.route(/\/strategy\/benchmark\/summary/, (route) => {
      summaryUrl = route.request().url();
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SUMMARY_WITH_ACTUAL) });
    });
    await page.route(/\/strategy\/benchmark\/trades/, (route) => {
      tradesUrl = route.request().url();
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TRADES_RESPONSE) });
    });

    await page.goto('/#/StrategyBenchmark');
    await expect(page.getByTestId('benchmark-market-uk')).toBeVisible({ timeout: 10000 });

    await page.getByTestId('benchmark-market-uk').click();
    await page.waitForTimeout(500);

    expect(summaryUrl).toContain('market=UK');
    expect(tradesUrl).toContain('market=UK');
  });
});

// ---------------------------------------------------------------------------
// SC-SB-03 — Panel 1 "—" placeholder when no live trades match
// ---------------------------------------------------------------------------

test.describe('SC-SB-03 — Panel 1 Actual column placeholder', () => {
  test('SC-SB-03a: Actual column shows "—" for all stat cards when actual_stats is null', async ({ page }) => {
    await mockBaseEndpoints(page, { summary: SUMMARY_NO_ACTUAL });
    await page.goto('/#/StrategyBenchmark');

    const statCards = page.getByTestId('benchmark-stat-cards');
    await expect(statCards).toBeVisible({ timeout: 10000 });

    // 5 stat cards x "Actual" placeholder = at least 5 em-dash occurrences.
    const placeholderCount = await statCards.getByText('—', { exact: true }).count();
    expect(placeholderCount).toBeGreaterThanOrEqual(5);
    // No numeric Actual figures should be present when actual_stats is null.
    await expect(statCards).not.toContainText('66.7%');
  });

  test('SC-SB-03b: Actual column shows real figures when actual_stats is present', async ({ page }) => {
    await mockBaseEndpoints(page, { summary: SUMMARY_WITH_ACTUAL });
    await page.goto('/#/StrategyBenchmark');

    const statCards = page.getByTestId('benchmark-stat-cards');
    await expect(statCards).toBeVisible({ timeout: 10000 });
    await expect(statCards).toContainText('66.7%');
  });
});

// ---------------------------------------------------------------------------
// SC-SB-04 — Panel 3 toggle modes and exit reason badge colours
// ---------------------------------------------------------------------------

test.describe('SC-SB-04 — Panel 3 toggle modes and exit reason badges', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/StrategyBenchmark');
    await expect(page.getByTestId('benchmark-panel-3')).toBeVisible({ timeout: 10000 });
  });

  test('SC-SB-04a: default (backtest) mode shows only backtest trades with correctly coloured exit badges', async ({ page }) => {
    const table = page.getByTestId('benchmark-trade-table');
    await expect(table).toBeVisible();

    // Stop (red), Risk-Off (amber), Rebalance (teal) — all 3 backtest rows present.
    await expect(table.getByText('Stop', { exact: true })).toHaveClass(/bg-red-600/);
    await expect(table.getByText('Risk-Off', { exact: true })).toHaveClass(/bg-amber-600/);
    await expect(table.getByText('Rebalance', { exact: true })).toHaveClass(/bg-teal-600/);

    // Actual-only trade (AAPL) must not be visible in backtest-only mode.
    await expect(table.getByText('AAPL')).not.toBeVisible();
  });

  test('SC-SB-04b: "Actual Only" toggle shows only the live trade', async ({ page }) => {
    await page.getByTestId('benchmark-mode-actual').click();

    const table = page.getByTestId('benchmark-trade-table');
    await expect(table.getByText('AAPL')).toBeVisible();
    await expect(table.getByText('NVDA')).not.toBeVisible();
  });

  test('SC-SB-04c: "Side by Side" toggle shows both backtest and live trades with source badges', async ({ page }) => {
    await page.getByTestId('benchmark-mode-side-by-side').click();

    const table = page.getByTestId('benchmark-trade-table');
    await expect(table.getByText('NVDA')).toBeVisible();
    await expect(table.getByText('AAPL')).toBeVisible();
    // 3 backtest rows -> 3 "BT" badges; 1 actual row -> 1 "Live" badge.
    // Multiple matches are expected here, so assert counts rather than a
    // single toBeVisible() (which requires exactly one match under
    // Playwright strict mode).
    await expect(table.getByText('BT', { exact: true })).toHaveCount(3);
    await expect(table.getByText('Live', { exact: true })).toHaveCount(1);
  });
});

// ---------------------------------------------------------------------------
// SC-SB-05 — Panel 0 conditional rendering (TEST-GAP-EPIC-03-v64, AC-01)
// ---------------------------------------------------------------------------

test.describe('SC-SB-05 — Panel 0 conditional rendering', () => {
  test('SC-SB-05a: panel is omitted entirely when there are 0 open positions', async ({ page }) => {
    await mockBaseEndpoints(page, { openPositions: OPEN_POSITIONS_EMPTY });
    await page.goto('/#/StrategyBenchmark');
    await expect(page.getByTestId('benchmark-panel-1')).toBeVisible({ timeout: 10000 });

    await expect(page.getByTestId('benchmark-panel-0')).toHaveCount(0);
  });

  test('SC-SB-05b: panel renders with the position row when ≥1 open position exists', async ({ page }) => {
    await mockBaseEndpoints(page, { openPositions: OPEN_POSITIONS_WITH_DATA });
    await page.goto('/#/StrategyBenchmark');

    const panel = page.getByTestId('benchmark-panel-0');
    await expect(panel).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('benchmark-open-positions-summary')).toContainText('1 open position');
    await expect(page.getByTestId('benchmark-open-position-TSLA')).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// SC-SB-06 — Panel 0 Market-filter-only interaction (TEST-GAP-EPIC-03-v64, AC-02)
// ---------------------------------------------------------------------------

test.describe('SC-SB-06 — Panel 0 Market-filter-only interaction', () => {
  test('SC-SB-06a: selecting a Market re-requests open-positions with the market param', async ({ page }) => {
    await mockBaseEndpoints(page, { openPositions: OPEN_POSITIONS_WITH_DATA });

    let openPositionsUrl = null;
    await page.route(/\/strategy\/benchmark\/open-positions/, (route) => {
      openPositionsUrl = route.request().url();
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(OPEN_POSITIONS_WITH_DATA) });
    });

    await page.goto('/#/StrategyBenchmark');
    await expect(page.getByTestId('benchmark-market-uk')).toBeVisible({ timeout: 10000 });

    await page.getByTestId('benchmark-market-uk').click();
    await page.waitForTimeout(500);

    expect(openPositionsUrl).toContain('market=UK');
  });

  test('SC-SB-06b: selecting a Year does not add a year param to the open-positions request', async ({ page }) => {
    await mockBaseEndpoints(page, { openPositions: OPEN_POSITIONS_WITH_DATA });

    let openPositionsUrl = null;
    await page.route(/\/strategy\/benchmark\/open-positions/, (route) => {
      openPositionsUrl = route.request().url();
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(OPEN_POSITIONS_WITH_DATA) });
    });

    await page.goto('/#/StrategyBenchmark');
    await expect(page.getByTestId('benchmark-year-filter')).toBeVisible({ timeout: 10000 });

    await page.getByTestId('benchmark-year-filter').selectOption('2023');
    await page.waitForTimeout(500);

    // Open positions are current-state, not year-filtered (ux_spec.md "Filter
    // Interaction") — the endpoint is still re-requested (fetchData refires
    // on every year/market change) but must never carry a year query param.
    expect(openPositionsUrl).not.toBeNull();
    expect(openPositionsUrl).not.toContain('year=');
  });
});

// ---------------------------------------------------------------------------
// SC-SB-07 — Panel 0 API-error state (TEST-GAP-EPIC-03-v64, AC-03)
// ---------------------------------------------------------------------------

test.describe('SC-SB-07 — Panel 0 API-error state', () => {
  test('SC-SB-07a: shows "Open positions temporarily unavailable." on a 500 and does not break the rest of the page', async ({ page }) => {
    await page.route(/\/strategy\/benchmark\/open-positions/, (route) =>
      route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ error: 'Internal Server Error' }) })
    );
    await page.route(/\/strategy\/benchmark\/summary/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SUMMARY_WITH_ACTUAL) })
    );
    await page.route(/\/strategy\/benchmark\/trades/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TRADES_RESPONSE) })
    );

    await page.goto('/#/StrategyBenchmark');

    const panel = page.getByTestId('benchmark-panel-0');
    await expect(panel).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('benchmark-open-positions-error')).toHaveText('Open positions temporarily unavailable.');

    // Rest of the page (Panel 1) must still render normally.
    await expect(page.getByTestId('benchmark-stat-cards')).toBeVisible();
  });
});
