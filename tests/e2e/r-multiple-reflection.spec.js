/**
 * R-multiple on Trade Reflection page — Automated Acceptance Tests
 * ST-02 (EPIC-01, v6.3) — BLG-FE-79
 *
 * Covers observable ACs on TradeReflection page:
 *
 *   SC-RM-01  R-multiple shows as numeric value for trade with net_r_multiple (AC-01)
 *   SC-RM-02  R-multiple shows "N/A" for trade with null net_r_multiple / no stop (AC-02)
 *   SC-RM-03  Positive R shown in green; negative in red; null in neutral (AC-01, AC-03)
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/TradeReflection').
 */

'use strict';

const { test, expect } = require('@playwright/test');

// ---------------------------------------------------------------------------
// Seed data — /trades returns { trades: [...] }
// ---------------------------------------------------------------------------

const TRADE_WITH_STOP = {
  id: 'rm-t1',
  ticker: 'NVDA',
  market: 'US',
  entry_price: 500.00,
  exit_price: 545.00,
  exit_reason: 'target',
  exit_date: '2026-05-15',
  holding_days: 14,
  pnl: 562.50,
  net_r_multiple: 1.50,
};

const TRADE_POSITIVE_R = {
  id: 'rm-t2',
  ticker: 'AAPL',
  market: 'US',
  entry_price: 170.00,
  exit_price: 155.00,
  exit_reason: 'stop_hit',
  exit_date: '2026-05-20',
  holding_days: 8,
  pnl: -187.50,
  net_r_multiple: -0.75,
};

const TRADE_NO_STOP = {
  id: 'rm-t3',
  ticker: 'SHEL',
  market: 'UK',
  entry_price: 2500,
  exit_price: 2650,
  exit_reason: 'manual',
  exit_date: '2026-05-25',
  holding_days: 20,
  pnl: 375.00,
  net_r_multiple: null,
};

const TRADES_PAYLOAD = { trades: [TRADE_WITH_STOP, TRADE_POSITIVE_R, TRADE_NO_STOP] };

// ---------------------------------------------------------------------------
// Shared setup
// ---------------------------------------------------------------------------

async function stubRoutesAndLoad(page) {
  await page.route('**/trades**', route => {
    const url = route.request().url();
    if (url.includes('/reflection') || url.includes('/costs')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({}) });
    }
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(TRADES_PAYLOAD),
    });
  });
  await page.route('**/portfolio**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/positions**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route('**/market/status**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ spy: { is_risk_on: true, price: 530 }, ftse: { is_risk_on: true, price: 8300 }, fx_rate: 1.25 }) })
  );
  await page.route('**/signals**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route('**/portfolio/gate-metrics**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ closed_trades_count: 3, gate_threshold: 20, gate_met: false }) })
  );
  await page.route('**/positions/grace-period-alerts**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/analytics/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route('**/alerts/history**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/screener/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ results: [] }) })
  );
  await page.route('**/compliance/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route('**/red-flag-journal**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/earnings/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null }) })
  );

  await page.goto('/#/TradeReflection');
  // Wait for at least one trade card to render
  await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
}

// ---------------------------------------------------------------------------
// SC-RM-01 — Numeric R-multiple displayed for trade with net_r_multiple (AC-01)
// ---------------------------------------------------------------------------

test.describe('SC-RM-01 — Numeric R-multiple for trade with stop price', () => {
  test('SC-RM-01: NVDA card shows +1.50R', async ({ page }) => {
    await stubRoutesAndLoad(page);

    // Locate the NVDA card — find its R-Multiple cell
    const nvdaCard = page.locator('button').filter({ hasText: 'NVDA' }).first();
    await expect(nvdaCard).toBeVisible({ timeout: 5000 });
    await expect(nvdaCard.getByText('+1.50R')).toBeVisible({ timeout: 3000 });
  });
});

// ---------------------------------------------------------------------------
// SC-RM-02 — "N/A" shown for trade with null net_r_multiple / no stop (AC-02)
// ---------------------------------------------------------------------------

test.describe('SC-RM-02 — N/A for trade with no stop price recorded', () => {
  test('SC-RM-02: SHEL card shows N/A for R-Multiple', async ({ page }) => {
    await stubRoutesAndLoad(page);

    const shelCard = page.locator('button').filter({ hasText: 'SHEL' }).first();
    await expect(shelCard).toBeVisible({ timeout: 5000 });
    await expect(shelCard.getByText('N/A')).toBeVisible({ timeout: 3000 });
    // Must not show "—" (the old broken display)
    await expect(shelCard.getByText('—')).not.toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// SC-RM-03 — Colour coding: positive green, negative red, null neutral (AC-01, AC-03)
// ---------------------------------------------------------------------------

test.describe('SC-RM-03 — R-multiple colour coding', () => {
  test('SC-RM-03a: Positive R-multiple (+1.50R) rendered in green', async ({ page }) => {
    await stubRoutesAndLoad(page);

    const nvdaCard = page.locator('button').filter({ hasText: 'NVDA' }).first();
    const rCell = nvdaCard.getByText('+1.50R');
    await expect(rCell).toBeVisible({ timeout: 3000 });
    await expect(rCell).toHaveClass(/text-emerald-400/);
  });

  test('SC-RM-03b: Negative R-multiple (-0.75R) rendered in red', async ({ page }) => {
    await stubRoutesAndLoad(page);

    const aaplCard = page.locator('button').filter({ hasText: 'AAPL' }).first();
    const rCell = aaplCard.getByText('-0.75R');
    await expect(rCell).toBeVisible({ timeout: 3000 });
    await expect(rCell).toHaveClass(/text-rose-400/);
  });

  test('SC-RM-03c: Null R-multiple (N/A) rendered in neutral slate colour, not green or red', async ({ page }) => {
    await stubRoutesAndLoad(page);

    const shelCard = page.locator('button').filter({ hasText: 'SHEL' }).first();
    const rCell = shelCard.getByText('N/A');
    await expect(rCell).toBeVisible({ timeout: 3000 });
    await expect(rCell).toHaveClass(/text-slate-400/);
    await expect(rCell).not.toHaveClass(/text-emerald-400/);
    await expect(rCell).not.toHaveClass(/text-rose-400/);
  });
});
