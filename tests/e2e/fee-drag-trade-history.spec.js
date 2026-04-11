/**
 * Fee Drag — Automated Acceptance Tests
 * ST-06 (v2.6)
 *
 * Covers: SC-FEE-01, SC-FEE-02, SC-FEE-03, SC-FEE-04
 * (SC-FEE-05 and SC-FEE-06 are backend unit tests in test_trade_service.py)
 *
 * Spec: docs/testing/fee-drag-scenarios.md v1.0
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/TradeHistory').
 * - api.trades.list() → GET /trades → { trades: [...], avg_fee_drag_pct: N }
 * - tradesData.avg_fee_drag_pct drives the Avg Fee Drag StatsCard
 * - Each trade.fee_drag_pct drives individual row colour in TradeHistoryTable
 *   (null → text-slate-500 "—", non-null → text-amber-400 "+X.XX%")
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Seed data
// ---------------------------------------------------------------------------

/** Trade with non-null fee drag (exit_fees / gross_proceeds computed server-side) */
const TRADE_WITH_FEE_DRAG = {
  id: 'fee-t1',
  ticker: 'LGEN',
  market: 'UK',
  entry_date: '2026-03-01',
  exit_date: '2026-03-15',
  entry_price: 200.00,
  exit_price: 220.00,
  shares: 100,
  pnl: 1990.05,
  pnl_percent: 9.95,
  fee_drag_pct: 0.45,       // exit_fees=9.95 / gross_proceeds=2200 * 100
  slippage_pct: null,
  exit_reason: 'Target Reached',
  tags: [],
};

/** Trade with null fee drag (no exit_fees recorded) */
const TRADE_NO_FEE_DRAG = {
  id: 'fee-t2',
  ticker: 'BARC',
  market: 'UK',
  entry_date: '2026-02-01',
  exit_date: '2026-02-28',
  entry_price: 150.00,
  exit_price: 155.00,
  shares: 50,
  pnl: 250.00,
  pnl_percent: 3.33,
  fee_drag_pct: null,       // no exit_fees recorded — pre-v2.5 trade
  slippage_pct: null,
  exit_reason: 'Manual Exit',
  tags: [],
};

/** Second trade with fee drag (for avg calculation) */
const TRADE_WITH_FEE_DRAG_2 = {
  id: 'fee-t3',
  ticker: 'VOD',
  market: 'UK',
  entry_date: '2026-01-10',
  exit_date: '2026-01-25',
  entry_price: 80.00,
  exit_price: 85.00,
  shares: 200,
  pnl: 990.10,
  pnl_percent: 6.19,
  fee_drag_pct: 0.25,       // second trade for avg test
  slippage_pct: null,
  exit_reason: 'Manual Exit',
  tags: [],
};

/** Response with two fee-drag trades (avg = (0.45+0.25)/2 = 0.35) */
const TRADES_WITH_AVG_RESPONSE = {
  status: 'ok',
  trades: [TRADE_WITH_FEE_DRAG, TRADE_WITH_FEE_DRAG_2],
  avg_fee_drag_pct: 0.35,
  avg_slippage_pct: null,
  total_pnl: 1980.15,
  total_trades: 2,
  win_rate: 100,
};

/** Response including null-drag trade */
const TRADES_MIXED_RESPONSE = {
  status: 'ok',
  trades: [TRADE_WITH_FEE_DRAG, TRADE_NO_FEE_DRAG],
  avg_fee_drag_pct: 0.45,   // only LGEN contributes — BARC excluded (null)
  avg_slippage_pct: null,
  total_pnl: 2240.05,
  total_trades: 2,
  win_rate: 100,
};

/** Response with all-null fee drag (no avg) */
const TRADES_NULL_AVG_RESPONSE = {
  status: 'ok',
  trades: [TRADE_NO_FEE_DRAG],
  avg_fee_drag_pct: null,
  avg_slippage_pct: null,
  total_pnl: 250.00,
  total_trades: 1,
  win_rate: 100,
};

const ANALYTICS_STUB = {
  status: 'ok',
  data: { trades_for_charts: [] },
};

// ---------------------------------------------------------------------------
// Shared mock setup
// ---------------------------------------------------------------------------

async function mockBaseEndpoints(page, tradesResponse) {
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(tradesResponse),
    })
  );
  await page.route(`${API}/analytics/metrics**`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(ANALYTICS_STUB),
    })
  );
  // Catch-all for any other endpoints
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

// ---------------------------------------------------------------------------
// SC-FEE-01 — Fee Drag column header is present
// ---------------------------------------------------------------------------

test.describe('SC-FEE-01 — Fee Drag column header', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page, TRADES_MIXED_RESPONSE);
    await page.goto('/#/TradeHistory');
    await page.waitForSelector('table', { timeout: 10000 });
  });

  test('SC-FEE-01a: Fee Drag column header is visible in the trade table', async ({ page }) => {
    // Column header rendered as a <button> for sortability (matching slippage pattern)
    await expect(page.getByRole('button', { name: /fee drag/i })).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// SC-FEE-02 — Non-null fee_drag_pct renders amber with +X.XX% format
// ---------------------------------------------------------------------------

test.describe('SC-FEE-02 — Non-null fee drag renders amber', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page, TRADES_MIXED_RESPONSE);
    await page.goto('/#/TradeHistory');
    await page.waitForSelector('table', { timeout: 10000 });
  });

  test('SC-FEE-02a: Trade with fee_drag_pct renders +X.XX% in amber', async ({ page }) => {
    // LGEN has fee_drag_pct: 0.45 → formatFeeDrag → "+0.45%", class → text-amber-400
    const feeCell = page.locator('.text-amber-400').filter({ hasText: '+0.45%' });
    await expect(feeCell).toBeVisible();
  });

  test('SC-FEE-02b: Fee drag value uses + prefix for non-negative values', async ({ page }) => {
    // fee drag is always a cost (≥ 0), formatFeeDrag always prepends "+"
    await expect(page.locator('text=+0.45%')).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// SC-FEE-03 — Avg Fee Drag StatsCard shows calculated average
// ---------------------------------------------------------------------------

test.describe('SC-FEE-03 — Avg Fee Drag StatsCard', () => {
  test('SC-FEE-03a: StatsCard shows avg_fee_drag_pct from API response', async ({ page }) => {
    await mockBaseEndpoints(page, TRADES_WITH_AVG_RESPONSE);
    await page.goto('/#/TradeHistory');
    await page.waitForSelector('table', { timeout: 10000 });

    // avg_fee_drag_pct: 0.35 → rendered as "+0.35%"
    const statsSection = page.locator('text=Avg Fee Drag').locator('..');
    await expect(statsSection).toBeVisible();
    await expect(page.locator('text=+0.35%')).toBeVisible();
  });

  test('SC-FEE-03b: StatsCard shows em dash when avg_fee_drag_pct is null', async ({ page }) => {
    await mockBaseEndpoints(page, TRADES_NULL_AVG_RESPONSE);
    await page.goto('/#/TradeHistory');
    await page.waitForSelector('table', { timeout: 10000 });

    // When avg_fee_drag_pct is null, StatsCard value renders as "—"
    const avgFeeDragCard = page.locator('text=Avg Fee Drag').locator('../..');
    await expect(avgFeeDragCard.locator('text=—')).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// SC-FEE-04 — Null fee_drag_pct renders em dash in slate colour
// ---------------------------------------------------------------------------

test.describe('SC-FEE-04 — Null fee drag shows em dash', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page, TRADES_MIXED_RESPONSE);
    await page.goto('/#/TradeHistory');
    await page.waitForSelector('table', { timeout: 10000 });
  });

  test('SC-FEE-04a: Trade without fee drag shows em dash in slate colour', async ({ page }) => {
    // BARC has fee_drag_pct: null → formatFeeDrag → "—", class → text-slate-500
    const barcRow = page.locator('tr').filter({ hasText: 'BARC' });
    await expect(barcRow).toBeVisible();
    const feeDragCell = barcRow.locator('.text-slate-500').filter({ hasText: '—' });
    await expect(feeDragCell).toBeVisible();
  });

  test('SC-FEE-04b: Trades with fee drag still render correctly alongside null rows', async ({ page }) => {
    // Confirm LGEN amber value is visible in the same table as BARC null row
    await expect(page.locator('text=+0.45%')).toBeVisible();
    await expect(page.locator('text=BARC')).toBeVisible();
  });
});
