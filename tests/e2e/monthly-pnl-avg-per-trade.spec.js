/**
 * Avg P&L/Trade column — Monthly P&L Report — ST-01 (BLG-FE-141, EPIC-01, v8.4)
 *
 * Design source: docs/design/2026-08-07__release-v8.4/avg-pnl-per-trade-column/decision_record.md
 * Spec: docs/specs/frontend/pages/reports.md §Monthly Financial Table (v0.14 — ST-01)
 *
 * Coverage:
 *   SC-MAPT-01  Avg P&L/Trade column renders in the Monthly Financial Table header
 *   SC-MAPT-02  Column value = realised_pnl_gbp / trade_count, GBP, 2dp
 *   SC-MAPT-03  Positive average renders emerald; negative renders rose
 *   SC-MAPT-04  Zero-trade month renders "—" (no colour), not a fabricated £0.00
 *   SC-MAPT-05  Monthly CSV export column set unchanged — Avg P&L/Trade excluded (AC regression)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click
 * the "Monthly P&L" tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

function monthlyPnlResponse({ months = [] } = {}) {
  return {
    status: 'ok',
    data: months,
    estimated_unrealised_pnl: null,
    unrealised_note: null,
    compliance_summary: null,
  };
}

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMonthlyPnl(page, response) {
  await page.route(new RegExp(`${API}/reports/monthly-pnl(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(response) })
  );
}

async function gotoMonthlyTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /monthly p&l/i }).click();
}

test('SC-MAPT-01: Avg P&L/Trade column header renders in the Monthly Financial Table', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, monthlyPnlResponse({
    months: [{ year: 2026, month: 7, realised_pnl_gbp: 250.00, trade_count: 4 }],
  }));
  await gotoMonthlyTab(page);

  await expect(page.getByTestId('monthly-avg-pnl-header')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-avg-pnl-header')).toHaveText('Avg P&L/Trade');
});

test('SC-MAPT-02: Avg P&L/Trade value = realised_pnl_gbp / trade_count, 2dp', async ({ page }) => {
  await mockFallback(page);
  // 250.00 / 4 = 62.50
  await mockMonthlyPnl(page, monthlyPnlResponse({
    months: [{ year: 2026, month: 7, realised_pnl_gbp: 250.00, trade_count: 4 }],
  }));
  await gotoMonthlyTab(page);

  await expect(page.getByTestId('monthly-avg-pnl-cell')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-avg-pnl-cell')).toHaveText('£62.50');
});

test('SC-MAPT-03: Positive average renders emerald; negative renders rose', async ({ page }) => {
  await mockFallback(page);
  // -80.50 / 2 = -40.25
  await mockMonthlyPnl(page, monthlyPnlResponse({
    months: [
      { year: 2026, month: 7, realised_pnl_gbp: 250.00, trade_count: 4 },
      { year: 2026, month: 6, realised_pnl_gbp: -80.50, trade_count: 2 },
    ],
  }));
  await gotoMonthlyTab(page);

  const cells = page.getByTestId('monthly-avg-pnl-cell');
  await expect(cells.first()).toBeVisible({ timeout: 8000 });
  await expect(cells.nth(0)).toHaveClass(/text-emerald-400/);
  await expect(cells.nth(1)).toHaveClass(/text-rose-400/);
});

test('SC-MAPT-04: Zero-trade month renders "—" with no colour, not £0.00', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, monthlyPnlResponse({
    months: [{ year: 2026, month: 7, realised_pnl_gbp: 0, trade_count: 0 }],
  }));
  await gotoMonthlyTab(page);

  const cell = page.getByTestId('monthly-avg-pnl-cell');
  await expect(cell).toBeVisible({ timeout: 8000 });
  await expect(cell).toHaveText('—');
  await expect(cell).not.toContainText('£0.00');
  await expect(cell).not.toHaveClass(/text-emerald-400/);
  await expect(cell).not.toHaveClass(/text-rose-400/);
});

test('SC-MAPT-05: Monthly CSV export column set unchanged — Avg P&L/Trade excluded (regression)', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, monthlyPnlResponse({
    months: [{ year: 2026, month: 7, realised_pnl_gbp: 250.00, trade_count: 4 }],
  }));

  let csvRequestUrl = null;
  await page.route(new RegExp(`${API}/reports/monthly-pnl\\?format=csv`), (route) => {
    csvRequestUrl = route.request().url();
    route.fulfill({
      status: 200,
      contentType: 'text/csv',
      headers: { 'content-disposition': 'attachment; filename="monthly-pnl.csv"' },
      body: 'Year,Month,Realised P&L (GBP),Trades\n2026,7,250.00,4\n',
    });
  });

  await gotoMonthlyTab(page);
  await expect(page.getByTestId('monthly-avg-pnl-cell')).toBeVisible({ timeout: 8000 });

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: /download csv/i }).click(),
  ]);

  expect(csvRequestUrl).toContain('/reports/monthly-pnl');
  expect(csvRequestUrl).toContain('format=csv');
  expect(download.suggestedFilename()).toBe('monthly-pnl.csv');
});
