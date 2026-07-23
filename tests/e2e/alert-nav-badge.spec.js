/**
 * Alert Notification Badge in Nav — Acceptance Tests — ST-10 (BLG-FE-05, v2.3)
 * Updated v1.4 (ST-02, EPIC-02, v7.7, BLG-FE-114): the "Alerts" nav item (Tools
 * group) was removed as a duplicate of "Notifications" (System group) — the
 * badge now lives on the retained "Notifications" item, propagating to the
 * System group header when that group is collapsed.
 *
 * Covers non-visual AC only. Visual AC (badge colour, position, typography)
 * requires DoQ staging/local-run verification — see
 * docs/testing/alert_nav_badge_scenarios.md SC-ANB-VIS-01 through SC-ANB-VIS-05.
 *
 * Scenarios:
 *   SC-ANB-01  Notifications nav item present in System group
 *   SC-ANB-02  Badge hidden when alert history is empty
 *   SC-ANB-03  Badge shows full history count when no prior Notifications visit (System group header, collapsed)
 *   SC-ANB-04  Badge reflects only evaluations after last-visit timestamp
 *   SC-ANB-05  Badge clears on navigation to Notifications page
 *   SC-ANB-06  Badge persists across non-Notifications page navigation
 *   SC-ANB-07  Badge displays "99+" when unacknowledged count exceeds 99
 *   SC-ANB-08  No regression: existing nav items still present after ST-10
 *
 * Spec refs:
 *   docs/specs/frontend/pages/notifications.md §Nav Alert Badge v0.5
 *   docs/specs/frontend/pages/navigation.md v1.4 §Alert Badge Integration
 *   docs/design/2026-03-24__release-v2.3/alert-nav-badge/ux_spec.md
 *   docs/design/2026-07-21__release-v7.7/nav-notification-digest-consolidation/ux_spec.md
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

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data helpers
// ---------------------------------------------------------------------------

/** Build a mock GET /alerts/history response with N evaluations. */
function makeHistoryResponse(count, baseTimestamp = null) {
  const ts = baseTimestamp || new Date(Date.now() - 60 * 60 * 1000).toISOString(); // 1h ago
  const evaluations = Array.from({ length: count }, (_, i) => ({
    id: `eval-${i + 1}`,
    evaluation_timestamp: new Date(new Date(ts).getTime() + i * 1000).toISOString(),
    rule_type: 'stop_loss_approach',
    symbol: 'AAPL',
    triggered: true,
    notification_sent: true,
    values_compared: { stop_price: 42.10, current_price: 43.50, gap_pct: 3.3, threshold_pct: 5.0 },
  }));
  return { status: 'ok', data: { evaluations, total: count } };
}

/** Mock GET /alerts/history with given response. */
async function mockHistory(page, response) {
  await page.route(/\/alerts\/history/, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(response),
    })
  );
}

/** Mock GET /watchlist (required for Watchlist page to render without cascade errors). */
async function mockWatchlist(page) {
  await page.route(/\/watchlist/, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ data: [] }),
    })
  );
}

/** Mock GET /notifications feed (required for Notifications page to render). */
async function mockNotificationsFeed(page) {
  await page.route(/\/notifications\?page=/, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }),
    })
  );
}

/** Navigate to Watchlist page (Tools group active — System group collapsed by default). */
async function gotoWatchlist(page) {
  await page.goto('/#/Watchlist');
  await page.waitForLoadState('domcontentloaded');
}

/** Navigate to the Notifications page (System group active — expanded). */
async function gotoNotifications(page) {
  await page.goto('/#/notifications');
  await page.waitForLoadState('domcontentloaded');
}

/** Locate the System group header button. */
function systemGroupHeader(page) {
  return page.getByRole('button', { name: /^system/i }).first();
}

/** Locate the badge on the System group header row (shown when System is collapsed). */
function systemGroupHeaderBadge(page) {
  return systemGroupHeader(page).locator('[class*="bg-red-500"]');
}

/** Locate the Notifications nav link (only in the DOM when System group is expanded). */
function notificationsNavLink(page) {
  return page.getByRole('link', { name: 'Notifications' }).first();
}

/** Locate the badge inside the Notifications nav link (item-level, System expanded). */
function notificationsNavBadge(page) {
  return notificationsNavLink(page).locator('[class*="bg-red-500"]');
}

// ---------------------------------------------------------------------------
// SC-ANB-01 — Notifications nav item present in System group
// ---------------------------------------------------------------------------

test('SC-ANB-01: Notifications nav item visible in System group', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(0));
  await mockWatchlist(page);

  await gotoWatchlist(page);

  // System group is not active here (Tools is) — expand it to reveal Notifications
  const systemHeader = systemGroupHeader(page);
  await expect(systemHeader).toBeVisible({ timeout: 5000 });
  const alreadyExpanded = await notificationsNavLink(page).isVisible().catch(() => false);
  if (!alreadyExpanded) {
    await systemHeader.click();
  }

  await expect(notificationsNavLink(page)).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ANB-02 — Badge hidden when alert history is empty
// ---------------------------------------------------------------------------

test('SC-ANB-02: Badge hidden when alert history returns 0 evaluations', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(0));
  await mockWatchlist(page);

  await gotoWatchlist(page);

  // Neither the collapsed-group header badge nor an item-level badge must exist
  await expect(systemGroupHeaderBadge(page)).toHaveCount(0, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ANB-03 — Badge shows full history count when no prior Notifications visit
// ---------------------------------------------------------------------------

test('SC-ANB-03: Badge shows full count when no prior Notifications page visit (no sessionStorage)', async ({ page }) => {
  const evalCount = 5;
  await mockHistory(page, makeHistoryResponse(evalCount));
  await mockWatchlist(page);

  // Ensure no prior visit timestamp
  await page.addInitScript(() => sessionStorage.removeItem('alerts-last-visit'));

  await gotoWatchlist(page);

  // Tools is active, System is collapsed by default — badge propagates to the group header
  const badge = systemGroupHeaderBadge(page);
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveText(String(evalCount));
});

// ---------------------------------------------------------------------------
// SC-ANB-04 — Badge reflects only evaluations after last-visit timestamp
// ---------------------------------------------------------------------------

test('SC-ANB-04: Badge counts only evaluations after last-visit timestamp', async ({ page }) => {
  const lastVisit = new Date(Date.now() - 30 * 60 * 1000).toISOString(); // 30 min ago
  const olderEval = {
    id: 'eval-old',
    evaluation_timestamp: new Date(Date.now() - 60 * 60 * 1000).toISOString(), // 1h ago — before lastVisit
    rule_type: 'stop_loss_approach',
    symbol: 'AAPL',
    triggered: true,
    notification_sent: true,
    values_compared: {},
  };
  const newerEval = {
    id: 'eval-new',
    evaluation_timestamp: new Date(Date.now() - 10 * 60 * 1000).toISOString(), // 10 min ago — after lastVisit
    rule_type: 'grace_period_warning',
    symbol: 'TSLA',
    triggered: true,
    notification_sent: true,
    values_compared: {},
  };

  await mockHistory(page, {
    status: 'ok',
    data: { evaluations: [olderEval, newerEval], total: 2 },
  });
  await mockWatchlist(page);

  // Set last-visit before page load so Layout reads it on mount
  await page.addInitScript((ts) => sessionStorage.setItem('alerts-last-visit', ts), lastVisit);

  await gotoWatchlist(page);

  // Badge must show 1 (only the newer eval after lastVisit), on the System group header
  const badge = systemGroupHeaderBadge(page);
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveText('1');
});

// ---------------------------------------------------------------------------
// SC-ANB-05 — Badge clears on navigation to Notifications page
// ---------------------------------------------------------------------------

test('SC-ANB-05: Badge count resets to 0 after navigating to Notifications page', async ({ page }) => {
  const evalCount = 3;
  await mockHistory(page, makeHistoryResponse(evalCount));
  await mockWatchlist(page);
  await mockNotificationsFeed(page);
  await page.route(/\/alerts\/rules$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(/\/notifications\/preferences/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { preferences: [] } }) })
  );

  await page.addInitScript(() => sessionStorage.removeItem('alerts-last-visit'));

  await gotoWatchlist(page);

  // Assert header badge is visible with count 3 (System collapsed, Tools active)
  await expect(systemGroupHeaderBadge(page)).toBeVisible({ timeout: 5000 });

  // Navigate to Notifications page (System becomes active/expanded)
  await gotoNotifications(page);

  // Badge must be gone — both the header and item-level forms
  await expect(systemGroupHeaderBadge(page)).toHaveCount(0, { timeout: 5000 });
  await expect(notificationsNavBadge(page)).toHaveCount(0, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ANB-06 — Badge persists across non-Notifications page navigation
// ---------------------------------------------------------------------------

test('SC-ANB-06: Badge count persists when navigating between non-Notifications pages', async ({ page }) => {
  const evalCount = 2;
  await mockHistory(page, makeHistoryResponse(evalCount));
  await mockWatchlist(page);
  // Stub positions to avoid cascade errors on navigation
  await page.route(/\/positions/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(/\/positions\/analyze/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({}) })
  );

  await page.addInitScript(() => sessionStorage.removeItem('alerts-last-visit'));

  await gotoWatchlist(page);

  // Badge visible on Watchlist (System group header, collapsed)
  await expect(systemGroupHeaderBadge(page)).toBeVisible({ timeout: 5000 });
  await expect(systemGroupHeaderBadge(page)).toHaveText(String(evalCount));

  // Navigate to Positions (non-Notifications page — Trading group becomes active)
  await page.goto('/#/Positions');
  await page.waitForLoadState('domcontentloaded');

  // Badge still visible with same count (System group still collapsed)
  await expect(systemGroupHeaderBadge(page)).toBeVisible({ timeout: 5000 });
  await expect(systemGroupHeaderBadge(page)).toHaveText(String(evalCount));
});

// ---------------------------------------------------------------------------
// SC-ANB-07 — Badge shows "99+" when count exceeds 99
// ---------------------------------------------------------------------------

test('SC-ANB-07: Badge shows "99+" when unacknowledged count > 99', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(150));
  await mockWatchlist(page);
  await page.addInitScript(() => sessionStorage.removeItem('alerts-last-visit'));

  await gotoWatchlist(page);

  const badge = systemGroupHeaderBadge(page);
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveText('99+');
});

// ---------------------------------------------------------------------------
// SC-ANB-08 — No regression: existing nav items still present
// ---------------------------------------------------------------------------

test('SC-ANB-08: No regression — all pre-existing nav items remain visible', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(0));
  await mockWatchlist(page);

  await gotoWatchlist(page);

  // Dashboard is ungrouped at top — always visible
  await expect(page.getByRole('link', { name: 'Dashboard' }).first()).toBeVisible({ timeout: 5000 });

  // Verify group headers present (button or text)
  for (const label of ['Trading', 'Analytics', 'Tools', 'System']) {
    await expect(page.getByText(label, { exact: true }).first()).toBeVisible({ timeout: 3000 });
  }
});
