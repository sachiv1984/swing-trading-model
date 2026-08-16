/**
 * Research Page — Trade Plan Status Badge Acceptance Tests — ST-14 (EPIC-03, v8.8, BLG-FE-162)
 *
 * Covers observable AC for the Research page's Trade Plan Panel (/research/:ticker):
 *   SC-RES-14  All 6 trade plan statuses render a human-readable label, none
 *              fall back to raw snake_case (draft, research_pending,
 *              research_complete, entry_conditions_set, active, closed)
 *   SC-RES-15  Badge is rendered via the shared TradePlanStatusBadge component
 *              (single source of truth, same visual pattern already live on
 *              the Trade Plans list page) — not a page-local map
 *
 * Spec refs: docs/specs/frontend/pages/research_view.md v1.3 §4.7
 * Design source: docs/design/2026-08-14__release-v8.8/research-status-badge-single-source/decision_record.md
 * Infrastructure: Playwright page.route() network interception. No live backend required.
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
const PLAN_ID = '00000000-0000-0000-0000-000000000002';

const RESEARCH_OK = {
  status: 'ok',
  data: {
    ticker: TICKER,
    market: 'US',
    signal: {
      signal_id: 'test-signal-002',
      direction: 'long',
      signal_date: '2026-05-01',
      // Deliberately "watch", not "active" — the Price/Signal region also
      // renders a status badge (SC-RES-02/03), and this suite asserts on
      // exact-text badge labels ("Active", "Closed", ...) in the separate
      // Trade Plan panel below. A signal status of "active" would collide
      // with the trade-plan-status="active" case's exact-text assertion.
      status: 'watch',
      rank: 1,
      atr: 4.2,
      entry_price: 178.50,
      stop_price: 172.00,
      r_target: 2.5,
    },
    regime: { label: 'risk_on', spy_risk_on: true, ftse_risk_on: true },
    sector: { sector: 'Technology', industry: 'Consumer Electronics' },
    screener: { in_latest_results: true, latest_run_timestamp: '2026-05-06T06:00:00Z', score: 85, atr_pct: 0.023 },
    earnings: { next_earnings_date: '2026-07-25', days_until_earnings: 80, fiscal_quarter: 'Q3 2026', data_source: 'yfinance' },
  },
};

function planWithStatus(status) {
  return {
    status: 'ok',
    data: [{ id: PLAN_ID, ticker: TICKER, status, stop_level: 175.0, risk_reward_notes: 'R/R looks good at current level with tight stop.' }],
  };
}

// STATUS_CONFIG (TradePlans.js) label map — the single canonical source this
// test asserts against, per decision record.
const STATUS_LABELS = {
  draft: 'Draft',
  research_pending: 'Research Pending',
  research_complete: 'Research Complete',
  entry_conditions_set: 'Entry Ready',
  active: 'Active',
  closed: 'Closed',
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockResearch(page) {
  await page.route(new RegExp(`${API}/research/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RESEARCH_OK) })
  );
}

async function mockHeat(page) {
  await page.route(new RegExp(`${API}/portfolio/prospective-heat`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: { valid: true, current_heat_percent: 12.0, prospective_heat_percent: 18.0, incremental_heat_percent: 6.0, prospective_risk_gbp: 650, portfolio_value_gbp: 50000, ticker: TICKER },
      }),
    })
  );
}

async function mockPlans(page, status) {
  await page.route(new RegExp(`${API}/trade-plans\\?ticker=`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(planWithStatus(status)) })
  );
}

async function gotoResearch(page) {
  await page.goto(`/#/research/${TICKER}`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: new RegExp(`${TICKER}.*Research`, 'i') })).toBeVisible({ timeout: 10000 });
}

for (const [statusValue, label] of Object.entries(STATUS_LABELS)) {
  test(`SC-RES-14: Trade plan status "${statusValue}" renders as "${label}", not raw snake_case`, async ({ page }) => {
    await mockFallback(page);
    await mockResearch(page);
    await mockHeat(page);
    await mockPlans(page, statusValue);
    await gotoResearch(page);

    await expect(page.getByText(label, { exact: true })).toBeVisible({ timeout: 8000 });
    // The raw snake_case value must never be rendered verbatim as the badge text.
    await expect(page.getByText(statusValue, { exact: true })).not.toBeVisible();
  });
}

test('SC-RES-15: Status badge uses the shared TradePlanStatusBadge visual pattern (solid pill, no border)', async ({ page }) => {
  await mockFallback(page);
  await mockResearch(page);
  await mockHeat(page);
  await mockPlans(page, 'active');
  await gotoResearch(page);

  const badge = page.getByText('Active', { exact: true });
  await expect(badge).toBeVisible({ timeout: 8000 });
  // TradePlanStatusBadge (TradePlans.js) renders a solid-fill pill
  // (bg-green-700) — the old page-local PlanStatusBadge used a
  // translucent/bordered pill (bg-emerald-500/20 + border). Asserting the
  // shared component's class signature confirms Research.js is no longer
  // rendering its own divergent map.
  await expect(badge).toHaveClass(/bg-green-700/);
});
