/**
 * Net-of-costs R-multiple — Automated Acceptance Tests
 * ST-03 (EPIC-02, v6.0) — BLG-FEAT-20
 *
 * Covers observable ACs on TradeHistory page:
 *
 *   SC-NR-01  Net R column header visible on Trade History page
 *   SC-NR-02  Net R value shown when commission_gbp and spread_cost_gbp present (AC-02)
 *   SC-NR-03  Net R shows "—" for trades with no cost data (AC-04 backward-compat)
 *   SC-NR-04  Net R positive value rendered in green; negative in red (AC-02)
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/TradeHistory').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Seed data
// ---------------------------------------------------------------------------

const TRADE_WITH_COSTS = {
  id: 'nr-t1',
  ticker: 'AAPL',
  market: 'US',
  entry_date: '2026-05-01',
  exit_date: '2026-05-20',
  entry_price: 175.00,
  exit_price: 192.50,
  shares: 50,
  pnl: 850.00,
  pnl_pct: 10.0,
  pnl_percent: 10.0,
  fee_drag_pct: 0.38,
  slippage_pct: -0.05,
  commission_gbp: 12.50,
  spread_cost_gbp: 3.20,
  net_r_multiple: 1.847,
  exit_reason: 'Target Reached',
  tags: [],
};

const TRADE_WITHOUT_COSTS = {
  id: 'nr-t2',
  ticker: 'LGEN',
  market: 'UK',
  entry_date: '2026-04-01',
  exit_date: '2026-04-15',
  entry_price: 200.00,
  exit_price: 215.00,
  shares: 100,
  pnl: 1500.00,
  pnl_pct: 7.5,
  pnl_percent: 7.5,
  fee_drag_pct: null,
  slippage_pct: null,
  commission_gbp: null,
  spread_cost_gbp: null,
  net_r_multiple: null,
  exit_reason: 'Manual Exit',
  tags: [],
};

const TRADE_NEGATIVE_NET_R = {
  id: 'nr-t3',
  ticker: 'TSLA',
  market: 'US',
  entry_date: '2026-03-01',
  exit_date: '2026-03-10',
  entry_price: 220.00,
  exit_price: 205.00,
  shares: 30,
  pnl: -450.00,
  pnl_pct: -6.8,
  pnl_percent: -6.8,
  fee_drag_pct: 0.52,
  slippage_pct: 0.10,
  commission_gbp: 15.00,
  spread_cost_gbp: 4.50,
  net_r_multiple: -1.234,
  exit_reason: 'Stop Loss',
  tags: [],
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
}

async function mockTrades(page, trades = [], extra = {}) {
  const payload = {
    status: 'ok',
    data: {
      total_trades: trades.length,
      win_rate: 60.0,
      total_pnl: trades.reduce((s, t) => s + t.pnl, 0),
      avg_slippage_pct: null,
      avg_fee_drag_pct: null,
      trades,
      ...extra,
    },
  };
  await page.route(`${API}/trades`, route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
  // reflection endpoint returns 404 (no reflection)
  await page.route(new RegExp(`${API}/trades/.+/reflection`), route =>
    route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ status: 'error' }) })
  );
  await page.route(new RegExp(`${API}/trades/.+/plan-vs-reality`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { plan_linked: false } }) })
  );
}

async function gotoTradeHistory(page) {
  await page.goto('/#/TradeHistory');
  await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-NR-01 — Net R column header visible
// ---------------------------------------------------------------------------

test.describe('SC-NR-01 — Net R column header', () => {
  test('SC-NR-01: "Net R" column header visible on Trade History page', async ({ page }) => {
    await mockFallback(page);
    await mockTrades(page, [TRADE_WITH_COSTS]);
    await gotoTradeHistory(page);

    await expect(page.getByText('Net R')).toBeVisible({ timeout: 10000 });
  });
});

// ---------------------------------------------------------------------------
// SC-NR-02 — Net R value shown when cost data present (AC-02)
// ---------------------------------------------------------------------------

test.describe('SC-NR-02 — Net R value visible when costs recorded (AC-02)', () => {
  test('SC-NR-02: Net R value rendered for trade with commission and spread cost data', async ({ page }) => {
    await mockFallback(page);
    await mockTrades(page, [TRADE_WITH_COSTS]);
    await gotoTradeHistory(page);

    // net_r_multiple = 1.847 → displayed as "+1.85R"
    await expect(page.getByText(/\+1\.8[0-9]R/)).toBeVisible({ timeout: 10000 });
  });
});

// ---------------------------------------------------------------------------
// SC-NR-03 — Net R shows "—" for trades with no cost data (AC-04)
// ---------------------------------------------------------------------------

test.describe('SC-NR-03 — Backward-compat: "—" when no cost data (AC-04)', () => {
  test('SC-NR-03: Trades without cost data show dash in Net R column', async ({ page }) => {
    await mockFallback(page);
    await mockTrades(page, [TRADE_WITHOUT_COSTS]);
    await gotoTradeHistory(page);

    await expect(page.getByText('Net R')).toBeVisible({ timeout: 10000 });
    // The "—" placeholder is rendered; use a more targeted selector to avoid
    // collisions with other "—" cells (Days, Slippage, etc.)
    const netRCells = page.locator('td span.text-slate-600');
    await expect(netRCells.first()).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-NR-04 — Colour coding: positive green, negative red (AC-02)
// ---------------------------------------------------------------------------

test.describe('SC-NR-04 — Net R colour coding (AC-02)', () => {
  test('SC-NR-04a: Positive net R rendered in emerald (green)', async ({ page }) => {
    await mockFallback(page);
    await mockTrades(page, [TRADE_WITH_COSTS]);
    await gotoTradeHistory(page);

    const positiveNetR = page.locator('td span.text-emerald-400', { hasText: /R$/ });
    await expect(positiveNetR.first()).toBeVisible({ timeout: 10000 });
  });

  test('SC-NR-04b: Negative net R rendered in rose (red)', async ({ page }) => {
    await mockFallback(page);
    await mockTrades(page, [TRADE_NEGATIVE_NET_R]);
    await gotoTradeHistory(page);

    const negativeNetR = page.locator('td span.text-rose-400', { hasText: /R$/ });
    await expect(negativeNetR.first()).toBeVisible({ timeout: 10000 });
  });
});
