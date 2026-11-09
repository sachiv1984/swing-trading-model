/**
 * Sidebar Navigation Areas — Acceptance Tests
 * Originally ST-13 (BLG-UX-01, v2.3) for the v1.x collapsible groups.
 * Rewritten for navigation.md v2.0 by ST-01 (EPIC-01, v9.16, BLG-FE-250):
 * five job-based areas (Today, Portfolio, Find trades, Review, Settings),
 * Today and Portfolio expanded by default, Trade Plans and Research surfaced.
 *
 * Visual AC (chevron colour, typography, animation smoothness) remains DoQ
 * manual review — see docs/testing/sidebar_nav_scenarios.md SC-SNV-VIS-02.
 *
 * Scenarios:
 *   SC-SNV-01  Default state: Today, Portfolio and the active area expanded; others collapsed
 *   SC-SNV-02  Area headers appear in spec order and expose aria-expanded
 *   SC-SNV-03  User can expand and collapse a non-active area
 *   SC-SNV-04  Active area cannot be collapsed by clicking its header
 *   SC-SNV-05  Active area auto-expands on page navigation
 *   SC-SNV-06  sessionStorage persists a user-expanded area across in-session navigation
 *   SC-SNV-07  Clearing stored state and reloading resets to the defaults
 *   SC-SNV-08  Every area lists exactly its spec entries, in order, and routes resolve
 *   SC-SNV-09  Trade Plans is reachable from the sidebar in one click (AC 2)
 *   SC-SNV-10  Research entry opens the /Research landing; a ticker goes to /research/:ticker
 *   SC-SNV-11  A page without a sidebar entry highlights its parent's entry
 *   SC-SNV-12  An explicit collapse of Today holds for the session
 *   SC-SNV-13  Mobile drawer shows the same areas, order and default expansion
 *   SC-SNV-14  A stored v1.x group-collapse value does not hide v2 areas
 *
 * Spec refs:
 *   docs/specs/frontend/pages/navigation.md v2.0 §Areas, §Page Placement,
 *     §Default Expansion and Collapse, §Area Header, §Active Item, §Responsive Behaviour
 *
 * Infrastructure: page.route() network interception. No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 *
 * DOM NOTES:
 *   - Area header: <button data-testid="nav-area-{key}" aria-expanded>
 *     keys: today, portfolio, find, review, settings
 *   - Desktop nav: [data-testid="desktop-sidebar-nav"]; mobile drawer nav:
 *     [data-testid="mobile-sidebar-nav"] (opened by [data-testid="mobile-menu-trigger"])
 *   - sessionStorage key: "nav-group-collapse"  (JSON: { today, portfolio, find, review, settings })
 *   - Area items are only in the DOM when the area is expanded (AnimatePresence unmounts them)
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

// navigation.md v2.0 §Page Placement — sidebar entries per area, in order.
const AREAS = [
  { key: 'today',     label: 'Today',       items: ['Dashboard', 'Notifications'] },
  { key: 'portfolio', label: 'Portfolio',   items: ['Positions', 'Trade Entry', 'Risk Dashboard'] },
  { key: 'find',      label: 'Find trades', items: ['Signals', 'Screener', 'Watchlist', 'Research', 'Trade Plans', 'Ticker Universe'] },
  { key: 'review',    label: 'Review',      items: ['Trade History', 'Analytics', 'Reports', 'Strategy Benchmark', 'Replay', 'Trade Reflections', 'Red Flag Journal', 'Weekly Digest'] },
  { key: 'settings',  label: 'Settings',    items: ['Settings', 'System Status'] },
];

// Expected href (hash route) per sidebar label.
const HREFS = {
  'Dashboard': '#/',
  'Notifications': '#/notifications',
  'Positions': '#/Positions',
  'Trade Entry': '#/TradeEntry',
  'Risk Dashboard': '#/RiskDashboard',
  'Signals': '#/Signals',
  'Screener': '#/Screener',
  'Watchlist': '#/Watchlist',
  'Research': '#/Research',
  'Trade Plans': '#/TradePlans',
  'Ticker Universe': '#/TickerUniverse',
  'Trade History': '#/TradeHistory',
  'Analytics': '#/PerformanceAnalytics',
  'Reports': '#/Reports',
  'Strategy Benchmark': '#/StrategyBenchmark',
  'Replay': '#/Replay',
  'Trade Reflections': '#/TradeReflection',
  'Red Flag Journal': '#/RedFlagJournal',
  'Weekly Digest': '#/WeeklyDigest',
  'Settings': '#/Settings',
  'System Status': '#/SystemStatus',
};

// ---------------------------------------------------------------------------
// Shared mocks — stub every backend call with an empty-but-valid body so the
// pages render without network errors unrelated to the nav behaviour.
// ---------------------------------------------------------------------------

async function stubAll(page) {
  await page.route(/localhost:8000\//, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(/localhost:8000\/positions(\?|$)/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(/localhost:8000\/portfolio(\?|$)/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route(/localhost:8000\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { evaluations: [], total: 0 } }) })
  );
  await page.route(/localhost:8000\/notifications\?/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }) })
  );
  await page.route(/localhost:8000\/notifications\/preferences/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { preferences: [] } }) })
  );
}

async function goto(page, hash) {
  await page.goto(hash);
  await page.waitForLoadState('domcontentloaded');
}

/** Clear stored collapse state before the first page load only. */
async function clearCollapseOnce(page) {
  await page.addInitScript(() => {
    if (!sessionStorage.getItem('__snv_cleared')) {
      sessionStorage.removeItem('nav-group-collapse');
      sessionStorage.setItem('__snv_cleared', '1');
    }
  });
}

const desktopNav = (page) => page.getByTestId('desktop-sidebar-nav');
const areaBtn = (scope, key) => scope.getByTestId(`nav-area-${key}`);
const navLink = (scope, name) => scope.getByRole('link', { name, exact: true });

async function expectExpanded(scope, key, expanded) {
  await expect(areaBtn(scope, key)).toHaveAttribute('aria-expanded', expanded ? 'true' : 'false', { timeout: 5000 });
}

// ---------------------------------------------------------------------------

test('SC-SNV-01: on fresh load, Today, Portfolio and the active area are expanded; others collapsed', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Watchlist'); // Watchlist is in Find trades

  const nav = desktopNav(page);
  await expectExpanded(nav, 'today', true);
  await expectExpanded(nav, 'portfolio', true);
  await expectExpanded(nav, 'find', true);
  await expectExpanded(nav, 'review', false);
  await expectExpanded(nav, 'settings', false);

  await expect(navLink(nav, 'Dashboard')).toBeVisible();
  await expect(navLink(nav, 'Positions')).toBeVisible();
  await expect(navLink(nav, 'Watchlist')).toBeVisible();
  await expect(navLink(nav, 'Trade History')).toHaveCount(0);
  await expect(navLink(nav, 'System Status')).toHaveCount(0);
});

test('SC-SNV-02: area headers appear in spec order', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Positions');

  const headers = desktopNav(page).locator('[data-testid^="nav-area-"]');
  await expect(headers).toHaveCount(5, { timeout: 5000 });
  const ids = await headers.evaluateAll((els) => els.map((e) => e.getAttribute('data-testid')));
  expect(ids).toEqual(AREAS.map((a) => `nav-area-${a.key}`));
  const texts = await headers.evaluateAll((els) => els.map((e) => e.textContent.trim()));
  expect(texts).toEqual(AREAS.map((a) => a.label));
});

test('SC-SNV-03: clicking a non-active area header expands and then collapses it', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Positions');

  const nav = desktopNav(page);
  await expectExpanded(nav, 'review', false);
  await areaBtn(nav, 'review').click();
  await expectExpanded(nav, 'review', true);
  await expect(navLink(nav, 'Analytics')).toBeVisible();
  await expect(navLink(nav, 'Weekly Digest')).toBeVisible();

  await areaBtn(nav, 'review').click();
  await expectExpanded(nav, 'review', false);
  await expect(navLink(nav, 'Analytics')).toHaveCount(0, { timeout: 3000 });
});

test('SC-SNV-04: clicking the active area header does not collapse it', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/TradeHistory'); // Review is active

  const nav = desktopNav(page);
  await expectExpanded(nav, 'review', true);
  await expect(areaBtn(nav, 'review')).toBeDisabled();
  await areaBtn(nav, 'review').click({ force: true });
  await expectExpanded(nav, 'review', true);
  await expect(navLink(nav, 'Trade History')).toBeVisible();
});

test('SC-SNV-05: navigating to a page auto-expands its area', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Positions');

  const nav = desktopNav(page);
  await expectExpanded(nav, 'settings', false);
  await goto(page, '/#/SystemStatus');
  await expectExpanded(nav, 'settings', true);
  await expect(navLink(nav, 'System Status')).toBeVisible();
});

test('SC-SNV-06: a user-expanded area stays expanded after in-session navigation', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Positions');

  const nav = desktopNav(page);
  await areaBtn(nav, 'review').click();
  await expectExpanded(nav, 'review', true);

  await goto(page, '/#/TradeEntry');
  await expectExpanded(nav, 'review', true);
});

test('SC-SNV-07: clearing stored state and reloading resets areas to the defaults', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Positions');

  const nav = desktopNav(page);
  await areaBtn(nav, 'review').click();
  await areaBtn(nav, 'settings').click();
  await expectExpanded(nav, 'review', true);
  await expectExpanded(nav, 'settings', true);

  await page.evaluate(() => sessionStorage.removeItem('nav-group-collapse'));
  await page.reload();
  await page.waitForLoadState('domcontentloaded');

  await expectExpanded(nav, 'today', true);
  await expectExpanded(nav, 'portfolio', true);
  await expectExpanded(nav, 'find', false);
  await expectExpanded(nav, 'review', false);
  await expectExpanded(nav, 'settings', false);
});

test('SC-SNV-08: every area lists exactly its spec entries in order, with the right routes', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Positions');

  const nav = desktopNav(page);
  for (const area of AREAS) {
    const btn = areaBtn(nav, area.key);
    if ((await btn.getAttribute('aria-expanded')) === 'false') await btn.click();
    await expectExpanded(nav, area.key, true);
  }
  const links = nav.getByRole('link');
  await expect(links).toHaveCount(21);
  const got = await links.evaluateAll((els) =>
    els.map((e) => [e.textContent.trim(), e.getAttribute('href')])
  );
  const expected = AREAS.flatMap((a) => a.items).map((name) => [name, HREFS[name]]);
  expect(got).toEqual(expected);
});

test('SC-SNV-09: Trade Plans is reachable from the sidebar in one click (AC 2)', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  // Trade Plans is its own sidebar entry (it was palette-only before v2.0):
  // from a Find trades page the entry is visible and one click opens the page.
  await goto(page, '/#/Signals');
  const nav = desktopNav(page);
  await expect(navLink(nav, 'Trade Plans')).toBeVisible();
  await navLink(nav, 'Trade Plans').click();
  await expect(page).toHaveURL(/#\/TradePlans$/);
  await expect(page.getByRole('heading', { level: 1, name: 'Trade Plans', exact: true })).toBeVisible({ timeout: 10000 });
  await expect(navLink(nav, 'Trade Plans')).toHaveAttribute('aria-current', 'page');
});

test('SC-SNV-10: the Research entry opens the landing, and a ticker goes to /research/:ticker', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Signals');

  const nav = desktopNav(page);
  await navLink(nav, 'Research').click();
  await expect(page).toHaveURL(/#\/Research$/);
  await expect(page.getByRole('heading', { level: 1, name: 'Research', exact: true })).toBeVisible({ timeout: 10000 });
  await expect(navLink(nav, 'Research')).toHaveAttribute('aria-current', 'page');
  await expect(page).toHaveTitle('Research · Position Manager');

  const input = page.getByTestId('research-landing-ticker');
  await expect(input).toBeVisible();
  await input.fill('aapl');
  await page.getByTestId('research-landing-submit').click();
  await expect(page).toHaveURL(/#\/research\/AAPL$/);
});

test('SC-SNV-11: a page without a sidebar entry highlights its parent entry', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  const nav = desktopNav(page);

  for (const [hash, parent, areaKey] of [
    ['/#/TradePlan', 'Trade Plans', 'find'],
    ['/#/research/AAPL', 'Research', 'find'],
    ['/#/notifications/history', 'Notifications', 'today'],
    ['/#/notifications/preferences', 'Notifications', 'today'],
  ]) {
    await goto(page, hash);
    await expectExpanded(nav, areaKey, true);
    await expect(areaBtn(nav, areaKey)).toBeDisabled();
    await expect(navLink(nav, parent)).toHaveAttribute('aria-current', 'page', { timeout: 5000 });
  }
});

test('SC-SNV-12: an explicit collapse of Today holds for the session', async ({ page }) => {
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Positions');

  const nav = desktopNav(page);
  await expectExpanded(nav, 'today', true);
  await areaBtn(nav, 'today').click();
  await expectExpanded(nav, 'today', false);
  await goto(page, '/#/TradeEntry');
  await expectExpanded(nav, 'today', false);
});

test('SC-SNV-13: the mobile drawer has the same areas, order and default expansion', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await clearCollapseOnce(page);
  await stubAll(page);
  await goto(page, '/#/Watchlist');

  await page.getByTestId('mobile-menu-trigger').click();
  const drawer = page.getByTestId('mobile-sidebar-nav');
  await expect(drawer).toBeVisible({ timeout: 5000 });

  const headers = drawer.locator('[data-testid^="nav-area-"]');
  const ids = await headers.evaluateAll((els) => els.map((e) => e.getAttribute('data-testid')));
  expect(ids).toEqual(AREAS.map((a) => `nav-area-${a.key}`));
  await expectExpanded(drawer, 'today', true);
  await expectExpanded(drawer, 'portfolio', true);
  await expectExpanded(drawer, 'find', true);
  await expectExpanded(drawer, 'review', false);
  await expectExpanded(drawer, 'settings', false);

  await navLink(drawer, 'Trade Plans').click();
  await expect(page).toHaveURL(/#\/TradePlans$/);
  await expect(drawer).toHaveCount(0, { timeout: 5000 });
});

test('SC-SNV-14: a stored v1.x group-collapse value does not hide the v2 areas', async ({ page }) => {
  await page.addInitScript(() => {
    if (!sessionStorage.getItem('__snv_v1')) {
      sessionStorage.setItem('nav-group-collapse', JSON.stringify({ trading: true, analytics: true, tools: true, system: true }));
      sessionStorage.setItem('__snv_v1', '1');
    }
  });
  await stubAll(page);
  await goto(page, '/#/Positions');

  const nav = desktopNav(page);
  await expectExpanded(nav, 'today', true);
  await expectExpanded(nav, 'portfolio', true);
  await expectExpanded(nav, 'find', false);
});
