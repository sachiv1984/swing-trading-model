/**
 * FX rate source indicator — Playwright E2E Tests
 * ST-04 / ST-05 (EPIC-01, v9.14, BLG-BE-194 / BLG-BE-169)
 * Design: docs/design/2026-10-29__release-v9.14/fx-rate-source-indicator/decision_record.md
 *
 *   SC-FXS-01: a last-known rate two days old shows its age on Dashboard Card 2 and the Risk Dashboard,
 *              and the Risk Dashboard notice carries the decision record §2.2 description
 *   SC-FXS-02: the fixed fallback is named as such on both surfaces, never as a live rate
 *   SC-FXS-03: a live rate shows no notice on either surface
 *   SC-FXS-04: the Signals FX tile shows its source line, and "—" with no rate (no page constant)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const TWO_DAYS_AGO = new Date(Date.now() - 2 * 24 * 60 * 60 * 1000 - 5 * 60 * 1000).toISOString();

function portfolio(fx) {
  return {
    cash: 5000, cash_balance: 5000, total_value: 10000, open_positions_value: 5000, total_pnl: 0,
    current_drawdown_percent: 0, peak_portfolio_value: 10000, portfolio_heat_percent: 8.5,
    position_risks: [], positions: [], ...fx,
  };
}

async function mockAll(page, fx, marketStatus) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(`${API}/portfolio`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(portfolio(fx)) })
  );
  if (marketStatus) {
    await page.route(`${API}/market/status`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: marketStatus }) })
    );
  }
}

const LAST_KNOWN = { live_fx_rate: 1.3301, fx_rate_source: 'last_known', fx_rate_as_of: TWO_DAYS_AGO };
const CONSTANT = { live_fx_rate: 1.27, fx_rate_source: 'constant', fx_rate_as_of: null };
const LIVE = { live_fx_rate: 1.3412, fx_rate_source: 'live', fx_rate_as_of: new Date().toISOString() };

async function gotoRisk(page) {
  await page.goto('/#/RiskDashboard');
  await expect(page.locator('h1').filter({ hasText: 'Risk Dashboard' })).toBeVisible({ timeout: 15000 });
}

test('SC-FXS-01: a two-day-old last-known rate shows its age on Card 2 and the Risk Dashboard', async ({ page }) => {
  await mockAll(page, LAST_KNOWN);
  await page.goto('/#/');
  const card = page.getByTestId('dashboard-fx-source-notice');
  await expect(card).toBeVisible({ timeout: 15000 });
  await expect(card).toHaveText('⚠ FX rate not live: GBP/USD 1.3301 from 2 days ago');
  await expect(page.getByRole('link').filter({ has: card })).toHaveAccessibleDescription(
    /^The live GBP\/USD rate is unavailable\. US values, P&L and heat use the last fetched rate, 1\.3301 at .+\. Reload the page to try again\.$/
  );

  await gotoRisk(page);
  const notice = page.getByTestId('risk-fx-source-notice');
  await expect(notice).toContainText('FX rate not live: GBP/USD 1.3301 from 2 days ago');
  await expect(notice).toHaveAccessibleDescription(
    /^The live GBP\/USD rate is unavailable\. US values, P&L and heat use the last fetched rate, 1\.3301 at .+\. Reload the page to try again\.$/
  );
});

test('SC-FXS-02: the fixed fallback is named, never shown as live', async ({ page }) => {
  await mockAll(page, CONSTANT);
  await page.goto('/#/');
  await expect(page.getByTestId('dashboard-fx-source-notice')).toHaveText(
    '⚠ FX rate unavailable: using fixed GBP/USD 1.2700', { timeout: 15000 }
  );
  await gotoRisk(page);
  const notice = page.getByTestId('risk-fx-source-notice');
  await expect(notice).toContainText('fixed GBP/USD 1.2700');
  await expect(notice).not.toContainText('live:');
});

test('SC-FXS-03: a live rate shows no FX notice', async ({ page }) => {
  await mockAll(page, LIVE);
  await page.goto('/#/');
  await expect(page.getByText('Portfolio Heat')).toBeVisible({ timeout: 15000 });
  await expect(page.getByText('8.5%').first()).toBeVisible({ timeout: 15000 });
  await expect(page.getByTestId('dashboard-fx-source-notice')).toHaveCount(0);
  await gotoRisk(page);
  await expect(page.getByTestId('risk-fx-source-notice')).toHaveCount(0);
});

test('SC-FXS-04: the Signals FX tile shows its source, and "—" with no rate', async ({ page }) => {
  const regime = { price: 500, ma200: 450, is_risk_on: true, regime_status: 'risk_on' };
  await mockAll(page, LIVE, {
    spy: regime, ftse: regime, fx_rate: 1.3301, fx_rate_source: 'last_known', fx_rate_as_of: TWO_DAYS_AGO,
  });
  await page.goto('/#/Signals');
  await expect(page.getByTestId('signals-fx-rate')).toHaveText('1 GBP = $1.3301 USD', { timeout: 15000 });
  await expect(page.getByTestId('signals-fx-source')).toHaveText('Not live: from 2 days ago');

  await page.unroute(`${API}/market/status`);
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'x' }) })
  );
  await page.reload();
  await expect(page.getByTestId('signals-fx-rate')).toHaveText('—', { timeout: 15000 });
  await expect(page.getByText('1.3611')).toHaveCount(0);
});
