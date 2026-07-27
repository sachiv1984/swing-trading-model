/**
 * Page-Title Dark-Theme Gradient Contrast — ST-04 (EPIC-04, v7.8) — BLG-FE-125
 *
 * Covers the observable AC for the consolidated dark-mode contrast audit's
 * single finding: `PageHeader.js`'s title gradient had `dark:from-white
 * dark:to-slate-400` overrides but no `dark:via-` pairing, so the middle
 * gradient stop fell through to the light-mode `via-slate-700` value in dark
 * theme — a washed-out/low-contrast segment in the heading gradient text on
 * nearly every page (`PageHeader` is used by 21 of 23 shipped pages).
 *
 *   SC-PHDG-01  Watchlist "Watchlist" h1 — dark theme: via-stop resolves to
 *               slate-300 (fixed), not slate-700 (defect)
 *   SC-PHDG-02  Watchlist "Watchlist" h1 — light theme: via-stop remains
 *               slate-700 (unchanged — light theme was never broken)
 *
 * Design source: docs/design/2026-07-24__release-v7.8/base44-dark-mode-contrast-audit/decision_record.md
 * Spec ref: docs/specs/frontend/design_system.md §Card Hierarchy / §Accessibility (v1.4)
 *
 * Theme toggle: Layout.js reads localStorage["theme"] (default "dark") on mount.
 * Light theme is set via page.addInitScript before navigation (same pattern as
 * heading-light-theme-contrast.spec.js).
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// Tailwind default palette, resolved to rgb() as the browser reports it.
const SLATE_700_RGB = '51, 65, 85';   // via-slate-700 (light-mode value, and the pre-fix dark-mode defect)
const SLATE_300_RGB = '203, 213, 225'; // dark:via-slate-300 (the fix)

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

test.describe('PageHeader gradient via-stop contrast (SC-PHDG-01/02)', () => {
  test('SC-PHDG-01: dark theme resolves via-stop to slate-300 (fixed), not slate-700', async ({ page }) => {
    await mockFallback(page);
    await page.goto('/#/Watchlist');

    const heading = page.locator('h1', { hasText: 'Watchlist' });
    await expect(heading).toBeVisible({ timeout: 8000 });
    const backgroundImage = await heading.evaluate((el) => getComputedStyle(el).backgroundImage);
    expect(backgroundImage).toContain(SLATE_300_RGB);
    expect(backgroundImage).not.toContain(SLATE_700_RGB);
  });

  test('SC-PHDG-02: light theme via-stop remains slate-700 (unchanged)', async ({ page }) => {
    await mockFallback(page);
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await page.goto('/#/Watchlist');

    const heading = page.locator('h1', { hasText: 'Watchlist' });
    await expect(heading).toBeVisible({ timeout: 8000 });
    const backgroundImage = await heading.evaluate((el) => getComputedStyle(el).backgroundImage);
    expect(backgroundImage).toContain(SLATE_700_RGB);
  });
});
