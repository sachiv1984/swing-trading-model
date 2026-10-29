/**
 * Notification Preferences inputs — typed text visible in the light theme
 * ST-23 (BLG-FE-200, EPIC-03, v9.12) — agent-mediated Director of Quality review must-fix 1
 *
 * The light-theme pass gave these inputs a white background. Their typed text
 * must then be dark (text-slate-900), not the old bare text-white. The page-level
 * axe scans could not catch this because the fields are empty or closed when the
 * scan runs, so each input is opened, filled and checked here.
 *
 * Coverage:
 *   SC-NIL-01  Alert rule create form: threshold input
 *   SC-NIL-02  Alert rule edit form: threshold input
 *   SC-NIL-03  Custom price alert create form: ticker and threshold price inputs
 *
 * Design source: docs/design/2026-10-12__release-v9.12/light-theme-support/decision_record.md §3
 * Infrastructure: Playwright page.route() network interception. No live backend.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;
const { TD_PREFS_ALL_ON, TD_ALERT_RULES } = require('./mocks/notifications-mock-data');

const API = 'http://localhost:8000';
const SLATE_900 = 'rgb(15, 23, 42)';
const WHITE = 'rgb(255, 255, 255)';

async function stub(page, rules) {
  await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(/\/notifications\/preferences/, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_PREFS_ALL_ON) })
  );
  await page.route(/\/alerts\/rules$/, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(rules) })
  );
  await page.route(/\/price-alerts$/, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function gotoPreferences(page) {
  await page.goto('/#/notifications/preferences');
  await expect(page.getByRole('heading', { name: 'Alert Thresholds' })).toBeVisible({ timeout: 10000 });
  await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);
}

/** Fill the input, then check its typed text is dark on white and passes a scoped axe contrast scan. */
async function expectVisibleTypedText(page, input, value) {
  await input.fill(value);
  await expect(input).toHaveValue(value);
  await expect(input).toHaveCSS('color', SLATE_900);
  await expect(input).toHaveCSS('background-color', WHITE);
  await page.waitForTimeout(300); // let colour transitions settle before axe reads them
  const results = await new AxeBuilder({ page }).include('input').withRules(['color-contrast']).analyze();
  expect(results.violations).toEqual([]);
}

test('SC-NIL-01: alert rule create form threshold input shows dark typed text', async ({ page }) => {
  await stub(page, { status: 'ok', data: [] });
  await gotoPreferences(page);
  await page.getByRole('button', { name: /add alert rule/i }).first().click();
  await expectVisibleTypedText(page, page.getByPlaceholder('5'), '7');
});

test('SC-NIL-02: alert rule edit form threshold input shows dark typed text', async ({ page }) => {
  await stub(page, TD_ALERT_RULES);
  await gotoPreferences(page);
  // The first rule (stop_loss_approach) is the only one with an edit control.
  await page.locator('button:has(svg[class*="lucide-pen"]), button:has(svg[class*="lucide-edit"])').first().click();
  await expectVisibleTypedText(page, page.getByPlaceholder('5'), '6');
});

test('SC-NIL-03: custom price alert ticker and threshold inputs show dark typed text', async ({ page }) => {
  await stub(page, { status: 'ok', data: [] });
  await gotoPreferences(page);
  await page.getByRole('button', { name: /add price alert/i }).first().click();
  await expectVisibleTypedText(page, page.getByPlaceholder('e.g. AAPL'), 'AAPL');
  await expectVisibleTypedText(page, page.getByPlaceholder('0.00'), '150.25');
});
