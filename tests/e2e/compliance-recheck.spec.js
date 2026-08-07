/**
 * On-Demand Compliance Recheck — Acceptance Tests
 * ST-01 (BLG-FEAT-64, v6.9)
 *
 * Covers AC-02 (Playwright-coverable per stage4_backlog_slice.md: "rendering +
 * pass/fail/override states are all deterministic given API response fixtures").
 * AC-01, AC-03 are backend-only (endpoint behaviour, no-polling) and are covered by
 * tests/test_compliance_recheck.py. AC-04 (§13 sign-off) is a governance gate, not
 * a testable UI behaviour.
 *
 *   SC-CR-01  "Recheck Compliance" action visible in Table View Actions column
 *   SC-CR-02  Clicking the action opens the modal and shows a loading state
 *   SC-CR-03  Pass result — "Pass" badge (emerald), all 5 rule rows shown, no override checkbox
 *   SC-CR-04  Warn result — "Warn" badge (amber), override checkbox visible
 *   SC-CR-05  Fail result — "Fail" badge (red), override checkbox visible and toggleable
 *   SC-CR-06  API failure — "Recheck unavailable — try again" + retry button shown
 *   SC-CR-07  Close (✕) button dismisses the modal
 *   SC-CR-08  Grid View — "Recheck" action also present on the position card footer
 *   SC-CR-09  Pass result shows the all-pass affirmation line (ST-02, EPIC-01, v8.2, BLG-FE-105)
 *   SC-CR-10  Warn/Fail results do not show the all-pass affirmation line
 *   SC-CR-11  Escape closes the modal; focus returns to the trigger button (ST-11, EPIC-03, v8.3, BLG-FE-103 —
 *             Dialog primitive migration, matching the TradePlan.js Abandon modal precedent)
 *
 * Spec refs:
 *   docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md
 *   docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/compliance-recheck
 *
 * ROUTING NOTE: App uses HashRouter — all navigation via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

function makePosition(overrides = {}) {
  return {
    id: 'pos-recheck-01',
    ticker: 'AAPL',
    market: 'US',
    entry_price: 150.00,
    current_price: 155.00,
    current_price_native: 160.00,
    stop_price: 140.00,
    stop_price_native: 145.00,
    shares: 10,
    pnl: 50.00,
    pnl_percent: 3.3,
    holding_days: 15,
    grace_days_remaining: null,
    status: 'open',
    entry_date: '2026-06-01',
    initial_stop: 130.00,
    current_trailing_stop: 0,
    risk_off_exit: false,
    tags: null,
    ...overrides,
  };
}

const PASS_RESULT = {
  overall_status: 'pass',
  checks: [
    { rule_key: 'regime_gate', status: 'pass', detail: 'US market is Risk-On (SPY above 200-day MA)' },
    { rule_key: 'cash_constraint', status: 'pass', detail: 'Estimated cost £1,000.00 within available cash £5,000.00' },
    { rule_key: 'sector_concentration', status: 'pass', detail: 'Current Technology sector allocation 4.0% within 30.0% advisory limit' },
    { rule_key: 'earnings_proximity', status: 'pass', detail: 'Next earnings 2026-08-01 (22 days) — outside 5-day proximity window' },
    { rule_key: 'sizing_validity', status: 'pass', detail: 'Stop distance 10.0 is valid (entry 150.0, stop 140.0)' },
  ],
};

const WARN_RESULT = {
  overall_status: 'warn',
  checks: [
    { rule_key: 'regime_gate', status: 'pass', detail: 'US market is Risk-On (SPY above 200-day MA)' },
    { rule_key: 'cash_constraint', status: 'pass', detail: 'Estimated cost £1,000.00 within available cash £5,000.00' },
    { rule_key: 'sector_concentration', status: 'warn', detail: 'Current Energy sector allocation 34.2% exceeds 30.0% advisory limit' },
    { rule_key: 'earnings_proximity', status: 'pass', detail: 'Next earnings 2026-08-01 (22 days) — outside 5-day proximity window' },
    { rule_key: 'sizing_validity', status: 'pass', detail: 'Stop distance 10.0 is valid (entry 150.0, stop 140.0)' },
  ],
};

const FAIL_RESULT = {
  overall_status: 'fail',
  checks: [
    { rule_key: 'regime_gate', status: 'fail', detail: 'US market is Risk-Off (SPY below 200-day MA)' },
    { rule_key: 'cash_constraint', status: 'fail', detail: 'Estimated cost £2,150.00 exceeds available cash £500.00' },
    { rule_key: 'sector_concentration', status: 'pass', detail: 'Current Technology sector allocation 4.0% within 30.0% advisory limit' },
    { rule_key: 'earnings_proximity', status: 'pass', detail: 'Next earnings 2026-08-01 (22 days) — outside 5-day proximity window' },
    { rule_key: 'sizing_validity', status: 'pass', detail: 'Stop distance 10.0 is valid (entry 150.0, stop 140.0)' },
  ],
};

async function stubPositionsPage(page, positions) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance-recheck') || url.includes('/positions/compliance') || url.includes('/gap-risk')) {
      return route.continue();
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) });
  });
  await page.route('**/portfolio*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/positions/compliance*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null, days_until_earnings: null }) })
  );
  await page.route('**/positions/*/gap-risk', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false } }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
}

async function mockRecheck(page, positionId, result, { fail = false } = {}) {
  await page.route(`**/positions/${positionId}/compliance-recheck`, (route) => {
    if (fail) {
      return route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'boom' }) });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: result }) });
  });
}

async function gotoPositionsTable(page, positions) {
  await stubPositionsPage(page, positions);
  await page.goto('/#/Positions');
  const firstTicker = positions[0]?.ticker || 'AAPL';
  await page.waitForSelector(`text=${firstTicker}`, { timeout: 8000 });
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 8000 });
  await tableBtn.click();
  await page.waitForSelector('table', { timeout: 5000 });
}

test('SC-CR-01: "Recheck Compliance" action visible in Table View Actions column', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, PASS_RESULT);
  await gotoPositionsTable(page, [pos]);

  await expect(page.locator('[data-testid="recheck-compliance-button"]').first()).toBeVisible({ timeout: 5000 });
});

test('SC-CR-02: Clicking the action opens the modal and shows a loading state', async ({ page }) => {
  const pos = makePosition();
  await page.route(`**/positions/${pos.id}/compliance-recheck`, async (route) => {
    await new Promise((r) => setTimeout(r, 300));
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: PASS_RESULT }) });
  });
  await gotoPositionsTable(page, [pos]);

  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  await expect(page.locator('[data-testid="compliance-recheck-modal"]')).toBeVisible({ timeout: 5000 });
  await expect(page.locator('[data-testid="compliance-recheck-loading"]')).toBeVisible({ timeout: 2000 });
});

test('SC-CR-03: Pass result shows "Pass" badge, all 5 rule rows, no override checkbox', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, PASS_RESULT);
  await gotoPositionsTable(page, [pos]);

  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  const badge = page.locator('[data-testid="compliance-recheck-overall-badge"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveText('Pass');
  await expect(badge).toHaveClass(/bg-emerald-500\/20/);

  for (const key of ['regime_gate', 'cash_constraint', 'sector_concentration', 'earnings_proximity', 'sizing_validity']) {
    await expect(page.locator(`[data-testid="compliance-check-${key}"]`)).toBeVisible();
  }
  await expect(page.locator('[data-testid="compliance-recheck-override-checkbox"]')).not.toBeVisible();
});

test('SC-CR-09: Pass result shows the all-pass affirmation line (ST-02, EPIC-01, v8.2, BLG-FE-105)', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, PASS_RESULT);
  await gotoPositionsTable(page, [pos]);

  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  const note = page.locator('[data-testid="compliance-recheck-all-pass-note"]');
  await expect(note).toBeVisible({ timeout: 5000 });
  await expect(note).toHaveText('All 5 checks passed — no action needed.');
  await expect(note).toHaveClass(/text-emerald-400/);
});

test('SC-CR-10: Warn/Fail results do not show the all-pass affirmation line', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, WARN_RESULT);
  await gotoPositionsTable(page, [pos]);

  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  await expect(page.locator('[data-testid="compliance-recheck-override-checkbox"]')).toBeVisible({ timeout: 5000 });
  await expect(page.locator('[data-testid="compliance-recheck-all-pass-note"]')).not.toBeVisible();
});

test('SC-CR-04: Warn result shows "Warn" badge and override checkbox', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, WARN_RESULT);
  await gotoPositionsTable(page, [pos]);

  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  const badge = page.locator('[data-testid="compliance-recheck-overall-badge"]');
  await expect(badge).toHaveText('Warn', { timeout: 5000 });
  await expect(badge).toHaveClass(/bg-amber-500\/20/);
  await expect(page.locator('[data-testid="compliance-recheck-override-checkbox"]')).toBeVisible();
});

test('SC-CR-05: Fail result shows "Fail" badge; override checkbox is toggleable', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, FAIL_RESULT);
  await gotoPositionsTable(page, [pos]);

  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  const badge = page.locator('[data-testid="compliance-recheck-overall-badge"]');
  await expect(badge).toHaveText('Fail', { timeout: 5000 });
  await expect(badge).toHaveClass(/bg-red-500\/20/);

  const checkbox = page.locator('[data-testid="compliance-recheck-override-checkbox"]');
  await expect(checkbox).toBeVisible();
  await expect(checkbox).not.toBeChecked();
  await checkbox.check();
  await expect(checkbox).toBeChecked();
});

test('SC-CR-06: API failure shows "Recheck unavailable" with a retry button', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, null, { fail: true });
  await gotoPositionsTable(page, [pos]);

  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  await expect(page.locator('[data-testid="compliance-recheck-error"]')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText(/recheck unavailable/i)).toBeVisible();
  await expect(page.getByRole('button', { name: /retry/i })).toBeVisible();
});

test('SC-CR-07: Close (✕) button dismisses the modal', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, PASS_RESULT);
  await gotoPositionsTable(page, [pos]);

  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  await expect(page.locator('[data-testid="compliance-recheck-modal"]')).toBeVisible({ timeout: 5000 });

  // ST-11 (BLG-FE-103, EPIC-03, v8.3): migrated onto the shared Dialog primitive —
  // the close control is now Radix's built-in DialogClose (sr-only accessible name "Close"),
  // not the modal's own bespoke aria-label="Close compliance recheck" button.
  await page.locator('[data-testid="compliance-recheck-modal"]').getByRole('button', { name: 'Close' }).click();
  await expect(page.locator('[data-testid="compliance-recheck-modal"]')).not.toBeVisible({ timeout: 3000 });
});

test('SC-CR-11: Escape closes the modal; focus returns to the trigger button', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, PASS_RESULT);
  await gotoPositionsTable(page, [pos]);

  const triggerBtn = page.locator('[data-testid="recheck-compliance-button"]').first();
  await triggerBtn.click();
  await expect(page.locator('[data-testid="compliance-recheck-modal"]')).toBeVisible({ timeout: 5000 });

  await page.keyboard.press('Escape');
  await expect(page.locator('[data-testid="compliance-recheck-modal"]')).not.toBeVisible({ timeout: 3000 });
  await expect(triggerBtn).toBeFocused();
});

test('SC-CR-08: Grid View — "Recheck" action present on the position card footer', async ({ page }) => {
  const pos = makePosition();
  await mockRecheck(page, pos.id, PASS_RESULT);
  await stubPositionsPage(page, [pos]);
  await page.goto('/#/Positions');
  await page.waitForSelector(`text=${pos.ticker}`, { timeout: 8000 });

  await expect(page.locator('[data-testid="recheck-compliance-button"]').first()).toBeVisible({ timeout: 5000 });
  await page.locator('[data-testid="recheck-compliance-button"]').first().click();
  await expect(page.locator('[data-testid="compliance-recheck-modal"]')).toBeVisible({ timeout: 5000 });
});
