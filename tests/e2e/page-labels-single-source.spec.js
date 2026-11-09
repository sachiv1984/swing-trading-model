/**
 * v9.15 ST-11 (BLG-FE-248, EPIC-02) — one name per page across sidebar, heading and palette.
 *
 * Spec: docs/reference/glossary.md §UI Labels (v1.3); rule: site-structure-phase1/decision_record.md §3.1
 * Label source in code: src/lib/pageLabels.js
 *
 *   SC-PL-01  For each page with a sidebar entry, the sidebar link text equals the page heading (AC 1)
 *   SC-PL-02  The command palette lists each palette page under the same label (AC 1), including
 *             the new Replay and Notifications entries
 *   SC-PL-03  The keyboard-shortcut legend uses "New position", not "New trade" (glossary trade/position rule)
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

// [route hash, canonical label] for every page with a sidebar entry
// (navigation.md v2.0 §Page Placement — 21 entries; ST-01, BLG-FE-250, v9.16
// added Research and Trade Plans). Deliberate differences (glossary §UI Labels)
// are not in this list: the Positions journal view keeps "Trade Journal".
const SIDEBAR_PAGES = [
  ['/#/', 'Dashboard'],
  ['/#/Positions', 'Positions'],
  ['/#/TradeEntry', 'Trade Entry'],
  ['/#/TradeHistory', 'Trade History'],
  ['/#/TradeReflection', 'Trade Reflections'],
  ['/#/RedFlagJournal', 'Red Flag Journal'],
  ['/#/PerformanceAnalytics', 'Analytics'],
  ['/#/StrategyBenchmark', 'Strategy Benchmark'],
  ['/#/Replay', 'Replay'],
  ['/#/RiskDashboard', 'Risk Dashboard'],
  ['/#/Signals', 'Signals'],
  ['/#/Reports', 'Reports'],
  ['/#/Screener', 'Screener'],
  ['/#/Watchlist', 'Watchlist'],
  ['/#/Research', 'Research'],
  ['/#/TradePlans', 'Trade Plans'],
  ['/#/TickerUniverse', 'Ticker Universe'],
  ['/#/Settings', 'Settings'],
  ['/#/SystemStatus', 'System Status'],
  ['/#/WeeklyDigest', 'Weekly Digest'],
  ['/#/notifications', 'Notifications'],
];

const PALETTE_ONLY_PAGES = [
  ['TradePlan', 'Trade Plan'],
];

test.beforeEach(async ({ page }) => {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(/localhost:8000\/notifications\?page=/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }) })
  );
});

for (const [hash, label] of SIDEBAR_PAGES) {
  test(`SC-PL-01: ${label} — sidebar label equals page heading`, async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(hash);
    await expect(page.getByRole('heading', { level: 1, name: label, exact: true })).toBeVisible({ timeout: 15000 });
    const sidebar = page.getByRole('complementary');
    const link = sidebar.getByRole('link', { name: label, exact: true }).first();
    // navigation.md v2.0 §Default Expansion: the active area is always expanded,
    // so the current page's own entry is visible without expanding anything.
    await expect(link).toBeVisible();
  });
}

test('SC-PL-02: the palette lists every palette page under its canonical label', async ({ page }) => {
  await page.goto('/#/Positions');
  await page.waitForLoadState('domcontentloaded');
  await page.keyboard.press('Control+k');
  const input = page.getByTestId('command-palette-input');
  await expect(input).toBeVisible();
  const all = [...SIDEBAR_PAGES.map(([, label]) => label), ...PALETTE_ONLY_PAGES.map(([, label]) => label)];
  for (const label of all) {
    await input.fill(label);
    await expect(page.getByRole('option', { name: label, exact: true })).toHaveCount(1);
  }
  // Superseded labels are gone.
  await input.fill('Trade Reflection');
  await expect(page.getByRole('option', { name: 'Trade Reflection', exact: true })).toHaveCount(0);
});

test('SC-PL-03: the shortcut legend says "New position"', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/#/Positions');
  await expect(page.getByText('New position', { exact: true })).toBeVisible({ timeout: 10000 });
  await expect(page.getByText('New trade', { exact: true })).toHaveCount(0);
});
