/**
 * Tax-Year P&L CSV Export — ST-13 (BLG-FEAT-69, EPIC-03, v7.0)
 *
 * The backend (GET /reports/tax-year?format=csv&year=YYYY, backend/main.py +
 * backend/services/reports_service.py build_tax_year_csv) and frontend
 * "Download CSV" button (src/pages/Reports.js) both pre-existed this sprint
 * (predate cycle 2026-07-12__release-v7.0 entirely — confirmed via git log)
 * but had zero Playwright coverage, and the button order (CSV was left of PDF)
 * diverged from the locked v7.0 design decision (CSV right of PDF) — fixed in
 * the same commit as this file. This closes both gaps: coverage for the
 * pre-met feature, and verification of the corrected button order.
 *
 * Design source: docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md
 * Spec: docs/specs/frontend/pages/reports.md §Page Header Controls, §Download CSV Button States
 *
 * Coverage:
 *   SC-CSV-01  "Download CSV" button visible, positioned right of "Download PDF"
 *   SC-CSV-02  Clicking "Download CSV" fires GET /reports/tax-year?format=csv&year=YYYY
 *              and triggers a browser download with the expected filename
 *   SC-CSV-03  Button shows "Generating…" spinner state while the request is pending
 *   SC-CSV-04  Error toast shown on failure — "CSV generation failed. Please try again."
 *   SC-CSV-05  Empty year (zero closed trades) — button still enabled, download still fires
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click
 * the "Tax Year P&L" tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const TAX_YEAR_REPORT = {
  status: 'ok',
  data: {
    tax_year_label: '2026/27',
    summary: {
      total_realised_pnl: 1250.50,
      total_gross_profit: 1800.00,
      total_gross_loss: -549.50,
      win_rate: 62.5,
      total_closed_trades: 8,
    },
    trades: [
      {
        ticker: 'AAPL', market: 'US', entry_date: '2026-05-01', exit_date: '2026-05-20',
        holding_days: 19, entry_price_native: 180.0, exit_price_native: 195.0, shares: 10,
        total_cost_gbp: 1440.0, exit_proceeds_gbp: 1560.0, realised_pnl_gbp: 120.0,
        pnl_pct: 8.33, tags: [],
      },
    ],
    estimated_unrealised_pnl: 340.0,
    unrealised_note: 'Estimated from currently open positions; not tax-year scoped.',
  },
};

const TAX_YEAR_REPORT_EMPTY = {
  status: 'ok',
  data: {
    tax_year_label: '2026/27',
    summary: { total_realised_pnl: 0, total_gross_profit: 0, total_gross_loss: 0, win_rate: 0, total_closed_trades: 0 },
    trades: [],
    estimated_unrealised_pnl: null,
    unrealised_note: '',
  },
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTaxYearReport(page, { reportData = TAX_YEAR_REPORT, csvFails = false } = {}) {
  await page.route(new RegExp(`${API}/reports/tax-year`), (route) => {
    const url = route.request().url();
    if (url.includes('format=csv')) {
      if (csvFails) {
        return route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'CSV generation failed' }) });
      }
      const csvBody = [
        'Tax Year,2026/27',
        `Total Realised P&L (GBP),${reportData.data.summary.total_realised_pnl}`,
        'Total Closed Trades,' + reportData.data.summary.total_closed_trades,
      ].join('\n');
      return route.fulfill({
        status: 200,
        contentType: 'text/csv',
        headers: { 'Content-Disposition': 'attachment; filename="tax-year-2026-pnl.csv"' },
        body: csvBody,
      });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(reportData) });
  });
}

async function gotoTaxYearTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();
  await expect(page.getByRole('button', { name: /download csv/i })).toBeVisible({ timeout: 10000 });
}

test('SC-CSV-01: "Download CSV" button visible, positioned right of "Download PDF"', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page);
  await gotoTaxYearTab(page);

  const pdfButton = page.getByRole('button', { name: /download pdf/i });
  const csvButton = page.getByRole('button', { name: /download csv/i });
  await expect(pdfButton).toBeVisible();
  await expect(csvButton).toBeVisible();

  const pdfBox = await pdfButton.boundingBox();
  const csvBox = await csvButton.boundingBox();
  expect(csvBox.x).toBeGreaterThan(pdfBox.x);
});

test('SC-CSV-02: Clicking "Download CSV" fires the format=csv request and triggers a download', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page);
  await gotoTaxYearTab(page);

  const [request, download] = await Promise.all([
    page.waitForRequest((req) => req.url().includes('/reports/tax-year') && req.url().includes('format=csv')),
    page.waitForEvent('download'),
    page.getByRole('button', { name: /download csv/i }).click(),
  ]);

  expect(request.url()).toContain('format=csv');
  expect(request.url()).toContain('year=');
  expect(download.suggestedFilename()).toMatch(/tax-year-\d{4}-pnl\.csv/);
});

test('SC-CSV-03: Button shows "Generating…" while the CSV request is pending', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/tax-year`), async (route) => {
    const url = route.request().url();
    if (url.includes('format=csv')) {
      await new Promise((r) => setTimeout(r, 800));
      return route.fulfill({ status: 200, contentType: 'text/csv', body: 'Tax Year,2026/27' });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TAX_YEAR_REPORT) });
  });
  await gotoTaxYearTab(page);

  const csvButton = page.getByRole('button', { name: /download csv/i });
  await csvButton.click();

  await expect(page.getByText('Generating…').first()).toBeVisible({ timeout: 2000 });
  await expect(page.getByText('Generating…')).toHaveCount(0, { timeout: 5000 });
});

test('SC-CSV-04: Error toast shown on CSV generation failure', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page, { csvFails: true });
  await gotoTaxYearTab(page);

  await page.getByRole('button', { name: /download csv/i }).click();

  await expect(page.getByText('CSV generation failed. Please try again.')).toBeVisible({ timeout: 5000 });
});

test('SC-CSV-05: Empty year (zero closed trades) — CSV button still enabled, download still fires', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page, { reportData: TAX_YEAR_REPORT_EMPTY });
  await gotoTaxYearTab(page);

  const csvButton = page.getByRole('button', { name: /download csv/i });
  await expect(csvButton).toBeEnabled();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    csvButton.click(),
  ]);
  expect(download.suggestedFilename()).toMatch(/tax-year-\d{4}-pnl\.csv/);
});
