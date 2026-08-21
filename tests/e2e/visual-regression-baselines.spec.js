/**
 * Visual Regression Baseline Snapshots (ST-18, BLG-QA-81, EPIC-04, v9.0)
 *
 * Establishes the FIRST pixel-level `toHaveScreenshot()` baselines in this
 * repo. `playwright.config.js` has carried the snapshot infra (snapshotDir,
 * maxDiffPixelRatio, animations: 'disabled') and
 * `.github/workflows/update-visual-snapshots.yml` has existed to refresh
 * baselines on CI — but until this story, zero tests actually called
 * `toHaveScreenshot()` and no baseline PNGs existed under
 * `tests/e2e/__snapshots__/`. `visual-snapshots.spec.js` (the older,
 * similarly-named file) covers the same visual-behaviour intent via CSS
 * class assertions instead of pixel diffs — see that file's header comment
 * for why (cross-platform Chromium rendering variance). This file is
 * additive, not a replacement.
 *
 * Scope (BLG-QA-81 AC):
 *   1. Contrast-sensitive baselines, dual-theme (dark + light), for the
 *      highest-traffic pages touched by the app-wide BLG-FE-87/88/89
 *      contrast remediation (v6.7) — that work was an app-wide sweep
 *      (764 instances / 102 files), so "the components touched" is
 *      represented here by a cross-section of high-traffic page types
 *      (dashboard, table/card toggle, form, settings), matching the same
 *      representative-sample approach ST-21's axe-core scan already used.
 *   2. At least one chart-heavy component end-to-end, as proof of pattern —
 *      PerformanceAnalytics, which renders `UnderwaterChart` (recharts
 *      AreaChart) and `TimeBasedCharts` (recharts BarChart/ScatterChart/
 *      ComposedChart) directly on load, no interaction required beyond the
 *      period-selector switch to "All Time" (see setupAnalytics() below —
 *      StrategyBenchmark was considered first, but its only recharts usage
 *      is `RMultipleComparisonChart`, gated behind running a Backtest Rule
 *      Change comparison — a much heavier baseline setup for the same
 *      "proof of pattern" AC that PerformanceAnalytics satisfies directly).
 *
 * Each baseline test sets the theme via localStorage BEFORE navigation
 * (page.addInitScript), matching src/Layout.js's own lazy-init read
 * (`localStorage.getItem("theme") || "dark"`) — no in-page toggle click is
 * needed, and no flash-of-wrong-theme risk.
 *
 * To (re)generate baseline PNGs locally or on CI:
 *   npx playwright test tests/e2e/visual-regression-baselines.spec.js --update-snapshots
 * (or trigger the existing "Update Visual Snapshot Baselines" workflow,
 * widened in this story to include this spec file — see that workflow file).
 *
 * Infrastructure: page.route() network interception. No live backend
 * required. HashRouter — all navigation via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');
const { ALL_TRADES, ANALYTICS_SETTINGS } = require('./mocks/analytics-mock-data');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Theme helper
// ---------------------------------------------------------------------------

async function setTheme(page, theme) {
  await page.addInitScript((t) => {
    window.localStorage.setItem('theme', t);
  }, theme);
}

// ---------------------------------------------------------------------------
// Generic mock routes (reused from accessibility-axe-scan.spec.js's
// mockRoutes — same broad catch-all shape, proven not to trigger the
// "allPositions.filter is not a function" runtime error since /positions
// returns a bare array here, not the {status,data} envelope).
// ---------------------------------------------------------------------------

async function mockRoutes(page) {
  await page.route(new RegExp(`${API}/`), (route) => {
    const url = route.request().url();
    if (url.includes('/market/status')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { spy: { is_risk_on: true }, ftse: { is_risk_on: true } } }),
      });
    }
    if (url.includes('/settings')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: [{ id: 'settings-1', default_risk_percent: 1.0 }] }),
      });
    }
    if (url.includes('/positions/compliance')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
    if (/\/positions(\?|$)/.test(url)) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
  });
}

// ---------------------------------------------------------------------------
// PerformanceAnalytics setup (reused verbatim from the proven
// setupAnalytics() helper in analytics-mobile-responsive.spec.js, including
// its "All Time" period-selector step — the default "last_month" period
// filters ALL_TRADES down to zero rows against the current run date,
// which was a real bug caught by CI when that file first introduced this
// pattern; see that file's comment for detail).
// ---------------------------------------------------------------------------

async function setupAnalytics(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ALL_TRADES) })
  );
  await page.route(`${API}/settings`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ANALYTICS_SETTINGS) })
  );
  await page.goto('/#/PerformanceAnalytics');
  await expect(
    page.locator('h1, [class*="text-2xl"], [class*="text-3xl"]').filter({ hasText: 'Performance Analytics' })
  ).toBeVisible({ timeout: 20000 });
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 15000 });

  const trigger = page.locator('[class*="SelectTrigger"], button[role="combobox"]').first();
  await trigger.click();
  await page.locator('[role="option"]').filter({ hasText: 'All Time' }).click();
  await page.waitForTimeout(500);
}

// ---------------------------------------------------------------------------
// Contrast-sensitive baselines — dark + light, 4 representative pages
// (same page set as ST-21's axe-core scan: DashboardHome, Positions,
// TradePlan, Settings)
// ---------------------------------------------------------------------------

test.describe('Visual regression baselines — contrast-sensitive pages (ST-18)', () => {
  test.beforeEach(async ({ page }) => {
    await mockRoutes(page);
  });

  for (const theme of ['dark', 'light']) {
    test(`DashboardHome baseline — ${theme} theme`, async ({ page }) => {
      await setTheme(page, theme);
      await page.goto('/#/DashboardHome');
      await page.waitForLoadState('networkidle');
      await expect(page).toHaveScreenshot(`dashboard-home-${theme}.png`, { fullPage: true });
    });

    test(`Positions baseline — ${theme} theme`, async ({ page }) => {
      await setTheme(page, theme);
      await page.goto('/#/positions');
      await page.waitForLoadState('networkidle');
      await expect(page).toHaveScreenshot(`positions-${theme}.png`, { fullPage: true });
    });

    test(`TradePlan baseline — ${theme} theme`, async ({ page }) => {
      await setTheme(page, theme);
      await page.goto('/#/TradePlan?ticker=AAPL&market=US');
      await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
      await expect(page).toHaveScreenshot(`trade-plan-${theme}.png`, { fullPage: true });
    });

    test(`Settings baseline — ${theme} theme`, async ({ page }) => {
      await setTheme(page, theme);
      await page.goto('/#/Settings');
      await page.waitForLoadState('networkidle');
      await expect(page).toHaveScreenshot(`settings-${theme}.png`, { fullPage: true });
    });
  }
});

// ---------------------------------------------------------------------------
// Chart-heavy component baseline — PerformanceAnalytics (recharts
// AreaChart/BarChart/ScatterChart/ComposedChart via UnderwaterChart +
// TimeBasedCharts)
// ---------------------------------------------------------------------------

test.describe('Visual regression baseline — chart-heavy component (ST-18)', () => {
  for (const theme of ['dark', 'light']) {
    test(`PerformanceAnalytics baseline (recharts charts) — ${theme} theme`, async ({ page }) => {
      await setTheme(page, theme);
      await setupAnalytics(page);
      // Wait for the recharts SVGs to actually paint before capturing —
      // ResponsiveContainer renders 0x0 for one frame before measuring
      // its parent, which would otherwise make the baseline flaky.
      await expect(page.locator('.recharts-wrapper svg').first()).toBeVisible({ timeout: 10000 });
      await expect(page).toHaveScreenshot(`performance-analytics-${theme}.png`, { fullPage: true });
    });
  }
});
