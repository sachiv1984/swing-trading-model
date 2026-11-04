/**
 * v9.15 ST-14 (BLG-FE-266, EPIC-02) — three chrome defects: version label, What's New heading, sidebar height.
 *
 * Design source: docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md §3.4, §6
 * Spec: navigation.md §Sidebar Footer and Height; dashboard.md §6A
 *
 *   SC-CHR-01  Footer shows the current release from GET /changelog/latest ("9.15" -> "v9.15"); no "v1.0.0"
 *   SC-CHR-02  A "v"-prefixed feed version is not doubled ("v9.15" -> "v9.15")
 *   SC-CHR-03  No version in the feed: no footer version text, and the heading is "What's New" (never "undefined")
 *   SC-CHR-04  With a version, the What's New heading reads "What's New — v9.15"
 *   SC-CHR-05  On a long page the desktop sidebar's background spans the viewport top to bottom
 *              at the top and at the bottom of the scroll (fixed sidebar; navigation.md "every scroll
 *              position and page length")
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

async function stub(page, latest) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(`${API}/changelog/latest`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: latest }) })
  );
}

test.beforeEach(async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
});

test('SC-CHR-01: the footer shows the current release, not v1.0.0', async ({ page }) => {
  await stub(page, { version: '9.15', changes: ['A change'] });
  await page.goto('/#/Positions');
  const footer = page.getByTestId('sidebar-footer-version').last();
  await expect(footer).toHaveText('v9.15', { timeout: 10000 });
  await expect(page.getByText('v1.0.0', { exact: true })).toHaveCount(0);
});

test('SC-CHR-02: a "v"-prefixed version is not doubled', async ({ page }) => {
  await stub(page, { version: 'v9.15', changes: ['A change'] });
  await page.goto('/#/Positions');
  await expect(page.getByTestId('sidebar-footer-version').last()).toHaveText('v9.15', { timeout: 10000 });
});

test('SC-CHR-03: no version: no footer version, heading "What\'s New" without "undefined"', async ({ page }) => {
  await stub(page, { changes: ['A change'] });
  await page.goto('/#/');
  const card = page.getByTestId('whats-new-card');
  await expect(card.getByRole('heading', { level: 2 })).toHaveText("What's New", { timeout: 10000 });
  await expect(card).not.toContainText('undefined');
  await expect(page.getByTestId('sidebar-footer-version').last()).toHaveText('');
});

test('SC-CHR-04: with a version, the heading reads "What\'s New — v9.15"', async ({ page }) => {
  await stub(page, { version: '9.15', changes: ['A change'] });
  await page.goto('/#/');
  await expect(page.getByTestId('whats-new-card').getByRole('heading', { level: 2 })).toHaveText("What's New — v9.15", { timeout: 10000 });
});

test('SC-CHR-05: the desktop sidebar background spans the viewport at the top and bottom of a long page', async ({ page }) => {
  await stub(page, { version: '9.15', changes: ['A change'] });
  await page.goto('/#/Settings');
  const aside = page.locator('aside').first();
  await expect(aside).toBeVisible({ timeout: 10000 });
  const docHeight = await page.evaluate(() => document.documentElement.scrollHeight);
  expect(docHeight).toBeGreaterThan(900); // a page longer than the viewport
  for (const y of [0, docHeight]) {
    await page.evaluate((top) => window.scrollTo(0, top), y);
    const box = await page.evaluate(() => {
      const r = document.querySelector('aside').getBoundingClientRect();
      return { top: r.top, bottom: r.bottom, innerHeight: window.innerHeight, bg: getComputedStyle(document.querySelector('aside')).backgroundColor };
    });
    expect(box.top).toBeLessThanOrEqual(0);
    expect(box.bottom).toBeGreaterThanOrEqual(box.innerHeight);
    expect(box.bg).not.toBe('rgba(0, 0, 0, 0)');
  }
});
