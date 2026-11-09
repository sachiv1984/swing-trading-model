/**
 * Nav Alert Badge Contrast Fix — ST-03 (EPIC-03, v7.8) — BLG-FE-127
 *
 * Covers the observable AC for the notification-accessibility-audit's single
 * finding: the unacknowledged-alert-count badge (`src/Layout.js`, both the
 * collapsed System-group-header instance and the item-level instance) used
 * `bg-red-500` with white count text, giving a computed contrast ratio of
 * 3.76:1 -- below the WCAG 2.1 AA 4.5:1 threshold for normal-size text (the
 * badge's 8-9px count text does not qualify for the "large text" exemption).
 * Fixed by swapping to `bg-red-600` (4.83:1).
 *
 *   SC-BC-01  Area-header badge (Today collapsed) resolves to red-600, not red-500
 *   SC-BC-02  Item-level badge (Today expanded) resolves to red-600, not red-500
 *
 * Updated v9.16 (ST-01, EPIC-01, BLG-FE-250): Notifications moved from the
 * System group to the Today area (navigation.md v2.0 §Alert Badge Integration),
 * which is expanded by default — SC-BC-01 now collapses Today explicitly.
 *
 * Design source: docs/design/2026-07-24__release-v7.8/notification-accessibility-audit/decision_record.md
 * Spec ref: docs/specs/frontend/pages/notifications.md §Nav Alert Badge (v0.7)
 * Also updates: docs/testing/alert_nav_badge_scenarios.md SC-ANB-VIS-01;
 * existing `tests/e2e/alert-nav-badge.spec.js` selectors (`[class*="bg-red-600"]`).
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const RED_600_RGB = 'rgb(220, 38, 38)';
const RED_500_RGB = 'rgb(239, 68, 68)';

function makeHistoryResponse(count) {
  const ts = new Date(Date.now() - 60 * 60 * 1000).toISOString();
  const evaluations = Array.from({ length: count }, (_, i) => ({
    id: `eval-${i + 1}`,
    evaluation_timestamp: new Date(new Date(ts).getTime() + i * 1000).toISOString(),
    rule_type: 'stop_loss_approach',
    symbol: 'AAPL',
    triggered: true,
    notification_sent: true,
    values_compared: { stop_price: 42.1, current_price: 43.5, gap_pct: 3.3, threshold_pct: 5.0 },
  }));
  return { status: 'ok', data: { evaluations, total: count } };
}

async function mockHistory(page, response) {
  await page.route(/\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(response) })
  );
}

async function mockWatchlist(page) {
  await page.route(/\/watchlist/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );
}

test('SC-BC-01: collapsed Today-header badge resolves to red-600 (fixed), not red-500', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(5));
  await mockWatchlist(page);
  await page.addInitScript(() => sessionStorage.removeItem('alerts-last-visit'));
  await page.addInitScript(() => sessionStorage.removeItem('nav-group-collapse'));

  await page.goto('/#/Watchlist');
  await page.waitForLoadState('domcontentloaded');

  const todayHeader = page.getByTestId('desktop-sidebar-nav').getByTestId('nav-area-today');
  await expect(todayHeader).toHaveAttribute('aria-expanded', 'true', { timeout: 5000 });
  await todayHeader.click();
  await expect(todayHeader).toHaveAttribute('aria-expanded', 'false');

  const badge = todayHeader.locator('[class*="bg-red-600"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  const bg = await badge.evaluate((el) => getComputedStyle(el).backgroundColor);
  expect(bg).toBe(RED_600_RGB);
  expect(bg).not.toBe(RED_500_RGB);
});

test('SC-BC-02: item-level badge (Today expanded, non-Notifications page) resolves to red-600, not red-500', async ({ page }) => {
  await mockHistory(page, makeHistoryResponse(5));
  await mockWatchlist(page);
  await page.addInitScript(() => sessionStorage.removeItem('alerts-last-visit'));
  await page.addInitScript(() => sessionStorage.removeItem('nav-group-collapse'));

  // Stay on Watchlist (count is only cleared by visiting the Notifications
  // page itself, per SC-ANB-05). Today is expanded by default, so the
  // item-level badge renders on the Notifications entry.
  await page.goto('/#/Watchlist');
  await page.waitForLoadState('domcontentloaded');

  const notificationsLink = page.getByTestId('desktop-sidebar-nav').locator('a[href="#/notifications"]');
  await expect(notificationsLink).toBeVisible({ timeout: 5000 });

  const badge = notificationsLink.locator('[class*="bg-red-600"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  const bg = await badge.evaluate((el) => getComputedStyle(el).backgroundColor);
  expect(bg).toBe(RED_600_RGB);
  expect(bg).not.toBe(RED_500_RGB);
});
