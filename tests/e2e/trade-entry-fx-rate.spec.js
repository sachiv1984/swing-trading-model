/**
 * Trade Entry — FX rate pre-filled from the live rate
 * ST-02 (BLG-FE-245, EPIC-01, v9.15)
 *
 * Design source: docs/design/2026-11-03__release-v9.15/trade-entry-fx-rate/decision_record.md §2.2, §2.3
 * Frontend spec: docs/specs/frontend/components/position_form.md v1.12 §FX Rate
 *
 * Coverage:
 *   SC-TEFX-01  A live rate of 1.35 pre-fills 1.3500 with "Live rate, 5 min ago" (AC 1)
 *   SC-TEFX-02  The backend's fixed fallback shows in the field with "Fallback rate: no live rate is available" (AC 2)
 *   SC-TEFX-03  A failed request leaves the field empty with "No rate available: enter the rate"
 *   SC-TEFX-04  A last-known rate says "Not live: last rate from {age}"
 *   SC-TEFX-05  A value typed before the rate arrives is never overwritten; the line says "Entered by you"
 *   SC-TEFX-06  Switching to UK hides the field and sends fx_rate 1
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradeEntry').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const US_TICKER = 'GOOGL'; // 5 letters: Trade Entry detects US (2–4 letters read as UK)

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMarketStatus(page, { rate, source, minutesAgo = 5, fail = false, delayMs = 0 }) {
  await page.route(`${API}/market/status`, async (route) => {
    if (delayMs) await new Promise((r) => setTimeout(r, delayMs));
    if (fail) {
      await route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'Internal server error' }) });
      return;
    }
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          spy: { price: 500, ma200: 480, is_risk_on: true, regime_status: 'risk_on' },
          ftse: { price: 7800, ma200: 7600, is_risk_on: true, regime_status: 'risk_on' },
          fx_rate: rate,
          fx_rate_source: source,
          fx_rate_as_of: new Date(Date.now() - minutesAgo * 60000).toISOString(),
        },
      }),
    });
  });
}

const fxInput = (page) => page.getByTestId('trade-entry-fx-input');
const fxSource = (page) => page.getByTestId('trade-entry-fx-source');

async function gotoAndEnterUsTicker(page) {
  await page.goto('/#/TradeEntry');
  await expect(page.getByPlaceholder('e.g., AAPL or VOD.L')).toBeVisible({ timeout: 10000 });
  await page.getByPlaceholder('e.g., AAPL or VOD.L').fill(US_TICKER);
}

test('SC-TEFX-01: a live rate of 1.35 pre-fills the field with its source and age', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page, { rate: 1.35, source: 'live', minutesAgo: 5 });
  await gotoAndEnterUsTicker(page);
  await expect(fxInput(page)).toHaveValue('1.3500', { timeout: 10000 });
  await expect(fxSource(page)).toHaveText('Live rate, 5 min ago');
  await expect(fxInput(page)).toHaveAttribute('aria-describedby', /trade-entry-fx-source/);
});

test('SC-TEFX-02: the backend fallback rate is shown with a visible fallback note', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page, { rate: 1.27, source: 'constant' });
  await gotoAndEnterUsTicker(page);
  await expect(fxInput(page)).toHaveValue('1.2700', { timeout: 10000 });
  await expect(fxSource(page)).toHaveText('Fallback rate: no live rate is available');
  await expect(fxSource(page)).toHaveClass(/text-amber-700/);
});

test('SC-TEFX-03: a failed rate request leaves the field empty and asks for the rate', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page, { fail: true });
  await gotoAndEnterUsTicker(page);
  await expect(fxSource(page)).toHaveText('No rate available: enter the rate', { timeout: 10000 });
  await expect(fxInput(page)).toHaveValue('');
});

test('SC-TEFX-04: a last-known rate is labelled not live with its age', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page, { rate: 1.3123, source: 'last_known', minutesAgo: 180 });
  await gotoAndEnterUsTicker(page);
  await expect(fxInput(page)).toHaveValue('1.3123', { timeout: 10000 });
  await expect(fxSource(page)).toHaveText('Not live: last rate from 3 h ago');
});

test('SC-TEFX-05: a value typed before the live rate arrives is never overwritten', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page, { rate: 1.35, source: 'live', delayMs: 2000 });
  await gotoAndEnterUsTicker(page);
  await expect(fxInput(page)).toHaveAttribute('placeholder', 'Fetching live rate…');
  await fxInput(page).fill('1.4');
  await expect(fxSource(page)).toHaveText('Entered by you (live rate 1.3500)', { timeout: 10000 });
  await expect(fxInput(page)).toHaveValue('1.4');
});

test('SC-TEFX-06: switching to a UK ticker hides the FX field and saves fx_rate 1', async ({ page }) => {
  let body = null;
  await mockFallback(page);
  await mockMarketStatus(page, { rate: 1.35, source: 'live' });
  await page.route(`${API}/portfolio/position`, (route) => {
    body = route.request().postDataJSON();
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { ticker: body.ticker, initial_stop: 90, position_id: 'p-fx', trade_plan_linked: false } }) });
  });
  await gotoAndEnterUsTicker(page);
  await expect(fxInput(page)).toHaveValue('1.3500', { timeout: 10000 });
  await page.getByPlaceholder('e.g., AAPL or VOD.L').fill('LGEN');
  await expect(fxInput(page)).toHaveCount(0);
  await page.getByPlaceholder('0.00').first().fill('100');
  await page.getByPlaceholder('Fetched automatically if blank').fill('2');
  await page.getByPlaceholder('0', { exact: true }).fill('10');
  await page.getByRole('button', { name: /create position/i }).click();
  await expect.poll(() => body).not.toBeNull();
  expect(body.fx_rate).toBe(1);
});
