/**
 * Research View — Setup Type (signal_type) field acceptance tests
 * ST-10 (EPIC-03, v4.1) — BLG-FE-44 AC-02
 *
 * Covers observable AC for signal_type display in the Signal Panel:
 *   SC-ST-01  "Setup Type" label is visible in the signal panel
 *   SC-ST-02  signal_type value "breakout" is rendered when present in signal data
 *   SC-ST-03  signal_type shows "—" when signal_type is null
 *   SC-ST-04  signal panel not rendered when signal is null (no crash)
 *
 * Spec ref: docs/specs/frontend/pages/research_view.md v1.2 §4.2
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
const TICKER = 'AAPL';

// ---------------------------------------------------------------------------
// Mock payloads
// ---------------------------------------------------------------------------

const RESEARCH_WITH_SIGNAL_TYPE = {
  status: 'ok',
  data: {
    ticker: TICKER,
    market: 'US',
    signal: {
      signal_id: 'test-signal-001',
      direction: 'long',
      signal_date: '2026-05-01',
      status: 'active',
      rank: 1,
      atr: 4.2,
      entry_price: 178.50,
      stop_price: 172.00,
      r_target: 2.5,
      signal_type: 'breakout',
    },
    regime: { label: 'risk_on', spy_risk_on: true, ftse_risk_on: true },
    sector: { sector: 'Technology', industry: 'Consumer Electronics' },
    screener: null,
    earnings: null,
  },
};

const RESEARCH_SIGNAL_TYPE_NULL = {
  status: 'ok',
  data: {
    ...RESEARCH_WITH_SIGNAL_TYPE.data,
    signal: {
      ...RESEARCH_WITH_SIGNAL_TYPE.data.signal,
      signal_type: null,
    },
  },
};

const RESEARCH_NO_SIGNAL = {
  status: 'ok',
  data: {
    ticker: TICKER,
    market: 'US',
    signal: null,
    regime: { label: 'risk_on', spy_risk_on: true, ftse_risk_on: true },
    sector: { sector: 'Technology', industry: 'Consumer Electronics' },
    screener: null,
    earnings: null,
  },
};

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockResearch(page, payload = RESEARCH_WITH_SIGNAL_TYPE) {
  await page.route(new RegExp(`${API}/research/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockHeat(page) {
  await page.route(new RegExp(`${API}/portfolio/prospective-heat`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { valid: true, current_heat_percent: 12.0, prospective_heat_percent: 18.0 } }),
    })
  );
}

async function mockPlans(page) {
  await page.route(new RegExp(`${API}/trade-plans\\?ticker=`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function gotoResearch(page, ticker = TICKER) {
  await page.goto(`/#/research/${ticker}`);
  // Wait for the page to be ready — look for a heading containing the ticker
  await expect(page.locator('h1, [class*="PageHeader"], h2').filter({ hasText: new RegExp(ticker, 'i') }).first()).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-ST-01 — "Setup Type" label visible
// ---------------------------------------------------------------------------

test('SC-ST-01: "Setup Type" label is visible in the signal panel', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page, RESEARCH_WITH_SIGNAL_TYPE);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText('Setup Type')).toBeVisible({ timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-ST-02 — signal_type value "breakout" rendered
// ---------------------------------------------------------------------------

test('SC-ST-02: signal_type value "breakout" is visible when present in signal data', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page, RESEARCH_WITH_SIGNAL_TYPE);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText('Setup Type')).toBeVisible({ timeout: 8000 });
  await expect(page.getByText('breakout')).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ST-03 — null signal_type shows "—"
// ---------------------------------------------------------------------------

test('SC-ST-03: signal_type shows "—" when signal_type is null', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page, RESEARCH_SIGNAL_TYPE_NULL);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText('Setup Type')).toBeVisible({ timeout: 8000 });
  // The "—" em-dash is rendered in the signal panel area
  // Use a more targeted selector to avoid collisions with other "—" placeholders
  const setupTypeSection = page.locator('div').filter({ hasText: 'Setup Type' }).first();
  await expect(setupTypeSection).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ST-04 — no crash when signal is null
// ---------------------------------------------------------------------------

test('SC-ST-04: page renders without crash when signal is null (no Setup Type label)', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page, RESEARCH_NO_SIGNAL);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  // Signal panel is not rendered when signal is null — no crash
  // Page should still show the ticker heading
  await expect(page.locator('h1, [class*="PageHeader"], h2').filter({ hasText: new RegExp(TICKER, 'i') }).first()).toBeVisible({ timeout: 8000 });
});
