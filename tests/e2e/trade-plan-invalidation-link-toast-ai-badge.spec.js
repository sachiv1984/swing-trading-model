/**
 * Invalidation Condition Field, Link-Confirmation Toast, AI-Draft Badge
 * ST-01 (BLG-FEAT-84) / ST-02 (BLG-FE-158) / ST-03 (BLG-BE-95) — EPIC-01, v8.7
 *
 * Covers observable AC:
 *   SC-INV-01  Invalidation Condition field renders on the trade plan form
 *   SC-INV-02  Field value is included in the POST /trade-plans payload on save
 *   SC-LNK-01  TradeEntry shows a success toast naming the linked ticker when
 *              trade_plan_linked: true (trade_plan.md Sec10.6)
 *   SC-LNK-02  TradeEntry shows a neutral "logged unlinked" toast when
 *              trade_plan_linked: false
 *   SC-AID-01  Setup Thesis Digest panel shows the "AI draft" badge when the
 *              linked plan's is_ai_draft is true (trade_plan.md Sec10.5)
 *   SC-AID-02  Badge is absent when is_ai_draft is false
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMarketStatus(page) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { regime_status: 'risk_on' } }) })
  );
}

async function mockByPosition(page) {
  await page.route(new RegExp(`${API}/trade-plans/by-position/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: null }) })
  );
}

async function gotoTradePlan(page, params = {}) {
  const qs = new URLSearchParams(params).toString();
  const hash = qs ? `/#/TradePlan?${qs}` : '/#/TradePlan';
  await page.goto(hash);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

test.describe('Invalidation Condition field (SC-INV-01/02)', () => {
  test('SC-INV-01: field renders with the spec placeholder', async ({ page }) => {
    await mockFallback(page);
    await mockMarketStatus(page);
    await mockByPosition(page);
    await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

    await expect(page.getByPlaceholder('What would prove this thesis wrong? (optional)')).toBeVisible({ timeout: 8000 });
  });

  test('SC-INV-02: field value is sent in the POST /trade-plans payload', async ({ page }) => {
    await mockFallback(page);
    await mockMarketStatus(page);
    await mockByPosition(page);
    let capturedBody = null;
    await page.route(`${API}/trade-plans`, (route) => {
      if (route.request().method() === 'POST') {
        capturedBody = route.request().postDataJSON();
        return route.fulfill({
          status: 201,
          contentType: 'application/json',
          body: JSON.stringify({ status: 'ok', data: { id: 'new-plan-1', ...capturedBody } }),
        });
      }
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    });
    await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

    await page.getByPlaceholder('What would prove this thesis wrong? (optional)').fill('Close below 200 SMA on volume');
    await page.getByRole('button', { name: /save plan/i }).click();

    await expect.poll(() => capturedBody).not.toBeNull();
    expect(capturedBody.invalidation_condition).toBe('Close below 200 SMA on volume');
  });
});

test.describe('Post-submission link-confirmation toast (SC-LNK-01/02)', () => {
  async function mockAddPosition(page, tradePlanLinked) {
    await page.route(`${API}/portfolio/position`, (route) => {
      const body = route.request().postDataJSON();
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            ticker: body.ticker,
            total_cost: 1500,
            fees_paid: 10,
            entry_price: body.entry_price,
            initial_stop: body.stop_price,
            remaining_cash: 5000,
            position_id: 'new-pos-1',
            trade_plan_linked: tradePlanLinked,
            trade_plan_id: tradePlanLinked ? 'plan-001' : null,
          },
        }),
      });
    });
  }

  async function fillAndSubmitTradeEntry(page) {
    await page.goto('/#/TradeEntry');
    await page.locator('input[placeholder*="AAPL"]').fill('MSFT');
    await page.getByPlaceholder('0.00').first().fill('300');
    await page.getByPlaceholder('0', { exact: true }).fill('5');
    await page.getByRole('button', { name: /create position/i }).click();
  }

  test('SC-LNK-01: success toast names the linked ticker when trade_plan_linked is true', async ({ page }) => {
    await mockFallback(page);
    await mockAddPosition(page, true);
    await fillAndSubmitTradeEntry(page);

    await expect(page.getByText('Linked to trade plan for MSFT.')).toBeVisible({ timeout: 8000 });
  });

  test('SC-LNK-02: neutral toast shown when trade_plan_linked is false', async ({ page }) => {
    await mockFallback(page);
    await mockAddPosition(page, false);
    await fillAndSubmitTradeEntry(page);

    await expect(page.getByText('No matching plan found — logged unlinked.')).toBeVisible({ timeout: 8000 });
  });
});

test.describe('Setup Thesis Digest AI-draft badge (SC-AID-01/02)', () => {
  const BASE_PLAN = {
    id: 'plan-001',
    ticker: 'AAPL',
    market: 'US',
    status: 'draft',
    position_id: null,
    setup_thesis: 'Breakout above 52-week high with volume confirmation.',
    early_exit_conditions: 'Close below 200 SMA.',
    confirmation_criteria: 'Volume > 1.5x average.',
    planned_entry_price: 150.0,
    planned_stop_price: 140.0,
    planned_quantity: 10,
  };

  async function mockTradePlansList(page, plans) {
    await page.route(`${API}/trade-plans`, (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plans }) });
      }
      return route.continue();
    });
  }

  async function mockTradePlanById(page, plan) {
    await page.route(new RegExp(`${API}/trade-plans/${plan.id}$`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plan }) })
    );
  }

  /** Navigates to TradeEntry the same way a real user would -- via the
   *  "Start Trade" action on the TradePlans list -- so react-router's
   *  location.state (trade_plan_prefill) is set by the app itself. */
  async function startTradeFromPlan(page, plan) {
    await mockTradePlansList(page, [plan]);
    await mockTradePlanById(page, plan);
    await page.goto('/#/TradePlans');
    await page.getByTestId(`start-trade-from-plan-${plan.id}`).click();
    await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });
  }

  test('SC-AID-01: AI draft badge shown when linked plan is_ai_draft is true', async ({ page }) => {
    await mockFallback(page);
    await startTradeFromPlan(page, { ...BASE_PLAN, is_ai_draft: true });

    await expect(page.getByTestId('setup-thesis-digest-panel')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('ai-draft-badge')).toBeVisible({ timeout: 8000 });
  });

  test('SC-AID-02: badge absent when linked plan is_ai_draft is false', async ({ page }) => {
    await mockFallback(page);
    await startTradeFromPlan(page, { ...BASE_PLAN, is_ai_draft: false });

    await expect(page.getByTestId('setup-thesis-digest-panel')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('ai-draft-badge')).toHaveCount(0);
  });
});
