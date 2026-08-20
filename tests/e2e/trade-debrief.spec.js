/**
 * Automated AI Post-Trade Debrief — Playwright E2E Tests
 * ST-06 (EPIC-02, v8.9) — BLG-FEAT-90
 * §13 review (CONDITIONAL): docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md
 *
 * Covers:
 *   SC-DBF-01: No debrief yet — empty state + "Generate Debrief" button shown
 *   SC-DBF-02: Clicking Generate calls POST and renders the returned debrief
 *   SC-DBF-03: Existing debrief (GET 200) renders summary + focus area directly
 *   SC-DBF-04: focus_area_text null (fallback) shows the compliance-fallback message, no focus-area block
 *   SC-DBF-05: Regression — Plan vs Reality section still renders alongside the new Debrief section
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradeHistory').
 * - Trades list: GET /trades
 * - Debrief fetch: GET /trades/{id}/debrief (lazy, triggered by row expand)
 * - Debrief generate: POST /trades/{id}/debrief
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const TRADE_ID = 'debrief-trade-uuid-0001';

const TRADE = {
  id: TRADE_ID,
  ticker: 'AAPL',
  market: 'US',
  entry_date: '2026-04-01',
  exit_date: '2026-04-20',
  entry_price: 170.00,
  exit_price: 184.00,
  shares: 100,
  pnl: 1400.00,
  pnl_pct: 8.24,
  fee_drag_pct: null,
  slippage_pct: null,
  exit_reason: 'Target Reached',
  tags: [],
  entry_note: null,
  exit_note: null,
};

const TRADES_RESPONSE = {
  status: 'ok',
  total_trades: 1,
  win_rate: 100,
  total_pnl: 1400.00,
  avg_slippage_pct: null,
  avg_fee_drag_pct: null,
  trades: [TRADE],
};

const ANALYTICS_STUB = { status: 'ok', data: { trades_for_charts: [] } };

const DEBRIEF_OK = {
  status: 'ok',
  data: {
    available: true,
    summary_text: 'Entered at 170.0, exited at 184.0. P&L: +1400.00 (+8.24%). Exit reason: Target Reached.',
    focus_area_text: 'Your exit was 3 days earlier than the median holding period across your last 5 closed trades in this setup type.',
    generation_status: 'ok',
    model_version: 'claude-haiku-4-5',
    prompt_version: 'v1.0',
    generated_at: '2026-08-20T09:00:00Z',
  },
};

const DEBRIEF_FALLBACK = {
  status: 'ok',
  data: {
    available: true,
    summary_text: 'Entered at 170.0, exited at 184.0. P&L: +1400.00 (+8.24%). Exit reason: Target Reached.',
    focus_area_text: null,
    generation_status: 'fallback_no_focus_area',
    model_version: 'claude-haiku-4-5',
    prompt_version: 'v1.0',
    generated_at: '2026-08-20T09:00:00Z',
  },
};

async function mockFallback(page) {
  await page.route(`${API}/**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTrades(page) {
  await page.route(/\/trades$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TRADES_RESPONSE) })
  );
}

async function mockAnalytics(page) {
  await page.route(/\/analytics\/metrics/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ANALYTICS_STUB) })
  );
}

async function mockPlanVsRealityNotFound(page) {
  await page.route(new RegExp(`/trades/${TRADE_ID}/plan-vs-reality`), (route) =>
    route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'No trade plan found for this trade' }) })
  );
}

async function gotoAndExpand(page) {
  await page.goto('/#/TradeHistory');
  await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });
  await page.getByText('AAPL').first().click();
}

// ─── SC-DBF-01/02 — Empty state, Generate action ──────────────────────────

test.describe('SC-DBF-01/02 — No debrief yet, on-demand generation', () => {
  test.beforeEach(async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await mockTrades(page);
    await mockPlanVsRealityNotFound(page);
    await page.route(new RegExp(`/trades/${TRADE_ID}/debrief`), (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'No debrief generated yet for this trade' }) });
      }
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(DEBRIEF_OK) });
    });
  });

  test('SC-DBF-01a: Post-Trade Debrief section appears with empty state and Generate button', async ({ page }) => {
    await gotoAndExpand(page);
    await expect(page.getByText(/post-trade debrief/i)).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('generate-debrief-btn')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/no debrief generated yet/i)).toBeVisible();
  });

  test('SC-DBF-02a: Clicking Generate renders the returned summary and focus area', async ({ page }) => {
    await gotoAndExpand(page);
    await page.getByTestId('generate-debrief-btn').click();

    await expect(page.getByTestId('debrief-content')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/exit reason: target reached/i)).toBeVisible();
    await expect(page.getByText(/your exit was 3 days earlier/i)).toBeVisible();
    await expect(page.getByText(/focus area/i)).toBeVisible();
  });

  test('SC-DBF-02b: No action affordance other than Generate/Regenerate is present (§13 Condition 4)', async ({ page }) => {
    await gotoAndExpand(page);
    const section = page.getByTestId('trade-debrief-section');
    // Only the generate button should exist before generation — no other
    // buttons, links, or affordances that could adjust a record.
    await expect(section.locator('button')).toHaveCount(1);
  });
});

// ─── SC-DBF-03 — Existing debrief renders directly ────────────────────────

test.describe('SC-DBF-03 — Existing debrief renders on load', () => {
  test('SC-DBF-03a: GET 200 with a debrief renders summary + focus area without needing to click Generate', async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await mockTrades(page);
    await mockPlanVsRealityNotFound(page);
    await page.route(new RegExp(`/trades/${TRADE_ID}/debrief`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(DEBRIEF_OK) })
    );

    await gotoAndExpand(page);
    await expect(page.getByTestId('debrief-content')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/your exit was 3 days earlier/i)).toBeVisible();
    await expect(page.getByTestId('regenerate-debrief-btn')).toBeVisible();
  });
});

// ─── SC-DBF-04 — Compliance-check fallback (no focus area) ────────────────

test.describe('SC-DBF-04 — Compliance-check fallback shows summary only', () => {
  test('SC-DBF-04a: focus_area_text null renders the fallback message, no focus-area block', async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await mockTrades(page);
    await mockPlanVsRealityNotFound(page);
    await page.route(new RegExp(`/trades/${TRADE_ID}/debrief`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(DEBRIEF_FALLBACK) })
    );

    await gotoAndExpand(page);
    await expect(page.getByTestId('debrief-content')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/exit reason: target reached/i)).toBeVisible();
    await expect(page.getByText(/didn't pass its automated compliance check/i)).toBeVisible();
    // No "Focus area" label should render when there is no focus area text.
    await expect(page.getByText(/^focus area$/i)).toHaveCount(0);
  });
});

// ─── SC-DBF-05 — Regression: Plan vs Reality section still renders ────────

test.describe('SC-DBF-05 — Regression: sibling Plan vs Reality section unaffected', () => {
  test('SC-DBF-05a: expanding a row with no plan shows neither Plan vs Reality nor an error, and Debrief still renders', async ({ page }) => {
    await mockFallback(page);
    await mockAnalytics(page);
    await mockTrades(page);
    await mockPlanVsRealityNotFound(page);
    await page.route(new RegExp(`/trades/${TRADE_ID}/debrief`), (route) =>
      route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'No debrief generated yet for this trade' }) })
    );

    await gotoAndExpand(page);
    await expect(page.locator('[data-testid="plan-vs-reality-section"]')).toHaveCount(0);
    await expect(page.getByTestId('trade-debrief-section')).toBeVisible({ timeout: 8000 });
  });
});
