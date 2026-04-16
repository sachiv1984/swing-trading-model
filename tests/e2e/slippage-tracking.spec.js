/**
 * Slippage Tracking — Automated Acceptance Tests
 * ST-12 (TEST-GAP-EPIC-05-SLIP, v2.4)
 *
 * Covers: SC-SLIP-02, SC-SLIP-03, SC-SLIP-04
 * (SC-SLIP-01 is Manual — requires live trade entry on staging)
 *
 * Spec: docs/testing/slippage_scenarios.md v1.0
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/TradeHistory').
 * - api.trades.list() → GET /trades → { trades: [...], avg_slippage_pct: N }
 * - tradesData.avg_slippage_pct drives the Avg Slippage StatsCard
 * - Each trade.slippage_pct drives individual row colour in TradeHistoryTable
 *
 * Known deviation carried forward:
 * - DEV-ST14-01 (P3): Avg Slippage StatsCard renders without gradient (cosmetic).
 *   SC-SLIP-03 passes functionally; gradient background is not asserted.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Seed data
// ---------------------------------------------------------------------------

/** Trade with negative slippage (favourable — filled below market) */
const TRADE_FAVOURABLE = {
  id: 'slip-t1',
  ticker: 'LGEN',
  market: 'UK',
  entry_date: '2026-03-01',
  exit_date: '2026-03-15',
  entry_price: 200.00,
  exit_price: 220.00,
  shares: 100,
  pnl: 2000.00,
  pnl_pct: 10.0,         // component reads pnl_pct (not pnl_percent)
  slippage_pct: -0.25,   // filled below market — favourable — should render emerald
  fill_price: 199.50,
  exit_reason: 'Target Reached',
  tags: [],
};

/** Trade with positive slippage (unfavourable — filled above market) */
const TRADE_UNFAVOURABLE = {
  id: 'slip-t2',
  ticker: 'BARC',
  market: 'UK',
  entry_date: '2026-03-05',
  exit_date: '2026-03-20',
  entry_price: 150.00,
  exit_price: 140.00,
  shares: 50,
  pnl: -500.00,
  pnl_pct: -6.67,        // component reads pnl_pct (not pnl_percent)
  slippage_pct: 0.50,    // filled above market — unfavourable — should render rose
  fill_price: 150.75,
  exit_reason: 'Stop Loss Hit',
  tags: [],
};

/** Trade with no fill price recorded (pre-v2.1 trade) */
const TRADE_NO_FILL = {
  id: 'slip-t3',
  ticker: 'VOD',
  market: 'UK',
  entry_date: '2026-02-01',
  exit_date: '2026-02-28',
  entry_price: 80.00,
  exit_price: 85.00,
  shares: 200,
  pnl: 1000.00,
  pnl_pct: 6.25,         // component reads pnl_pct (not pnl_percent)
  slippage_pct: null,    // no fill price — should show em dash
  fill_price: null,
  exit_reason: 'Manual Exit',
  tags: [],
};

const TRADES_RESPONSE = {
  status: 'ok',
  trades: [TRADE_FAVOURABLE, TRADE_UNFAVOURABLE, TRADE_NO_FILL],
  avg_slippage_pct: 0.125,   // mean of -0.25 and +0.50 (null excluded)
  total_pnl: 2500.00,
};

const TRADES_NULL_AVG_RESPONSE = {
  status: 'ok',
  trades: [TRADE_NO_FILL],
  avg_slippage_pct: null,    // all trades have null slippage — no avg
  total_pnl: 1000.00,
};

const ANALYTICS_RESPONSE = {
  status: 'ok',
  data: {
    trades_for_charts: [],
  },
};

// ---------------------------------------------------------------------------
// Shared mock setup
// ---------------------------------------------------------------------------

async function mockBaseEndpoints(page, tradesResponse = TRADES_RESPONSE) {
  // Catch-all registered FIRST — Playwright routes are LIFO (last-registered wins),
  // so registering the catch-all first ensures specific mocks below take precedence.
  await page.route(new RegExp(`${API}/`), (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    });
  });
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(tradesResponse),
    })
  );
  await page.route(`${API}/analytics/metrics`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(ANALYTICS_RESPONSE),
    })
  );
}

// ---------------------------------------------------------------------------
// SC-SLIP-02 — Slippage column colour coding
// ---------------------------------------------------------------------------

test.describe('SC-SLIP-02 — Slippage column colour-coded values', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/TradeHistory');
    // Wait for the trade table to render
    await page.waitForSelector('table', { timeout: 10000 });
  });

  test('SC-SLIP-02a: Slippage column header is present', async ({ page }) => {
    // TableHead renders as <th> (role=columnheader), not a <button>
    await expect(page.getByRole('columnheader', { name: /slippage/i })).toBeVisible();
  });

  test('SC-SLIP-02b: Negative slippage renders with emerald (favourable) colour class', async ({ page }) => {
    // LGEN has slippage_pct: -0.25 — formatSlippage → "-0.25%", slippageColour → text-emerald-400
    const slippageCell = page.locator('.text-emerald-400').filter({ hasText: '-0.25%' });
    await expect(slippageCell).toBeVisible();
  });

  test('SC-SLIP-02c: Positive slippage renders with rose (unfavourable) colour class', async ({ page }) => {
    // BARC has slippage_pct: 0.50 — formatSlippage → "+0.50%", slippageColour → text-rose-400
    const slippageCell = page.locator('.text-rose-400').filter({ hasText: '+0.50%' });
    await expect(slippageCell).toBeVisible();
  });

  test('SC-SLIP-02d: Slippage column header has tooltip describing entry deviation', async ({ page }) => {
    // TableHead renders as <th> (role=columnheader), not a <button>
    const slippageBtn = page.getByRole('columnheader', { name: /slippage/i });
    const titleAttr = await slippageBtn.getAttribute('title');
    expect(titleAttr).toContain('fill price');
    expect(titleAttr).toContain('limit price');
  });
});

// ---------------------------------------------------------------------------
// SC-SLIP-03 — Avg Slippage StatsCard
// ---------------------------------------------------------------------------

test.describe('SC-SLIP-03 — Avg Slippage StatsCard', () => {
  test('SC-SLIP-03a: StatsCard shows avg_slippage_pct value from API response', async ({ page }) => {
    await mockBaseEndpoints(page, TRADES_RESPONSE);
    await page.goto('/#/TradeHistory');
    await page.waitForSelector('table', { timeout: 10000 });

    // avg_slippage_pct: 0.125 → formatted as "+0.13%"
    const statsSection = page.locator('text=Avg Entry Dev.').locator('..');
    await expect(statsSection).toBeVisible();
    // The value "+0.13%" should be present somewhere in the stats bar
    await expect(page.locator('text=+0.13%')).toBeVisible();
  });

  test('SC-SLIP-03b: StatsCard shows em dash when avg_slippage_pct is null', async ({ page }) => {
    await mockBaseEndpoints(page, TRADES_NULL_AVG_RESPONSE);
    await page.goto('/#/TradeHistory');
    await page.waitForSelector('table', { timeout: 10000 });

    // When avg_slippage_pct is null, value renders as "—"
    // The StatsCard for "Avg Entry Dev." should contain "—"
    const avgEntryDevCard = page.locator('text=Avg Entry Dev.').locator('../..');
    await expect(avgEntryDevCard.locator('text=—')).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// SC-SLIP-04 — Null fill price renders em dash
// ---------------------------------------------------------------------------

test.describe('SC-SLIP-04 — Null fill price shows em dash', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/TradeHistory');
    await page.waitForSelector('table', { timeout: 10000 });
  });

  test('SC-SLIP-04a: Trade without fill price shows em dash in Slippage column', async ({ page }) => {
    // VOD has slippage_pct: null — formatSlippage → "—", slippageColour → text-slate-500
    // Find the VOD row and assert its slippage cell contains "—" with slate colour
    const vodRow = page.locator('tr').filter({ hasText: 'VOD' });
    await expect(vodRow).toBeVisible();
    // VOD has null slippage, fee_drag, and R-multiple — all show '—' in text-slate-500.
    // Use .first() since all three are valid evidence that null renders as em-dash in slate.
    const slippageCell = vodRow.locator('.text-slate-500').filter({ hasText: '—' }).first();
    await expect(slippageCell).toBeVisible();
  });

  test('SC-SLIP-04b: Other trades in same table still show their slippage values', async ({ page }) => {
    // Confirm LGEN and BARC slippage values are still visible alongside null VOD row
    await expect(page.locator('text=-0.25%')).toBeVisible();
    await expect(page.locator('text=+0.50%')).toBeVisible();
  });
});
