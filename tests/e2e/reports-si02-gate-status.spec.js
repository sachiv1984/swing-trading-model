/**
 * SI-02 Gate Status Section — Reports Page, Tax Year P&L tab (ST-06, BLG-FEAT-71, EPIC-02, v6.8)
 *
 * Design source: docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md
 * Spec: docs/specs/frontend/pages/reports.md §SI-02 Gate Status
 *
 * Covers observable AC (ST-06 AC-05):
 *   SC-SI02-01  Section renders collapsed by default; expands on toggle click
 *   SC-SI02-02  Total closed trades and linked-to-a-trade-plan counts displayed
 *   SC-SI02-03  3 gate condition badges render MET/NOT MET per live data
 *   SC-SI02-04  Values sourced live — not hardcoded (reflects ST-01/BLG-BE-46 finding as-is)
 *   SC-SI02-05  Error state does not block rest of Reports page
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click
 * the "Tax Year P&L" tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const TAX_YEAR_REPORT_EMPTY = {
  status: 'ok',
  data: {
    tax_year_label: '2026/27',
    summary: {
      total_realised_pnl: 0,
      total_gross_profit: 0,
      total_gross_loss: 0,
      win_rate: 0,
      total_closed_trades: 0,
    },
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

async function mockTaxYearReport(page) {
  await page.route(new RegExp(`${API}/reports/tax-year`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TAX_YEAR_REPORT_EMPTY) })
  );
}

async function mockTrades(page, totalTrades) {
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { total_trades: totalTrades, win_rate: 0, total_pnl: 0, trades: [] } }),
    })
  );
}

async function mockTradePlans(page, plans) {
  await page.route(`${API}/trade-plans`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plans }) })
  );
}

async function mockArc5Compliance(page, tradePlanAdherenceRate) {
  await page.route(new RegExp(`${API}/analytics/arc5-compliance`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          period: '7d',
          validation_pass_rate_by_rule: {},
          events_per_week: 0,
          override_rate: null,
          top_rule_breach: null,
          trade_plan_adherence_rate: tradePlanAdherenceRate,
        },
      }),
    })
  );
}

async function gotoTaxYearTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();
  await expect(page.getByTestId('si02-gate-status-section')).toBeVisible({ timeout: 10000 });
}

test('SC-SI02-01: Section renders collapsed by default; expands on toggle click', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page);
  await mockTrades(page, 20);
  await mockTradePlans(page, []);
  await mockArc5Compliance(page, 0);
  await gotoTaxYearTab(page);

  await expect(page.getByText('Total Closed Trades', { exact: true })).not.toBeVisible();

  await page.getByTestId('si02-gate-status-toggle').click();

  await expect(page.getByText('Total Closed Trades', { exact: true })).toBeVisible({ timeout: 5000 });
});

test('SC-SI02-02: Total and linked closed-trade counts displayed live (BLG-BE-46 pre-fix: 20 total, 0 linked)', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page);
  await mockTrades(page, 20);
  await mockTradePlans(page, [
    { id: 'p1', ticker: 'AAPL', position_id: null },
    { id: 'p2', ticker: 'MSFT', position_id: null },
  ]);
  await mockArc5Compliance(page, 0);
  await gotoTaxYearTab(page);
  await page.getByTestId('si02-gate-status-toggle').click();

  await expect(page.getByText('20 total closed trades')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('0 linked to a trade plan')).toBeVisible();
});

test('SC-SI02-03: All 3 conditions show NOT MET when 0 trades are linked', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page);
  await mockTrades(page, 20);
  await mockTradePlans(page, [{ id: 'p1', ticker: 'AAPL', position_id: null }]);
  await mockArc5Compliance(page, 0);
  await gotoTaxYearTab(page);
  await page.getByTestId('si02-gate-status-toggle').click();

  await expect(page.getByText('20 total closed trades')).toBeVisible({ timeout: 5000 });
  const notMetBadges = page.getByText('NOT MET');
  await expect(notMetBadges).toHaveCount(2); // condition 2 (linked<20) and condition 3 (adherence=0)
  await expect(page.getByText('MET', { exact: true })).toHaveCount(1); // condition 1 (total>=20)
});

test('SC-SI02-04: Conditions show MET once trades are linked and adherence is positive', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page);
  await mockTrades(page, 20);
  const linkedPlans = Array.from({ length: 20 }, (_, i) => ({ id: `p${i}`, ticker: 'AAPL', position_id: `pos-${i}` }));
  await mockTradePlans(page, linkedPlans);
  await mockArc5Compliance(page, 1.0);
  await gotoTaxYearTab(page);
  await page.getByTestId('si02-gate-status-toggle').click();

  await expect(page.getByText('20 total closed trades')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('20 linked to a trade plan')).toBeVisible();
  await expect(page.getByText('MET', { exact: true })).toHaveCount(3);
});

test('SC-SI02-05: Error state shown without blocking rest of Reports page', async ({ page }) => {
  await mockFallback(page);
  await mockTaxYearReport(page);
  await page.route(`${API}/trades`, (route) => route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'fail' }) }));
  await mockTradePlans(page, []);
  await mockArc5Compliance(page, 0);
  await gotoTaxYearTab(page);
  await page.getByTestId('si02-gate-status-toggle').click();

  await expect(page.getByText(/unable to load gate status/i)).toBeVisible({ timeout: 5000 });
  // Rest of the page (Scope Note) still renders
  await expect(page.getByText(/UK tax year only/i)).toBeVisible();
});
