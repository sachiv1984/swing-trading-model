/**
 * Realised P&L Exact-Zero Colour Convention — ST-08 (BLG-FE-144, EPIC-03, v8.5)
 *
 * DEV-REPORTS-ST01-02 found the Tax Year Trades Table (`TaxYearReport`) and
 * the Monthly Financial Table (`MonthlyPnlTable`) disagreed on how to colour
 * an exactly-zero Realised P&L: the Tax Year table used a binary rule
 * (`pnl > 0 ? emerald : rose`, so zero rendered red like a loss); the
 * Monthly table already used a three-way rule (grey/neutral for exactly
 * zero). Design Gate decision (docs/design/2026-08-08__release-v8.5/
 * exact-zero-pnl-colour-convention/decision_record.md): converge both
 * tables on grey/neutral-for-zero — a breakeven trade is not a loss.
 *
 * Spec: docs/specs/frontend/pages/reports.md v0.16 §Realised P&L (both tables)
 *
 * Coverage:
 *   SC-RPZ-01  Tax Year table: positive Realised P&L renders emerald
 *   SC-RPZ-02  Tax Year table: negative Realised P&L renders rose
 *   SC-RPZ-03  Tax Year table: exactly-zero Realised P&L renders neutral
 *              (text-slate-600/text-slate-400), NOT rose — this is the AC
 *              this story exists to fix (was red before this story)
 *   SC-RPZ-04  Monthly table: exactly-zero Realised P&L renders neutral
 *              (unchanged behaviour — confirms no regression to the
 *              already-correct table while fixing the other one)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then
 * click the relevant tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

function taxYearTrade(overrides) {
  return {
    ticker: 'AAPL', market: 'US', entry_date: '2026-05-01', exit_date: '2026-05-20',
    holding_days: 19, entry_price_native: 180.0, exit_price_native: 195.0, shares: 10,
    total_cost_gbp: 1440.0, exit_proceeds_gbp: 1560.0, realised_pnl_gbp: 120.0,
    pnl_pct: 8.33, tags: [],
    ...overrides,
  };
}

function taxYearReportResponse(trades) {
  return {
    status: 'ok',
    data: {
      tax_year_label: '2026/27',
      summary: {
        total_realised_pnl: 0, total_gross_profit: 0, total_gross_loss: 0,
        win_rate: 0, total_closed_trades: trades.length,
      },
      trades,
      estimated_unrealised_pnl: 0,
      unrealised_note: null,
    },
  };
}

function monthlyPnlResponse(months) {
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

test('SC-RPZ-01: Tax Year table — positive Realised P&L renders emerald', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/tax-year(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(taxYearReportResponse([taxYearTrade({ realised_pnl_gbp: 120.0 })])) })
  );
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();

  const cell = page.getByTestId('tax-year-realised-pnl-cell');
  await expect(cell).toBeVisible({ timeout: 8000 });
  await expect(cell).toHaveClass(/text-emerald-400/);
  await expect(cell).not.toHaveClass(/text-rose-400/);
});

test('SC-RPZ-02: Tax Year table — negative Realised P&L renders rose', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/tax-year(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(taxYearReportResponse([taxYearTrade({ realised_pnl_gbp: -50.0 })])) })
  );
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();

  const cell = page.getByTestId('tax-year-realised-pnl-cell');
  await expect(cell).toBeVisible({ timeout: 8000 });
  await expect(cell).toHaveClass(/text-rose-400/);
  await expect(cell).not.toHaveClass(/text-emerald-400/);
});

test('SC-RPZ-03: Tax Year table — exactly-zero Realised P&L renders neutral, not rose (DEV-REPORTS-ST01-02)', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/tax-year(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(taxYearReportResponse([taxYearTrade({ realised_pnl_gbp: 0 })])) })
  );
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();

  const cell = page.getByTestId('tax-year-realised-pnl-cell');
  await expect(cell).toBeVisible({ timeout: 8000 });
  await expect(cell).not.toHaveClass(/text-rose-400/);
  await expect(cell).not.toHaveClass(/text-emerald-400/);
  await expect(cell).toHaveClass(/text-slate-600/);
});

test('SC-RPZ-04: Monthly table — exactly-zero Realised P&L renders neutral (no regression)', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/monthly-pnl(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(monthlyPnlResponse([{ year: 2026, month: 7, realised_pnl_gbp: 0, trade_count: 0 }])) })
  );
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /monthly p&l/i }).click();

  const cell = page.getByTestId('monthly-realised-pnl-cell');
  await expect(cell).toBeVisible({ timeout: 8000 });
  await expect(cell).not.toHaveClass(/text-rose-400/);
  await expect(cell).not.toHaveClass(/text-emerald-400/);
  await expect(cell).toHaveClass(/text-slate-600/);
});
