/**
 * Split detected on an open position — ST-27 (BLG-BE-223, EPIC-05, v9.18)
 *
 * Spec: docs/specs/frontend/pages/positions.md v2.31 §Split Detected State
 * Design: docs/design/2026-11-18__release-v9.18/position-data-states/decision_record.md §2
 * Rule: claude/strategy/strategy_rules.md §9.1 (v1.28)
 *
 *   SC-SPL-01  Tier 0 sorts first; Action needed reads "Split detected — confirm adjustment";
 *              Stop and To stop read "Paused: split to confirm"; P&L % has "pre-split basis";
 *              no breach badge although 104 < 180 (the worked example on day D)
 *   SC-SPL-02  The expanded row shows the paused line with ratio, date and source
 *   SC-SPL-03  The dialog shows the title, Before → After (20 shares, 100.00, 90.00) and
 *              "Cost unchanged"; Escape cancels and the row stays in tier 0
 *   SC-SPL-04  Confirm adjustment sends one request with no body fields and refetches positions
 *   SC-SPL-05  Odd lot (3:2 on 7): the share-count input is required, the cost line shows the
 *              cash in lieu, and the entered count is sent
 *   SC-SPL-06  A failed confirmation shows the server's message in the dialog
 *   SC-SPL-07  Grid view: the same Action needed line and a paused stop tile
 *   SC-SPL-08  Narrow-screen decision card: the same line and paused cells
 *   SC-SPL-09  axe: the table with a pending split and the open dialog, light and dark
 *
 * Mock layer: page.route(). HashRouter: navigate with '/#/…'.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;
const { makePosition, stubPositionsPage } = require('./fixtures/positions-table');

// Shape from GET /positions (position_service.get_positions_with_prices +
// split_service.split_preview): native figures, the worked example.
const PENDING_2_FOR_1 = {
  id: 'split-1', ratio: 2, ratio_label: '2:1', effective_date: '2026-11-23', source: 'yahoo',
  detected_at: '2026-11-23T22:30:00+00:00',
  shares_before: 10, shares_after: 20, shares_after_exact: 20, shares_after_is_whole: true,
  entry_before: 200, entry_after: 100, stop_before: 180, stop_after: 90,
  cost_before: 2000, cost_after: 2000,
};

const PENDING_3_FOR_2_ODD = {
  id: 'split-2', ratio: 1.5, ratio_label: '3:2', effective_date: '2026-11-20', source: 'yahoo',
  detected_at: '2026-11-20T22:30:00+00:00',
  shares_before: 7, shares_after: null, shares_after_exact: 10.5, shares_after_is_whole: false,
  entry_before: 3, entry_after: 2, stop_before: 2.7, stop_after: 1.8,
  cost_before: 21, cost_after: null,
};

const SPLIT = makePosition({
  id: 'pos-mu', ticker: 'MU', market: 'US',
  entry_price: 200, current_price: 80, current_price_native: 104,
  current_trailing_stop: 138.46, current_trailing_stop_native: 180,
  stop_price: 138.46, stop_price_native: 180, initial_stop: 180,
  pnl: -738.46, pnl_percent: -48, lifecycle_state: 'LOSING', position_state: 'LOSING',
  split_pending: PENDING_2_FOR_1, split_adjustments: [],
});
const BREACH = makePosition({
  id: 'pos-brc', ticker: 'BRCH', current_price: 95, current_price_native: 95,
  current_trailing_stop: 100, current_trailing_stop_native: 100,
  split_pending: null, split_adjustments: [],
});
const ODD = makePosition({
  id: 'pos-vod', ticker: 'VOD', market: 'UK', entry_price: 3, current_price: 2.05, current_price_native: 2.05,
  current_trailing_stop: 2.7, current_trailing_stop_native: 2.7, initial_stop: 2.7, shares: 7,
  split_pending: PENDING_3_FOR_2_ODD, split_adjustments: [],
});

async function gotoTable(page, positions) {
  await stubPositionsPage(page, positions);
  await page.goto('/#/Positions');
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 10000 });
  await tableBtn.click();
  await page.waitForSelector('[data-testid="position-row"]', { timeout: 8000 });
}

const row = (page, ticker) => page.getByTestId('position-row').filter({ hasText: ticker });

async function routeConfirm(page, { status = 200, body = { status: 'ok', data: {} } } = {}) {
  const calls = [];
  await page.route('**/positions/*/split-adjustment/confirm', (route) => {
    calls.push({ url: route.request().url(), body: route.request().postDataJSON() });
    route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(body) });
  });
  return calls;
}

test.describe('Split detected (ST-27, BLG-BE-223)', () => {
  test('SC-SPL-01 — tier 0 first; paused stop cells; pre-split P&L; no breach', async ({ page }) => {
    await gotoTable(page, [BREACH, SPLIT]);
    const first = page.getByTestId('position-row').first();
    await expect(first).toContainText('MU');
    await expect(row(page, 'MU').getByTestId('action-needed')).toHaveText('Split detected — confirm adjustment');
    await expect(row(page, 'MU').getByTestId('split-detected-MU')).toHaveClass(/text-app-warning/);
    await expect(row(page, 'MU').getByTestId('stop-value')).toHaveText('Paused: split to confirm');
    await expect(row(page, 'MU').getByTestId('stop-distance')).toHaveText('Paused: split to confirm');
    await expect(row(page, 'MU').getByTestId('pnl-pre-split')).toContainText('pre-split basis');
    await expect(row(page, 'MU').getByTestId('breach-badge')).toHaveCount(0);
    // The control row without a split still shows its breach.
    await expect(row(page, 'BRCH').getByTestId('action-needed')).toHaveText('STOP REACHED');
  });

  test('SC-SPL-02 — the expanded row states what is paused and why', async ({ page }) => {
    await gotoTable(page, [SPLIT]);
    await page.getByRole('button', { name: 'Show details for MU' }).click();
    await expect(page.getByTestId('split-paused-line')).toHaveText(
      '2:1 split on 23 Nov 2026 (Yahoo Finance). Stop alerts and exit suggestions are paused for this position until you confirm.'
    );
  });

  test('SC-SPL-03 — the dialog shows Before → After; Escape cancels', async ({ page }) => {
    const calls = await routeConfirm(page);
    await gotoTable(page, [SPLIT]);
    await page.getByTestId('split-detected-MU').click();
    const dialog = page.getByTestId('split-confirm-dialog');
    await expect(dialog.getByRole('heading', { name: 'Confirm MU 2:1 split' })).toBeVisible();
    const table = dialog.getByTestId('split-before-after');
    await expect(table.getByRole('row', { name: /Shares/ })).toContainText('10');
    await expect(table.getByRole('row', { name: /Shares/ })).toContainText('20');
    await expect(table.getByRole('row', { name: /Entry price/ })).toContainText('$200.00');
    await expect(table.getByRole('row', { name: /Entry price/ })).toContainText('$100.00');
    await expect(table.getByRole('row', { name: /Stop/ })).toContainText('$180.00');
    await expect(table.getByRole('row', { name: /Stop/ })).toContainText('$90.00');
    await expect(dialog.getByTestId('split-cost-line')).toHaveText('Cost unchanged: $2,000.00');
    await expect(dialog.getByTestId('split-shares-input')).toHaveCount(0);

    await page.keyboard.press('Escape');
    await expect(dialog).toHaveCount(0);
    expect(calls).toHaveLength(0);
    await expect(row(page, 'MU').getByTestId('action-needed')).toHaveText('Split detected — confirm adjustment');
    // Focus returns to the button that opened the dialog.
    await expect(page.getByTestId('split-detected-MU')).toBeFocused();
  });

  test('SC-SPL-04 — Confirm adjustment sends one request and refetches positions', async ({ page }) => {
    const calls = await routeConfirm(page);
    await gotoTable(page, [SPLIT]);
    let positionsCalls = 0;
    page.on('request', (r) => { if (/\/positions(\?|$)/.test(new URL(r.url()).pathname + new URL(r.url()).search)) positionsCalls += 1; });
    await page.getByTestId('split-detected-MU').click();
    await page.getByTestId('split-confirm-button').click();
    await expect(page.getByTestId('split-confirm-dialog')).toHaveCount(0);
    expect(calls).toHaveLength(1);
    expect(calls[0].url).toMatch(/\/positions\/pos-mu\/split-adjustment\/confirm$/);
    expect(calls[0].body).toEqual({});
    await expect.poll(() => positionsCalls).toBeGreaterThan(0);
  });

  test('SC-SPL-05 — odd lot: the share count is required and sent; cash in lieu shown', async ({ page }) => {
    const calls = await routeConfirm(page);
    await gotoTable(page, [ODD]);
    await page.getByTestId('split-detected-VOD').click();
    const dialog = page.getByTestId('split-confirm-dialog');
    const input = dialog.getByLabel('Post-split shares');
    await expect(input).toBeVisible();
    await expect(dialog.getByText('7 × 3:2 is 10.5, not a whole number. Enter the share count your broker shows.')).toBeVisible();
    await expect(dialog.getByTestId('split-confirm-button')).toBeDisabled();
    await expect(dialog.getByTestId('split-cost-line')).toHaveText('Cost before: £21.00');
    await input.pressSequentially('10');
    await expect(dialog.getByTestId('split-cost-line')).toHaveText('Cost: £21.00 → £20.00 (cash in lieu: £1.00)');
    await dialog.getByTestId('split-confirm-button').click();
    await expect(dialog).toHaveCount(0);
    expect(calls.map((c) => c.body)).toEqual([{ shares: 10 }]);
  });

  test('SC-SPL-06 — a failed confirmation shows the server message', async ({ page }) => {
    await routeConfirm(page, { status: 400, body: { detail: 'The post-split share count must be within 1 share of 10.5 (quantity × ratio).' } });
    await gotoTable(page, [ODD]);
    await page.getByTestId('split-detected-VOD').click();
    await page.getByLabel('Post-split shares').pressSequentially('20');
    await page.getByTestId('split-confirm-button').click();
    await expect(page.getByTestId('split-confirm-error')).toHaveText(
      'The post-split share count must be within 1 share of 10.5 (quantity × ratio).'
    );
    await expect(page.getByTestId('split-confirm-dialog')).toBeVisible();
  });

  test('SC-SPL-07 — Grid view shows the same line and a paused stop', async ({ page }) => {
    await routeConfirm(page);
    await stubPositionsPage(page, [SPLIT]);
    await page.goto('/#/Positions');
    const gridBtn = page.locator('[aria-label="Grid view"]');
    await gridBtn.waitFor({ state: 'visible', timeout: 10000 });
    await gridBtn.click();
    const line = page.getByTestId('split-detected-card-line');
    await expect(line.getByTestId('split-detected-MU')).toHaveText('Split detected — confirm adjustment');
    await expect(page.getByTestId('stop-value')).toHaveText('Paused: split to confirm');
    await expect(page.getByTestId('trail-stop-breach-icon')).toHaveCount(0);
    await line.getByTestId('split-detected-MU').click();
    await expect(page.getByTestId('split-confirm-dialog')).toBeVisible();
  });

  test('SC-SPL-08 — narrow-screen card shows the same line and paused cells', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await stubPositionsPage(page, [SPLIT]);
    await page.goto('/#/Positions');
    const tableBtn = page.locator('[aria-label="Table view"]');
    await tableBtn.waitFor({ state: 'visible', timeout: 10000 });
    await tableBtn.click();
    const card = page.getByTestId('position-decision-card').filter({ hasText: 'MU' });
    await expect(card.getByTestId('action-needed')).toHaveText('Split detected — confirm adjustment', { timeout: 10000 });
    await expect(card.getByTestId('stop-value')).toHaveText('Paused: split to confirm');
    await expect(card.getByTestId('stop-distance')).toHaveText('Paused: split to confirm');
  });

  for (const theme of ['light', 'dark']) {
    test(`SC-SPL-09 — axe: pending split row and open dialog (${theme})`, async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await routeConfirm(page);
      await gotoTable(page, [SPLIT, ODD]);
      await page.getByRole('button', { name: 'Show details for MU' }).click();
      const tableScan = await new AxeBuilder({ page }).analyze();
      const blocking = (r) => r.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical').map((v) => v.id);
      expect(blocking(tableScan)).toEqual([]);
      await page.getByTestId('split-detected-VOD').click();
      await expect(page.getByTestId('split-confirm-dialog')).toBeVisible();
      await page.waitForTimeout(400); // dialog entrance animation (runAxeScan waits the same way)
      const dialogScan = await new AxeBuilder({ page }).include('[data-testid="split-confirm-dialog"]').analyze();
      expect(blocking(dialogScan)).toEqual([]);
    });
  }
});
