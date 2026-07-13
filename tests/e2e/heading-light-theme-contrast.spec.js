/**
 * Page-Title Light-Theme Contrast — ST-08 (EPIC-02, v7.0) — BLG-FE-95
 *
 * Covers the observable AC for the Dashboard/StrategyBenchmark primary
 * page-title contrast fix: both headings switch from bare `text-white`
 * (invisible on light theme, ~1.1:1 contrast) to `text-slate-900 dark:text-white`.
 *
 *   SC-HTC-01  Dashboard "Dashboard" h1 — dark theme: resolves to white (unchanged)
 *   SC-HTC-02  Dashboard "Dashboard" h1 — light theme: resolves to slate-900 (fixed)
 *   SC-HTC-03  StrategyBenchmark "Strategy Benchmark" h1 — dark theme: resolves to white (unchanged)
 *   SC-HTC-04  StrategyBenchmark "Strategy Benchmark" h1 — light theme: resolves to slate-900 (fixed)
 *
 * Design source: docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md
 * Spec refs: docs/specs/frontend/pages/dashboard.md §Page Header (v2.8),
 *            docs/specs/frontend/pages/strategy_benchmark.md §2 (v0.3)
 *
 * Theme toggle: Layout.js reads localStorage["theme"] (default "dark") on mount.
 * Light theme is set via page.addInitScript before navigation (same pattern as
 * secondary-text-contrast.spec.js).
 *
 * Infrastructure: Playwright page.route() network interception, catch-all
 * fallback for any endpoint not explicitly stubbed (page content beyond the
 * static h1 heading is out of scope for this test — same approach as
 * morning-briefing.spec.js's mockFallback).
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const SLATE_900_RGB = 'rgb(15, 23, 42)';
const WHITE_RGB = 'rgb(255, 255, 255)';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
}

test.describe('Dashboard heading contrast (SC-HTC-01/02)', () => {
  test('SC-HTC-01: Dashboard h1 resolves to white in dark theme (unchanged)', async ({ page }) => {
    await mockFallback(page);
    await page.goto('/#/DashboardHome');

    const heading = page.locator('h1', { hasText: 'Dashboard' });
    await expect(heading).toBeVisible({ timeout: 8000 });
    const color = await heading.evaluate((el) => getComputedStyle(el).color);
    expect(color).toBe(WHITE_RGB);
  });

  test('SC-HTC-02: Dashboard h1 resolves to slate-900 in light theme (fixed)', async ({ page }) => {
    await mockFallback(page);
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await page.goto('/#/DashboardHome');

    const heading = page.locator('h1', { hasText: 'Dashboard' });
    await expect(heading).toBeVisible({ timeout: 8000 });
    const color = await heading.evaluate((el) => getComputedStyle(el).color);
    expect(color).toBe(SLATE_900_RGB);
    expect(color).not.toBe(WHITE_RGB);
  });
});

test.describe('Strategy Benchmark heading contrast (SC-HTC-03/04)', () => {
  test('SC-HTC-03: Strategy Benchmark h1 resolves to white in dark theme (unchanged)', async ({ page }) => {
    await mockFallback(page);
    await page.goto('/#/StrategyBenchmark');

    const heading = page.locator('h1', { hasText: 'Strategy Benchmark' });
    await expect(heading).toBeVisible({ timeout: 8000 });
    const color = await heading.evaluate((el) => getComputedStyle(el).color);
    expect(color).toBe(WHITE_RGB);
  });

  test('SC-HTC-04: Strategy Benchmark h1 resolves to slate-900 in light theme (fixed)', async ({ page }) => {
    await mockFallback(page);
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await page.goto('/#/StrategyBenchmark');

    const heading = page.locator('h1', { hasText: 'Strategy Benchmark' });
    await expect(heading).toBeVisible({ timeout: 8000 });
    const color = await heading.evaluate((el) => getComputedStyle(el).color);
    expect(color).toBe(SLATE_900_RGB);
    expect(color).not.toBe(WHITE_RGB);
  });
});
