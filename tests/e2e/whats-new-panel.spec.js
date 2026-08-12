/**
 * In-App "What's New" Panel — ST-01 (EPIC-01, v7.8) — BLG-FE-128
 *
 * Covers the observable AC for the Dashboard's new What's New card
 * (docs/specs/frontend/pages/dashboard.md §6A): shows the most recent
 * release's changelog entries, parsed server-side by GET /changelog/latest.
 *
 *   SC-WN-01  Ready state: header shows version, bullets render, in order
 *   SC-WN-02  Truncation: >8 changes shows first 8 + "+N more" trailer
 *   SC-WN-03  Empty state: data null renders "Nothing to show"
 *   SC-WN-04  Error state: request failure renders "Unable to load release notes"
 *   SC-WN-05  Loading state: spinner visible before response resolves
 *
 * Design source: docs/design/2026-07-24__release-v7.8/whats-new-panel/ux_spec.md
 * Spec ref: docs/specs/frontend/pages/dashboard.md §6A (v3.2)
 * Contract: docs/specs/api_contracts/changelog_endpoints.md
 *
 * Infrastructure: Playwright page.route() network interception, catch-all
 * fallback for any endpoint not explicitly stubbed (same approach as
 * morning-briefing.spec.js's mockFallback).
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
}

async function mockChangelogLatest(page, body) {
  await page.route(`${API}/changelog/latest`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) })
  );
}

async function gotoDashboard(page) {
  await page.goto('/#/DashboardHome');
  await expect(page.locator('[data-testid="whats-new-card"]')).toBeVisible({ timeout: 10000 });
}

test('SC-WN-01: ready state shows version header and bullets in order', async ({ page }) => {
  await mockFallback(page);
  await mockChangelogLatest(page, {
    status: 'ok',
    data: { version: 'v7.8', changes: ['First change', 'Second change', 'Third change'] },
  });

  await gotoDashboard(page);

  const card = page.locator('[data-testid="whats-new-card"]');
  await expect(card.getByText("What's New — v7.8")).toBeVisible({ timeout: 8000 });
  const items = card.locator('li');
  await expect(items).toHaveCount(3);
  await expect(items.nth(0)).toContainText('First change');
  await expect(items.nth(1)).toContainText('Second change');
  await expect(items.nth(2)).toContainText('Third change');
});

test('SC-WN-02: truncates to 8 bullets with a "+N more" trailer', async ({ page }) => {
  await mockFallback(page);
  const changes = Array.from({ length: 11 }, (_, i) => `Change number ${i + 1}`);
  await mockChangelogLatest(page, { status: 'ok', data: { version: 'v7.8', changes } });

  await gotoDashboard(page);

  const card = page.locator('[data-testid="whats-new-card"]');
  // 8 bullet <li> + 1 "+N more" <li> = 9 total <li> elements
  await expect(card.locator('li')).toHaveCount(9);
  await expect(card.getByText('+3 more')).toBeVisible();
  await expect(card.getByText('Change number 9')).toHaveCount(0);

  // ST-06 (EPIC-03, v8.6, BLG-FE-149): the bullet marker and "+N more"
  // overflow item were both missing a dark: variant (bare text-slate-500) --
  // must now carry the canonical secondary-text token pair, consistent with
  // the sibling <li> text (already text-slate-600 dark:text-slate-400).
  const bulletMarker = card.locator('li').first().locator('span').first();
  await expect(bulletMarker).toHaveClass(/text-slate-600/);
  await expect(bulletMarker).toHaveClass(/dark:text-slate-400/);

  const overflowItem = card.getByText('+3 more');
  await expect(overflowItem).toHaveClass(/text-slate-600/);
  await expect(overflowItem).toHaveClass(/dark:text-slate-400/);
});

test('SC-WN-03: empty state (data null) shows "Nothing to show"', async ({ page }) => {
  await mockFallback(page);
  await mockChangelogLatest(page, { status: 'ok', data: null });

  await gotoDashboard(page);

  const card = page.locator('[data-testid="whats-new-card"]');
  await expect(card.getByText('Nothing to show')).toBeVisible({ timeout: 8000 });
  await expect(card.getByText('Check back after the next release.')).toBeVisible();
});

test('SC-WN-04: error state shows "Unable to load release notes"', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/changelog/latest`, (route) => route.fulfill({ status: 500 }));

  await gotoDashboard(page);

  const card = page.locator('[data-testid="whats-new-card"]');
  await expect(card.getByText('Unable to load release notes')).toBeVisible({ timeout: 8000 });
});

test('SC-WN-05: loading state shows a spinner before the response resolves', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/changelog/latest`, async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { version: 'v7.8', changes: ['A change'] } }),
    });
  });

  await page.goto('/#/DashboardHome');
  const card = page.locator('[data-testid="whats-new-card"]');
  await expect(card).toBeVisible({ timeout: 10000 });
  await expect(card.locator('.animate-spin')).toBeVisible({ timeout: 2000 });
  await expect(card.getByText('A change')).toBeVisible({ timeout: 8000 });
});
