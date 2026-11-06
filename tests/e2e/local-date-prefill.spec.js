/**
 * Trade, exit and cash dates default to the user's local date
 * ST-04 (BLG-FE-243, EPIC-01, v9.15)
 *
 * At 00:30 BST the UTC date is still the previous day, so a date taken from
 * toISOString() is a day early. The browser runs under Europe/London with the
 * clock fixed at 2026-07-15 00:30 BST (2026-07-14T23:30:00Z).
 *
 * Coverage:
 *   SC-LDP-01  Trade Entry's Entry Date prefills 2026-07-15
 *   SC-LDP-02  The Exit dialog's Exit Date prefills 2026-07-15, and Confirm Exit sends it
 *   SC-LDP-03  A Cash Management deposit is sent with date 2026-07-15
 *
 * Infrastructure: Playwright page.route() network interception and page.clock.setFixedTime.
 * ROUTING NOTE: App uses HashRouter.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const NOW_UTC = new Date('2026-07-14T23:30:00Z'); // 00:30 BST on 15 July
const LOCAL_DATE = '2026-07-15';

test.use({ timezoneId: 'Europe/London' });

const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

const POSITION = {
  id: 'pos-ldp-01', ticker: 'AAPL', market: 'US', entry_price: 150, current_price: 155, current_price_native: 160,
  stop_price: 140, initial_stop: 140, shares: 10, entry_date: '2026-06-01', status: 'open', pnl: 50, pnl_pct: 3.33,
  holding_days: 44, fx_rate: 1.25, live_fx_rate: 1.25, display_status: 'PROFITABLE', grace_period: false,
  stop_source: 'trailing',
};

async function stubBase(page) {
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill(json({ status: 'ok', data: { spy: { price: 500, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7600, is_risk_on: true }, fx_rate: 1.25, fx_rate_source: 'live', fx_rate_as_of: NOW_UTC.toISOString() } }))
  );
}

test.beforeEach(async ({ page }) => {
  await page.clock.setFixedTime(NOW_UTC);
});

test('SC-LDP-01: Trade Entry prefills the local date at 00:30 BST', async ({ page }) => {
  await stubBase(page);
  await page.goto('/#/TradeEntry');
  const entryDate = page.locator('input[type="date"]').first();
  await expect(entryDate).toHaveValue(LOCAL_DATE, { timeout: 10000 });
});

test('SC-LDP-02: the Exit dialog prefills the local date and sends it on Confirm Exit', async ({ page }) => {
  const exitBodies = [];
  await stubBase(page);
  await page.route(`${API}/positions**`, (route) => {
    const url = route.request().url();
    if (url.includes('/exit')) {
      exitBodies.push(route.request().postDataJSON());
      return route.fulfill(json({ status: 'ok', data: { position_id: POSITION.id, exit_price: 160, shares: 10 } }));
    }
    if (url.includes('/gap-risk')) {
      return route.fulfill(json({ status: 'ok', data: { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false } }));
    }
    if (url.includes('/compliance') || url.includes('/grace-period-alerts')) return route.fulfill(json({ status: 'ok', data: [] }));
    return route.fulfill(json([POSITION]));
  });
  await page.goto('/#/Positions');
  await page.waitForSelector('text=AAPL', { timeout: 10000 });
  await page.locator('[aria-label="Table view"]').click();
  await page.getByRole('button', { name: 'Exit AAPL' }).click();
  const modal = page.getByRole('dialog', { name: 'Exit Position' });
  await expect(modal).toBeVisible({ timeout: 5000 });
  await expect(modal.locator('input[type="date"]')).toHaveValue(LOCAL_DATE);
  await modal.getByRole('button', { name: 'Confirm Exit' }).click();
  await expect.poll(() => exitBodies.length).toBe(1);
  expect(exitBodies[0].exit_date).toBe(LOCAL_DATE);
});

test('SC-LDP-03: a Cash Management deposit is dated with the local date', async ({ page }) => {
  let body = null;
  await stubBase(page);
  await page.route(`${API}/portfolio`, (route) => route.fulfill(json({ status: 'ok', data: { cash: 1000, initial_cash: 1000 } })));
  await page.route(`${API}/positions`, (route) => route.fulfill(json([])));
  await page.route(`${API}/cash/transaction`, (route) => {
    body = route.request().postDataJSON();
    return route.fulfill(json({ status: 'ok', data: { amount: 100, type: 'deposit' } }));
  });
  await page.goto('/#/DashboardHome');
  await page.getByTestId('cash-management-trigger-desktop').click();
  const dialog = page.getByRole('dialog');
  await expect(dialog).toBeVisible({ timeout: 5000 });
  await dialog.getByLabel('Amount (£)').fill('100');
  await dialog.getByRole('button', { name: 'Add Funds' }).click();
  await expect.poll(() => body).not.toBeNull();
  expect(body.date).toBe(LOCAL_DATE);
});
