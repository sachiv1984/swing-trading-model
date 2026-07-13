/**
 * Realized vs. Unrealized Gain Distinction — Monthly P&L — ST-14 (BLG-FEAT-70, EPIC-03, v7.0)
 *
 * Design source: docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md
 * Spec: docs/specs/frontend/pages/reports.md §Unrealised P&L Card (v7.0 — ST-14)
 *
 * Coverage:
 *   SC-MRU-01  Unrealised P&L Card shown below the Monthly Financial Table when
 *              estimated_unrealised_pnl is present
 *   SC-MRU-02  Combined Total line = sum(displayed months' realised_pnl_gbp) + estimated_unrealised_pnl
 *   SC-MRU-03  Positive unrealised P&L renders emerald; negative renders rose
 *   SC-MRU-04  Card absent when estimated_unrealised_pnl is null (no portfolio yet)
 *   SC-MRU-05  Monthly Financial Table rows unchanged — still realised-only per row (AC regression)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click
 * the "Monthly P&L" tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

function monthlyPnlResponse({ months = [], estimatedUnrealisedPnl = 340.50, unrealisedNote = 'Reflects current open positions; indicative only.' } = {}) {
  return {
    status: 'ok',
    data: months,
    estimated_unrealised_pnl: estimatedUnrealisedPnl,
    unrealised_note: unrealisedNote,
    compliance_summary: null,
  };
}

const MONTHS = [
  { year: 2026, month: 7, realised_pnl_gbp: 250.00, trade_count: 3 },
  { year: 2026, month: 6, realised_pnl_gbp: -80.50, trade_count: 2 },
];

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMonthlyPnl(page, response) {
  await page.route(new RegExp(`${API}/reports/monthly-pnl`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(response) })
  );
}

async function gotoMonthlyTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /monthly p&l/i }).click();
}

test('SC-MRU-01: Unrealised P&L Card shown below the Monthly Financial Table', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, monthlyPnlResponse({ months: MONTHS }));
  await gotoMonthlyTab(page);

  const card = page.getByTestId('monthly-unrealised-pnl-card');
  await expect(card).toBeVisible({ timeout: 8000 });
  await expect(card.getByText('Indicative Unrealised P&L (current positions)')).toBeVisible();
  await expect(card).toContainText('£340.50');
});

test('SC-MRU-02: Combined Total line sums displayed months + estimated unrealised P&L', async ({ page }) => {
  await mockFallback(page);
  // 250.00 + (-80.50) = 169.50 realised; + 340.50 unrealised = 510.00
  await mockMonthlyPnl(page, monthlyPnlResponse({ months: MONTHS, estimatedUnrealisedPnl: 340.50 }));
  await gotoMonthlyTab(page);

  const total = page.getByTestId('monthly-combined-total');
  await expect(total).toBeVisible({ timeout: 8000 });
  await expect(total).toContainText('Total (Realised + Unrealised)');
  await expect(total).toContainText('£510.00');
});

test('SC-MRU-03: Positive unrealised P&L renders emerald; negative renders rose', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, monthlyPnlResponse({ months: MONTHS, estimatedUnrealisedPnl: 340.50 }));
  await gotoMonthlyTab(page);

  const positiveFigure = page.getByTestId('monthly-unrealised-pnl-card').locator('p.text-2xl');
  await expect(positiveFigure).toHaveClass(/text-emerald-400/);

  await mockMonthlyPnl(page, monthlyPnlResponse({ months: MONTHS, estimatedUnrealisedPnl: -120.00 }));
  await page.reload();
  await page.getByRole('button', { name: /monthly p&l/i }).click();

  const negativeFigure = page.getByTestId('monthly-unrealised-pnl-card').locator('p.text-2xl');
  await expect(negativeFigure).toHaveClass(/text-rose-400/);
});

test('SC-MRU-04: Card absent when estimated_unrealised_pnl is null', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, monthlyPnlResponse({ months: MONTHS, estimatedUnrealisedPnl: null }));
  await gotoMonthlyTab(page);

  await expect(page.getByTestId('monthly-unrealised-pnl-card')).not.toBeVisible({ timeout: 5000 });
});

test('SC-MRU-05: Monthly Financial Table rows remain realised-only (regression)', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, monthlyPnlResponse({ months: MONTHS }));
  await gotoMonthlyTab(page);

  await expect(page.getByText('July 2026')).toBeVisible({ timeout: 8000 });
  await expect(page.getByText('£250.00').first()).toBeVisible();
  // Table row P&L values must not include the unrealised figure (£340.50 appears only in the card)
  const table = page.locator('table');
  await expect(table).not.toContainText('£340.50');
});
