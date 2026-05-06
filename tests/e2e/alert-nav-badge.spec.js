/**
 * Alert Notification Badge in Nav — Acceptance Tests — ST-10 (BLG-FE-05, v2.3)
 *
 * Covers non-visual AC only. Visual AC (badge colour, position, typography)
 * requires DoQ staging/local-run verification — see
 * docs/testing/alert_nav_badge_scenarios.md SC-ANB-VIS-01 through SC-ANB-VIS-05.
 *
 * Scenarios:
 *   SC-ANB-01  Alerts nav item present in Tools group
 *   SC-ANB-02  Badge hidden when alert history is empty
 *   SC-ANB-03  Badge shows full history count when no prior Alerts page visit
 *   SC-ANB-04  Badge reflects only evaluations after last-visit timestamp
 *   SC-ANB-05  Badge clears on navigation to Alerts page
 *   SC-ANB-06  Badge persists across non-Alerts page navigation
 *   SC-ANB-07  Badge displays "99+" when unacknowledged count exceeds 99
 *   SC-ANB-08  No regression: existing nav items still present after ST-10
 *
 * Spec refs:
 *   docs/specs/frontend/pages/notifications.md §Nav Alert Badge v0.3
 *   docs/design/2026-03-24__release-v2.3/alert-nav-badge/ux_spec.md
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

/** Mock GET /notifications feed (required for Alerts page to render). */
async function mockNotificationsFeed(page) {
  await page.route(/\/notifications\?page=/, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }),
    })
  );
}

/** Navigate to Watchlist page and wait for idle. */
async function gotoWatchlist(page) {
  await page.goto('/#/Watchlist');
  await page.waitForLoadState('domcontentloaded');
}

/** Navigate to Alerts/Notifications page and wait for idle. */
async function gotoAlerts(page) {
  await page.goto('/#/notifications');
  await page.waitForLoadState('domcontentloaded');
}

/** Locate the Alerts nav link in the Tools group (identified by text "Alerts" in nav). */
function alertsNavLink(page) {
  // The Alerts item is a Link with text "Alerts" inside the Tools group nav
  return page.getByRole('link', { name: 'Alerts' }).first();
}

/** Locate the red badge inside the Alerts nav link. */
function alertsNavBadge(page) {
  return alertsNavLink(page).locator('[class*="bg-red-500"]');
}

// ---------------------------------------------------------------------------
// SC-ANB-01 — Alerts nav item present in Tools group
// ---------------------------------------------------------------------------

test('SC-ANB-01: Alerts nav item visible in Tools group', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(0));
  await mockWatchlist(page);

  await gotoWatchlist(page);

  // Expand Tools group if collapsed (click the group header)
  const toolsHeader = page.getByRole('button', { name: /tools/i });
  if (await toolsHeader.isVisible()) {
    const collapsed = await toolsHeader.getAttribute('disabled');
    if (collapsed === null) {
      // Not disabled (i.e., not active group) — may need to expand
      const chevron = toolsHeader.locator('svg').first();
      const isExpanded = await alertsNavLink(page).isVisible().catch(() => false);
      if (!isExpanded) {
        await toolsHeader.click();
      }
    }
  }

  await expect(alertsNavLink(page)).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ANB-02 — Badge hidden when alert history is empty
// ---------------------------------------------------------------------------

test('SC-ANB-02: Badge hidden when alert history returns 0 evaluations', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(0));
  await mockWatchlist(page);

  await gotoWatchlist(page);

  // Badge element must not exist
  await expect(alertsNavBadge(page)).toHaveCount(0, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ANB-03 — Badge shows full history count when no prior Alerts visit
// ---------------------------------------------------------------------------

test('SC-ANB-03: Badge shows full count when no prior Alerts page visit (no sessionStorage)', async ({ page }) => {
  const evalCount = 5;
  await mockHistory(page, makeHistoryResponse(evalCount));
  await mockWatchlist(page);

  // Ensure no prior visit timestamp
  await page.addInitScript(() => sessionStorage.removeItem('alerts-last-visit'));

  await gotoWatchlist(page);

  // Badge must show count = 5
  const badge = alertsNavBadge(page);
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

  // Badge must show 1 (only the newer eval after lastVisit)
  const badge = alertsNavBadge(page);
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveText('1');
});

// ---------------------------------------------------------------------------
// SC-ANB-05 — Badge clears on navigation to Alerts page
// ---------------------------------------------------------------------------

test('SC-ANB-05: Badge count resets to 0 after navigating to Alerts page', async ({ page }) => {
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

  // Assert badge is visible with count 3
  await expect(alertsNavBadge(page)).toBeVisible({ timeout: 5000 });

  // Navigate to Alerts (notifications) page
  await gotoAlerts(page);

  // Badge must be gone
  await expect(alertsNavBadge(page)).toHaveCount(0, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ANB-06 — Badge persists across non-Alerts page navigation
// ---------------------------------------------------------------------------

test('SC-ANB-06: Badge count persists when navigating between non-Alerts pages', async ({ page }) => {
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

  // Badge visible on Watchlist
  await expect(alertsNavBadge(page)).toBeVisible({ timeout: 5000 });
  await expect(alertsNavBadge(page)).toHaveText(String(evalCount));

  // Navigate to Positions (non-Alerts page)
  await page.goto('/#/Positions');
  await page.waitForLoadState('domcontentloaded');

  // Badge still visible with same count
  await expect(alertsNavBadge(page)).toBeVisible({ timeout: 5000 });
  await expect(alertsNavBadge(page)).toHaveText(String(evalCount));
});

// ---------------------------------------------------------------------------
// SC-ANB-07 — Badge shows "99+" when count exceeds 99
// ---------------------------------------------------------------------------

test('SC-ANB-07: Badge shows "99+" when unacknowledged count > 99', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(150));
  await mockWatchlist(page);
  await page.addInitScript(() => sessionStorage.removeItem('alerts-last-visit'));

  await gotoWatchlist(page);

  const badge = alertsNavBadge(page);
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
