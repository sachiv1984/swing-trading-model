/**
 * Trade Plan Linkage Advisory — ST-28 (EPIC-06, v9.4, BLG-FEAT-95)
 *
 * Coverage (per position_form.md §Trade Plan Linkage Advisory's own
 * "Test coverage required" clause):
 *
 *   SC-TPA-01  Advisory banner renders on TradeEntry when no trade_plan_id is linked
 *   SC-TPA-02  Advisory banner does not render when a trade plan is linked (real "Start Trade from Plan" flow)
 *   SC-TPA-03  Submission succeeds with the banner visible (non-blocking — no new gate)
 *
 * Reuses the exact mock helpers and "Start Trade from Plan" click-through
 * pattern already established in v7.2-dashboard-tradeplan-ux-hardening.spec.js
 * (ST-01, EPIC-01, v7.3) rather than re-deriving TradeEntry's plan-linkage
 * navigation state from scratch — that file's own SC-STP-06 already proves
 * `mockFallback` + `mockTradePlansList(page, [])` is sufficient to load
 * TradeEntry.js and submit successfully with no plan linked.
 *
 * Infrastructure: Playwright page.route() network interception. No live
 * backend required. HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const PLAN_DRAFT_UNLINKED = {
  id: 'plan-tpa-001',
  ticker: 'AAPL',
  market: 'US',
  status: 'draft',
  position_id: null,
  r_target: 2.5,
  setup_thesis: 'Breakout setup',
  updated_at: '2026-09-15T10:00:00Z',
  planned_entry_price: 150.0,
  planned_stop_price: 140.0,
  planned_quantity: 10,
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTradePlansList(page, plans) {
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plans }) });
    } else {
      route.continue();
    }
  });
}

async function mockAddPositionCapture(page, { onRequest } = {}) {
  await page.route(`${API}/portfolio/position`, (route) => {
    const body = route.request().postDataJSON();
    if (onRequest) onRequest(body);
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: { ticker: body.ticker, total_cost: 1500, fees_paid: 10, entry_price: body.entry_price, initial_stop: body.stop_price, remaining_cash: 5000, position_id: 'new-pos-tpa-1' },
      }),
    });
  });
}

test.describe('ST-28 — Trade Plan Linkage Advisory', () => {
  test('SC-TPA-01: Advisory banner renders when no trade plan is linked', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, []);

    await page.goto('/#/TradeEntry');

    await expect(page.locator('input[placeholder*="AAPL"]')).toBeVisible({ timeout: 10000 });

    const advisory = page.getByTestId('trade-plan-linkage-advisory');
    await expect(advisory).toBeVisible({ timeout: 5000 });
    await expect(advisory).toContainText('No trade plan linked to this position');
    await expect(advisory.getByRole('button', { name: 'Create Trade Plan' })).toBeVisible();
  });

  test('SC-TPA-02: Advisory banner does not render once a trade plan is linked via "Start Trade from Plan"', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, [PLAN_DRAFT_UNLINKED]);

    await page.goto('/#/TradePlans');
    await page.getByTestId(`start-trade-from-plan-${PLAN_DRAFT_UNLINKED.id}`).click();

    await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });
    // The pre-existing linked-plan banner (ST-01, v7.3) confirms a plan is
    // in fact linked for this navigation.
    await expect(page.getByTestId('trade-plan-linked-banner')).toBeVisible({ timeout: 5000 });
    // This story's new advisory must not also render once linked.
    await expect(page.getByTestId('trade-plan-linkage-advisory')).toHaveCount(0);
  });

  test('SC-TPA-03: Submission succeeds with the advisory banner visible (non-blocking)', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, []);
    let capturedBody = null;
    await mockAddPositionCapture(page, { onRequest: (body) => { capturedBody = body; } });

    await page.goto('/#/TradeEntry');

    const advisory = page.getByTestId('trade-plan-linkage-advisory');
    await expect(advisory).toBeVisible({ timeout: 10000 });

    await page.locator('input[placeholder*="AAPL"]').fill('MSFT');
    await page.getByPlaceholder('0.00').first().fill('300');
    await page.getByPlaceholder('0.00').last().fill('280');
    await page.getByPlaceholder('0', { exact: true }).fill('5');

    // Advisory still visible immediately before submit — it adds no new
    // gate; the Create Position button is enabled regardless.
    await expect(advisory).toBeVisible();

    await page.getByRole('button', { name: /create position/i }).click();

    await expect.poll(() => capturedBody).not.toBeNull();
    expect(capturedBody.ticker).toBe('MSFT');
    expect(capturedBody.trade_plan_id).toBeNull();
  });
});
