/**
 * EPIC-01 v6.2 — Trailing Stop Display, Risk-Off Alerts, Rebalance Exit Signals
 *
 * Coverage (ST-01 through ST-05, BLG-FEAT-46/47/49):
 *
 *   SC-TS-01  Trailing stop value shown in Stop column (ST-02/AC-01)
 *   SC-TS-02  "Init: £X.XX" label present in Stop column (ST-02/AC-01)
 *   SC-TS-03  Breach badge present when current_price ≤ current_trailing_stop (ST-02/AC-02)
 *   SC-TS-04  Breach badge has rose styling — distinct from risk-off blue (ST-02/AC-03)
 *   SC-TS-05  No breach badge when current_price > current_trailing_stop (ST-02/AC-04)
 *   SC-TS-06  No breach badge when current_trailing_stop is zero (ST-02/AC-04)
 *
 *   SC-RO-01  "RISK OFF" badge present when risk_off_exit=true (ST-05/AC-02)
 *   SC-RO-02  Risk-off badge uses spec colour #1E40AF — distinct from breach rose (ST-03/BLG-FE-107, v7.1)
 *   SC-RO-03  No risk-off badge when risk_off_exit=false (ST-05/AC-02)
 *   SC-RO-04  US position risk_off_exit=true shows badge (ST-05/AC-04)
 *   SC-RO-05  UK position risk_off_exit=true shows badge (ST-05/AC-04)
 *   SC-RO-06  US position risk_off_exit=false — no badge (ST-05/AC-04 isolation)
 *
 *   SC-TS-RO-01  Both badges simultaneously on same row (ST-02 + ST-05)
 *
 *   SC-RB-01  exit_rebalance signal shows "Month-End Exit" label (ST-03/AC-05)
 *   SC-RB-02  exit_rebalance badge has amber styling — distinct from new-signal cyan (ST-03/AC-05)
 *   SC-RB-03  exit_rebalance signal visible alongside new signals in list (ST-03/AC-05)
 *
 * Visual assertions use CSS class checks (not pixel screenshots) — consistent with
 * visual-snapshots.spec.js. Reliable across platforms in CI; no snapshot baselines needed.
 *
 * HashRouter: all navigation via page.goto('/#/…')
 * Table view uses [aria-label="Table view"] locator.
 */

'use strict';

const { test, expect } = require('@playwright/test');

// ---------------------------------------------------------------------------
// Mock data builders
// ---------------------------------------------------------------------------

function makePosition(overrides = {}) {
  const merged = {
    id: 'pos-epic01-01',
    ticker: 'AAPL',
    market: 'US',
    entry_price: 150.00,
    current_price: 120.00,
    current_price_native: 150.00,
    stop_price: 130.00,
    stop_price_native: 162.50,
    shares: 10,
    pnl: -300.00,
    pnl_percent: -20.00,
    holding_days: 15,
    grace_days_remaining: null,
    status: 'open',
    entry_date: '2026-05-01',
    initial_stop: 130.00,
    current_trailing_stop: 0,
    risk_off_exit: false,
    tags: null,
    ...overrides,
  };
  // ST-02 (BLG-BE-103, v8.9): these fixtures predate current_trailing_stop_native
  // and don't model currency conversion — mirror current_trailing_stop unless a
  // test explicitly overrides it, so existing scenarios asserting on a single
  // trailing-stop number keep exercising the same value under the corrected
  // native-display field (PositionCard.js/Positions.js now render
  // current_trailing_stop_native, not the GBP-basis current_trailing_stop).
  if (merged.current_trailing_stop_native === undefined) {
    merged.current_trailing_stop_native = merged.current_trailing_stop;
  }
  return merged;
}

function makeSignal(overrides = {}) {
  return {
    id: 'sig-epic01-01',
    ticker: 'AAPL',
    market: 'US',
    rank: 1,
    momentum_percent: 42.5,
    current_price: 150.00,
    price_gbp: 120.00,
    atr_value: 5.00,
    volatility: 1.8,
    initial_stop: 125.00,
    status: 'new',
    allocation_gbp: 1000.00,
    suggested_shares: 8,
    total_cost: 984.00,
    signal_date: '2026-06-24',
    created_at: '2026-06-24T10:00:00Z',
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// Route helpers
// ---------------------------------------------------------------------------

async function stubPositionsPage(page, positions) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/positions/compliance')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) });
  });
  await page.route('**/portfolio*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/compliance/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null, days_until_earnings: null }) })
  );
  // Layout-level routes (sidebar badge, watchlist icon)
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
}

async function gotoPositionsTable(page, positions) {
  await stubPositionsPage(page, positions);
  await page.goto('/#/Positions');
  // Wait for ticker, then switch to table view
  const firstTicker = positions[0]?.ticker || 'AAPL';
  await page.waitForSelector(`text=${firstTicker}`, { timeout: 8000 });
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 8000 });
  await tableBtn.click();
  await page.waitForSelector('table', { timeout: 5000 });
}

async function stubSignalsPage(page, signals, positions = []) {
  await page.route('**/signals**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(signals) })
  );
  await page.route('**/positions**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) })
  );
  await page.route('**/cash/summary**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ current_cash: 10000 }) })
  );
  await page.route('**/market/status**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ spy: { is_risk_on: true, price: 530 }, ftse: { is_risk_on: true, price: 8300 }, fx_rate: 1.25 }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
}

// ---------------------------------------------------------------------------
// ST-02 — Trailing stop display (Positions table)
// ---------------------------------------------------------------------------

test('SC-TS-01: Trailing stop value shown in Stop column', async ({ page }) => {
  const pos = makePosition({ current_trailing_stop: 115.00, current_price: 118.00, market: 'UK' });
  await gotoPositionsTable(page, [pos]);

  // Trailing stop £115.00 rendered in Stop cell (UK position → £ symbol)
  await expect(page.locator('text=£115.00').first()).toBeVisible({ timeout: 5000 });
});

test('SC-TS-02: "Init:" label present in Stop column', async ({ page }) => {
  const pos = makePosition({ initial_stop: 130.00, current_trailing_stop: 115.00 });
  await gotoPositionsTable(page, [pos]);

  // "Init: £130.00" sub-label shown above the trailing stop value
  await expect(page.locator('text=/Init:.*130/').first()).toBeVisible({ timeout: 5000 });
});

test('SC-TS-03: Breach badge present when current_price ≤ current_trailing_stop', async ({ page }) => {
  // GBP price 120 ≤ trailing stop 125 → BREACH
  const pos = makePosition({ current_price: 120.00, current_trailing_stop: 125.00 });
  await gotoPositionsTable(page, [pos]);

  const badge = page.locator('[data-testid="breach-badge"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toContainText('BREACH');
});

test('SC-TS-04: Breach badge has spec orange styling — distinct from risk-off blue and GAP RISK amber (ST-09, BLG-FE-96)', async ({ page }) => {
  const pos = makePosition({ current_price: 120.00, current_trailing_stop: 125.00 });
  await gotoPositionsTable(page, [pos]);

  const badge = page.locator('[data-testid="breach-badge"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  // orange classes applied — ST-09/BLG-FE-96, matches positions.md §Trailing Stop Column (#EA580C)
  await expect(badge).toHaveClass(/bg-orange-600/);
  await expect(badge).toHaveClass(/text-white/);
  // must NOT have amber classes (those belong to GAP RISK badge only)
  await expect(badge).not.toHaveClass(/text-amber/);
  await expect(badge).not.toHaveClass(/bg-amber/);
});

test('SC-TS-05: No breach badge when current_price > current_trailing_stop', async ({ page }) => {
  // Price 135 > trailing stop 115 → no breach
  const pos = makePosition({ current_price: 135.00, current_trailing_stop: 115.00 });
  await gotoPositionsTable(page, [pos]);

  const badge = page.locator('[data-testid="breach-badge"]');
  await expect(badge).not.toBeVisible({ timeout: 5000 });
});

test('SC-TS-06: No breach badge when current_trailing_stop is zero', async ({ page }) => {
  // Guard: trailStop > 0 required before breach logic fires
  const pos = makePosition({ current_price: 120.00, current_trailing_stop: 0 });
  await gotoPositionsTable(page, [pos]);

  const badge = page.locator('[data-testid="breach-badge"]');
  await expect(badge).not.toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// ST-05 — Risk-off exit alerts (Positions table)
// ---------------------------------------------------------------------------

test('SC-RO-01: "RISK OFF" badge present when risk_off_exit=true', async ({ page }) => {
  const pos = makePosition({ risk_off_exit: true });
  await gotoPositionsTable(page, [pos]);

  const badge = page.locator('span[title="Risk-off regime: index below MA200 — consider exit"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toContainText('RISK OFF');
});

test('SC-RO-02: Risk-off badge uses spec colour #1E40AF — distinct from breach rose and GAP RISK amber (ST-03, BLG-FE-107)', async ({ page }) => {
  const pos = makePosition({ risk_off_exit: true });
  await gotoPositionsTable(page, [pos]);

  const badge = page.locator('span[title="Risk-off regime: index below MA200 — consider exit"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  // positions.md §Alerts Column spec colour — blue-800 #1E40AF, matching Grid View parity (SC-GVP-02)
  await expect(badge).toHaveCSS('background-color', 'rgb(30, 64, 175)'); // #1E40AF
  // must NOT have amber/rose classes (those belong to GAP RISK / breach badges only)
  await expect(badge).not.toHaveClass(/text-amber/);
  await expect(badge).not.toHaveClass(/bg-amber/);
  await expect(badge).not.toHaveClass(/text-rose/);
  await expect(badge).not.toHaveClass(/bg-rose/);
});

test('SC-RO-03: No risk-off badge when risk_off_exit=false', async ({ page }) => {
  const pos = makePosition({ risk_off_exit: false });
  await gotoPositionsTable(page, [pos]);

  const badge = page.locator('span[title="Risk-off regime: index below MA200 — consider exit"]');
  await expect(badge).not.toBeVisible({ timeout: 5000 });
});

test('SC-RO-04: US position with risk_off_exit=true shows risk-off badge', async ({ page }) => {
  const pos = makePosition({ market: 'US', risk_off_exit: true });
  await gotoPositionsTable(page, [pos]);

  await expect(
    page.locator('span[title="Risk-off regime: index below MA200 — consider exit"]')
  ).toBeVisible({ timeout: 5000 });
});

test('SC-RO-05: UK position with risk_off_exit=true shows risk-off badge', async ({ page }) => {
  const pos = makePosition({
    ticker: 'BP',
    market: 'UK',
    current_price_native: 4.50,
    stop_price_native: 4.00,
    risk_off_exit: true,
  });
  await gotoPositionsTable(page, [pos]);

  await expect(
    page.locator('span[title="Risk-off regime: index below MA200 — consider exit"]')
  ).toBeVisible({ timeout: 5000 });
});

test('SC-RO-06: US position with risk_off_exit=false has no badge (market isolation)', async ({ page }) => {
  // Verifies US risk-off does NOT bleed onto positions that haven't been flagged
  const pos = makePosition({ market: 'US', risk_off_exit: false });
  await gotoPositionsTable(page, [pos]);

  await expect(
    page.locator('span[title="Risk-off regime: index below MA200 — consider exit"]')
  ).not.toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// ST-02 + ST-05 — Both badges on same row
// ---------------------------------------------------------------------------

test('SC-TS-RO-01: Breach and risk-off badges both present when both conditions met', async ({ page }) => {
  const pos = makePosition({
    current_price: 110.00,
    current_trailing_stop: 120.00,   // breach: 110 ≤ 120
    risk_off_exit: true,
  });
  await gotoPositionsTable(page, [pos]);

  await expect(
    page.locator('[data-testid="breach-badge"]')
  ).toBeVisible({ timeout: 5000 });
  await expect(
    page.locator('span[title="Risk-off regime: index below MA200 — consider exit"]')
  ).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// ST-03 — Month-end rebalance exit signals (Signals page)
// ---------------------------------------------------------------------------

test('SC-RB-01: exit_rebalance signal shows "Month-End Exit" label', async ({ page }) => {
  const sig = makeSignal({
    ticker: 'TSLA',
    status: 'exit_rebalance',
    suggested_shares: 0,
    allocation_gbp: 0,
    total_cost: 0,
  });
  await stubSignalsPage(page, [sig]);
  await page.goto('/#/Signals');

  await page.waitForSelector('text=TSLA', { timeout: 8000 });
  await expect(page.locator('text=Month-End Exit').first()).toBeVisible({ timeout: 5000 });
});

test('SC-RB-02: exit_rebalance badge has amber styling — distinct from new-signal cyan', async ({ page }) => {
  const sig = makeSignal({
    ticker: 'TSLA',
    status: 'exit_rebalance',
    suggested_shares: 0,
    allocation_gbp: 0,
    total_cost: 0,
  });
  await stubSignalsPage(page, [sig]);
  await page.goto('/#/Signals');

  await page.waitForSelector('text=Month-End Exit', { timeout: 8000 });

  // The Badge component carries the colour classes directly on the element containing the text
  const badge = page.locator('text=Month-End Exit').first();
  await expect(badge).toHaveClass(/text-amber-400/);
  // Must NOT be cyan (that's the "New Signal" colour)
  await expect(badge).not.toHaveClass(/text-cyan-400/);
});

test('SC-RB-03: exit_rebalance signal visible alongside new signals', async ({ page }) => {
  const signals = [
    makeSignal({ ticker: 'NVDA', status: 'new', rank: 1 }),
    makeSignal({
      id: 'sig-rb-02',
      ticker: 'TSLA',
      status: 'exit_rebalance',
      rank: 2,
      suggested_shares: 0,
      allocation_gbp: 0,
      total_cost: 0,
    }),
  ];
  await stubSignalsPage(page, signals);
  await page.goto('/#/Signals');

  await page.waitForSelector('text=NVDA', { timeout: 8000 });
  await expect(page.locator('text=TSLA').first()).toBeVisible({ timeout: 5000 });
  await expect(page.locator('text=Month-End Exit').first()).toBeVisible({ timeout: 5000 });
});
