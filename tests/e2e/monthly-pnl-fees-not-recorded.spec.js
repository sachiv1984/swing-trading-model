/**
 * NULL-fee visibility — Monthly P&L Report — ST-03 (BLG-FE-187, EPIC-02, v9.7)
 *
 * Design source: docs/design/2026-09-23__release-v9.7/monthly-pnl-fees-surfacing/decision_record.md
 * Spec: docs/specs/frontend/pages/reports.md §Fees-Not-Recorded Visibility (v0.19 — ST-03)
 * Data contract: docs/specs/api_contracts/reports_endpoints.md v0.13 (`null_fee_trade_count` per month;
 * no top-level aggregate — the notice's N is summed client-side from the loaded rows).
 *
 * Coverage:
 *   SC-MPF-01  A month with null_fee_trade_count > 0 shows the per-month indicator; a month with 0 does not
 *   SC-MPF-02  Aggregate notice shows the client-side sum across loaded months
 *   SC-MPF-03  Aggregate notice uses singular wording at N = 1
 *   SC-MPF-04  No notice and no indicator when every month has null_fee_trade_count = 0
 *   SC-MPF-05  Aggregate notice is non-dismissible
 *   SC-MPF-06  Basis caption is always shown, stating the net-of-fees basis
 *   SC-MPF-07  No notice when the report fails to load
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click
 * the "Monthly P&L" tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const month = (m, overrides = {}) => ({
  year: 2026,
  month: m,
  realised_pnl_gbp: 100,
  trade_count: 4,
  null_fee_trade_count: 0,
  snapshotted: true,
  restated: false,
  snapshot_realised_pnl_gbp: 100,
  restated_diff_gbp: 0,
  ...overrides,
});

function monthlyPnlResponse(months) {
  return { status: 'ok', data: months, estimated_unrealised_pnl: null, unrealised_note: null, compliance_summary: null };
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

async function gotoMonthlyTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /monthly p&l/i }).click();
}

test('SC-MPF-01: a month with null_fee_trade_count > 0 shows the indicator; a month with 0 does not', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [
    month(7, { trade_count: 5, null_fee_trade_count: 2 }),
    month(6, { trade_count: 3, null_fee_trade_count: 0 }),
  ]);
  await gotoMonthlyTab(page);

  const julyRow = page.getByRole('row', { name: /July 2026/ });
  const indicator = julyRow.getByTestId('monthly-fees-missing-count');
  await expect(indicator).toBeVisible({ timeout: 8000 });
  await expect(indicator).toHaveText('5 · 2 no fees');
  await expect(indicator).toHaveAttribute('aria-label', '5 trades, 2 without fees recorded');

  // June has k = 0: renders unchanged — the bare trade count, no indicator.
  const juneRow = page.getByRole('row', { name: /June 2026/ });
  await expect(juneRow.getByTestId('monthly-fees-missing-count')).toHaveCount(0);
  await expect(juneRow.getByRole('cell', { name: '3', exact: true })).toBeVisible();
});

test('SC-MPF-02: aggregate notice shows the client-side sum of null_fee_trade_count across loaded months', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [
    month(7, { null_fee_trade_count: 2 }),
    month(6, { null_fee_trade_count: 0 }),
    month(5, { null_fee_trade_count: 1 }),
  ]);
  await gotoMonthlyTab(page);

  const notice = page.getByTestId('monthly-fees-missing-notice');
  await expect(notice).toBeVisible({ timeout: 8000 });
  await expect(notice).toContainText('3 closed trades have no fees recorded, so these figures may not reflect their costs.');
});

test('SC-MPF-03: aggregate notice uses singular wording at N = 1', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [month(7, { null_fee_trade_count: 1 }), month(6)]);
  await gotoMonthlyTab(page);

  await expect(page.getByTestId('monthly-fees-missing-notice')).toContainText(
    '1 closed trade has no fees recorded, so these figures may not reflect its costs.',
    { timeout: 8000 }
  );
});

test('SC-MPF-04: no notice and no indicator when every month has null_fee_trade_count = 0', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [month(7), month(6)]);
  await gotoMonthlyTab(page);

  // Wait for the table to render before asserting absence.
  await expect(page.getByRole('row', { name: /July 2026/ })).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-fees-missing-notice')).toHaveCount(0);
  await expect(page.getByTestId('monthly-fees-missing-count')).toHaveCount(0);
});

test('SC-MPF-05: aggregate notice is non-dismissible', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [month(7, { null_fee_trade_count: 2 })]);
  await gotoMonthlyTab(page);

  const notice = page.getByTestId('monthly-fees-missing-notice');
  await expect(notice).toBeVisible({ timeout: 8000 });
  await expect(notice.getByTestId('standing-alert-dismiss')).toHaveCount(0);
});

test('SC-MPF-06: basis caption is always shown and states the net-of-fees basis', async ({ page }) => {
  await mockFallback(page);
  await mockMonthlyPnl(page, [month(7)]); // N = 0 — the caption must not depend on any NULL-fee trade existing
  await gotoMonthlyTab(page);

  await expect(page.getByTestId('monthly-basis-caption')).toHaveText('Realised P&L is net of recorded fees.', { timeout: 8000 });
});

test('SC-MPF-07: no notice when the report fails to load', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/monthly-pnl(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error' }) })
  );
  await gotoMonthlyTab(page);

  await expect(page.getByText('Monthly P&L Report')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-fees-missing-notice')).toHaveCount(0);
});
