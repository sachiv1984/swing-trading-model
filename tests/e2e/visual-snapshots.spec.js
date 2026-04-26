/**
 * Visual Snapshot Tests — ST-05, ST-06, ST-07, ST-11 (EPIC-02/03, v3.0)
 *
 * Element-level pixel snapshots for visual AC that cannot be verified by
 * DOM assertions alone. Each test captures a small, stable UI element and
 * compares it against a committed baseline PNG.
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
 *   VS-09  SkeletonRow — shimmer row structure (animation disabled)
 *   VS-10  Sidebar shortcut hints — Positions page (n + r kbd hints)
 *   VS-11  Sidebar shortcut hints — Screener page (w + r kbd hints)
 *   VS-12  Filter bar — market segment control (All / US / UK)
 *
 * ── Snapshot management ───────────────────────────────────────────────────
 * Baselines live in: tests/e2e/__snapshots__/
 * Generate / refresh: npx playwright test tests/e2e/visual-snapshots.spec.js --update-snapshots
 * Commit the generated PNGs. CI compares against committed baselines.
 *
 * ── Why these thresholds are safe ────────────────────────────────────────
 * maxDiffPixelRatio: 0.02 (configured globally in playwright.config.js).
 * Handles font-hinting differences between developer macOS and CI Linux
 * without masking genuine colour regressions.
 *
 * ── What is NOT snapshotted ───────────────────────────────────────────────
 * - Full-page screenshots (too noisy; minor layout shifts cause false failures)
 * - Animated states mid-transition (animation is disabled before capture)
 * - Popover/tooltip position (depends on viewport scroll position)
 *
 * ── Infrastructure ────────────────────────────────────────────────────────
 * page.route() network interception — no live backend required.
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
  await page.goto('/#/Screener');
  await page.waitForLoadState('networkidle');
}

// ---------------------------------------------------------------------------
// VS-01 — RegimeBadge risk_on (green)
// ---------------------------------------------------------------------------
test('VS-01: RegimeBadge risk_on is green', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString(); // "just now" — stable
  await gotoScreener(page, [makeRow({ ticker: 'AAPL', regime_status: 'risk_on' })], ts);

  const badge = page.locator('span').filter({ hasText: 'Risk On' }).first();
  await expect(badge).toBeVisible({ timeout: 8000 });
  await expect(badge).toHaveScreenshot('regime-badge-risk-on.png');
});

// ---------------------------------------------------------------------------
// VS-02 — RegimeBadge risk_off (red)
// ---------------------------------------------------------------------------
test('VS-02: RegimeBadge risk_off is red', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'BEAR', regime_status: 'risk_off' })], ts);

  const badge = page.locator('span').filter({ hasText: 'Risk Off' }).first();
  await expect(badge).toBeVisible({ timeout: 8000 });
  await expect(badge).toHaveScreenshot('regime-badge-risk-off.png');
});

// ---------------------------------------------------------------------------
// VS-03 — MarketBadge US (violet)
// ---------------------------------------------------------------------------
test('VS-03: MarketBadge US is violet', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'AAPL', market: 'US' })], ts);

  // MarketBadge renders span with "US" text
  const badge = page.locator('span').filter({ hasText: /^US$/ }).first();
  await expect(badge).toBeVisible({ timeout: 8000 });
  await expect(badge).toHaveScreenshot('market-badge-us.png');
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
  await expect(badge).toHaveScreenshot('market-badge-uk.png');
});

// ---------------------------------------------------------------------------
// VS-05 — News count badge (icon + number)
// ---------------------------------------------------------------------------
test('VS-05: News count badge has correct icon and count styling', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow({ ticker: 'AAPL', market: 'US', news_headline_count: 4 })], ts);

  await page.waitForSelector('text=AAPL', { timeout: 8000 });
  // News button: contains Newspaper icon + count
  const newsBtn = page.locator('button[title="Show news headlines"]').first();
  await expect(newsBtn).toBeVisible({ timeout: 3000 });
  await expect(newsBtn).toHaveScreenshot('news-count-badge.png');
});

// ---------------------------------------------------------------------------
// VS-06 — "Added" / In Watchlist chip (emerald checkmark)
// ---------------------------------------------------------------------------
test('VS-06: In Watchlist chip is emerald with checkmark', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  // Pre-populate watchlist so AAPL shows "Added" on load
  await page.route(`${API}/watchlist**`, (route) => {
    if (route.request().method() === 'GET') {
      return route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify({ items: [{ ticker: 'AAPL', market: 'US' }] }),
      });
    }
    return route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ id: 1 }) });
  });
  await gotoScreener(page, [makeRow({ ticker: 'AAPL' })], ts);

  await page.waitForSelector('text=AAPL', { timeout: 8000 });
  const chip = page.locator('span').filter({ hasText: /Added/ }).first();
  await expect(chip).toBeVisible({ timeout: 3000 });
  await expect(chip).toHaveScreenshot('watchlist-added-chip.png');
});

// ---------------------------------------------------------------------------
// VS-07 — Freshness badge — fresh state (slate grey)
// ---------------------------------------------------------------------------
test('VS-07: Freshness badge fresh state is grey with "Last screened"', async ({ page }) => {
  await stubCommon(page);
  // 10s ago → "just now" — stable text
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow()], ts);

  await page.waitForSelector('text=Last screened', { timeout: 8000 });
  const freshnessEl = page.locator('span').filter({ hasText: /Last screened/ }).first();
  await expect(freshnessEl).toBeVisible();
  await expect(freshnessEl).toHaveScreenshot('freshness-badge-fresh.png');
});

// ---------------------------------------------------------------------------
// VS-08 — Freshness badge — stale state (amber)
// ---------------------------------------------------------------------------
test('VS-08: Freshness badge stale state is amber with "Results may be stale"', async ({ page }) => {
  await stubCommon(page);
  // 2 days ago → "2 days ago" — stable text; always > STALE_HOURS threshold
  const ts = new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString();
  await gotoScreener(page, [makeRow()], ts);

  await page.waitForSelector('text=Results may be stale', { timeout: 8000 });
  const freshnessEl = page.locator('span').filter({ hasText: /Results may be stale/ }).first();
  await expect(freshnessEl).toBeVisible();
  await expect(freshnessEl).toHaveScreenshot('freshness-badge-stale.png');
});

// ---------------------------------------------------------------------------
// VS-09 — SkeletonRow structure (animation disabled by Playwright)
// ---------------------------------------------------------------------------
test('VS-09: SkeletonRow renders correct shimmer structure', async ({ page }) => {
  await stubCommon(page);
  // Delay the screener response so skeleton is visible when we snapshot
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

  await page.goto('/#/Screener');
  // Don't wait for networkidle — we want to capture the loading state
  await page.waitForTimeout(300);

  const firstSkeleton = page.locator('tr.border-b').first();
  const visible = await firstSkeleton.isVisible().catch(() => false);
  if (visible) {
    // animations: 'disabled' is set globally in playwright.config.js
    await expect(firstSkeleton).toHaveScreenshot('skeleton-row.png');
  } else {
    test.skip(true, 'Skeleton not visible — response too fast in this environment');
  }
});

// ---------------------------------------------------------------------------
// VS-10 — Sidebar shortcut hints — Positions page (n + r)
// ---------------------------------------------------------------------------
test('VS-10: Sidebar footer shows n and r shortcut hints on Positions', async ({ page }) => {
  await stubCommon(page);
  await page.goto('/#/Positions');
  await page.waitForLoadState('networkidle');

  // Desktop sidebar aside — the footer is the last child div with border-t
  const sidebarFooter = page.locator('aside').first().locator('div').filter({ hasText: /New trade/ });
  await expect(sidebarFooter).toBeVisible({ timeout: 5000 });
  await expect(sidebarFooter).toHaveScreenshot('sidebar-shortcuts-positions.png');
});

// ---------------------------------------------------------------------------
// VS-11 — Sidebar shortcut hints — Screener page (w + r)
// ---------------------------------------------------------------------------
test('VS-11: Sidebar footer shows w and r shortcut hints on Screener', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow()], ts);

  const sidebarFooter = page.locator('aside').first().locator('div').filter({ hasText: /Add to watchlist/ });
  await expect(sidebarFooter).toBeVisible({ timeout: 5000 });
  await expect(sidebarFooter).toHaveScreenshot('sidebar-shortcuts-screener.png');
});

// ---------------------------------------------------------------------------
// VS-12 — Filter bar: market segment control
// ---------------------------------------------------------------------------
test('VS-12: Market filter bar renders All / US / UK segments', async ({ page }) => {
  await stubCommon(page);
  const ts = new Date(Date.now() - 10_000).toISOString();
  await gotoScreener(page, [makeRow()], ts);

  await page.waitForSelector('text=AAPL', { timeout: 8000 });

  // The market filter renders three buttons: All, US, UK
  // Locate the container that holds all three
  const allBtn = page.getByRole('button', { name: /^All$/ });
  const usBtn  = page.getByRole('button', { name: /^US$/ });
  const ukBtn  = page.getByRole('button', { name: /^UK$/ });
  await expect(allBtn).toBeVisible();
  await expect(usBtn).toBeVisible();
  await expect(ukBtn).toBeVisible();

  // Snapshot the parent container of the three buttons
  const filterBar = allBtn.locator('..').first();
  await expect(filterBar).toHaveScreenshot('market-filter-bar.png');
});
