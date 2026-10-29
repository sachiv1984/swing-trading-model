/**
 * Unknown market regime — Playwright E2E Tests
 * ST-03 (EPIC-01, v9.14, BLG-BE-193)
 * Design: docs/design/2026-10-29__release-v9.14/market-regime-unknown/decision_record.md
 *
 *   SC-MRU-01: Dashboard Card 4 shows UNKNOWN ? for an unmeasured SPY (never RISK-OFF), with the
 *              ruling explanation as the badge's accessible description; FTSE stays RISK-ON ✓
 *   SC-MRU-02: the Signals market status bar shows "Unknown" and "Price unavailable" for the same mock
 *   SC-MRU-03: the customisable Dashboard regime widget shows Unknown, not Risk Off, for an unknown market
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const US_EXPLANATION =
  'US market regime could not be measured: index data is unavailable. New entries in this market are blocked until it is measured.';

const MARKET_STATUS = {
  status: 'ok',
  data: {
    spy: { price: null, ma200: null, is_risk_on: null, regime_status: 'unknown' },
    ftse: { price: 8200.5, ma200: 8000.1, is_risk_on: true, regime_status: 'risk_on' },
    fx_rate: 1.3412,
    fx_rate_source: 'live',
    fx_rate_as_of: '2026-10-29T09:00:00+00:00',
    last_updated: '2026-10-29T09:00:00',
  },
};

async function mockApi(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MARKET_STATUS) })
  );
  await page.route(`${API}/market/regime`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: [{ market: 'US', status: 'unknown' }, { market: 'UK', status: 'risk_on' }],
        as_of: '2026-10-29T09:00:00',
      }),
    })
  );
}

test('SC-MRU-01: Card 4 shows SPY as UNKNOWN with the ruling as its accessible description', async ({ page }) => {
  await mockApi(page);
  await page.goto('/#/');
  const badge = page.getByTestId('regime-unknown-SPY');
  await expect(badge).toBeVisible({ timeout: 15000 });
  await expect(badge).toHaveText('UNKNOWN ?');
  await expect(badge).toHaveAccessibleDescription(US_EXPLANATION);
  await expect(page.getByRole('link').filter({ has: badge })).toHaveAccessibleDescription(US_EXPLANATION);
  await expect(page.getByText('RISK-ON ✓')).toHaveCount(1);
  await expect(page.getByText('RISK-OFF ✗')).toHaveCount(0);
});

test('SC-MRU-02: the Signals bar shows Unknown and "Price unavailable" for SPY', async ({ page }) => {
  await mockApi(page);
  await page.goto('/#/Signals');
  const tile = page.getByTestId('signals-regime-US');
  await expect(tile).toBeVisible({ timeout: 15000 });
  await expect(tile.getByText('Unknown')).toBeVisible();
  await expect(tile.getByText('Price unavailable')).toBeVisible();
  await expect(tile.getByText('Risk Off')).toHaveCount(0);
  await expect(tile.getByText('$0.00')).toHaveCount(0);
  await expect(page.getByTestId('signals-regime-unknown-US')).toHaveAccessibleDescription(US_EXPLANATION);
  await expect(page.getByTestId('signals-regime-UK').getByText('Risk On')).toBeVisible();
});

test('SC-MRU-03: the Dashboard US regime widget shows Unknown, not Risk Off', async ({ page }) => {
  await mockApi(page);
  await page.goto('/#/Dashboard');
  const pill = page.getByTestId('regime-widget-unknown-US');
  await expect(pill).toBeVisible({ timeout: 15000 });
  await expect(pill).toHaveText('Unknown');
  await expect(pill).toHaveAccessibleDescription(US_EXPLANATION);
  await pill.focus();
  await expect(page.getByRole('tooltip')).toContainText('could not be measured');
});
