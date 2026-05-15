/**
 * Paper Account Panel — Playwright E2E Tests
 * ST-03 (EPIC-01, v3.5) — IT-06 Frontend: Paper Positions Display Panel
 *
 * AC-7: Playwright E2E test covers:
 *   SC-PA-01: Panel visible with mock paper positions data
 *   SC-PA-02: Panel hidden when paper tracking not configured (paper_tracking_enabled: false)
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Positions').
 * - Paper positions: GET /portfolio/paper-positions
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ─── Mock data ─────────────────────────────────────────────────────────────────

const PAPER_POSITIONS_RESPONSE = {
  status: 'ok',
  paper_tracking_enabled: true,
  positions: [
    {
      ticker: 'AAPL',
      paper_entry_price: 170.50,
      current_market_price: 182.00,
      paper_pnl_usd: 1150.00,
      paper_pnl_pct: 6.74,
      date_opened: null,
      position_size: 100,
    },
    {
      ticker: 'NVDA',
      paper_entry_price: 620.00,
      current_market_price: 580.00,
      paper_pnl_usd: -400.00,
      paper_pnl_pct: -0.65,
      date_opened: null,
      position_size: 10,
    },
  ],
};

const PAPER_DISABLED_RESPONSE = {
  paper_tracking_enabled: false,
};

const PORTFOLIO_STUB = {
  status: 'ok',
  data: {
    cash: 5000,
    cash_balance: 5000,
    total_value: 15000,
    open_positions_value: 10000,
    total_pnl: 500,
    initial_value: 14500,
    net_deposits: 14500,
    live_fx_rate: 1.27,
    last_updated: '2026-05-15T10:00:00Z',
    current_drawdown_percent: 0,
    peak_portfolio_value: 15000,
    positions: [
      {
        id: 'pos-001',
        ticker: 'AAPL',
        market: 'US',
        entry_date: '2026-04-01',
        entry_price: 170.50,
        shares: 100,
        current_price: 182.00,
        current_value: 18200,
        pnl: 1150,
        pnl_pct: 6.74,
        current_stop: 160.00,
        holding_days: 44,
        status: 'open',
        display_status: 'PROFITABLE',
        fx_rate: 1.27,
        grace_period: false,
        grace_days_remaining: null,
        live_fx_rate: 1.27,
      },
    ],
  },
};

const POSITIONS_STUB = {
  status: 'ok',
  data: PORTFOLIO_STUB.data.positions,
};

// ─── Route helpers ─────────────────────────────────────────────────────────────

async function mockFallback(page) {
  await page.route(`${API}/**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockPortfolio(page) {
  await page.route(/\/portfolio$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PORTFOLIO_STUB) })
  );
}

async function mockPositions(page) {
  await page.route(/\/positions$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(POSITIONS_STUB) })
  );
}

async function mockPaperEnabled(page) {
  await page.route(/\/portfolio\/paper-positions/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PAPER_POSITIONS_RESPONSE) })
  );
}

async function mockPaperDisabled(page) {
  await page.route(/\/portfolio\/paper-positions/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PAPER_DISABLED_RESPONSE) })
  );
}

// ─── SC-PA-01 — Panel visible with mock paper positions ────────────────────────

test.describe('SC-PA-01 — Paper Account Panel visible when configured', () => {
  test.beforeEach(async ({ page }) => {
    // LIFO: catch-all first, then specific mocks override
    await mockFallback(page);
    await mockPositions(page);
    await mockPortfolio(page);
    await mockPaperEnabled(page);

    await page.goto('/#/Positions');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });
  });

  test('SC-PA-01a: Paper Account panel header is visible', async ({ page }) => {
    await expect(page.getByTestId('paper-account-panel')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('Paper Account')).toBeVisible({ timeout: 8000 });
  });

  test('SC-PA-01b: Paper positions table renders with position data', async ({ page }) => {
    await expect(page.getByTestId('paper-positions-table')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('NVDA').first()).toBeVisible({ timeout: 8000 });
  });

  test('SC-PA-01c: §13 disclaimer label is present', async ({ page }) => {
    await expect(page.getByText(/hypothetical tracking/i).first()).toBeVisible({ timeout: 8000 });
  });
});

// ─── SC-PA-02 — Panel hidden when not configured ──────────────────────────────

test.describe('SC-PA-02 — Paper Account Panel hidden when not configured', () => {
  test.beforeEach(async ({ page }) => {
    await mockFallback(page);
    await mockPositions(page);
    await mockPortfolio(page);
    await mockPaperDisabled(page);

    await page.goto('/#/Positions');
    await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });
  });

  test('SC-PA-02a: Paper Account panel is NOT rendered when credentials absent', async ({ page }) => {
    await page.waitForTimeout(1500);
    await expect(page.getByTestId('paper-account-panel')).toHaveCount(0);
  });

  test('SC-PA-02b: No "Paper Account" header text when disabled', async ({ page }) => {
    await page.waitForTimeout(1500);
    const headers = page.locator('button').filter({ hasText: /^paper account$/i });
    await expect(headers).toHaveCount(0);
  });
});
