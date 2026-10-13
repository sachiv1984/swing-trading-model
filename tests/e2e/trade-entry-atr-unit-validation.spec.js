/**
 * Trade Entry — ATR unit label and implausible typed ATR
 * ST-18 (BLG-FE-203, EPIC-03, v9.12)
 *
 * Design source: docs/design/2026-10-12__release-v9.12/trade-entry-atr-preview/decision_record.md §2.2, §2.3, §6
 * Frontend spec: docs/specs/frontend/components/position_form.md v1.9 §ATR (14-day), §Validation Errors
 *
 * Coverage:
 *   SC-TAU-01  The ATR label shows £ for a UK ticker and $ for a US ticker; "ATR (14-day)" before a ticker (AC 1)
 *   SC-TAU-02  Entry 10, ATR 2 (5× ATR = entry): inline error on blur, aria wiring, submit disabled (AC 3)
 *   SC-TAU-03  Entry 10, ATR 1.5: no error, submit enabled (AC 3)
 *   SC-TAU-04  A US ticker's error names $
 *
 * Backend AC 2 (400 from POST /portfolio/position) is pinned in
 * tests/test_add_position_stop_handling.py::TestImplausibleTypedAtrRejected.
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

async function gotoTradeEntry(page) {
  await page.goto('/#/TradeEntry');
  await expect(page.getByPlaceholder('e.g., AAPL or VOD.L')).toBeVisible({ timeout: 10000 });
}

// LGEN is detected as UK; GOOGL (5 letters) as US.
async function fillEntry(page, { ticker = 'LGEN', entry = '10', atr, shares = '10' }) {
  await page.getByPlaceholder('e.g., AAPL or VOD.L').fill(ticker);
  await page.getByPlaceholder('0.00').first().fill(entry);
  await page.getByPlaceholder('0', { exact: true }).fill(shares);
  const atrInput = page.getByPlaceholder('Fetched automatically if blank');
  await atrInput.fill(atr);
  await atrInput.blur();
}

test('SC-TAU-01: the ATR label shows the market currency unit', async ({ page }) => {
  await mockFallback(page);
  await gotoTradeEntry(page);
  await expect(page.locator('label[for="trade-entry-atr"]')).toHaveText('ATR (14-day)');

  await page.getByPlaceholder('e.g., AAPL or VOD.L').fill('LGEN');
  await expect(page.locator('label[for="trade-entry-atr"]')).toHaveText('ATR (14-day, £)');

  await page.getByPlaceholder('e.g., AAPL or VOD.L').fill('GOOGL');
  await expect(page.locator('label[for="trade-entry-atr"]')).toHaveText('ATR (14-day, $)');
});

test('SC-TAU-02: an implausible typed ATR shows the inline error and disables submit', async ({ page }) => {
  await mockFallback(page);
  await gotoTradeEntry(page);
  await fillEntry(page, { entry: '10', atr: '2' }); // 5 × 2 = 10 ≥ entry

  const error = page.getByTestId('atr-implausible-error');
  await expect(error).toHaveText('This ATR puts the stop at or below zero. Check the unit: ATR is in £, not pence or cents.');
  await expect(error).toHaveClass(/text-rose-700/);
  const atrInput = page.getByPlaceholder('Fetched automatically if blank');
  await expect(atrInput).toHaveAttribute('aria-invalid', 'true');
  await expect(atrInput).toHaveAttribute('aria-describedby', 'atr-implausible-error');
  await expect(page.getByRole('button', { name: /create position/i })).toBeDisabled();
});

test('SC-TAU-03: a plausible typed ATR shows no error and leaves submit enabled', async ({ page }) => {
  await mockFallback(page);
  await gotoTradeEntry(page);
  await fillEntry(page, { entry: '10', atr: '1.5' }); // 5 × 1.5 = 7.5 < entry

  await expect(page.getByTestId('atr-implausible-error')).toHaveCount(0);
  await expect(page.getByPlaceholder('Fetched automatically if blank')).not.toHaveAttribute('aria-invalid', 'true');
  await expect(page.getByRole('button', { name: /create position/i })).toBeEnabled();
});

test('SC-TAU-04: a US ticker\'s error names $', async ({ page }) => {
  await mockFallback(page);
  await gotoTradeEntry(page);
  await fillEntry(page, { ticker: 'GOOGL', entry: '10', atr: '3' });

  await expect(page.getByTestId('atr-implausible-error')).toHaveText('This ATR puts the stop at or below zero. Check the unit: ATR is in $, not pence or cents.');
  await expect(page.getByRole('button', { name: /create position/i })).toBeDisabled();
});
