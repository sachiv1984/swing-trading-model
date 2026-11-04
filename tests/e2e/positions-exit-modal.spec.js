/**
 * Positions-page Exit Modal Submit
 * ST-29 (BLG-QA-237, EPIC-05, v9.14)
 *
 * Inventory: docs/testing/state_changing_action_coverage.md row 2
 * ("Confirm exit (Positions page Exit modal)", POST /positions/{id}/exit).
 * Contract: docs/specs/api_contracts/position_endpoints.md §POST /positions/{position_id}/exit
 *
 * Coverage:
 *   SC-PEM-01  Confirm Exit sends POST /positions/{id}/exit with the expected body; the modal
 *              closes and the position leaves the open list
 *   SC-PEM-02  A failed exit (400 "Position already closed", ST-10's documented error) keeps the
 *              modal open and shows the error; the position stays in the open list
 *
 * The Daily Position Monitor's exit path is covered separately by monitor-exit-queue.spec.js.
 * On the Positions page the error is shown with window.alert, not the modal's inline
 * exit-error block (BLG-FE-241), so SC-PEM-02 asserts the alert text.
 *
 * Infrastructure: Playwright page.route() network interception, under the suite's
 * API status guard. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Positions').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const POSITION = {
  id: 'pos-pem-01',
  ticker: 'AAPL',
  market: 'US',
  entry_price: 150.00,
  current_price: 155.00,
  current_price_native: 160.00,
  stop_price: 140.00,
  stop_price_native: 145.00,
  live_fx_rate: 1.25,
  fx_rate: 1.27,
  shares: 10,
  pnl: 50.00,
  pnl_percent: 3.3,
  holding_days: 30,
  grace_days_remaining: null,
  status: 'open',
  entry_date: new Date().toISOString(),
  initial_stop: 130.00,
  current_trailing_stop: 135.00,
  risk_off_exit: false,
  lifecycle_state: 'PROFITABLE',
  position_state: 'PROFITABLE',
  days_in_state: 20,
  tags: null,
  last_reviewed_at: new Date().toISOString(),
};

// The browser and this test run in the same timezone here, so the local date matches.
function localToday() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

// state.open is the list GET /positions returns; a successful exit empties it.
async function stubPositionsPage(page, state) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance') || url.includes('/grace-period-alerts') || url.includes('/gap-risk') || url.includes('/exit')) {
      return route.fallback();
    }
    return route.fulfill(json(state.open));
  });
  await page.route('**/positions/*/gap-risk', (route) =>
    route.fulfill(json({ status: 'ok', data: { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false } }))
  );
  await page.route('**/positions/compliance*', (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route('**/positions/grace-period-alerts', (route) => route.fulfill(json({ data: [] })));
  await page.route('**/portfolio/drawdown-status', (route) => route.fulfill(json({ status: 'ok', data: { threshold_breached: false } })));
  await page.route('**/portfolio/concentration-status', (route) => route.fulfill(json({ status: 'ok', data: { any_breach: false } })));
  await page.route('**/portfolio*', (route) => route.fulfill(json({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } })));
  await page.route('**/analytics/**', (route) => route.fulfill(json({ status: 'ok', data: { last_sync_at: null } })));
  await page.route('**/alerts/history**', (route) => route.fulfill(json({ data: { evaluations: [] } })));
  await page.route('**/watchlist**', (route) => route.fulfill(json({ items: [] })));
  await page.route('**/earnings/**', (route) => route.fulfill(json({ next_earnings_date: null, days_until_earnings: null })));
  // After a successful exit the page fetches the latest trade for the reflection modal; none here.
  await page.route('**/trades', (route) => route.fulfill(json({ trades: [] })));
}

async function openExitModal(page) {
  await page.goto('/#/Positions');
  await page.waitForSelector('text=AAPL', { timeout: 8000 });
  await page.locator('[aria-label="Table view"]').click();
  await page.waitForSelector('table', { timeout: 5000 });
  await page.getByRole('button', { name: 'Exit AAPL' }).click();
  const modal = page.getByRole('dialog', { name: 'Exit Position' });
  await expect(modal).toBeVisible({ timeout: 5000 });
  return modal;
}

test('SC-PEM-01: Confirm Exit posts the exit, closes the modal and removes the position', async ({ page }) => {
  const state = { open: [POSITION] };
  const exitRequests = [];
  await stubPositionsPage(page, state);
  await page.route('**/positions/pos-pem-01/exit', (route) => {
    exitRequests.push({ method: route.request().method(), body: route.request().postDataJSON() });
    state.open = [];
    return route.fulfill(json({ status: 'ok', data: { position_id: 'pos-pem-01', exit_price: 160, shares: 10 } }));
  });

  const modal = await openExitModal(page);
  await modal.getByRole('button', { name: 'Confirm Exit' }).click();

  await expect(modal).toBeHidden({ timeout: 5000 });
  expect(exitRequests).toHaveLength(1);
  const { method, body } = exitRequests[0];
  expect(method).toBe('POST');
  expect(body).toMatchObject({
    shares: 10,
    exit_price: 160,
    exit_fx_rate: 1.25,
    // ST-04 (BLG-FE-243, v9.15): the exit date defaults to the user's local date.
    exit_date: localToday(),
  });
  expect(typeof body.exit_reason).toBe('string');
  expect(body.exit_reason.length).toBeGreaterThan(0);

  await expect(page.getByText('0 active positions')).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('button', { name: 'Exit AAPL' })).toHaveCount(0);
});

test('SC-PEM-02: a failed exit keeps the modal open and shows the error', async ({ page }) => {
  const state = { open: [POSITION] };
  let exitCalls = 0;
  await stubPositionsPage(page, state);
  await page.route('**/positions/pos-pem-01/exit', (route) => {
    exitCalls += 1;
    return route.fulfill(json({ detail: 'Position already closed' }, 400));
  });
  const alertMessage = new Promise((resolve) => {
    page.once('dialog', async (dialog) => {
      resolve(dialog.message());
      await dialog.accept();
    });
  });

  const modal = await openExitModal(page);
  await modal.getByRole('button', { name: 'Confirm Exit' }).click();

  expect(await alertMessage).toBe('Failed to exit position: Position already closed');
  expect(exitCalls).toBe(1);
  await expect(modal).toBeVisible();
  await expect(modal.getByRole('button', { name: 'Confirm Exit' })).toBeEnabled();
  await expect(page.getByText('1 active position', { exact: true })).toBeVisible();
});
