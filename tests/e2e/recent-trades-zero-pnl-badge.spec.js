/**
 * Recent Trades widget — zero-P&L icon badge colour
 * ST-35 (BLG-FE-192, EPIC-06, cycle 2026-09-30__release-v9.9)
 *
 * The trade-row icon badge in src/components/dashboard/widgets/RecentTradesWidget.js
 * used a two-way `pnl >= 0` split, so a break-even trade got the same green badge as
 * a winner. It now uses the same three-way split as the adjacent P&L text:
 * emerald > 0, rose < 0, neutral slate for exactly 0.
 *
 *   SC-RTB-01  pnl === 0  -> neutral badge (not emerald, not rose), matching the P&L text's neutral treatment
 *   SC-RTB-02  pnl > 0    -> emerald badge (unchanged)
 *   SC-RTB-03  pnl < 0    -> rose badge (unchanged)
 *   SC-RTB-04  missing pnl (null) is treated as 0 -> neutral badge
 *   SC-RTB-05  glyph: zero/missing pnl -> neutral Minus; winner -> TrendingUp; loser -> TrendingDown
 *              (ST-10, BLG-FE-194, EPIC-02, cycle 2026-10-06__release-v9.10)
 *   SC-RTB-06  pnl 0.004 (displays as £0.00) -> neutral glyph and colour; pnl 0.01 -> up arrow
 *              (ST-15, BLG-FE-204, EPIC-02, cycle 2026-10-08__release-v9.11)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const CLOSED_TRADES = [
  { id: 'rt-zero', ticker: 'ZERO', market: 'US', status: 'closed', exit_date: '2026-09-30', pnl: 0, shares: 10 },
  { id: 'rt-win', ticker: 'WINR', market: 'US', status: 'closed', exit_date: '2026-09-29', pnl: 125.5, shares: 5 },
  { id: 'rt-loss', ticker: 'LOSS', market: 'US', status: 'closed', exit_date: '2026-09-28', pnl: -42.25, shares: 8 },
  { id: 'rt-null', ticker: 'NULL', market: 'US', status: 'closed', exit_date: '2026-09-27', pnl: null, shares: 3 },
];

// ST-15: the widget shows the 5 most recent trades, so the rounding cases use their own list.
const ROUNDING_TRADES = [
  { id: 'rt-tiny', ticker: 'TINY', market: 'US', status: 'closed', exit_date: '2026-09-26', pnl: 0.004, shares: 2 },
  { id: 'rt-cent', ticker: 'CENT', market: 'US', status: 'closed', exit_date: '2026-09-25', pnl: 0.01, shares: 2 },
];

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function gotoDashboardWithTrades(page, trades = CLOSED_TRADES) {
  await mockFallback(page);
  // GET /positions returns a raw array (src/api/base44Client.js positions.list, raw: true).
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(trades) })
  );
  await page.goto('/#/Dashboard');
  await expect(page.getByRole('heading', { name: 'Recent Trades' })).toBeVisible({ timeout: 10000 });
}

test.describe('Recent Trades icon badge colour', () => {
  test('SC-RTB-01: a zero-P&L trade renders a neutral badge, matching the neutral P&L text', async ({ page }) => {
    await gotoDashboardWithTrades(page);
    const badge = page.getByTestId('recent-trade-badge-rt-zero');
    await expect(badge).toBeVisible({ timeout: 8000 });
    await expect(badge).toHaveClass(/bg-slate-500\/20/);
    await expect(badge).toHaveClass(/text-slate-300/);
    await expect(badge).not.toHaveClass(/emerald/);
    await expect(badge).not.toHaveClass(/rose/);
  });

  test('SC-RTB-02: a winning trade keeps the emerald badge', async ({ page }) => {
    await gotoDashboardWithTrades(page);
    const badge = page.getByTestId('recent-trade-badge-rt-win');
    await expect(badge).toBeVisible({ timeout: 8000 });
    await expect(badge).toHaveClass(/bg-emerald-500\/20/);
    await expect(badge).toHaveClass(/text-emerald-400/);
    await expect(badge).not.toHaveClass(/rose|slate/);
  });

  test('SC-RTB-03: a losing trade keeps the rose badge', async ({ page }) => {
    await gotoDashboardWithTrades(page);
    const badge = page.getByTestId('recent-trade-badge-rt-loss');
    await expect(badge).toBeVisible({ timeout: 8000 });
    await expect(badge).toHaveClass(/bg-rose-500\/20/);
    await expect(badge).toHaveClass(/text-rose-400/);
    await expect(badge).not.toHaveClass(/emerald|slate/);
  });

  test('SC-RTB-04: a trade with no pnl value is treated as zero and renders neutral', async ({ page }) => {
    await gotoDashboardWithTrades(page);
    const badge = page.getByTestId('recent-trade-badge-rt-null');
    await expect(badge).toBeVisible({ timeout: 8000 });
    await expect(badge).toHaveClass(/bg-slate-500\/20/);
    await expect(badge).not.toHaveClass(/emerald|rose/);
  });

  test('SC-RTB-05: the glyph is neutral for break-even and missing P&L, arrows for winners and losers', async ({ page }) => {
    await gotoDashboardWithTrades(page);
    const glyph = (id, kind) => page.getByTestId(`recent-trade-badge-${id}`).getByTestId(`recent-trade-glyph-${kind}`);
    await expect(glyph('rt-zero', 'neutral')).toBeVisible({ timeout: 8000 });
    await expect(glyph('rt-zero', 'up')).toHaveCount(0);
    await expect(glyph('rt-null', 'neutral')).toBeVisible();
    await expect(glyph('rt-win', 'up')).toBeVisible();
    await expect(glyph('rt-win', 'neutral')).toHaveCount(0);
    await expect(glyph('rt-loss', 'down')).toBeVisible();
  });

  test('SC-RTB-06: a P&L that rounds to £0.00 is break-even; £0.01 is still a winner (ST-15)', async ({ page }) => {
    await gotoDashboardWithTrades(page, ROUNDING_TRADES);
    const tiny = page.getByTestId('recent-trade-badge-rt-tiny');
    await expect(tiny.getByTestId('recent-trade-glyph-neutral')).toBeVisible({ timeout: 8000 });
    await expect(tiny.getByTestId('recent-trade-glyph-up')).toHaveCount(0);
    await expect(tiny).toHaveClass(/bg-slate-500\/20/);
    await expect(tiny).not.toHaveClass(/emerald/);
    const cent = page.getByTestId('recent-trade-badge-rt-cent');
    await expect(cent.getByTestId('recent-trade-glyph-up')).toBeVisible();
    await expect(cent).toHaveClass(/bg-emerald-500\/20/);
  });
});
