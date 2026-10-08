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
 *   SC-DBF-06: Regenerate has a visible border/background in dark and light themes; axe scan of the
 *              debrief section reports no colour-contrast violations (ST-05, v9.11, BLG-FE-205)
 *   SC-DBF-07: A mocked 500 on POST shows the regenerate error and keeps the existing debrief (ST-05)
 *   SC-DBF-08: After a successful regenerate, the generated timestamp updates (ST-05)
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
const AxeBuilder = require('@axe-core/playwright').default;

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


// ─── SC-DBF-06/07/08 — Regenerate button, failure message, generated time ──
// ST-05 (EPIC-01, v9.11, BLG-FE-205). Design:
// docs/design/2026-10-08__release-v9.11/debrief-regenerate-feedback/decision_record.md

async function mockExistingDebrief(page, { postStatus = 200, postBody = null } = {}) {
  await mockFallback(page);
  await mockAnalytics(page);
  await mockTrades(page);
  await mockPlanVsRealityNotFound(page);
  await page.route(new RegExp(`/trades/${TRADE_ID}/debrief`), (route) => {
    if (route.request().method() === 'GET') {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(DEBRIEF_OK) });
    }
    return route.fulfill({
      status: postStatus,
      contentType: 'application/json',
      body: JSON.stringify(postBody || { status: 'error', message: 'Internal Server Error' }),
    });
  });
}

for (const theme of ['dark', 'light']) {
  test(`SC-DBF-06a: Regenerate has a visible border and background, and the debrief section passes axe colour contrast (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await mockExistingDebrief(page);
    await gotoAndExpand(page);
    const btn = page.getByTestId('regenerate-debrief-btn');
    await expect(btn).toBeVisible({ timeout: 8000 });
    if (theme === 'dark') {
      await expect(page.locator('html')).toHaveClass(/\bdark\b/);
    } else {
      await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);
    }

    const style = await btn.evaluate((el) => {
      const cs = getComputedStyle(el);
      return { borderWidth: cs.borderTopWidth, borderStyle: cs.borderTopStyle, borderColor: cs.borderTopColor, bg: cs.backgroundColor };
    });
    expect(style.borderStyle).toBe('solid');
    expect(parseFloat(style.borderWidth)).toBeGreaterThan(0);
    expect(style.borderColor).not.toMatch(/rgba\(0, 0, 0, 0\)|transparent/);
    expect(style.bg).not.toMatch(/rgba\(0, 0, 0, 0\)|transparent/);

    // Let the row-expand animation settle before sampling colours.
    await page.waitForTimeout(1000);
    const results = await new AxeBuilder({ page })
      .include('[data-testid="trade-debrief-section"]')
      .withRules(['color-contrast'])
      .analyze();
    const contrast = results.violations.filter((v) => v.id === 'color-contrast');
    expect(contrast, JSON.stringify(contrast.map((v) => v.nodes.map((n) => n.target)), null, 1)).toEqual([]);
  });
}

test('SC-DBF-07a: a 500 on POST shows the regenerate error and keeps the existing debrief', async ({ page }) => {
  await mockExistingDebrief(page, { postStatus: 500 });
  await gotoAndExpand(page);
  await expect(page.getByTestId('debrief-content')).toBeVisible({ timeout: 8000 });
  await page.getByTestId('regenerate-debrief-btn').click();

  const error = page.getByTestId('debrief-regenerate-error');
  await expect(error).toBeVisible({ timeout: 8000 });
  await expect(error).toHaveAttribute('role', 'status');
  await expect(error).toHaveText(/could not regenerate the debrief\. the previous version is still shown/i);
  // The existing debrief is still on screen, unchanged.
  await expect(page.getByTestId('debrief-content')).toBeVisible();
  await expect(page.getByText(/your exit was 3 days earlier/i)).toBeVisible();
  await expect(page.getByTestId('debrief-empty-state')).toHaveCount(0);
});

test('SC-DBF-08a: after a successful regenerate, the generated timestamp updates', async ({ page }) => {
  const fresh = {
    status: 'ok',
    data: { ...DEBRIEF_OK.data, focus_area_text: 'Your exit matched the plan on this trade.', generated_at: new Date().toISOString() },
  };
  await mockExistingDebrief(page, { postStatus: 200, postBody: fresh });
  await gotoAndExpand(page);

  const stamp = page.getByTestId('debrief-generated-at');
  await expect(stamp).toBeVisible({ timeout: 8000 });
  const before = await stamp.textContent();
  expect(before).toMatch(/^Generated \d+ days? ago$/);

  await page.getByTestId('regenerate-debrief-btn').click();
  await expect(stamp).toHaveText('Generated just now', { timeout: 8000 });
  await expect(page.getByText(/your exit matched the plan on this trade/i)).toBeVisible();
  await expect(page.getByTestId('debrief-regenerate-error')).toHaveCount(0);
});
