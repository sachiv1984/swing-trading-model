/**
 * Critical-Path Smoke Tests — ST-05 (BLG-QA-05)
 *
 * Covers 3 critical paths:
 *   PATH-1: Add trade   — form submits → POST /portfolio/position fires
 *   PATH-2: View portfolio — open positions render on Positions page
 *   PATH-3: View alerts    — notification feed renders with unread items
 *
 * Spec ref: stage4_backlog_slice.md#ST-05
 *
 * ── Scope constraints (§3 — carried forward from sprint planning) ──────────
 * - Playwright PASS is supporting evidence for non-visual AC only.
 * - Visual AC (colours, badges, chart rendering) remain DoQ manual review.
 * - Flaky failures are advisory — they MUST NOT block the PR.
 * - This suite does NOT replace DoQ human sign-off.
 *
 * ── Infrastructure ────────────────────────────────────────────────────────
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 *   — NOT page.goto('/path'). Path-based navigation loads Dashboard silently.
 * - Run time target: < 2 minutes for the full suite.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const {
  SMOKE_SETTINGS,
  SMOKE_POSITIONS,
  SMOKE_PORTFOLIO,
  SMOKE_SIZE_RESULT,
  SMOKE_POSITION_CREATED,
  SMOKE_NOTIFICATIONS,
} = require('./mocks/smoke-mock-data');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Shared mock helpers
// ---------------------------------------------------------------------------

/** Catch-all fallback — prevents unmocked endpoints from hanging the test. */
async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) => {
    // Only handle requests not already matched by a more specific route
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    });
  });
}

/** Mock GET /settings (loaded by TradeEntry on mount). */
async function mockSettings(page) {
  await page.route(/\/settings/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SMOKE_SETTINGS),
      });
    } else {
      route.continue();
    }
  });
}

/** Mock GET /positions (Positions page + position-tags query in TradeEntry). */
async function mockPositions(page, payload = SMOKE_POSITIONS) {
  await page.route(/\/positions(\?.*)?$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(payload),
      });
    } else {
      route.continue();
    }
  });
}

/** Mock GET /portfolio and GET /portfolio/* (excludes /portfolio/position and /portfolio/size). */
async function mockPortfolio(page) {
  await page.route(/\/portfolio$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SMOKE_PORTFOLIO),
      });
    } else {
      route.continue();
    }
  });
}

/** Mock POST /portfolio/size (PositionSizingWidget — auto-fills shares field). */
async function mockPortfolioSize(page) {
  await page.route(/\/portfolio\/size/, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(SMOKE_SIZE_RESULT),
    });
  });
}

/** Mock GET /notifications feed. */
async function mockNotificationsFeed(page, payload = SMOKE_NOTIFICATIONS) {
  await page.route(/\/notifications\?page=/, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    });
  });
}

// ---------------------------------------------------------------------------
// PATH-1: Add trade
//
// Smoke path: navigate to TradeEntry → fill form → submit → POST fires.
//
// Non-visual AC verified here:
//   - Form renders with required fields present
//   - POST /portfolio/position fires with correct ticker and entry_price
//   - App transitions away from TradeEntry on success
//
// Visual AC (button gradient, icon colours): DoQ manual review.
// ---------------------------------------------------------------------------

test('PATH-1: add trade — form submits and POST /portfolio/position fires', async ({ page }) => {
  // Set up mocks before navigation
  await mockSettings(page);
  await mockPositions(page);
  await mockPortfolio(page);
  await mockPortfolioSize(page);

  // Capture POST /portfolio/position to verify payload
  let capturedPostBody = null;
  await page.route(/\/portfolio\/position$/, (route) => {
    if (route.request().method() === 'POST') {
      capturedPostBody = route.request().postDataJSON();
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SMOKE_POSITION_CREATED),
      });
    } else {
      // GET /positions (for positions page after redirect) — already mocked above
      route.continue();
    }
  });

  await page.goto('/#/TradeEntry');

  // ── Form renders ───────────────────────────────────────────────────────
  const tickerInput = page.getByPlaceholder('e.g., AAPL or VOD.L');
  await expect(tickerInput).toBeVisible({ timeout: 10000 });

  // "Create Position" button present (disabled until form valid)
  const submitBtn = page.getByRole('button', { name: /Create Position/ });
  await expect(submitBtn).toBeVisible({ timeout: 5000 });

  // ── Fill required fields ───────────────────────────────────────────────
  // Ticker: LGEN — 4-char uppercase, auto-detected as UK market
  await tickerInput.fill('LGEN');

  // Entry price (first placeholder="0.00" input)
  const entryPriceInput = page.getByPlaceholder('0.00').first();
  await entryPriceInput.fill('2.45');

  // Stop price (last placeholder="0.00" input)
  const stopPriceInput = page.getByPlaceholder('0.00').last();
  await stopPriceInput.fill('2.15');

  // ── Wait for PositionSizingWidget to auto-fill shares ──────────────────
  // Widget debounces ~300ms, then calls POST /portfolio/size.
  // Mock returns suggested_shares=100, which auto-fills formData.shares.
  // This makes isFormValid = true and enables the Create Position button.
  await page.waitForResponse(/\/portfolio\/size/, { timeout: 5000 });

  // Wait for button to be enabled (shares now auto-filled via widget)
  await expect(submitBtn).toBeEnabled({ timeout: 3000 });

  // ── Submit ─────────────────────────────────────────────────────────────
  // Set up waitForResponse BEFORE click to avoid race condition where
  // the response arrives before the listener is registered.
  const postResponsePromise = page.waitForResponse(
    (resp) => resp.url().includes('/portfolio/position') && resp.request().method() === 'POST',
    { timeout: 5000 }
  );
  await submitBtn.click();

  // Verify POST /portfolio/position was called
  const postResponse = await postResponsePromise;
  expect(postResponse.status()).toBe(200);

  // Verify payload includes expected ticker and entry_price
  expect(capturedPostBody).not.toBeNull();
  expect(capturedPostBody.ticker).toBe('LGEN');
  expect(String(capturedPostBody.entry_price)).toBe('2.45');

  // App navigates away from TradeEntry on success
  await expect(page).toHaveURL(/Positions/, { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// PATH-2: View portfolio
//
// Smoke path: navigate to Positions page → open positions render.
//
// Non-visual AC verified here:
//   - Positions page loads and renders position data
//   - Both seeded positions (LGEN, BARC) are visible by ticker name
//
// Visual AC (P&L colour, badge styling): DoQ manual review.
// ---------------------------------------------------------------------------

test('PATH-2: view portfolio — open positions render on Positions page', async ({ page }) => {
  // Fallback registered FIRST — Playwright routes are LIFO, so specific mocks
  // registered after the fallback take precedence and won't be swallowed by it.
  await mockFallback(page);
  await mockPositions(page);
  await mockPortfolio(page);

  // Wait for the positions mock to be hit before asserting — more reliable than
  // networkidle on slow CI runners where React may not have rendered yet.
  const positionsResponse = page.waitForResponse(/\/positions(\?.*)?$/);
  await page.goto('/#/Positions');
  await positionsResponse;

  // Wait for position data — "Open Positions" is a title= attribute, not visible text.
  // LGEN is the first seeded position ticker and confirms the page has rendered data.
  await expect(page.getByText('LGEN').first()).toBeVisible({ timeout: 10000 });

  // Both seeded position tickers visible
  await expect(page.getByText('LGEN').first()).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('BARC').first()).toBeVisible({ timeout: 5000 });

  // "New Position" button present — confirms page is fully interactive
  await expect(
    page.getByRole('link', { name: /New Position/i }).or(
      page.getByRole('button', { name: /New Position/i })
    ).first()
  ).toBeVisible({ timeout: 3000 });
});

// ---------------------------------------------------------------------------
// PATH-3: View alerts
//
// Smoke path: navigate to Notifications page → notification feed renders.
//
// Non-visual AC verified here:
//   - Notification feed loads and renders notifications
//   - Unread notification is present (stop_loss_approach)
//   - "Mark as read" action is available
//
// Visual AC (unread cyan border, icon colours): DoQ manual review.
// ---------------------------------------------------------------------------

test('PATH-3: view alerts — notification feed renders with unread items', async ({ page }) => {
  // Fallback registered FIRST — Playwright routes are LIFO, so mockNotificationsFeed
  // (registered last) takes precedence and the notifications endpoint is not swallowed.
  await mockFallback(page);
  await mockNotificationsFeed(page);

  await page.goto('/#/notifications');
  await page.waitForLoadState('networkidle');

  // Notification feed has loaded — unread item title visible
  await expect(
    page.getByText('Stop Loss Approaching: LGEN').or(
      page.getByText(/Stop Loss Approach/i)
    ).first()
  ).toBeVisible({ timeout: 10000 });

  // "Mark as read" button present — confirms unread state rendered correctly
  await expect(page.getByText('Mark as read').first()).toBeVisible({ timeout: 3000 });

  // "Mark all as read" button present (at least one unread item)
  await expect(page.getByText('Mark all as read')).toBeVisible({ timeout: 3000 });
});
