/**
 * Alert History Empty State — Acceptance Tests — v9.7 ST-06 (BLG-FE-179)
 *
 * Scenarios:
 *   SC-AHE-01  Empty history renders the heading "No alert history yet" with no trailing period
 *   SC-AHE-02  Empty-state body text is still shown beneath the heading (no regression)
 *
 * Spec refs:
 *   docs/design/design_system.md §Data States (empty-state microcopy: no trailing period)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 *
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const EMPTY_HISTORY = { status: 'ok', data: { evaluations: [], total: 0 } };

test.beforeEach(async ({ page }) => {
  // Regex (not exact string) so the page's ?last_n_days=30 query string still matches.
  await page.route(/\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_HISTORY) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/portfolio/positions**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { positions: [] } }) })
  );
});

test('SC-AHE-01: empty-state heading reads "No alert history yet" with no trailing period', async ({ page }) => {
  await page.goto('/#/notifications/history');
  await page.waitForLoadState('domcontentloaded');

  const heading = page.getByText('No alert history yet', { exact: true });
  await expect(heading).toBeVisible({ timeout: 5000 });
  await expect(heading).toHaveText('No alert history yet');
});

test('SC-AHE-02: empty-state body text still shown beneath the heading', async ({ page }) => {
  await page.goto('/#/notifications/history');
  await page.waitForLoadState('domcontentloaded');

  await expect(
    page.getByText('Alert evaluations will appear here once the system has run.')
  ).toBeVisible({ timeout: 5000 });
});
