/**
 * Alert Thresholds Empty State — Acceptance Tests — ST-11 (BLG-FE-04, v2.3)
 *
 * Covers non-visual AC only. Visual AC (button colour, icon rendering) requires
 * DoQ staging/local-run verification and cannot be asserted by Playwright.
 *
 * Scenarios:
 *   SC-ATS-01  CTA button present in empty state
 *   SC-ATS-02  CTA button opens create form on click
 *   SC-ATS-03  Create form: alert type selector present with all 4 types
 *   SC-ATS-04  Create form: threshold input shown for stop_loss_approach; hidden for others
 *   SC-ATS-05  Create form: threshold validation — non-numeric value
 *   SC-ATS-06  Create form: threshold validation — value ≤ 0
 *   SC-ATS-07  Create form: threshold validation — value > 50
 *   SC-ATS-08  Create form: successful save fires POST /alerts/rules and refreshes list
 *   SC-ATS-09  Create form: API error shows inline message
 *   SC-ATS-10  Create form: Cancel closes form, CTA button re-appears
 *   SC-ATS-11  Populated state: no regression — CTA button absent when rules exist
 *
 * Spec refs:
 *   docs/specs/frontend/pages/notifications.md §Section 2 v0.3
 *   Known deviation: DEV-EPIC02-ST04-01
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
const { TD_NOTIF_EMPTY, TD_PREFS_ALL_ON, TD_ALERT_RULES } = require('./mocks/notifications-mock-data');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

const EMPTY_RULES = { status: 'ok', data: [] };

/** Mock GET /notifications feed (needed for preferences page to load). */
async function mockFeed(page) {
  await page.route(/\/notifications\?page=/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_NOTIF_EMPTY) })
  );
}

/** Mock GET /notifications/preferences. */
async function mockPrefs(page) {
  await page.route(/\/notifications\/preferences/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_PREFS_ALL_ON) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) });
    }
  });
}

/** Mock GET /alerts/rules — returns empty list. */
async function mockRulesEmpty(page) {
  await page.route(/\/alerts\/rules$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_RULES) });
    } else {
      route.continue();
    }
  });
}

/** Mock GET /alerts/rules — returns populated list. */
async function mockRulesPopulated(page) {
  await page.route(/\/alerts\/rules$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_ALERT_RULES) });
    } else {
      route.continue();
    }
  });
}

/** Navigate to the preferences page and wait for the thresholds section to load. */
async function gotoPreferences(page) {
  await page.goto('/#/notifications/preferences');
  await page.waitForLoadState('networkidle');
}

// ---------------------------------------------------------------------------
// SC-ATS-01 — CTA button present in empty state
// ---------------------------------------------------------------------------

test('SC-ATS-01: "Add alert rule" CTA button visible in empty state', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesEmpty(page);

  await gotoPreferences(page);

  await expect(page.getByRole('button', { name: 'Add alert rule' })).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-ATS-02 — CTA button opens create form on click
// ---------------------------------------------------------------------------

test('SC-ATS-02: clicking "Add alert rule" opens create form', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesEmpty(page);

  await gotoPreferences(page);

  await page.getByRole('button', { name: 'Add alert rule' }).click();

  // Create form Save button now visible
  await expect(page.getByRole('button', { name: 'Save' })).toBeVisible({ timeout: 2000 });

  // Alert type selector present
  await expect(page.locator('select').first()).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-ATS-03 — Create form: all 4 alert types in selector
// ---------------------------------------------------------------------------

test('SC-ATS-03: create form selector contains all 4 alert types', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesEmpty(page);

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add alert rule' }).click();

  const select = page.locator('select').first();
  await expect(select).toBeVisible({ timeout: 2000 });

  // Verify all 4 options are present by text
  const options = await select.locator('option').allTextContents();
  expect(options).toContain('Stop Loss Approach');
  expect(options).toContain('Grace Period Warning');
  expect(options).toContain('Market Regime Change');
  expect(options).toContain('Daily Portfolio Summary');
});

// ---------------------------------------------------------------------------
// SC-ATS-04 — Threshold input shown only for stop_loss_approach
// ---------------------------------------------------------------------------

test('SC-ATS-04a: threshold input visible when stop_loss_approach selected', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesEmpty(page);

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add alert rule' }).click();

  // Default selection is stop_loss_approach
  const select = page.locator('select').first();
  await select.selectOption('stop_loss_approach');

  // Threshold input must be visible
  await expect(page.getByPlaceholder('5')).toBeVisible({ timeout: 2000 });
});

test('SC-ATS-04b: threshold input hidden when non-threshold type selected', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesEmpty(page);

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add alert rule' }).click();

  const select = page.locator('select').first();

  for (const type of ['grace_period_warning', 'market_regime_change', 'daily_portfolio_summary']) {
    await select.selectOption(type);
    await expect(page.getByPlaceholder('5')).toHaveCount(0);
  }
});

// ---------------------------------------------------------------------------
// SC-ATS-05 — Threshold validation: non-numeric value
//
// NOTE: Browsers coerce input[type=number] values to "" when set to a
// non-numeric string, so this validation path cannot be triggered by
// Playwright UI interaction. Verification is DoQ manual only (code review
// confirms validateThreshold('abc') returns "Please enter a valid number.").
// ---------------------------------------------------------------------------

test.skip('SC-ATS-05: threshold validation rejects non-numeric input (DoQ manual — browser coerces type=number)', () => {
  // Cannot be tested via Playwright: input[type=number] coerces non-numeric
  // values to empty string at the DOM level, preventing the NaN code path
  // from being reached via simulated keyboard/fill interaction.
  // validateThreshold() is verified correct by code review.
});

// ---------------------------------------------------------------------------
// SC-ATS-06 — Threshold validation: value ≤ 0
// ---------------------------------------------------------------------------

test('SC-ATS-06: threshold validation rejects value ≤ 0', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesEmpty(page);

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add alert rule' }).click();

  await page.getByPlaceholder('5').fill('0');

  await expect(page.getByText('Threshold must be greater than 0.')).toBeVisible({ timeout: 2000 });
  await expect(page.getByRole('button', { name: 'Save' })).toBeDisabled();
});

// ---------------------------------------------------------------------------
// SC-ATS-07 — Threshold validation: value > 50
// ---------------------------------------------------------------------------

test('SC-ATS-07: threshold validation rejects value > 50', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesEmpty(page);

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add alert rule' }).click();

  await page.getByPlaceholder('5').fill('51');

  await expect(page.getByText('Threshold cannot exceed 50%.')).toBeVisible({ timeout: 2000 });
  await expect(page.getByRole('button', { name: 'Save' })).toBeDisabled();
});

// ---------------------------------------------------------------------------
// SC-ATS-08 — Successful save fires POST /alerts/rules and refreshes list
// ---------------------------------------------------------------------------

test('SC-ATS-08: save fires POST /alerts/rules with correct body and refreshes', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);

  // Use postFired flag rather than a call counter: React StrictMode can
  // double-invoke effects in development, causing a counter to overshoot
  // and return the populated payload before the user has acted.
  let postFired = false;
  let postBody = null;

  await page.route(/\/alerts\/rules$/, (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      const payload = postFired ? TD_ALERT_RULES : EMPTY_RULES;
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) });
    } else if (method === 'POST') {
      postBody = route.request().postDataJSON();
      postFired = true;
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { id: 'rule-new', type: 'stop_loss_approach', threshold_percent: 7.0 } }) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);

  // Open create form
  await page.getByRole('button', { name: 'Add alert rule' }).click();

  // Set threshold to 7
  await page.getByPlaceholder('5').fill('7');

  // Save
  await page.getByRole('button', { name: 'Save' }).click();

  // POST was fired with correct body
  await expect.poll(() => postBody, { timeout: 3000 }).not.toBeNull();
  expect(postBody.type).toBe('stop_loss_approach');
  expect(postBody.threshold_percent).toBe(7.0);

  // After save the list reloads — populated rules now visible
  await expect(page.getByText('Stop Loss Approach').first()).toBeVisible({ timeout: 5000 });

  // Create form no longer shown (form closed after save)
  await expect(page.getByRole('button', { name: 'Save' })).toHaveCount(0, { timeout: 3000 });
});

// ---------------------------------------------------------------------------
// SC-ATS-09 — Create form: API error shows inline message
// ---------------------------------------------------------------------------

test('SC-ATS-09: POST failure shows "Failed to save alert rule" error', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);

  await page.route(/\/alerts\/rules$/, (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_RULES) });
    } else if (method === 'POST') {
      route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ message: 'Internal server error' }) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add alert rule' }).click();

  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText('Failed to save alert rule. Please try again.')).toBeVisible({ timeout: 5000 });

  // Form stays open after error
  await expect(page.getByRole('button', { name: 'Save' })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-ATS-10 — Cancel closes form; CTA button re-appears
// ---------------------------------------------------------------------------

test('SC-ATS-10: Cancel closes create form and re-shows CTA button', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesEmpty(page);

  await gotoPreferences(page);

  await page.getByRole('button', { name: 'Add alert rule' }).click();
  await expect(page.getByRole('button', { name: 'Save' })).toBeVisible({ timeout: 2000 });

  await page.getByRole('button', { name: 'Cancel' }).click();

  // Form gone
  await expect(page.getByRole('button', { name: 'Save' })).toHaveCount(0, { timeout: 2000 });

  // CTA button re-appears
  await expect(page.getByRole('button', { name: 'Add alert rule' })).toBeVisible({ timeout: 2000 });
});

// ---------------------------------------------------------------------------
// SC-ATS-11 — Populated state: no regression; CTA button absent
// ---------------------------------------------------------------------------

test('SC-ATS-11: populated state — "Add alert rule" CTA button absent', async ({ page }) => {
  await mockFeed(page);
  await mockPrefs(page);
  await mockRulesPopulated(page);

  await gotoPreferences(page);

  // Rules list loads — at least one rule visible
  await expect(page.getByText('Stop Loss Approach').first()).toBeVisible({ timeout: 5000 });

  // CTA button must NOT be present in populated state
  await expect(page.getByRole('button', { name: 'Add alert rule' })).toHaveCount(0);
});
