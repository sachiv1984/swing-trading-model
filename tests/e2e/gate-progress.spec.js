/**
 * Trade Gate Proximity Indicator — ST-07 (EPIC-03, v6.1)
 *
 * Covers:
 *   SC-GP-01: Gate progress strip renders below session-summary cards on Dashboard
 *   SC-GP-02: Shows "{N}/20 closed trades · {M} more to unlock quality insights" with progress bar
 *   SC-GP-03: "Quality insights unlocked ✓" shown when gate is met
 *   SC-GP-04: Component hides silently on API error
 *
 * Infrastructure: Playwright page.route() network interception.
 * HashRouter note: use page.goto('/') (root maps to DashboardHome).
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API_BASE = 'http://localhost:8000';

const GATE_IN_PROGRESS = {
  status: 'ok',
  data: {
    closed_trades_count: 12,
    closed_trades_with_plans: 5,
    active_positions_count: 3,
    ai_journal_entry_count: null,
    oldest_trade_date: '2024-01-15',
    newest_trade_date: '2025-11-30',
  },
};

const GATE_MET = {
  status: 'ok',
  data: {
    closed_trades_count: 23,
    closed_trades_with_plans: 18,
    active_positions_count: 2,
    ai_journal_entry_count: null,
    oldest_trade_date: '2024-01-15',
    newest_trade_date: '2026-05-20',
  },
};

async function mockGateMetrics(page, response) {
  await page.route(`${API_BASE}/portfolio/gate-metrics`, async (route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(response) });
  });
}

async function mockGateMetricsError(page) {
  await page.route(`${API_BASE}/portfolio/gate-metrics`, async (route) => {
    await route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ message: 'error' }) });
  });
}

async function navigateToDashboard(page) {
  await page.goto('/');
  await expect(page.locator('h1').filter({ hasText: 'Dashboard' })).toBeVisible({ timeout: 15000 });
}

test.describe('Trade Gate Proximity Indicator', () => {
  test('SC-GP-01: Gate progress strip is present on Dashboard homepage', async ({ page }) => {
    await mockGateMetrics(page, GATE_IN_PROGRESS);
    await navigateToDashboard(page);

    await expect(page.getByTestId('gate-progress-strip')).toBeVisible({ timeout: 8000 });
  });

  test('SC-GP-02: Strip shows closed trade count, threshold, and gate label', async ({ page }) => {
    await mockGateMetrics(page, GATE_IN_PROGRESS);
    await navigateToDashboard(page);

    // Current shipped copy (GateProgressStrip.js): "{closed}/{threshold} closed
    // trades · {remaining} more to unlock quality insights" — the "PT-04/SI-02
    // gate" internal code name is not surfaced to end users. Spec
    // (dashboard.md §6) is stale relative to this; see BLG-SPEC-73.
    await expect(page.getByText(/12\/20 closed trades/i)).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/more to unlock quality insights/i)).toBeVisible();
  });

  test('SC-GP-03: "Quality insights unlocked" shown when closed trades meet or exceed threshold', async ({ page }) => {
    await mockGateMetrics(page, GATE_MET);
    await navigateToDashboard(page);

    await expect(page.getByTestId('gate-progress-strip')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/quality insights unlocked/i)).toBeVisible();
  });

  test('SC-GP-04: Component hides silently on API error — Dashboard remains usable', async ({ page }) => {
    await mockGateMetricsError(page);
    await navigateToDashboard(page);

    await expect(page.locator('h1').filter({ hasText: 'Dashboard' })).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('gate-progress-strip')).not.toBeVisible();
  });
});
