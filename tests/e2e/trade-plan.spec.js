/**
 * Trade Plan Acceptance Tests — ST-03 (EPIC-01, v3.1)
 *
 * Covers observable AC for the Trade Plan creation/edit form:
 *   SC-TP-01  Form renders with all required fields
 *   SC-TP-02  Ticker/market pre-populated from query params
 *   SC-TP-03  Regime context auto-populated from GET /market/status
 *   SC-TP-04  Save button disabled when ticker is empty
 *   SC-TP-05  Existing plan banner shown when position already has a plan
 *   SC-TP-06  Success banner shown after saving
 *   SC-TP-07  No regression — Positions and Watchlist pages still render
 *
 * Spec refs: GitHub Issue #311 (ST-03 AC)
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const PLAN_ID = '00000000-0000-0000-0000-000000000001';
const POSITION_ID = '00000000-0000-0000-0000-000000000002';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

const MARKET_STATUS_OK = {
  status: 'ok',
  data: { regime_status: 'risk_on' },
};

const TRADE_PLAN_SAVED = {
  status: 'ok',
  data: {
    id: PLAN_ID,
    ticker: 'AAPL',
    market: 'US',
    status: 'draft',
    setup_thesis: 'Test thesis',
    entry_rationale: 'Test rationale',
    regime_context_at_entry: 'risk_on',
    r_target: 2.5,
    early_exit_conditions: null,
    confirmation_criteria: null,
    checklist_completed: false,
    checklist_items: [],
  },
};

const EXISTING_PLAN_FOR_POSITION = {
  status: 'ok',
  data: [
    {
      id: PLAN_ID,
      ticker: 'AAPL',
      market: 'US',
      position_id: POSITION_ID,
      status: 'active',
    },
  ],
};

const NO_PLAN_FOR_POSITION = { status: 'ok', data: null };

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMarketStatus(page, payload = MARKET_STATUS_OK) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockTradePlansPost(page, payload = TRADE_PLAN_SAVED) {
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(payload) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
  });
}

async function mockByPosition(page, payload) {
  await page.route(new RegExp(`${API}/trade-plans/by-position/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

/** Navigate to the TradePlan page with optional query params. */
async function gotoTradePlan(page, params = {}) {
  const qs = new URLSearchParams(params).toString();
  const hash = qs ? `/#/TradePlan?${qs}` : '/#/TradePlan';
  await page.goto(hash);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-TP-01 — Form renders with all required fields
// ---------------------------------------------------------------------------

test('SC-TP-01: Trade Plan form renders all required fields', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  // Text areas for reasoning fields
  await expect(page.getByPlaceholder(/describe the setup/i)).toBeVisible({ timeout: 5000 });
  await expect(page.getByPlaceholder(/why enter now/i)).toBeVisible();
  await expect(page.getByPlaceholder(/what must be true/i)).toBeVisible();
  await expect(page.getByPlaceholder(/under what conditions/i)).toBeVisible();

  // Numeric and select fields
  await expect(page.getByPlaceholder(/e\.g\. 2\.5/i)).toBeVisible();
  await expect(page.locator('select').filter({ has: page.locator('option[value="US"]') })).toBeVisible();

  // Checklist checkbox
  await expect(page.locator('#checklist_completed')).toBeVisible();

  // Save button present
  await expect(page.getByRole('button', { name: /save plan/i })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-TP-02 — Ticker and market pre-populated from query params
// ---------------------------------------------------------------------------

test('SC-TP-02: Ticker and market pre-populated from query params', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await gotoTradePlan(page, { ticker: 'TSLA', market: 'US' });

  await expect(page.locator('input[placeholder*="AAPL"]')).toHaveValue('TSLA', { timeout: 5000 });

  // Market select shows the passed value
  const marketSelect = page.locator('select').filter({ has: page.locator('option[value="US"]') }).first();
  await expect(marketSelect).toHaveValue('US');
});

// ---------------------------------------------------------------------------
// SC-TP-03 — Regime context auto-populated from GET /market/status
// ---------------------------------------------------------------------------

test('SC-TP-03: Regime context input auto-populated from market status API', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page, { status: 'ok', data: { regime_status: 'risk_off' } });
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  // The regime context input shows the value from the API.
  // Placeholder is dynamic (regimeFromHealth || "e.g. risk_on"), so when risk_off
  // loads, placeholder becomes "risk_off". Locate by the Field label instead.
  const regimeInput = page.locator('label').filter({ hasText: /regime context/i }).locator('xpath=../input');
  await expect(regimeInput).toHaveValue('risk_off', { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-TP-04 — Save button disabled when ticker is empty
// ---------------------------------------------------------------------------

test('SC-TP-04: Save Plan button is disabled when ticker field is empty', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await gotoTradePlan(page);

  // No ticker passed — button should be disabled
  const saveBtn = page.getByRole('button', { name: /save plan/i });
  await expect(saveBtn).toBeDisabled({ timeout: 5000 });

  // Entering a ticker enables the button
  await page.locator('input[placeholder*="AAPL"]').fill('MSFT');
  await expect(saveBtn).toBeEnabled({ timeout: 3000 });
});

// ---------------------------------------------------------------------------
// SC-TP-05 — Existing plan banner when position already has a plan
// ---------------------------------------------------------------------------

test('SC-TP-05: Amber banner shown when position already has an existing trade plan', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockByPosition(page, EXISTING_PLAN_FOR_POSITION);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US', position_id: POSITION_ID });

  // Amber banner with "edit it instead" link
  await expect(page.locator('[class*="amber"]').filter({ hasText: /existing trade plan/i })).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('button', { name: /edit it instead/i })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-TP-06 — Success banner shown after saving
// ---------------------------------------------------------------------------

test('SC-TP-06: Success banner shown after trade plan is saved', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockByPosition(page, NO_PLAN_FOR_POSITION);
  await mockTradePlansPost(page);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  await page.getByRole('button', { name: /save plan/i }).click();

  await expect(page.locator('[class*="emerald"]').filter({ hasText: /saved successfully/i })).toBeVisible({ timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-TP-07 — No regression to Positions and Watchlist pages
// ---------------------------------------------------------------------------

test('SC-TP-07a: Positions page still renders after Trade Plan routes are registered', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );

  await page.goto('/#/Positions');
  await page.waitForLoadState('networkidle');

  // No crash — page heading is always present (h1 alone avoids strict-mode
  // violation when both the heading and empty-state text are simultaneously visible)
  await expect(page.locator('h1').filter({ hasText: /positions/i })).toBeVisible({ timeout: 8000 });
});

test('SC-TP-07b: Watchlist page still renders after Trade Plan routes are registered', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/watchlist`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );

  await page.goto('/#/Watchlist');
  await page.waitForLoadState('networkidle');

  await expect(page.locator('h1').filter({ hasText: /watchlist/i })).toBeVisible({ timeout: 8000 });
});
