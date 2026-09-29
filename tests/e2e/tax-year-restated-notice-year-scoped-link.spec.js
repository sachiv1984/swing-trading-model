/**
 * Tax Year restated-months notice links to a Monthly view that actually shows the
 * counted months — ST-03 (BLG-FE-190, EPIC-01, v9.8)
 *
 * Design source: docs/design/2026-09-28__release-v9.8/tax-year-restated-notice-year-scoped-link/decision_record.md
 * Spec: docs/specs/frontend/pages/reports.md §Monthly Financial Table Tax Year Filter (v0.20)
 *       + §Summary Bar Restated-months notice (v0.20)
 * API contract: docs/specs/api_contracts/reports_endpoints.md v0.14 §GET /reports/monthly-pnl (year param)
 *
 * Coverage:
 *   SC-TYL-01  Older-tax-year case (the story's own AC): selecting a non-current tax year with
 *              >=1 restated month and clicking the notice link lands on the Monthly tab with its
 *              Tax Year filter pre-set to that year, showing the months the notice counted.
 *   SC-TYL-02  Direct tab navigation (not via the notice link) still defaults the Monthly tab's
 *              Tax Year filter to the current tax year — even after a prior notice-link visit.
 *   SC-TYL-03  Changing the Monthly tab's own Tax Year filter re-fetches GET /reports/monthly-pnl
 *              with the new year and re-renders the table.
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click the
 * relevant tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

function getCurrentUKTaxYear() {
  const today = new Date();
  const year = today.getFullYear();
  const taxYearStart = new Date(year, 3, 6); // April 6
  return today >= taxYearStart ? year : year - 1;
}

const CURRENT_TAX_YEAR = getCurrentUKTaxYear();
const OLDER_TAX_YEAR = CURRENT_TAX_YEAR - 2;

function taxYearReportResponse({ restatedMonthCount = 0 } = {}) {
  return {
    status: 'ok',
    data: {
      tax_year_label: `${OLDER_TAX_YEAR}/${String(OLDER_TAX_YEAR + 1).slice(2)}`,
      summary: {
        total_realised_pnl: 0, total_gross_profit: 0, total_gross_loss: 0,
        win_rate: 0, total_closed_trades: 0, restated_month_count: restatedMonthCount,
      },
      trades: [],
      estimated_unrealised_pnl: 0,
      unrealised_note: null,
    },
  };
}

function monthlyPnlResponse(months) {
  return { status: 'ok', data: months, estimated_unrealised_pnl: null, unrealised_note: null, compliance_summary: null };
}

// Distinct, easily-asserted-on month rows per tax year, so a test can prove which
// year's data actually rendered.
const OLDER_YEAR_MONTH = {
  year: OLDER_TAX_YEAR + 1, month: 1, realised_pnl_gbp: 777, trade_count: 2, null_fee_trade_count: 0,
  snapshotted: true, restated: true, snapshot_realised_pnl_gbp: 750, restated_diff_gbp: 27,
};
const CURRENT_YEAR_MONTH = {
  year: CURRENT_TAX_YEAR, month: 9, realised_pnl_gbp: 111, trade_count: 1, null_fee_trade_count: 0,
  snapshotted: false, restated: false, snapshot_realised_pnl_gbp: null, restated_diff_gbp: null,
};

async function setupPage(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  await page.route(new RegExp(`${API}/reports/tax-year(?!\\?format=csv)`), (route) => {
    const url = new URL(route.request().url());
    const year = Number(url.searchParams.get('year'));
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(taxYearReportResponse({ restatedMonthCount: year === OLDER_TAX_YEAR ? 1 : 0 })),
    });
  });

  // Year-aware mock: /reports/monthly-pnl?year=<n> returns different rows per year,
  // so a test can prove the filter genuinely re-scoped the fetch (not just always the same data).
  await page.route(new RegExp(`${API}/reports/monthly-pnl(?!\\?format=csv)`), (route) => {
    const url = new URL(route.request().url());
    const year = Number(url.searchParams.get('year'));
    const months = year === OLDER_TAX_YEAR ? [OLDER_YEAR_MONTH] : [CURRENT_YEAR_MONTH];
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(monthlyPnlResponse(months)) });
  });

  await page.goto('/#/Reports');
}

test('SC-TYL-01: selecting an older tax year and clicking the restated-months notice link lands on the Monthly tab filtered to that year', async ({ page }) => {
  await setupPage(page);
  await page.getByRole('button', { name: /tax year p&l/i }).click();

  // Select the older tax year (>=1 restated month per the mock above).
  await page.locator('button[role="combobox"]').first().click();
  await page.getByRole('option', { name: `${OLDER_TAX_YEAR}/${String(OLDER_TAX_YEAR + 1).slice(2)}` }).click();

  const notice = page.getByTestId('taxyear-restated-notice');
  await expect(notice).toBeVisible({ timeout: 8000 });
  await expect(notice).toContainText('Includes 1 restated month — see the Monthly tab for details.');

  await notice.getByRole('button', { name: 'Monthly tab' }).click();
  await expect(page.getByText('Monthly P&L Report')).toBeVisible();

  // The Monthly tab's own Tax Year filter reflects the year the notice was shown for.
  await expect(page.getByTestId('monthly-tax-year-filter')).toContainText(
    `${OLDER_TAX_YEAR}/${String(OLDER_TAX_YEAR + 1).slice(2)}`
  );

  // The month(s) the notice counted are visible in the rendered table — not the
  // current-tax-year row, which is a different, distinguishable dataset.
  await expect(page.getByText('£777.00')).toBeVisible();
  await expect(page.getByText('£111.00')).toHaveCount(0);
});

test('SC-TYL-02: direct navigation to the Monthly tab still defaults to the current tax year, even after a prior notice-link visit', async ({ page }) => {
  await setupPage(page);
  await page.getByRole('button', { name: /tax year p&l/i }).click();
  await page.locator('button[role="combobox"]').first().click();
  await page.getByRole('option', { name: `${OLDER_TAX_YEAR}/${String(OLDER_TAX_YEAR + 1).slice(2)}` }).click();
  await page.getByTestId('taxyear-restated-notice').getByRole('button', { name: 'Monthly tab' }).click();
  await expect(page.getByTestId('monthly-tax-year-filter')).toContainText(String(OLDER_TAX_YEAR));

  // Now navigate away and back to Monthly via the plain tab button (not the notice link).
  await page.getByRole('button', { name: /^performance$/i }).click();
  await page.getByRole('button', { name: /monthly p&l/i }).click();

  await expect(page.getByTestId('monthly-tax-year-filter')).toContainText(
    `${CURRENT_TAX_YEAR}/${String(CURRENT_TAX_YEAR + 1).slice(2)}`
  );
  await expect(page.getByTestId('monthly-realised-pnl-cell')).toContainText('£111.00');
});

test('SC-TYL-03: changing the Monthly tab Tax Year filter re-fetches and re-renders for the new year', async ({ page }) => {
  await setupPage(page);
  await page.getByRole('button', { name: /monthly p&l/i }).click();
  await expect(page.getByTestId('monthly-realised-pnl-cell')).toContainText('£111.00', { timeout: 8000 });

  await page.getByTestId('monthly-tax-year-filter').click();
  await page.getByRole('option', { name: `${OLDER_TAX_YEAR}/${String(OLDER_TAX_YEAR + 1).slice(2)}` }).click();

  await expect(page.getByText('£777.00')).toBeVisible();
  await expect(page.getByText('£111.00')).toHaveCount(0);
});
