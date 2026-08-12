/**
 * Watchlist — Baseline Acceptance Tests
 * ST-16 (BLG-QA-86, EPIC-04, v8.3)
 *
 * BLG-QA-86's problem statement: Watchlist.js had no baseline Playwright
 * coverage at all. This file establishes it — entry rendering, the news
 * toggle, and the Add Ticker modal open — per the story's own AC.
 *
 * Spec ref: docs/specs/frontend/pages/watchlist.md
 *
 *   SC-WL-01  Watchlist entry renders (ticker, market badge, added-days)
 *   SC-WL-02  News toggle expands a headlines row for a US entry; toggle again collapses it
 *   SC-WL-03  Non-US entry has no news toggle (shows a dash instead)
 *   SC-WL-04  "Add Ticker" opens the modal in add mode
 *   SC-WL-05  Invalid ticker format shows the canonical validation error text and colour
 *             token (ST-21, EPIC-04, v8.3, BLG-SPEC-108)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — all navigation via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const US_ENTRY = {
  id: 'wl-us-001',
  ticker: 'AAPL',
  market: 'US',
  company_name: 'Apple Inc.',
  signal_status: 'no_signal',
  tags: [],
  target_entry_price: null,
  initial_stop_price: null,
  current_stop_price: null,
  created_at: '2026-07-20T10:00:00Z',
  updated_at: '2026-07-20T10:00:00Z',
  added_at: '2026-07-20T10:00:00Z',
  days_on_watchlist: 5,
  is_stale: false,
};

const UK_ENTRY = {
  id: 'wl-uk-001',
  ticker: 'VOD.L',
  market: 'UK',
  company_name: 'Vodafone Group',
  signal_status: 'no_signal',
  tags: [],
  target_entry_price: null,
  initial_stop_price: null,
  current_stop_price: null,
  created_at: '2026-07-18T10:00:00Z',
  updated_at: '2026-07-18T10:00:00Z',
  added_at: '2026-07-18T10:00:00Z',
  days_on_watchlist: 7,
  is_stale: false,
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockWatchlist(page, entries) {
  await page.route(`${API}/watchlist`, (route) => {
    if (route.request().method() === 'GET') {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: entries }) });
    }
    return route.continue();
  });
  await page.route(`${API}/watchlist/tags`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/screener/results`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );
}

test.beforeEach(async ({ page }) => {
  await mockFallback(page);
});

test('SC-WL-01: watchlist entry renders ticker, market, and added-days', async ({ page }) => {
  await mockWatchlist(page, [US_ENTRY]);
  await page.goto('/#/Watchlist');

  await expect(page.getByText('AAPL', { exact: true })).toBeVisible({ timeout: 10000 });
  await expect(page.getByText('Apple Inc.')).toBeVisible();
  await expect(page.getByText('5d', { exact: true })).toBeVisible();
});

test('SC-WL-02: news toggle expands headlines for a US entry, then collapses on second click', async ({ page }) => {
  await mockWatchlist(page, [US_ENTRY]);
  await page.route(`${API}/news/AAPL*`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: { headlines: [{ headline: 'Apple announces new product', source: 'Reuters', published_at: '2026-08-01T09:00:00Z', url: 'https://example.com/a' }] },
      }),
    })
  );
  await page.goto('/#/Watchlist');
  await expect(page.getByText('AAPL', { exact: true })).toBeVisible({ timeout: 10000 });

  const newsToggle = page.locator('button[title="Show news headlines"]');
  await expect(newsToggle).toBeVisible();
  await newsToggle.click();

  await expect(page.getByText('Apple announces new product')).toBeVisible({ timeout: 5000 });

  await newsToggle.click();
  await expect(page.getByText('Apple announces new product')).not.toBeVisible({ timeout: 3000 });
});

test('SC-WL-03: non-US entry shows no news toggle', async ({ page }) => {
  await mockWatchlist(page, [UK_ENTRY]);
  await page.goto('/#/Watchlist');

  await expect(page.getByText('VOD.L', { exact: true })).toBeVisible({ timeout: 10000 });
  await expect(page.locator('button[title="Show news headlines"]')).toHaveCount(0);
});

test('SC-WL-04: "Add Ticker" opens the modal in add mode', async ({ page }) => {
  await mockWatchlist(page, []);
  await page.goto('/#/Watchlist');
  await expect(page.getByText('Your watchlist is empty')).toBeVisible({ timeout: 10000 });

  // Two "Add Ticker" buttons render simultaneously on the empty state (the
  // persistent PageHeader action + DataState's emptyAction CTA) — both are a
  // deliberate, valid UX pattern (always-available header action + a
  // contextual empty-state CTA), not a defect. .first() picks the PageHeader
  // one (earlier in DOM order) to avoid a Playwright strict-mode collision.
  await page.getByRole('button', { name: 'Add Ticker' }).first().click();

  await expect(page.getByRole('heading', { name: 'Add Ticker to Watchlist' })).toBeVisible({ timeout: 5000 });
  await expect(page.getByPlaceholder('e.g. AAPL')).toBeVisible();
});

test('SC-WL-05: invalid ticker format shows the canonical validation error text and colour token (ST-21, EPIC-04, v8.3, BLG-SPEC-108)', async ({ page }) => {
  await mockWatchlist(page, []);
  await page.goto('/#/Watchlist');
  await expect(page.getByText('Your watchlist is empty')).toBeVisible({ timeout: 10000 });

  await page.getByRole('button', { name: 'Add Ticker' }).first().click();
  await expect(page.getByRole('heading', { name: 'Add Ticker to Watchlist' })).toBeVisible({ timeout: 5000 });

  await page.getByPlaceholder('e.g. AAPL').fill('!!!invalid!!!');

  const error = page.getByText('Invalid format. Use 1–10 alphanumeric characters.');
  await expect(error).toBeVisible({ timeout: 5000 });
  await expect(error).toHaveClass(/text-rose-700/);
  await expect(error).toHaveClass(/dark:text-rose-400/);
});

test('SC-WL-06: WatchlistModal DialogDescription resolves the winning cascade colour, not an empty rule (ST-05, EPIC-03, v8.6, BLG-FE-148)', async ({ page }) => {
  // Investigation finding for ST-05 AC-02: `DialogDescription`'s own default
  // styling (src/components/ui/dialog.js) is `text-sm text-muted-foreground`.
  // Every live call site (WatchlistModal, ExportModal, PositionEntryModal,
  // WidgetLibrary, ExitModal) additionally passes an explicit
  // `className="text-slate-600 dark:text-slate-400"` override. `cn()` in
  // this codebase is plain `clsx` (src/lib/utils.js) with no Tailwind-merge
  // dedup, so BOTH class lists are applied to the element. Resolved via the
  // compiled CSS (`npx tailwindcss` build, checked against cascade rules,
  // not guessed): in dark theme (this app's default) `dark:text-slate-400`
  // compiles to `.dark\:text-slate-400:is(.dark *)` -- a compound selector
  // with higher specificity (0,2,0) than the bare single-class
  // `.text-muted-foreground` (0,1,0) -- so it always wins regardless of
  // stylesheet order. Tailwind slate-400 is rgb(148, 163, 184).
  await mockWatchlist(page, []);
  await page.goto('/#/Watchlist');
  await expect(page.getByText('Your watchlist is empty')).toBeVisible({ timeout: 10000 });

  await page.getByRole('button', { name: 'Add Ticker' }).first().click();
  await expect(page.getByRole('heading', { name: 'Add Ticker to Watchlist' })).toBeVisible({ timeout: 5000 });

  const description = page.getByText('Track a new ticker for entry opportunities.');
  await expect(description).toBeVisible();
  const color = await description.evaluate((el) => getComputedStyle(el).color);
  expect(color).toBe('rgb(148, 163, 184)');
});
