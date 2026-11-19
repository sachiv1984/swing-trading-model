/**
 * Keyboard-operable controls (ST-01, BLG-FE-311, EPIC-01, v9.18)
 *
 * AC 1: each of the four formerly mouse-only controls can be reached with Tab
 * and operated with Enter/Space, and the two toggles expose aria-expanded.
 * Every test here uses the keyboard only: Tab moves focus, Enter/Space acts.
 *
 *   SC-KOP-01  Daily Position Monitor exit selection (checkbox row)
 *   SC-KOP-02  Notification History row expansion (toggle)
 *   SC-KOP-03  Trade History AI Journal Summary (toggle)
 *   SC-KOP-04  Performance monthly heatmap tile and its detail dialog
 *   SC-KOP-05  Screener watchlist popover close button
 *
 * AC 2 (axe with the heatmap detail and the Screener popover open) is in
 * accessibility-axe-scan.spec.js.
 *
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const routed = require('./fixtures/routed-pages-populated');
const { mockAnalyticsMetrics } = require('./fixtures/analytics-metrics');
const { ALL_TRADES, ANALYTICS_SETTINGS } = require('./mocks/analytics-mock-data');

const API = 'http://localhost:8000';

/** Press Tab until `locator` has focus. Fails if it is not reached. */
async function tabTo(page, locator, maxPresses = 80) {
  for (let i = 0; i < maxPresses; i += 1) {
    await page.keyboard.press('Tab');
    if (await locator.evaluate((el) => el === document.activeElement).catch(() => false)) return;
  }
  throw new Error(`Element not reached with Tab after ${maxPresses} presses`);
}

async function expectFocused(locator) {
  await expect.poll(() => locator.evaluate((el) => el === document.activeElement)).toBe(true);
}

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => window.localStorage.setItem('command-palette-tooltip-seen', 'true'));
});

test('SC-KOP-01: Daily Position Monitor exit selection works with Tab and Space/Enter', async ({ page }) => {
  test.setTimeout(60000);
  await routed.mockDailyMonitor(page);
  await page.goto('/#/Positions');
  await page.getByTestId('daily-monitor-button').click();
  const dialog = page.getByRole('dialog');
  await expect(dialog.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible({ timeout: 10000 });

  const stopRow = dialog.getByRole('checkbox', { name: 'Select STOP for exit' });
  await expect(stopRow).toHaveAttribute('aria-checked', 'false');
  // The checkbox role hides the row's content, so the reason and prices are its description.
  await expect(stopRow).toHaveAccessibleDescription(/Current .+, stop .+, entry .+\./);
  await tabTo(page, stopRow);

  await page.keyboard.press('Space');
  await expect(stopRow).toHaveAttribute('aria-checked', 'true');
  await expect(dialog.getByText('1 position selected for exit')).toBeVisible();

  await page.keyboard.press('Enter');
  await expect(stopRow).toHaveAttribute('aria-checked', 'false');
  await expect(dialog.getByRole('button', { name: 'Exit Selected' })).toHaveCount(0);
});

test('SC-KOP-02: Notification History rows expand and collapse with Tab and Enter/Space', async ({ page }) => {
  await routed.catchAll(page);
  await page.route(/\/alerts\/history/, (route) => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      status: 'ok',
      data: {
        total: 1,
        evaluations: [{
          id: 'eval-1', evaluation_timestamp: '2026-10-05T08:00:00Z', rule_type: 'stop_loss_approach', symbol: 'AAPL',
          triggered: true, notification_sent: true,
          values_compared: { stop_price: 42.1, current_price: 43.5, gap_pct: 3.3, threshold_pct: 5.0 },
        }],
      },
    }),
  }));
  await page.goto('/#/notifications/history');
  const toggle = page.getByTestId('alert-history-expand').first();
  await expect(toggle).toBeVisible({ timeout: 10000 });
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  const detail = page.locator('#alert-history-detail-eval-1');
  await expect(detail).toHaveCount(0);

  await tabTo(page, toggle);
  await page.keyboard.press('Enter');
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');
  await expect(detail).toBeVisible();
  await expect(toggle).toHaveAttribute('aria-controls', 'alert-history-detail-eval-1');

  await page.keyboard.press('Space');
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  await expect(detail).toHaveCount(0);
});

test('SC-KOP-03: Trade History AI Journal Summary opens and closes with Tab and Enter/Space', async ({ page }) => {
  await routed.catchAll(page);
  await page.route(/\/trades$/, (route) => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      status: 'ok',
      trades: [{
        id: 'kop-t1', ticker: 'AAPL', market: 'US', entry_date: '2026-03-01', exit_date: '2026-03-15',
        entry_price: 200, exit_price: 220, shares: 10, pnl: 199.5, pnl_pct: 9.95, exit_reason: 'Target Reached', tags: [],
      }],
      total_pnl: 199.5, total_trades: 1, win_rate: 100,
    }),
  }));
  await page.goto('/#/TradeHistory');
  const toggle = page.getByTestId('ai-journal-summary-toggle');
  await expect(toggle).toBeVisible({ timeout: 15000 });
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');

  await tabTo(page, toggle);
  await page.keyboard.press('Enter');
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('#ai-journal-summary-panel')).toBeVisible();
  await expect(page.getByTestId('ai-journal-summary-generate-btn')).toBeVisible();

  await page.keyboard.press('Space');
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  await expect(page.locator('#ai-journal-summary-panel')).toHaveCount(0);
});

test('SC-KOP-04: heatmap tile opens its detail dialog by keyboard; focus moves in, stays in and returns', async ({ page }) => {
  test.setTimeout(60000);
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) }));
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ALL_TRADES) }));
  await page.route(`${API}/settings`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ANALYTICS_SETTINGS) }));
  await mockAnalyticsMetrics(page, { trades: ALL_TRADES });
  await page.goto('/#/Performance?section=analytics');
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 20000 });
  const trigger = page.locator('button[role="combobox"]').first();
  await trigger.click();
  await page.locator('[role="option"]').filter({ hasText: 'All Time' }).click();

  const tile = page.getByRole('button').filter({ hasText: '2026-01' });
  await expect(tile).toBeVisible({ timeout: 10000 });
  await expect(tile).toHaveAttribute('aria-haspopup', 'dialog');

  // Enter opens the dialog, focus moves to its close button.
  await tabTo(page, tile);
  await page.keyboard.press('Enter');
  const dialog = page.getByRole('dialog', { name: /Trades\s*—\s*Jan 2026/ });
  await expect(dialog).toBeVisible({ timeout: 5000 });
  await expect(dialog).toHaveAttribute('aria-modal', 'true');
  const close = dialog.getByRole('button', { name: 'Close' });
  await expectFocused(close);

  // Tab reaches the trade list's scroll region; Tab and Shift+Tab stay inside the dialog.
  const list = dialog.getByRole('region', { name: 'Trades closed in Jan 2026' });
  await page.keyboard.press('Tab');
  await expectFocused(list);
  await page.keyboard.press('Tab');
  await expectFocused(close);
  await page.keyboard.press('Shift+Tab');
  await expectFocused(list);

  // A click on non-focusable text inside the dialog does not let Tab escape it.
  await dialog.getByText('Total P&L').click();
  await page.keyboard.press('Tab');
  await expect.poll(() => dialog.evaluate((el) => el.contains(document.activeElement))).toBe(true);

  // Escape closes it and focus returns to the tile.
  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expectFocused(tile);

  // Space also opens it; Enter on the focused close button closes it.
  await page.keyboard.press('Space');
  await expect(dialog).toBeVisible({ timeout: 5000 });
  await expectFocused(close);
  await page.keyboard.press('Enter');
  await expect(dialog).toHaveCount(0);
  await expectFocused(tile);
});

test('SC-KOP-05: Screener watchlist popover close button is named and works by keyboard', async ({ page }) => {
  await routed.mockScreener(page);
  await page.goto('/#/Screener');
  await expect(page.locator('main').getByText('BARC').first()).toBeVisible({ timeout: 15000 });
  const open = page.locator('main').getByRole('button', { name: 'Watchlist', exact: true }).first();
  await tabTo(page, open);
  await page.keyboard.press('Enter');
  const close = page.getByRole('button', { name: 'Cancel', exact: true });
  await expect(close).toBeVisible();
  await expect(page.getByLabel('Target entry')).toBeVisible();

  await tabTo(page, close);
  await page.keyboard.press('Enter');
  await expect(close).toHaveCount(0);
});
