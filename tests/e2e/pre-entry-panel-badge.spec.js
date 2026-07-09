'use strict';
/**
 * ST-11 (BLG-FE-57, v5.9 EPIC-02)
 * Pre-entry panel: show warning/fail count when collapsed
 *
 * Covers:
 *   SC-PEP-BADGE-01: Collapsed header shows fail+warn count when advisory status is warn/fail
 *   SC-PEP-BADGE-02: No count badge shown when advisory status is pass (collapsed)
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/TradePlan?…').
 * - Pre-entry validation mock returns controlled advisory_status + checks.
 */

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Pre-entry mock payloads
// ---------------------------------------------------------------------------

const PRE_ENTRY_WARN = {
  status: 'ok',
  data: {
    ticker: 'AAPL',
    market: 'US',
    quantity: 10,
    advisory_status: 'warn',
    override_required: false,
    checks: [
      { rule: 'regime_gate', status: 'pass', detail: 'US market is Risk-On', severity: 'fail' },
      { rule: 'cash_constraint', status: 'warn', detail: 'Cash within 10% of limit', severity: 'warn' },
      { rule: 'sector_concentration', status: 'warn', detail: 'Sector at 28% (limit 30%)', severity: 'warn' },
      { rule: 'earnings_proximity', status: 'pass', detail: 'Earnings 30 days away', severity: 'warn' },
      { rule: 'sizing_validity', status: 'pass', detail: 'Position sizing valid', severity: 'warn' },
    ],
  },
};

const PRE_ENTRY_FAIL = {
  status: 'ok',
  data: {
    ticker: 'AAPL',
    market: 'US',
    quantity: 10,
    advisory_status: 'fail',
    override_required: true,
    checks: [
      { rule: 'regime_gate', status: 'fail', detail: 'US market is Risk-Off', severity: 'fail' },
      { rule: 'cash_constraint', status: 'warn', detail: 'Cash within 5% of limit', severity: 'warn' },
      { rule: 'sector_concentration', status: 'pass', detail: 'Sector within limits', severity: 'warn' },
      { rule: 'earnings_proximity', status: 'pass', detail: 'Earnings 60 days away', severity: 'warn' },
      { rule: 'sizing_validity', status: 'fail', detail: 'Quantity exceeds max position size', severity: 'fail' },
    ],
  },
};

const PRE_ENTRY_PASS = {
  status: 'ok',
  data: {
    ticker: 'AAPL',
    market: 'US',
    quantity: 10,
    advisory_status: 'pass',
    override_required: false,
    checks: [
      { rule: 'regime_gate', status: 'pass', detail: 'US market is Risk-On', severity: 'fail' },
      { rule: 'cash_constraint', status: 'pass', detail: 'Within available cash', severity: 'fail' },
      { rule: 'sector_concentration', status: 'pass', detail: 'Sector within limits', severity: 'warn' },
      { rule: 'earnings_proximity', status: 'pass', detail: 'Earnings 71 days away', severity: 'warn' },
      { rule: 'sizing_validity', status: 'pass', detail: 'Position sizing valid', severity: 'warn' },
    ],
  },
};

// ---------------------------------------------------------------------------
// Shared setup helpers
// ---------------------------------------------------------------------------

async function mockPreEntry(page, payload) {
  await page.route(new RegExp(`${API}/portfolio/pre-entry-validation`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    })
  );
}

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

async function gotoTradePlanWithChecks(page) {
  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  // PreEntryValidationPanel requires a non-zero quantity to render at all
  // (TradePlan.js: `if (!ticker || !quantity || Number(quantity) <= 0) return null`)
  // — it cannot be visible yet at this point, before quantity is filled in.
  // Wait for the page itself instead; each test fills quantity afterward.
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-PEP-BADGE-01: warn state — collapsed header shows issue count
// ---------------------------------------------------------------------------

test('SC-PEP-BADGE-01a: collapsed warn panel shows warn count badge', async ({ page }) => {
  await mockFallback(page);
  await mockPreEntry(page, PRE_ENTRY_WARN);
  await gotoTradePlanWithChecks(page);

  // Panel starts expanded — fill quantity to trigger validation query
  await page.getByPlaceholder('e.g. 50').fill('10');

  // Wait for checks to load
  await expect(page.locator('[data-testid="pre-entry-checks-panel"]')).toBeVisible({ timeout: 8000 });

  // Collapse the panel
  await page.click('[data-testid="pre-entry-panel-toggle"]');

  // Issue count badge should be visible (2 warn items)
  const badge = page.locator('[data-testid="pre-entry-issue-count"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toContainText('warn');
});

test('SC-PEP-BADGE-01b: collapsed fail panel shows fail+warn count badge', async ({ page }) => {
  await mockFallback(page);
  await mockPreEntry(page, PRE_ENTRY_FAIL);
  await gotoTradePlanWithChecks(page);

  await page.getByPlaceholder('e.g. 50').fill('10');

  await expect(page.locator('[data-testid="pre-entry-checks-panel"]')).toBeVisible({ timeout: 8000 });

  // Collapse the panel
  await page.click('[data-testid="pre-entry-panel-toggle"]');

  // Issue count badge should show both fail and warn counts
  const badge = page.locator('[data-testid="pre-entry-issue-count"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toContainText('fail');
  await expect(badge).toContainText('warn');
});

// ---------------------------------------------------------------------------
// SC-PEP-BADGE-02: pass state — no count badge when collapsed
// ---------------------------------------------------------------------------

test('SC-PEP-BADGE-02: collapsed pass panel shows no count badge', async ({ page }) => {
  await mockFallback(page);
  await mockPreEntry(page, PRE_ENTRY_PASS);
  await gotoTradePlanWithChecks(page);

  await page.getByPlaceholder('e.g. 50').fill('10');

  await expect(page.locator('[data-testid="pre-entry-checks-panel"]')).toBeVisible({ timeout: 8000 });

  // Collapse the panel
  await page.click('[data-testid="pre-entry-panel-toggle"]');

  // No count badge should be visible when all checks pass
  await expect(page.locator('[data-testid="pre-entry-issue-count"]')).not.toBeVisible();
});
