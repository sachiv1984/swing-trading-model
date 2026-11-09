/**
 * Nav / Notification / Digest Consolidation — Acceptance Tests
 * ST-02 (EPIC-02, v7.7, BLG-FE-114)
 *
 * Scenarios:
 *   SC-NND-01  No nav entry named "Alerts" remains (duplicate of Notifications removed)
 *   SC-NND-02  Notifications is in Today and Weekly Digest in Review (navigation.md v2.0;
 *              superseded the v1.4 "same System group" rule — ST-01, EPIC-01, v9.16, BLG-FE-250)
 *   SC-NND-03  Weekly Digest's "Alerts Fired (7d)" value links to /notifications?since_days=7
 *   SC-NND-04  Weekly Digest's "Alerts Dismissed (7d)" value links to /notifications?since_days=7&read=true
 *   SC-NND-05  Clicking the "Alerts Fired (7d)" link navigates to the filtered Notification Feed
 *   SC-NND-06  Notification Feed applies since_days/read query params from the URL to its API call
 *   SC-NND-07  Daily Portfolio Summary preference row links to the Weekly Digest page
 *
 * Spec refs:
 *   docs/specs/frontend/pages/navigation.md v2.0 §Page Placement
 *   docs/specs/frontend/pages/notifications.md v0.5
 *   docs/specs/frontend/pages/weekly_digest.md v0.2
 *   docs/specs/api_contracts/alerts_endpoints.md v0.6
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

async function stubLayout(page) {
  await page.route(/\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { evaluations: [], total: 0 } }) })
  );
  await page.route(/\/watchlist/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );
}

const DIGEST_SEED = {
  status: 'ok',
  data: {
    realised_pnl_7d: 166.10,
    unrealised_pnl_delta_7d: -42.80,
    alerts_fired_7d: 5,
    alerts_dismissed_7d: 3,
    compliance_score_current: 80.0,
    compliance_score_7d_ago: 75.0,
    staleness_hours: 18.5,
    as_of_utc: '2026-04-01T10:30:00+00:00',
  },
};

async function stubDigest(page) {
  await page.route(/\/digest\/weekly/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(DIGEST_SEED) })
  );
}

async function stubNotificationsFeed(page) {
  await page.route(/\/notifications\?/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }) })
  );
}

// ---------------------------------------------------------------------------
// SC-NND-01 — No "Alerts" nav entry remains
// ---------------------------------------------------------------------------

test('SC-NND-01: no nav entry named "Alerts" exists', async ({ page }) => {
  await stubLayout(page);
  await page.goto('/#/Watchlist');
  await page.waitForLoadState('domcontentloaded');

  // Expand every area to make sure "Alerts" isn't hiding in a collapsed one
  const nav = page.getByTestId('desktop-sidebar-nav');
  for (const key of ['today', 'portfolio', 'find', 'review', 'settings']) {
    const btn = nav.getByTestId(`nav-area-${key}`);
    await expect(btn).toBeVisible({ timeout: 5000 });
    if ((await btn.getAttribute('aria-expanded')) === 'false') await btn.click();
    await expect(btn).toHaveAttribute('aria-expanded', 'true');
  }

  await expect(nav.getByRole('link', { name: 'Alerts', exact: true })).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-NND-02 — Notifications in Today, Weekly Digest in Review (navigation.md v2.0)
// ---------------------------------------------------------------------------

test('SC-NND-02: Notifications is in the Today area and Weekly Digest in the Review area', async ({ page }) => {
  await stubLayout(page);
  await page.addInitScript(() => sessionStorage.removeItem('nav-group-collapse'));
  await page.goto('/#/Watchlist');
  await page.waitForLoadState('domcontentloaded');

  const nav = page.getByTestId('desktop-sidebar-nav');
  // Today is expanded by default; Review is collapsed while on Watchlist.
  await expect(nav.getByTestId('nav-area-today')).toHaveAttribute('aria-expanded', 'true', { timeout: 5000 });
  await expect(nav.locator('a[href="#/notifications"]')).toBeVisible();
  await expect(nav.getByRole('link', { name: 'Weekly Digest', exact: true })).toHaveCount(0);

  await nav.getByTestId('nav-area-review').click();
  await expect(nav.getByRole('link', { name: 'Weekly Digest', exact: true })).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-NND-03 / 04 — Alert-count deep-links point at the filtered Notification Feed
// ---------------------------------------------------------------------------

test('SC-NND-03: "Alerts Fired (7d)" links to /notifications?since_days=7', async ({ page }) => {
  await stubLayout(page);
  await stubDigest(page);
  await page.goto('/#/WeeklyDigest');

  const link = page.getByTestId('digest-link-alerts_fired_7d');
  await expect(link).toBeVisible({ timeout: 8000 });
  await expect(link).toHaveAttribute('href', /#\/notifications\?since_days=7$/);
});

test('SC-NND-04: "Alerts Dismissed (7d)" links to /notifications?since_days=7&read=true', async ({ page }) => {
  await stubLayout(page);
  await stubDigest(page);
  await page.goto('/#/WeeklyDigest');

  const link = page.getByTestId('digest-link-alerts_dismissed_7d');
  await expect(link).toBeVisible({ timeout: 8000 });
  await expect(link).toHaveAttribute('href', /#\/notifications\?since_days=7&read=true$/);
});

// ---------------------------------------------------------------------------
// SC-NND-05 — Clicking the link navigates to the Notification Feed
// ---------------------------------------------------------------------------

test('SC-NND-05: clicking "Alerts Fired (7d)" navigates to the Notification Feed', async ({ page }) => {
  await stubLayout(page);
  await stubDigest(page);
  await stubNotificationsFeed(page);
  await page.goto('/#/WeeklyDigest');

  await page.getByTestId('digest-link-alerts_fired_7d').click();
  await page.waitForLoadState('domcontentloaded');

  await expect(page).toHaveURL(/#\/notifications\?since_days=7$/);
  await expect(page.locator('main').getByText('Notifications', { exact: true }).first()).toBeVisible({ timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-NND-06 — Notification Feed applies since_days/read from the URL to its API call
// ---------------------------------------------------------------------------

test('SC-NND-06: Notification Feed forwards since_days/read query params to the API', async ({ page }) => {
  await stubLayout(page);

  let capturedUrl = null;
  await page.route(/\/notifications\?/, (route) => {
    capturedUrl = route.request().url();
    return route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }) });
  });

  await page.goto('/#/notifications?since_days=7&read=true');
  await page.waitForLoadState('domcontentloaded');
  await expect.poll(() => capturedUrl).not.toBeNull();

  expect(capturedUrl).toContain('since_days=7');
  expect(capturedUrl).toContain('read=true');
});

// ---------------------------------------------------------------------------
// SC-NND-07 — Daily Portfolio Summary preference row links to Weekly Digest
// ---------------------------------------------------------------------------

test('SC-NND-07: Daily Portfolio Summary preference row links to Weekly Digest page', async ({ page }) => {
  await stubLayout(page);
  await page.route(/\/notifications\/preferences/, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          preferences: [
            { alert_type: 'stop_loss_approach', email_enabled: true },
            { alert_type: 'grace_period_warning', email_enabled: true },
            { alert_type: 'market_regime_change', email_enabled: true },
            { alert_type: 'daily_portfolio_summary', email_enabled: true },
          ],
        },
      }),
    })
  );
  await page.route(/\/alerts\/rules$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(/\/price-alerts/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  await page.goto('/#/notifications/preferences');
  await page.waitForLoadState('domcontentloaded');

  // Scope to <main> — the sidebar also has a "Weekly Digest" nav link
  const link = page.locator('main').getByRole('link', { name: 'Weekly Digest' });
  await expect(link).toBeVisible({ timeout: 8000 });
  await expect(link).toHaveAttribute('href', /#\/WeeklyDigest$/);
});
