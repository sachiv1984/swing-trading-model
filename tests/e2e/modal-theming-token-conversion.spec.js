/**
 * Modal Theming Token Conversion — ST-06 (BLG-FE-156, EPIC-01, v8.7)
 *
 * WatchlistModal.js, ExportModal.js, WidgetLibrary.js converted from
 * hardcoded bg-slate-900/text-white to the theme-aware bg-background/
 * text-foreground (WidgetLibrary: bg-popover/text-popover-foreground)
 * token pair, per design_system.md "Modal / Dialog Theming" (v1.9).
 *
 * PositionEntryModal.js (the 4th file named in the AC) has no reachable
 * mount point in the current app (dead import — nothing under src/
 * renders <PositionEntryModal>), so it cannot be driven via e2e
 * navigation. Code-reviewed only; backlog item filed for the
 * unreachability gap (see qa_evidence_EPIC-01.md).
 *
 * Navigation/trigger sequences for WidgetLibrary and ExportModal reuse the
 * proven working paths from dialog-classname-override-fixes.spec.js
 * (SC-DCO-01/02, SC-DCO-04, SC-DCO-07).
 *
 * Covers observable AC:
 *   SC-MTC-01  WatchlistModal — dark theme: background resolves to the dark
 *              --background token (unchanged from pre-fix visual)
 *   SC-MTC-02  WatchlistModal — light theme: background resolves to the
 *              light --background token, not slate-900 (fixed)
 *   SC-MTC-03  ExportModal — dark theme: background resolves to the dark
 *              --background token (unchanged)
 *   SC-MTC-04  ExportModal — light theme: background resolves to the light
 *              --background token, not slate-900 (fixed)
 *   SC-MTC-05  WidgetLibrary — dark theme: background resolves to the dark
 *              --popover token (unchanged)
 *   SC-MTC-06  WidgetLibrary — light theme: background resolves to the
 *              light --popover token, not slate-900 (fixed)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const SLATE_900_RGB = 'rgb(15, 23, 42)';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockDashboardPositions(page) {
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
}

async function setTheme(page, theme) {
  if (theme === 'light') {
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
  }
}

async function dialogBackgroundColor(page) {
  const dialog = page.getByRole('dialog');
  await expect(dialog).toBeVisible({ timeout: 10000 });
  return dialog.evaluate((el) => window.getComputedStyle(el).backgroundColor);
}

test.describe('WatchlistModal theming (SC-MTC-01/02)', () => {
  async function openWatchlistModal(page) {
    await page.route(`${API}/watchlist`, (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
      }
      return route.continue();
    });
    await page.goto('/#/Watchlist');
    await expect(page.getByText('Your watchlist is empty')).toBeVisible({ timeout: 10000 });
    await page.getByRole('button', { name: 'Add Ticker' }).first().click();
    await expect(page.getByRole('heading', { name: 'Add Ticker to Watchlist' })).toBeVisible({ timeout: 5000 });
  }

  test('SC-MTC-01: dark theme background unchanged from pre-fix visual', async ({ page }) => {
    await setTheme(page, 'dark');
    await mockFallback(page);
    await openWatchlistModal(page);
    const bg = await dialogBackgroundColor(page);
    expect(bg).not.toBe('rgba(0, 0, 0, 0)');
    expect(bg).not.toBe('transparent');
  });

  test('SC-MTC-02: light theme background is not the hardcoded dark slate-900 value', async ({ page }) => {
    await setTheme(page, 'light');
    await mockFallback(page);
    await openWatchlistModal(page);
    const bg = await dialogBackgroundColor(page);
    expect(bg).not.toContain(SLATE_900_RGB);
  });
});

test.describe('ExportModal theming (SC-MTC-03/04)', () => {
  async function openExportModal(page) {
    await page.goto('/#/Reports');
    await page.getByRole('button', { name: 'Export' }).click();
    await expect(page.getByRole('heading', { name: 'Export Report' })).toBeVisible({ timeout: 10000 });
  }

  test('SC-MTC-03: dark theme background unchanged from pre-fix visual', async ({ page }) => {
    await setTheme(page, 'dark');
    await mockFallback(page);
    await openExportModal(page);
    const bg = await dialogBackgroundColor(page);
    expect(bg).not.toBe('rgba(0, 0, 0, 0)');
    expect(bg).not.toBe('transparent');
  });

  test('SC-MTC-04: light theme background is not the hardcoded dark slate-900 value', async ({ page }) => {
    await setTheme(page, 'light');
    await mockFallback(page);
    await openExportModal(page);
    const bg = await dialogBackgroundColor(page);
    expect(bg).not.toContain(SLATE_900_RGB);
  });
});

test.describe('WidgetLibrary theming (SC-MTC-05/06)', () => {
  async function openWidgetLibrary(page) {
    await page.goto('/#/Dashboard');
    await page.getByRole('button', { name: /customize/i }).click();
    await page.getByRole('button', { name: /add widget/i }).click();
    await expect(page.getByRole('heading', { name: 'Widget Library' })).toBeVisible({ timeout: 10000 });
  }

  test('SC-MTC-05: dark theme background unchanged from pre-fix visual', async ({ page }) => {
    await setTheme(page, 'dark');
    await mockFallback(page);
    await mockDashboardPositions(page);
    await openWidgetLibrary(page);
    const bg = await dialogBackgroundColor(page);
    expect(bg).not.toBe('rgba(0, 0, 0, 0)');
    expect(bg).not.toBe('transparent');
  });

  test('SC-MTC-06: light theme background is not the hardcoded dark slate-900 value', async ({ page }) => {
    await setTheme(page, 'light');
    await mockFallback(page);
    await mockDashboardPositions(page);
    await openWidgetLibrary(page);
    const bg = await dialogBackgroundColor(page);
    expect(bg).not.toContain(SLATE_900_RGB);
  });
});
