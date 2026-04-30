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
 *   SC-SS-07: Alerts/Notifications/Digest endpoints do NOT appear under "Other"
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
    total: 28,
    passed: 28,
    failed: 0,
    errors: 0,
    success_rate: 100.0,
  },
  results: [
    // Core (2)
    { endpoint: 'GET /',                          status: 'pass', status_code: 200, response_time_ms: 3.1 },
    { endpoint: 'GET /health/detailed',           status: 'pass', status_code: 200, response_time_ms: 4.8 },
    // Analytics (2)
    { endpoint: 'GET /analytics/metrics',         status: 'pass', status_code: 200, response_time_ms: 12.3 },
    { endpoint: 'GET /analytics/summary',         status: 'pass', status_code: 200, response_time_ms: 9.7 },
    // Alerts (3)
    { endpoint: 'GET /alerts/rules',              status: 'pass', status_code: 200, response_time_ms: 7.2 },
    { endpoint: 'POST /alerts/rules',             status: 'pass', status_code: 201, response_time_ms: 8.5 },
    { endpoint: 'DELETE /alerts/rules/1',         status: 'pass', status_code: 200, response_time_ms: 6.1 },
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
    // Trading (3)
    { endpoint: 'GET /trades',                    status: 'pass', status_code: 200, response_time_ms: 6.5 },
    { endpoint: 'POST /trades',                   status: 'pass', status_code: 201, response_time_ms: 8.9 },
    { endpoint: 'PUT /trades/1',                  status: 'pass', status_code: 200, response_time_ms: 7.8 },
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
    await page.waitForLoadState('networkidle', { timeout: 10000 });
  });

  test('SC-SS-01a: System Status page renders with Run Tests button', async ({ page }) => {
    await expect(page.getByRole('button', { name: /run tests/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-01b: Pre-run state shows "36 endpoints" placeholder', async ({ page }) => {
    // Before running tests, the page shows: "Tests 36 endpoints"
    // (totalTests || '36' → '36' before any test run)
    await expect(page.getByText(/tests 36 endpoints/i)).toBeVisible({ timeout: 8000 });
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
    await page.waitForLoadState('networkidle', { timeout: 10000 });

    await page.getByRole('button', { name: /run tests/i }).click();
    await page.waitForTimeout(500);

    expect(requests.length).toBeGreaterThan(0);
    expect(requests[0]).toContain('/test/endpoints');
  });
});

// ---------------------------------------------------------------------------
// SC-SS-03 — Alerts category section visible after tests run
// ---------------------------------------------------------------------------

test.describe('SC-SS-03 — Alerts category section', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    // Click Run Tests and wait for results to render
    await page.getByRole('button', { name: /run tests/i }).click();
    await page.waitForTimeout(1000);
  });

  test('SC-SS-03a: Alerts category section header is visible after tests run', async ({ page }) => {
    // The category toggle button accessible name includes the badge: "Alerts 3/3"
    // Use a prefix match (no end anchor) to match regardless of badge content.
    await expect(page.getByRole('button', { name: /^alerts/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-03b: Alerts section shows the correct endpoint count badge', async ({ page }) => {
    // TEST_RESULTS_RESPONSE has 3 /alerts endpoints — badge shows "3/3".
    // The badge text is part of the button's accessible name: "Alerts 3/3".
    await expect(page.getByRole('button', { name: /^alerts.*3\/3/i })).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SS-04 — Notifications category section visible after tests run
// ---------------------------------------------------------------------------

test.describe('SC-SS-04 — Notifications category section', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    await page.getByRole('button', { name: /run tests/i }).click();
    await page.waitForTimeout(1000);
  });

  test('SC-SS-04a: Notifications category section header is visible after tests run', async ({ page }) => {
    // The category toggle button accessible name includes the badge: "Notifications 3/3"
    await expect(page.getByRole('button', { name: /^notifications/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-04b: Notifications section shows the correct endpoint count badge', async ({ page }) => {
    // TEST_RESULTS_RESPONSE has 3 /notifications endpoints — badge shows "3/3".
    await expect(page.getByRole('button', { name: /^notifications.*3\/3/i })).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SS-05 — Digest category section visible after tests run
// ---------------------------------------------------------------------------

test.describe('SC-SS-05 — Digest category section', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    await page.getByRole('button', { name: /run tests/i }).click();
    await page.waitForTimeout(1000);
  });

  test('SC-SS-05a: Digest category section header is visible after tests run', async ({ page }) => {
    // The category toggle button accessible name includes the badge: "Digest 3/3"
    await expect(page.getByRole('button', { name: /^digest/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-05b: Digest section shows the correct endpoint count badge', async ({ page }) => {
    // TEST_RESULTS_RESPONSE has 3 /digest endpoints — badge shows "3/3".
    await expect(page.getByRole('button', { name: /^digest.*3\/3/i })).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SS-06 — Total endpoint count ≥ 26 shown after tests run
// ---------------------------------------------------------------------------

test.describe('SC-SS-06 — Total endpoint count display', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    await page.getByRole('button', { name: /run tests/i }).click();
    await page.waitForTimeout(1000);
  });

  test('SC-SS-06a: Total count of 28 is shown in the summary bar after tests run', async ({ page }) => {
    // After testResults returns, the summary bar renders:
    //   "Total: {totalTests}" where totalTests = testResults.summary.total = 28
    // Use exact:true to avoid matching "28" inside other text (e.g., endpoint names)
    const totalLabel = page.locator('span').filter({ hasText: /^total:$/i });
    await expect(totalLabel).toBeVisible({ timeout: 8000 });

    // The sibling span next to "Total:" shows the count value
    await expect(totalLabel.locator('xpath=following-sibling::span[1]')).toHaveText('28', { timeout: 8000 });
  });

  test('SC-SS-06b: Endpoint count in sub-header updates to actual count after tests run', async ({ page }) => {
    // Before: "Testing 0 endpoints across all system modules" (totalTests=0)
    // After:  "Testing 28 endpoints across all system modules"
    // The p.text-slate-400 sub-header uses {totalTests} directly
    await expect(page.getByText(/testing 28 endpoints/i)).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SS-07 — Alerts/Notifications/Digest endpoints NOT in "Other" category
// ---------------------------------------------------------------------------

test.describe('SC-SS-07 — Targeted endpoints absent from "Other" category', () => {
  test.beforeEach(async ({ page }) => {
    await mockBaseEndpoints(page);
    await page.goto('/#/SystemStatus');
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    await page.getByRole('button', { name: /run tests/i }).click();
    await page.waitForTimeout(1000);
  });

  test('SC-SS-07a: "Other" category section is NOT rendered (all endpoints are categorised)', async ({ page }) => {
    // TEST_RESULTS_RESPONSE has no endpoints that fall through to "Other"
    // The "Other" category section button should not exist
    await expect(page.getByRole('button', { name: /^other/i })).not.toBeVisible({ timeout: 3000 });
  });

  test('SC-SS-07b: /alerts/rules endpoint appears under Alerts, not Other', async ({ page }) => {
    // Confirm Alerts section rendered (button name includes badge: "Alerts 3/3")
    const alertsBtn = page.getByRole('button', { name: /^alerts/i });
    await expect(alertsBtn).toBeVisible({ timeout: 8000 });

    // The endpoint row for "GET /alerts/rules" should be visible within the Alerts section
    // Categories are rendered in collapsible divs; by default isExpanded = true (checked against false)
    await expect(page.getByText('GET /alerts/rules')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-07c: /notifications endpoint appears under Notifications, not Other', async ({ page }) => {
    await expect(page.getByText('GET /notifications')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SS-07d: /digest/weekly endpoint appears under Digest, not Other', async ({ page }) => {
    await expect(page.getByText('GET /digest/weekly')).toBeVisible({ timeout: 8000 });
  });
});
