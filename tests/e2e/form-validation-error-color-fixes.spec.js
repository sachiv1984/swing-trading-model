/**
 * Form-Validation-Error Colour Token Fixes — ST-16 (BLG-FE-140, EPIC-04, v8.4)
 *
 * A bare `text-rose-400` token used for inline form-validation/inline-save-error
 * text fails WCAG contrast in light mode (the token is tuned for dark backgrounds).
 * The canonical fix, already established for WatchlistModal.js (see
 * `watchlist.spec.js` SC-WL-05, ST-21, v8.3, BLG-SPEC-108), is the light/dark pair
 * `text-rose-700 dark:text-rose-400` — same dark-mode rendering (the `dark:` value
 * is unchanged), a fixed light-mode value added.
 *
 * This story closed the remaining gaps: StrategyBenchmark.js, AlertThresholdsSection.js,
 * PreferenceRow.js, CustomPriceAlertsSection.js, ProspectiveHeatPanel.js,
 * SavedFiltersControl.js — see `docs/ops/dialog_classname_override_audit_2026-08-07.md`'s
 * sibling for the ST-16 audit trail (findings enumerated directly in the story's own
 * AC and sprint backlog).
 *
 * Coverage — each scenario triggers the field's genuine error state and asserts both
 * the canonical light-mode class and the unchanged dark-mode class are present:
 *
 *   SC-FVE-01  StrategyBenchmark.js — "To" version field error (version_order_error)
 *   SC-FVE-02  AlertThresholdsSection.js — threshold validation error (client-side)
 *   SC-FVE-03  PreferenceRow.js — toggle save-failure error
 *   SC-FVE-04  CustomPriceAlertsSection.js — ticker validation error (client-side)
 *   SC-FVE-05  ProspectiveHeatPanel.js — field validation error (client-side)
 *   SC-FVE-06  SavedFiltersControl.js — duplicate-name save error
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function expectCanonicalErrorClasses(locator) {
  await expect(locator).toBeVisible({ timeout: 5000 });
  await expect(locator).toHaveClass(/text-rose-700/);
  await expect(locator).toHaveClass(/dark:text-rose-400/);
}

// ---------------------------------------------------------------------------
// SC-FVE-01 — StrategyBenchmark.js
// ---------------------------------------------------------------------------

test('SC-FVE-01: StrategyBenchmark "To" version field error uses canonical colour tokens', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/analytics/strategy-version-comparison`), (route) =>
    route.fulfill({
      status: 400,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'error', code: 'version_order_error', message: "Must be chronologically after the 'From' version." }),
    })
  );
  await page.goto('/#/StrategyBenchmark');
  await page.getByTestId('benchmark-tab-version-comparison').click();

  const compareButton = page.getByTestId('version-compare-btn');
  await expect(compareButton).toBeVisible({ timeout: 10000 });
  await compareButton.click();

  await expectCanonicalErrorClasses(page.getByTestId('version-to-error'));
});

// ---------------------------------------------------------------------------
// SC-FVE-02 — AlertThresholdsSection.js (threshold validation, client-side)
// ---------------------------------------------------------------------------

test('SC-FVE-02: AlertThresholdsSection threshold validation error uses canonical colour tokens', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/alerts/rules`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/notifications/preferences`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { preferences: [] } }) })
  );
  await page.goto('/#/NotificationPreferences');

  await page.getByRole('button', { name: /add alert rule/i }).click();
  // Alert Type defaults to "Stop Loss Approach" — the only THRESHOLD_TYPES entry —
  // so the Threshold input is present without further selection.
  const thresholdInput = page.getByPlaceholder('5');
  await expect(thresholdInput).toBeVisible({ timeout: 5000 });
  await thresholdInput.fill('75');

  await expectCanonicalErrorClasses(page.getByText('Threshold cannot exceed 50%.'));
});

// ---------------------------------------------------------------------------
// SC-FVE-03 — PreferenceRow.js (toggle save-failure)
// ---------------------------------------------------------------------------

test('SC-FVE-03: PreferenceRow toggle save-failure error uses canonical colour tokens', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/notifications/preferences`, (route) => {
    if (route.request().method() === 'PATCH') {
      return route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error' }) });
    }
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { preferences: [{ alert_type: 'stop_loss_approach', email_enabled: false }] } }),
    });
  });
  await page.route(`${API}/alerts/rules`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.goto('/#/NotificationPreferences');

  const toggle = page.locator('button[role="switch"]').first();
  await expect(toggle).toBeVisible({ timeout: 10000 });
  await toggle.click();

  await expectCanonicalErrorClasses(page.getByText('Failed to save preference. Please try again.'));
});

// ---------------------------------------------------------------------------
// SC-FVE-04 — CustomPriceAlertsSection.js (ticker validation, client-side)
// ---------------------------------------------------------------------------

test('SC-FVE-04: CustomPriceAlertsSection ticker validation error uses canonical colour tokens', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/notifications/preferences`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { preferences: [] } }) })
  );
  await page.route(`${API}/price-alerts`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.goto('/#/NotificationPreferences');

  await page.getByRole('button', { name: /add price alert/i }).click();
  const tickerInput = page.getByPlaceholder('e.g. AAPL');
  await expect(tickerInput).toBeVisible({ timeout: 5000 });
  await tickerInput.fill('!!!bad!!!');

  await expectCanonicalErrorClasses(page.getByText('Invalid format. Use 1–10 alphanumeric characters.'));
});

// ---------------------------------------------------------------------------
// SC-FVE-05 — ProspectiveHeatPanel.js (field validation, client-side)
// ---------------------------------------------------------------------------

test('SC-FVE-05: ProspectiveHeatPanel field validation error uses canonical colour tokens', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/portfolio`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.goto('/#/RiskDashboard');

  await page.locator('button', { hasText: 'Prospective Heat Calculator' }).click();
  await page.getByRole('button', { name: 'Calculate' }).click();

  await expectCanonicalErrorClasses(page.getByText('Required', { exact: true }));
});

// ---------------------------------------------------------------------------
// SC-FVE-06 — SavedFiltersControl.js (duplicate-name save error)
// ---------------------------------------------------------------------------

const MOCK_TRADE = {
  id: 'fve-t1', ticker: 'NVDA', market: 'US',
  entry_date: '2026-05-01', exit_date: '2026-05-15',
  entry_price: 500.0, exit_price: 545.0, fill_price: 500.0,
  shares: 10, pnl: 562.5, pnl_pct: 9.0, slippage_pct: 0,
  exit_reason: 'Target Reached', tags: [],
};

test('SC-FVE-06: SavedFiltersControl duplicate-name save error uses canonical colour tokens', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ trades: [MOCK_TRADE] }) })
  );
  await page.route(`${API}/saved-filters`, (route) => {
    if (route.request().method() === 'POST') {
      return route.fulfill({ status: 400, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'duplicate' }) });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
  });
  await page.goto('/#/TradeHistory');
  await expect(page.getByText('NVDA').first()).toBeVisible({ timeout: 10000 });

  // Activate a filter so "Save current filters as…" appears (SC-SFC-02 convention,
  // saved-filters-calendar-view.spec.js) — Market combobox is the first on the page.
  await page.locator('button[role="combobox"]').first().click();
  await page.getByRole('option', { name: 'UK' }).click();
  await page.getByText('Save current filters as…').click();
  await page.getByPlaceholder(/preset name/i).fill('My Preset');
  await page.getByRole('button', { name: /^save$/i }).click();

  await expectCanonicalErrorClasses(page.getByText("A preset named 'My Preset' already exists."));
});
