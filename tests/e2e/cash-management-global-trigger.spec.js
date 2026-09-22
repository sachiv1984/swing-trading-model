/**
 * Global Cash Management Trigger — Acceptance Tests (P1 hotfix, this session)
 *
 * Background: the widget-based Dashboard.js ("Cash Balance" tile →
 * CashManagementModal) was replaced by DashboardHome.js (EPIC-03/ST-05,
 * dashboard.md v2.0) without carrying the cash deposit/withdraw feature
 * forward. CashManagementModal and POST /cash/transaction kept working but
 * became unreachable from the shipped UI — confirmed live when a user hit
 * "Insufficient funds" adding a WDC position and had no way to add cash.
 *
 * Head of UX & Design decision (see Layout.js, above the cashModalOpen
 * state): mount the trigger globally (sidebar/header), not as a DashboardHome
 * card or a Trade-Entry-local button, so it is reachable from every page —
 * including mid Trade-Entry, without losing in-progress form state.
 *
 * Also covers the companion silent-failure fix: TradeEntry's createMutation
 * previously had no onError handler at all, and base44Client.js's doFetch
 * only read a `message` field from error responses — FastAPI's
 * HTTPException(detail=...) serialises as {"detail": "..."}, so the real
 * reason (e.g. "Insufficient funds...") was silently replaced with a generic
 * 'Request failed' with no UI feedback whatsoever.
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const MOCK_PORTFOLIO = {
  cash_balance: 500.25,
  id: 'portfolio-1',
};

async function stubCommon(page) {
  // Catch-all fallback registered first — specific routes registered after
  // it take precedence (Playwright matches most-recently-registered first).
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/portfolio`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: MOCK_PORTFOLIO }) })
  );
  await page.route(`${API}/cash/transactions?order=DESC`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(`${API}/settings`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/trade-plans`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function goto(page, hash) {
  await page.goto(hash);
  await page.waitForLoadState('domcontentloaded');
}

test.beforeEach(async ({ page }) => {
  await stubCommon(page);
});

test('SC-CASH-01: "Manage Cash" trigger is visible and opens the modal from the Dashboard', async ({ page }) => {
  await goto(page, '/#/DashboardHome');
  await expect(page.getByTestId('cash-management-trigger-desktop')).toBeVisible();
  await page.getByTestId('cash-management-trigger-desktop').click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.getByText('Cash Management')).toBeVisible();
});

test('SC-CASH-02: "Manage Cash" trigger is reachable mid Trade Entry, without losing form input', async ({ page }) => {
  await goto(page, '/#/TradeEntry');
  const tickerInput = page.getByPlaceholder('e.g., AAPL or VOD.L');
  await expect(tickerInput).toBeVisible({ timeout: 10000 });
  await tickerInput.fill('WDC');

  await page.getByTestId('cash-management-trigger-desktop').click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.getByText('Cash Management')).toBeVisible();

  // Closing the modal must not navigate away or clear the in-progress entry.
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page).toHaveURL(/#\/TradeEntry/);
  await expect(tickerInput).toHaveValue('WDC');
});

test('SC-CASH-03: modal shows the current cash balance from GET /portfolio', async ({ page }) => {
  await goto(page, '/#/DashboardHome');
  await page.getByTestId('cash-management-trigger-desktop').click();
  await expect(page.getByRole('dialog').getByText('£500.25')).toBeVisible();
});

test('SC-CASH-04: depositing funds posts to /cash/transaction and shows a success toast', async ({ page }) => {
  let postedBody = null;
  await page.route(`${API}/cash/transaction`, (route) => {
    postedBody = route.request().postDataJSON();
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { amount: 250, type: 'deposit' } }),
    });
  });

  await goto(page, '/#/DashboardHome');
  await page.getByTestId('cash-management-trigger-desktop').click();
  await page.locator('#amount').fill('250');
  await page.getByRole('button', { name: 'Add Funds' }).click();

  await expect(page.locator('[data-sonner-toast]', { hasText: 'deposited' })).toBeVisible();
  expect(postedBody).toMatchObject({ type: 'deposit', amount: 250 });
});

test('SC-CASH-05: mobile "Manage Cash" icon trigger opens the modal', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await goto(page, '/#/DashboardHome');
  await page.getByTestId('cash-management-trigger-mobile').click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.getByText('Cash Management')).toBeVisible();
});

test('SC-CASH-06: an Insufficient Funds rejection from POST /portfolio/position surfaces the real backend message as a toast', async ({ page }) => {
  await page.route(`${API}/portfolio/position`, (route) =>
    route.fulfill({
      status: 400,
      contentType: 'application/json',
      body: JSON.stringify({ detail: 'Insufficient funds. Need £1310.70, have £500.25' }),
    })
  );

  await goto(page, '/#/TradeEntry');
  const tickerInput = page.getByPlaceholder('e.g., AAPL or VOD.L');
  await expect(tickerInput).toBeVisible({ timeout: 10000 });
  await tickerInput.fill('WDC');
  await page.getByPlaceholder('0.00').first().fill('175.53'); // Fill Price
  await page.getByPlaceholder('0', { exact: true }).fill('10'); // Number of Shares

  await page.getByRole('button', { name: 'Create Position' }).click();

  await expect(
    page.locator('[data-sonner-toast]', { hasText: 'Insufficient funds. Need £1310.70, have £500.25' })
  ).toBeVisible();
  // Must stay on the form — no silent navigation away on failure.
  await expect(page).toHaveURL(/#\/TradeEntry/);
});
