/**
 * Screener Data Quality Panel — Playwright Acceptance Tests
 * ST-04 (EPIC-03, v6.0) — AC-07
 *
 * Covers:
 *   SC-SQ-01  FULL state: green badge + loaded ratio (AC-02, AC-03)
 *   SC-SQ-02  DEGRADED state: amber badge + loaded ratio + failed ticker count (AC-02, AC-04)
 *   SC-SQ-03  DEGRADED state: expandable failed ticker list (AC-04)
 *   SC-SQ-04  FAILED state: red badge + retry prompt (AC-02, AC-05)
 *   SC-SQ-05  Stale advisory renders when last_full_run_utc > 24h ago (AC-06)
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/Screener').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock payloads
// ---------------------------------------------------------------------------

function makeScreenerPayload(overrides = {}) {
  return {
    status: 'ok',
    data: {
      results: [],
      run_id: 'run-001',
      run_timestamp: '2026-06-19T08:00:00Z',
      total: 0,
      limit: 200,
      offset: 0,
      degraded_run: false,
      failure_rate: 0,
      tickers_requested: 500,
      tickers_loaded: 480,
      tickers_failed: [],
      run_quality: 'FULL',
      last_full_run_utc: '2026-06-19T08:00:00Z',
      ...overrides,
    },
  };
}

const PAYLOAD_FULL = makeScreenerPayload({
  tickers_requested: 500,
  tickers_loaded: 500,
  tickers_failed: [],
  run_quality: 'FULL',
  last_full_run_utc: '2026-06-19T08:00:00Z',
});

const PAYLOAD_DEGRADED = makeScreenerPayload({
  degraded_run: true,
  failure_rate: 0.25,
  tickers_requested: 500,
  tickers_loaded: 375,
  tickers_failed: ['BBBY', 'SVFAU', 'TRNX'],
  run_quality: 'DEGRADED',
  last_full_run_utc: '2026-06-18T08:00:00Z',
});

const PAYLOAD_FAILED = makeScreenerPayload({
  degraded_run: true,
  failure_rate: 1.0,
  tickers_requested: 500,
  tickers_loaded: 0,
  tickers_failed: [],
  run_quality: 'FAILED',
  last_full_run_utc: null,
});

// Stale: last_full_run_utc is 30 hours ago
const STALE_TIMESTAMP = new Date(Date.now() - 30 * 3600 * 1000).toISOString();
const PAYLOAD_STALE = makeScreenerPayload({
  run_quality: 'FULL',
  last_full_run_utc: STALE_TIMESTAMP,
  tickers_requested: 500,
  tickers_loaded: 500,
});

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
}

async function mockScreener(page, payload) {
  await page.route(new RegExp(`${API}/screener/results`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function gotoScreener(page) {
  await page.goto('/#/Screener');
  await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-SQ-01 — FULL state (AC-02, AC-03)
// ---------------------------------------------------------------------------

test.describe('SC-SQ-01 — FULL state quality panel (AC-02, AC-03)', () => {
  test('SC-SQ-01: FULL quality panel renders with "Full run" badge and loaded ratio', async ({ page }) => {
    await mockFallback(page);
    await mockScreener(page, PAYLOAD_FULL);
    await gotoScreener(page);

    const panel = page.locator('[data-testid="screener-quality-panel"][data-quality="FULL"]');
    await expect(panel).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Full run', { exact: true })).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/500 \/ 500/)).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SQ-02 — DEGRADED state (AC-02, AC-04)
// ---------------------------------------------------------------------------

test.describe('SC-SQ-02 — DEGRADED state quality panel (AC-02, AC-04)', () => {
  test('SC-SQ-02: DEGRADED panel renders with amber badge, loaded ratio, and failure count', async ({ page }) => {
    await mockFallback(page);
    await mockScreener(page, PAYLOAD_DEGRADED);
    await gotoScreener(page);

    const panel = page.locator('[data-testid="screener-quality-panel"][data-quality="DEGRADED"]');
    await expect(panel).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Degraded run')).toBeVisible({ timeout: 5000 });
    // Loaded ratio
    await expect(page.getByText(/375 \/ 500/)).toBeVisible({ timeout: 5000 });
    // Failure count message
    await expect(page.getByText(/3 tickers failed to load/)).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SQ-03 — DEGRADED expandable failed ticker list (AC-04)
// ---------------------------------------------------------------------------

test.describe('SC-SQ-03 — DEGRADED expandable failed ticker list (AC-04)', () => {
  test('SC-SQ-03: Clicking "Show failed tickers" reveals the failed ticker list', async ({ page }) => {
    await mockFallback(page);
    await mockScreener(page, PAYLOAD_DEGRADED);
    await gotoScreener(page);

    await expect(page.locator('[data-testid="screener-quality-panel"][data-quality="DEGRADED"]')).toBeVisible({ timeout: 10000 });
    const showBtn = page.getByRole('button', { name: /show failed tickers/i });
    await expect(showBtn).toBeVisible({ timeout: 5000 });
    await showBtn.click();

    const failedList = page.locator('[data-testid="failed-ticker-list"]');
    await expect(failedList).toBeVisible({ timeout: 5000 });
    await expect(failedList.getByText('BBBY')).toBeVisible({ timeout: 3000 });
    await expect(failedList.getByText('SVFAU')).toBeVisible({ timeout: 3000 });
    await expect(failedList.getByText('TRNX')).toBeVisible({ timeout: 3000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SQ-04 — FAILED state (AC-02, AC-05)
// ---------------------------------------------------------------------------

test.describe('SC-SQ-04 — FAILED state quality panel (AC-02, AC-05)', () => {
  test('SC-SQ-04: FAILED panel renders with red indicator and retry prompt', async ({ page }) => {
    await mockFallback(page);
    await mockScreener(page, PAYLOAD_FAILED);
    await gotoScreener(page);

    const panel = page.locator('[data-testid="screener-quality-panel"][data-quality="FAILED"]');
    await expect(panel).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Screener run failed')).toBeVisible({ timeout: 5000 });
    await expect(page.getByRole('button', { name: /retry/i })).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SQ-05 — Stale advisory (AC-06)
// ---------------------------------------------------------------------------

test.describe('SC-SQ-05 — Stale advisory renders when last_full_run_utc > 24h (AC-06)', () => {
  test('SC-SQ-05: Stale advisory visible when last full run was >24 hours ago', async ({ page }) => {
    await mockFallback(page);
    await mockScreener(page, PAYLOAD_STALE);
    await gotoScreener(page);

    await expect(page.locator('[data-testid="screener-quality-panel"]')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('[data-testid="stale-advisory"]')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/Last full run:.*hours ago/)).toBeVisible({ timeout: 5000 });
  });
});
