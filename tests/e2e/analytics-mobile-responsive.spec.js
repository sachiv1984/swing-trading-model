/**
 * PerformanceAnalytics Mobile Responsive Audit — ST-12 (BLG-FE-94, EPIC-04, v8.5)
 *
 * Audit against docs/specs/frontend/pages/analytics.md §Responsive Behavior
 * found 4 real drift instances (fixed in this story, not just filed --
 * corrective-only per Design Pre-Approved, `analytics.md` v2.0):
 *
 *   1. TimeBasedCharts.js's "Day of Week" grid was a fixed 5-column grid
 *      with no mobile breakpoint (each cell ~69px at 375px viewport width,
 *      genuinely cramped) -- now grid-cols-3 sm:grid-cols-5.
 *   2. MonthlyHeatmap.js's trade-drilldown modal table had no
 *      overflow-x-auto (spec: "All tables support horizontal scroll on
 *      small screens") -- 4 sibling table components already had it.
 *   3. RMultipleAnalysis.js's "R-Multiple by Tag" table had the same
 *      missing overflow-x-auto gap.
 *   4. PerformanceAnalytics.js's period-selector + export-button header row
 *      was a bare `flex gap-2` with no stacking (spec: "Period selector and
 *      export button stack or compress at smaller widths") -- now
 *      flex-col sm:flex-row, matching PageHeader's own convention.
 *
 * Infrastructure: reuses chart-interactivity.spec.js's setupAnalytics()
 * mock-data pattern (ALL_TRADES / ANALYTICS_SETTINGS fixtures).
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');
const { ALL_TRADES, ANALYTICS_SETTINGS } = require('./mocks/analytics-mock-data');

const API_BASE = 'http://localhost:8000';
const MOBILE_VIEWPORT = { width: 375, height: 812 }; // iPhone-class width

async function setupAnalytics(page) {
  await page.route(new RegExp(`${API_BASE}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API_BASE}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ALL_TRADES) })
  );
  await page.route(`${API_BASE}/settings`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ANALYTICS_SETTINGS) })
  );
  await page.goto('/#/PerformanceAnalytics');
  await expect(
    page.locator('h1, [class*="text-2xl"], [class*="text-3xl"]').filter({ hasText: 'Performance Analytics' })
  ).toBeVisible({ timeout: 20000 });
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 15000 });

  // Switch to All Time so trades from all months are visible (Radix UI select) --
  // default timePeriod is "last_month", which filters ALL_TRADES down to zero
  // rows (mock dates aren't necessarily within "last month" of the CI run time),
  // triggering the "not enough trades" empty state instead of the real dashboard.
  // Same pattern as chart-interactivity.spec.js's setupAnalytics() -- omitting
  // this step was a real bug in this file caught by real CI (all 4 mobile/
  // desktop-regression tests failed with "element(s) not found" since none of
  // TimeBasedCharts/MonthlyHeatmap/RMultipleAnalysis ever rendered).
  const trigger = page.locator('[class*="SelectTrigger"], button[role="combobox"]').first();
  await trigger.click();
  await page.locator('[role="option"]').filter({ hasText: 'All Time' }).click();
  await page.waitForTimeout(500);
}

test.describe('ST-12 mobile responsive fixes', () => {
  test.use({ viewport: MOBILE_VIEWPORT });

  test('SC-PA-M01: Day-of-Week grid uses 3 columns at mobile width, not the pre-fix fixed 5', async ({ page }) => {
    await setupAnalytics(page);

    const grid = page.locator('h3', { hasText: 'Time-Based Analysis' })
      .locator('xpath=following::div[contains(@class,"grid-cols-3")][1]');
    await expect(grid).toBeVisible({ timeout: 10000 });
    const columns = await grid.evaluate((el) => getComputedStyle(el).gridTemplateColumns.split(' ').length);
    expect(columns).toBe(3);
  });

  test('SC-PA-M02: MonthlyHeatmap drill-down modal table scrolls horizontally at mobile width', async ({ page }) => {
    await setupAnalytics(page);

    const tile = page.locator('[class*="aspect-square"]').filter({ hasText: '2026-01' });
    await expect(tile).toBeVisible({ timeout: 10000 });
    await tile.click();
    await expect(page.locator('[data-testid="heatmap-modal"]')).toBeVisible({ timeout: 5000 });

    const scrollContainer = page.locator('[data-testid="heatmap-modal"] table').locator('xpath=ancestor::div[contains(@class,"overflow-y-auto")][1]');
    await expect(scrollContainer).toBeVisible();
    const overflowX = await scrollContainer.evaluate((el) => getComputedStyle(el).overflowX);
    expect(overflowX).toBe('auto');
  });

  test('SC-PA-M03: R-Multiple by Tag table scrolls horizontally at mobile width', async ({ page }) => {
    await setupAnalytics(page);

    const expandButton = page.getByRole('button', { name: /r-multiple by tag/i });
    await expect(expandButton).toBeVisible({ timeout: 10000 });
    await expandButton.click();

    // ST-12 CI fix: TagPerformance.js renders its own separate table with a
    // "Tag" column header on the same page, so a bare `th:has-text("Tag")`
    // filter is ambiguous (strict-mode violation, 2 matches). Scope to the
    // table immediately following the expand button instead.
    const table = expandButton.locator('xpath=following::table[1]');
    await expect(table).toBeVisible({ timeout: 5000 });
    const scrollContainer = table.locator('xpath=ancestor::div[contains(@class,"overflow-x-auto")][1]');
    await expect(scrollContainer).toBeVisible();
    const overflowX = await scrollContainer.evaluate((el) => getComputedStyle(el).overflowX);
    expect(overflowX).toBe('auto');
  });

  test('SC-PA-M04: period-selector/export-button header stacks vertically at mobile width', async ({ page }) => {
    await setupAnalytics(page);

    const actionsRow = page.locator('div.flex.flex-col').filter({ has: page.getByRole('button', { name: /export pdf/i }) }).first();
    await expect(actionsRow).toBeVisible({ timeout: 10000 });
    const flexDirection = await actionsRow.evaluate((el) => getComputedStyle(el).flexDirection);
    expect(flexDirection).toBe('column');
  });
});

test.describe('ST-12 desktop regression (no change at lg width)', () => {
  test('SC-PA-M05: Day-of-Week grid uses 5 columns at desktop width (unchanged)', async ({ page }) => {
    await setupAnalytics(page);

    const grid = page.locator('h3', { hasText: 'Time-Based Analysis' })
      .locator('xpath=following::div[contains(@class,"grid-cols-3")][1]');
    await expect(grid).toBeVisible({ timeout: 10000 });
    const columns = await grid.evaluate((el) => getComputedStyle(el).gridTemplateColumns.split(' ').length);
    expect(columns).toBe(5);
  });

  test('SC-PA-M06: period-selector/export-button header stays horizontal at desktop width (unchanged)', async ({ page }) => {
    await setupAnalytics(page);

    const actionsRow = page.locator('div.flex.flex-col').filter({ has: page.getByRole('button', { name: /export pdf/i }) }).first();
    await expect(actionsRow).toBeVisible({ timeout: 10000 });
    const flexDirection = await actionsRow.evaluate((el) => getComputedStyle(el).flexDirection);
    expect(flexDirection).toBe('row');
  });
});
