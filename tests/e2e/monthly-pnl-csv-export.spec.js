/**
 * Monthly Realized P&L CSV Export — ST-05 (BLG-FEAT-81, EPIC-05, v7.8)
 *
 * Verbatim reuse of the Tax Year tab's "Download CSV" pattern (idle/
 * generating/success/error states, same visual weight, same interaction
 * model) for the Monthly P&L Report view — no new pattern invented, per
 * monthly-csv-export/ux_spec.md §2/§4.
 *
 * Design source: docs/design/2026-07-24__release-v7.8/monthly-csv-export/ux_spec.md
 * Spec: docs/specs/frontend/pages/reports.md, docs/specs/api_contracts/reports_endpoints.md §CSV Export
 *
 * Coverage:
 *   SC-MCSV-01  "Download CSV" button visible on the Monthly P&L tab
 *   SC-MCSV-02  Clicking "Download CSV" fires GET /reports/monthly-pnl?format=csv
 *               and triggers a browser download named monthly-pnl.csv
 *   SC-MCSV-03  Button shows "Generating…" spinner state while the request is pending
 *   SC-MCSV-04  Error toast shown on failure — "CSV generation failed. Please try again."
 *   SC-MCSV-05  Empty months (zero closed trades) — button still enabled, download still fires
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click
 * the "Monthly P&L" tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const MONTHLY_PNL_REPORT = {
  status: 'ok',
  data: [
    { year: 2026, month: 4, realised_pnl_gbp: 340.5, trade_count: 3 },
    { year: 2026, month: 3, realised_pnl_gbp: -120.0, trade_count: 1 },
  ],
  estimated_unrealised_pnl: 200.0,
  unrealised_note: 'Estimated from currently open positions.',
  compliance_summary: null,
};

const MONTHLY_PNL_REPORT_EMPTY = {
  status: 'ok',
  data: [],
  estimated_unrealised_pnl: null,
  unrealised_note: '',
  compliance_summary: null,
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMonthlyPnl(page, { reportData = MONTHLY_PNL_REPORT, csvFails = false } = {}) {
  await page.route(new RegExp(`${API}/reports/monthly-pnl`), (route) => {
    const url = route.request().url();
    if (url.includes('format=csv')) {
      if (csvFails) {
        return route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'CSV generation failed' }) });
      }
      const csvBody = ['Year,Month,Realised P&L (GBP),Trades']
        .concat(reportData.data.map((r) => `${r.year},${r.month},${r.realised_pnl_gbp},${r.trade_count}`))
        .join('\n');
      return route.fulfill({
        status: 200,
        contentType: 'text/csv',
        headers: { 'Content-Disposition': 'attachment; filename="monthly-pnl.csv"' },
        body: csvBody,
      });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(reportData) });
  });
}

async function gotoMonthlyTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /monthly p&l/i }).click();
  await expect(page.getByRole('button', { name: /download csv/i })).toBeVisible({ timeout: 10000 });
}

test('SC-MCSV-01: "Download CSV" button visible on the Monthly P&L tab', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page);
  await gotoMonthlyTab(page);

  await expect(page.getByRole('button', { name: /download csv/i })).toBeVisible();
});

test('SC-MCSV-02: Clicking "Download CSV" fires the format=csv request and triggers a download', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page);
  await gotoMonthlyTab(page);

  const [request, download] = await Promise.all([
    page.waitForRequest((req) => req.url().includes('/reports/monthly-pnl') && req.url().includes('format=csv')),
    page.waitForEvent('download'),
    page.getByRole('button', { name: /download csv/i }).click(),
  ]);

  expect(request.url()).toContain('format=csv');
  expect(download.suggestedFilename()).toBe('monthly-pnl.csv');
});

test('SC-MCSV-03: Button shows "Generating…" while the CSV request is pending', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/monthly-pnl`), async (route) => {
    const url = route.request().url();
    if (url.includes('format=csv')) {
      await new Promise((r) => setTimeout(r, 800));
      return route.fulfill({ status: 200, contentType: 'text/csv', body: 'Year,Month,Realised P&L (GBP),Trades' });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MONTHLY_PNL_REPORT) });
  });
  await gotoMonthlyTab(page);

  const csvButton = page.getByRole('button', { name: /download csv/i });
  await csvButton.click();

  await expect(page.getByText('Generating…').first()).toBeVisible({ timeout: 2000 });
  await expect(page.getByText('Generating…')).toHaveCount(0, { timeout: 5000 });
});

test('SC-MCSV-04: Error toast shown on CSV generation failure', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, { csvFails: true });
  await gotoMonthlyTab(page);

  await page.getByRole('button', { name: /download csv/i }).click();

  await expect(page.getByText('CSV generation failed. Please try again.')).toBeVisible({ timeout: 5000 });
});

test('SC-MCSV-05: Empty months (zero closed trades) — CSV button still enabled, download still fires', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, { reportData: MONTHLY_PNL_REPORT_EMPTY });
  await gotoMonthlyTab(page);

  const csvButton = page.getByRole('button', { name: /download csv/i });
  await expect(csvButton).toBeEnabled();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    csvButton.click(),
  ]);
  expect(download.suggestedFilename()).toBe('monthly-pnl.csv');
});
