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

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function gotoDashboardWithTrades(page) {
  await mockFallback(page);
  // GET /positions returns a raw array (src/api/base44Client.js positions.list, raw: true).
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(CLOSED_TRADES) })
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
});
