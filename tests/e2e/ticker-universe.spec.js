/**
 * Ticker Universe Management Page — Playwright Tests
 * ST-09 (v3.8 EPIC-04)
 *
 * Covers:
 *   SC-TU-01: Page renders with table of tickers and "Add Ticker" button
 *   SC-TU-02: Adding a ticker via the form calls POST /ticker-universe and updates table
 *   SC-TU-03: Toggle deactivates an active ticker (DELETE /ticker-universe/{ticker})
 *   SC-TU-04: Delete button calls DELETE /ticker-universe/{ticker}
 *   SC-TU-05: Market filter (All/US/UK) shows only matching rows
 *   SC-TU-06: Active status filter shows only matching rows
 *
 * Infrastructure:
 * - Playwright page.route() network interception — no live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TickerUniverse').
 * - LIFO ordering: catch-all registered FIRST so specific mocks take precedence.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

const TICKER_LIST = [
  { ticker: 'AAPL', market: 'US', active: true,  sector: 'Technology', industry: 'Software' },
  { ticker: 'MSFT', market: 'US', active: true,  sector: 'Technology', industry: 'Software' },
  { ticker: 'BATS', market: 'UK', active: true,  sector: 'Consumer',   industry: 'Tobacco' },
  { ticker: 'TSLA', market: 'US', active: false, sector: 'Auto',       industry: 'EV' },
];

// ---------------------------------------------------------------------------
// Shared setup helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTickerUniverse(page, tickers = TICKER_LIST) {
  await page.route(`${API}/ticker-universe?active_only=false`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: tickers }),
    })
  );
}

async function mockAddTicker(page, responseRow = { ticker: 'NVDA', market: 'US', active: true, sector: 'Technology', industry: 'Chips' }) {
  await page.route(`${API}/ticker-universe`, (route) => {
    if (route.request().method() === 'POST') {
      route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: responseRow }),
      });
    } else {
      route.continue();
    }
  });
}

async function mockDeleteTicker(page) {
  await page.route(new RegExp(`${API}/ticker-universe/\\w+`), (route) => {
    if (route.request().method() === 'DELETE') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok' }) });
    } else {
      route.continue();
    }
  });
}

async function setup(page) {
  // LIFO — catch-all first, specific mocks last (last wins)
  await mockFallback(page);
  await mockDeleteTicker(page);
  await mockAddTicker(page);
  await mockTickerUniverse(page);
  await page.goto('/#/TickerUniverse');
}

// ---------------------------------------------------------------------------
// SC-TU-01 — Page renders
// ---------------------------------------------------------------------------

test.describe('SC-TU-01 — Page renders', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-01a: Ticker Universe heading is visible', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /ticker universe/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-TU-01b: Add Ticker button is visible', async ({ page }) => {
    await expect(page.getByTestId('add-ticker-btn')).toBeVisible({ timeout: 8000 });
  });

  test('SC-TU-01c: Ticker table renders with expected rows', async ({ page }) => {
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('ticker-row-AAPL')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('ticker-row-MSFT')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('ticker-row-BATS')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('ticker-row-TSLA')).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TU-02 — Add ticker
// ---------------------------------------------------------------------------

test.describe('SC-TU-02 — Add ticker form', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-02a: Clicking Add Ticker reveals the add form', async ({ page }) => {
    await page.getByTestId('add-ticker-btn').click();
    await expect(page.getByTestId('add-ticker-form')).toBeVisible({ timeout: 5000 });
  });

  test('SC-TU-02b: Submitting form sends POST /ticker-universe', async ({ page }) => {
    const requests = [];
    page.on('request', (req) => {
      if (req.url().includes('/ticker-universe') && req.method() === 'POST') {
        requests.push(req);
      }
    });

    await page.getByTestId('add-ticker-btn').click();
    await page.getByLabel('Ticker symbol').fill('NVDA');
    await page.getByTestId('add-ticker-form').getByRole('button', { name: /add ticker/i }).click();
    await page.waitForTimeout(500);

    expect(requests.length).toBeGreaterThan(0);
    const body = JSON.parse(requests[0].postData());
    expect(body.ticker).toBe('NVDA');
    expect(body.market).toBe('US');
  });

  test('SC-TU-02c: Form closes after successful add', async ({ page }) => {
    await page.getByTestId('add-ticker-btn').click();
    await page.getByLabel('Ticker symbol').fill('NVDA');
    await page.getByTestId('add-ticker-form').getByRole('button', { name: /add ticker/i }).click();
    await expect(page.getByTestId('add-ticker-form')).not.toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TU-03 — Toggle deactivates active ticker
// ---------------------------------------------------------------------------

test.describe('SC-TU-03 — Toggle ticker active/inactive', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-03a: Toggle button is visible for each row', async ({ page }) => {
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('toggle-AAPL')).toBeVisible({ timeout: 5000 });
  });

  test('SC-TU-03b: Clicking toggle on active ticker sends DELETE', async ({ page }) => {
    const requests = [];
    page.on('request', (req) => {
      if (req.url().includes('/ticker-universe/') && req.method() === 'DELETE') {
        requests.push(req.url());
      }
    });

    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('toggle-AAPL').click();
    await page.waitForTimeout(500);

    expect(requests.length).toBeGreaterThan(0);
    expect(requests[0]).toContain('/ticker-universe/AAPL');
  });
});

// ---------------------------------------------------------------------------
// SC-TU-04 — Delete ticker
// ---------------------------------------------------------------------------

test.describe('SC-TU-04 — Delete ticker', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-04a: Delete button is visible for each row', async ({ page }) => {
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('delete-AAPL')).toBeVisible({ timeout: 5000 });
  });

  test('SC-TU-04b: Clicking delete with confirmation sends DELETE request', async ({ page }) => {
    const requests = [];
    page.on('request', (req) => {
      if (req.url().includes('/ticker-universe/') && req.method() === 'DELETE') {
        requests.push(req.url());
      }
    });

    // Auto-accept confirm dialog
    page.on('dialog', (dialog) => dialog.accept());

    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('delete-MSFT').click();
    await page.waitForTimeout(500);

    expect(requests.length).toBeGreaterThan(0);
    expect(requests[0]).toContain('/ticker-universe/MSFT');
  });
});

// ---------------------------------------------------------------------------
// SC-TU-05 — Market filter
// ---------------------------------------------------------------------------

test.describe('SC-TU-05 — Market filter', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-05a: Filter bar is visible', async ({ page }) => {
    await expect(page.getByTestId('filter-bar')).toBeVisible({ timeout: 8000 });
  });

  test('SC-TU-05b: UK filter shows only UK tickers', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByLabel('Filter market UK').click();

    await expect(page.getByTestId('ticker-row-BATS')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-AAPL')).not.toBeVisible({ timeout: 3000 });
    await expect(page.getByTestId('ticker-row-MSFT')).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-TU-05c: US filter shows only US tickers', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByLabel('Filter market US').click();

    await expect(page.getByTestId('ticker-row-AAPL')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-BATS')).not.toBeVisible({ timeout: 3000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TU-06 — Active status filter
// ---------------------------------------------------------------------------

test.describe('SC-TU-06 — Active status filter', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-06a: Active filter hides inactive tickers', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByLabel('Filter status active').click();

    await expect(page.getByTestId('ticker-row-AAPL')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-TSLA')).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-TU-06b: Inactive filter shows only inactive tickers', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByLabel('Filter status inactive').click();

    await expect(page.getByTestId('ticker-row-TSLA')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-AAPL')).not.toBeVisible({ timeout: 3000 });
  });
});
