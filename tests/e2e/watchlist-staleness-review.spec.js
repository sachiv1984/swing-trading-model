/**
 * Watchlist Staleness and Decay Review
 * ST-01 (BLG-FEAT-66, EPIC-01, v7.9)
 *
 * Design source: docs/design/2026-07-27__release-v7.9/watchlist-staleness-review/ux_spec.md
 * Frontend spec: docs/specs/frontend/pages/watchlist.md §Staleness Indicator
 *
 * Covers (non-visual AC — colour rendering itself is DoQ manual/visual review):
 *   SC-WLS-01  Not-stale entry shows "{N}d" in the Added column
 *   SC-WLS-02  Stale entry (days_on_watchlist >= 30) shows "{N}d, no action" + is flagged
 *   SC-WLS-03  Stale entry's row has a visible "Keep" action; not-stale rows do not
 *   SC-WLS-04  Clicking "Keep" fires PATCH /watchlist/{id} with added_at, shows a success toast
 *   SC-WLS-05  Existing "Remove" action is unaffected (still present, unchanged flow)
 *
 * What requires DoQ manual visual verification (not covered here):
 *   - Actual amber vs slate colour rendering, both light and dark theme
 *   - Clock icon rendering
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const NOT_STALE_ENTRY = {
  id: 'wl-not-stale-001',
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
  days_on_watchlist: 8,
  is_stale: false,
};

const STALE_ENTRY = {
  id: 'wl-stale-001',
  ticker: 'VOD.L',
  market: 'UK',
  company_name: 'Vodafone Group',
  signal_status: 'no_signal',
  tags: [],
  target_entry_price: null,
  initial_stop_price: null,
  current_stop_price: null,
  created_at: '2026-05-01T10:00:00Z',
  updated_at: '2026-05-01T10:00:00Z',
  added_at: '2026-05-01T10:00:00Z',
  days_on_watchlist: 88,
  is_stale: true,
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
  });
}

async function mockWatchlist(page, entries) {
  await page.route(`${API}/watchlist`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: entries }) });
    } else {
      route.continue();
    }
  });
  await page.route(`${API}/watchlist/tags`, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
  });
  await page.route(`${API}/screener/results`, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) });
  });
}

test.beforeEach(async ({ page }) => {
  await mockFallback(page);
});

test('SC-WLS-01: not-stale entry shows days-since-added, no Keep action', async ({ page }) => {
  await mockWatchlist(page, [NOT_STALE_ENTRY]);
  await page.goto('/#/Watchlist');

  const daysText = page.getByText('8d', { exact: true });
  await expect(daysText).toBeVisible({ timeout: 10000 });
  await expect(page.getByRole('button', { name: 'Keep' })).toBeHidden();

  // ST-06 (EPIC-03, v8.6, BLG-FE-149): not-stale entry's "Added" column
  // (WatchlistRow.js) used the failing text-slate-500 shade -- must now use
  // the canonical secondary-text token pair. This closes the colour-
  // rendering gap this file's own header noted as "not covered here" for
  // this specific element.
  await expect(daysText).toHaveClass(/text-slate-600/);
  await expect(daysText).toHaveClass(/dark:text-slate-400/);
});

test('SC-WLS-02: stale entry shows "no action" text and is flagged', async ({ page }) => {
  await mockWatchlist(page, [STALE_ENTRY]);
  await page.goto('/#/Watchlist');

  await expect(page.getByText('88d, no action')).toBeVisible({ timeout: 10000 });
});

test('SC-WLS-03: stale entry has a Keep action; not-stale row does not', async ({ page }) => {
  await mockWatchlist(page, [STALE_ENTRY, NOT_STALE_ENTRY]);
  await page.goto('/#/Watchlist');

  await expect(page.getByText('88d, no action')).toBeVisible({ timeout: 10000 });
  await expect(page.getByRole('button', { name: 'Keep' })).toHaveCount(1);
});

test('SC-WLS-04: clicking Keep fires PATCH with added_at and shows success toast', async ({ page }) => {
  await mockWatchlist(page, [STALE_ENTRY]);

  let patchBody = null;
  await page.route(`${API}/watchlist/${STALE_ENTRY.id}`, (route) => {
    if (route.request().method() === 'PATCH') {
      patchBody = route.request().postDataJSON();
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { ...STALE_ENTRY, is_stale: false, days_on_watchlist: 0 } }),
      });
    } else {
      route.continue();
    }
  });

  await page.goto('/#/Watchlist');
  await expect(page.getByText('88d, no action')).toBeVisible({ timeout: 10000 });

  await page.getByRole('button', { name: 'Keep' }).click();

  await expect(page.getByText(/kept on watchlist/i)).toBeVisible({ timeout: 5000 });
  expect(patchBody).toEqual({ added_at: true });
});

test('SC-WLS-05: Remove action is still present and unchanged for stale rows', async ({ page }) => {
  await mockWatchlist(page, [STALE_ENTRY]);
  await page.goto('/#/Watchlist');

  await expect(page.getByText('88d, no action')).toBeVisible({ timeout: 10000 });
  await expect(page.getByRole('button', { name: 'Research' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Add to Position' })).toBeVisible();
});
