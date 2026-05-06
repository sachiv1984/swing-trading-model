/**
 * Pre-Trade Research View Acceptance Tests — ST-01/02/03/04 (EPIC-01, v3.2)
 *
 * Covers observable AC for the Research page at /research/:ticker:
 *   SC-RES-01  Page header shows "{TICKER} — Research" title
 *   SC-RES-02  Price and Signal region renders: price, ATR, signal badge
 *   SC-RES-03  Signal badge reflects API status (Active/Watch/No Signal)
 *   SC-RES-04  Price change indicator shows direction and percentage
 *   SC-RES-05  Prospective heat region renders current and prospective heat
 *   SC-RES-06  Prospective heat shows N/A when endpoint errors (partial error)
 *   SC-RES-07  Trade plan panel shows plan details when plan exists
 *   SC-RES-08  Trade plan panel shows "Create Trade Plan" CTA when no plan
 *   SC-RES-09  Recent news headlines rendered (up to 5)
 *   SC-RES-10  News empty state shown when no headlines
 *   SC-RES-11  Full-page error + Retry shown when research endpoint fails
 *   SC-RES-12  "Research" link present in Screener row actions
 *   SC-RES-13  "Research" link present in Watchlist actions column
 *
 * Spec refs: docs/specs/frontend/pages/pre_trade_research.md v0.1
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
const PLAN_ID = '00000000-0000-0000-0000-000000000001';

// ---------------------------------------------------------------------------
// Mock payloads
// ---------------------------------------------------------------------------

const RESEARCH_OK = {
  status: 'ok',
  data: {
    ticker: TICKER,
    name: 'Apple Inc.',
    sector: 'Technology',
    market_cap: 3200000000000,
    price: 182.5,
    price_change_pct: 0.015,
    signal_status: 'active',
    atr: 4.2,
    updated_at: new Date(Date.now() - 120000).toISOString(),
    news_headlines: [
      { headline: 'Apple hits new all-time high', source: 'Reuters', published_at: new Date(Date.now() - 3600000).toISOString() },
      { headline: 'iPhone demand remains strong', source: 'Bloomberg', published_at: new Date(Date.now() - 7200000).toISOString() },
    ],
  },
};

const RESEARCH_NO_NEWS = {
  status: 'ok',
  data: { ...RESEARCH_OK.data, news_headlines: [] },
};

const RESEARCH_WATCH = {
  status: 'ok',
  data: { ...RESEARCH_OK.data, signal_status: 'watch', price_change_pct: -0.008 },
};

const HEAT_OK = {
  status: 'ok',
  data: { current_heat: 0.12, prospective_heat: 0.18 },
};

const PLANS_WITH_ACTIVE = {
  status: 'ok',
  data: [{ id: PLAN_ID, ticker: TICKER, status: 'active', stop_level: 175.0, risk_reward_notes: 'R/R looks good at current level with tight stop.' }],
};

const PLANS_EMPTY = { status: 'ok', data: [] };

const SCREENER_RESULTS = {
  data: {
    results: [
      { ticker: TICKER, market: 'US', price: 182.5, currency: 'USD', atr: 4.2, atr_pct: 0.023, signal_score: 0.85, regime_status: 'risk_on', sector: 'Technology', proximity_to_entry_zone: 0.03, news_headline_count: 2 },
    ],
    run_timestamp: new Date().toISOString(),
    run_id: 'run-001',
  },
};

const WATCHLIST_ENTRIES = {
  status: 'ok',
  data: [
    { id: 'w-001', ticker: TICKER, market: 'US', signal_status: 'active', target_entry_price: 180.0, initial_stop_price: 170.0, current_stop_price: 172.0 },
  ],
};

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockResearch(page, payload = RESEARCH_OK) {
  await page.route(new RegExp(`${API}/research/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockHeat(page, payload = HEAT_OK, status = 200) {
  await page.route(new RegExp(`${API}/portfolio/prospective-heat`), (route) =>
    route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockPlans(page, payload = PLANS_EMPTY) {
  await page.route(new RegExp(`${API}/trade-plans\\?ticker=`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function gotoResearch(page, ticker = TICKER) {
  await page.goto(`/#/research/${ticker}`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: new RegExp(`${ticker}.*Research`, 'i') })).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-RES-01 — Page header
// ---------------------------------------------------------------------------

test('SC-RES-01: Research page header shows ticker and Research title', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /AAPL.*Research/i })).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('button', { name: /back/i })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-RES-02 — Price and Signal region renders
// ---------------------------------------------------------------------------

test('SC-RES-02: Price and Signal region renders price, ATR, and signal badge', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText(/\$182\.50/)).toBeVisible({ timeout: 8000 });
  await expect(page.getByText(/\$4\.20/)).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Active')).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-RES-03 — Signal badge reflects status
// ---------------------------------------------------------------------------

test('SC-RES-03: Signal badge shows Watch status from API', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page, RESEARCH_WATCH);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText('Watch')).toBeVisible({ timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-RES-04 — Price change indicator
// ---------------------------------------------------------------------------

test('SC-RES-04: Price change shows positive percentage', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText(/\+1\.5%/)).toBeVisible({ timeout: 8000 });
});

test('SC-RES-04b: Price change shows negative percentage', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page, RESEARCH_WATCH);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText(/-0\.8%/)).toBeVisible({ timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-RES-05 — Prospective heat region
// ---------------------------------------------------------------------------

test('SC-RES-05: Prospective heat region shows current and prospective heat', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText(/prospective heat at entry/i)).toBeVisible({ timeout: 5000 });
  await expect(page.getByText(/12\.0%/)).toBeVisible({ timeout: 8000 });
  await expect(page.getByText(/18\.0%/)).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-RES-06 — Partial error: heat endpoint fails
// ---------------------------------------------------------------------------

test('SC-RES-06: Heat region shows N/A when endpoint errors; rest of page renders', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page, {}, 500);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText(/n\/a/i).first()).toBeVisible({ timeout: 15000 });
  await expect(page.getByText(/\$182\.50/)).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-RES-07 — Trade plan panel with existing plan
// ---------------------------------------------------------------------------

test('SC-RES-07: Trade plan panel shows plan details when plan exists', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page);
  await mockPlans(page, PLANS_WITH_ACTIVE);
  await gotoResearch(page);

  await expect(page.getByText(/\$175\.00/)).toBeVisible({ timeout: 8000 });
  await expect(page.getByText(/view full plan/i)).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-RES-08 — Trade plan panel: no plan
// ---------------------------------------------------------------------------

test('SC-RES-08: Trade plan panel shows Create Trade Plan CTA when no plan exists', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page);
  await mockPlans(page, PLANS_EMPTY);
  await gotoResearch(page);

  await expect(page.getByText(/no trade plan for AAPL/i)).toBeVisible({ timeout: 8000 });
  await expect(page.getByRole('button', { name: /create trade plan/i })).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-RES-09 — Recent news headlines
// ---------------------------------------------------------------------------

test('SC-RES-09: Recent news section renders up to 5 headlines', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText('Apple hits new all-time high')).toBeVisible({ timeout: 8000 });
  await expect(page.getByText('iPhone demand remains strong')).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-RES-10 — News empty state
// ---------------------------------------------------------------------------

test('SC-RES-10: News section shows empty state when no headlines available', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page, RESEARCH_NO_NEWS);
  await mockHeat(page);
  await mockPlans(page);
  await gotoResearch(page);

  await expect(page.getByText(/no recent news available/i)).toBeVisible({ timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-RES-11 — Full-page error on research endpoint failure
// ---------------------------------------------------------------------------

test('SC-RES-11: Full-page error with Retry button when research endpoint fails', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/research/`), (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ error: 'Internal server error' }) })
  );
  await mockHeat(page);
  await mockPlans(page);

  await page.goto(`/#/research/${TICKER}`);
  await expect(page.getByText(/unable to load research data/i)).toBeVisible({ timeout: 10000 });
  await expect(page.getByRole('button', { name: /retry/i })).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-RES-12 — Research link in Screener
// ---------------------------------------------------------------------------

test('SC-RES-12: Screener row actions include Research link', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/screener/results*`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SCREENER_RESULTS) })
  );
  await page.goto('/#/Screener');
  await expect(page.getByRole('button', { name: /research/i }).first()).toBeVisible({ timeout: 10000 });
});

// ---------------------------------------------------------------------------
// SC-RES-13 — Research link in Watchlist
// ---------------------------------------------------------------------------

test('SC-RES-13: Watchlist row actions include Research button', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/watchlist`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(WATCHLIST_ENTRIES) })
  );
  await page.goto('/#/Watchlist');
  await expect(page.getByRole('button', { name: /research/i }).first()).toBeVisible({ timeout: 10000 });
});
