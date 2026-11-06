/**
 * v9.15 ST-12 (BLG-FE-247, EPIC-02) — the legacy widget Dashboard route is removed.
 *
 * Design source: docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md §3.3, §6
 * Spec: navigation.md §Legacy Dashboard Route
 *
 *   SC-LDR-01  /#/Dashboard lands on the Dashboard home (/) — AC 2
 *   SC-LDR-02  the redirect is a replace navigation: Back does not return to /#/Dashboard
 *   SC-LDR-03  a palette search for "Dashboard" lists exactly one "Dashboard" page entry — AC 1
 *   SC-LDR-04  the Daily Position Monitor opens from the Positions header
 *              (Product Owner ruling ESC-EXEC-20261104-05 (a))
 *   SC-LDR-05  at 375px the Positions header actions (Daily Monitor, New Position) stay in the viewport
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

async function stubApi(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
}

test.beforeEach(async ({ page }) => {
  await stubApi(page);
});

test('SC-LDR-01: /#/Dashboard lands on the Dashboard home', async ({ page }) => {
  await page.goto('/#/Dashboard');
  await expect(page).toHaveURL(/#\/$/, { timeout: 10000 });
  await expect(page.getByRole('heading', { level: 1, name: 'Dashboard' })).toBeVisible({ timeout: 10000 });
  // The legacy page's widget-editing controls are gone.
  await expect(page.getByRole('button', { name: /customize/i })).toHaveCount(0);
});

test('SC-LDR-02: the redirect replaces history, so Back does not return to /#/Dashboard', async ({ page }) => {
  await page.goto('/#/Positions');
  await page.waitForLoadState('domcontentloaded');
  await page.evaluate(() => { window.location.hash = '#/Dashboard'; });
  await expect(page).toHaveURL(/#\/$/, { timeout: 10000 });
  await page.goBack();
  await expect(page).toHaveURL(/#\/Positions$/, { timeout: 10000 });
});

test('SC-LDR-03: the command palette lists exactly one "Dashboard" page entry', async ({ page }) => {
  await page.goto('/#/Positions');
  await page.waitForLoadState('domcontentloaded');
  await page.keyboard.press('Control+k');
  const input = page.getByTestId('command-palette-input');
  await expect(input).toBeVisible();
  await input.fill('Dashboard');
  await expect(page.getByTestId('command-palette-page-DashboardHome')).toBeVisible();
  await expect(page.getByTestId('command-palette-page-Dashboard')).toHaveCount(0);
  await expect(page.getByRole('option', { name: 'Dashboard', exact: true })).toHaveCount(1);
});

test('SC-LDR-04: the Daily Position Monitor opens from the Positions header', async ({ page }) => {
  await page.goto('/#/Positions');
  await page.getByTestId('daily-monitor-button').click();
  await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible({ timeout: 10000 });
});

test('SC-LDR-05: at phone width the Positions header actions stay inside the viewport', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 800 });
  await page.goto('/#/Positions');
  for (const locator of [page.getByTestId('daily-monitor-button'), page.getByRole('button', { name: 'New Position' })]) {
    await expect(locator).toBeVisible({ timeout: 10000 });
    const box = await locator.boundingBox();
    expect(box.x).toBeGreaterThanOrEqual(0);
    expect(box.x + box.width).toBeLessThanOrEqual(375);
  }
});
