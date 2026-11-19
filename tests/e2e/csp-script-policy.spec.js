/**
 * Content-Security-Policy script-src in the real built page (BLG-FE-325, 2026-11-19)
 *
 *   SC-CSPS-01  Loading the app with CSP enforced raises no script-src violation
 *   SC-CSPS-02  The GitHub Pages SPA redirect (public/spa-redirect.js) runs under the
 *               CSP: a /?/<path> URL from public/404.html is restored before the app loads
 *
 * Every other spec runs with bypassCSP: true (playwright.config.js), because the CSP's
 * connect-src blocks the localhost:8000 mocks. That is why BLG-FE-325 (an inline script
 * whose hash matched the source, not the minified build) was never seen. This file
 * turns the bypass off and listens for securitypolicyviolation events, ignoring
 * connect-src ones (the API mocks are expected to be blocked here).
 * The build-output companion check is scripts/check_csp_inline_scripts.py.
 *
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

test.use({ bypassCSP: false });

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    window.__cspViolations = [];
    document.addEventListener('securitypolicyviolation', (e) => {
      window.__cspViolations.push({ directive: e.effectiveDirective || e.violatedDirective, blocked: e.blockedURI, sample: e.sample });
    });
    window.localStorage.setItem('command-palette-tooltip-seen', 'true');
  });
});

const scriptViolations = (page) =>
  page.evaluate(() => window.__cspViolations.filter((v) => /^script-src/.test(v.directive)));

test('SC-CSPS-01: the built app raises no script-src CSP violation', async ({ page }) => {
  await page.goto('/#/DashboardHome');
  await expect(page.locator('main h1').first()).toBeVisible({ timeout: 15000 });
  expect(await scriptViolations(page)).toEqual([]);
});

test('SC-CSPS-02: the SPA redirect script runs under the CSP and restores the path', async ({ page }) => {
  // public/404.html sends /Positions to /?/Positions; spa-redirect.js turns it back.
  await page.goto('/?/Positions');
  await expect.poll(() => page.evaluate(() => window.location.search)).toBe('');
  expect(new URL(page.url()).pathname).toBe('/Positions');
  expect(await scriptViolations(page)).toEqual([]);
});
