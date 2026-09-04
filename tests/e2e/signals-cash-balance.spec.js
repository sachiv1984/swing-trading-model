/**
 * Signals Page — Cash Balance Integration Tests
 * ST-16 (v2.6 EPIC-01 test gap closure)
 *
 * Covers the frontend behaviour introduced by EPIC-01 (ST-03):
 *   SC-SIG-CB-01: Cash balance rendered from /cash/summary current_cash field
 *   SC-SIG-CB-02: Cash balance falls back to £0.00 when /cash/summary returns null/error
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Signals').
 * - api.cash.getSummary() → GET /cash/summary
 *   availableCashBalance = cashSummary?.current_cash ?? 0
 * - availableCash is passed to PositionSizerPanel which renders it as a
 *   formatted currency string.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

/** Cash summary with a known current_cash value */
const CASH_SUMMARY_FUNDED = {
  current_cash: 8250.00,
  total_deposited: 10000.00,
  total_withdrawn: 0.00,
  realised_pnl: 750.00,
  unrealised_pnl: 0.00,
};

/** Signals list — non-empty so the page renders position sizer panel */
const SIGNALS_LIST = [
  {
    id: 'sig-1',
    ticker: 'LGEN',
    market: 'UK',
    status: 'active',
    signal_date: '2026-04-10',
    direction: 'long',
    entry_price: 220.00,
    stop_price: 200.00,
    target_price: 260.00,
    risk_reward: 2.0,
    atr: 8.5,
    rationale: 'Breakout above resistance',
  },
];

// ---------------------------------------------------------------------------
// Shared setup helpers
// ---------------------------------------------------------------------------

async function mockSignals(page, signals = SIGNALS_LIST) {
  await page.route(`${API}/signals`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: signals }),
      });
    } else {
      route.continue();
    }
  });
}

async function mockCashSummary(page, payload = CASH_SUMMARY_FUNDED) {
  await page.route(`${API}/cash/summary`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    })
  );
}

async function mockCashSummaryError(page) {
  await page.route(`${API}/cash/summary`, (route) =>
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ detail: 'Internal Server Error' }),
    })
  );
}

/** Catch-all: prevent unmocked endpoints from hanging tests */
async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

// ---------------------------------------------------------------------------
// SC-SIG-CB-01 — Cash balance rendered from /cash/summary
// ---------------------------------------------------------------------------

test.describe('SC-SIG-CB-01 — Cash balance from /cash/summary', () => {
  test.beforeEach(async ({ page }) => {
    // Catch-all first — Playwright routes are LIFO, so registering catch-all first
    // ensures the specific mocks below take precedence.
    await mockFallback(page);
    await mockCashSummary(page, CASH_SUMMARY_FUNDED);
    await mockSignals(page);
    await page.goto('/#/Signals');
    // Wait for all API calls to settle before asserting
  });

  test('SC-SIG-CB-01a: GET /cash/summary is called on Signals page load', async ({ page }) => {
    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await mockFallback(page);
    await mockCashSummary(page, CASH_SUMMARY_FUNDED);
    await mockSignals(page);

    // Attach request listener before navigation so no requests are missed.
    const cashRequests = [];
    page.on('request', (req) => {
      if (req.url().includes('/cash/summary')) cashRequests.push(req.url());
    });

    // Navigate to about:blank to fully destroy the React app and React Query cache
    // (beforeEach already navigated to /#/Signals and warmed the cache; changing the
    // hash alone keeps the SPA mounted so React Query serves from cache and skips the fetch).
    await page.goto('about:blank');

    // DEV-EPIC02-ST08-01 (BLG-TECH-18/ST-08, v9.1): page.goto() only waits for
    // the 'load' event, not for React to mount and useQuery's queryFn to
    // actually fire — a quarterly dependency bump shifted bundle init/parse
    // timing enough that goto() now reliably resolves before the app's first
    // /cash/summary fetch, where it previously (coincidentally) didn't. Wait
    // for the actual request alongside the navigation (Playwright's standard
    // trigger-and-wait-concurrently pattern) instead of asserting immediately
    // after goto() resolves — confirmed via a local reproduction that this is
    // a pure test-synchronization gap, not an app behaviour change: the fetch
    // reliably fires, just not always before this line used to run.
    await Promise.all([
      page.waitForRequest((req) => req.url().includes('/cash/summary'), { timeout: 10000 }),
      page.goto('/#/Signals'),
    ]);

    expect(cashRequests.length).toBeGreaterThan(0);
    expect(cashRequests[0]).toContain('/cash/summary');
  });

  test('SC-SIG-CB-01b: Available cash rendered from current_cash field', async ({ page }) => {
    // availableCashBalance = cashSummary.current_cash = 8250.00
    // PositionSizerPanel renders this as a formatted currency string
    // Exact format depends on the component — check for the numeric value
    await expect(page.getByText(/8[,.]?250/)).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SIG-CB-02 — Fallback to £0 when /cash/summary returns null or error
// ---------------------------------------------------------------------------

test.describe('SC-SIG-CB-02 — Cash balance fallback to 0', () => {
  test('SC-SIG-CB-02a: Cash shows 0 when /cash/summary returns server error', async ({ page }) => {
    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await mockFallback(page);
    await mockCashSummaryError(page);
    await mockSignals(page);
    await page.goto('/#/Signals');
    await page.waitForTimeout(500);

    // availableCashBalance = cashSummary?.current_cash ?? 0 = 0
    // Should render 0 / £0 / £0.00 — not a hard crash
    // Verify the page rendered without throwing (no error boundary shown)
    await expect(page.locator('body')).not.toContainText('Something went wrong');
    // Verify 0 cash is rendered. Use exact:true + first() to avoid strict-mode violation:
    // the regex also matches signal price data ("£0.00 vs MA200") and other zero values.
    // The cash balance renders as a bold "£0" element (distinct from small signal data text).
    await expect(page.getByText('£0', { exact: true }).first()).toBeVisible({ timeout: 8000 });
  });

  test('SC-SIG-CB-02b: Cash shows 0 when /cash/summary returns null current_cash', async ({ page }) => {
    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await mockFallback(page);
    await page.route(`${API}/cash/summary`, (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ current_cash: null, total_deposited: 0 }),
      })
    );
    await mockSignals(page);
    await page.goto('/#/Signals');
    await page.waitForTimeout(500);

    // cashSummary?.current_cash ?? 0 → 0 when current_cash is null
    await expect(page.locator('body')).not.toContainText('Something went wrong');
    // Use exact:true + first() — same strict-mode fix as SC-SIG-CB-02a.
    await expect(page.getByText('£0', { exact: true }).first()).toBeVisible({ timeout: 8000 });
  });
});
