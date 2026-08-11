/**
 * Reconciliation Tab — Reports Page (ST-01, EPIC-01, v8.2, BLG-FEAT-88)
 *
 * Design source: docs/design/2026-08-04__release-v8.2/pnl-reconciliation-report/decision_record.md
 * Spec: docs/specs/api_contracts/reports_endpoints.md §GET /reports/reconciliation
 *
 * Covers observable AC:
 *   SC-RECON-01  Reconciliation tab renders and can be selected
 *   SC-RECON-02  Matched totals render the "✓ Reconciled" badge
 *   SC-RECON-03  Diverging totals render the "⚠ Discrepancy" badge with the £ difference
 *   SC-RECON-04  Empty year (zero closed trades) renders the empty-state message
 *   SC-RECON-05  Error state renders without blocking rest of Reports page
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click
 * the "Reconciliation" tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockReconciliation(page, data, status = 200) {
  await page.route(new RegExp(`${API}/reports/reconciliation`), (route) =>
    route.fulfill({
      status,
      contentType: 'application/json',
      body: JSON.stringify(status === 200 ? { status: 'ok', data } : { status: 'error', message: 'fail' }),
    })
  );
}

async function gotoReconciliationTab(page) {
  await page.goto('/#/Reports');
  await page.getByTestId('reports-tab-reconciliation').click();
  await expect(page.getByTestId('reconciliation-content')).toBeVisible({ timeout: 10000 });
}

test('SC-RECON-01: Reconciliation tab renders reconciliation content', async ({ page }) => {
  await mockFallback(page);
  await mockReconciliation(page, {
    tax_year_label: '2025/26',
    total_closed_trades: 3,
    system_total_pnl_gbp: 500.0,
    export_total_pnl_gbp: 500.0,
    matched: true,
  });
  await gotoReconciliationTab(page);

  await expect(page.getByTestId('reconciliation-system-total')).toBeVisible({ timeout: 5000 });
});

test('SC-RECON-02: Matched totals render the Reconciled badge', async ({ page }) => {
  await mockFallback(page);
  await mockReconciliation(page, {
    tax_year_label: '2025/26',
    total_closed_trades: 3,
    system_total_pnl_gbp: 500.0,
    export_total_pnl_gbp: 500.0,
    matched: true,
  });
  await gotoReconciliationTab(page);

  await expect(page.getByTestId('reconciliation-match-badge')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('reconciliation-match-badge')).toHaveText(/reconciled/i);
  await expect(page.getByTestId('reconciliation-system-total')).toHaveText('£500.00');
  await expect(page.getByTestId('reconciliation-export-total')).toHaveText('£500.00');
  await expect(page.getByTestId('reconciliation-sign-off-note')).toContainText(/Financial Reporting & Records Owner/i);
  // ST-06 (EPIC-03, v8.6, BLG-FE-149): this note was missing a dark: variant
  // entirely (bare text-slate-500, no theme-awareness) -- must now carry the
  // canonical secondary-text token pair.
  await expect(page.getByTestId('reconciliation-sign-off-note')).toHaveClass(/text-slate-600/);
  await expect(page.getByTestId('reconciliation-sign-off-note')).toHaveClass(/dark:text-slate-400/);
});

test('SC-RECON-03: Diverging totals render the Discrepancy badge with the £ difference', async ({ page }) => {
  await mockFallback(page);
  await mockReconciliation(page, {
    tax_year_label: '2025/26',
    total_closed_trades: 3,
    system_total_pnl_gbp: 500.0,
    export_total_pnl_gbp: 480.0,
    matched: false,
  });
  await gotoReconciliationTab(page);

  await expect(page.getByTestId('reconciliation-match-badge')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('reconciliation-match-badge')).toHaveText(/discrepancy.*£20\.00/i);
});

test('SC-RECON-04: Empty year (zero closed trades) renders the empty-state message', async ({ page }) => {
  await mockFallback(page);
  await mockReconciliation(page, {
    tax_year_label: '2025/26',
    total_closed_trades: 0,
    system_total_pnl_gbp: 0,
    export_total_pnl_gbp: 0,
    matched: true,
  });
  await gotoReconciliationTab(page);

  await expect(page.getByTestId('reconciliation-empty')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('reconciliation-empty')).toContainText('No trade data available for 2025/26');
});

test('SC-RECON-05: Error state shown without blocking rest of Reports page', async ({ page }) => {
  await mockFallback(page);
  await mockReconciliation(page, null, 500);
  await gotoReconciliationTab(page);

  await expect(page.getByTestId('reconciliation-error')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText(/independently re-derived sum/i)).toBeVisible();
});
