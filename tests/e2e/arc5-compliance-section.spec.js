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

/**
 * PerformanceAnalytics gates all sections behind a minimum-trades check
 * (settingsData.min_trades_for_analytics, default 10). Without at least 10
 * closed trades in the selected period, the page shows "Not enough trades"
 * and none of the analytics sections (including Arc5ComplianceSection)
 * render at all.
 */
function buildMockTrades(count = 12) {
  const now = new Date();
  return Array.from({ length: count }, (_, i) => ({
    id: `trade-${i}`,
    ticker: 'AAPL',
    market: 'US',
    entry_date: new Date(now.getTime() - (i + 5) * 86400000).toISOString(),
    exit_date: new Date(now.getTime() - i * 86400000).toISOString(),
    entry_price: 100,
    exit_price: 105,
    pnl: 50,
    shares: 10,
  }));
}

/** Mock all API calls not explicitly set to return empty 200s to prevent hangs. */
async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route(new RegExp(`${API}/trades$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: buildMockTrades() }) })
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

    // mockFallback must be registered FIRST: Playwright evaluates page.route()
    // handlers in reverse registration order (most-recently-registered first).
    // Registering the delayed arc5-compliance route last ensures it — not
    // mockFallback's generic catch-all — wins the match and actually holds
    // the request open (shared_standards.md §18 route-ordering advisory).
    await mockFallback(page);

    await page.route(new RegExp(`${API}/analytics/arc5-compliance`), async (route) => {
      // Hold the request until the test resolves it — this simulates the loading state
      await routePromise;
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ARC5_COMPLIANCE_OK) });
    });

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

// ---------------------------------------------------------------------------
// SC-ARC5-05 — Compliance score metric values formatted correctly (BLG-QA-58 — v5.7 ST-08)
// ---------------------------------------------------------------------------

const ARC5_KNOWN_VALUES = {
  status: 'ok',
  data: {
    events_per_week: 3.0,
    override_rate: 0.200,
    top_rule_breach: 'cash_constraint',
    trade_plan_adherence_rate: 0.850,
    validation_pass_rate_by_rule: {
      regime_gate: 0.90,
      cash_constraint: 0.75,
      sector_concentration: 0.95,
      earnings_proximity: 0.88,
      sizing_validity: 0.99,
    },
  },
};

test.describe('SC-ARC5-05 — Compliance score metric values formatted as percentages', () => {
  test('SC-ARC5-05: Trade Plan Adherence displays as formatted percentage (85.0%)', async ({ page }) => {
    await mockFallback(page);
    await mockArc5Compliance(page, ARC5_KNOWN_VALUES);
    await gotoAnalytics(page);

    // Section heading confirms the component is rendered
    await expect(page.getByText('Arc 5 Signal Compliance')).toBeVisible({ timeout: 10000 });

    // trade_plan_adherence_rate: 0.850 → fmtRate → "85.0%"
    await expect(page.getByText('85.0%')).toBeVisible({ timeout: 8000 });

    // override_rate: 0.200 → fmtRate → "20.0%"
    await expect(page.getByText('20.0%')).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-ARC5-06 — events_per_week value formatted via fmtCount (ST-12, BLG-QA-154)
// ---------------------------------------------------------------------------

test.describe('SC-ARC5-06 — Red Flag Events/Week value formatted via fmtCount', () => {
  test('SC-ARC5-06: events_per_week renders as fmtCount output (3.0) for a known mock value', async ({ page }) => {
    await mockFallback(page);
    await mockArc5Compliance(page, ARC5_KNOWN_VALUES);
    await gotoAnalytics(page);

    await expect(page.getByText('Arc 5 Signal Compliance')).toBeVisible({ timeout: 10000 });

    // events_per_week: 3.0 → fmtCount → val.toFixed(1) → "3.0"
    await expect(page.getByText('3.0', { exact: true })).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-ARC5-07 — top_rule_breach text formatted via fmtText (ST-13, BLG-QA-155)
// ---------------------------------------------------------------------------

test.describe('SC-ARC5-07 — Top Rule Breach text formatted via fmtText', () => {
  test('SC-ARC5-07: top_rule_breach renders with underscores replaced with spaces', async ({ page }) => {
    await mockFallback(page);
    await mockArc5Compliance(page, ARC5_KNOWN_VALUES);
    await gotoAnalytics(page);

    await expect(page.getByText('Arc 5 Signal Compliance')).toBeVisible({ timeout: 10000 });

    // top_rule_breach: 'cash_constraint' → fmtText → val.replace(/_/g, ' ') → "cash constraint"
    await expect(page.getByText('cash constraint', { exact: true })).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-ARC5-08 — Null-value handling across fmtRate/fmtCount/fmtText (ST-14, BLG-QA-156)
// ---------------------------------------------------------------------------

const ARC5_ALL_NULL = {
  status: 'ok',
  data: {
    events_per_week: null,
    override_rate: null,
    top_rule_breach: null,
    trade_plan_adherence_rate: null,
    validation_pass_rate_by_rule: {},
  },
};

test.describe('SC-ARC5-08 — Null values render as em dash across all formatters', () => {
  test('SC-ARC5-08: "—" renders for null events_per_week (fmtCount), override_rate/trade_plan_adherence_rate (fmtRate), and top_rule_breach (fmtText)', async ({ page }) => {
    await mockFallback(page);
    await mockArc5Compliance(page, ARC5_ALL_NULL);
    await gotoAnalytics(page);

    const heading = page.getByText('Arc 5 Signal Compliance');
    await expect(heading).toBeVisible({ timeout: 10000 });

    // Scope to the Arc5ComplianceSection container (heading's parent) so the count
    // isn't inflated by unrelated "—" placeholders elsewhere on the analytics page.
    const section = heading.locator('..');

    // All four cards render fmtCount(null) / fmtRate(null) / fmtText(null) → "—"
    const dashValues = section.getByText('—', { exact: true });
    await expect(dashValues).toHaveCount(4, { timeout: 8000 });
  });
});
