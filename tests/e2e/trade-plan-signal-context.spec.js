/**
 * Trade Plan Form — Signal Context Panel Tests
 * ST-03 (BLG-FE-34, v3.7 EPIC-01)
 *
 * Covers:
 *   SC-TP-SIG-01: Panel is visible when a watchlisted signal exists for the form ticker.
 *   SC-TP-SIG-02: Panel is absent when no watchlisted signal exists for the form ticker.
 *   SC-TP-SIG-03: Pre-population — entry_rationale field is pre-filled when signal linked.
 *   SC-TP-SIG-04: Panel absent in edit mode (hidden regardless of signal status).
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradePlan?...').
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
  rank: 2,
  momentum_percent: 14.3,
  current_price: 182.30,
  atr_value: 3.45,
  initial_stop: 164.85,
  price_vs_50d_ma: 8.2,
  regime: 'on',
  status: 'watchlisted',
};

const MARKET_STATUS = {
  spy: { price: 521.0, ma200: 480.0, is_risk_on: true },
  ftse: { price: 7800.0, ma200: 7200.0, is_risk_on: true },
  fx_rate: 1.27,
  regime_status: 'risk_on',
};

const MOCK_TRADE_PLAN = {
  id: 'tp-uuid-0001',
  ticker: 'AAPL',
  market: 'US',
  status: 'draft',
  entry_rationale: 'My existing rationale',
  confirmation_criteria: 'My existing criteria',
  early_exit_conditions: '',
  checklist_items: [],
  r_target: null,
  regime_context_at_entry: '',
  setup_thesis: '',
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function setupCommonRoutes(page) {
  await page.route(`${API}/market/status`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: MARKET_STATUS } });
  });

  await page.route(`${API}/trade-plans/by-position/**`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: [] } });
  });

  await page.route(`${API}/trade-plans/**`, async (route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({ json: { status: 'ok', data: MOCK_TRADE_PLAN } });
    } else {
      await route.continue();
    }
  });
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

test.describe('SC-TP-SIG-01 — Panel visible when watchlisted signal exists for ticker', () => {
  test('Signal Context panel renders when GET /signals returns a watchlisted signal for AAPL', async ({ page }) => {
    await setupCommonRoutes(page);

    await page.route(`${API}/signals**`, async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ json: { status: 'ok', data: [MOCK_SIGNAL] } });
      } else {
        await route.continue();
      }
    });

    await page.goto('/#/TradePlan?ticker=AAPL&market=US');

    const panel = page.getByTestId('signal-context-panel');
    await expect(panel).toBeVisible({ timeout: 8000 });
    await expect(panel).toContainText('Signal Context');
    await expect(panel).toContainText('#2');
    await expect(panel).toContainText('14.3%');
  });
});

test.describe('SC-TP-SIG-02 — Panel absent when no watchlisted signal exists', () => {
  test('Signal Context panel is not rendered when GET /signals returns empty array', async ({ page }) => {
    await setupCommonRoutes(page);

    await page.route(`${API}/signals**`, async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ json: { status: 'ok', data: [] } });
      } else {
        await route.continue();
      }
    });

    await page.goto('/#/TradePlan?ticker=AAPL&market=US');

    // Wait for page to load (market status should resolve)
    await page.waitForTimeout(2000);

    const panel = page.getByTestId('signal-context-panel');
    await expect(panel).not.toBeVisible();
  });
});

test.describe('SC-TP-SIG-03 — Pre-population when signal is linked', () => {
  test('Entry rationale and confirmation criteria fields are pre-populated from signal data', async ({ page }) => {
    await setupCommonRoutes(page);

    await page.route(`${API}/signals**`, async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ json: { status: 'ok', data: [MOCK_SIGNAL] } });
      } else {
        await route.continue();
      }
    });

    await page.goto('/#/TradePlan?ticker=AAPL&market=US');

    // Panel must be visible first (confirms signal loaded)
    await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 8000 });

    // Entry rationale should contain the rank
    const entryRationaleTextarea = page.locator('textarea').filter({ hasText: /Rank 2 momentum signal/i }).first();
    await expect(entryRationaleTextarea).toBeVisible({ timeout: 5000 });
  });
});

test.describe('SC-TP-SIG-04 — Panel absent in edit mode', () => {
  test('Signal Context panel is not shown when editing an existing trade plan', async ({ page }) => {
    await setupCommonRoutes(page);

    // Even if signals API returns data, panel should not show in edit mode
    await page.route(`${API}/signals**`, async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ json: { status: 'ok', data: [MOCK_SIGNAL] } });
      } else {
        await route.continue();
      }
    });

    await page.goto('/#/TradePlan?edit=tp-uuid-0001&ticker=AAPL&market=US');

    // Wait for edit form to load
    await page.waitForTimeout(2000);

    const panel = page.getByTestId('signal-context-panel');
    await expect(panel).not.toBeVisible();
  });
});
