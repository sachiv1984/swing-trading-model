/**
 * Secondary-Text Contrast Remediation — ST-01/ST-02 (EPIC-01, v6.7) — BLG-FE-87/88
 *
 * Covers observable AC for the app-wide secondary-text contrast fix:
 *   SC-CTR-01  Dark theme (default): secondary-text elements resolve to slate-400
 *              (rgb(148, 163, 184)) — WCAG-AA pass (5.71:1 vs bg-slate-800),
 *              not the pre-fix slate-500 (rgb(100, 116, 139), 3.07:1 FAIL).
 *
 * Design source: docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md §3
 * Canonical class pair: text-slate-600 dark:text-slate-400 (light bare / dark: variant)
 *
 * Sampling approach: AiChatWidget's empty-state message and advisory footer are
 * fixed secondary-text instances rendered on both /positions and /signals. This
 * mirrors the audit's own documented "class-based" method (contrast_audit_findings.md
 * §Scope and Method) — verifying resolved computed colour on a representative,
 * testid-addressable sample rather than asserting all 226 remediated instances.
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const SLATE_400_RGB = 'rgb(148, 163, 184)';
const SLATE_500_RGB = 'rgb(100, 116, 139)';

async function mockCommonRoutes(page) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/positions/compliance')) {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) });
    }
  });
  await page.route('**/portfolio*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 10000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/compliance/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/alerts/history', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/signals*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

test.describe('Secondary-Text Contrast — Dark Theme (SC-CTR-01)', () => {
  test.beforeEach(async ({ page }) => {
    await mockCommonRoutes(page);
    await page.goto('/#/positions');
  });

  test('SC-CTR-01a — AI chat empty-state message resolves to slate-400, not slate-500', async ({ page }) => {
    await page.locator('[data-testid="ai-chat-open-btn"]').click();
    const empty = page.locator('[data-testid="ai-chat-empty"]');
    await expect(empty).toBeVisible({ timeout: 8000 });
    const color = await empty.evaluate((el) => getComputedStyle(el).color);
    expect(color).toBe(SLATE_400_RGB);
    expect(color).not.toBe(SLATE_500_RGB);
  });

  test('SC-CTR-01b — AI chat advisory footer resolves to slate-400, not slate-500', async ({ page }) => {
    await page.locator('[data-testid="ai-chat-open-btn"]').click();
    const footer = page.locator('[data-testid="ai-chat-advisory-footer"]');
    await expect(footer).toBeVisible({ timeout: 8000 });
    const color = await footer.evaluate((el) => getComputedStyle(el).color);
    expect(color).toBe(SLATE_400_RGB);
    expect(color).not.toBe(SLATE_500_RGB);
  });
});
