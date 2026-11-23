/**
 * Reports Unrealised P&L — live basis and stale-price line
 * (ST-30, BLG-SPEC-203, EPIC-05, v9.18)
 *
 * Spec: docs/specs/frontend/pages/reports.md v0.28 §Unrealised P&L Card (live basis).
 * Design source: docs/design/2026-11-18__release-v9.18/position-data-states/decision_record.md §3.
 *
 * Coverage:
 *   SC-RUL-01  Tax Year card renders from data.summary (the real response shape,
 *              reports_service.get_tax_year_report) with the live figure and note
 *   SC-RUL-02  Tax Year card shows "⚠ 1 position price stale" for one stale price
 *   SC-RUL-03  Monthly card shows "⚠ 2 position prices stale" for two stale prices
 *   SC-RUL-04  No stale line when unrealised_price_stale_count is 0
 *
 * AC 1 (Reports and Positions figures match at the same moment) is a staging AC:
 * mocks cannot show two endpoints agreeing on live prices. The backend test
 * tests/test_reports_integration.py::TestEstimatedUnrealisedPnlLiveBasis asserts
 * the figure is the sum of the Positions page's per-position pnl.
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: HashRouter — '/#/Performance?section=reports', then the tab.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const LIVE_NOTE =
  'Reflects current open positions at time of report generation, not positions open during the ' +
  'specified tax year. Indicative only — not a tax liability. Calculated live at current prices, ' +
  'on the same basis as the Positions page.';

function taxYearResponse({ unrealised = 255.55, staleCount = 0 } = {}) {
  // Shape from reports_service.get_tax_year_report(): the unrealised fields sit in summary.
  return {
    status: 'ok',
    data: {
      tax_year_start: '2026-04-06',
      tax_year_end: '2027-04-05',
      tax_year_label: '2026/27',
      generated_at: '2026-11-23T09:00:00Z',
      summary: {
        total_closed_trades: 0,
        total_realised_pnl: 0,
        total_gross_profit: 0,
        total_gross_loss: 0,
        win_count: 0,
        loss_count: 0,
        win_rate: 0,
        estimated_unrealised_pnl: unrealised,
        unrealised_note: LIVE_NOTE,
        unrealised_price_stale_count: staleCount,
        restated_month_count: 0,
        restated_months_notice: null,
      },
      trades: [],
    },
  };
}

function monthlyResponse({ unrealised = -40.13, staleCount = 0 } = {}) {
  // Shape from main.get_monthly_pnl_endpoint(): unrealised fields are top-level.
  return {
    status: 'ok',
    data: [{ year: 2026, month: 10, realised_pnl_gbp: 120.0, trade_count: 2, null_fee_trade_count: 0 }],
    estimated_unrealised_pnl: unrealised,
    unrealised_note: LIVE_NOTE,
    unrealised_price_stale_count: staleCount,
    compliance_summary: null,
  };
}

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function gotoTaxYear(page, response) {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/tax-year(?!\\?format=csv)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(response) })
  );
  await page.goto('/#/Performance?section=reports');
  await page.getByRole('tab', { name: 'Tax year' }).click();
}

async function gotoMonthly(page, response) {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/reports/monthly-pnl`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(response) })
  );
  await page.goto('/#/Performance?section=reports');
  await page.getByRole('tab', { name: 'Monthly' }).click();
}

test('SC-RUL-01: Tax Year card renders the live figure and note from data.summary', async ({ page }) => {
  await gotoTaxYear(page, taxYearResponse({ unrealised: 255.55 }));
  const card = page.getByTestId('tax-year-unrealised-pnl-card');
  await expect(card).toBeVisible({ timeout: 10000 });
  await expect(card.getByText('Indicative Unrealised P&L (current positions)')).toBeVisible();
  await expect(card).toContainText('£255.55');
  await expect(card).toContainText('Calculated live at current prices, on the same basis as the Positions page.');
});

test('SC-RUL-02: Tax Year card says one position price is stale', async ({ page }) => {
  await gotoTaxYear(page, taxYearResponse({ staleCount: 1 }));
  const notice = page.getByTestId('tax-year-unrealised-stale-notice');
  await expect(notice).toBeVisible({ timeout: 10000 });
  await expect(notice).toHaveText('⚠ 1 position price stale');
});

test('SC-RUL-03: Monthly card says two position prices are stale', async ({ page }) => {
  await gotoMonthly(page, monthlyResponse({ staleCount: 2 }));
  const card = page.getByTestId('monthly-unrealised-pnl-card');
  await expect(card).toBeVisible({ timeout: 10000 });
  await expect(card.getByTestId('monthly-unrealised-stale-notice')).toHaveText('⚠ 2 position prices stale');
});

test('SC-RUL-04: no stale line when every price is live', async ({ page }) => {
  await gotoTaxYear(page, taxYearResponse({ staleCount: 0 }));
  await expect(page.getByTestId('tax-year-unrealised-pnl-card')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('tax-year-unrealised-stale-notice')).toHaveCount(0);

  await gotoMonthly(page, monthlyResponse({ staleCount: 0 }));
  await expect(page.getByTestId('monthly-unrealised-pnl-card')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('monthly-unrealised-stale-notice')).toHaveCount(0);
});
