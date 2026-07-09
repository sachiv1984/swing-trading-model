/**
 * Trade Plan Tag Filter (§14a) — Performance Analytics Page (ST-05, BLG-FEAT-52, EPIC-02, v6.8)
 *
 * Design source: docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md §3
 * Spec: docs/specs/frontend/pages/analytics.md §14a
 *
 * Covers observable AC (ST-05 AC-03, AC-05):
 *   SC-TPTF-01  Filter control renders above the §14 TagPerformance table
 *   SC-TPTF-02  Selecting a tag shows a dismissible pill and fetches comparison data
 *   SC-TPTF-03  Comparison row shows win rate + avg R-multiple per selected tag
 *   SC-TPTF-04  Deselecting all tags hides the comparison row
 *   SC-TPTF-05  No closed trades for selected tag shows the empty-state message
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PerformanceAnalytics').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
}

// PerformanceAnalytics.js gates its entire body (including TradePlanTagFilter)
// behind a "Not enough trades" DataState until >= settingsData.min_trades_for_analytics
// (default 10) closed trades are present in the selected period. Provide 12 recent
// closed trades so the gate clears.
async function mockTrades(page) {
  const now = new Date();
  const trades = Array.from({ length: 12 }, (_, i) => {
    const exitDate = new Date(now);
    exitDate.setDate(exitDate.getDate() - i);
    return {
      id: `t${i}`,
      ticker: 'AAPL',
      market: 'US',
      entry_date: exitDate.toISOString().slice(0, 10),
      exit_date: exitDate.toISOString().slice(0, 10),
      pnl: i % 2 === 0 ? 100 : -50,
      pnl_pct: i % 2 === 0 ? 5 : -2,
    };
  });
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { total_trades: trades.length, win_rate: 50, total_pnl: 300, trades } }),
    })
  );
}

async function mockTradePlanTags(page, tags) {
  await page.route(`${API}/trade-plans/tags`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: tags }) })
  );
}

async function mockTagPerformance(page, rows) {
  await page.route(new RegExp(`${API}/analytics/tag-performance`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: rows }) })
  );
}

async function gotoAnalytics(page) {
  await page.goto('/#/PerformanceAnalytics');
  await expect(page.getByTestId('trade-plan-tag-filter')).toBeVisible({ timeout: 10000 });
}

test('SC-TPTF-01: Filter control renders on the Performance Analytics page', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockTradePlanTags(page, ['breakout', 'momentum']);
  await gotoAnalytics(page);

  await expect(page.getByTestId('trade-plan-tag-filter-toggle')).toBeVisible();
  await expect(page.getByTestId('trade-plan-tag-filter-toggle')).toContainText(/filter by trade plan tag/i);
});

test('SC-TPTF-02: Selecting a tag shows a dismissible pill', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockTradePlanTags(page, ['breakout', 'momentum']);
  await mockTagPerformance(page, [{ tag: 'breakout', win_rate: 62.5, avg_r_multiple: 1.8, trade_count: 8 }]);
  await gotoAnalytics(page);

  await page.getByTestId('trade-plan-tag-filter-toggle').click();
  await page.getByTestId('trade-plan-tag-filter-option-breakout').click();

  await expect(page.getByText('breakout').first()).toBeVisible({ timeout: 5000 });
});

test('SC-TPTF-03: Comparison row shows win rate and avg R-multiple for the selected tag', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockTradePlanTags(page, ['breakout']);
  await mockTagPerformance(page, [{ tag: 'breakout', win_rate: 62.5, avg_r_multiple: 1.8, trade_count: 8 }]);
  await gotoAnalytics(page);

  await page.getByTestId('trade-plan-tag-filter-toggle').click();
  await page.getByTestId('trade-plan-tag-filter-option-breakout').click();

  await expect(page.getByTestId('trade-plan-tag-comparison-row')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('trade-plan-tag-comparison-row')).toContainText('62.5% win rate');
  await expect(page.getByTestId('trade-plan-tag-comparison-row')).toContainText('+1.8R');
});

test('SC-TPTF-04: Deselecting the tag hides the comparison row', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockTradePlanTags(page, ['breakout']);
  await mockTagPerformance(page, [{ tag: 'breakout', win_rate: 62.5, avg_r_multiple: 1.8, trade_count: 8 }]);
  await gotoAnalytics(page);

  await page.getByTestId('trade-plan-tag-filter-toggle').click();
  await page.getByTestId('trade-plan-tag-filter-option-breakout').click();
  await expect(page.getByTestId('trade-plan-tag-comparison-row')).toBeVisible({ timeout: 5000 });

  // Dropdown stays open after selection (OR-logic multi-select) — click the same
  // option again to deselect, without re-toggling the dropdown closed first.
  await page.getByTestId('trade-plan-tag-filter-option-breakout').click();

  await expect(page.getByTestId('trade-plan-tag-comparison-row')).toHaveCount(0);
});

test('SC-TPTF-05: "No closed trades" message shown when selected tag has zero matching trades', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockTradePlanTags(page, ['unused-tag']);
  await mockTagPerformance(page, [{ tag: 'unused-tag', win_rate: 0.0, avg_r_multiple: null, trade_count: 0 }]);
  await gotoAnalytics(page);

  await page.getByTestId('trade-plan-tag-filter-toggle').click();
  await page.getByTestId('trade-plan-tag-filter-option-unused-tag').click();

  await expect(page.getByText(/no closed trades for selected tag/i)).toBeVisible({ timeout: 5000 });
});
