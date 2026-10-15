/**
 * Trade Entry — ATR preview before save
 * ST-17 (BLG-BE-146, EPIC-03, v9.12)
 *
 * Design source: docs/design/2026-10-12__release-v9.12/trade-entry-atr-preview/decision_record.md §2.1, §6
 * Frontend spec: docs/specs/frontend/components/position_form.md v1.9 §ATR (14-day), §Initial Stop, §Widget inputs
 *
 * Coverage:
 *   SC-TAP-01  ATR blank + preview ATR: numeric stop, risk and suggested shares show before save (AC 1);
 *              the fetched ATR is a hint only, never placed into the input
 *   SC-TAP-02  Preview returns atr: null — the "Calculated on save" states remain (AC 3)
 *   SC-TAP-03  Preview call fails (500) — "Calculated on save", no error banner (AC 3)
 *   SC-TAP-04  A typed ATR takes precedence: the hint hides and the typed ATR drives the stop
 *   SC-TAP-05  The submitted payload carries a blank ATR when only the preview was used
 *
 * Backend AC 2 (preview stop == saved initial_stop) is pinned in tests/test_market_atr_preview_endpoint.py.
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradeEntry').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

/** Mocks GET /market/atr/{ticker}; records each requested URL. */
async function mockAtrPreview(page, { atr = 2, status = 200, calls = [] } = {}) {
  await page.route(/\/market\/atr\//, (route) => {
    calls.push(route.request().url());
    if (status !== 200) {
      route.fulfill({ status, contentType: 'application/json', body: JSON.stringify({ detail: 'Internal server error' }) });
      return;
    }
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: { ticker: 'LGEN', market: 'UK', atr, atr_period: 14, as_of: '2026-10-13T09:00:00+00:00' },
      }),
    });
  });
  return calls;
}

/** Mocks POST /portfolio/size; records each request body. */
async function mockPortfolioSize(page, bodies = []) {
  await page.route(/\/portfolio\/size/, (route) => {
    bodies.push(route.request().postDataJSON());
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          valid: true, suggested_shares: 10.0, risk_amount: 100.0, stop_distance: 10.0,
          estimated_cost: 1000.0, estimated_fees: 0.0, fx_rate_used: 1.0, cash_sufficient: true,
          available_cash: 20000.0, concentration_adjusted: false, concentration_reason: null,
        },
      }),
    });
  });
  return bodies;
}

async function gotoTradeEntry(page) {
  await page.goto('/#/TradeEntry');
  await expect(page.getByPlaceholder('e.g., AAPL or VOD.L')).toBeVisible({ timeout: 10000 });
}

// UK ticker so no FX conversion applies to the risk figure. ATR left blank.
async function fillUkEntryNoAtr(page, { entry = '100', shares = null } = {}) {
  await page.getByPlaceholder('e.g., AAPL or VOD.L').fill('LGEN');
  await page.getByPlaceholder('0.00').first().fill(entry);
  if (shares !== null) await page.getByPlaceholder('0', { exact: true }).fill(shares);
}

test('SC-TAP-01: with ATR blank, the previewed ATR drives a numeric stop, risk and suggested shares', async ({ page }) => {
  await mockFallback(page);
  const atrCalls = await mockAtrPreview(page, { atr: 2 });
  const sizeBodies = await mockPortfolioSize(page);
  await gotoTradeEntry(page);
  await fillUkEntryNoAtr(page, { entry: '100' });

  await expect(page.getByTestId('system-initial-stop-value')).toHaveText('£90.00'); // 100 − 5 × 2
  await expect(page.getByTestId('system-initial-stop')).toContainText(
    'Entry − 5× ATR (§5), using the fetched 14-day ATR. The stop is recalculated at save and may differ slightly if prices update before then.'
  );
  await expect(page.getByTestId('atr-fetched-hint')).toHaveText('Fetched: £2.00 (14-day, 13 Oct)');
  // The fetched value is never placed into the input.
  await expect(page.getByPlaceholder('Fetched automatically if blank')).toHaveValue('');

  // The sizing widget is sized from the preview stop and fills Shares.
  await expect(page.getByText('10.0000')).toBeVisible({ timeout: 5000 });
  await expect(page.getByPlaceholder('0', { exact: true })).toHaveValue('10');
  expect(sizeBodies.some((b) => b.stop_price === 90)).toBe(true);
  // Risk (to stop) = (100 − 90) × 10 shares.
  await expect(page.getByTestId('risk-to-stop')).toHaveText('£100.00');

  expect(atrCalls.some((u) => /\/market\/atr\/LGEN\?market=UK$/.test(u))).toBe(true);
});

test('SC-TAP-02: a null preview ATR keeps the "Calculated on save" states', async ({ page }) => {
  await mockFallback(page);
  await mockAtrPreview(page, { atr: null });
  await gotoTradeEntry(page);
  await fillUkEntryNoAtr(page, { shares: '10' });

  await expect(page.getByTestId('system-initial-stop-value')).toHaveText('Calculated on save');
  await expect(page.getByTestId('system-initial-stop')).toContainText('The system fetches the 14-day ATR for LGEN and sets the stop at Entry − 5× ATR.');
  await expect(page.getByTestId('risk-to-stop')).toHaveText('Calculated on save');
  await expect(page.getByTestId('sizing-empty-hint')).toHaveText('Enter an entry price and ATR to size this position.');
  await expect(page.getByTestId('atr-fetched-hint')).toHaveCount(0);
});

test('SC-TAP-03: a failed preview falls back to "Calculated on save" with no error banner', async ({ page }) => {
  await mockFallback(page);
  const calls = await mockAtrPreview(page, { status: 500 });
  await gotoTradeEntry(page);
  await fillUkEntryNoAtr(page, { shares: '10' });

  await expect.poll(() => calls.length).toBeGreaterThan(0);
  await expect(page.getByTestId('system-initial-stop-value')).toHaveText('Calculated on save');
  await expect(page.getByTestId('atr-fetched-hint')).toHaveCount(0);
  await expect(page.getByRole('alert')).toHaveCount(0);
});

test('SC-TAP-04: a typed ATR takes precedence over the preview', async ({ page }) => {
  await mockFallback(page);
  await mockAtrPreview(page, { atr: 2 });
  await gotoTradeEntry(page);
  await fillUkEntryNoAtr(page, { entry: '100', shares: '10' });
  await expect(page.getByTestId('atr-fetched-hint')).toBeVisible();

  await page.getByPlaceholder('Fetched automatically if blank').fill('3');
  await expect(page.getByTestId('atr-fetched-hint')).toHaveCount(0);
  await expect(page.getByTestId('system-initial-stop-value')).toHaveText('£85.00'); // 100 − 5 × 3
  await expect(page.getByTestId('system-initial-stop')).toContainText('Entry − 5× ATR (§5). This is the stop that will be stored.');
});

test('SC-TAP-05: the payload submits a blank ATR when only the preview was used', async ({ page }) => {
  await mockFallback(page);
  await mockAtrPreview(page, { atr: 2 });
  let captured = null;
  await page.route(`${API}/portfolio/position`, (route) => {
    captured = route.request().postDataJSON();
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { ticker: 'LGEN', initial_stop: 90, trade_plan_linked: false, position_id: 'p-tap' } }),
    });
  });
  await gotoTradeEntry(page);
  await fillUkEntryNoAtr(page, { entry: '100', shares: '10' });
  await expect(page.getByTestId('system-initial-stop-value')).toHaveText('£90.00');

  await page.getByRole('button', { name: /create position/i }).click();
  await expect.poll(() => captured).not.toBeNull();
  expect(captured.atr_value).toBeNull();
  expect(captured).not.toHaveProperty('stop_price');
});
