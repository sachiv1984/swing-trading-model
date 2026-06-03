'use strict';
/**
 * ST-04 (BLG-FE-61, v5.1 EPIC-03)
 * SignalCard allocation_insufficient badge — Playwright E2E coverage
 *
 * Covers the observable AC deferred from v5.0 EPIC-03 ST-06:
 *   SC-SIG-AI-01: Orange "Cannot Size" badge visible when status=allocation_insufficient
 *   SC-SIG-AI-02: Reason text rendered inline on the signal card
 *   SC-SIG-AI-03: allocation_insufficient signal is visually distinct from active signals
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Signals').
 * - Signal payload uses backend field names: rank, momentum_percent, current_price,
 *   initial_stop, status, reason (see backend/services/signal_service.py).
 */

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

/** allocation_insufficient signal with a non-empty reason */
const ALLOCATION_INSUFFICIENT_SIGNAL = {
  id: 'sig-ai-1',
  ticker: 'BARC',
  market: 'UK',
  status: 'allocation_insufficient',
  signal_date: '2026-06-21',
  rank: 1,
  momentum_percent: 12.3,
  current_price: 220.50,
  initial_stop: 205.00,
  suggested_shares: 0,
  total_cost: 0,
  reason: 'Insufficient cash to meet minimum position size of £500',
};

/** Active signal for contrast (status=new) */
const ACTIVE_SIGNAL = {
  id: 'sig-active-1',
  ticker: 'LGEN',
  market: 'UK',
  status: 'new',
  signal_date: '2026-06-21',
  rank: 2,
  momentum_percent: 8.5,
  current_price: 210.00,
  initial_stop: 195.00,
  suggested_shares: 5,
  total_cost: 1050.00,
  reason: null,
};

// ---------------------------------------------------------------------------
// Shared setup helpers
// ---------------------------------------------------------------------------

async function mockSignals(page, signals) {
  await page.route(`${API}/signals`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: signals }),
      });
    } else {
      route.continue();
    }
  });
}

async function mockCashSummary(page) {
  await page.route(`${API}/cash/summary`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ current_cash: 150.00, total_deposited: 10000.00 }),
    })
  );
}

async function mockPositions(page) {
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { positions: [] } }),
    })
  );
}

/** Catch-all: prevent unmocked endpoints from hanging tests */
async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

async function navigateToSignals(page) {
  await page.goto('/#/Signals');
  await expect(page.locator('body')).not.toContainText('Something went wrong', { timeout: 8000 });
}

// ---------------------------------------------------------------------------
// SC-SIG-AI-01: "Cannot Size" badge visible when status=allocation_insufficient
// ---------------------------------------------------------------------------

test.describe('SC-SIG-AI-01 — Cannot Size badge rendered', () => {
  test.beforeEach(async ({ page }) => {
    await mockFallback(page);
    await mockCashSummary(page);
    await mockPositions(page);
    await mockSignals(page, [ALLOCATION_INSUFFICIENT_SIGNAL]);
  });

  test('SC-SIG-AI-01a: orange "Cannot Size" badge is visible on the signal card', async ({ page }) => {
    await navigateToSignals(page);
    // Badge label "Cannot Size" rendered via statusConfig.allocation_insufficient.label
    await expect(page.getByText('Cannot Size')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SIG-AI-01b: "Allocation insufficient" panel is rendered below the card metrics', async ({ page }) => {
    await navigateToSignals(page);
    // The orange bottom panel shows "⚠ Allocation insufficient"
    await expect(page.getByText(/Allocation insufficient/)).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SIG-AI-02: Reason text rendered inline on the signal card
// ---------------------------------------------------------------------------

test.describe('SC-SIG-AI-02 — Reason text rendered inline', () => {
  test('SC-SIG-AI-02a: reason string is rendered within the allocation_insufficient card', async ({ page }) => {
    await mockFallback(page);
    await mockCashSummary(page);
    await mockPositions(page);
    await mockSignals(page, [ALLOCATION_INSUFFICIENT_SIGNAL]);

    await navigateToSignals(page);
    // Reason text rendered as: signal.reason inside the orange panel
    await expect(
      page.getByText('Insufficient cash to meet minimum position size of £500')
    ).toBeVisible({ timeout: 8000 });
  });

  test('SC-SIG-AI-02b: signal with no reason renders card without error', async ({ page }) => {
    const noReasonSignal = { ...ALLOCATION_INSUFFICIENT_SIGNAL, reason: null };

    await mockFallback(page);
    await mockCashSummary(page);
    await mockPositions(page);
    await mockSignals(page, [noReasonSignal]);

    await navigateToSignals(page);
    // Card renders without crashing; badge still shows
    await expect(page.getByText('Cannot Size')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('body')).not.toContainText('Something went wrong');
  });
});

// ---------------------------------------------------------------------------
// SC-SIG-AI-03: allocation_insufficient is visually distinct from active signals
// ---------------------------------------------------------------------------

test.describe('SC-SIG-AI-03 — Distinct from active signals', () => {
  test('SC-SIG-AI-03a: active signal shows "New Signal" badge, not "Cannot Size"', async ({ page }) => {
    await mockFallback(page);
    await mockCashSummary(page);
    await mockPositions(page);
    // Mix: one allocation_insufficient, one new/active
    await mockSignals(page, [ALLOCATION_INSUFFICIENT_SIGNAL, ACTIVE_SIGNAL]);

    await navigateToSignals(page);
    // Both cards rendered
    await expect(page.getByText('Cannot Size')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('New Signal')).toBeVisible({ timeout: 8000 });
    // Only one "Cannot Size" badge (the allocation_insufficient signal)
    await expect(page.getByText('Cannot Size')).toHaveCount(1);
  });
});
