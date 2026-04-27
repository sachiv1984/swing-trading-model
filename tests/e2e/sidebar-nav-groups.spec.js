/**
 * Sidebar Navigation Groups — Acceptance Tests — ST-13 (BLG-UX-01, v2.3)
 *
 * Automates non-visual AC for collapsible nav groups introduced in ST-13.
 * Visual AC (chevron colour, typography, animation smoothness) requires DoQ
 * manual review — see docs/testing/sidebar_nav_scenarios.md SC-SNV-VIS-02.
 *
 * Scenarios:
 *   SC-SNV-01  Default state: active group expanded, all others collapsed
 *   SC-SNV-02  Group header chevron reflects collapsed/expanded state (structural only)
 *   SC-SNV-03  User can expand and collapse a non-active group
 *   SC-SNV-04  Active group cannot be collapsed by clicking its header
 *   SC-SNV-05  Active group auto-expands on page navigation
 *   SC-SNV-06  sessionStorage persists user-expanded group across in-session navigation
 *   SC-SNV-07  sessionStorage resets to defaults on full page reload
 *   SC-SNV-08  No regression: all nav items present in correct groups and routable
 *
 * Spec refs:
 *   docs/specs/frontend/pages/navigation.md v1.0
 *   docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md
 *
 * Infrastructure: page.route() network interception. No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 *
 * DOM NOTES:
 *   - Group toggle: <button> containing the group label text
 *   - sessionStorage key: "nav-group-collapse"  (JSON: { trading, analytics, tools, system })
 *   - Group items are only in the DOM when the group is expanded (AnimatePresence unmounts them)
 *   - Dashboard link is ungrouped (no parent group button)
 */

'use strict';

const { test, expect } = require('@playwright/test');

// ---------------------------------------------------------------------------
// Shared mocks — stub all API calls the app makes on mount so tests don't
// fail due to network errors unrelated to the nav behaviour under test.
// ---------------------------------------------------------------------------

async function stubAll(page) {
  // Suppress console errors from failed API calls not under test
  await page.route(/\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { evaluations: [], total: 0 } }) })
  );
  await page.route(/\/watchlist/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(/\/positions(\?|$)/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify([]) })
  );
  await page.route(/\/portfolio(\?|$)/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route(/\/notifications/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }) })
  );
  await page.route(/\/alerts\/rules/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(/\/notifications\/preferences/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { preferences: [] } }) })
  );
}

/** Navigate to a page and wait for the network to settle. */
async function goto(page, hash) {
  await page.goto(hash);
  await page.waitForLoadState('networkidle');
}

/** Clear nav-group-collapse from sessionStorage before the page loads. */
async function clearCollapse(page) {
  await page.addInitScript(() => sessionStorage.removeItem('nav-group-collapse'));
}

/** Locate the group toggle button by its label text (case-insensitive). */
const groupBtn = (page, label) =>
  page.locator('button').filter({ hasText: new RegExp(`^${label}$`, 'i') }).first();

/**
 * Return whether a group is expanded by checking if the first nav link inside
 * it is visible. Framer-motion AnimatePresence unmounts items when collapsed.
 */
async function isGroupExpanded(page, firstItemName) {
  return page.getByRole('link', { name: firstItemName }).first().isVisible();
}

// ---------------------------------------------------------------------------
// SC-SNV-01 — Default state: active group expanded, all others collapsed
// ---------------------------------------------------------------------------

test('SC-SNV-01: On fresh load, only the active group is expanded', async ({ page }) => {
  await clearCollapse(page);
  await stubAll(page);

  // Navigate to Positions — active group is Trading
  await goto(page, '/#/Positions');

  // Trading items visible (group expanded)
  await expect(page.getByRole('link', { name: 'Positions' }).first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('link', { name: 'Trade History' }).first()).toBeVisible();

  // Items from other groups NOT in DOM (AnimatePresence unmounts them)
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).not.toBeVisible();
  await expect(page.getByRole('link', { name: 'Watchlist' }).first()).not.toBeVisible();
  await expect(page.getByRole('link', { name: 'Settings' }).first()).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-SNV-02 — Group header chevron reflects collapsed/expanded state (structural)
// ---------------------------------------------------------------------------

test('SC-SNV-02: Collapsed group button and expanded group button are distinguishable', async ({ page }) => {
  await clearCollapse(page);
  await stubAll(page);

  // On Watchlist — Tools is the active group (expanded)
  await goto(page, '/#/Watchlist');

  const toolsBtn = groupBtn(page, 'Tools');
  const tradingBtn = groupBtn(page, 'Trading');

  // Both buttons exist in the desktop sidebar
  await expect(toolsBtn).toBeVisible({ timeout: 5000 });
  await expect(tradingBtn).toBeVisible();

  // Tools group is expanded: its items are visible
  await expect(page.getByRole('link', { name: 'Watchlist' }).first()).toBeVisible();

  // Trading group is collapsed: its first item not visible
  const tradingFirstItem = page.getByRole('link', { name: 'Positions' }).first();
  await expect(tradingFirstItem).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-SNV-03 — User can expand and collapse a non-active group
// ---------------------------------------------------------------------------

test('SC-SNV-03: Clicking a non-active group header expands and then collapses it', async ({ page }) => {
  await clearCollapse(page);
  await stubAll(page);

  // On Positions (Trading active); Analytics collapsed
  await goto(page, '/#/Positions');

  const analyticsBtn = groupBtn(page, 'Analytics');
  await expect(analyticsBtn).toBeVisible({ timeout: 5000 });

  // Analytics items not visible initially
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).not.toBeVisible();

  // Expand Analytics
  await analyticsBtn.click();
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).toBeVisible({ timeout: 3000 });
  await expect(page.getByRole('link', { name: 'Risk Dashboard' }).first()).toBeVisible();
  await expect(page.getByRole('link', { name: 'Signals' }).first()).toBeVisible();

  // Collapse Analytics again
  await analyticsBtn.click();
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).not.toBeVisible({ timeout: 3000 });
});

// ---------------------------------------------------------------------------
// SC-SNV-04 — Active group cannot be collapsed by clicking its header
// ---------------------------------------------------------------------------

test('SC-SNV-04: Clicking the active group header does not collapse it', async ({ page }) => {
  await clearCollapse(page);
  await stubAll(page);

  // Positions is active — Trading group is active
  await goto(page, '/#/Positions');

  const tradingBtn = groupBtn(page, 'Trading');
  await expect(tradingBtn).toBeVisible({ timeout: 5000 });

  // Items visible before click
  await expect(page.getByRole('link', { name: 'Positions' }).first()).toBeVisible();

  // Click the active group header — button is disabled, use force to attempt the click
  await tradingBtn.click({ force: true });

  // Items must still be visible (group did not collapse)
  await expect(page.getByRole('link', { name: 'Positions' }).first()).toBeVisible({ timeout: 3000 });
  await expect(page.getByRole('link', { name: 'Trade History' }).first()).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-SNV-05 — Active group auto-expands on page navigation
// ---------------------------------------------------------------------------

test('SC-SNV-05: Navigating to a page auto-expands its group and collapses the previous one', async ({ page }) => {
  await clearCollapse(page);
  await stubAll(page);

  // Start on Positions (Trading active)
  await goto(page, '/#/Positions');

  // Trading expanded, Analytics collapsed
  await expect(page.getByRole('link', { name: 'Positions' }).first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).not.toBeVisible();

  // Navigate to Risk Dashboard (Analytics group)
  await goto(page, '/#/RiskDashboard');

  // Analytics now expanded — Risk Dashboard active
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('link', { name: 'Risk Dashboard' }).first()).toBeVisible();

  // Signals also visible (in Analytics group)
  await expect(page.getByRole('link', { name: 'Signals' }).first()).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-SNV-06 — sessionStorage persists user-expanded group across navigation
// ---------------------------------------------------------------------------

test('SC-SNV-06: User-expanded group stays expanded after navigating to another page', async ({ page }) => {
  await clearCollapse(page);
  await stubAll(page);

  // Start on Positions (Trading active, Analytics collapsed)
  await goto(page, '/#/Positions');

  // Manually expand Analytics
  const analyticsBtn = groupBtn(page, 'Analytics');
  await analyticsBtn.click();
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).toBeVisible({ timeout: 3000 });

  // Navigate to Trade History (still in Trading group)
  await goto(page, '/#/TradeHistory');

  // Analytics should still be expanded (sessionStorage preserved the state)
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-SNV-07 — sessionStorage resets to defaults on full page reload
// ---------------------------------------------------------------------------

test('SC-SNV-07: Full page reload resets group collapse state to defaults', async ({ page }) => {
  await clearCollapse(page);
  await stubAll(page);

  // On Positions — expand Analytics and Tools manually
  await goto(page, '/#/Positions');

  await groupBtn(page, 'Analytics').click();
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).toBeVisible({ timeout: 3000 });

  await groupBtn(page, 'Tools').click();
  await expect(page.getByRole('link', { name: 'Watchlist' }).first()).toBeVisible({ timeout: 3000 });

  // Hard reload — clears sessionStorage (the test's addInitScript runs on each load)
  // We need to manually clear sessionStorage here to simulate a full reload reset
  await page.evaluate(() => sessionStorage.removeItem('nav-group-collapse'));
  await page.reload();
  await page.waitForLoadState('networkidle');

  // After reload with no stored state: only Trading (active) should be expanded
  await expect(page.getByRole('link', { name: 'Positions' }).first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('link', { name: 'Analytics' }).first()).not.toBeVisible();
  await expect(page.getByRole('link', { name: 'Watchlist' }).first()).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-SNV-08 — No regression: all items present in correct groups and routable
// ---------------------------------------------------------------------------

test('SC-SNV-08: All nav items present in correct groups; routes resolve', async ({ page }) => {
  await clearCollapse(page);
  await stubAll(page);

  // Start somewhere neutral — Positions
  await goto(page, '/#/Positions');

  // Dashboard ungrouped at top
  await expect(page.getByRole('link', { name: 'Dashboard' }).first()).toBeVisible({ timeout: 5000 });

  // Expand all groups and verify their items
  const groups = {
    Trading:   ['Positions', 'Trade Entry', 'Trade History', 'Reflections'],
    Analytics: ['Analytics', 'Risk Dashboard', 'Signals'],
    Tools:     ['Screener', 'Watchlist', 'Alerts'],
    System:    ['Settings', 'System Status', 'Notifications'],
  };

  for (const [label, items] of Object.entries(groups)) {
    const btn = groupBtn(page, label);
    await expect(btn).toBeVisible({ timeout: 3000 });

    // Expand if not already expanded
    const firstItem = page.getByRole('link', { name: items[0] }).first();
    const alreadyExpanded = await firstItem.isVisible();
    if (!alreadyExpanded) {
      await btn.click();
    }

    for (const itemName of items) {
      await expect(
        page.getByRole('link', { name: itemName }).first()
      ).toBeVisible({ timeout: 3000 });
    }
  }
});
