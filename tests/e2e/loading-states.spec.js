/**
 * Loading State Standardisation Acceptance Tests — ST-12 (BLG-FE-02, v2.3)
 *
 * Covers non-visual AC only. Visual AC (colours, icon rendering, spinner
 * centring) requires DoQ staging/local-run verification and cannot be
 * asserted by Playwright.
 *
 * Scenarios:
 *   SC-LS-01  Positions — spinner shown while loading
 *   SC-LS-02  Positions — error state on API failure
 *   SC-LS-03  Positions — empty state when no positions
 *   SC-LS-04  Watchlist — spinner shown while loading
 *   SC-LS-05  Watchlist — error state on API failure
 *   SC-LS-06  Watchlist — empty state when no entries
 *   SC-LS-07  Notifications (Alerts) — spinner shown while loading
 *   SC-LS-08  Notifications (Alerts) — error state on API failure
 *   SC-LS-09  Notifications (Alerts) — empty state when no notifications
 *   SC-LS-10  Analytics — spinner shown while loading
 *   SC-LS-11  Analytics — error state on API failure
 *   SC-LS-12  Dashboard (Portfolio) — spinner shown while loading
 *
 * Spec refs:
 *   docs/specs/frontend/patterns/loading_states.md v1.0
 *   docs/design/2026-03-24__release-v2.3/loading-states/ux_spec.md
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
// Shared helpers
// ---------------------------------------------------------------------------

/** Delay a route by `ms` then fulfill with the given payload. */
async function mockDelayed(page, urlPattern, payload, ms = 800) {
  await page.route(urlPattern, async (route) => {
    await new Promise((r) => setTimeout(r, ms));
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    });
  });
}

/** Fulfill a route immediately with a 500 error. */
async function mockError(page, urlPattern) {
  await page.route(urlPattern, (route) =>
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ message: 'Internal server error' }),
    })
  );
}

/** Fulfill a route immediately with a 200 and given payload. */
async function mockOk(page, urlPattern, payload) {
  await page.route(urlPattern, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    })
  );
}

// Minimal base44 entity response shapes used across tests
const EMPTY_POSITIONS_ARRAY = [];
const EMPTY_TRADES = { trades: [] };
const EMPTY_WATCHLIST = { data: [] };
const EMPTY_NOTIFICATIONS = {
  data: { notifications: [], has_more: false },
};
const POPULATED_POSITIONS = [
  { id: '1', ticker: 'AAPL', market: 'US', status: 'open', entry_price: 100, shares: 10, entry_date: '2026-01-01' },
];
const PORTFOLIO_OK = {
  status: 'ok',
  data: { cash_balance: 5000, open_positions_value: 0, total_pnl: 0 },
};
const PORTFOLIO_HISTORY_EMPTY = { data: [] };
const MARKET_REGIMES_EMPTY = [];

// ---------------------------------------------------------------------------
// Helpers — per-page navigation + shared mock stubs
// ---------------------------------------------------------------------------

/** Mock all base44/backend calls Dashboard needs to avoid cascading failures. */
async function stubDashboardSidecalls(page) {
  await mockOk(page, `${API}/portfolio/history*`, PORTFOLIO_HISTORY_EMPTY);
  await mockOk(page, `${API}/cash/transactions*`, { data: [] });
  // market regimes (base44 entity call) — fulfilled via /entities path
  await page.route(/\/entities\/MarketRegime/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MARKET_REGIMES_EMPTY) })
  );
}

/** Stub the positions entity call used by Dashboard widgets. */
async function mockPositionsEntity(page, data = EMPTY_POSITIONS_ARRAY) {
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(data) })
  );
}

// ---------------------------------------------------------------------------
// SC-LS-01 — Positions: spinner shown while loading
// ---------------------------------------------------------------------------

test('SC-LS-01: Positions — spinner visible while API response is pending', async ({ page }) => {
  // Delay /positions by 1.5s so we can assert spinner before it resolves
  await mockDelayed(page, `${API}/positions`, POPULATED_POSITIONS, 1500);
  await mockOk(page, `${API}/positions/analyze`, {});

  await page.goto('/#/Positions');

  // Spinner must appear immediately
  await expect(page.locator('[class*="animate-spin"]').first()).toBeVisible({ timeout: 3000 });

  // After response arrives, spinner must disappear
  await expect(page.locator('[class*="animate-spin"]').first()).toHaveCount(0, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-LS-02 — Positions: error state on API failure
// ---------------------------------------------------------------------------

test('SC-LS-02: Positions — error state shown on API failure', async ({ page }) => {
  await mockError(page, `${API}/positions`);

  await page.goto('/#/Positions');
  await page.waitForLoadState('networkidle');

  await expect(page.getByText('Something went wrong')).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('button', { name: 'Try again' })).toBeVisible();

  // No raw HTTP status codes or stack traces in UI
  await expect(page.getByText(/500|Internal server error|stack/i)).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-LS-03 — Positions: empty state when API returns no data
// ---------------------------------------------------------------------------

test('SC-LS-03: Positions — empty state shown when no positions', async ({ page }) => {
  await mockOk(page, `${API}/positions`, EMPTY_POSITIONS_ARRAY);

  await page.goto('/#/Positions');
  await page.waitForLoadState('networkidle');

  await expect(page.getByText('No open positions')).toBeVisible({ timeout: 5000 });

  // Empty state must not look like error (no "Something went wrong")
  await expect(page.getByText('Something went wrong')).toHaveCount(0);
  // No retry button in empty state
  await expect(page.getByRole('button', { name: 'Try again' })).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-LS-04 — Watchlist: spinner shown while loading
// ---------------------------------------------------------------------------

test('SC-LS-04: Watchlist — spinner visible while API response is pending', async ({ page }) => {
  await mockDelayed(page, `${API}/watchlist`, EMPTY_WATCHLIST, 1500);

  await page.goto('/#/Watchlist');

  await expect(page.locator('[class*="animate-spin"]').first()).toBeVisible({ timeout: 3000 });
  await expect(page.locator('[class*="animate-spin"]').first()).toHaveCount(0, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-LS-05 — Watchlist: error state on API failure
// ---------------------------------------------------------------------------

test('SC-LS-05: Watchlist — error state shown on API failure', async ({ page }) => {
  await mockError(page, `${API}/watchlist`);

  await page.goto('/#/Watchlist');
  await page.waitForLoadState('networkidle');

  await expect(page.getByText('Something went wrong')).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('button', { name: 'Try again' })).toBeVisible();
  await expect(page.getByText(/500|Internal server error/i)).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-LS-06 — Watchlist: empty state when no entries
// ---------------------------------------------------------------------------

test('SC-LS-06: Watchlist — empty state shown when watchlist is empty', async ({ page }) => {
  await mockOk(page, `${API}/watchlist`, EMPTY_WATCHLIST);

  await page.goto('/#/Watchlist');
  await page.waitForLoadState('networkidle');

  await expect(page.getByText('Your watchlist is empty')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Something went wrong')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Try again' })).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-LS-07 — Notifications (Alerts): spinner shown while loading
// ---------------------------------------------------------------------------

test('SC-LS-07: Notifications — spinner visible while API response is pending', async ({ page }) => {
  await mockDelayed(page, /\/notifications\?page=/, EMPTY_NOTIFICATIONS, 1500);

  await page.goto('/#/notifications');

  await expect(page.locator('[class*="animate-spin"]').first()).toBeVisible({ timeout: 3000 });
  await expect(page.locator('[class*="animate-spin"]').first()).toHaveCount(0, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-LS-08 — Notifications (Alerts): error state on API failure
// ---------------------------------------------------------------------------

test('SC-LS-08: Notifications — error state shown on API failure', async ({ page }) => {
  await mockError(page, /\/notifications\?page=/);

  await page.goto('/#/notifications');
  await page.waitForLoadState('networkidle');

  await expect(page.getByText('Something went wrong')).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('button', { name: 'Try again' })).toBeVisible();
  await expect(page.getByText(/500|Internal server error/i)).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-LS-09 — Notifications (Alerts): empty state when no notifications
// ---------------------------------------------------------------------------

test('SC-LS-09: Notifications — empty state shown when no notifications', async ({ page }) => {
  await mockOk(page, /\/notifications\?page=/, EMPTY_NOTIFICATIONS);

  await page.goto('/#/notifications');
  await page.waitForLoadState('networkidle');

  await expect(page.getByText('No notifications yet')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Something went wrong')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Try again' })).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-LS-10 — Analytics: spinner shown while loading
// ---------------------------------------------------------------------------

test('SC-LS-10: Analytics — spinner visible while API response is pending', async ({ page }) => {
  await mockDelayed(page, `${API}/trades`, EMPTY_TRADES, 1500);
  // Settings call — stub immediately so it doesn't also delay
  await mockOk(page, /\/settings/, { data: [{ min_trades_for_analytics: 10 }] });

  await page.goto('/#/PerformanceAnalytics');

  await expect(page.locator('[class*="animate-spin"]').first()).toBeVisible({ timeout: 3000 });
  await expect(page.locator('[class*="animate-spin"]').first()).toHaveCount(0, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-LS-11 — Analytics: error state on API failure
// ---------------------------------------------------------------------------

test('SC-LS-11: Analytics — error state shown on API failure', async ({ page }) => {
  await mockError(page, `${API}/trades`);
  await mockOk(page, /\/settings/, { data: [{ min_trades_for_analytics: 10 }] });

  await page.goto('/#/PerformanceAnalytics');
  await page.waitForLoadState('networkidle');

  await expect(page.getByText('Something went wrong')).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('button', { name: 'Try again' })).toBeVisible();
  await expect(page.getByText(/500|Internal server error/i)).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-LS-12 — Dashboard (Portfolio): spinner shown while loading
// ---------------------------------------------------------------------------

test('SC-LS-12: Dashboard — spinner visible while portfolio API is pending', async ({ page }) => {
  await mockDelayed(page, `${API}/portfolio`, PORTFOLIO_OK, 1500);
  await mockPositionsEntity(page, EMPTY_POSITIONS_ARRAY);
  await stubDashboardSidecalls(page);

  await page.goto('/#/Dashboard');

  await expect(page.locator('[class*="animate-spin"]').first()).toBeVisible({ timeout: 3000 });
  await expect(page.locator('[class*="animate-spin"]').first()).toHaveCount(0, { timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-LS-13 — Retry button re-triggers the API call
// ---------------------------------------------------------------------------

test('SC-LS-13: Positions — retry button re-triggers API call after error', async ({ page }) => {
  // Phase 1: all /positions calls fail (for both queries on the page)
  const errorHandler = (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: '{"message":"error"}' });
  await page.route(`${API}/positions`, errorHandler);

  await page.goto('/#/Positions');

  // Error state appears once all retries are exhausted
  await expect(page.getByText('Something went wrong')).toBeVisible({ timeout: 10000 });

  // Phase 2: swap error route for success route before clicking retry
  await page.unroute(`${API}/positions`, errorHandler);
  await mockOk(page, `${API}/positions`, POPULATED_POSITIONS);

  // Click retry — should now succeed
  await page.getByRole('button', { name: 'Try again' }).click();

  // Data loads — error state gone, AAPL row visible
  await expect(page.getByText('AAPL')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Something went wrong')).toHaveCount(0);
});
