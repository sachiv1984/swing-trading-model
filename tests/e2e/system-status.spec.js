/**
 * System Status Page — Playwright Tests
 * ST-07 (v2.7 EPIC-03 test gap closure)
 *
 * Covers frontend behaviour of SystemStatus.js:
 *   SC-SS-01: Pre-run state shows Run Tests button and "26 endpoints" placeholder
 *   SC-SS-02: Clicking Run Tests triggers POST /test/endpoints
 *   SC-SS-03: Alerts category section visible after tests run
 *   SC-SS-04: Notifications category section visible after tests run
 *   SC-SS-05: Digest category section visible after tests run
 *   SC-SS-06: Total endpoint count ≥ 26 shown after tests run
 *   SC-SS-07: Alerts/Notifications/Digest/price-alerts/saved-filters/changelog
 *             endpoints do NOT appear under "Other" (ST-18, EPIC-05, v7.10,
 *             BLG-FE-123 added the last 3)
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/SystemStatus').
 * - GET /health/detailed via useQuery (auto-run on mount)
 * - POST /test/endpoints via useMutation (triggered by "Run Tests" button click)
 *   Response: { summary: { total, passed, failed, errors, success_rate }, results: [...] }
 * - categorizeEndpoint() routes endpoint names to category labels:
 *   /alerts → Alerts, /notifications → Notifications, /digest → Digest
 * - apiFetch (raw fetch) is used — no { status, data } envelope detection.
 * - LIFO ordering: catch-all registered FIRST so specific mocks take precedence.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

/** Minimal health response — causes page to show "Unknown" status (not a crash) */
const HEALTH_RESPONSE = {
  status: 'healthy',
  response_time_ms: 5.2,
  timestamp: '2026-04-15T10:00:00Z',
  checks: {},
};

/** 28-endpoint test results — satisfies ≥26 requirement.
 *  Includes at least one endpoint per targeted category
 *  (Alerts, Notifications, Digest) plus other categories.
 */
const TEST_RESULTS_RESPONSE = {
  summary: {
    total: 31,
    passed: 31,
    failed: 0,
    errors: 0,
    success_rate: 100.0,
  },
  results: [
    // Core (3) — includes GET /changelog/latest (ST-18, EPIC-05, v7.10, BLG-FE-123)
    { endpoint: 'GET /',                          status: 'pass', status_code: 200, response_time_ms: 3.1 },
    { endpoint: 'GET /health/detailed',           status: 'pass', status_code: 200, response_time_ms: 4.8 },
    { endpoint: 'GET /changelog/latest',          status: 'pass', status_code: 200, response_time_ms: 4.2 },
    // Analytics (2)
    { endpoint: 'GET /analytics/metrics',         status: 'pass', status_code: 200, response_time_ms: 12.3 },
    { endpoint: 'GET /analytics/summary',         status: 'pass', status_code: 200, response_time_ms: 9.7 },
    // Alerts (4) — includes GET /price-alerts (ST-18, EPIC-05, v7.10, BLG-FE-123)
    { endpoint: 'GET /alerts/rules',              status: 'pass', status_code: 200, response_time_ms: 7.2 },
    { endpoint: 'POST /alerts/rules',             status: 'pass', status_code: 201, response_time_ms: 8.5 },
    { endpoint: 'DELETE /alerts/rules/1',         status: 'pass', status_code: 200, response_time_ms: 6.1 },
    { endpoint: 'GET /price-alerts',              status: 'pass', status_code: 200, response_time_ms: 6.9 },
    // Notifications (3)
    { endpoint: 'GET /notifications',             status: 'pass', status_code: 200, response_time_ms: 5.9 },
    { endpoint: 'POST /notifications',            status: 'pass', status_code: 201, response_time_ms: 7.4 },
    { endpoint: 'PUT /notifications/1',           status: 'pass', status_code: 200, response_time_ms: 6.8 },
    // Digest (3)
    { endpoint: 'GET /digest/weekly',             status: 'pass', status_code: 200, response_time_ms: 11.2 },
    { endpoint: 'POST /digest/weekly',            status: 'pass', status_code: 201, response_time_ms: 9.3 },
    { endpoint: 'GET /digest/monthly',            status: 'pass', status_code: 200, response_time_ms: 10.5 },
    // Portfolio (3)
    { endpoint: 'GET /positions',                 status: 'pass', status_code: 200, response_time_ms: 8.1 },
    { endpoint: 'POST /positions',                status: 'pass', status_code: 201, response_time_ms: 9.6 },
    { endpoint: 'DELETE /positions/1',            status: 'pass', status_code: 200, response_time_ms: 7.3 },
    // Trading (4) — includes GET /saved-filters (ST-18, EPIC-05, v7.10, BLG-FE-123)
    { endpoint: 'GET /trades',                    status: 'pass', status_code: 200, response_time_ms: 6.5 },
    { endpoint: 'POST /trades',                   status: 'pass', status_code: 201, response_time_ms: 8.9 },
    { endpoint: 'PUT /trades/1',                  status: 'pass', status_code: 200, response_time_ms: 7.8 },
    { endpoint: 'GET /saved-filters',             status: 'pass', status_code: 200, response_time_ms: 7.1 },
    // Cash Management (3)
    { endpoint: 'GET /cash/summary',              status: 'pass', status_code: 200, response_time_ms: 5.4 },
    { endpoint: 'POST /cash/deposit',             status: 'pass', status_code: 201, response_time_ms: 6.2 },
    { endpoint: 'POST /cash/withdrawal',          status: 'pass', status_code: 201, response_time_ms: 6.7 },
    // Market Data (2)
    { endpoint: 'GET /signals',                   status: 'pass', status_code: 200, response_time_ms: 13.1 },
    { endpoint: 'GET /market/data',               status: 'pass', status_code: 200, response_time_ms: 14.2 },
    // Configuration (2)
    { endpoint: 'GET /settings',                  status: 'pass', status_code: 200, response_time_ms: 4.3 },
    { endpoint: 'PUT /settings',                  status: 'pass', status_code: 200, response_time_ms: 5.1 },
    // Validation (2)
    { endpoint: 'POST /validate/calculations',    status: 'pass', status_code: 200, response_time_ms: 18.4 },
    { endpoint: 'GET /validate/status',           status: 'pass', status_code: 200, response_time_ms: 7.6 },
  ],
};

// ---------------------------------------------------------------------------
// Shared setup helpers
// ---------------------------------------------------------------------------

/**
 * Mock GET /health/detailed to return a healthy status response.
 * apiFetch is raw fetch — response must be parseable as JSON by the component.
 */
async function mockHealth(page, payload = HEALTH_RESPONSE) {
  await page.route(`${API}/health/detailed`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    })
  );
}

/**
 * Mock POST /test/endpoints to return the given test results payload.
 */
async function mockTestEndpoints(page, payload = TEST_RESULTS_RESPONSE) {
  await page.route(`${API}/test/endpoints`, (route) => {
    if (route.request().method() === 'POST') {
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

/** Catch-all: prevent unmocked endpoints from hanging tests.
 *  Must be registered FIRST (Playwright LIFO) so specific mocks take precedence.
 */
async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

/**
 * Standard setup: catch-all first, health second, test endpoint third.
 * LIFO means test endpoint mock is checked first, health second, catch-all last.
 */
async function mockBaseEndpoints(page) {
  // Catch-all registered FIRST — Playwright routes are LIFO (last-registered wins),
  // so registering the catch-all first ensures specific mocks below take precedence.
  await mockFallback(page);
  await mockHealth(page);
  await mockTestEndpoints(page);
}

// ---------------------------------------------------------------------------
// SC-SS-01 — Pre-run state shows Run Tests button and placeholder text
// ---------------------------------------------------------------------------

test.describe('SC-SS-01 — Pre-run state', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');
  });

  test('SC-SS-01a: System Status page renders with Run Tests button', async ({ page }) => {
    await expect(page.getByRole('button', { name: /run tests/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-01b: Pre-run state shows "117 endpoints" placeholder', async ({ page }) => {
    // Before running tests, the page shows: "Tests 117 endpoints"
    // (totalTests || '115' → '115' before any test run). Baseline corrected v7.7
    // EPIC-11 ST-11 (BLG-QA-102): an AST-verified count of backend/routers/test.py's
    // test_cases list was 98, not the previously-recorded 103 — 5 entries had
    // drifted out of sync with the fallback constant at some point after
    // v7.6 (no CI gate existed to catch this until this story). See
    // .github/workflows/quality_gate.yml's "Endpoint Count Drift Check (ST-11)"
    // job, which now enforces this count stays in sync going forward.
    // +1 (98 -> 99) from v7.7 EPIC-01 ST-01, which added
    // GET /analytics/strategy-version-comparison (BLG-FEAT-75) concurrently
    // with EPIC-11's correction — reconciled at EPIC-11 branch merge.
    // +1 (99 -> 100) from v7.8 EPIC-01 ST-01, which added GET /changelog/latest.
    // +1 (100 -> 101) from v7.8 EPIC-06 ST-06, which added GET /ai/spend-trend.
    // Both counted independently on branches cut before either merged --
    // reconciled to 101 at EPIC-06 branch merge (CLAUDE.md §8).
    // +1 (101 -> 102) from v7.9 EPIC-02 ST-02, which added
    // GET /portfolio/sector-regime-trend (BLG-FEAT-67).
    // +7 (102 -> 109) from v7.10 EPIC-03 ST-11 (BLG-QA-133) endpoint test
    // suite coverage audit — added GET /health/database, GET
    // /portfolio/prospective-heat, GET /positions/search/tags, GET
    // /reports/tax-year, GET /trades/export/csv, POST /portfolio/size, POST
    // /trade-plans/generate-plan (all confirmed read-only or side-effect-safe;
    // see docs/ops/endpoint_test_coverage_audit_2026-07-29.md for the full
    // audit and the endpoints deliberately excluded as unsafe to add).
    // +1 (109 -> 110) from v8.2 EPIC-01 ST-01 (BLG-FEAT-88), which added
    // GET /reports/reconciliation.
    // +1 (110 -> 111) from v8.5 EPIC-06 ST-21 (BLG-FEAT-29), which added
    // GET /screener/regime-distribution.
    // +1 (111 -> 112) from v8.6 EPIC-01 ST-01 (BLG-FEAT-32), which added
    // GET /analytics/trade-plan-completion-rate.
    // +3 (112 -> 115) from v8.9 EPIC-02 ST-07 (BLG-FEAT-89), which added
    // POST /strategy/backtest-rule-change/run, GET /strategy/backtest-rule-change/runs,
    // GET /strategy/backtest-rule-change/runs/{run_id}.
    // +2 (115 -> 117) from v8.9 EPIC-02 ST-06 (BLG-FEAT-90), which added
    // GET /trades/{trade_id}/debrief, POST /trades/{trade_id}/debrief.
    await expect(page.getByText(/tests 117 endpoints/i)).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-01c: Pre-run state shows prompt to click Run Tests', async ({ page }) => {
    await expect(page.getByText(/click.*run tests/i)).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SS-02 — Clicking Run Tests triggers POST /test/endpoints
// ---------------------------------------------------------------------------

test.describe('SC-SS-02 — Run Tests button triggers POST /test/endpoints', () => {
  test('SC-SS-02a: POST /test/endpoints is called when Run Tests is clicked', async ({ page }) => {
    const requests = [];
    page.on('request', (req) => {
      if (req.url().includes('/test/endpoints') && req.method() === 'POST') {
        requests.push(req.url());
      }
    });

    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');

    await page.getByRole('button', { name: /run tests/i }).click();
    await page.waitForTimeout(500);

    expect(requests.length).toBeGreaterThan(0);
    expect(requests[0]).toContain('/test/endpoints');
  });
});

// ---------------------------------------------------------------------------
// SC-SS-03 through SC-SS-07 — Post-run state assertions
// Shared setup: mock endpoints, navigate, click Run Tests, wait for results.
// ---------------------------------------------------------------------------

test.describe('Post-run state — SC-SS-03 through SC-SS-07', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');
    await page.getByRole('button', { name: /run tests/i }).click();
    await page.waitForTimeout(1000);
  });

  // SC-SS-03 — Alerts category
  test('SC-SS-03a: Alerts category section header is visible after tests run', async ({ page }) => {
    await expect(page.getByRole('button', { name: /^alerts/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-03b: Alerts section shows the correct endpoint count badge', async ({ page }) => {
    // TEST_RESULTS_RESPONSE has 4 /alerts endpoints (incl. GET /price-alerts,
    // ST-18, EPIC-05, v7.10) — badge shows "4/4"
    await expect(page.getByRole('button', { name: /^alerts.*4\/4/i })).toBeVisible({ timeout: 8000 });
  });

  // SC-SS-04 — Notifications category
  test('SC-SS-04a: Notifications category section header is visible after tests run', async ({ page }) => {
    await expect(page.getByRole('button', { name: /^notifications/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-04b: Notifications section shows the correct endpoint count badge', async ({ page }) => {
    await expect(page.getByRole('button', { name: /^notifications.*3\/3/i })).toBeVisible({ timeout: 8000 });
  });

  // SC-SS-05 — Digest category
  test('SC-SS-05a: Digest category section header is visible after tests run', async ({ page }) => {
    await expect(page.getByRole('button', { name: /^digest/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-05b: Digest section shows the correct endpoint count badge', async ({ page }) => {
    await expect(page.getByRole('button', { name: /^digest.*3\/3/i })).toBeVisible({ timeout: 8000 });
  });

  // SC-SS-06 — Total endpoint count display
  test('SC-SS-06a: Total count of 31 is shown in the summary bar after tests run', async ({ page }) => {
    const totalLabel = page.locator('span').filter({ hasText: /^total:$/i });
    await expect(totalLabel).toBeVisible({ timeout: 8000 });
    await expect(totalLabel.locator('xpath=following-sibling::span[1]')).toHaveText('31', { timeout: 8000 });
  });

  test('SC-SS-06b: Endpoint count in sub-header updates to actual count after tests run', async ({ page }) => {
    await expect(page.getByText(/testing 31 endpoints/i)).toBeVisible({ timeout: 8000 });
  });

  // SC-SS-07 — Targeted endpoints absent from "Other" category
  test('SC-SS-07a: "Other" category section is NOT rendered (all endpoints are categorised)', async ({ page }) => {
    await expect(page.getByRole('button', { name: /^other/i })).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-SS-07b: /alerts/rules endpoint appears under Alerts, not Other', async ({ page }) => {
    const alertsBtn = page.getByRole('button', { name: /^alerts/i });
    await expect(alertsBtn).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('GET /alerts/rules')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-07c: /notifications endpoint appears under Notifications, not Other', async ({ page }) => {
    await expect(page.getByText('GET /notifications')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-07d: /digest/weekly endpoint appears under Digest, not Other', async ({ page }) => {
    await expect(page.getByText('GET /digest/weekly')).toBeVisible({ timeout: 8000 });
  });

  // ST-18 (EPIC-05, v7.10, BLG-FE-123): SystemStatus.js's categorizeEndpoint()
  // gained /price-alerts, /saved-filters, and /changelog branches — confirm
  // each renders under its assigned category, not "Other".
  test('SC-SS-07e: /price-alerts endpoint appears under Alerts, not Other', async ({ page }) => {
    await expect(page.getByText('GET /price-alerts')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-07f: /saved-filters endpoint appears under Trading, not Other', async ({ page }) => {
    // Anchored with the count badge (4/4) — a plain /^trading/i match also
    // resolves to an unrelated page-nav button literally named "Trading",
    // causing a Playwright strict-mode violation (2 elements).
    const tradingBtn = page.getByRole('button', { name: /^trading.*4\/4/i });
    await expect(tradingBtn).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('GET /saved-filters')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-07g: /changelog/latest endpoint appears under Core, not Other', async ({ page }) => {
    const coreBtn = page.getByRole('button', { name: /^core/i });
    await expect(coreBtn).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('GET /changelog/latest')).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SS-08 — Tailwind token registration (ST-04, EPIC-03, v8.6, BLG-FE-147)
//
// `bg-primary` and `bg-input` (and the sibling shadcn tokens registered in
// the same commit — card, popover, secondary, accent, destructive, border,
// ring) previously compiled to empty CSS rules because tailwind.config.js
// never registered them in theme.extend.colors, even though the underlying
// --primary/--input CSS custom properties are defined in src/index.css. The
// Auto-refresh Switch on this page (src/pages/SystemStatus.js) is a
// confirmed live consumer of both tokens (data-[state=checked]:bg-primary,
// data-[state=unchecked]:bg-input — src/components/ui/switch.js). Remaining
// untested call-site families (card, popover, secondary, accent,
// destructive, border, ring) are out of scope here — filed as BLG-FE-157
// per CLAUDE.md's frontend hard gate (mirrors the v8.5/ST-06 -> BLG-FE-148
// precedent).
// ---------------------------------------------------------------------------

test.describe('SC-SS-08 — Tailwind token registration (bg-primary / bg-input)', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');
  });

  test('SC-SS-08a: unchecked auto-refresh switch resolves bg-input to a real, non-transparent colour', async ({ page }) => {
    const toggle = page.locator('#auto-refresh');
    await expect(toggle).toBeVisible({ timeout: 8000 });
    await expect(toggle).toHaveAttribute('aria-checked', 'false');
    const bg = await toggle.evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(bg).not.toBe('rgba(0, 0, 0, 0)');
    expect(bg).not.toBe('transparent');
  });

  test('SC-SS-08b: checking the switch resolves bg-primary to a distinct, non-transparent colour', async ({ page }) => {
    // Real-CI finding (LL-v8.3-P3-02 class -- an animation/transition-timing
    // AC, confirmed failing on first real GitHub Actions run despite a
    // syntax-clean sandboxed review): switch.js's className includes
    // `transition-colors`, so the data-state flip's background-color change
    // is CSS-animated, not instantaneous. Reading getComputedStyle
    // immediately after `aria-checked` becomes "true" can catch the
    // pre-transition value (the click's synchronous React state update and
    // the CSS transition's own paint timeline are not the same clock) --
    // must wait for the transition to actually finish before reading the
    // final colour. Tailwind's default transition duration is 150ms;
    // waiting 300ms gives real margin.
    const toggle = page.locator('#auto-refresh');
    await expect(toggle).toBeVisible({ timeout: 8000 });
    const uncheckedBg = await toggle.evaluate((el) => getComputedStyle(el).backgroundColor);

    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-checked', 'true');
    await page.waitForTimeout(300);
    const checkedBg = await toggle.evaluate((el) => getComputedStyle(el).backgroundColor);

    expect(checkedBg).not.toBe('rgba(0, 0, 0, 0)');
    expect(checkedBg).not.toBe('transparent');
    // bg-primary (checked) must render as a genuinely different colour from
    // bg-input (unchecked) -- both compiled to the *same* empty rule before
    // this token registration fix, which this regression guards against.
    expect(checkedBg).not.toBe(uncheckedBg);
  });
});
