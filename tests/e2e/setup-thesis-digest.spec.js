/**
 * SetupThesisDigestPanel — Playwright Acceptance Tests
 * ST-02 (EPIC-01, v8.6) — BLG-FEAT-56
 *
 * Covers observable ACs for the Setup Thesis Digest panel on the Trade
 * Entry page (trade_plan.md §10.5):
 *
 *   SC-TSD-01  Panel renders with "Setup Thesis Digest" heading when the
 *              linked plan has setup_thesis content
 *   SC-TSD-02  Setup Thesis text is visible
 *   SC-TSD-03  Key Risk Factors bullets are visible, sourced from
 *              early_exit_conditions/confirmation_criteria
 *   SC-TSD-04  Panel does not render at all when the linked plan has no
 *              setup_thesis and no early_exit_conditions
 *   SC-TSD-05  "View full plan →" link navigates to the plan detail view
 *   SC-TSD-06  Collapse/expand toggle hides and re-shows the panel body
 *
 * Spec ref: docs/specs/frontend/pages/trade_plan.md §10.5
 * Design source: docs/design/2026-08-11__release-v8.6/ai-thesis-digest-order-placement/ux_spec.md
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required. Reaches TradeEntry via the existing
 * "Start Trade from Plan" flow (v7.2-dashboard-tradeplan-ux-hardening.spec.js
 * pattern) so trade_plan_id/linkedPlanId is populated the same way
 * production traffic reaches it.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const PLAN_WITH_THESIS = {
  id: 'plan-tsd-01',
  ticker: 'AAPL',
  market: 'US',
  status: 'draft',
  position_id: null,
  r_target: 2.5,
  setup_thesis: 'Breakout above the 50-day moving average with rising volume. Sector momentum is strong.',
  early_exit_conditions: 'Close below the 20-day moving average. Volume dries up on the breakout attempt.',
  confirmation_criteria: 'Price holds above resistance for two consecutive closes.',
  updated_at: '2026-08-11T10:00:00Z',
  planned_entry_price: 150.0,
  planned_stop_price: 140.0,
  planned_quantity: 10,
};

const PLAN_NO_THESIS = {
  id: 'plan-tsd-02',
  ticker: 'MSFT',
  market: 'US',
  status: 'draft',
  position_id: null,
  r_target: 2.0,
  setup_thesis: '',
  early_exit_conditions: '',
  confirmation_criteria: '',
  updated_at: '2026-08-11T10:00:00Z',
  planned_entry_price: 300.0,
  planned_stop_price: 280.0,
  planned_quantity: 5,
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

async function mockTradePlanById(page, plan) {
  await page.route(new RegExp(`${API}/trade-plans/${plan.id}$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plan }) })
  );
}

async function startTradeFromPlan(page, plan) {
  await mockFallback(page);
  await mockTradePlansList(page, [plan]);
  await mockTradePlanById(page, plan);

  await page.goto('/#/TradePlans');
  await page.getByTestId(`start-trade-from-plan-${plan.id}`).click();
  await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });
}

test.describe('SC-TSD-01/02/03 — Panel renders with thesis and risk factors', () => {
  test('SC-TSD-01/02/03: heading, thesis text, and risk factor bullets are visible', async ({ page }) => {
    await startTradeFromPlan(page, PLAN_WITH_THESIS);

    const panel = page.getByTestId('setup-thesis-digest-panel');
    await expect(panel).toBeVisible({ timeout: 10000 });
    await expect(panel.getByText('Setup Thesis Digest')).toBeVisible();
    await expect(panel.getByText(/Breakout above the 50-day moving average/)).toBeVisible();
    await expect(panel.getByText(/Close below the 20-day moving average/)).toBeVisible();
    await expect(panel.getByText(/Price holds above resistance/)).toBeVisible();
  });
});

test.describe('SC-TSD-04 — Panel hidden when no thesis content', () => {
  test('SC-TSD-04: panel does not render when the linked plan has no thesis or exit conditions', async ({ page }) => {
    await startTradeFromPlan(page, PLAN_NO_THESIS);

    await expect(page.getByTestId('trade-plan-linked-banner')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('setup-thesis-digest-panel')).toHaveCount(0);
  });
});

test.describe('SC-TSD-05 — View full plan link', () => {
  test('SC-TSD-05: "View full plan" link points to the plan detail view', async ({ page }) => {
    await startTradeFromPlan(page, PLAN_WITH_THESIS);

    const panel = page.getByTestId('setup-thesis-digest-panel');
    await expect(panel).toBeVisible({ timeout: 10000 });

    const link = panel.getByText('View full plan →');
    await expect(link).toBeVisible();
    await expect(link).toHaveAttribute('href', new RegExp(`/TradePlan\\?edit=${PLAN_WITH_THESIS.id}`));
  });
});

test.describe('SC-TSD-06 — Collapse/expand toggle', () => {
  test('SC-TSD-06: collapsing hides the body, expanding re-shows it', async ({ page }) => {
    await startTradeFromPlan(page, PLAN_WITH_THESIS);

    const panel = page.getByTestId('setup-thesis-digest-panel');
    await expect(panel).toBeVisible({ timeout: 10000 });
    await expect(panel.getByText('Setup Thesis')).toBeVisible();

    await panel.getByLabel('Collapse details').click();
    await expect(panel.getByText('Setup Thesis')).not.toBeVisible();

    await panel.getByLabel('Expand details').click();
    await expect(panel.getByText('Setup Thesis')).toBeVisible();
  });
});
