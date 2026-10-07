/**
 * Trade Entry — System Initial Stop
 * ST-07 (BLG-FE-197, EPIC-02, v9.10)
 *
 * Design source: docs/design/2026-10-06__release-v9.10/trade-entry-system-stop/decision_record.md §5
 * Frontend spec: docs/specs/frontend/components/position_form.md §ATR (14-day), §Initial Stop (set by system)
 *
 * Coverage:
 *   SC-TES-01  Entry + ATR shows Entry − 5×ATR as the stored stop; Risk (to stop) = (entry − system stop) × shares (AC 1)
 *   SC-TES-02  No Stop Price input exists, and the submitted payload carries no stop_price (AC 2)
 *   SC-TES-03  ATR field is labelled "ATR (14-day)" with no "(Optional)" wording (AC 3)
 *   SC-TES-04  With ATR blank, the stop and the risk both show "Calculated on save"; sizing shows its empty hint
 *   SC-TES-05  A trade-plan prefill renders the plan stop as a reference note, not an input value
 *   SC-TES-06  The success toast appends the stored initial stop from the response
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradeEntry').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const PLAN = {
  id: 'plan-tes-1',
  ticker: 'AAPL',
  market: 'US',
  status: 'draft',
  position_id: null,
  r_target: 2.5,
  setup_thesis: 'Breakout setup',
  updated_at: '2026-10-05T10:00:00Z',
  planned_entry_price: 150.0,
  planned_stop_price: 140.0,
  planned_quantity: 10,
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTradePlansList(page, plans) {
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plans }) });
    } else {
      route.continue();
    }
  });
}

/** Captures the next POST /portfolio/position body; replies with the stop the backend would store. */
async function mockAddPosition(page, { initialStop, onRequest } = {}) {
  await page.route(`${API}/portfolio/position`, (route) => {
    const body = route.request().postDataJSON();
    if (onRequest) onRequest(body);
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: { ticker: body.ticker, total_cost: 1000, fees_paid: 5, entry_price: body.entry_price, trade_plan_linked: false, initial_stop: initialStop, remaining_cash: 5000, position_id: 'new-pos-tes' },
      }),
    });
  });
}

async function gotoTradeEntry(page) {
  await page.goto('/#/TradeEntry');
  await expect(page.getByPlaceholder('e.g., AAPL or VOD.L')).toBeVisible({ timeout: 10000 });
}

// UK ticker so no FX conversion applies to the risk figure.
async function fillUkEntry(page, { entry = '100', atr = '2', shares = '10' } = {}) {
  await page.getByPlaceholder('e.g., AAPL or VOD.L').fill('LGEN');
  await page.getByPlaceholder('0.00').first().fill(entry);
  if (atr !== null) await page.getByPlaceholder('Fetched automatically if blank').fill(atr);
  await page.getByPlaceholder('0', { exact: true }).fill(shares);
}

test('SC-TES-01: the shown stop is Entry − 5×ATR and the risk is computed from it', async ({ page }) => {
  await mockFallback(page);
  await gotoTradeEntry(page);
  await fillUkEntry(page, { entry: '100', atr: '2', shares: '10' });

  await expect(page.getByTestId('system-initial-stop')).toContainText('Initial Stop (set by system)');
  await expect(page.getByTestId('system-initial-stop-value')).toHaveText('£90.00'); // 100 − 5 × 2
  await expect(page.getByTestId('system-initial-stop')).toContainText('Entry − 5× ATR (§5). This is the stop that will be stored.');
  await expect(page.getByTestId('risk-to-stop')).toHaveText('£100.00'); // (100 − 90) × 10
});

test('SC-TES-02: no input sets the stop, and the payload carries no stop_price', async ({ page }) => {
  await mockFallback(page);
  let captured = null;
  await mockAddPosition(page, { initialStop: 90, onRequest: (b) => { captured = b; } });
  await gotoTradeEntry(page);

  await expect(page.getByText(/^Stop Price/)).toHaveCount(0);
  await expect(page.getByTestId('system-initial-stop').locator('input')).toHaveCount(0);

  await fillUkEntry(page);
  await page.getByRole('button', { name: /create position/i }).click();
  await expect.poll(() => captured).not.toBeNull();
  expect(captured).not.toHaveProperty('stop_price');
  expect(captured.atr_value).toBe(2);
});

test('SC-TES-03: the ATR field is "ATR (14-day)" and not labelled optional', async ({ page }) => {
  await mockFallback(page);
  await gotoTradeEntry(page);

  await expect(page.getByLabel('ATR (14-day)')).toHaveAttribute('placeholder', 'Fetched automatically if blank');
  await expect(page.getByText(/ATR Value \(Optional\)/)).toHaveCount(0);
  await expect(page.getByText(/For stop suggestion/)).toHaveCount(0);
});

test('SC-TES-04: with ATR blank, stop and risk show "Calculated on save"', async ({ page }) => {
  await mockFallback(page);
  await gotoTradeEntry(page);
  await fillUkEntry(page, { atr: null });

  await expect(page.getByTestId('system-initial-stop-value')).toHaveText('Calculated on save');
  await expect(page.getByTestId('system-initial-stop')).toContainText('The system fetches the 14-day ATR for LGEN and sets the stop at Entry − 5× ATR.');
  await expect(page.getByTestId('risk-to-stop')).toHaveText('Calculated on save');
  await expect(page.getByTestId('sizing-empty-hint')).toHaveText('Enter an entry price and ATR to size this position.');
});

test('SC-TES-05: a trade-plan prefill shows the plan stop as a reference note only', async ({ page }) => {
  await mockFallback(page);
  await mockTradePlansList(page, [PLAN]);
  await page.goto('/#/TradePlans');
  await page.getByTestId(`start-trade-from-plan-${PLAN.id}`).click();
  await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });

  await expect(page.getByTestId('plan-stop-reference')).toHaveText(
    'Trade plan stop: $140.00. Shown for reference; the stored stop follows the strategy formula.'
  );
  await expect(page.getByTestId('system-initial-stop-value')).toHaveText('Calculated on save');
  await expect(page.locator('input[value="140"]')).toHaveCount(0);
});

test('SC-TES-06: the success toast reports the stored initial stop', async ({ page }) => {
  await mockFallback(page);
  await mockAddPosition(page, { initialStop: 90 });
  await gotoTradeEntry(page);
  await fillUkEntry(page);
  await page.getByRole('button', { name: /create position/i }).click();

  await expect(page.getByText('No matching plan found — logged unlinked. Initial stop £90.00.')).toBeVisible({ timeout: 8000 });
});
