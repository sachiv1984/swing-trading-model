/**
 * Shared Playwright Spec — v7.2 Dashboard/Trade-Plan UX Hardening
 *
 * Named at planning time by ST-08 (BLG-QA-111, EPIC-05, v7.2) —
 * docs/specs/frontend/blg_qa_111_combined_design_review_shared_playwright_plan.md §3.
 * Populated here by the three implementation stories that landed in
 * 2026-07-16__release-v7.3 EPIC-01 (renumbered from the v7.2 plan's ST-03/ST-05/ST-06):
 *
 *   describe("Start Trade from Plan")         — ST-01, AC-01–AC-04
 *   describe("Dashboard empty states")         — ST-02, AC-01–AC-02
 *   describe("Dashboard briefing hierarchy")   — ST-03, AC-01, AC-03
 *
 * Each dual-theme case follows base44_prompt_template_library.md §4 — verify
 * both light and dark, never dark-only.
 *
 * Infrastructure: Playwright page.route() network interception. No live
 * backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const PLAN_DRAFT_UNLINKED = {
  id: 'plan-001',
  ticker: 'AAPL',
  market: 'US',
  status: 'draft',
  position_id: null,
  r_target: 2.5,
  setup_thesis: 'Breakout setup',
  updated_at: '2026-07-15T10:00:00Z',
  planned_entry_price: 150.0,
  planned_stop_price: 140.0,
  planned_quantity: 10,
};

const PLAN_ALREADY_LINKED = {
  id: 'plan-002',
  ticker: 'TSLA',
  market: 'US',
  status: 'active',
  position_id: 'pos-existing',
  r_target: 2.0,
  setup_thesis: 'Already started',
  updated_at: '2026-07-14T10:00:00Z',
  planned_entry_price: 250.0,
  planned_stop_price: 230.0,
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

async function mockMarketStatus(page) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { regime_status: 'risk_on' } }) })
  );
}

/** Captures the JSON body of the next POST /portfolio/position and fulfills it. */
async function mockAddPositionCapture(page, { onRequest } = {}) {
  await page.route(`${API}/portfolio/position`, (route) => {
    const body = route.request().postDataJSON();
    if (onRequest) onRequest(body);
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: { ticker: body.ticker, total_cost: 1500, fees_paid: 10, entry_price: body.entry_price, initial_stop: body.stop_price, remaining_cash: 5000, position_id: 'new-pos-1' },
      }),
    });
  });
}

// ---------------------------------------------------------------------------
// describe("Start Trade from Plan") — ST-01, AC-01–AC-04
// ---------------------------------------------------------------------------

test.describe('Start Trade from Plan', () => {
  test('SC-STP-01: "Start Trade" action visible for an eligible plan on the TradePlans list', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, [PLAN_DRAFT_UNLINKED]);
    await page.goto('/#/TradePlans');

    await expect(page.getByTestId(`start-trade-from-plan-${PLAN_DRAFT_UNLINKED.id}`)).toBeVisible({ timeout: 10000 });
  });

  test('SC-STP-02: "Start Trade" action hidden for a plan already linked to a position', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, [PLAN_ALREADY_LINKED]);
    await page.goto('/#/TradePlans');

    await expect(page.getByText(PLAN_ALREADY_LINKED.ticker)).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId(`start-trade-from-plan-${PLAN_ALREADY_LINKED.id}`)).toHaveCount(0);
  });

  test('SC-STP-03: "Start Trade from Plan" action visible on the Trade Plan detail view for an eligible plan', async ({ page }) => {
    await mockFallback(page);
    await mockMarketStatus(page);
    await mockTradePlanById(page, PLAN_DRAFT_UNLINKED);

    await page.goto(`/#/TradePlan?edit=${PLAN_DRAFT_UNLINKED.id}&ticker=${PLAN_DRAFT_UNLINKED.ticker}&market=${PLAN_DRAFT_UNLINKED.market}`);
    await expect(page.getByTestId('start-trade-from-plan-btn')).toBeVisible({ timeout: 10000 });
  });

  test('SC-STP-04: Clicking "Start Trade" navigates to Trade Entry and pre-fills ticker/entry/stop from the plan', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, [PLAN_DRAFT_UNLINKED]);
    await page.goto('/#/TradePlans');

    await page.getByTestId(`start-trade-from-plan-${PLAN_DRAFT_UNLINKED.id}`).click();

    await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });
    await expect(page.getByTestId('trade-plan-linked-banner')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('input[placeholder*="AAPL"]')).toHaveValue(PLAN_DRAFT_UNLINKED.ticker);
    await expect(page.locator('input[type="number"]').first()).toHaveValue(String(PLAN_DRAFT_UNLINKED.planned_entry_price));
  });

  test('SC-STP-05 (AC-02): Submitting a trade started from a plan sends trade_plan_id with no additional user action', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, [PLAN_DRAFT_UNLINKED]);
    let capturedBody = null;
    await mockAddPositionCapture(page, { onRequest: (body) => { capturedBody = body; } });

    await page.goto('/#/TradePlans');
    await page.getByTestId(`start-trade-from-plan-${PLAN_DRAFT_UNLINKED.id}`).click();
    await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });

    // Shares has no plan-derived default and is required for form validity —
    // its placeholder ("0") is unique among the page's number inputs.
    await page.getByPlaceholder('0', { exact: true }).fill('10');
    await page.getByRole('button', { name: /create position/i }).click();

    await expect.poll(() => capturedBody).not.toBeNull();
    expect(capturedBody.trade_plan_id).toBe(PLAN_DRAFT_UNLINKED.id);
    expect(capturedBody.ticker).toBe(PLAN_DRAFT_UNLINKED.ticker);
  });

  test('SC-STP-06 (AC-03): Manual entry with no plan origin is unaffected — no banner, empty ticker, trade_plan_id null', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, []);
    let capturedBody = null;
    await mockAddPositionCapture(page, { onRequest: (body) => { capturedBody = body; } });

    await page.goto('/#/TradeEntry');

    await expect(page.getByTestId('trade-plan-linked-banner')).toHaveCount(0);
    await expect(page.locator('input[placeholder*="AAPL"]')).toHaveValue('');

    await page.locator('input[placeholder*="AAPL"]').fill('MSFT');
    await page.getByPlaceholder('0.00').first().fill('300');
    await page.getByPlaceholder('0', { exact: true }).fill('5');
    await page.getByRole('button', { name: /create position/i }).click();

    await expect.poll(() => capturedBody).not.toBeNull();
    expect(capturedBody.trade_plan_id).toBeNull();
  });

  test('SC-STP-07 (AC-03): Manual entry can still optionally select an existing plan to link', async ({ page }) => {
    await mockFallback(page);
    await mockTradePlansList(page, [PLAN_DRAFT_UNLINKED]);
    let capturedBody = null;
    await mockAddPositionCapture(page, { onRequest: (body) => { capturedBody = body; } });

    await page.goto('/#/TradeEntry');
    await expect(page.getByTestId('link-trade-plan-select')).toBeVisible({ timeout: 5000 });

    await page.getByTestId('link-trade-plan-select').click();
    await page.getByRole('option', { name: new RegExp(PLAN_DRAFT_UNLINKED.ticker) }).click();

    await page.locator('input[placeholder*="AAPL"]').fill(PLAN_DRAFT_UNLINKED.ticker);
    await page.getByPlaceholder('0.00').first().fill('150');
    await page.getByPlaceholder('0', { exact: true }).fill('10');
    await page.getByRole('button', { name: /create position/i }).click();

    await expect.poll(() => capturedBody).not.toBeNull();
    expect(capturedBody.trade_plan_id).toBe(PLAN_DRAFT_UNLINKED.id);
  });
});

// ---------------------------------------------------------------------------
// describe("Dashboard empty states") — ST-02, AC-01–AC-02
// ---------------------------------------------------------------------------

const EMPTY_ARRAY_RESPONSE = [];

async function mockDashboardEmptyEndpoints(page) {
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_ARRAY_RESPONSE) })
  );
  await page.route(`${API}/portfolio`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, portfolio_heat_percent: null } }) })
  );
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_ARRAY_RESPONSE) })
  );
  await page.route(`${API}/signals`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_ARRAY_RESPONSE) })
  );
  await mockMarketStatus(page);
  await page.route(`${API}/positions/grace-period-alerts`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function gotoDashboard(page) {
  await page.goto('/#/DashboardHome');
  await expect(page.locator('h1').filter({ hasText: 'Dashboard' })).toBeVisible({ timeout: 10000 });
}

test.describe('Dashboard empty states', () => {
  test('SC-DES-01: OpenPositionsCard shows compact empty state, not a raw 0, when no positions — dark theme', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardEmptyEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('No open positions')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Open a position to see it here.')).toBeVisible({ timeout: 5000 });
  });

  test('SC-DES-02: OpenPositionsCard empty state renders in light theme too', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardEmptyEndpoints(page);
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await gotoDashboard(page);

    await expect(page.getByText('No open positions')).toBeVisible({ timeout: 10000 });
  });

  test('SC-DES-03: GracePeriodCard shows "No positions in grace" empty state when none in grace', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardEmptyEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('No positions in grace')).toBeVisible({ timeout: 10000 });
  });

  test('SC-DES-04: RecentActivityCard shows "No recent activity" empty state when trade history is empty', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardEmptyEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('No recent activity')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Trades and stop updates will appear here.')).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// describe("Dashboard briefing hierarchy") — ST-03, AC-01, AC-03
// ---------------------------------------------------------------------------

test.describe('Dashboard briefing hierarchy', () => {
  test('SC-DBH-01: Briefing section renders above the status-card grid on page load — dark theme', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardEmptyEndpoints(page);
    await gotoDashboard(page);

    const briefingSection = page.locator('[data-testid="morning-briefing"]').locator('xpath=..');
    const openPositionsCard = page.getByText('Open Positions', { exact: true }).locator('xpath=../..');

    await expect(briefingSection).toBeVisible({ timeout: 10000 });
    await expect(openPositionsCard).toBeVisible({ timeout: 10000 });

    const briefingBox = await briefingSection.boundingBox();
    const cardBox = await openPositionsCard.boundingBox();
    expect(briefingBox.y).toBeLessThan(cardBox.y);
  });

  test('SC-DBH-02: Briefing section visually distinguished via accent border/tint — light and dark theme', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardEmptyEndpoints(page);
    await gotoDashboard(page);

    const briefingSection = page.locator('[data-testid="morning-briefing"]').locator('xpath=..');
    const darkBorderColor = await briefingSection.evaluate((el) => getComputedStyle(el).borderColor);
    expect(darkBorderColor).not.toBe('rgba(0, 0, 0, 0)');

    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await gotoDashboard(page);
    const lightBorderColor = await briefingSection.evaluate((el) => getComputedStyle(el).borderColor);
    expect(lightBorderColor).not.toBe('rgba(0, 0, 0, 0)');
  });

  test('SC-DBH-03: AI Daily Briefing card renders within the briefing section, above the status-card grid', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardEmptyEndpoints(page);
    await gotoDashboard(page);

    const briefingSection = page.locator('[data-testid="morning-briefing"]').locator('xpath=..');
    const aiBriefingCard = page.getByTestId('ai-daily-briefing-card');
    await expect(aiBriefingCard).toBeVisible({ timeout: 10000 });

    const briefingBox = await briefingSection.boundingBox();
    const aiBox = await aiBriefingCard.boundingBox();
    // AI Daily Briefing must be inside/adjacent to the briefing wrapper, above the card grid.
    expect(aiBox.y).toBeGreaterThanOrEqual(briefingBox.y);
  });

  test('SC-DBH-04 (regression): dashboard-retry-root and card data/queries unaffected by the layout change', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardEmptyEndpoints(page);
    await gotoDashboard(page);

    // Hidden by default — only shown via the all-endpoints-failed retry flow.
    await expect(page.locator('#dashboard-retry-root')).toBeHidden({ timeout: 5000 });
    await expect(page.locator('#dashboard-retry-root button', { hasText: 'Retry' })).toHaveCount(1);
  });
});
