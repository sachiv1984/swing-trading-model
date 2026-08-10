/**
 * Screener UK Ticker Suffix Tests — ST-06 (EPIC-03, v3.1)
 *
 * Verifies that UK tickers returned by the API with a `.L` suffix are
 * stripped before display in the screener results table and watchlist
 * promotion popover, and that POST /watchlist receives the stripped ticker.
 *
 * Scenarios:
 *   SC-UK-01  UK ticker `BP.L` displayed as `BP` in results table (no .L)
 *   SC-UK-02  US ticker displayed unchanged
 *   SC-UK-03  Watchlist promotion popover header shows stripped UK ticker
 *   SC-UK-04  POST /watchlist body sends stripped ticker (no .L)
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

function makeResult(overrides = {}) {
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

function screenerBody(results) {
  return {
    results,
    run_id: 'run-001',
    run_timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
    total: results.length,
    limit: 200,
    offset: 0,
  };
}

async function stubScreener(page, results) {
  await page.route(`${API}/screener/results**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(screenerBody(results)) })
  );
  await page.route(`${API}/screener/run`, (route) =>
    route.fulfill({ status: 202, contentType: 'application/json', body: JSON.stringify({ ok: true, data: { run_id: 'r2', status: 'accepted' } }) })
  );
  // ST-21 (BLG-FEAT-29, v8.5): stub the Regime History panel's own data call
  // so it doesn't fire an unhandled real network request during these tests.
  await page.route(`${API}/screener/regime-distribution**`, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ ok: true, data: { window: '30d', run_count: 1, total_observations: 2, risk_on_count: 2, risk_off_count: 0, risk_on_pct: 100.0, risk_off_pct: 0.0 } }),
    })
  );
}

async function stubWatchlistGet(page) {
  await page.route(`${API}/watchlist`, (route) => {
    if (route.request().method() === 'GET') {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) });
    }
    return route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ id: 1 }) });
  });
}

async function goto(page, hash) {
  await page.goto(hash);
  await page.waitForLoadState('domcontentloaded');
}

test.beforeEach(async ({ page }) => {
  await page.route(`${API}/alerts/history`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  // Stub earnings — null for all tickers so it doesn't interfere
  await page.route(`${API}/earnings/**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null, days_until_earnings: null, fiscal_quarter: null, data_source: null }) })
  );
});

// SC-UK-01: UK ticker .L suffix stripped in screener results table
test('SC-UK-01: UK ticker .L suffix stripped in screener results table', async ({ page }) => {
  await stubScreener(page, [makeResult({ ticker: 'BP.L', market: 'UK', currency: 'GBP' })]);
  await stubWatchlistGet(page);

  await goto(page, '/#/Screener');

  // Table should show 'BP', not 'BP.L'
  await expect(page.getByText('BP').first()).toBeVisible({ timeout: 8000 });
  const cells = page.locator('td');
  const allText = await cells.allTextContents();
  expect(allText.some((t) => t.includes('BP.L'))).toBe(false);
});

// SC-UK-02: US ticker unaffected — no suffix stripped
test('SC-UK-02: US ticker displayed unchanged in screener results table', async ({ page }) => {
  await stubScreener(page, [makeResult({ ticker: 'AAPL', market: 'US' })]);
  await stubWatchlistGet(page);

  await goto(page, '/#/Screener');

  await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
});

// SC-UK-03: Watchlist promotion popover header shows stripped UK ticker
test('SC-UK-03: Watchlist promotion popover header strips .L from UK ticker', async ({ page }) => {
  await stubScreener(page, [makeResult({ ticker: 'BP.L', market: 'UK', currency: 'GBP' })]);
  await stubWatchlistGet(page);

  await goto(page, '/#/Screener');
  await expect(page.getByText('BP').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('button', { name: /add.*watchlist|watchlist/i }).first().click();

  // Popover header: "Add BP to Watchlist" — no .L
  await expect(page.getByText(/Add BP to Watchlist/i)).toBeVisible({ timeout: 3000 });
  // .L must not appear anywhere visible
  await expect(page.locator('body')).not.toContainText('BP.L');
});

// SC-UK-04: POST /watchlist body sends stripped ticker (no .L) for UK tickers
test('SC-UK-04: POST /watchlist body ticker has .L stripped for UK tickers', async ({ page }) => {
  await stubScreener(page, [makeResult({ ticker: 'BP.L', market: 'UK', currency: 'GBP' })]);

  let capturedBody = null;
  await page.route(`${API}/watchlist`, (route) => {
    if (route.request().method() === 'GET') {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) });
    }
    capturedBody = route.request().postDataJSON();
    return route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ id: 1 }) });
  });

  await goto(page, '/#/Screener');
  await expect(page.getByText('BP').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('button', { name: /add.*watchlist|watchlist/i }).first().click();

  // Confirm if popover has a confirm button
  const confirmBtn = page.getByRole('button', { name: /confirm|add|save/i }).last();
  const visible = await confirmBtn.isVisible().catch(() => false);
  if (visible) await confirmBtn.click();

  await page.waitForTimeout(500);
  expect(capturedBody).not.toBeNull();
  expect(capturedBody.ticker).toBe('BP');
  expect(capturedBody.ticker).not.toContain('.L');
});
