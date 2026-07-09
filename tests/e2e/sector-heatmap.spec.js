/**
 * Sector Concentration Heat Map — ST-06 (EPIC-03, v6.1)
 *
 * Covers:
 *   SC-SHM-01: Sector tiles render on Risk Dashboard with correct data
 *   SC-SHM-02: Concentration alert badge appears when ≥40% in one sector
 *   SC-SHM-03: Empty state when no open positions
 *   SC-SHM-04: Component hides silently on API error (no cascade)
 *
 * Infrastructure: Playwright page.route() network interception.
 * HashRouter note: use page.goto('/#/RiskDashboard') — NOT page.goto('/risk-dashboard').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API_BASE = 'http://localhost:8000';

const SECTOR_WEIGHTS_WITH_ALERT = {
  status: 'ok',
  data: {
    sectors: [
      { sector_name: 'Technology', position_count: 3, exposure_pct: 42.5 },
      { sector_name: 'Financials', position_count: 2, exposure_pct: 31.0 },
      { sector_name: 'Healthcare', position_count: 1, exposure_pct: 18.2 },
      { sector_name: 'Industrials', position_count: 1, exposure_pct: 8.3 },
    ],
    total_positions: 7,
    concentration_alert: true,
  },
};

const SECTOR_WEIGHTS_NO_ALERT = {
  status: 'ok',
  data: {
    sectors: [
      { sector_name: 'Technology', position_count: 2, exposure_pct: 35.0 },
      { sector_name: 'Financials', position_count: 2, exposure_pct: 35.0 },
      { sector_name: 'Healthcare', position_count: 1, exposure_pct: 30.0 },
    ],
    total_positions: 5,
    concentration_alert: false,
  },
};

const SECTOR_WEIGHTS_EMPTY = {
  status: 'ok',
  data: { sectors: [], total_positions: 0, concentration_alert: false },
};

async function mockPortfolioOk(page) {
  await page.route(`${API_BASE}/portfolio`, async (route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { positions: [], portfolio_heat_percent: 0, current_drawdown_percent: 0, peak_portfolio_value: 0 } }),
      });
    } else {
      await route.continue();
    }
  });
  await page.route(`${API_BASE}/positions`, async (route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) });
  });
}

async function mockSectorWeights(page, response) {
  await page.route(`${API_BASE}/portfolio/sector-weights`, async (route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(response) });
  });
}

async function mockSectorWeightsError(page) {
  await page.route(`${API_BASE}/portfolio/sector-weights`, async (route) => {
    await route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ message: 'error' }) });
  });
}

async function navigateToRiskDashboard(page) {
  await page.goto('/#/RiskDashboard');
  await expect(page.locator('h1').filter({ hasText: 'Risk Dashboard' })).toBeVisible({ timeout: 15000 });
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 15000 });
}

test.describe('Sector Concentration Heat Map', () => {
  test('SC-SHM-01: Sector tiles render with correct sector names and exposure percentages', async ({ page }) => {
    await mockPortfolioOk(page);
    await mockSectorWeights(page, SECTOR_WEIGHTS_NO_ALERT);
    await navigateToRiskDashboard(page);

    await expect(page.getByText('Sector Concentration')).toBeVisible({ timeout: 8000 });

    const techTile = page.locator('[data-testid="sector-tile"][data-sector="Technology"]');
    await expect(techTile).toContainText('Technology');
    await expect(techTile).toContainText('35.0%');
    await expect(techTile).toContainText('2 positions');

    const financialsTile = page.locator('[data-testid="sector-tile"][data-sector="Financials"]');
    await expect(financialsTile).toContainText('Financials');
    await expect(financialsTile).toContainText('35.0%');
    await expect(financialsTile).toContainText('2 positions');

    const healthcareTile = page.locator('[data-testid="sector-tile"][data-sector="Healthcare"]');
    await expect(healthcareTile).toContainText('Healthcare');
    await expect(healthcareTile).toContainText('30.0%');
    await expect(healthcareTile).toContainText('1 position');
  });

  test('SC-SHM-02: Concentration alert badge visible when a sector reaches ≥40%', async ({ page }) => {
    await mockPortfolioOk(page);
    await mockSectorWeights(page, SECTOR_WEIGHTS_WITH_ALERT);
    await navigateToRiskDashboard(page);

    await expect(page.getByText('Sector Concentration')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('Concentration Alert')).toBeVisible();
    await expect(page.getByText('Technology')).toBeVisible();
    await expect(page.getByText('42.5%')).toBeVisible();
  });

  test('SC-SHM-03: Empty state renders when there are no open positions', async ({ page }) => {
    await mockPortfolioOk(page);
    await mockSectorWeights(page, SECTOR_WEIGHTS_EMPTY);
    await navigateToRiskDashboard(page);

    await expect(page.getByText('Sector Concentration')).toBeVisible({ timeout: 8000 });
    // Exact text (SectorHeatMap.js: "No open positions.") — the page also has an
    // unrelated "No open positions to display." message elsewhere.
    await expect(page.getByText('No open positions.', { exact: true })).toBeVisible();
    await expect(page.getByText('Concentration Alert')).not.toBeVisible();
  });

  test('SC-SHM-04: Component hides silently on API error — no error cascade to Risk Dashboard', async ({ page }) => {
    await mockPortfolioOk(page);
    await mockSectorWeightsError(page);
    await navigateToRiskDashboard(page);

    // Risk Dashboard heading must still be visible (no cascade)
    await expect(page.locator('h1').filter({ hasText: 'Risk Dashboard' })).toBeVisible({ timeout: 8000 });
    // Sector Concentration section should not appear
    await expect(page.getByText('Sector Concentration')).not.toBeVisible();
  });
});
