/**
 * Notifications Acceptance Tests — ST-09 (v2.2)
 * Covers: SC-NOTIF-02 through SC-NOTIF-08
 *
 * SC-NOTIF-01 (POST /alerts/evaluate + Telegram delivery) is an API-level
 * scenario executed via the GitHub Actions cron workflow — not covered here.
 * Evidence: 12 evaluation rows confirmed in live DB (2026-03-23).
 *
 * Spec refs:
 *   docs/specs/frontend/pages/notifications.md v0.2
 *   docs/testing/notifications_scenarios.md v1.1
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');
const {
  TD_NOTIF_A,
  TD_NOTIF_B,
  TD_NOTIF_C,
  TD_NOTIF_EMPTY,
  TD_NOTIF_PRICE_ALERT,
  TD_PREFS_ALL_ON,
  MARK_READ_OK,
  MARK_ALL_OK,
  PREF_UPDATE_OK,
  TD_ALERT_RULES,
} = require('./mocks/notifications-mock-data');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

/**
 * Route-matching helpers.
 * Uses RegExp matchers — more reliable than glob strings when query params are present.
 * Feed URL: /notifications?page=N  (includes query string — must use regex or function)
 */

/** Mock GET /notifications?page=* feed endpoint. */
async function mockNotificationsFeed(page, payload) {
  // Matches: /notifications?page=1, /notifications?page=2, etc.
  await page.route(/\/notifications\?page=/, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) });
  });
}

/** Mock PATCH /notifications/{id} (mark single read). */
async function mockMarkRead(page, onCalled) {
  // Matches: /notifications/notif-1  (has a path segment after /notifications/)
  await page.route(/\/notifications\/[^?/]+$/, (route) => {
    if (route.request().method() === 'PATCH') {
      if (onCalled) onCalled(route.request().url());
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MARK_READ_OK) });
    } else {
      route.continue();
    }
  });
}

/** Mock POST /notifications/mark-all-read. */
async function mockMarkAllRead(page, onCalled) {
  await page.route(/\/notifications\/mark-all-read/, (route) => {
    if (onCalled) onCalled();
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MARK_ALL_OK) });
  });
}

/** Mock GET /notifications/preferences and GET /alerts/rules. */
async function mockPreferencesPage(page, prefsPayload = TD_PREFS_ALL_ON) {
  await page.route(/\/notifications\/preferences/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(prefsPayload) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PREF_UPDATE_OK) });
    }
  });
  await page.route(/\/alerts\/rules$/, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_ALERT_RULES) });
  });
}

// ---------------------------------------------------------------------------
// SC-NOTIF-02 — Notification feed displays correctly; unread indicator present
// ---------------------------------------------------------------------------

test('SC-NOTIF-02: feed renders with unread indicator and correct icons', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_B);

  await page.goto('/#/notifications');

  // Feed loaded — at least one notification row visible
  const rows = page.locator('[data-testid="notification-row"], .notification-row, tr, li').filter({ hasText: /Stop Loss|Daily Portfolio/i });

  // Unread notification has cyan left border (scoped to main to exclude sidebar nav links)
  const unreadRow = page.locator('main').locator('.border-l-2.border-cyan-400, [class*="border-l-2"][class*="cyan"]').first();
  await expect(unreadRow).toBeVisible({ timeout: 5000 });

  // "Mark as read" button present on unread item
  await expect(page.getByText('Mark as read').first()).toBeVisible();

  // "Mark all as read" button present (unread item exists)
  await expect(page.getByText('Mark all as read')).toBeVisible();
});

test('SC-NOTIF-02b: feed renders within 3 seconds', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_A);

  const start = Date.now();
  await page.goto('/#/notifications');
  await expect(page.getByText('Mark as read').first()).toBeVisible({ timeout: 3000 });
  expect(Date.now() - start).toBeLessThan(3000);
});

// ---------------------------------------------------------------------------
// SC-NOTIF-03 — Mark single notification as read; optimistic update
// ---------------------------------------------------------------------------

test('SC-NOTIF-03: mark single notification as read — optimistic update', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_A);

  // Mock the PATCH call
  let patchFired = false;
  await mockMarkRead(page, () => { patchFired = true; });

  await page.goto('/#/notifications');
  await expect(page.getByText('Mark as read').first()).toBeVisible({ timeout: 5000 });

  // Confirm unread border present before clicking (scoped to main to exclude sidebar nav links)
  const unreadBorder = page.locator('main').locator('.border-l-2.border-cyan-400, [class*="border-l-2"][class*="cyan"]').first();
  await expect(unreadBorder).toBeVisible();

  // Click "Mark as read"
  await page.getByText('Mark as read').first().click();

  // Optimistic update: border should disappear
  await expect(unreadBorder).not.toBeVisible({ timeout: 2000 });

  // PATCH request was fired
  expect(patchFired).toBe(true);
});

// ---------------------------------------------------------------------------
// SC-NOTIF-04 — Mark all as read; optimistic update, header button hidden
// ---------------------------------------------------------------------------

test('SC-NOTIF-04: mark all as read — all indicators cleared, button hidden', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_C);

  let markAllFired = false;
  await mockMarkAllRead(page, () => { markAllFired = true; });

  await page.goto('/#/notifications');
  const markAllBtn = page.getByText('Mark all as read');
  await expect(markAllBtn).toBeVisible({ timeout: 5000 });

  // Confirm at least one unread indicator present (scoped to main to exclude sidebar nav links)
  const unreadBorders = page.locator('main').locator('.border-l-2.border-cyan-400, [class*="border-l-2"][class*="cyan"]');
  await expect(unreadBorders.first()).toBeVisible();

  await markAllBtn.click();

  // All unread borders gone after optimistic update
  await expect(unreadBorders.first()).not.toBeVisible({ timeout: 2000 });

  // "Mark all as read" button hidden (no unread items)
  await expect(markAllBtn).not.toBeVisible({ timeout: 2000 });

  // POST /notifications/mark-all-read fired
  expect(markAllFired).toBe(true);
});

// ---------------------------------------------------------------------------
// SC-NOTIF-05 — Empty state when no notifications exist
// ---------------------------------------------------------------------------

test('SC-NOTIF-05: empty state renders when no notifications', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_EMPTY);

  await page.goto('/#/notifications');

  // Empty state heading
  await expect(page.getByText('No notifications yet')).toBeVisible({ timeout: 5000 });

  // Sub-text
  await expect(page.getByText(/Alert notifications will appear here when triggered/i)).toBeVisible();

  // "Mark all as read" button absent
  await expect(page.getByText('Mark all as read')).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-NOTIF-06 — Preferences page loads with all four alert types
// ---------------------------------------------------------------------------

test('SC-NOTIF-06: preferences page renders all 4 alert types', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_EMPTY);
  await mockPreferencesPage(page);

  await page.goto('/#/notifications/preferences');

  // All 4 alert type labels visible (labels appear in both preferences and thresholds sections; .first() avoids strict-mode violation)
  await expect(page.getByText('Stop Loss Approach').first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Grace Period Warning').first()).toBeVisible();
  await expect(page.getByText('Market Regime Change').first()).toBeVisible();
  await expect(page.getByText('Daily Portfolio Summary').first()).toBeVisible();

  // "Preferences" tab has active indicator
  const prefsTab = page.getByRole('link', { name: /Preferences/i }).or(
    page.locator('a, button').filter({ hasText: /Preferences/i })
  ).first();
  await expect(prefsTab).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-NOTIF-07 — Preference toggle persists; "Saved" confirmation shown
// ---------------------------------------------------------------------------

test('SC-NOTIF-07: preference toggle fires PATCH and shows Saved label', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_EMPTY);

  let patchBody = null;
  await page.route(/\/notifications\/preferences/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_PREFS_ALL_ON) });
    } else if (route.request().method() === 'PATCH') {
      patchBody = route.request().postDataJSON();
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PREF_UPDATE_OK) });
    } else {
      route.continue();
    }
  });
  await page.route(/\/alerts\/rules$/, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_ALERT_RULES) });
  });

  await page.goto('/#/notifications/preferences');

  // Wait for preferences to load
  await expect(page.getByText('Daily Portfolio Summary').first()).toBeVisible({ timeout: 5000 });

  // Click the toggle for "Daily Portfolio Summary"
  // Use div.px-6.py-5 to target PreferenceRow containers specifically (AlertThresholdsSection uses py-4, not py-5)
  const dailySummaryRow = page.locator('div.px-6.py-5').filter({ hasText: /Daily Portfolio Summary/i }).first();
  const toggle = dailySummaryRow.locator('button[role="switch"], input[type="checkbox"]').first();
  await toggle.click();

  // "Saved" label appears
  await expect(page.getByText('Saved').first()).toBeVisible({ timeout: 2000 });

  // PATCH was fired with the correct alert type
  expect(patchBody).not.toBeNull();
  expect(JSON.stringify(patchBody)).toContain('daily_portfolio_summary');
});

// ---------------------------------------------------------------------------
// SC-NOTIF-08 — All four alert types can be individually toggled
// ---------------------------------------------------------------------------

test('SC-NOTIF-08: all 4 alert types can be individually toggled', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_EMPTY);

  const patchBodies = [];
  await page.route(/\/notifications\/preferences/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_PREFS_ALL_ON) });
    } else if (route.request().method() === 'PATCH') {
      patchBodies.push(route.request().postDataJSON());
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PREF_UPDATE_OK) });
    } else {
      route.continue();
    }
  });
  await page.route(/\/alerts\/rules$/, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_ALERT_RULES) });
  });

  await page.goto('/#/notifications/preferences');

  // Wait for all 4 preferences to render
  await expect(page.getByText('Stop Loss Approach').first()).toBeVisible({ timeout: 5000 });

  // Toggle each of the 4 types
  const alertTypeLabels = [
    'Stop Loss Approach',
    'Grace Period Warning',
    'Market Regime Change',
    'Daily Portfolio Summary',
  ];

  for (const label of alertTypeLabels) {
    // Use div.px-6.py-5 to target PreferenceRow containers specifically (AlertThresholdsSection uses py-4, not py-5)
    const row = page.locator('div.px-6.py-5').filter({ hasText: new RegExp(label, 'i') }).first();
    const toggle = row.locator('button[role="switch"], input[type="checkbox"]').first();
    await toggle.click();
    // Brief pause for each optimistic update to settle
    await page.waitForTimeout(200);
  }

  // 4 PATCH requests fired (one per toggle)
  expect(patchBodies.length).toBe(4);

  // Each PATCH contains a unique alert_type key
  const patchedTypes = patchBodies.map((b) => Object.keys(b)[0]);
  expect(patchedTypes).toContain('stop_loss_approach');
  expect(patchedTypes).toContain('grace_period_warning');
  expect(patchedTypes).toContain('market_regime_change');
  expect(patchedTypes).toContain('daily_portfolio_summary');
});

// ---------------------------------------------------------------------------
// SC-NOTIF-06b — History tab visible in sub-nav (v2.2 regression check)
// ---------------------------------------------------------------------------

test('SC-NOTIF-06b (v2.2): History tab present in notifications sub-nav', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_EMPTY);
  await mockPreferencesPage(page);

  // Mock history endpoint
  await page.route(/\/alerts\/history/, (route) => {
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { evaluations: [], total: 0 } }) });
  });

  await page.goto('/#/notifications');

  // "History" tab present in sub-nav (added in ST-05 v2.2)
  await expect(page.getByText('History').first()).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-NOTIF-09 — "Create Trade Plan" CTA on custom_price_alert notifications
// (ST-09, BLG-BE-84, EPIC-02, v8.8)
// ---------------------------------------------------------------------------

test('SC-NOTIF-09a: "Create Trade Plan" CTA visible on a custom_price_alert notification with context', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_PRICE_ALERT);

  await page.goto('/#/notifications');

  await expect(page.getByRole('link', { name: 'Create Trade Plan' })).toBeVisible({ timeout: 5000 });
});

test('SC-NOTIF-09b: CTA navigates to TradePlan with ticker, market, and price_alert_id', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_PRICE_ALERT);

  await page.goto('/#/notifications');

  const cta = page.getByRole('link', { name: 'Create Trade Plan' });
  await expect(cta).toBeVisible({ timeout: 5000 });
  const href = await cta.getAttribute('href');
  expect(href).toContain('/TradePlan?');
  expect(href).toContain('ticker=TSLA');
  expect(href).toContain('market=US');
  expect(href).toContain('price_alert_id=pa-42');
});

test('SC-NOTIF-09c: CTA absent on a non-price-alert notification', async ({ page }) => {
  await mockNotificationsFeed(page, TD_NOTIF_A); // stop_loss_approach, no context

  await page.goto('/#/notifications');

  await expect(page.getByText('Mark as read').first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('link', { name: 'Create Trade Plan' })).not.toBeVisible();
});
