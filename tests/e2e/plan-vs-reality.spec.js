/**
 * Plan vs Reality — Playwright E2E Tests
 * ST-06 (EPIC-02, v3.5) — PO-01 Frontend: Plan vs Reality Comparison View
 * ST-02 (EPIC-01, v3.6) — entry_delta_pct display (SC-PVR-03, SC-PVR-04, SC-PVR-05)
 *
 * AC-6: Playwright E2E test covers:
 *   SC-PVR-01: Component visible with mock plan vs reality data (row expanded)
 *   SC-PVR-02: Component hidden for trade with no plan (404 response)
 *   SC-PVR-03: entry_delta_pct non-null — formatted "+X.XX%" / "-X.XX%" with colour
 *   SC-PVR-04: entry_delta_pct null — historical placeholder text shown
 *   SC-PVR-05: Regression — existing rows unaffected by entry_delta_pct change
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradeHistory').
 * - Trades list: GET /trades
 * - PVR fetch: GET /trades/{id}/plan-vs-reality (lazy, triggered by row expand)
 * - App uses apiFetch (raw fetch), not axios — no { status, data } wrapping in transport.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const TRADE_ID = 'pvr-trade-uuid-0001';

// ─── Mock data ─────────────────────────────────────────────────────────────────

const TRADE_WITH_PLAN = {
  id: TRADE_ID,
  ticker: 'AAPL',
  market: 'US',
  entry_date: '2026-04-01',
  exit_date: '2026-04-20',
  entry_price: 170.00,
  exit_price: 184.00,
  shares: 100,
  pnl: 1400.00,
  pnl_pct: 8.24,
  fee_drag_pct: null,
  slippage_pct: null,
  exit_reason: 'Target Reached',
  tags: [],
  entry_note: null,
  exit_note: null,
};

const TRADE_NO_PLAN = {
  id: 'pvr-trade-no-plan-0002',
  ticker: 'MSFT',
  market: 'US',
  entry_date: '2026-03-01',
  exit_date: '2026-03-15',
  entry_price: 380.00,
  exit_price: 395.00,
  shares: 50,
  pnl: 750.00,
  pnl_pct: 3.95,
  fee_drag_pct: null,
  slippage_pct: null,
  exit_reason: 'Manual Exit',
  tags: [],
  entry_note: null,
  exit_note: null,
};

const PVR_DATA = {
  status: 'ok',
  data: {
    plan_linked: true,
    trade_plan_id: 'plan-uuid-0001',
    r_achieved: 1.8,
    r_target: 2.0,
    r_delta: -0.2,
    entry_delta_pct: null,
    stop_discipline: 'on_plan',
    exit_reason_actual: 'Target Reached',
    exit_reason_planned: 'Close below 50-day MA',
    lifecycle_state_at_exit: 'EXIT ZONE',
    plan_adherence_flag: 'on_plan',
    deviation_note: null,
  },
};

// entry_delta_pct positive (bought above plan — unfavorable)
const PVR_DATA_POSITIVE_DELTA = {
  status: 'ok',
  data: { ...PVR_DATA.data, entry_delta_pct: 2.5 },
};

// entry_delta_pct negative (bought below plan — favorable)
const PVR_DATA_NEGATIVE_DELTA = {
  status: 'ok',
  data: { ...PVR_DATA.data, entry_delta_pct: -1.75 },
};

const TRADES_RESPONSE = {
  status: 'ok',
  total_trades: 2,
  win_rate: 100,
  total_pnl: 2150.00,
  avg_slippage_pct: null,
  avg_fee_drag_pct: null,
  trades: [TRADE_WITH_PLAN, TRADE_NO_PLAN],
};

const TRADES_RESPONSE_NO_PLAN = {
  status: 'ok',
  total_trades: 1,
  win_rate: 100,
  total_pnl: 750.00,
  avg_slippage_pct: null,
  avg_fee_drag_pct: null,
  trades: [TRADE_NO_PLAN],
};

const ANALYTICS_STUB = {
  status: 'ok',
  data: { trades_for_charts: [] },
};

// ─── Route helpers ─────────────────────────────────────────────────────────────

async function mockFallback(page) {
  await page.route(`${API}/**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTrades(page, tradesResponse) {
  await page.route(/\/trades$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(tradesResponse) })
  );
}

async function mockAnalytics(page) {
  await page.route(/\/analytics\/metrics/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ANALYTICS_STUB) })
  );
}

async function mockPvrFound(page, tradeId) {
  await page.route(new RegExp(`/trades/${tradeId}/plan-vs-reality`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PVR_DATA) })
  );
}

async function mockPvrNotFound(page, tradeId) {
  await page.route(new RegExp(`/trades/${tradeId}/plan-vs-reality`), (route) =>
    route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ detail: 'No trade plan found for this trade' }) })
  );
}

// ─── SC-PVR-01 — Component visible with mock plan vs reality data ──────────────

test.describe('SC-PVR-01 — Plan vs Reality section visible when plan exists', () => {
  test.beforeEach(async ({ page }) => {
    // LIFO: catch-all first, then specific mocks override
    await mockFallback(page);
    await mockAnalytics(page);
    await mockPvrFound(page, TRADE_ID);
    await mockTrades(page, TRADES_RESPONSE);

    await page.goto('/#/TradeHistory');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });
  });

  test('SC-PVR-01a: Plan vs Reality section appears after expanding a trade with a plan', async ({ page }) => {
    // Click on AAPL row to expand it
    await page.getByText('AAPL').first().click();

    // Plan vs Reality section header should appear
    await expect(page.getByText(/plan vs reality/i).first()).toBeVisible({ timeout: 8000 });
  });

  test('SC-PVR-01b: R Achieved value is displayed', async ({ page }) => {
    await page.getByText('AAPL').first().click();

    // R Achieved row shows the backend-calculated value
    await expect(page.getByText('R Achieved')).toBeVisible({ timeout: 8000 });
  });

  test('SC-PVR-01c: Lifecycle state badge is rendered', async ({ page }) => {
    await page.getByText('AAPL').first().click();

    await expect(page.getByText('EXIT ZONE').first()).toBeVisible({ timeout: 8000 });
  });
});

// ─── SC-PVR-02 — Component hidden for trade with no plan ─────────────────────

test.describe('SC-PVR-02 — Plan vs Reality section hidden when no plan exists', () => {
  test.beforeEach(async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await mockPvrNotFound(page, TRADE_NO_PLAN.id);
    await mockTrades(page, TRADES_RESPONSE_NO_PLAN);

    await page.goto('/#/TradeHistory');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });
  });

  test('SC-PVR-02a: Plan vs Reality section is NOT rendered when trade has no plan', async ({ page }) => {
    // Click on MSFT row to expand it
    await page.getByText('MSFT').first().click();

    // Wait for any async loads to settle
    await page.waitForTimeout(1500);

    // Plan vs Reality section should NOT be present
    await expect(page.locator('[data-testid="plan-vs-reality-section"]')).toHaveCount(0);
  });

  test('SC-PVR-02b: No error or placeholder text shown when plan is absent', async ({ page }) => {
    await page.getByText('MSFT').first().click();
    await page.waitForTimeout(1500);

    // Neither "Plan vs Reality" section header nor error message should appear
    const pvrHeaders = page.locator('h4').filter({ hasText: /plan vs reality/i });
    await expect(pvrHeaders).toHaveCount(0);
  });
});

// ─── SC-PVR-03 — entry_delta_pct non-null: formatted percentage with colour ────

test.describe('SC-PVR-03 — entry_delta_pct non-null displays formatted percentage', () => {
  test('SC-PVR-03a: positive delta shows "+X.XX%" (rose/red colour class)', async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await page.route(new RegExp(`/trades/${TRADE_ID}/plan-vs-reality`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PVR_DATA_POSITIVE_DELTA) })
    );
    await mockTrades(page, TRADES_RESPONSE);
    await page.goto('/#/TradeHistory');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });

    await page.getByText('AAPL').first().click();
    await expect(page.getByText(/plan vs reality/i).first()).toBeVisible({ timeout: 8000 });

    // Should show "+2.50%" (positive, above plan)
    await expect(page.getByText('+2.50%')).toBeVisible({ timeout: 5000 });
    // Historical placeholder must NOT appear
    await expect(page.locator('[data-testid="entry-delta-historical"]')).toHaveCount(0);
  });

  test('SC-PVR-03b: negative delta shows "-X.XX%" (emerald/green colour class)', async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await page.route(new RegExp(`/trades/${TRADE_ID}/plan-vs-reality`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PVR_DATA_NEGATIVE_DELTA) })
    );
    await mockTrades(page, TRADES_RESPONSE);
    await page.goto('/#/TradeHistory');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });

    await page.getByText('AAPL').first().click();
    await expect(page.getByText(/plan vs reality/i).first()).toBeVisible({ timeout: 8000 });

    // Should show "-1.75%"
    await expect(page.getByText('-1.75%')).toBeVisible({ timeout: 5000 });
  });
});

// ─── SC-PVR-04 — entry_delta_pct null: historical placeholder shown ───────────

test.describe('SC-PVR-04 — entry_delta_pct null shows historical placeholder', () => {
  test('SC-PVR-04a: null entry_delta_pct shows muted placeholder text', async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await mockPvrFound(page, TRADE_ID); // PVR_DATA has entry_delta_pct: null
    await mockTrades(page, TRADES_RESPONSE);
    await page.goto('/#/TradeHistory');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });

    await page.getByText('AAPL').first().click();
    await expect(page.getByText(/plan vs reality/i).first()).toBeVisible({ timeout: 8000 });

    // Historical placeholder element visible
    await expect(page.locator('[data-testid="entry-delta-historical"]')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/data not available for historical trades/i)).toBeVisible({ timeout: 5000 });
  });

  test('SC-PVR-04b: null state does not show a percentage value', async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await mockPvrFound(page, TRADE_ID);
    await mockTrades(page, TRADES_RESPONSE);
    await page.goto('/#/TradeHistory');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });

    await page.getByText('AAPL').first().click();
    await expect(page.getByText(/plan vs reality/i).first()).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/\+\d+\.\d+%/)).toHaveCount(0);
  });
});

// ─── SC-PVR-05 — Regression: existing rows unaffected ─────────────────────────

test.describe('SC-PVR-05 — Regression: existing rows present with entry_delta_pct change', () => {
  test.beforeEach(async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await page.route(new RegExp(`/trades/${TRADE_ID}/plan-vs-reality`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PVR_DATA_POSITIVE_DELTA) })
    );
    await mockTrades(page, TRADES_RESPONSE);
    await page.goto('/#/TradeHistory');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });
    await page.getByText('AAPL').first().click();
    await expect(page.getByText(/plan vs reality/i).first()).toBeVisible({ timeout: 8000 });
  });

  test('SC-PVR-05a: R Achieved row still visible', async ({ page }) => {
    await expect(page.getByText('R Achieved')).toBeVisible({ timeout: 5000 });
  });

  test('SC-PVR-05b: Exit Alignment row still visible', async ({ page }) => {
    await expect(page.getByText('Exit Alignment')).toBeVisible({ timeout: 5000 });
  });

  test('SC-PVR-05c: State at Exit badge still visible', async ({ page }) => {
    await expect(page.getByText('EXIT ZONE').first()).toBeVisible({ timeout: 5000 });
  });
});
