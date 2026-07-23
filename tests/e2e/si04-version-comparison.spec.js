/**
 * SI-04 Strategy Version Comparison Tab — Scenario Coverage
 * ST-01 (EPIC-01, v7.7, BLG-FEAT-75)
 *
 * Spec refs:
 *   docs/specs/frontend/pages/strategy_benchmark.md §7.5
 *   docs/design/2026-07-21__release-v7.7/si04-strategy-version-comparison/ux_spec.md
 *   docs/specs/api_contracts/strategy_version_comparison_contract.md v0.2.0
 *
 * Covers: SC-SI04-01 (tab + idle state), SC-SI04-02 (loaded — selector UI +
 * side-by-side render with all 3 required metrics: win rate, avg R,
 * compliance rate), SC-SI04-03 (insufficient data), SC-SI04-04 (version not
 * found), SC-SI04-05 (invalid version order).
 *
 * Component: src/pages/StrategyBenchmark.js (VersionComparisonTab)
 * ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/StrategyBenchmark').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const SUMMARY_EMPTY = {
  filters: { year: null, market: 'ALL' },
  last_imported_at: null,
  available_years: [],
  backtest_stats: null,
  actual_stats: null,
  yearly_breakdown: [],
};

const TRADES_EMPTY = {
  filters: { year: null, market: 'ALL' },
  backtest_trades: [],
  actual_trades: [],
};

const OPEN_POSITIONS_EMPTY = {
  filters: { market: 'ALL' },
  open_positions: [],
  summary: { count: 0, total_unrealized_pnl_gbp: null },
};

const COMPARISON_RESULT = {
  version_from: '1.0',
  version_to: '1.4',
  date_range: null,
  version_from_metrics: { trade_count: 42, win_rate: 0.55, avg_R: 0.32, performance_delta: null, compliance_rate: 0.71 },
  version_to_metrics: { trade_count: 18, win_rate: 0.61, avg_R: 0.48, performance_delta: 0.16, compliance_rate: 0.82 },
  comparison_summary: { win_rate_delta: 0.06, avg_R_delta: 0.16, trade_count_delta: -24, assessment: 'Improved' },
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

test.describe('SI-04 Strategy Version Comparison', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/StrategyBenchmark');
  });

  test('SC-SI04-01: Version Comparison tab shows controls and idle state', async ({ page }) => {
    await page.getByTestId('benchmark-tab-version-comparison').click();
    await expect(page.getByTestId('version-comparison-tab')).toBeVisible();
    await expect(page.getByTestId('version-from-select')).toBeVisible();
    await expect(page.getByTestId('version-to-select')).toBeVisible();
    await expect(page.getByTestId('version-comparison-idle')).toContainText('Select two strategy versions to compare.');
  });

  test('SC-SI04-02: Compare renders side-by-side table with win rate, avg R, and compliance rate for both versions', async ({ page }) => {
    await page.route(/\/analytics\/strategy-version-comparison/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(COMPARISON_RESULT) })
    );

    await page.getByTestId('benchmark-tab-version-comparison').click();
    await page.getByTestId('version-from-select').selectOption('1.0');
    await page.getByTestId('version-to-select').selectOption('1.4');
    await page.getByTestId('version-compare-btn').click();

    const table = page.getByTestId('version-comparison-table');
    await expect(table).toBeVisible();
    await expect(table).toContainText('42'); // trade_count version_from
    await expect(table).toContainText('18'); // trade_count version_to
    await expect(table).toContainText('55.0%'); // win_rate version_from
    await expect(table).toContainText('61.0%'); // win_rate version_to
    await expect(table).toContainText('+0.32R'); // avg_R version_from
    await expect(table).toContainText('+0.48R'); // avg_R version_to
    await expect(table).toContainText('71.0%'); // compliance_rate version_from
    await expect(table).toContainText('82.0%'); // compliance_rate version_to

    await expect(page.getByTestId('version-comparison-assessment')).toContainText('Improved');
  });

  test('SC-SI04-03: Insufficient data (422) shows the minimum-trades message', async ({ page }) => {
    await page.route(/\/analytics\/strategy-version-comparison/, (route) =>
      route.fulfill({
        status: 422,
        contentType: 'application/json',
        body: JSON.stringify({
          detail: {
            status: 'error', code: 'insufficient_data',
            message: "Version '1.1' has only 3 trades — minimum 10 required for reliable comparison",
            version: '1.1', trade_count: 3, min_trades_required: 10,
          },
        }),
      })
    );

    await page.getByTestId('benchmark-tab-version-comparison').click();
    await page.getByTestId('version-compare-btn').click();

    await expect(page.getByTestId('version-comparison-error')).toContainText('Not enough trades to compare');
    await expect(page.getByTestId('version-comparison-error')).toContainText('minimum 10 required');
  });

  test('SC-SI04-04: Version not found (404) shows inline dropdown error', async ({ page }) => {
    await page.route(/\/analytics\/strategy-version-comparison/, (route) =>
      route.fulfill({
        status: 404,
        contentType: 'application/json',
        body: JSON.stringify({
          detail: {
            status: 'error', code: 'version_not_found',
            message: "Strategy version '1.4' not found in version registry",
            missing_version: '1.4',
          },
        }),
      })
    );

    await page.getByTestId('benchmark-tab-version-comparison').click();
    await page.getByTestId('version-compare-btn').click();

    await expect(page.getByTestId('version-to-error')).toContainText('Version not found.');
  });

  test('SC-SI04-05: Invalid version order (400) shows inline error under "To"', async ({ page }) => {
    await page.route(/\/analytics\/strategy-version-comparison/, (route) =>
      route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({
          detail: {
            status: 'error', code: 'version_order_error',
            message: 'version_to must be chronologically after version_from',
          },
        }),
      })
    );

    await page.getByTestId('benchmark-tab-version-comparison').click();
    await page.getByTestId('version-from-select').selectOption('1.4');
    await page.getByTestId('version-to-select').selectOption('1.0');
    await page.getByTestId('version-compare-btn').click();

    await expect(page.getByTestId('version-to-error')).toContainText("Must be chronologically after the 'From' version.");
  });
});
