/**
 * Arc5ComplianceSection — Playwright Acceptance Tests
 * ST-11 (EPIC-03, v4.1) — BLG-QA-28 AC-01
 *
 * Covers observable ACs for the Arc5ComplianceSection component on the
 * Performance Analytics page:
 *
 *   SC-ARC5-01  Heading "Arc 5 Signal Compliance" is visible
 *   SC-ARC5-02  Four stat card titles visible: "Red Flag Events/Week",
 *               "Override Rate", "Top Rule Breach", "Trade Plan Adherence"
 *   SC-ARC5-03  Loading skeleton shown when data is pending (isLoading state)
 *   SC-ARC5-04  Error state shows "Unable to load" when API returns error
 *
 * Spec ref: docs/specs/frontend/components/arc5_compliance_section.md v1.0.0
 * API contract: docs/specs/api_contracts/arc5_compliance_analytics.md
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 *
 * ACs 02–04 (staging-only) delegated to QA Lead per DEL-20260527-01.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock payloads
// ---------------------------------------------------------------------------

const ARC5_COMPLIANCE_OK = {
  status: 'ok',
  data: {
    events_per_week: 2.3,
    override_rate: 0.143,
    top_rule_breach: 'regime_gate',
    trade_plan_adherence_rate: 0.725,
    validation_pass_rate_by_rule: {
      regime_gate: 0.82,
      cash_constraint: 0.95,
      sector_concentration: 0.91,
      earnings_proximity: 0.88,
      sizing_validity: 0.97,
    },
  },
};

const ARC5_COMPLIANCE_ERROR = {
  status: 'error',
  detail: 'Internal server error',
};

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

/** Mock all API calls not explicitly set to return empty 200s to prevent hangs. */
async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
}

/** Mock GET /analytics/arc5-compliance with the given payload and status. */
async function mockArc5Compliance(page, payload = ARC5_COMPLIANCE_OK, status = 200) {
  await page.route(new RegExp(`${API}/analytics/arc5-compliance`), (route) =>
    route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

/** Navigate to the Performance Analytics page and wait for it to mount. */
async function gotoAnalytics(page) {
  await page.goto('/#/PerformanceAnalytics');
  // Wait for the page to mount — look for any content that indicates we're on the analytics page
  await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-ARC5-01 — Heading "Arc 5 Signal Compliance" is visible
// ---------------------------------------------------------------------------

test.describe('SC-ARC5-01 — Arc 5 Signal Compliance heading', () => {
  test('SC-ARC5-01: Heading "Arc 5 Signal Compliance" is visible on the analytics page', async ({ page }) => {
    await mockFallback(page);
    await mockArc5Compliance(page, ARC5_COMPLIANCE_OK);
    await gotoAnalytics(page);

    await expect(page.getByText('Arc 5 Signal Compliance')).toBeVisible({ timeout: 10000 });
  });
});

// ---------------------------------------------------------------------------
// SC-ARC5-02 — Four stat card titles visible
// ---------------------------------------------------------------------------

test.describe('SC-ARC5-02 — Four stat card titles', () => {
  test('SC-ARC5-02: All four stat card titles are visible when data is loaded', async ({ page }) => {
    await mockFallback(page);
    await mockArc5Compliance(page, ARC5_COMPLIANCE_OK);
    await gotoAnalytics(page);

    // Wait for heading first to confirm the section is rendered
    await expect(page.getByText('Arc 5 Signal Compliance')).toBeVisible({ timeout: 10000 });

    // Then verify all four card titles
    await expect(page.getByText('Red Flag Events/Week')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Override Rate')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Top Rule Breach')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Trade Plan Adherence')).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-ARC5-03 — Loading skeleton shown when data is pending
// ---------------------------------------------------------------------------

test.describe('SC-ARC5-03 — Loading skeleton state', () => {
  test('SC-ARC5-03: Loading skeleton shown while arc5-compliance data is pending', async ({ page }) => {
    // Use a delayed route to simulate loading state
    let resolveRoute;
    const routePromise = new Promise((resolve) => { resolveRoute = resolve; });

    await page.route(new RegExp(`${API}/analytics/arc5-compliance`), async (route) => {
      // Hold the request until the test resolves it — this simulates the loading state
      await routePromise;
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ARC5_COMPLIANCE_OK) });
    });

    await mockFallback(page);
    await gotoAnalytics(page);

    // While the request is pending, the heading should be visible and skeleton pulses should be rendered
    await expect(page.getByText('Arc 5 Signal Compliance')).toBeVisible({ timeout: 10000 });

    // Skeleton elements are rendered as animated pulse divs — verify at least one is present
    // The ComplianceCard renders: <div className="h-7 w-16 bg-slate-700 rounded animate-pulse" />
    const skeletons = page.locator('.animate-pulse');
    await expect(skeletons.first()).toBeVisible({ timeout: 5000 });

    // Resolve the pending request
    resolveRoute();
  });
});

// ---------------------------------------------------------------------------
// SC-ARC5-04 — Error state shows "Unable to load"
// ---------------------------------------------------------------------------

test.describe('SC-ARC5-04 — Error state', () => {
  test('SC-ARC5-04: "Unable to load" shown in cards when API returns error', async ({ page }) => {
    await mockFallback(page);
    await mockArc5Compliance(page, ARC5_COMPLIANCE_ERROR, 500);
    await gotoAnalytics(page);

    await expect(page.getByText('Arc 5 Signal Compliance')).toBeVisible({ timeout: 10000 });

    // All four cards render "Unable to load" on error
    const errorMessages = page.getByText('Unable to load');
    await expect(errorMessages.first()).toBeVisible({ timeout: 8000 });
  });
});
