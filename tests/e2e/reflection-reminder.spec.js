/**
 * Reflection Reminder — Notification feed, re-entry to Trade History, and preference
 * (ST-04, EPIC-01, v9.6, BLG-FEAT-98)
 *
 * Design source: docs/design/2026-09-21__release-v9.6/reflection-reminder/decision_record.md §5
 * Spec: docs/specs/frontend/pages/notifications.md v0.9 (§Reflection Reminder Row, §Email Preferences)
 *
 * Covers observable AC (ST-04 AC-01, AC-02, AC-03):
 *   SC-RR-01  A reflection_reminder feed row renders its title, message and a "Write reflection" link
 *   SC-RR-02  The link opens the reflection modal for the right trade and clears the ?reflect param (Back does not reopen it)
 *   SC-RR-03  An unknown trade_id is ignored silently (no modal, no toast) and the param is still cleared
 *   SC-RR-04  "Mark as read" (the dismiss action) removes the unread indicator and calls PATCH /notifications/{id}
 *   SC-RR-05  Notification Preferences lists "Reflection Reminder", defaulting Off, and toggling it PATCHes only that type
 *   SC-RR-06  The reminder has no "Write reflection" link when its context carries no trade_id (no dead link)
 *
 * NOT covered here (server-side, by tests/test_reflection_reminder.py): the 48 h trigger, at-most-one-per-trade,
 * no reminder when a reflection is saved first, and auto-mark-read when it is saved afterwards.
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const TRADE_ID = '33333333-3333-3333-3333-333333333333';
const OTHER_TRADE_ID = '44444444-4444-4444-4444-444444444444';
const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

const REMINDER = {
  id: 'notif-rr-1',
  alert_type: 'reflection_reminder',
  title: 'Reflection Reminder — NVDA',
  message: 'NVDA closed on 2026-09-17. Take a few minutes to record what you learned.',
  read: false,
  created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
  context: { trade_id: TRADE_ID, ticker: 'NVDA', exit_date: '2026-09-17' },
};

const TRADES = [
  { id: TRADE_ID, ticker: 'NVDA', market: 'US', entry_price: 118, exit_price: 131.5, shares: 20, pnl: 270, pnl_pct: 11.4,
    holding_days: 9, exit_reason: 'MANUAL', entry_date: '2026-09-08', exit_date: '2026-09-17' },
  { id: OTHER_TRADE_ID, ticker: 'AAPL', market: 'US', entry_price: 200, exit_price: 190, shares: 5, pnl: -50, pnl_pct: -5,
    holding_days: 4, exit_reason: 'STOP', entry_date: '2026-09-10', exit_date: '2026-09-14' },
];

async function mockAll(page, { notifications = [REMINDER] } = {}) {
  const patched = [];
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(/\/notifications\?page=/, (route) =>
    route.fulfill(json({ status: 'ok', data: { notifications, has_more: false } })));
  await page.route(/\/notifications\/[^?/]+$/, (route) => {
    if (route.request().method() === 'PATCH') {
      patched.push(route.request().url());
      return route.fulfill(json({ status: 'ok', data: { ...REMINDER, read: true } }));
    }
    return route.fallback();
  });
  await page.route(/\/trades$/, (route) => route.fulfill(json({ status: 'ok', data: { trades: TRADES } })));
  await page.route(/\/analytics\/metrics/, (route) => route.fulfill(json({ status: 'ok', data: { trades_for_charts: [] } })));
  // "No reflection saved yet" is a 404 for the modal's pre-populate read
  await page.route(/\/trades\/[^/]+\/reflection$/, (route) =>
    route.fulfill(json({ status: 'error', message: 'not found' }, 404)));
  return { patched };
}

test('SC-RR-01: A reflection_reminder row renders its title, message and "Write reflection" link', async ({ page }) => {
  await mockAll(page);
  await page.goto('/#/notifications');
  await expect(page.getByText('Reflection Reminder — NVDA')).toBeVisible({ timeout: 10000 });
  await expect(page.getByText('NVDA closed on 2026-09-17. Take a few minutes to record what you learned.')).toBeVisible();
  const link = page.getByRole('link', { name: 'Write reflection' });
  await expect(link).toBeVisible();
  await expect(link).toHaveAttribute('href', `#/TradeHistory?reflect=${TRADE_ID}`);
  // Standard unread affordances are unchanged
  await expect(page.getByText('Mark as read').first()).toBeVisible();
});

test('SC-RR-02: The link opens the reflection modal for the right trade and clears ?reflect (Back does not reopen it)', async ({ page }) => {
  await mockAll(page);
  await page.goto('/#/notifications');
  await page.getByRole('link', { name: 'Write reflection' }).click();

  const modal = page.getByRole('dialog', { name: 'Trade Reflection — NVDA' });
  await expect(modal).toBeVisible({ timeout: 10000 });
  await expect(page).toHaveURL(/#\/TradeHistory$/); // param removed
  expect(page.url()).not.toContain('reflect=');

  // Close it; navigating Back must not reopen it (the param was replaced, not pushed)
  await page.keyboard.press('Escape');
  await expect(modal).toHaveCount(0);
  await page.goBack();
  await expect(page).toHaveURL(/#\/notifications/);
  await expect(page.getByRole('dialog')).toHaveCount(0);
});

test('SC-RR-03: An unknown trade_id is ignored silently — no modal, no toast — and the param is cleared', async ({ page }) => {
  await mockAll(page);
  await page.goto('/#/TradeHistory?reflect=99999999-9999-9999-9999-999999999999');
  await expect(page.getByText('NVDA').first()).toBeVisible({ timeout: 10000 }); // trades loaded
  await expect(page).toHaveURL(/#\/TradeHistory$/);
  await expect(page.getByRole('dialog')).toHaveCount(0);
  await expect(page.locator('[data-sonner-toast]')).toHaveCount(0);
});

test('SC-RR-04: "Mark as read" removes the unread indicator and calls PATCH /notifications/{id}', async ({ page }) => {
  const { patched } = await mockAll(page);
  await page.goto('/#/notifications');
  await expect(page.getByText('Reflection Reminder — NVDA')).toBeVisible({ timeout: 10000 });
  const unread = page.locator('main .border-l-2.border-cyan-400');
  await expect(unread).toHaveCount(1);
  await page.getByText('Mark as read').first().click();
  await expect(unread).toHaveCount(0);
  await expect.poll(() => patched.length).toBe(1);
  expect(patched[0]).toContain('/notifications/notif-rr-1');
  // The link stays available after dismissal (a read reminder can still be acted on)
  await expect(page.getByRole('link', { name: 'Write reflection' })).toBeVisible();
});

test('SC-RR-05: Preferences lists "Reflection Reminder" defaulting Off; toggling PATCHes only that type', async ({ page }) => {
  await mockAll(page);
  const bodies = [];
  await page.route(/\/notifications\/preferences/, (route) => {
    if (route.request().method() === 'GET') {
      return route.fulfill(json({ status: 'ok', data: { preferences: [
        { alert_type: 'stop_loss_approach', email_enabled: true },
        { alert_type: 'reflection_reminder', email_enabled: false },
      ] } }));
    }
    bodies.push(JSON.parse(route.request().postData() || '{}'));
    return route.fulfill(json({ status: 'ok', data: { preferences: [] } }));
  });
  // GET /alerts/rules returns {status, data: [rule, ...]} (see mocks/notifications-mock-data.js)
  await page.route(/\/alerts\/rules$/, (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.goto('/#/notifications/preferences');

  const row = page.locator('div.px-6.py-5', { hasText: 'Reflection Reminder' }).first();
  await expect(row).toBeVisible({ timeout: 10000 });
  await expect(row).toContainText('Notify by email when a closed trade has no reflection after 48 hours');
  const toggle = row.locator('button[role="switch"]').first();
  await expect(toggle).toHaveAttribute('aria-checked', 'false'); // default Off
  await toggle.click();
  await expect.poll(() => bodies.length, { timeout: 5000 }).toBe(1);
  expect(bodies[0]).toEqual({ reflection_reminder: { email_enabled: true } });
});

test('SC-RR-06: No "Write reflection" link is rendered when the reminder carries no trade_id', async ({ page }) => {
  await mockAll(page, { notifications: [{ ...REMINDER, context: { ticker: 'NVDA' } }] });
  await page.goto('/#/notifications');
  await expect(page.getByText('Reflection Reminder — NVDA')).toBeVisible({ timeout: 10000 });
  await expect(page.getByRole('link', { name: 'Write reflection' })).toHaveCount(0);
});
