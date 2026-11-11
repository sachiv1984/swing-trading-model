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
 *   SC-PHDG-01  Watchlist "Watchlist" h1 — dark theme: solid white title, no
 *               gradient (ST-09, v9.16 — was: via-stop resolves to slate-300)
 *   SC-PHDG-02  Watchlist "Watchlist" h1 — light theme: solid slate-900 title,
 *               no gradient (ST-09, v9.16 — was: via-stop remains slate-700)
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

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

// ST-09 (EPIC-03, v9.16, BLG-FE-264): PageHeader's title is no longer a
// gradient. It is solid `text-app-fg` (design_system.md v1.25 §Semantic Colour
// Tokens rule 5), so the v7.8 via-stop defect this file guarded can no longer
// occur. The two scenarios now check the solid title colour in each theme and
// that no gradient background remains; the gradient-stop form is in git history.
const WHITE_RGB = 'rgb(255, 255, 255)';
const SLATE_900_RGB = 'rgb(15, 23, 42)';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

test.describe('PageHeader title colour (SC-PHDG-01/02)', () => {
  test('SC-PHDG-01: dark theme title is solid white, with no gradient', async ({ page }) => {
    await mockFallback(page);
    await page.goto('/#/Watchlist');

    const heading = page.locator('h1', { hasText: 'Watchlist' });
    await expect(heading).toBeVisible({ timeout: 8000 });
    await expect(heading).toHaveCSS('color', WHITE_RGB);
    await expect(heading).toHaveCSS('background-image', 'none');
  });

  test('SC-PHDG-02: light theme title is solid slate-900, with no gradient', async ({ page }) => {
    await mockFallback(page);
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await page.goto('/#/Watchlist');

    const heading = page.locator('h1', { hasText: 'Watchlist' });
    await expect(heading).toBeVisible({ timeout: 8000 });
    await expect(heading).toHaveCSS('color', SLATE_900_RGB);
    await expect(heading).toHaveCSS('background-image', 'none');
  });
});
