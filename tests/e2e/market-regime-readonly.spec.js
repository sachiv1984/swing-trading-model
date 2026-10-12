/**
 * Read-only market regime — Playwright E2E Tests
 * ST-19 (EPIC-03, v9.11, BLG-BE-140)
 *
 *   SC-MRR-01: the Dashboard's US/UK regime widgets render from GET /market/regime and the page makes
 *              no call to /positions/analyze (which fetches prices and ATR and writes stops)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

test('SC-MRR-01a: regime widgets render from GET /market/regime with no /positions/analyze call', async ({ page }) => {
  const analyzeCalls = [];
  let regimeCalls = 0;
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(/\/positions\/analyze/, (route) => {
    analyzeCalls.push(route.request().url());
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) });
  });
  await page.route(`${API}/market/regime`, (route) => {
    regimeCalls += 1;
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: [{ market: 'US', status: 'risk_on' }, { market: 'UK', status: 'risk_off' }],
        as_of: '2026-10-08T09:00:00',
      }),
    });
  });

  await page.goto('/#/Dashboard');
  // The smallest element holding both the market name and its regime badge is that card.
  const card = (name) => page.locator('div').filter({ hasText: name }).filter({ hasText: /Risk (On|Off)/ }).last();
  const us = card('US Market');
  const uk = card('UK Market');
  await expect(page.getByText('UK Market', { exact: true })).toBeVisible({ timeout: 15000 });
  await expect(uk.getByText('Risk Off')).toBeVisible({ timeout: 8000 });
  await expect(us.getByText('Risk On')).toBeVisible();
  await page.waitForLoadState('networkidle');
  expect(regimeCalls).toBeGreaterThan(0);
  expect(analyzeCalls).toEqual([]);
});
