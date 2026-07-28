/**
 * Sector & Regime Exposure Trend — Risk Dashboard §8b
 * ST-02 (BLG-FEAT-67, EPIC-02, v7.9)
 *
 * Design source: docs/design/2026-07-27__release-v7.9/sector-regime-exposure-trend/ux_spec.md
 * Frontend spec: docs/specs/frontend/pages/risk_dashboard.md §8b
 *
 * Covers (non-visual AC only — colour rendering itself is DoQ manual/visual review):
 *   SC-SRT-01  Insufficient-history state renders when weeks_available < 8
 *   SC-SRT-02  Trend chart + regime strip render when insufficient_history: false
 *   SC-SRT-03  Error state renders on a failed sector-regime-trend fetch, does not
 *              affect the sibling Sector Concentration Heat Map panel
 *
 * What requires DoQ manual visual verification (not covered here):
 *   - Actual stacked-area colour rendering, both light and dark theme
 *   - Regime strip green/amber fill colour accuracy
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');
const { TD_01, EMPTY_POSITIONS } = require('./mocks/portfolio-mock-data');

const API_BASE = 'http://localhost:8000';

const INSUFFICIENT_HISTORY_RESPONSE = {
  status: 'ok',
  data: { insufficient_history: true, weeks_available: 3 },
};

const SUFFICIENT_HISTORY_RESPONSE = {
  status: 'ok',
  data: {
    insufficient_history: false,
    weeks: [
      {
        week_start: '2026-06-01',
        sectors: [
          { sector_name: 'Technology', exposure_pct: 42.5 },
          { sector_name: 'Financials', exposure_pct: 31.0 },
          { sector_name: 'Other', exposure_pct: 26.5 },
        ],
        regime_us: true,
        regime_uk: false,
      },
      {
        week_start: '2026-06-08',
        sectors: [
          { sector_name: 'Technology', exposure_pct: 45.0 },
          { sector_name: 'Financials', exposure_pct: 29.0 },
          { sector_name: 'Other', exposure_pct: 26.0 },
        ],
        regime_us: true,
        regime_uk: true,
      },
    ],
  },
};

async function mockCommonRiskDashboardRoutes(page) {
  await page.route(`${API_BASE}/portfolio`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_01) });
    } else {
      route.continue();
    }
  });
  await page.route(`${API_BASE}/positions`, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_POSITIONS) });
  });
  await page.route(`${API_BASE}/portfolio/sector-weights`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { sectors: [], total_positions: 0, concentration_alert: false } }),
    });
  });
  await page.route(`${API_BASE}/portfolio/prospective-heat*`, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) });
  });
}

async function navigateToRiskDashboard(page) {
  await page.goto('/#/RiskDashboard');
  await expect(page.locator('h1').filter({ hasText: 'Risk Dashboard' })).toBeVisible({ timeout: 15000 });
}

test('SC-SRT-01: insufficient-history state renders when fewer than 8 weeks exist', async ({ page }) => {
  await mockCommonRiskDashboardRoutes(page);
  await page.route(`${API_BASE}/portfolio/sector-regime-trend*`, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(INSUFFICIENT_HISTORY_RESPONSE) });
  });

  await navigateToRiskDashboard(page);

  await expect(page.getByText('Sector & Regime Exposure Trend')).toBeVisible({ timeout: 10000 });
  await expect(page.getByText(/not enough history yet/i)).toBeVisible({ timeout: 10000 });
  await expect(page.getByText(/8 weeks of data required; 3 available/i)).toBeVisible();
});

test('SC-SRT-02: trend chart and regime strip render when sufficient history exists', async ({ page }) => {
  await mockCommonRiskDashboardRoutes(page);
  await page.route(`${API_BASE}/portfolio/sector-regime-trend*`, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SUFFICIENT_HISTORY_RESPONSE) });
  });

  await navigateToRiskDashboard(page);

  await expect(page.getByText('Sector & Regime Exposure Trend')).toBeVisible({ timeout: 10000 });
  await expect(page.getByText(/not enough history yet/i)).toHaveCount(0);
  await expect(page.getByTestId('regime-row-regime_us')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('regime-row-regime_uk')).toBeVisible();
});

test('SC-SRT-03: error state renders on failed fetch, sibling Sector Concentration panel unaffected', async ({ page }) => {
  await mockCommonRiskDashboardRoutes(page);
  await page.route(`${API_BASE}/portfolio/sector-regime-trend*`, (route) => {
    route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ message: 'Internal server error' }) });
  });

  await navigateToRiskDashboard(page);

  await expect(page.getByText(/unable to load exposure trend/i)).toBeVisible({ timeout: 10000 });
  await expect(page.getByText('Sector Concentration')).toBeVisible();
});
