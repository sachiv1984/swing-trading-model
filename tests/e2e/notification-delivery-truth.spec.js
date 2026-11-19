/**
 * Notification delivery truth (ST-03, BLG-FE-318, EPIC-01, v9.18)
 *
 * Spec: docs/specs/frontend/pages/notifications.md v0.13 (§Notification List delivery line,
 * §Section 1: Telegram Alerts, §Channel Scope); contract alerts_endpoints.md v0.15
 * §GET /notifications (delivery_status, delivery_reason).
 *
 *   SC-NDT-01  Notification Preferences has no "email" wording; says Telegram (AC 1)
 *   SC-NDT-02  Feed: a not_sent row with telegram_not_configured shows
 *              "Not sent: Telegram not configured" (AC 2, UI half)
 *   SC-NDT-03  Feed: a not_sent row with delivery_failed shows "Not sent: Telegram delivery failed"
 *   SC-NDT-04  Feed: sent, not_requested and pending rows, and a row with no
 *              delivery_status (older API), show no delivery line
 *
 * AC 2's backend half (a new notification stored as not delivered with Telegram
 * unconfigured) is tests/test_notification_delivery_status.py.
 *
 * Fixtures follow the writer, alerts_service.get_notifications: each item has id,
 * alert_type, title, message, read, created_at, context, delivery_status, delivery_reason.
 *
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const routed = require('./fixtures/routed-pages-populated');
const { TD_PREFS_ALL_ON } = require('./mocks/notifications-mock-data');

const created = (hoursAgo) => new Date(Date.now() - hoursAgo * 3600 * 1000).toISOString();

const item = (id, title, delivery_status, delivery_reason, extra = {}) => ({
  id,
  alert_type: 'stop_loss_approach',
  title,
  message: `${title} message`,
  read: false,
  created_at: created(1),
  context: null,
  delivery_status,
  delivery_reason,
  ...extra,
});

const FEED = [
  item('n-unconf', 'Stop Loss Approach — AAA', 'not_sent', 'telegram_not_configured'),
  item('n-failed', 'Stop Loss Approach — BBB', 'not_sent', 'delivery_failed'),
  item('n-sent', 'Stop Loss Approach — CCC', 'sent', null),
  item('n-off', 'Grace Period Warning — DDD', 'not_requested', null, { alert_type: 'grace_period_warning' }),
  item('n-pending', 'Stop Loss Approach — EEE', 'pending', null),
  // An item from an API without the field (pre-v9.18 backend still deploying).
  (({ delivery_status, delivery_reason, ...rest }) => rest)(item('n-old', 'Stop Loss Approach — FFF', null, null)),
];

async function mockFeed(page) {
  await routed.catchAll(page);
  await page.route(/localhost:8000\/notifications\?/, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { notifications: FEED, total: FEED.length, page: 1, per_page: 50, has_more: false } }),
    }));
}

const rowFor = (page, title) =>
  page.getByTestId('notification-row').filter({ has: page.getByText(title, { exact: true }) });

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => window.localStorage.setItem('command-palette-tooltip-seen', 'true'));
});

test('SC-NDT-01: Notification Preferences says Telegram and has no "email" wording', async ({ page }) => {
  await routed.catchAll(page);
  // GET /notifications/preferences seeds all five types (alerts_endpoints.md), so the
  // reflection_reminder row (default off) is part of the real response.
  const prefs = {
    ...TD_PREFS_ALL_ON,
    data: { preferences: [...TD_PREFS_ALL_ON.data.preferences, { alert_type: 'reflection_reminder', email_enabled: false }] },
  };
  await page.route(/\/notifications\/preferences/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(prefs) }));
  await page.goto('/#/notifications/preferences');
  const main = page.locator('main');
  await expect(main.getByText('Stop Loss Approach').first()).toBeVisible({ timeout: 10000 });

  await expect(main.getByRole('heading', { name: 'Telegram Alerts', level: 2 })).toBeVisible();
  await expect(main.getByText('Send to Telegram', { exact: true })).toBeVisible();
  await expect(main.getByText('Choose which alerts are also sent to Telegram, and set custom thresholds.')).toBeVisible();
  await expect(main.getByText('Send to Telegram when a closed trade has no reflection after 48 hours')).toBeVisible();

  // No "email" wording anywhere on the page's visible text.
  const text = await main.innerText();
  expect(text).not.toMatch(/e-?mail/i);
});

test('SC-NDT-02: a not_sent row with Telegram unconfigured says "Not sent: Telegram not configured"', async ({ page }) => {
  await mockFeed(page);
  await page.goto('/#/notifications');
  const row = rowFor(page, 'Stop Loss Approach — AAA');
  await expect(row).toBeVisible({ timeout: 10000 });
  const line = row.getByTestId('notification-not-sent');
  await expect(line).toHaveText('Not sent: Telegram not configured');
  await expect(line).toHaveClass(/text-app-warning/);
  await expect(line.locator('svg')).toHaveAttribute('aria-hidden', 'true');
});

test('SC-NDT-03: a not_sent row whose delivery failed says "Not sent: Telegram delivery failed"', async ({ page }) => {
  await mockFeed(page);
  await page.goto('/#/notifications');
  const row = rowFor(page, 'Stop Loss Approach — BBB');
  await expect(row).toBeVisible({ timeout: 10000 });
  await expect(row.getByTestId('notification-not-sent')).toHaveText('Not sent: Telegram delivery failed');
});

test('SC-NDT-04: sent, not_requested, pending and legacy rows show no delivery line', async ({ page }) => {
  await mockFeed(page);
  await page.goto('/#/notifications');
  await expect(rowFor(page, 'Stop Loss Approach — AAA')).toBeVisible({ timeout: 10000 });
  for (const title of [
    'Stop Loss Approach — CCC',
    'Grace Period Warning — DDD',
    'Stop Loss Approach — EEE',
    'Stop Loss Approach — FFF',
  ]) {
    const row = rowFor(page, title);
    await expect(row).toBeVisible();
    await expect(row.getByTestId('notification-not-sent')).toHaveCount(0);
  }
  // Exactly the two not_sent rows carry the line.
  await expect(page.getByTestId('notification-not-sent')).toHaveCount(2);
});
