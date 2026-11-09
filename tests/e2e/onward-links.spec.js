/**
 * Onward Links on Dead-End Pages — ST-03 (EPIC-01, v9.16, BLG-FE-252)
 *
 * navigation.md v2.0 §Onward Links: every page has at least one in-page link
 * to the next page a user is likely to need, beyond the sidebar. The v2.0 scan
 * found 11 dead-end pages (8 in BLG-FE-252 plus Settings, Trade History and
 * Analytics — stage4_backlog_slice_addendum.md). Each gets the link the table
 * names; Notification History's is its parent link (ST-02, parent-links.spec.js).
 *
 * Scenarios (one per new link — presence, href, click lands on the target):
 *   SC-ONW-01  Ticker Universe → Screener
 *   SC-ONW-02  Trade History → Research for a trade's ticker
 *   SC-ONW-03  Analytics → Trade History (populated state)
 *   SC-ONW-04  Reports → Analytics
 *   SC-ONW-05  Strategy Benchmark → Analytics
 *   SC-ONW-06  Replay → Trade History
 *   SC-ONW-07  Trade Reflections → Trade History
 *   SC-ONW-08  Red Flag Journal → Trade History filtered to the event's ticker
 *   SC-ONW-09  Trade History ?ticker= filter shows only that ticker; "Show all trades" clears it
 *   SC-ONW-10  Settings → Notification Preferences
 *   SC-ONW-11  System Status → Settings
 *   SC-ONW-12  Dead-end scan re-run over the 11 former dead-end pages: 0 dead ends
 *
 * Infrastructure: page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate with page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const TRADES = [
  { id: 't-1', ticker: 'AAPL', market: 'US', entry_date: '2026-09-01', exit_date: '2026-09-20', entry_price: 100, exit_price: 110, shares: 10, pnl: 100, pnl_percent: 10, exit_reason: 'Target', tags: [] },
  { id: 't-2', ticker: 'VOD.L', market: 'UK', entry_date: '2026-09-02', exit_date: '2026-09-21', entry_price: 70, exit_price: 65, shares: 100, pnl: -500, pnl_percent: -7.1, exit_reason: 'Stop Loss', tags: [] },
];

const RED_FLAG_EVENTS = {
  status: 'ok',
  data: {
    items: [
      { id: 'e-1', event_type: 'stop_widened', ticker: 'VOD.L', created_at: new Date(Date.now() - 3600e3).toISOString(), context: {} },
    ],
    total: 1,
    page: 1,
    page_size: 20,
  },
};

async function stubAll(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(/localhost:8000\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { evaluations: [], total: 0 } }) })
  );
  await page.route(/localhost:8000\/notifications\?/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }) })
  );
  await page.route(/localhost:8000\/notifications\/preferences/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { preferences: [] } }) })
  );
}

async function stubTrades(page) {
  await page.route(/localhost:8000\/trades(\?|$)/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { trades: TRADES } }) })
  );
}

test.beforeEach(async ({ page }) => {
  await stubAll(page);
});

/** Header onward link: visible, right text/href, click lands on the target heading. */
async function checkOnward(page, { from, heading, label, href, lands, targetHeading }) {
  await page.goto(from);
  await expect(page.getByRole('heading', { level: 1, name: heading, exact: true })).toBeVisible({ timeout: 15000 });
  const link = page.locator('main').getByTestId('onward-link');
  await expect(link).toHaveCount(1);
  await expect(link).toHaveText(label);
  await expect(link).toHaveAttribute('href', href);
  await link.click();
  await expect(page).toHaveURL(lands);
  await expect(page.getByRole('heading', { level: 1, name: targetHeading, exact: true })).toBeVisible({ timeout: 15000 });
}

test('SC-ONW-01: Ticker Universe links onward to Screener', async ({ page }) => {
  await checkOnward(page, { from: '/#/TickerUniverse', heading: 'Ticker Universe', label: 'Screener', href: '#/Screener', lands: /#\/Screener$/, targetHeading: 'Screener' });
});

test('SC-ONW-02: a Trade History row links its ticker to Research', async ({ page }) => {
  await stubTrades(page);
  await page.goto('/#/TradeHistory');
  const links = page.getByTestId('trade-ticker-research-link');
  await expect(links).toHaveCount(2, { timeout: 15000 });
  await expect(page.getByRole('link', { name: 'Research VOD', exact: true })).toHaveAttribute('href', '#/research/VOD.L');
  // The ticker text itself still expands the row (it is not the link).
  await expect(page.getByRole('link', { name: 'AAPL', exact: true })).toHaveCount(0);
  await page.getByRole('link', { name: 'Research AAPL', exact: true }).click();
  await expect(page).toHaveURL(/#\/research\/AAPL$/);
  await expect(page.getByRole('heading', { level: 1, name: 'AAPL — Research', exact: true })).toBeVisible({ timeout: 15000 });
});

test('SC-ONW-03: Analytics (populated) links onward to Trade History', async ({ page }) => {
  // Populated analytics: enough closed trades for the main view.
  const many = Array.from({ length: 12 }, (_, i) => ({ ...TRADES[0], id: `t-${i}`, exit_date: `2026-09-${String(10 + i).padStart(2, '0')}` }));
  await page.route(/localhost:8000\/trades(\?|$)/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { trades: many } }) })
  );
  await page.goto('/#/PerformanceAnalytics');
  await expect(page.getByRole('heading', { level: 1, name: 'Analytics', exact: true })).toBeVisible({ timeout: 15000 });
  const link = page.locator('main').getByTestId('onward-link');
  await expect(link).toHaveCount(1);
  await expect(link).toHaveText('Trade History');
  await expect(link).toHaveAttribute('href', '#/TradeHistory');
  await link.click();
  await expect(page).toHaveURL(/#\/TradeHistory$/);
});

test('SC-ONW-04: Reports links onward to Analytics', async ({ page }) => {
  await checkOnward(page, { from: '/#/Reports', heading: 'Reports', label: 'Analytics', href: '#/PerformanceAnalytics', lands: /#\/PerformanceAnalytics$/, targetHeading: 'Analytics' });
});

test('SC-ONW-05: Strategy Benchmark links onward to Analytics', async ({ page }) => {
  await checkOnward(page, { from: '/#/StrategyBenchmark', heading: 'Strategy Benchmark', label: 'Analytics', href: '#/PerformanceAnalytics', lands: /#\/PerformanceAnalytics$/, targetHeading: 'Analytics' });
});

test('SC-ONW-06: Replay links onward to Trade History', async ({ page }) => {
  await checkOnward(page, { from: '/#/Replay', heading: 'Replay', label: 'Trade History', href: '#/TradeHistory', lands: /#\/TradeHistory$/, targetHeading: 'Trade History' });
});

test('SC-ONW-07: Trade Reflections links onward to Trade History', async ({ page }) => {
  await checkOnward(page, { from: '/#/TradeReflection', heading: 'Trade Reflections', label: 'Trade History', href: '#/TradeHistory', lands: /#\/TradeHistory$/, targetHeading: 'Trade History' });
});

test('SC-ONW-08: a Red Flag Journal event links to Trade History filtered to its ticker', async ({ page }) => {
  await page.route(/localhost:8000\/portfolio\/red-flag-journal/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RED_FLAG_EVENTS) })
  );
  await stubTrades(page);
  await page.goto('/#/RedFlagJournal');
  const link = page.getByTestId('event-trade-history-link');
  await expect(link).toHaveCount(1, { timeout: 15000 });
  await expect(link).toHaveText('Trade History');
  await expect(link).toHaveAttribute('href', '#/TradeHistory?ticker=VOD.L');
  await link.click();
  await expect(page).toHaveURL(/#\/TradeHistory\?ticker=VOD\.L$/);
  await expect(page.getByTestId('trade-history-ticker-filter')).toContainText('VOD');
  await expect(page.getByTestId('trade-ticker-research-link')).toHaveCount(1);
});

test('SC-ONW-09: the Trade History ?ticker= filter can be cleared', async ({ page }) => {
  await stubTrades(page);
  await page.goto('/#/TradeHistory?ticker=aapl');
  await expect(page.getByTestId('trade-history-ticker-filter')).toContainText('AAPL', { timeout: 15000 });
  await expect(page.getByTestId('trade-ticker-research-link')).toHaveCount(1);
  await page.getByTestId('trade-history-ticker-filter-clear').click();
  await expect(page.getByTestId('trade-history-ticker-filter')).toHaveCount(0);
  await expect(page.getByTestId('trade-ticker-research-link')).toHaveCount(2);
  await expect(page).toHaveURL(/#\/TradeHistory$/);
});

test('SC-ONW-10: Settings links onward to Notification Preferences', async ({ page }) => {
  await checkOnward(page, { from: '/#/Settings', heading: 'Settings', label: 'Notification Preferences', href: '#/notifications/preferences', lands: /#\/notifications\/preferences$/, targetHeading: 'Notification Preferences' });
});

test('SC-ONW-11: System Status links onward to Settings', async ({ page }) => {
  await checkOnward(page, { from: '/#/SystemStatus', heading: 'System Status', label: 'Settings', href: '#/Settings', lands: /#\/Settings$/, targetHeading: 'Settings' });
});

// ---------------------------------------------------------------------------
// SC-ONW-12 — Re-run of the inter-page link scan over the 11 pages the v2.0
// scan found to be dead ends (navigation.md §Onward Links; addendum to
// ST-03). For each, count in-page links inside <main> whose target is another
// route, in the page's normal populated state. The other 14 pages were already
// "Exists" in the v2.0 scan and are unchanged by this story; several of their
// links are buttons that call navigate() or need specific data, which a pure
// anchor scan would not see — their re-check is recorded in the QA evidence.
// Notification History's onward link is its parent link (ST-02).
// ---------------------------------------------------------------------------

const DEAD_END_PAGES = [
  '/#/notifications/history', '/#/TickerUniverse', '/#/TradeHistory', '/#/PerformanceAnalytics',
  '/#/Reports', '/#/StrategyBenchmark', '/#/Replay', '/#/TradeReflection', '/#/RedFlagJournal',
  '/#/Settings', '/#/SystemStatus',
];

// Hash-route path of a link, or of the page itself (query string and case ignored).
function routeOf(hash) {
  return (hash.replace(/^\/?#/, '').split('?')[0] || '/').toLowerCase();
}

test('SC-ONW-12: dead-end scan re-run — the 11 former dead-end pages all link onward', async ({ page }) => {
  test.setTimeout(180000);
  const many = Array.from({ length: 12 }, (_, i) => ({ ...TRADES[0], id: `t-${i}`, exit_date: `2026-09-${String(10 + i).padStart(2, '0')}` }));
  await page.route(/localhost:8000\/trades(\?|$)/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { trades: many } }) })
  );
  await page.route(/localhost:8000\/portfolio\/red-flag-journal/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RED_FLAG_EVENTS) })
  );

  const deadEnds = [];
  for (const hash of DEAD_END_PAGES) {
    await page.goto(hash);
    await expect(page.locator('main h1').first()).toBeVisible({ timeout: 15000 });
    await page.waitForTimeout(500);
    const self = routeOf(hash);
    const targets = await page.locator('main a[href^="#/"]').evaluateAll((els) => els.map((e) => e.getAttribute('href')));
    if (!targets.some((h) => routeOf(h) !== self)) deadEnds.push(hash);
  }
  expect(deadEnds, `dead-end pages: ${deadEnds.join(', ')}`).toEqual([]);
});
