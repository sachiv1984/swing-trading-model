/**
 * Price-Alert-to-Trade-Plan Linkage — ST-09 (EPIC-02, v8.8) — BLG-BE-84
 *
 * Covers the remainder of the round trip not exercised by
 * notifications.spec.js's SC-NOTIF-09a/b/c (which cover the CTA's presence
 * and href): navigating to TradePlan with a price_alert_id query param and
 * confirming it is included in the POST /trade-plans body on save.
 *
 * Spec ref: docs/specs/api_contracts/trade_plan_endpoints.md
 *           (triggered_by_price_alert_id, v0.12)
 * Infrastructure: Playwright page.route() network interception. No live backend.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const TICKER = 'TSLA';
const PLAN_ID = '00000000-0000-0000-0000-000000000009';
const PRICE_ALERT_ID = 'pa-42';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMarketStatus(page) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { regime_status: 'risk_on' } }),
    })
  );
}

async function mockTradePlansListEmpty(page) {
  await page.route(new RegExp(`${API}/trade-plans$`), (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    } else {
      route.continue();
    }
  });
}

test('SC-PA-TP-01: price_alert_id query param is included in POST /trade-plans body on save', async ({ page }) => {
  let capturedBody = null;

  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);

  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      const body = route.request().postDataJSON();
      capturedBody = body;
      route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { id: PLAN_ID, ...body } }),
      });
    } else {
      route.continue();
    }
  });

  await page.goto(`/#/TradePlan?ticker=${TICKER}&market=US&price_alert_id=${PRICE_ALERT_ID}`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });

  const saveBtn = page.getByRole('button', { name: /save/i });
  await saveBtn.waitFor({ timeout: 5000 });
  await saveBtn.click();

  await page.waitForTimeout(1000);
  expect(capturedBody).not.toBeNull();
  expect(capturedBody.triggered_by_price_alert_id).toBe(PRICE_ALERT_ID);
});

test('SC-PA-TP-02: no price_alert_id query param leaves triggered_by_price_alert_id null', async ({ page }) => {
  let capturedBody = null;

  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);

  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      const body = route.request().postDataJSON();
      capturedBody = body;
      route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { id: PLAN_ID, ...body } }),
      });
    } else {
      route.continue();
    }
  });

  await page.goto(`/#/TradePlan?ticker=${TICKER}&market=US`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });

  const saveBtn = page.getByRole('button', { name: /save/i });
  await saveBtn.waitFor({ timeout: 5000 });
  await saveBtn.click();

  await page.waitForTimeout(1000);
  expect(capturedBody).not.toBeNull();
  expect(capturedBody.triggered_by_price_alert_id).toBeNull();
});
