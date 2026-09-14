'use strict';
/**
 * SignalCard — Consolidated Playwright E2E Coverage
 * ST-05 (BLG-QA-82, v9.3 EPIC-02)
 *
 * Consolidates 3 previously-separate spec files that each covered a different
 * SignalCard feature added incrementally over time, with overlapping page
 * setup/mocking boilerplate:
 *   - signals-add-to-watchlist.spec.js   (ST-02, BLG-FE-33, v3.7 EPIC-01)
 *   - signals-cash-balance.spec.js       (ST-16, v2.6 EPIC-01 test gap closure)
 *   - signals-allocation-insufficient.spec.js (ST-04, BLG-FE-61, v5.1 EPIC-03)
 *
 * No scenario coverage was dropped in the consolidation — every SC-* scenario
 * ID below has a 1:1 counterpart in the original 3 files (see git history for
 * the pre-consolidation versions). Grouped into 3 `test.describe` sections,
 * one per source feature, each with its own namespaced mock helpers (helper
 * names below are prefixed per section to avoid the naming collisions that
 * existed across the original files, e.g. two independent `mockSignals`
 * implementations with different signatures).
 *
 * Infrastructure:
 * - Playwright page.route() network interception. No live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Signals').
 */

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// =============================================================================
// SC-SIG-WL — Add to Watchlist CTA (from signals-add-to-watchlist.spec.js)
// =============================================================================
//   SC-SIG-WL-01: Add to Watchlist happy path — new signal card shows CTA,
//                 clicking it calls POST /watchlist + PATCH /signals/{id},
//                 card transitions to watchlisted state with "View in Watchlist" link.
//   SC-SIG-WL-02: Duplicate add — 409 from POST /watchlist shows "Already on your watchlist"
//                 toast; signal still transitions to watchlisted state.
//   SC-SIG-WL-03: No "Add Position" CTA present on new signal cards (non-regression).

const WL_MOCK_SIGNAL = {
  id: 'sig-uuid-0001',
  ticker: 'AAPL',
  market: 'US',
  signal_date: '2026-05-18',
  rank: 1,
  momentum_percent: 18.5,
  current_price: 182.30,
  price_gbp: 143.00,
  atr_value: 3.45,
  volatility: 0.012,
  initial_stop: 164.85,
  suggested_shares: 10,
  allocation_gbp: 1430.00,
  total_cost: 1430.00,
  status: 'new',
};

const WL_MOCK_WATCHLISTED_SIGNAL = { ...WL_MOCK_SIGNAL, status: 'watchlisted' };

const WL_MARKET_STATUS = {
  spy: { price: 521.0, ma200: 480.0, is_risk_on: true },
  ftse: { price: 7800.0, ma200: 7200.0, is_risk_on: true },
  fx_rate: 1.27,
};

const WL_CASH_SUMMARY = { current_cash: 10000.0 };

async function wlSetupBaseRoutes(page, signalStatus = 'new') {
  const signal = signalStatus === 'watchlisted' ? WL_MOCK_WATCHLISTED_SIGNAL : WL_MOCK_SIGNAL;

  await page.route(`${API}/signals**`, async (route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({ json: { status: 'ok', data: [signal] } });
    } else {
      await route.fallback();
    }
  });

  await page.route(`${API}/signals/${WL_MOCK_SIGNAL.id}`, async (route) => {
    if (route.request().method() === 'PATCH') {
      await route.fulfill({ json: { status: 'ok', data: { ...signal, status: 'watchlisted' } } });
    } else {
      await route.continue();
    }
  });

  await page.route(`${API}/market/status`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: WL_MARKET_STATUS } });
  });

  await page.route(`${API}/cash/summary`, async (route) => {
    await route.fulfill({ json: { status: 'ok', ...WL_CASH_SUMMARY } });
  });

  await page.route(`${API}/positions**`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: [] } });
  });
}

test.describe('SC-SIG-WL-01 — Add to Watchlist happy path', () => {
  test('New signal card shows "Add to Watchlist" button and transitions to watchlisted state', async ({ page }) => {
    await wlSetupBaseRoutes(page, 'new');

    // Mock POST /watchlist → 201 success
    await page.route(`${API}/watchlist`, async (route) => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 201,
          json: { status: 'ok', data: { id: 'wl-uuid-0001', ticker: 'AAPL', market: 'US' } },
        });
      } else {
        await route.continue();
      }
    });

    // After PATCH, return watchlisted signal on next GET /signals
    let patchCalled = false;
    await page.route(`${API}/signals/${WL_MOCK_SIGNAL.id}`, async (route) => {
      if (route.request().method() === 'PATCH') {
        patchCalled = true;
        await route.fulfill({ json: { status: 'ok', data: WL_MOCK_WATCHLISTED_SIGNAL } });
      } else {
        await route.continue();
      }
    });

    // After PATCH, refetch returns watchlisted signal
    let fetchCount = 0;
    await page.route(`${API}/signals**`, async (route) => {
      if (route.request().method() === 'GET') {
        fetchCount++;
        const signal = fetchCount > 1 ? WL_MOCK_WATCHLISTED_SIGNAL : WL_MOCK_SIGNAL;
        await route.fulfill({ json: { status: 'ok', data: [signal] } });
      } else {
        await route.fallback();
      }
    });

    await page.goto('/#/Signals');

    // Verify "Add to Watchlist" button is present
    const addBtn = page.getByTestId('add-to-watchlist-btn');
    await expect(addBtn).toBeVisible({ timeout: 8000 });
    await expect(addBtn).toContainText('Add to Watchlist');

    // No "Add Position" button present (non-regression)
    await expect(page.getByRole('button', { name: /add position/i })).not.toBeVisible();

    // Click Add to Watchlist
    await addBtn.click();

    // After click, watchlisted state appears
    const viewLink = page.getByTestId('view-in-watchlist-link');
    await expect(viewLink).toBeVisible({ timeout: 5000 });
    await expect(viewLink).toContainText('View in Watchlist');
  });
});

test.describe('SC-SIG-WL-02 — Duplicate add handling', () => {
  test('409 from POST /watchlist shows toast and signal still transitions to watchlisted', async ({ page }) => {
    await wlSetupBaseRoutes(page, 'new');

    // POST /watchlist → 409 duplicate
    await page.route(`${API}/watchlist`, async (route) => {
      if (route.request().method() === 'POST') {
        await route.fulfill({ status: 409, json: { detail: 'ticker already on watchlist' } });
      } else {
        await route.continue();
      }
    });

    // After PATCH, return watchlisted signal on next GET
    let fetchCount = 0;
    await page.route(`${API}/signals**`, async (route) => {
      if (route.request().method() === 'GET') {
        fetchCount++;
        const signal = fetchCount > 1 ? WL_MOCK_WATCHLISTED_SIGNAL : WL_MOCK_SIGNAL;
        await route.fulfill({ json: { status: 'ok', data: [signal] } });
      } else {
        await route.fallback();
      }
    });

    await page.goto('/#/Signals');

    const addBtn = page.getByTestId('add-to-watchlist-btn');
    await expect(addBtn).toBeVisible({ timeout: 8000 });
    await addBtn.click();

    // Toast: "Already on your watchlist"
    await expect(page.getByText(/already on your watchlist/i)).toBeVisible({ timeout: 5000 });

    // Signal still transitions to watchlisted
    const viewLink = page.getByTestId('view-in-watchlist-link');
    await expect(viewLink).toBeVisible({ timeout: 5000 });
  });
});

test.describe('SC-SIG-WL-03 — No Add Position CTA on signal cards', () => {
  test('"Add Position" button is absent from new signal cards', async ({ page }) => {
    await wlSetupBaseRoutes(page, 'new');
    await page.goto('/#/Signals');

    // Wait for signal card to render
    await expect(page.getByTestId('add-to-watchlist-btn')).toBeVisible({ timeout: 8000 });

    // "Add Position" must not be present
    const addPositionBtn = page.getByRole('button', { name: /add position/i });
    await expect(addPositionBtn).not.toBeVisible();
  });
});

// =============================================================================
// SC-SIG-CB — Cash Balance Integration (from signals-cash-balance.spec.js)
// =============================================================================
//   SC-SIG-CB-01: Cash balance rendered from /cash/summary current_cash field
//   SC-SIG-CB-02: Cash balance falls back to £0.00 when /cash/summary returns null/error
//
// - api.cash.getSummary() → GET /cash/summary
//   availableCashBalance = cashSummary?.current_cash ?? 0
// - availableCash is passed to PositionSizerPanel which renders it as a
//   formatted currency string.

const CB_CASH_SUMMARY_FUNDED = {
  current_cash: 8250.00,
  total_deposited: 10000.00,
  total_withdrawn: 0.00,
  realised_pnl: 750.00,
  unrealised_pnl: 0.00,
};

const CB_SIGNALS_LIST = [
  {
    id: 'sig-1',
    ticker: 'LGEN',
    market: 'UK',
    status: 'active',
    signal_date: '2026-04-10',
    direction: 'long',
    entry_price: 220.00,
    stop_price: 200.00,
    target_price: 260.00,
    risk_reward: 2.0,
    atr: 8.5,
    rationale: 'Breakout above resistance',
  },
];

async function cbMockSignals(page, signals = CB_SIGNALS_LIST) {
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

async function cbMockCashSummary(page, payload = CB_CASH_SUMMARY_FUNDED) {
  await page.route(`${API}/cash/summary`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload),
    })
  );
}

async function cbMockCashSummaryError(page) {
  await page.route(`${API}/cash/summary`, (route) =>
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ detail: 'Internal Server Error' }),
    })
  );
}

/** Catch-all: prevent unmocked endpoints from hanging tests */
async function cbMockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

test.describe('SC-SIG-CB-01 — Cash balance from /cash/summary', () => {
  test.beforeEach(async ({ page }) => {
    // Catch-all first — Playwright routes are LIFO, so registering catch-all first
    // ensures the specific mocks below take precedence.
    await cbMockFallback(page);
    await cbMockCashSummary(page, CB_CASH_SUMMARY_FUNDED);
    await cbMockSignals(page);
    await page.goto('/#/Signals');
    // Wait for all API calls to settle before asserting
  });

  test('SC-SIG-CB-01a: GET /cash/summary is called on Signals page load', async ({ page }) => {
    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await cbMockFallback(page);
    await cbMockCashSummary(page, CB_CASH_SUMMARY_FUNDED);
    await cbMockSignals(page);

    // Attach request listener before navigation so no requests are missed.
    const cashRequests = [];
    page.on('request', (req) => {
      if (req.url().includes('/cash/summary')) cashRequests.push(req.url());
    });

    // Navigate to about:blank to fully destroy the React app and React Query cache
    // (beforeEach already navigated to /#/Signals and warmed the cache; changing the
    // hash alone keeps the SPA mounted so React Query serves from cache and skips the fetch).
    await page.goto('about:blank');

    // DEV-EPIC02-ST08-01 (BLG-TECH-18/ST-08, v9.1): page.goto() only waits for
    // the 'load' event, not for React to mount and useQuery's queryFn to
    // actually fire — a quarterly dependency bump shifted bundle init/parse
    // timing enough that goto() now reliably resolves before the app's first
    // /cash/summary fetch, where it previously (coincidentally) didn't. Wait
    // for the actual request alongside the navigation (Playwright's standard
    // trigger-and-wait-concurrently pattern) instead of asserting immediately
    // after goto() resolves — confirmed via a local reproduction that this is
    // a pure test-synchronization gap, not an app behaviour change: the fetch
    // reliably fires, just not always before this line used to run.
    await Promise.all([
      page.waitForRequest((req) => req.url().includes('/cash/summary'), { timeout: 10000 }),
      page.goto('/#/Signals'),
    ]);

    expect(cashRequests.length).toBeGreaterThan(0);
    expect(cashRequests[0]).toContain('/cash/summary');
  });

  test('SC-SIG-CB-01b: Available cash rendered from current_cash field', async ({ page }) => {
    // availableCashBalance = cashSummary.current_cash = 8250.00
    // PositionSizerPanel renders this as a formatted currency string
    // Exact format depends on the component — check for the numeric value
    await expect(page.getByText(/8[,.]?250/)).toBeVisible({ timeout: 8000 });
  });
});

test.describe('SC-SIG-CB-02 — Cash balance fallback to 0', () => {
  test('SC-SIG-CB-02a: Cash shows 0 when /cash/summary returns server error', async ({ page }) => {
    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await cbMockFallback(page);
    await cbMockCashSummaryError(page);
    await cbMockSignals(page);
    await page.goto('/#/Signals');
    await page.waitForTimeout(500);

    // availableCashBalance = cashSummary?.current_cash ?? 0 = 0
    // Should render 0 / £0 / £0.00 — not a hard crash
    // Verify the page rendered without throwing (no error boundary shown)
    await expect(page.locator('body')).not.toContainText('Something went wrong');
    // Verify 0 cash is rendered. Use exact:true + first() to avoid strict-mode violation:
    // the regex also matches signal price data ("£0.00 vs MA200") and other zero values.
    // The cash balance renders as a bold "£0" element (distinct from small signal data text).
    await expect(page.getByText('£0', { exact: true }).first()).toBeVisible({ timeout: 8000 });
  });

  test('SC-SIG-CB-02b: Cash shows 0 when /cash/summary returns null current_cash', async ({ page }) => {
    // Catch-all first — LIFO order ensures specific mocks below take precedence.
    await cbMockFallback(page);
    await page.route(`${API}/cash/summary`, (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ current_cash: null, total_deposited: 0 }),
      })
    );
    await cbMockSignals(page);
    await page.goto('/#/Signals');
    await page.waitForTimeout(500);

    // cashSummary?.current_cash ?? 0 → 0 when current_cash is null
    await expect(page.locator('body')).not.toContainText('Something went wrong');
    // Use exact:true + first() — same strict-mode fix as SC-SIG-CB-02a.
    await expect(page.getByText('£0', { exact: true }).first()).toBeVisible({ timeout: 8000 });
  });
});

// =============================================================================
// SC-SIG-AI — allocation_insufficient badge (from signals-allocation-insufficient.spec.js)
// =============================================================================
//   SC-SIG-AI-01: Orange "Cannot Size" badge visible when status=allocation_insufficient
//   SC-SIG-AI-02: Reason text rendered inline on the signal card
//   SC-SIG-AI-03: allocation_insufficient signal is visually distinct from active signals
//
// - Signal payload uses backend field names: rank, momentum_percent, current_price,
//   initial_stop, status, reason (see backend/services/signal_service.py).

const AI_ALLOCATION_INSUFFICIENT_SIGNAL = {
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
const AI_ACTIVE_SIGNAL = {
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

async function aiMockSignals(page, signals) {
  await page.route(`${API}/signals**`, (route) => {
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

async function aiMockCashSummary(page) {
  await page.route(`${API}/cash/summary`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ current_cash: 150.00, total_deposited: 10000.00 }),
    })
  );
}

async function aiMockPositions(page) {
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { positions: [] } }),
    })
  );
}

/** Catch-all: prevent unmocked endpoints from hanging tests */
async function aiMockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [] }),
    })
  );
}

async function aiNavigateToSignals(page) {
  await page.goto('/#/Signals');
  await expect(page.locator('body')).not.toContainText('Something went wrong', { timeout: 8000 });
}

test.describe('SC-SIG-AI-01 — Cannot Size badge rendered', () => {
  test.beforeEach(async ({ page }) => {
    await aiMockFallback(page);
    await aiMockCashSummary(page);
    await aiMockPositions(page);
    await aiMockSignals(page, [AI_ALLOCATION_INSUFFICIENT_SIGNAL]);
  });

  test('SC-SIG-AI-01a: orange "Cannot Size" badge is visible on the signal card', async ({ page }) => {
    await aiNavigateToSignals(page);
    // Badge label "Cannot Size" rendered via statusConfig.allocation_insufficient.label
    await expect(page.getByText('Cannot Size')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SIG-AI-01b: "Allocation insufficient" panel is rendered below the card metrics', async ({ page }) => {
    await aiNavigateToSignals(page);
    // The orange bottom panel shows "⚠ Allocation insufficient"
    await expect(page.getByText(/Allocation insufficient/)).toBeVisible({ timeout: 8000 });
  });
});

test.describe('SC-SIG-AI-02 — Reason text rendered inline', () => {
  test('SC-SIG-AI-02a: reason string is rendered within the allocation_insufficient card', async ({ page }) => {
    await aiMockFallback(page);
    await aiMockCashSummary(page);
    await aiMockPositions(page);
    await aiMockSignals(page, [AI_ALLOCATION_INSUFFICIENT_SIGNAL]);

    await aiNavigateToSignals(page);
    // Reason text rendered as: signal.reason inside the orange panel
    await expect(
      page.getByText('Insufficient cash to meet minimum position size of £500')
    ).toBeVisible({ timeout: 8000 });
  });

  test('SC-SIG-AI-02b: signal with no reason renders card without error', async ({ page }) => {
    const noReasonSignal = { ...AI_ALLOCATION_INSUFFICIENT_SIGNAL, reason: null };

    await aiMockFallback(page);
    await aiMockCashSummary(page);
    await aiMockPositions(page);
    await aiMockSignals(page, [noReasonSignal]);

    await aiNavigateToSignals(page);
    // Card renders without crashing; badge still shows
    await expect(page.getByText('Cannot Size')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('body')).not.toContainText('Something went wrong');
  });
});

test.describe('SC-SIG-AI-03 — Distinct from active signals', () => {
  test('SC-SIG-AI-03a: active signal shows "New Signal" badge, not "Cannot Size"', async ({ page }) => {
    await aiMockFallback(page);
    await aiMockCashSummary(page);
    await aiMockPositions(page);
    // Mix: one allocation_insufficient, one new/active
    await aiMockSignals(page, [AI_ALLOCATION_INSUFFICIENT_SIGNAL, AI_ACTIVE_SIGNAL]);

    await aiNavigateToSignals(page);
    // Both cards rendered
    await expect(page.getByText('Cannot Size')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('New Signal', { exact: true })).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('Cannot Size')).toHaveCount(1);
  });
});
