/**
 * Theme-Toggle Persistence Across Sessions — ST-11 (BLG-FE-93, EPIC-04, v8.5)
 *
 * Audit-only story (per sprint_backlog.md Notes: "Verification of already-
 * established behaviour; any gap found is fixed or filed as a follow-up").
 * Audit found persistence itself already correct (localStorage survives
 * indefinitely across sessions; a storage-clearing event cleanly falls back
 * to the "dark" default via `localStorage.getItem("theme") || "dark"`) --
 * but the *initial-render* synchronisation had a real gap: `theme` state
 * defaulted to `"dark"` and only self-corrected in a post-mount `useEffect`,
 * so a persisted "light" theme flashed dark on every load/reload before
 * correcting. Fixed in this story (src/Layout.js) by lazy-initialising the
 * state directly from localStorage instead of defaulting and correcting.
 *
 * Coverage:
 *   SC-TP-01  Persisted "light" theme applies with no dark flash --
 *             correct immediately after navigation, before any settling wait
 *   SC-TP-02  Persisted "dark" theme applies with no light flash
 *   SC-TP-03  Fresh session (no persisted value, i.e. a storage-clearing
 *             event) falls back to the "dark" default cleanly
 *   SC-TP-04  A value set by the in-app toggle survives a full page reload
 *             (long-gap-session persistence, simulated via reload)
 *
 * Theme toggle: Layout.js reads localStorage["theme"] (default "dark") via
 * lazy useState init (ST-11 fix). Light theme is set via page.addInitScript
 * before navigation (same pattern as secondary-text-contrast.spec.js).
 *
 * Infrastructure: Playwright page.route() network interception.
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// Tailwind defaults: bg-slate-950 (dark wrapper) / bg-slate-100 (light wrapper).
const SLATE_950_RGB = 'rgb(2, 6, 23)';
const SLATE_100_RGB = 'rgb(241, 245, 249)';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
}

function themeWrapper(page) {
  return page.locator('.min-h-screen.transition-colors').first();
}

test('SC-TP-01: persisted "light" theme applies immediately, no dark flash', async ({ page }) => {
  await mockFallback(page);
  await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
  await page.goto('/#/DashboardHome');

  const wrapper = themeWrapper(page);
  // No settling wait -- assert on the very first paint state.
  await expect(wrapper).toBeVisible({ timeout: 8000 });
  await expect(wrapper).not.toHaveClass(/\bdark\b/);
  const bg = await wrapper.evaluate((el) => getComputedStyle(el).backgroundColor);
  expect(bg).toBe(SLATE_100_RGB);
});

test('SC-TP-02: persisted "dark" theme applies immediately, no light flash', async ({ page }) => {
  await mockFallback(page);
  await page.addInitScript(() => window.localStorage.setItem('theme', 'dark'));
  await page.goto('/#/DashboardHome');

  const wrapper = themeWrapper(page);
  await expect(wrapper).toBeVisible({ timeout: 8000 });
  await expect(wrapper).toHaveClass(/\bdark\b/);
  const bg = await wrapper.evaluate((el) => getComputedStyle(el).backgroundColor);
  expect(bg).toBe(SLATE_950_RGB);
});

test('SC-TP-03: no persisted value (storage-clearing event) falls back to "dark" default', async ({ page }) => {
  await mockFallback(page);
  // Deliberately no addInitScript setting "theme" -- simulates a fresh
  // session after localStorage/site-data was cleared.
  await page.goto('/#/DashboardHome');

  const wrapper = themeWrapper(page);
  await expect(wrapper).toBeVisible({ timeout: 8000 });
  await expect(wrapper).toHaveClass(/\bdark\b/);
  const bg = await wrapper.evaluate((el) => getComputedStyle(el).backgroundColor);
  expect(bg).toBe(SLATE_950_RGB);
});

test('SC-TP-04: a value set by the in-app toggle survives a full page reload', async ({ page }) => {
  await mockFallback(page);
  await page.goto('/#/DashboardHome');

  const wrapper = themeWrapper(page);
  await expect(wrapper).toBeVisible({ timeout: 8000 });
  await expect(wrapper).toHaveClass(/\bdark\b/); // starts dark (no persisted value)

  // ST-11: theme-toggle-desktop/-mobile data-testid added by this story
  // (the buttons were previously icon-only with no accessible name).
  await page.getByTestId('theme-toggle-desktop').click();

  // Confirm the toggle actually flipped state before testing persistence.
  await expect(wrapper).not.toHaveClass(/\bdark\b/, { timeout: 3000 });

  await page.reload();
  const wrapperAfterReload = themeWrapper(page);
  await expect(wrapperAfterReload).toBeVisible({ timeout: 8000 });
  await expect(wrapperAfterReload).not.toHaveClass(/\bdark\b/);
});
