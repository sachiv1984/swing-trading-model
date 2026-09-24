/**
 * Month-end restatement surfacing — Monthly P&L + Tax Year summary — ST-04 (BLG-FE-188, EPIC-02, v9.7)
 *
 * Design source: docs/design/2026-09-23__release-v9.7/monthly-pnl-restatement-surfacing/decision_record.md
 * Spec: docs/specs/frontend/pages/reports.md §Monthly Restatement Marker + §Summary Bar (v0.19 — ST-04)
 * Data contract: docs/specs/api_contracts/reports_endpoints.md v0.13 — flat per-month fields
 * `snapshotted` / `restated` / `snapshot_realised_pnl_gbp` / `restated_diff_gbp` (no nested object, no
 * snapshot trade-count field); `summary.restated_month_count` on the tax-year report.
 *
 * Coverage:
 *   SC-MPR-01  "Restated" marker shows only on months with restated = true
 *   SC-MPR-02  Detail row is collapsed by default, expands/collapses on click and via the keyboard
 *   SC-MPR-03  Detail row shows As reviewed / Now / Change with signed, toned values
 *   SC-MPR-04  Trade-count-only fallback line shows when restated = true and restated_diff_gbp = 0 — and only then
 *   SC-MPR-05  "Restatement check unavailable." shows only when the rows carry no snapshot fields
 *   SC-MPR-06  Tax Year summary notice shows when restated_month_count >= 1 and links to the Monthly tab
 *   SC-MPR-07  Tax Year summary notice is absent when restated_month_count = 0
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click the relevant tab
 * (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// May 2026: restated upward (+£25.00). April 2026: restated downward (−£40.00).
// March 2026: closed, snapshotted, not restated. June 2026: in-progress month — never snapshotted.
const RESTATED_UP = {
  year: 2026, month: 5, realised_pnl_gbp: 175, trade_count: 4, null_fee_trade_count: 0,
  snapshotted: true, restated: true, snapshot_realised_pnl_gbp: 150, restated_diff_gbp: 25,
};
const RESTATED_DOWN = {
  year: 2026, month: 4, realised_pnl_gbp: 60, trade_count: 3, null_fee_trade_count: 0,
  snapshotted: true, restated: true, snapshot_realised_pnl_gbp: 100, restated_diff_gbp: -40,
};
const RESTATED_TRADE_COUNT_ONLY = {
  year: 2026, month: 2, realised_pnl_gbp: 80, trade_count: 5, null_fee_trade_count: 0,
  snapshotted: true, restated: true, snapshot_realised_pnl_gbp: 80, restated_diff_gbp: 0,
};
const NOT_RESTATED = {
  year: 2026, month: 3, realised_pnl_gbp: 90, trade_count: 2, null_fee_trade_count: 0,
  snapshotted: true, restated: false, snapshot_realised_pnl_gbp: 90, restated_diff_gbp: 0,
};
const IN_PROGRESS = {
  year: 2026, month: 6, realised_pnl_gbp: 30, trade_count: 1, null_fee_trade_count: 0,
  snapshotted: false, restated: false, snapshot_realised_pnl_gbp: null, restated_diff_gbp: null,
};

function monthlyPnlResponse(months) {
  return { status: 'ok', data: months, estimated_unrealised_pnl: null, unrealised_note: null, compliance_summary: null };
}

function taxYearReportResponse(restatedMonthCount) {
  return {
    status: 'ok',
    data: {
      tax_year_label: '2026/27',
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

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMonthlyPnl(page, months) {
  await page.route(new RegExp(`${API}/reports/monthly-pnl(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(monthlyPnlResponse(months)) })
  );
}

async function mockTaxYear(page, restatedMonthCount) {
  await page.route(new RegExp(`${API}/reports/tax-year(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(taxYearReportResponse(restatedMonthCount)) })
  );
}

async function gotoMonthlyTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /monthly p&l/i }).click();
}

test('SC-MPR-01: "Restated" marker shows only on months with restated = true', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [IN_PROGRESS, RESTATED_UP, RESTATED_DOWN, NOT_RESTATED]);
  await gotoMonthlyTab(page);

  await expect(page.getByRole('row', { name: /May 2026/ }).getByTestId('monthly-restated-marker')).toBeVisible({ timeout: 8000 });
  await expect(page.getByRole('row', { name: /April 2026/ }).getByTestId('monthly-restated-marker')).toBeVisible();
  await expect(page.getByRole('row', { name: /March 2026/ }).getByTestId('monthly-restated-marker')).toHaveCount(0);
  // The in-progress month has no snapshot and never shows a marker.
  await expect(page.getByRole('row', { name: /June 2026/ }).getByTestId('monthly-restated-marker')).toHaveCount(0);
  await expect(page.getByTestId('monthly-restated-marker')).toHaveCount(2);
  await expect(page.getByTestId('monthly-restated-marker').first()).toContainText('Restated');
});

test('SC-MPR-02: detail row is collapsed by default and expands/collapses on click and keyboard', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [RESTATED_UP, NOT_RESTATED]);
  await gotoMonthlyTab(page);

  const marker = page.getByTestId('monthly-restated-marker');
  await expect(marker).toBeVisible({ timeout: 8000 });
  await expect(marker).toHaveAttribute('aria-expanded', 'false');
  await expect(page.getByTestId('monthly-restatement-detail')).toHaveCount(0);

  await marker.click();
  await expect(marker).toHaveAttribute('aria-expanded', 'true');
  await expect(page.getByTestId('monthly-restatement-detail')).toBeVisible();

  await marker.click();
  await expect(marker).toHaveAttribute('aria-expanded', 'false');
  await expect(page.getByTestId('monthly-restatement-detail')).toHaveCount(0);

  // Keyboard-operable: focus + Enter toggles, focus + Space toggles back.
  await marker.focus();
  await page.keyboard.press('Enter');
  await expect(page.getByTestId('monthly-restatement-detail')).toBeVisible();
  await page.keyboard.press('Space');
  await expect(page.getByTestId('monthly-restatement-detail')).toHaveCount(0);
});

test('SC-MPR-03: detail row shows As reviewed / Now / Change with signed, toned values', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [RESTATED_UP, RESTATED_DOWN]);
  await gotoMonthlyTab(page);

  await page.getByRole('row', { name: /May 2026/ }).getByTestId('monthly-restated-marker').click();
  await page.getByRole('row', { name: /April 2026/ }).getByTestId('monthly-restated-marker').click();

  const details = page.getByTestId('monthly-restatement-detail');
  await expect(details).toHaveCount(2);
  const [up, down] = [details.nth(0), details.nth(1)]; // rows render in the order the API returned them

  await expect(up.getByTestId('monthly-restatement-as-reviewed')).toHaveText('£150.00');
  await expect(up.getByTestId('monthly-restatement-now')).toHaveText('£175.00');
  await expect(up.getByTestId('monthly-restatement-change')).toHaveText('+£25.00');
  await expect(up.getByTestId('monthly-restatement-change')).toHaveClass(/text-emerald-400/);

  await expect(down.getByTestId('monthly-restatement-as-reviewed')).toHaveText('£100.00');
  await expect(down.getByTestId('monthly-restatement-now')).toHaveText('£60.00');
  await expect(down.getByTestId('monthly-restatement-change')).toHaveText('−£40.00'); // typographic minus (U+2212)
  await expect(down.getByTestId('monthly-restatement-change')).toHaveClass(/text-rose-400/);
});

test('SC-MPR-04: trade-count-only fallback line shows when restated with a zero P&L change — and only then', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [RESTATED_UP, RESTATED_TRADE_COUNT_ONLY]);
  await gotoMonthlyTab(page);

  await page.getByRole('row', { name: /May 2026/ }).getByTestId('monthly-restated-marker').click();
  // Non-zero change: no fallback line.
  await expect(page.getByTestId('monthly-restatement-detail')).toBeVisible();
  await expect(page.getByTestId('monthly-restatement-trade-count-note')).toHaveCount(0);

  await page.getByRole('row', { name: /February 2026/ }).getByTestId('monthly-restated-marker').click();
  const note = page.getByTestId('monthly-restatement-trade-count-note');
  await expect(note).toBeVisible();
  await expect(note).toHaveText('Trade count for this month has also changed since it was reviewed.');
  await expect(page.getByTestId('monthly-restatement-detail').filter({ has: note })
    .getByTestId('monthly-restatement-change')).toHaveText('£0.00');
});

test('SC-MPR-05: "Restatement check unavailable." shows only when the rows carry no snapshot fields', async ({ page }) => {
  // Snapshot fields present -> no unavailable line.
  await mockFallback(page);
  await mockMonthlyPnl(page, [NOT_RESTATED, IN_PROGRESS]);
  await gotoMonthlyTab(page);
  await expect(page.getByRole('row', { name: /March 2026/ })).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-restatement-unavailable')).toHaveCount(0);
});

test('SC-MPR-05b: rows without snapshot fields render normally, without markers, plus the unavailable line', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [
    { year: 2026, month: 5, realised_pnl_gbp: 175, trade_count: 4 },
    { year: 2026, month: 4, realised_pnl_gbp: 60, trade_count: 3 },
  ]);
  await gotoMonthlyTab(page);

  // P&L figures are never blocked.
  await expect(page.getByRole('row', { name: /May 2026/ })).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-restatement-unavailable')).toHaveText('Restatement check unavailable.');
  await expect(page.getByTestId('monthly-restated-marker')).toHaveCount(0);
});

test('SC-MPR-06: Tax Year notice shows when restated_month_count >= 1 and links to the Monthly tab', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYear(page, 2);
  await mockMonthlyPnl(page, [RESTATED_UP]);
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();

  const notice = page.getByTestId('taxyear-restated-notice');
  await expect(notice).toBeVisible({ timeout: 8000 });
  await expect(notice).toContainText('Includes 2 restated months — see the Monthly tab for details.');

  await notice.getByRole('button', { name: 'Monthly tab' }).click();
  await expect(page.getByText('Monthly P&L Report')).toBeVisible();
  await expect(page.getByTestId('monthly-restated-marker')).toBeVisible();
});

test('SC-MPR-06b: Tax Year notice uses singular wording at restated_month_count = 1', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYear(page, 1);
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();

  await expect(page.getByTestId('taxyear-restated-notice')).toContainText(
    'Includes 1 restated month — see the Monthly tab for details.',
    { timeout: 8000 }
  );
});

test('SC-MPR-07: Tax Year notice is absent when restated_month_count = 0', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYear(page, 0);
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();

  // Wait for the summary bar (loaded state) before asserting absence.
  await expect(page.getByText('Total Realised P&L')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('taxyear-restated-notice')).toHaveCount(0);
});
