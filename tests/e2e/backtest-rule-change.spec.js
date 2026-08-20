/**
 * Backtest Rule Change Tab — Acceptance Tests (V-BACKTEST-01..04)
 * ST-07 (BLG-FEAT-89, EPIC-02, v8.9) — In-app backtesting engine for
 * strategy rule changes.
 *
 * AC-01: A candidate strategy_rules.md change can be run against historical
 *        data from inside the app, with no external script step.
 * AC-02: Output includes win rate, R-multiple distribution, and drawdown
 *        compared against the current live rule set.
 * AC-03: Each backtest run is persisted with enough detail to audit later.
 *
 * Design source: docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md
 * Spec: docs/specs/api_contracts/strategy_benchmark_endpoints.md
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

const SUMMARY_EMPTY = { backtest_stats: {}, yearly_breakdown: [] };
const TRADES_EMPTY = { backtest_trades: [], actual_trades: [] };
const OPEN_POSITIONS_EMPTY = { open_positions: [], summary: { count: 0, total_unrealized_pnl_gbp: null } };

const RUN_RESULT = {
  status: 'ok',
  data: {
    id: 'run-001',
    created_at: '2026-08-18T10:00:00Z',
    initiated_by: null,
    rule_diff_summary: 'min_hold_days: 10 -> 15',
    candidate_params: { lookback: 252, top_n: 5, min_hold_days: 15 },
    live_params: { lookback: 252, top_n: 5, min_hold_days: 10 },
    universe_tickers: ['AAPL', 'MSFT', 'VOD.L'],
    universe_start_date: '2022-08-18',
    universe_end_date: '2026-08-18',
    candidate_result: {
      trade_count: 34,
      win_rate_pct: 58.82,
      max_drawdown_pct: -14.21,
      median_r: 0.42,
      r_multiple_buckets: [
        { label: '< -3R', count: 0 },
        { label: '-3R to -2R', count: 1 },
        { label: '-2R to -1R', count: 3 },
        { label: '-1R to 0R', count: 8 },
        { label: '0R to 1R', count: 10 },
        { label: '1R to 2R', count: 7 },
        { label: '2R to 3R', count: 3 },
        { label: '> 3R', count: 2 },
      ],
    },
    live_result: {
      trade_count: 31,
      win_rate_pct: 54.84,
      max_drawdown_pct: -15.03,
      median_r: 0.35,
      r_multiple_buckets: [
        { label: '< -3R', count: 1 },
        { label: '-3R to -2R', count: 2 },
        { label: '-2R to -1R', count: 4 },
        { label: '-1R to 0R', count: 6 },
        { label: '0R to 1R', count: 5 },
        { label: '1R to 2R', count: 7 },
        { label: '2R to 3R', count: 4 },
        { label: '> 3R', count: 2 },
      ],
    },
  },
};

const RUN_HISTORY = {
  status: 'ok',
  data: [
    {
      id: 'run-001',
      initiated_by: 'Product Owner',
      rule_diff_summary: 'min_hold_days: 10 -> 15',
      universe_start_date: '2022-08-18',
      universe_end_date: '2026-08-18',
      universe_size: 20,
      candidate_result: { trade_count: 34, win_rate_pct: 58.82, max_drawdown_pct: -14.21, median_r: 0.42 },
      live_result: { trade_count: 31, win_rate_pct: 54.84, max_drawdown_pct: -15.03, median_r: 0.35 },
      created_at: '2026-08-18T10:00:00Z',
    },
  ],
};

async function mockBaseEndpoints(page) {
  await page.route(/\/strategy\/benchmark\/open-positions/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(OPEN_POSITIONS_EMPTY) })
  );
  await page.route(/\/strategy\/benchmark\/summary/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SUMMARY_EMPTY) })
  );
  await page.route(/\/strategy\/benchmark\/trades/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TRADES_EMPTY) })
  );
}

test.describe('Backtest Rule Change Tab (V-BACKTEST-01..04)', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/StrategyBenchmark');
    await page.getByTestId('benchmark-tab-backtest-rule-change').click();
    await expect(page.getByTestId('backtest-rule-change-tab')).toBeVisible();
  });

  test('V-BACKTEST-01 — tab shows candidate form and empty results state', async ({ page }) => {
    await expect(page.getByTestId('backtest-input-min_hold_days')).toBeVisible();
    await expect(page.getByTestId('backtest-run-btn')).toBeVisible();
    await expect(page.getByTestId('backtest-results-empty')).toBeVisible();
  });

  test('V-BACKTEST-02 — running a backtest shows win rate, R-multiple distribution, and drawdown vs. live (AC-02)', async ({ page }) => {
    await page.route(new RegExp(`${API}/strategy/backtest-rule-change/run`), (route) => {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RUN_RESULT) });
    });

    await page.getByTestId('backtest-input-min_hold_days').fill('15');

    const runPromise = page.waitForResponse(/\/strategy\/backtest-rule-change\/run/);
    await page.getByTestId('backtest-run-btn').click();
    await runPromise;

    await expect(page.getByTestId('backtest-results-loaded')).toBeVisible({ timeout: 5000 });
    // fmtPct formats to 1dp (not the raw 2dp API value).
    await expect(page.getByText('58.8%')).toBeVisible();
    await expect(page.getByText('54.8%')).toBeVisible();
    await expect(page.getByText('-14.2%')).toBeVisible();
    await expect(page.getByText('-15.0%')).toBeVisible();
    // R-multiple histogram renders (recharts SVG with the candidate/live bar series).
    await expect(page.getByRole('application')).toBeVisible();
    await expect(page.locator('.recharts-legend-item-text', { hasText: 'Candidate' })).toBeVisible();
    await expect(page.locator('.recharts-legend-item-text', { hasText: 'Live' })).toBeVisible();
    await expect(page.getByTestId('backtest-run-metadata')).toContainText('min_hold_days: 10 -> 15');
  });

  test('V-BACKTEST-03 — Run Backtest button shows a spinner while running (AC-01, no external script step)', async ({ page }) => {
    await page.route(new RegExp(`${API}/strategy/backtest-rule-change/run`), async (route) => {
      await new Promise((r) => setTimeout(r, 300));
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RUN_RESULT) });
    });

    await page.getByTestId('backtest-run-btn').click();
    await expect(page.getByText(/running backtest/i)).toBeVisible();
    await expect(page.getByTestId('backtest-results-loading')).toBeVisible();
    await expect(page.getByTestId('backtest-results-loaded')).toBeVisible({ timeout: 5000 });
  });

  test('V-BACKTEST-04 — Run History lists a prior run, expandable to re-view stored output (AC-03)', async ({ page }) => {
    await page.route(new RegExp(`${API}/strategy/backtest-rule-change/runs(\\?.*)?$`), (route) => {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RUN_HISTORY) });
    });

    await page.getByTestId('backtest-run-history-toggle-panel').click();
    await expect(page.getByTestId('backtest-run-history-list')).toBeVisible();
    await expect(page.getByTestId('backtest-run-history-item')).toBeVisible();
    await expect(page.getByText('min_hold_days: 10 -> 15')).toBeVisible();

    // Expand the item to re-view its stored output without re-running.
    await page.getByTestId('backtest-run-history-toggle').click();
    await expect(page.getByText('By: Product Owner')).toBeVisible();
    await expect(page.getByText(/Universe: 20 tickers/)).toBeVisible();
  });

  test('V-BACKTEST-05 — run failure shows an inline error, not a blank/broken panel', async ({ page }) => {
    await page.route(new RegExp(`${API}/strategy/backtest-rule-change/run`), (route) => {
      route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'error', message: "Unknown parameter field(s): ['bogus']" }),
      });
    });

    await page.getByTestId('backtest-run-btn').click();
    await expect(page.getByTestId('backtest-run-error')).toBeVisible({ timeout: 5000 });
    // Spec text (strategy_benchmark.md §7.6 States): generic message, not the
    // raw backend error — "Retry" is re-clicking the same Run Backtest button.
    await expect(page.getByTestId('backtest-run-error')).toHaveText('Backtest failed to complete. Please try again.');
    await expect(page.getByTestId('backtest-run-btn')).toBeEnabled();
  });
});
