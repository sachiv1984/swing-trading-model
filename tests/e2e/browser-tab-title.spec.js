/**
 * v9.15 ST-13 (BLG-FE-249, EPIC-02) — a browser-tab title for each page.
 *
 * Design source: docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md §3.2, §6
 * Spec: navigation.md §Browser Tab Title; labels: glossary.md §UI Labels (src/lib/pageLabels.js)
 *
 *   SC-BTT-01  Positions: "Positions · Position Manager"
 *   SC-BTT-02  Trade History: "Trade History · Position Manager"
 *   SC-BTT-03  Research with a ticker: "AAPL · Research · Position Manager" (UK ".L" dropped, as in the heading)
 *   SC-BTT-04  Navigating between pages updates the title, and each routed page's title is distinct
 *   SC-BTT-05  A detail route under another page's Layout key gets its own label (Notification History)
 *   SC-BTT-06  An unknown route: "Page not found · Position Manager"
 *   SC-BTT-07  A malformed Research URL does not crash the app (BLG-FE-273, PR #2191 review)
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

test.beforeEach(async ({ page }) => {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
});

test('SC-BTT-01: Positions sets "Positions · Position Manager"', async ({ page }) => {
  await page.goto('/#/Positions');
  await expect(page).toHaveTitle('Positions · Position Manager', { timeout: 10000 });
});

test('SC-BTT-02: Trade History sets "Trade History · Position Manager"', async ({ page }) => {
  await page.goto('/#/TradeHistory');
  await expect(page).toHaveTitle('Trade History · Position Manager', { timeout: 10000 });
});

test('SC-BTT-03: a Research page includes its ticker', async ({ page }) => {
  await page.goto('/#/research/AAPL');
  await expect(page).toHaveTitle('AAPL · Research · Position Manager', { timeout: 10000 });
  await page.goto('/#/research/LGEN.L');
  await expect(page).toHaveTitle('LGEN · Research · Position Manager', { timeout: 10000 });
});

test('SC-BTT-04: navigating updates the title, and routed pages get distinct titles', async ({ page }) => {
  const seen = new Set();
  for (const [hash, title] of [
    ['/#/', 'Dashboard · Position Manager'],
    ['/#/Signals', 'Signals · Position Manager'],
    ['/#/PerformanceAnalytics', 'Analytics · Position Manager'],
    ['/#/TradePlan', 'Trade Plan · Position Manager'],
  ]) {
    await page.goto(hash);
    await expect(page).toHaveTitle(title, { timeout: 10000 });
    seen.add(await page.title());
  }
  expect(seen.size).toBe(4);
});

test('SC-BTT-05: Notification History has its own title', async ({ page }) => {
  await page.goto('/#/notifications/history');
  await expect(page).toHaveTitle('Notification History · Position Manager', { timeout: 10000 });
});

test('SC-BTT-06: an unknown route sets "Page not found · Position Manager"', async ({ page }) => {
  await page.goto('/#/NoSuchPage');
  await expect(page).toHaveTitle('Page not found · Position Manager', { timeout: 10000 });
});

test('SC-BTT-07: a malformed Research URL renders the page instead of crashing (BLG-FE-273)', async ({ page }) => {
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(e.message));
  await page.goto('/#/research/%E0%A4%A');
  await expect(page).toHaveTitle(/ · Research · Position Manager$/, { timeout: 10000 });
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  expect(pageErrors.filter((m) => /URI malformed/i.test(m))).toEqual([]);
});
