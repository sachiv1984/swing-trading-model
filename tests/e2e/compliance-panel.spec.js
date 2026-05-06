/**
 * Strategy Compliance Panel — Acceptance Tests
 * ST-01 (BLG-FEAT-11, v2.3)
 * Covers: SC-COMP-01 through SC-COMP-07
 *
 * Spec refs:
 *   docs/specs/frontend/pages/positions.md §Strategy Compliance Panel
 *   docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md
 *
 * What these tests cover (non-visual AC only):
 *   SC-COMP-01  Panel absent in Grid View (default view — no compliance endpoint called)
 *   SC-COMP-02  Table View, all compliant → "Compliant" badge present, body collapsed
 *   SC-COMP-03  Table View, 1 non-compliant → "Needs Attention" badge, expanded, ⚠ visible
 *   SC-COMP-04  Table View, all non-compliant → "Review Required" badge present
 *   SC-COMP-05  Table View, grace position → "Not set" stop age, "—" for null flags
 *   SC-COMP-06  No open positions → panel hidden entirely
 *   SC-COMP-07  Manual toggle — click header to collapse; click again to expand
 *
 * What requires DoQ manual visual verification (not covered here):
 *   - Green/amber/red badge background colour rendering
 *   - ✅ / ⚠ icon colours (green checkmark vs amber triangle)
 *   - Smooth CSS max-height transition animation on expand/collapse
 *   - Ticker text white/bold; market pill appearance (slate bg, border)
 *   - Panel gradient background (slate-900 → slate-800) and border
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 *
 * VIEW SWITCHER NOTE: The three view-mode icon buttons share class 'p-0 rounded-lg'
 * with no text labels. .nth(0)=Grid, .nth(1)=Table/List, .nth(2)=Journal.
 *
 * SELECTOR NOTE: "Stop Compliance", "Stop Age", "Size Compliance" are the compliance
 * table column headers — they are unique to the compliance panel and serve as the
 * canonical "panel is expanded" indicator. "AAPL" also appears in the positions table
 * so ticker-based selectors always use .first() or are scoped to the compliance panel.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');
const {
  TWO_OPEN_POSITIONS,
  COMPLIANCE_ALL_COMPLIANT,
  COMPLIANCE_NEEDS_ATTENTION,
  COMPLIANCE_REVIEW_REQUIRED,
  COMPLIANCE_WITH_GRACE,
  COMPLIANCE_NO_POSITIONS,
  ANALYTICS_STUB,
} = require('./mocks/compliance-mock-data');

// ---------------------------------------------------------------------------
// Shared mock helpers
// ---------------------------------------------------------------------------

/** Mock GET /positions — returns array directly (raw, no envelope). */
async function mockPositions(page, payload) {
  await page.route(/\/positions(\?|$)/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(payload),
      });
    } else {
      route.continue();
    }
  });
}

/**
 * Mock GET /positions/compliance — enveloped response { status, data }.
 * Route regex: /positions/compliance only (NOT matched by /positions(\?|$)).
 */
async function mockCompliance(page, payload) {
  await page.route(/\/positions\/compliance(\?|$)/, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    });
  });
}

/** Mock GET /analytics/metrics — prevents staleness indicator console errors. */
async function mockAnalyticsMetrics(page) {
  await page.route(/\/analytics\/metrics(\?|$)/, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(ANALYTICS_STUB),
    });
  });
}

/**
 * Switch from Grid View (default) to Table View.
 * View switcher buttons: .nth(0)=Grid, .nth(1)=Table, .nth(2)=Journal.
 */
async function switchToTableView(page) {
  const tableBtn = page.locator('button.p-0.rounded-lg').nth(1);
  await tableBtn.click();
}

/**
 * Full page setup: positions mock + compliance mock + analytics stub.
 * Navigate to /#/Positions and wait for page load.
 */
async function setupPositionsPage(page, positionsPayload, compliancePayload) {
  await mockPositions(page, positionsPayload);
  await mockCompliance(page, compliancePayload);
  await mockAnalyticsMetrics(page);

  await page.goto('/#/Positions');
}

// ---------------------------------------------------------------------------
// SC-COMP-01 — Panel absent in Grid View (default)
// ---------------------------------------------------------------------------

test('SC-COMP-01: compliance panel is absent in Grid View (default view mode)', async ({ page }) => {
  // Grid View is the default — no view switch needed.
  // Positions.js gates the panel on viewMode === "table", so it must not appear here.
  await setupPositionsPage(page, TWO_OPEN_POSITIONS, COMPLIANCE_ALL_COMPLIANT);

  // "Strategy Compliance" heading must not exist in Grid View
  await expect(page.getByText('Strategy Compliance')).not.toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-COMP-02 — All compliant: "Compliant" badge, panel collapsed by default
// ---------------------------------------------------------------------------

test('SC-COMP-02: Table View — all compliant shows "Compliant" badge and panel is collapsed', async ({ page }) => {
  await setupPositionsPage(page, TWO_OPEN_POSITIONS, COMPLIANCE_ALL_COMPLIANT);
  await switchToTableView(page);

  // Panel header label must be visible
  await expect(page.getByText('Strategy Compliance')).toBeVisible({ timeout: 5000 });

  // "Compliant" badge must be visible — use .first() because the parent button element
  // also matches (its accessible text tree contains "Compliant" from the badge).
  await expect(page.getByText('Compliant').first()).toBeVisible({ timeout: 5000 });

  // Summary text present
  await expect(page.getByText(/2 of 2 positions fully compliant/i)).toBeVisible({ timeout: 5000 });

  // Panel is collapsed by default — aria-expanded="false" on the toggle button.
  // (CSS max-height:0/overflow:hidden doesn't satisfy Playwright's toBeVisible check,
  // so we verify collapse state via the aria-expanded attribute instead.)
  const toggleBtn = page.locator('button[aria-expanded]').first();
  await expect(toggleBtn).toHaveAttribute('aria-expanded', 'false');
});

// ---------------------------------------------------------------------------
// SC-COMP-03 — One non-compliant: "Needs Attention" badge, expanded, ⚠ shown
// ---------------------------------------------------------------------------

test('SC-COMP-03: Table View — one non-compliant shows "Needs Attention" badge and expands with ⚠', async ({ page }) => {
  await setupPositionsPage(page, TWO_OPEN_POSITIONS, COMPLIANCE_NEEDS_ATTENTION);
  await switchToTableView(page);

  // "Needs Attention" badge — unique string, no strict-mode issue
  await expect(page.getByText('Needs Attention')).toBeVisible({ timeout: 5000 });

  // Summary text
  await expect(page.getByText(/1 of 2 positions fully compliant/i)).toBeVisible({ timeout: 5000 });

  // Panel expanded by default — compliance table column headers visible
  await expect(page.getByText('Stop Compliance')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Stop Age')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Size Compliance')).toBeVisible({ timeout: 5000 });

  // Warning icon present for non-compliant stop (pos-1: stop_compliant: false)
  // ⚠️ emoji is rendered by ComplianceFlag when value === false
  await expect(page.getByText('⚠️').first()).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-COMP-04 — All non-compliant: "Review Required" badge, expanded
// ---------------------------------------------------------------------------

test('SC-COMP-04: Table View — all non-compliant shows "Review Required" badge', async ({ page }) => {
  await setupPositionsPage(page, TWO_OPEN_POSITIONS, COMPLIANCE_REVIEW_REQUIRED);
  await switchToTableView(page);

  // "Review Required" badge — unique string
  await expect(page.getByText('Review Required')).toBeVisible({ timeout: 5000 });

  // Summary: 0 of 2
  await expect(page.getByText(/0 of 2 positions fully compliant/i)).toBeVisible({ timeout: 5000 });

  // Panel expanded — compliance table headers visible
  await expect(page.getByText('Stop Compliance')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Stop Age')).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-COMP-05 — Grace position: "Not set" stop age, "—" for null flags
// ---------------------------------------------------------------------------

test('SC-COMP-05: Table View — grace period position shows "Not set" and "—" for null flags', async ({ page }) => {
  await setupPositionsPage(page, TWO_OPEN_POSITIONS, COMPLIANCE_WITH_GRACE);
  await switchToTableView(page);

  // Panel header visible
  await expect(page.getByText('Strategy Compliance')).toBeVisible({ timeout: 5000 });

  // Overall status is Compliant (2 of 2 — grace counts as compliant in this fixture)
  await expect(page.getByText('Compliant').first()).toBeVisible({ timeout: 5000 });

  // Expand the panel (collapsed because all-compliant default)
  await page.getByText('Strategy Compliance').click();
  await page.waitForTimeout(400); // allow CSS max-height transition

  // Grace position: stop_age_days null → "Not set"
  await expect(page.getByText('Not set')).toBeVisible({ timeout: 5000 });

  // Grace position: null flags → "—" dash displayed for each null field
  // At least one "—" must be present in the compliance table
  await expect(page.getByText('—').first()).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-COMP-06 — No open positions: panel hidden entirely
// ---------------------------------------------------------------------------

test('SC-COMP-06: Table View — panel hidden when no open positions', async ({ page }) => {
  // Empty positions list — Positions.js gates on openPositions.length > 0
  await setupPositionsPage(page, [], COMPLIANCE_NO_POSITIONS);
  await switchToTableView(page);

  // Panel must not render at all
  await expect(page.getByText('Strategy Compliance')).not.toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-COMP-07 — Manual toggle: click to collapse; click again to expand
// ---------------------------------------------------------------------------

test('SC-COMP-07: panel can be manually collapsed and re-expanded by clicking the header', async ({ page }) => {
  // Use "Needs Attention" so panel starts expanded (non-compliant present)
  await setupPositionsPage(page, TWO_OPEN_POSITIONS, COMPLIANCE_NEEDS_ATTENTION);
  await switchToTableView(page);

  // Panel starts expanded — compliance column headers visible
  await expect(page.getByText('Stop Compliance')).toBeVisible({ timeout: 5000 });

  // Click header to collapse
  await page.getByText('Strategy Compliance').click();
  await page.waitForTimeout(400); // allow CSS transition

  // Panel now collapsed — aria-expanded="false"
  const toggleBtn = page.locator('button[aria-expanded]').first();
  await expect(toggleBtn).toHaveAttribute('aria-expanded', 'false');

  // Click header again to expand
  await page.getByText('Strategy Compliance').click();
  await page.waitForTimeout(400);

  // Panel now expanded — aria-expanded="true"
  await expect(toggleBtn).toHaveAttribute('aria-expanded', 'true');
});
