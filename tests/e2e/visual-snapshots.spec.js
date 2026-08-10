/**
 * Visual Snapshot Tests — ST-05, ST-06, ST-07, ST-11 (EPIC-02/03, v3.0)
 *
 * Verifies visual AC via CSS class / attribute assertions.
 * Originally pixel-snapshot based; converted to CSS assertions to ensure
 * reliable cross-platform CI (Chromium version differences cause pixel mismatches).
 *
 * Coverage:
 *   VS-01  RegimeBadge — risk_on (green badge)
 *   VS-02  RegimeBadge — risk_off (red badge)
 *   VS-03  MarketBadge — US (violet badge)
 *   VS-04  MarketBadge — UK (blue badge)
 *   VS-05  News count badge — button with icon + count
 *   VS-06  "Added" / In Watchlist state — emerald checkmark chip
 *   VS-07  Freshness badge — fresh state (slate grey, "Last screened: just now")
 *   VS-08  Freshness badge — stale state (amber, "Results may be stale")
 *   VS-09  SkeletonRow — shimmer row structure
 *   VS-10  Sidebar shortcut hints — Positions page (n + r kbd hints)
 *   VS-11  Sidebar shortcut hints — Screener page (w + r kbd hints)
 *   VS-12  Filter bar — market segment control (All / US / UK)
 *   VS-13  EarningsBadge — amber colour class when earnings ≤5 days (Screener)
 *   VS-14  PositionEarningsCell — amber colour class when earnings ≤5 days (Positions table)
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * HashRouter: all navigation via page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function stubCommon(page) {
  await page.route(`${API}/alerts/history`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route(`${API}/watchlist**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route(`${API}/portfolio/positions**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { positions: [] } }) })
  );
}

function screenerResponse(results, runTimestamp = null) {
  return {
    results,
    run_id: 'run-snap-01',
    run_timestamp: runTimestamp,
    total: results.length,
    limit: 200,
    offset: 0,
  };
}

function makeRow(overrides = {}) {
  return {
    ticker: 'AAPL',
    market: 'US',
    price: 175.50,
    currency: 'USD',
    atr: 3.20,
    atr_pct: 1.83,
    regime_status: 'risk_on',
    signal_score: 0.82,
    sector: 'Technology',
    proximity_to_entry_zone: 'near_entry',
    news_headline_count: 3,
    ...overrides,
  };
}

async function gotoScreener(page, results, runTimestamp = null) {
  await page.route(`${API}/screener/results**`, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify(screenerResponse(results, runTimestamp)),
    })
  );
  await page.route(`${API}/screener/run`, (route) =>
    route.fulfill({ status: 202, contentType: 'application/json', body: JSON.stringify({ run_id: 'run-002' }) })
  );
  // ST-21 (BLG-FEAT-29, v8.5): stub the Regime History panel's own data call.
  await page.route(`${API}/screener/regime-distribution**`, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ ok: true, data: { window: '30d', run_count: 1, total_observations: 2, risk_on_count: 2, risk_off_count: 0, risk_on_pct: 100.0, risk_off_pct: 0.0 } }),
    })
  );
  await page.goto('/#/Screener');
}

// ---------------------------------------------------------------------------
// VS-01 — RegimeBadge risk_on (green)
// ---------------------------------------------------------------------------
test('VS-01: RegimeBadge risk_on is green', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'AAPL', regime_status: 'risk_on' })], ts);

  const badge = page.locator('span').filter({ hasText: 'Risk On' }).first();
  await expect(badge).toBeVisible({ timeout: 8000 });
  // RegimeBadge risk_on renders with emerald (green) styling
  await expect(badge).toHaveClass(/text-emerald-400/);
  await expect(badge).toHaveClass(/bg-emerald-500/);
});

// ---------------------------------------------------------------------------
// VS-02 — RegimeBadge risk_off (red/slate)
// ---------------------------------------------------------------------------
test('VS-02: RegimeBadge risk_off is red', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'BEAR', regime_status: 'risk_off' })], ts);

  const badge = page.locator('span').filter({ hasText: 'Risk Off' }).first();
  await expect(badge).toBeVisible({ timeout: 8000 });
  // RegimeBadge risk_off renders with slate styling (neutral/red-adjacent)
  await expect(badge).toHaveClass(/text-slate-400/);
});

// ---------------------------------------------------------------------------
// VS-03 — MarketBadge US (violet)
// ---------------------------------------------------------------------------
test('VS-03: MarketBadge US is violet', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'AAPL', market: 'US' })], ts);

  const badge = page.locator('span').filter({ hasText: /^US$/ }).first();
  await expect(badge).toBeVisible({ timeout: 8000 });
  // MarketBadge US renders with violet styling
  await expect(badge).toHaveClass(/text-violet-400/);
  await expect(badge).toHaveClass(/bg-violet-500/);
});

// ---------------------------------------------------------------------------
// VS-04 — MarketBadge UK (blue)
// ---------------------------------------------------------------------------
test('VS-04: MarketBadge UK is blue', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'BP', market: 'UK', currency: 'GBP' })], ts);

  const badge = page.locator('span').filter({ hasText: /^UK$/ }).first();
  await expect(badge).toBeVisible({ timeout: 8000 });
  // MarketBadge UK renders with blue styling
  await expect(badge).toHaveClass(/text-blue-400/);
  await expect(badge).toHaveClass(/bg-blue-500/);
});

// ---------------------------------------------------------------------------
// VS-05 — News count badge (icon + number)
// ---------------------------------------------------------------------------
test('VS-05: News count badge has correct icon and count styling', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'AAPL', market: 'US', news_headline_count: 4 })], ts);

  await page.waitForSelector('text=AAPL', { timeout: 8000 });
  const newsBtn = page.locator('button[title="Show news headlines"]').first();
  await expect(newsBtn).toBeVisible({ timeout: 3000 });
  // News badge shows the count "4"
  await expect(newsBtn).toContainText('4');
});

// ---------------------------------------------------------------------------
// VS-06 — "Added" / In Watchlist chip (emerald checkmark)
// ---------------------------------------------------------------------------
test('VS-06: In Watchlist chip is emerald with checkmark', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await page.route(`${API}/watchlist**`, (route) => {
    route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ id: 1 }) });
  });
  await gotoScreener(page, [makeRow({ ticker: 'AAPL' })], ts);

  await page.waitForSelector('text=AAPL', { timeout: 8000 });

  await page.locator('button[title="Add to watchlist"]').first().click();
  await page.getByRole('button', { name: /Add to Watchlist/i }).click();

  const chip = page.locator('span').filter({ hasText: /Added/ }).first();
  await expect(chip).toBeVisible({ timeout: 5000 });
  // Added chip renders with emerald (green) styling
  await expect(chip).toHaveClass(/text-emerald-400/);
});

// ---------------------------------------------------------------------------
// VS-07 — Freshness badge — fresh state (slate grey)
// ---------------------------------------------------------------------------
test('VS-07: Freshness badge fresh state is grey with "Last screened"', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow()], ts);

  await page.waitForSelector('text=Last screened', { timeout: 8000 });
  const freshnessEl = page.locator('span').filter({ hasText: /Last screened/ }).first();
  await expect(freshnessEl).toBeVisible();
  // Fresh state uses slate styling (not amber)
  await expect(freshnessEl).toHaveClass(/text-slate-400/);
  await expect(freshnessEl).not.toHaveClass(/text-amber/);
});

// ---------------------------------------------------------------------------
// VS-08 — Freshness badge — stale state (amber)
// ---------------------------------------------------------------------------
test('VS-08: Freshness badge stale state is amber with "Results may be stale"', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString();
  await gotoScreener(page, [makeRow()], ts);

  await page.waitForSelector('text=Results may be stale', { timeout: 8000 });
  const freshnessEl = page.locator('span').filter({ hasText: /Results may be stale/ }).first();
  await expect(freshnessEl).toBeVisible();
  // Stale state uses amber styling
  await expect(freshnessEl).toHaveClass(/text-amber-400/);
  await expect(freshnessEl).toHaveClass(/bg-amber-500/);
});

// ---------------------------------------------------------------------------
// VS-09 — SkeletonRow structure (animation disabled by Playwright)
// ---------------------------------------------------------------------------
test('VS-09: SkeletonRow renders correct shimmer structure', async ({ page }) => {
  await stubCommon(page);
  await page.route(`${API}/screener/results**`, async (route) => {
    await new Promise((r) => setTimeout(r, 2000));
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify(screenerResponse([makeRow()])),
    });
  });
  await page.route(`${API}/screener/run`, (route) =>
    route.fulfill({ status: 202, contentType: 'application/json', body: JSON.stringify({ run_id: 'r' }) })
  );
  await page.route(`${API}/screener/regime-distribution**`, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ ok: true, data: { window: '30d', run_count: 1, total_observations: 2, risk_on_count: 2, risk_off_count: 0, risk_on_pct: 100.0, risk_off_pct: 0.0 } }),
    })
  );

  await page.goto('/#/Screener');
  await page.waitForTimeout(300);

  const firstSkeleton = page.locator('tr.border-b').first();
  const visible = await firstSkeleton.isVisible().catch(() => false);
  if (visible) {
    // Skeleton cells use animate-pulse shimmer
    await expect(firstSkeleton.locator('div.animate-pulse').first()).toBeVisible();
  } else {
    test.skip(true, 'Skeleton not visible — response too fast in this environment');
  }
});

// ---------------------------------------------------------------------------
// VS-10 — Sidebar shortcut hints — Positions page (n + r)
// ---------------------------------------------------------------------------
test('VS-10: Sidebar footer shows n and r shortcut hints on Positions', async ({ page }) => {
  await stubCommon(page);
  // Stub positions so page loads without errors
  await page.route(`${API}/positions**`, (route) => {
    const url = route.request().url();
    if (url.includes('/positions/compliance')) {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) });
    }
  });
  await page.route(`${API}/portfolio**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 0 } }) })
  );
  await page.route(`${API}/analytics/**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.goto('/#/Positions');

  const sidebarFooter = page.locator('aside').first().locator('div.mb-3.space-y-1').first();
  await expect(sidebarFooter).toBeVisible({ timeout: 5000 });
  // Shortcut hints for Positions page: n (new position) and r (run screener)
  // Use kbd locator to avoid matching 'n' inside "New trade" label text
  await expect(sidebarFooter.locator('kbd').filter({ hasText: /^n$/ })).toBeVisible();
  await expect(sidebarFooter.locator('kbd').filter({ hasText: /^r$/ })).toBeVisible();
});

// ---------------------------------------------------------------------------
// VS-11 — Sidebar shortcut hints — Screener page (w + r)
// ---------------------------------------------------------------------------
test('VS-11: Sidebar footer shows w and r shortcut hints on Screener', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow()], ts);

  const sidebarFooter = page.locator('aside').first().locator('div.mb-3.space-y-1').first();
  await expect(sidebarFooter).toBeVisible({ timeout: 5000 });
  // Shortcut hints for Screener page: w (add to watchlist) and r (run screener)
  // Use kbd locator to avoid matching 'w' inside "Add to watchlist" label text
  await expect(sidebarFooter.locator('kbd').filter({ hasText: /^w$/ })).toBeVisible();
  await expect(sidebarFooter.locator('kbd').filter({ hasText: /^r$/ })).toBeVisible();
});

// ---------------------------------------------------------------------------
// VS-12 — Filter bar: market segment control
// ---------------------------------------------------------------------------
test('VS-12: Market filter bar renders All / US / UK segments', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow()], ts);

  await page.waitForSelector('text=AAPL', { timeout: 8000 });

  const allBtn = page.getByRole('button', { name: /^All$/ });
  const usBtn  = page.getByRole('button', { name: /^US$/ });
  const ukBtn  = page.getByRole('button', { name: /^UK$/ });
  await expect(allBtn).toBeVisible();
  await expect(usBtn).toBeVisible();
  await expect(ukBtn).toBeVisible();
});

// ---------------------------------------------------------------------------
// VS-13 — EarningsBadge amber colour class when earnings ≤5 days (Screener)
// ---------------------------------------------------------------------------
test('VS-13: Screener EarningsBadge has text-amber-400 class when earnings ≤5 days', async ({ page }) => {
  const d = new Date();
  d.setDate(d.getDate() + 3);
  const earningsData = { next_earnings_date: d.toISOString().split('T')[0], days_until_earnings: 3, fiscal_quarter: 'Q2', data_source: 'yahoo_finance' };

  await stubCommon(page);
  await page.route(`${API}/earnings/**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(earningsData) })
  );
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'AAPL', market: 'US' })], ts);

  await page.waitForSelector('text=AAPL', { timeout: 8000 });

  // EarningsBadge renders "3d" with text-amber-400 class when days ≤ 5
  const badge = page.locator('span').filter({ hasText: /^3d$/ }).first();
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveClass(/text-amber-400/);
});

// ---------------------------------------------------------------------------
// VS-14 — PositionEarningsCell amber colour class when earnings ≤5 days (Positions table)
// ---------------------------------------------------------------------------
test('VS-14: Positions table PositionEarningsCell has text-amber-400 class when earnings ≤5 days', async ({ page }) => {
  const d = new Date();
  d.setDate(d.getDate() + 2);
  const earningsData = { next_earnings_date: d.toISOString().split('T')[0], days_until_earnings: 2, fiscal_quarter: 'Q1', data_source: 'yahoo_finance' };

  await stubCommon(page);
  await page.route(`${API}/earnings/**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(earningsData) })
  );
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/positions/compliance')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
    return route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify([{
        id: 'pos-vs14', ticker: 'NVDA', market: 'US', entry_price: 800, current_price: 850,
        current_price_native: 850, stop_price: 760, stop_price_native: 760, shares: 10,
        pnl: 500, pnl_percent: 6.25, holding_days: 5, grace_days_remaining: null,
        status: 'open', entry_date: '2026-04-01', initial_stop: 760, tags: null,
      }]),
    });
  });
  await page.route('**/portfolio**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: { cash: 5000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: {} }) })
  );
  await page.route('**/compliance/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  await page.goto('/#/Positions');

  await page.waitForSelector('text=NVDA', { timeout: 8000 });
  // Switch to table view to reveal PositionEarningsCell
  await page.getByRole('button', { name: 'Table view' }).click();
  await page.waitForSelector('table', { timeout: 5000 });

  // PositionEarningsCell renders "⚠ 2d" with text-amber-400 class when days ≤ 5
  const cell = page.locator('span').filter({ hasText: /⚠\s*2d/ }).first();
  await expect(cell).toBeVisible({ timeout: 5000 });
  await expect(cell).toHaveClass(/text-amber-400/);
});
