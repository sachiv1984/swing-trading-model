/**
 * Risk Dashboard Acceptance Tests — ST-11
 * Canonical Test Scenario Library Phase 1
 *
 * Covers: SC-RD-02 through SC-RD-06, SC-RD-07 through SC-RD-12,
 *         SC-RD-15, SC-RD-16 through SC-RD-18, SC-RD-24, SC-RD-25
 * (17 scenarios previously blocked by TEST-GAP-EPIC-01)
 *
 * Spec refs: docs/specs/frontend/pages/risk_dashboard.md
 *            docs/specs/metrics_definitions.md
 * Scenario definitions: docs/testing/risk_dashboard_scenarios.md
 * Mock data: tests/e2e/mocks/portfolio-mock-data.js
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required. Intercepts GET http://localhost:8000/portfolio
 * and GET http://localhost:8000/portfolio/prospective-heat.
 *
 * Decision record: 2026-03-09 session — Facilitator/Challenger/DoQ agreed
 * mock layer approach (RISK-07 resolution).
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE (Friction 3 — 2026-03-06__release-v1.9 Sprint 1):
 * This app uses HashRouter. ALL navigation must use page.goto('/#/PageKey')
 * — NOT page.goto('/path'). Path-based navigation silently loads the wrong
 * page (the main Dashboard) without a 404 error. Page keys are defined in
 * src/pages.config.js. This comment must be preserved in all future
 * Playwright spec files added to this suite.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const {
  TD_01,
  TD_02,
  TD_03,
  TD_04,
  TD_05,
  TD_06,
  TD_07,
  TD_08,
  TD_10,
  PROSPECTIVE_HEAT_TD10_ABOVE_20,
  PROSPECTIVE_HEAT_GENERIC,
  EMPTY_POSITIONS,
} = require('./mocks/portfolio-mock-data');

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

const API_BASE = 'http://localhost:8000';

/** Mock GET /portfolio with a specific dataset. */
async function mockPortfolio(page, dataset) {
  await page.route(`${API_BASE}/portfolio`, async (route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(dataset) });
    } else {
      await route.continue();
    }
  });
}

/** Mock GET /positions to return empty array (prevents entity fallback). */
async function mockPositions(page, data = EMPTY_POSITIONS) {
  await page.route(`${API_BASE}/positions`, async (route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(data) });
  });
}

/** Mock GET /portfolio to return 500 (triggers error states). */
async function mockPortfolioError(page) {
  await page.route(`${API_BASE}/portfolio`, async (route) => {
    await route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ message: 'Internal server error' }) });
  });
  // Also suppress entity fallback so error state renders
  await mockPositions(page, EMPTY_POSITIONS);
}

/** Mock GET /portfolio/prospective-heat with a given response. */
async function mockProspectiveHeat(page, response) {
  await page.route(`${API_BASE}/portfolio/prospective-heat*`, async (route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(response) });
  });
}

/** Mock GET /portfolio/prospective-heat to return 500. */
async function mockProspectiveHeatError(page) {
  await page.route(`${API_BASE}/portfolio/prospective-heat*`, async (route) => {
    await route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ message: 'Calculation failed' }) });
  });
}

/** Navigate to the Risk Dashboard and wait for loading to resolve. */
async function navigateToRiskDashboard(page) {
  // HashRouter: routes are hash-based (/#/PageKey)
  await page.goto('/#/RiskDashboard');
  // Wait for the Risk Dashboard heading to confirm we're on the right page
  await expect(page.locator('h1').filter({ hasText: 'Risk Dashboard' })).toBeVisible({ timeout: 15000 });
  // Wait for loading spinner to disappear (portfolio data loaded)
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 15000 });
}

/** Get the center SVG text element that shows the gauge percentage.
 *  Scoped to the HeatGauge SVG via its viewBox to avoid matching any
 *  other SVG text elements that may exist in the page layout.
 */
const gaugeValueText = (page) =>
  page.locator('svg[viewBox="20 25 160 90"] text').first();

/** Expand the Prospective Heat panel. */
async function expandProspectiveHeat(page) {
  await page.locator('button', { hasText: 'Prospective Heat Calculator' }).click();
  await expect(page.locator('#ticker')).toBeVisible();
}

// ---------------------------------------------------------------------------
// Group A — Portfolio Heat Gauge: Threshold Boundaries
// Spec: risk_dashboard.md §3.3; metrics_definitions.md §Portfolio Heat Display Thresholds
// ---------------------------------------------------------------------------

test.describe('Group A — Heat Gauge Threshold Colours', () => {

  // SC-RD-02
  test('SC-RD-02: heat at 9.9% renders green Low colour', async ({ page }) => {
    await mockPortfolio(page, TD_02);
    await navigateToRiskDashboard(page);

    // Gauge text shows correct value
    await expect(gaugeValueText(page)).toContainText('9.9%');
    // Colour is #22c55e (green — Low band, < 10%)
    await expect(gaugeValueText(page)).toHaveAttribute('fill', '#22c55e');
  });

  // SC-RD-03
  test('SC-RD-03: heat at exactly 10.0% renders amber Moderate colour (boundary)', async ({ page }) => {
    await mockPortfolio(page, TD_03);
    await navigateToRiskDashboard(page);

    await expect(gaugeValueText(page)).toContainText('10.0%');
    // Boundary rule: 10% falls into Moderate, NOT Low
    await expect(gaugeValueText(page)).toHaveAttribute('fill', '#f59e0b');
  });

  // SC-RD-04
  test('SC-RD-04: heat at exactly 20.0% renders orange High colour (boundary)', async ({ page }) => {
    await mockPortfolio(page, TD_04);
    await navigateToRiskDashboard(page);

    await expect(gaugeValueText(page)).toContainText('20.0%');
    // Boundary rule: 20% falls into High, NOT Moderate
    await expect(gaugeValueText(page)).toHaveAttribute('fill', '#f97316');
  });

  // SC-RD-05
  test('SC-RD-05: heat at exactly 30.0% renders red Extreme colour (boundary)', async ({ page }) => {
    await mockPortfolio(page, TD_05);
    await navigateToRiskDashboard(page);

    await expect(gaugeValueText(page)).toContainText('30.0%');
    // Boundary rule: 30% falls into Extreme, NOT High
    await expect(gaugeValueText(page)).toHaveAttribute('fill', '#ef4444');
  });

  // SC-RD-06
  test('SC-RD-06: heat at 35.0% renders red Extreme colour', async ({ page }) => {
    await mockPortfolio(page, TD_06);
    await navigateToRiskDashboard(page);

    await expect(gaugeValueText(page)).toContainText('35.0%');
    await expect(gaugeValueText(page)).toHaveAttribute('fill', '#ef4444');
  });

});

// ---------------------------------------------------------------------------
// Group B — Grace Period Panel
// Spec: risk_dashboard.md v0.1.16 §5.2 (§5.3, §5.4 retired with the rows at ST-04)
// ---------------------------------------------------------------------------

test.describe('Group B — Grace Period Panel', () => {
  // ST-04 (BLG-FE-257, v9.17): risk_dashboard.md v0.1.16 §5.2. The per-position
  // rows (and §5.3 colour coding, §5.4 sort) are removed; the panel shows the
  // count badge, when the next grace period ends, and a link to the single grace
  // view on Positions. grace_days_remaining 1 is the last day ("Ends today"), so
  // a value n ends in n − 1 days (the Positions strip's convention).
  const panel = (page) => page.locator('div.rounded-2xl').filter({ has: page.getByRole('heading', { name: 'Grace Period Positions', exact: true }) });

  // SC-RD-07
  test('SC-RD-07: panel shows the count, next end and the link to Positions; no rows', async ({ page }) => {
    await mockPortfolio(page, TD_07);
    await navigateToRiskDashboard(page);

    // INDI has grace_period=false, so it is not counted.
    await expect(page.getByText('3 positions in grace period', { exact: true })).toBeVisible();
    await expect(page.getByTestId('grace-panel-next-ends')).toHaveText('Ends today');
    const link = page.getByTestId('grace-panel-link');
    await expect(link).toHaveText('View grace periods on Positions');
    await expect(link).toHaveAttribute('href', /#\/Positions\?grace=open$/);
    await expect(link.locator('svg.lucide-chevron-right')).toHaveAttribute('aria-hidden', 'true');
    await expect(page.locator('[data-testid="grace-period-row"]')).toHaveCount(0);
    await expect(panel(page)).not.toContainText('FOXT');
  });

  // SC-RD-08
  test('SC-RD-08: lowest grace_days_remaining 1 reads "Ends today"', async ({ page }) => {
    await mockPortfolio(page, TD_07); // FOXT has 1 day remaining
    await navigateToRiskDashboard(page);
    await expect(page.getByTestId('grace-panel-next-ends')).toHaveText('Ends today');
  });

  // SC-RD-09
  test('SC-RD-09: lowest grace_days_remaining 2 reads "Next ends in 1 day"', async ({ page }) => {
    const td = {
      ...TD_07,
      positions: [{ ...TD_07.positions[1], ticker: 'TEST2', grace_days_remaining: 2 }],
    };
    await mockPortfolio(page, td);
    await navigateToRiskDashboard(page);
    await expect(page.getByText('1 position in grace period', { exact: true })).toBeVisible();
    await expect(page.getByTestId('grace-panel-next-ends')).toHaveText('Next ends in 1 day');
  });

  // SC-RD-10
  test('SC-RD-10: the line uses the lowest grace_days_remaining across positions', async ({ page }) => {
    const td = {
      ...TD_07,
      positions: [
        { ...TD_07.positions[1], ticker: 'GOLF', grace_days_remaining: 4 },
        { ...TD_07.positions[1], id: 'p-hotl2', ticker: 'HOTL', grace_days_remaining: 5 },
      ],
    };
    await mockPortfolio(page, td);
    await navigateToRiskDashboard(page);
    await expect(page.getByTestId('grace-panel-next-ends')).toHaveText('Next ends in 3 days');
  });

  // SC-RD-11
  test('SC-RD-11: the line is omitted when grace_days_remaining is null', async ({ page }) => {
    const td = {
      ...TD_07,
      positions: [{ ...TD_07.positions[1], ticker: 'NULLD', grace_days_remaining: null }],
    };
    await mockPortfolio(page, td);
    await navigateToRiskDashboard(page);
    await expect(page.getByTestId('grace-panel-link')).toBeVisible();
    await expect(page.getByTestId('grace-panel-next-ends')).toHaveCount(0);
  });

  // SC-RD-12
  test('SC-RD-12: expired grace position (grace_period=false) not counted', async ({ page }) => {
    await mockPortfolio(page, TD_08);
    await navigateToRiskDashboard(page);
    // JULIET (grace_period=true, 10d) counts; KILO (grace_period=false) does not.
    await expect(page.getByText('1 position in grace period', { exact: true })).toBeVisible();
    await expect(page.getByTestId('grace-panel-next-ends')).toHaveText('Next ends in 9 days');
  });

});

// ---------------------------------------------------------------------------
// Group C — Position Risk Table (empty state only — SC-RD-14 sort test in Group C full)
// Spec: risk_dashboard.md §6.5
// ---------------------------------------------------------------------------

test.describe('Group C — Position Risk Table', () => {

  // SC-RD-15
  test('SC-RD-15: empty state — no open positions', async ({ page }) => {
    await mockPortfolio(page, TD_01);
    await navigateToRiskDashboard(page);

    // Table shows empty message; no table rows
    await expect(page.locator('text=No open positions to display')).toBeVisible();
    await expect(page.locator('tbody tr')).toHaveCount(0);
  });

});

// ---------------------------------------------------------------------------
// Group D — Prospective Heat Calculator
// Spec: risk_dashboard.md §7.4, §7.5, §7.6
// ---------------------------------------------------------------------------

test.describe('Group D — Prospective Heat Calculator', () => {

  // SC-RD-16
  test('SC-RD-16: prospective heat crossing 20% — shows 21.0% High and +6.0% delta', async ({ page }) => {
    await mockPortfolio(page, TD_10);
    await mockProspectiveHeat(page, PROSPECTIVE_HEAT_TD10_ABOVE_20);
    await navigateToRiskDashboard(page);
    await expandProspectiveHeat(page);

    await page.fill('#ticker', 'PAPA');
    await page.fill('#shares', '100');
    await page.fill('#entry_price', '20.00');
    await page.fill('#stop_price', '14.00');
    await page.locator('button[type="submit"]').click();

    // Wait for result
    await expect(page.locator('text=21.0%')).toBeVisible({ timeout: 10000 });
    // Delta: +6.0% (21.0 - 15.0)
    await expect(page.locator('text=+6.0%')).toBeVisible();
  });

  // SC-RD-17
  test('SC-RD-17: stop price >= entry price rejected client-side — no API call', async ({ page }) => {
    await mockPortfolio(page, TD_10);
    // Track whether API was called
    let apiCalled = false;
    await page.route(`${API_BASE}/portfolio/prospective-heat*`, async (route) => {
      apiCalled = true;
      await route.continue();
    });
    await navigateToRiskDashboard(page);
    await expandProspectiveHeat(page);

    // Stop = Entry (equal)
    await page.fill('#ticker', 'TEST');
    await page.fill('#shares', '100');
    await page.fill('#entry_price', '10.00');
    await page.fill('#stop_price', '10.00');
    await page.locator('button[type="submit"]').click();

    await expect(page.locator('text=Must be less than entry price')).toBeVisible();
    expect(apiCalled).toBe(false);

    // Stop > Entry
    await page.fill('#stop_price', '10.01');
    await page.locator('button[type="submit"]').click();
    await expect(page.locator('text=Must be less than entry price')).toBeVisible();
    expect(apiCalled).toBe(false);
  });

  // SC-RD-18
  test('SC-RD-18: valid inputs — projected heat and delta displayed to 1dp', async ({ page }) => {
    // Current heat = 9.0% (use TD_02 adjusted, close enough; mock returns 12.0%)
    const currentHeatData = { ...TD_02, portfolio_heat_percent: 9.0 };
    await mockPortfolio(page, currentHeatData);
    await mockProspectiveHeat(page, PROSPECTIVE_HEAT_GENERIC);
    await navigateToRiskDashboard(page);
    await expandProspectiveHeat(page);

    await page.fill('#ticker', 'QRST');
    await page.fill('#shares', '100');
    await page.fill('#entry_price', '15.00');
    await page.fill('#stop_price', '12.00');
    await page.locator('button[type="submit"]').click();

    // Projected heat shown to 1dp
    await expect(page.locator('text=12.0%')).toBeVisible({ timeout: 10000 });
    // Delta: +3.0% (12.0 - 9.0), shown in red (positive delta)
    await expect(page.locator('text=+3.0%')).toBeVisible();
  });

});

// ---------------------------------------------------------------------------
// Group E (partial) — API Error States
// SC-RD-24: Prospective heat endpoint error
// Spec: risk_dashboard.md §7.6
// ---------------------------------------------------------------------------

test.describe('Group E — API Error States (partial)', () => {

  // SC-RD-24
  test('SC-RD-24: prospective heat endpoint 500 — inline error shown, no crash', async ({ page }) => {
    await mockPortfolio(page, TD_10);
    await mockProspectiveHeatError(page);
    await navigateToRiskDashboard(page);
    await expandProspectiveHeat(page);

    await page.fill('#ticker', 'ERR');
    await page.fill('#shares', '100');
    await page.fill('#entry_price', '20.00');
    await page.fill('#stop_price', '14.00');
    await page.locator('button[type="submit"]').click();

    // Inline error displayed (apiError paragraph — className="text-sm text-rose-700 dark:text-rose-400"
    // as of ST-16, EPIC-04, v8.4, BLG-FE-140 — light/dark colour-token pair, was bare text-rose-400)
    const apiErrorText = page.getByText('Calculation failed');
    await expect(apiErrorText).toBeVisible({ timeout: 10000 });
    await expect(apiErrorText).toHaveClass(/text-rose-700/);
    await expect(apiErrorText).toHaveClass(/dark:text-rose-400/);
    // No projected heat value shown
    await expect(page.locator('text=Projected Heat')).toHaveCount(0);
    // Page has not crashed — heading still visible
    await expect(page.locator('h1').filter({ hasText: 'Risk Dashboard' })).toBeVisible();
    // Input fields still accessible
    await expect(page.locator('#ticker')).toBeVisible();
  });

});

// ---------------------------------------------------------------------------
// Group F — Empty State (No Open Positions)
// Spec: risk_dashboard.md §3.4, §5.5, §6.5
// ---------------------------------------------------------------------------

test.describe('Group F — Full Empty State', () => {

  // SC-RD-25
  test('SC-RD-25: full empty state — no positions, all components render correct empty views', async ({ page }) => {
    await mockPortfolio(page, TD_01);
    await navigateToRiskDashboard(page);

    // Heat gauge: 0.0% green
    await expect(gaugeValueText(page)).toContainText('0.0%');
    await expect(gaugeValueText(page)).toHaveAttribute('fill', '#22c55e');

    // Grace period panel: empty state (text updated in EPIC-04 ST-08)
    await expect(page.locator('text=No positions currently in grace period')).toBeVisible();

    // Position risk table: empty state
    await expect(page.locator('text=No open positions to display')).toBeVisible();

    // Prospective heat: still interactive
    await expandProspectiveHeat(page);
    await expect(page.locator('#ticker')).toBeVisible();

    // No console errors (verified separately via SC-RD-26)
    // No crash: page heading still present
    await expect(page.locator('h1').filter({ hasText: 'Risk Dashboard' })).toBeVisible();
  });

});
