/**
 * Signals Page — Add to Watchlist CTA Tests
 * ST-02 (BLG-FE-33, v3.7 EPIC-01)
 *
 * Covers:
 *   SC-SIG-WL-01: Add to Watchlist happy path — new signal card shows CTA,
 *                 clicking it calls POST /watchlist + PATCH /signals/{id},
 *                 card transitions to watchlisted state with "View in Watchlist" link.
 *   SC-SIG-WL-02: Duplicate add — 409 from POST /watchlist shows "Already on your watchlist"
 *                 toast; signal still transitions to watchlisted state.
 *   SC-SIG-WL-03: No "Add Position" CTA present on new signal cards (non-regression).
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Signals').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

const MOCK_SIGNAL = {
  id: 'sig-uuid-0001',
  ticker: 'AAPL',
  market: 'US',
  signal_date: '2026-05-18',
  rank: 1,
  momentum_percent: 18.5,
  current_price: 182.30,
  price_gbp: 143.00,
  atr_value: 3.45,
  volatility: 0.012,
  initial_stop: 164.85,
  suggested_shares: 10,
  allocation_gbp: 1430.00,
  total_cost: 1430.00,
  status: 'new',
};

const MOCK_WATCHLISTED_SIGNAL = { ...MOCK_SIGNAL, status: 'watchlisted' };

const MARKET_STATUS = {
  spy: { price: 521.0, ma200: 480.0, is_risk_on: true },
  ftse: { price: 7800.0, ma200: 7200.0, is_risk_on: true },
  fx_rate: 1.27,
};

const CASH_SUMMARY = { current_cash: 10000.0 };

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function setupBaseRoutes(page, signalStatus = 'new') {
  const signal = signalStatus === 'watchlisted' ? MOCK_WATCHLISTED_SIGNAL : MOCK_SIGNAL;

  await page.route(`${API}/signals**`, async (route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({ json: { status: 'ok', data: [signal] } });
    } else {
      await route.continue();
    }
  });

  await page.route(`${API}/signals/${MOCK_SIGNAL.id}`, async (route) => {
    if (route.request().method() === 'PATCH') {
      await route.fulfill({ json: { status: 'ok', data: { ...signal, status: 'watchlisted' } } });
    } else {
      await route.continue();
    }
  });

  await page.route(`${API}/market/status`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: MARKET_STATUS } });
  });

  await page.route(`${API}/cash/summary`, async (route) => {
    await route.fulfill({ json: { status: 'ok', ...CASH_SUMMARY } });
  });

  await page.route(`${API}/positions**`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: [] } });
  });
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

test.describe('SC-SIG-WL-01 — Add to Watchlist happy path', () => {
  test('New signal card shows "Add to Watchlist" button and transitions to watchlisted state', async ({ page }) => {
    await setupBaseRoutes(page, 'new');

    // Mock POST /watchlist → 201 success
    await page.route(`${API}/watchlist`, async (route) => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 201,
          json: { status: 'ok', data: { id: 'wl-uuid-0001', ticker: 'AAPL', market: 'US' } },
        });
      } else {
        await route.continue();
      }
    });

    // After PATCH, return watchlisted signal on next GET /signals
    let patchCalled = false;
    await page.route(`${API}/signals/${MOCK_SIGNAL.id}`, async (route) => {
      if (route.request().method() === 'PATCH') {
        patchCalled = true;
        await route.fulfill({ json: { status: 'ok', data: MOCK_WATCHLISTED_SIGNAL } });
      } else {
        await route.continue();
      }
    });

    // After PATCH, refetch returns watchlisted signal
    let fetchCount = 0;
    await page.route(`${API}/signals**`, async (route) => {
      if (route.request().method() === 'GET') {
        fetchCount++;
        const signal = fetchCount > 1 ? MOCK_WATCHLISTED_SIGNAL : MOCK_SIGNAL;
        await route.fulfill({ json: { status: 'ok', data: [signal] } });
      } else {
        await route.continue();
      }
    });

    await page.goto('/#/Signals');

    // Verify "Add to Watchlist" button is present
    const addBtn = page.getByTestId('add-to-watchlist-btn');
    await expect(addBtn).toBeVisible({ timeout: 8000 });
    await expect(addBtn).toContainText('Add to Watchlist');

    // No "Add Position" button present (non-regression)
    await expect(page.getByRole('button', { name: /add position/i })).not.toBeVisible();

    // Click Add to Watchlist
    await addBtn.click();

    // After click, watchlisted state appears
    const viewLink = page.getByTestId('view-in-watchlist-link');
    await expect(viewLink).toBeVisible({ timeout: 5000 });
    await expect(viewLink).toContainText('View in Watchlist');
  });
});

test.describe('SC-SIG-WL-02 — Duplicate add handling', () => {
  test('409 from POST /watchlist shows toast and signal still transitions to watchlisted', async ({ page }) => {
    await setupBaseRoutes(page, 'new');

    // POST /watchlist → 409 duplicate
    await page.route(`${API}/watchlist`, async (route) => {
      if (route.request().method() === 'POST') {
        await route.fulfill({ status: 409, json: { detail: 'ticker already on watchlist' } });
      } else {
        await route.continue();
      }
    });

    // After PATCH, return watchlisted signal on next GET
    let fetchCount = 0;
    await page.route(`${API}/signals**`, async (route) => {
      if (route.request().method() === 'GET') {
        fetchCount++;
        const signal = fetchCount > 1 ? MOCK_WATCHLISTED_SIGNAL : MOCK_SIGNAL;
        await route.fulfill({ json: { status: 'ok', data: [signal] } });
      } else {
        await route.continue();
      }
    });

    await page.goto('/#/Signals');

    const addBtn = page.getByTestId('add-to-watchlist-btn');
    await expect(addBtn).toBeVisible({ timeout: 8000 });
    await addBtn.click();

    // Toast: "Already on your watchlist"
    await expect(page.getByText(/already on your watchlist/i)).toBeVisible({ timeout: 5000 });

    // Signal still transitions to watchlisted
    const viewLink = page.getByTestId('view-in-watchlist-link');
    await expect(viewLink).toBeVisible({ timeout: 5000 });
  });
});

test.describe('SC-SIG-WL-03 — No Add Position CTA on signal cards', () => {
  test('"Add Position" button is absent from new signal cards', async ({ page }) => {
    await setupBaseRoutes(page, 'new');
    await page.goto('/#/Signals');

    // Wait for signal card to render
    await expect(page.getByTestId('add-to-watchlist-btn')).toBeVisible({ timeout: 8000 });

    // "Add Position" must not be present
    const addPositionBtn = page.getByRole('button', { name: /add position/i });
    await expect(addPositionBtn).not.toBeVisible();
  });
});
