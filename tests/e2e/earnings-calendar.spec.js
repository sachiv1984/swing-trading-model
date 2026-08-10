/**
 * Earnings Calendar UI Tests — ST-08 (EPIC-03, v3.1)
 *
 * Verifies that the earnings column renders correctly across Screener,
 * Watchlist, and Positions pages, and that the Positions page shows an
 * amber proximity warning when earnings are ≤5 days away.
 *
 * Scenarios:
 *   SC-EARN-01  Screener page has "Earnings" column header
 *   SC-EARN-02  Screener row shows days until earnings when data available
 *   SC-EARN-03  Screener row shows "—" when earnings data unavailable (null)
 *   SC-EARN-04  Watchlist page has "Earnings" column header
 *   SC-EARN-05  Watchlist row shows days until earnings when data available
 *   SC-EARN-06  Watchlist row shows "—" when earnings data unavailable (null)
 *   SC-EARN-07  Positions page has "Earnings" column header
 *   SC-EARN-08  Positions row shows amber ⚠ warning when earnings ≤5 days away
 *   SC-EARN-09  Positions row shows plain days (no ⚠) when earnings >5 days away
 *
 * Infrastructure: page.route() network interception — no live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data helpers
// ---------------------------------------------------------------------------

function makeEarnings(days) {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return {
    next_earnings_date: d.toISOString().split('T')[0],
    days_until_earnings: days,
    fiscal_quarter: 'Q2',
    data_source: 'yahoo_finance',
  };
}

const NULL_EARNINGS = {
  next_earnings_date: null,
  days_until_earnings: null,
  fiscal_quarter: null,
  data_source: null,
};

function makeScreenerResult(overrides = {}) {
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
    news_headline_count: 0,
    ...overrides,
  };
}

function makeWatchlistEntry(overrides = {}) {
  return {
    id: 1,
    ticker: 'MSFT',
    market: 'US',
    target_entry_price: 380.00,
    initial_stop_price: 360.00,
    current_stop_price: 362.00,
    notes: '',
    added_date: '2026-04-01',
    ...overrides,
  };
}

function makePosition(overrides = {}) {
  return {
    id: 'pos-001',
    ticker: 'NVDA',
    market: 'US',
    entry_price: 800.00,
    current_price: 850.00,
    current_price_native: 850.00,
    stop_price: 760.00,
    stop_price_native: 760.00,
    shares: 10,
    pnl: 500.00,
    pnl_percent: 6.25,
    holding_days: 5,
    grace_days_remaining: null,
    status: 'open',
    entry_date: '2026-04-01',
    initial_stop: 760.00,
    tags: null,
    ...overrides,
  };
}

async function stubAlerts(page) {
  await page.route(`${API}/alerts/history`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
}

async function goto(page, hash) {
  await page.goto(hash);
  await page.waitForLoadState('domcontentloaded');
}

// ---------------------------------------------------------------------------
// Screener — SC-EARN-01 to SC-EARN-03
// ---------------------------------------------------------------------------

test.describe('Screener — Earnings column', () => {
  test.beforeEach(async ({ page }) => {
    await stubAlerts(page);
  });

  async function setupScreener(page, earningsPayload) {
    const result = makeScreenerResult();
    await page.route(`${API}/screener/results**`, (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          results: [result],
          run_id: 'r1',
          run_timestamp: new Date().toISOString(),
          total: 1,
          limit: 200,
          offset: 0,
        }),
      })
    );
    await page.route(`${API}/screener/run`, (route) =>
      route.fulfill({ status: 202, contentType: 'application/json', body: JSON.stringify({ ok: true, data: { run_id: 'r2', status: 'accepted' } }) })
    );
    await page.route(`${API}/watchlist`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
    );
    await page.route(`${API}/earnings/**`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(earningsPayload) })
    );
    // ST-21 (BLG-FEAT-29, v8.5): stub the Regime History panel's own data call.
    await page.route(`${API}/screener/regime-distribution**`, (route) =>
      route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify({ ok: true, data: { window: '30d', run_count: 1, total_observations: 2, risk_on_count: 2, risk_off_count: 0, risk_on_pct: 100.0, risk_off_pct: 0.0 } }),
      })
    );
  }

  test('SC-EARN-01: Screener page has Earnings column header', async ({ page }) => {
    await setupScreener(page, NULL_EARNINGS);
    await goto(page, '/#/Screener');

    await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
    await expect(page.getByRole('columnheader', { name: /earnings/i })).toBeVisible();
  });

  test('SC-EARN-02: Screener row shows days until earnings when data available', async ({ page }) => {
    await setupScreener(page, makeEarnings(14));
    await goto(page, '/#/Screener');

    await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('body')).toContainText(/14d/i, { timeout: 5000 });
  });

  test('SC-EARN-03: Screener row shows dash when earnings data unavailable', async ({ page }) => {
    await setupScreener(page, NULL_EARNINGS);
    await goto(page, '/#/Screener');

    await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('body')).toContainText('—', { timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// Watchlist — SC-EARN-04 to SC-EARN-06
// ---------------------------------------------------------------------------

test.describe('Watchlist — Earnings column', () => {
  test.beforeEach(async ({ page }) => {
    await stubAlerts(page);
  });

  async function setupWatchlist(page, earningsPayload) {
    await page.route(`${API}/watchlist`, (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({
          status: 200,
          contentType: 'application/json',
          // Watchlist page parses json.data (not json.items)
          body: JSON.stringify({ data: [makeWatchlistEntry()] }),
        });
      }
      return route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ id: 2 }) });
    });
    await page.route(`${API}/earnings/**`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(earningsPayload) })
    );
    await page.route(`${API}/news/**`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ headlines: [] }) })
    );
    await page.route(`${API}/portfolio/**`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: {} }) })
    );
  }

  test('SC-EARN-04: Watchlist page has Earnings column header', async ({ page }) => {
    await setupWatchlist(page, NULL_EARNINGS);
    await goto(page, '/#/Watchlist');

    await expect(page.getByText('MSFT')).toBeVisible({ timeout: 8000 });
    await expect(page.getByRole('columnheader', { name: /earnings/i })).toBeVisible();
  });

  test('SC-EARN-05: Watchlist row shows days until earnings when data available', async ({ page }) => {
    await setupWatchlist(page, makeEarnings(21));
    await goto(page, '/#/Watchlist');

    await expect(page.getByText('MSFT')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('body')).toContainText(/21d/i, { timeout: 5000 });
  });

  test('SC-EARN-06: Watchlist row shows dash when earnings data unavailable', async ({ page }) => {
    await setupWatchlist(page, NULL_EARNINGS);
    await goto(page, '/#/Watchlist');

    await expect(page.getByText('MSFT')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('body')).toContainText('—', { timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// Positions — SC-EARN-07 to SC-EARN-09
// ---------------------------------------------------------------------------

test.describe('Positions — Earnings column and proximity warning', () => {
  test.beforeEach(async ({ page }) => {
    await stubAlerts(page);
  });

  async function setupPositions(page, earningsPayload) {
    await page.route('**/positions*', (route) => {
      const url = route.request().url();
      if (url.includes('/positions/compliance')) {
        return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
      }
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([makePosition()]),
      });
    });
    await page.route('**/portfolio**', (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: { portfolio_size: 10000, cash: 5000 } }) })
    );
    await page.route('**/analytics/**', (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: {} }) })
    );
    await page.route('**/compliance/**', (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
    );
    await page.route(`${API}/watchlist**`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
    );
    await page.route(`${API}/earnings/**`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(earningsPayload) })
    );
  }

  async function switchToTableView(page) {
    await page.getByRole('button', { name: 'Table view' }).click();
    // Wait for table to render
    await page.waitForSelector('table', { timeout: 5000 });
  }

  test('SC-EARN-07: Positions table view has Earnings column header', async ({ page }) => {
    await setupPositions(page, NULL_EARNINGS);
    await goto(page, '/#/Positions');

    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    await switchToTableView(page);
    await expect(page.getByRole('columnheader', { name: /earnings/i })).toBeVisible();
  });

  test('SC-EARN-08: Positions table row shows amber warning when earnings ≤5 days away', async ({ page }) => {
    await setupPositions(page, makeEarnings(3));
    await goto(page, '/#/Positions');

    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    await switchToTableView(page);
    // PositionEarningsCell renders "⚠ 3d" when days ≤ 5
    await expect(page.locator('body')).toContainText(/⚠/, { timeout: 5000 });
    await expect(page.locator('body')).toContainText(/3d/, { timeout: 5000 });
  });

  test('SC-EARN-09: Positions table row shows plain days (no ⚠) when earnings >5 days away', async ({ page }) => {
    await setupPositions(page, makeEarnings(30));
    await goto(page, '/#/Positions');

    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    await switchToTableView(page);
    // Should show "30d" without warning icon
    await expect(page.locator('body')).toContainText(/30d/, { timeout: 5000 });
    const bodyText = await page.locator('body').textContent();
    expect(bodyText).not.toMatch(/⚠\s*30d|30d\s*⚠/);
  });
});
