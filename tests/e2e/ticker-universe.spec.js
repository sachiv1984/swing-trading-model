/**
 * Ticker Universe Management Page — Playwright Tests
 * ST-09 (v3.8 EPIC-04); Search/Sector/Industry filters added ST-15 (EPIC-03, v8.8, BLG-FE-163)
 *
 * Covers:
 *   SC-TU-01: Page renders with table of tickers and "Add Ticker" button
 *   SC-TU-02: Adding a ticker via the form calls POST /ticker-universe and updates table
 *   SC-TU-03: Toggle deactivates an active ticker (DELETE /ticker-universe/{ticker})
 *   SC-TU-04: Delete button calls DELETE /ticker-universe/{ticker}
 *   SC-TU-05: Market filter (All/US/UK) shows only matching rows
 *   SC-TU-06: Active status filter shows only matching rows
 *   SC-TU-07: Search filter narrows by ticker/company substring, debounced
 *   SC-TU-08: Sector and Industry filters narrow rows; options derived from loaded list
 *   SC-TU-09: "Clear filters" control shown when any filter active; resets all 5, then hides
 *
 * Spec ref: docs/specs/frontend/pages/ticker_universe.md §10
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
  { ticker: 'AAPL',   market: 'US', active: true,  sector: 'Technology', industry: 'Software', company_name: 'Apple Inc.' },
  { ticker: 'MSFT',   market: 'US', active: true,  sector: 'Technology', industry: 'Software', company_name: 'Microsoft Corporation' },
  { ticker: 'BATS.L', market: 'UK', active: true,  sector: 'Consumer',   industry: 'Tobacco',  company_name: 'British American Tobacco' },
  { ticker: 'TSLA',   market: 'US', active: false, sector: 'Auto',       industry: 'EV',       company_name: 'Tesla, Inc.' },
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
    await expect(page.getByTestId('ticker-row-BATS.L')).toBeVisible({ timeout: 8000 });
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

    await expect(page.getByTestId('ticker-row-BATS.L')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-AAPL')).not.toBeVisible({ timeout: 3000 });
    await expect(page.getByTestId('ticker-row-MSFT')).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-TU-05c: US filter shows only US tickers', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByLabel('Filter market US').click();

    await expect(page.getByTestId('ticker-row-AAPL')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-BATS.L')).not.toBeVisible({ timeout: 3000 });
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

// ---------------------------------------------------------------------------
// SC-TU-DISP-01 — ST-05: LSE ticker displayed without .L suffix
// ---------------------------------------------------------------------------

test.describe('SC-TU-DISP-01 — LSE .L suffix stripped in display', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-DISP-01a: BATS.L row displays as BATS in the ticker cell', async ({ page }) => {
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 8000 });
    const row = page.getByTestId('ticker-row-BATS.L');
    await expect(row).toBeVisible({ timeout: 5000 });
    const tickerCell = row.locator('td').first();
    await expect(tickerCell).toHaveText('BATS');
    await expect(tickerCell).not.toHaveText('BATS.L');
  });

  test('SC-TU-DISP-01b: US tickers display unchanged', async ({ page }) => {
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 8000 });
    const row = page.getByTestId('ticker-row-AAPL');
    await expect(row).toBeVisible({ timeout: 5000 });
    const tickerCell = row.locator('td').first();
    await expect(tickerCell).toHaveText('AAPL');
  });

  test('SC-TU-DISP-01c: Toggle request for BATS.L sends full .L suffix in URL', async ({ page }) => {
    const requests = [];
    page.on('request', (req) => {
      if (req.url().includes('/ticker-universe/') && req.method() === 'DELETE') {
        requests.push(req.url());
      }
    });

    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('toggle-BATS.L').click();
    await page.waitForTimeout(500);

    expect(requests.length).toBeGreaterThan(0);
    expect(requests[0]).toContain('/ticker-universe/BATS.L');
  });
});

// ---------------------------------------------------------------------------
// SC-TU-07 — Search filter (ST-15)
// ---------------------------------------------------------------------------

test.describe('SC-TU-07 — Search filter', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-07a: Typing a ticker substring narrows to matching rows (debounced)', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('ticker-search-input').fill('AAPL');

    await expect(page.getByTestId('ticker-row-AAPL')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-MSFT')).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-TU-07b: Search matches company name, case-insensitively', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('ticker-search-input').fill('tesla');

    await expect(page.getByTestId('ticker-row-TSLA')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-AAPL')).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-TU-07c: Clearing the search input restores all rows', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('ticker-search-input').fill('AAPL');
    await expect(page.getByTestId('ticker-row-MSFT')).not.toBeVisible({ timeout: 3000 });

    await page.getByTestId('ticker-search-input').fill('');
    await expect(page.getByTestId('ticker-row-MSFT')).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TU-08 — Sector and Industry filters (ST-15)
// ---------------------------------------------------------------------------

test.describe('SC-TU-08 — Sector and Industry filters', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-08a: Sector select options are derived from the loaded ticker list', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    const options = await page.getByTestId('sector-filter').locator('option').allTextContents();
    expect(options).toEqual(expect.arrayContaining(['All Sectors', 'Technology', 'Consumer', 'Auto']));
  });

  test('SC-TU-08b: Selecting a sector narrows to matching rows', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('sector-filter').selectOption('Auto');

    await expect(page.getByTestId('ticker-row-TSLA')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-AAPL')).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-TU-08c: Selecting an industry narrows to matching rows', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('industry-filter').selectOption('Tobacco');

    await expect(page.getByTestId('ticker-row-BATS.L')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-AAPL')).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-TU-08d: Sector and Market filters AND-combine', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('sector-filter').selectOption('Technology');
    await page.getByLabel('Filter market UK').click();

    await expect(page.getByTestId('ticker-row-AAPL')).not.toBeVisible({ timeout: 3000 });
    await expect(page.getByTestId('ticker-row-BATS.L')).not.toBeVisible({ timeout: 3000 });
  });
});

// ---------------------------------------------------------------------------
// SC-TU-09 — Clear filters control (ST-15)
// ---------------------------------------------------------------------------

test.describe('SC-TU-09 — Clear filters control', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-09a: Clear filters is hidden when all filters are at default', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await expect(page.getByTestId('clear-filters-badge')).not.toBeVisible();
  });

  test('SC-TU-09b: Clear filters appears once a filter is active', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByTestId('sector-filter').selectOption('Auto');
    await expect(page.getByTestId('clear-filters-badge')).toBeVisible({ timeout: 5000 });
  });

  test('SC-TU-09c: Clicking Clear filters resets Market/Status/Search/Sector/Industry and hides itself', async ({ page }) => {
    await page.getByTestId('ticker-table').waitFor({ timeout: 8000 });
    await page.getByLabel('Filter market UK').click();
    await page.getByTestId('sector-filter').selectOption('Auto');
    await page.getByTestId('ticker-search-input').fill('AAPL');
    await expect(page.getByTestId('clear-filters-badge')).toBeVisible({ timeout: 5000 });

    await page.getByTestId('clear-filters-badge').click();

    await expect(page.getByTestId('clear-filters-badge')).not.toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-AAPL')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-row-TSLA')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('ticker-search-input')).toHaveValue('');
  });
});

// ---------------------------------------------------------------------------
// SC-TU-COMP-01 — ST-06: Company name visible in table
// ---------------------------------------------------------------------------

test.describe('SC-TU-COMP-01 — Company name column renders', () => {
  test.beforeEach(async ({ page }) => { await setup(page); });

  test('SC-TU-COMP-01a: Company name column header is visible', async ({ page }) => {
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 8000 });
    await expect(page.getByRole('columnheader', { name: /company name/i })).toBeVisible({ timeout: 5000 });
  });

  test('SC-TU-COMP-01b: Known ticker row shows company name', async ({ page }) => {
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 8000 });
    const companyCell = page.getByTestId('company-name-AAPL');
    await expect(companyCell).toBeVisible({ timeout: 5000 });
    await expect(companyCell).toHaveText('Apple Inc.');
  });

  test('SC-TU-COMP-01c: LSE ticker company name renders', async ({ page }) => {
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 8000 });
    const companyCell = page.getByTestId('company-name-BATS.L');
    await expect(companyCell).toBeVisible({ timeout: 5000 });
    await expect(companyCell).toHaveText('British American Tobacco');
  });
});
