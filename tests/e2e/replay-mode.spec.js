/**
 * PO-05 Lightweight Replay Mode — Acceptance Tests — ST-01c (EPIC-01, v9.7, BLG-FEAT-74)
 *
 * Design source: docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md
 * Wire contract: docs/product/decisions/po05_replay_scope_confirmation.md (rev 3)
 * Spec: docs/specs/frontend/pages/replay_mode.md v0.2
 *
 * Coverage:
 *   SC-REP-01  "Replay" nav item present; navigates to /Replay
 *   SC-REP-02  Selector: two mutually exclusive tabs; each shows its own controls
 *   SC-REP-03  "Run Replay" disabled until a valid date range / trade selection; enabled once valid
 *   SC-REP-04  Running state: spinner shown, button disabled
 *   SC-REP-05  Retrospective banner always present, non-dismissible, exact §13 wording
 *   SC-REP-06  Success (>=1 trade): summary row, independence note, FX-basis caption, results table with badges
 *   SC-REP-07  Success (0 trades, no skips): empty-result text, no summary/table
 *   SC-REP-08  Success (0 trades, with skips): empty-result text AND the skipped notice both shown
 *   SC-REP-09  Skipped notice shown alongside a populated result too
 *   SC-REP-10  Failure state: fixed wording banner; selector remains usable
 *   SC-REP-11  No write-capable control anywhere in the output view (negative assertion, per replay_mode.md's own Testability note)
 *   SC-REP-12  Trade Set tab lists the user's own closed trades (ticker, exit date) as checkboxes
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/Replay').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const RETROSPECTIVE_NOTICE =
  'Retrospective result — shows what the current rules would have produced over this past period. Not a prediction of future performance.';

const CLOSED_TRADES = [
  { id: '11111111-1111-1111-1111-111111111111', ticker: 'NVDA', exit_date: '2026-05-12' },
  { id: '22222222-2222-2222-2222-222222222222', ticker: 'AAPL', exit_date: '2026-04-01' },
];

function tradesListResponse(trades = CLOSED_TRADES) {
  return { status: 'ok', data: { total_trades: trades.length, win_rate: 50, total_pnl: 0, trades } };
}

function replayRunResponse({ trades = [], skipped = [], retrospective_notice = RETROSPECTIVE_NOTICE, mode = 'date_range' } = {}) {
  const winCount = trades.filter((t) => t.simulated_pnl_native > 0).length;
  return {
    status: 'ok',
    data: {
      retrospective_notice,
      run: {
        mode, date_from: mode === 'date_range' ? '2026-03-01' : null, date_to: mode === 'date_range' ? '2026-06-30' : null,
        requested_trade_count: trades.length + skipped.length, replayed_trade_count: trades.length,
        skipped,
        rule_set: { stop_loss_mode: 'profit_lock', atr_mult: 2, initial_atr_mult: 5, profit_atr_mult: 2, min_hold_days: 10, risk_off_mode: 'single' },
        price_data_source: 'yfinance', price_data_fingerprint: trades.length ? 'sha256:deadbeef' : null,
      },
      summary: {
        trade_count: trades.length, win_count: winCount,
        win_rate_pct: trades.length ? Math.round((winCount / trades.length) * 10000) / 100 : null,
        total_simulated_pnl_gbp: trades.reduce((s, t) => s + (t.simulated_pnl_gbp ?? 0), 0),
        excluded_from_gbp_total: trades.filter((t) => t.fx_basis === 'unavailable').length,
      },
      trades,
    },
  };
}

const SAMPLE_TRADE = {
  trade_id: '11111111-1111-1111-1111-111111111111', ticker: 'NVDA', market: 'US', currency: 'USD',
  entry_date: '2026-03-04', entry_price: 121.5, shares: 10.0, initial_stop: 110.2,
  simulated_exit_date: '2026-05-12', simulated_exit_price: 133.1, simulated_exit_reason: 'Stop',
  holding_days: 69, simulated_pnl_native: 114.0, simulated_pnl_gbp: 89.63, fx_basis: 'entry_fx_rate',
};

const SAMPLE_TRADE_RISKOFF = {
  ...SAMPLE_TRADE, trade_id: '33333333-3333-3333-3333-333333333333', ticker: 'MSFT',
  simulated_exit_reason: 'Risk-Off', simulated_pnl_native: -20, simulated_pnl_gbp: -15.72,
};

const SAMPLE_TRADE_ACTUAL_EXIT = {
  ...SAMPLE_TRADE, trade_id: '44444444-4444-4444-4444-444444444444', ticker: 'TSLA',
  simulated_exit_reason: 'Actual Exit', simulated_pnl_native: 40, simulated_pnl_gbp: 31.45,
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTrades(page, trades = CLOSED_TRADES) {
  await page.route(`${API}/trades`, (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(tradesListResponse(trades)) }));
}

async function mockReplayRun(page, responseBody, status = 200) {
  await page.route(`${API}/replay/run`, (route) =>
    route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(responseBody) })
  );
}

async function gotoReplay(page) {
  await page.goto('/#/Replay');
  await page.waitForLoadState('domcontentloaded');
}

// ---------------------------------------------------------------------------
// SC-REP-01 — Navigation
// ---------------------------------------------------------------------------

test('SC-REP-01: "Replay" nav item is present and navigates to the Replay page', async ({ page }) => {
  await mockFallback(page);
  await page.goto('/#/DashboardHome');
  await page.waitForLoadState('domcontentloaded');

  // The sidebar groups items under collapsible sections (Trading, Analytics, Tools,
  // System -- Layout.js NAV_GROUPS). Only the group containing the *current* page
  // starts expanded; "Replay" lives in "Analytics", collapsed by default from
  // DashboardHome. Expand it before clicking the link (same pattern as
  // strategy-benchmark.spec.js).
  await page.getByRole('button', { name: 'Analytics' }).click();
  await page.getByRole('link', { name: 'Replay' }).click();

  await expect(page).toHaveURL(/#\/Replay/);
  await expect(page.getByRole('heading', { name: 'Replay Mode' })).toBeVisible({ timeout: 10000 });
});

// ---------------------------------------------------------------------------
// SC-REP-02 — Selector tabs
// ---------------------------------------------------------------------------

test('SC-REP-02: selector tabs are mutually exclusive and show their own controls', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await gotoReplay(page);

  await expect(page.getByTestId('replay-date-range-controls')).toBeVisible();
  await expect(page.getByTestId('replay-trade-set-controls')).toHaveCount(0);

  await page.getByTestId('replay-mode-tab-trade-set').click();
  await expect(page.getByTestId('replay-trade-set-controls')).toBeVisible();
  await expect(page.getByTestId('replay-date-range-controls')).toHaveCount(0);

  await page.getByTestId('replay-mode-tab-date-range').click();
  await expect(page.getByTestId('replay-date-range-controls')).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-REP-03 — Run Replay disabled/enabled
// ---------------------------------------------------------------------------

test('SC-REP-03: "Run Replay" is disabled until a valid date range is selected', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await gotoReplay(page);

  await expect(page.getByTestId('replay-run-button')).toBeDisabled();
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await expect(page.getByTestId('replay-run-button')).toBeDisabled();
  await page.getByTestId('replay-date-to').fill('2026-06-30');
  await expect(page.getByTestId('replay-run-button')).toBeEnabled();
});

test('SC-REP-03b: "Run Replay" is disabled until at least one trade is selected in Trade Set mode', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await gotoReplay(page);
  await page.getByTestId('replay-mode-tab-trade-set').click();

  await expect(page.getByTestId('replay-run-button')).toBeDisabled();
  await page.getByTestId(`replay-trade-checkbox-${CLOSED_TRADES[0].id}`).click();
  await expect(page.getByTestId('replay-run-button')).toBeEnabled();
});

// ---------------------------------------------------------------------------
// SC-REP-04 — Running state
// ---------------------------------------------------------------------------

test('SC-REP-04: running state shows a spinner and disables the button', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await page.route(`${API}/replay/run`, async (route) => {
    await new Promise((r) => setTimeout(r, 400));
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(replayRunResponse({ trades: [] })) });
  });
  await gotoReplay(page);
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await page.getByTestId('replay-date-to').fill('2026-06-30');

  await page.getByTestId('replay-run-button').click();
  await expect(page.getByTestId('replay-run-button')).toBeDisabled();
  await expect(page.getByTestId('replay-run-button').locator('.animate-spin')).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-REP-05 — Retrospective banner
// ---------------------------------------------------------------------------

test('SC-REP-05: retrospective banner is present with the exact approved wording and is non-dismissible', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockReplayRun(page, replayRunResponse({ trades: [] }));
  await gotoReplay(page);
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await page.getByTestId('replay-date-to').fill('2026-06-30');
  await page.getByTestId('replay-run-button').click();

  const banner = page.getByTestId('replay-retrospective-banner');
  await expect(banner).toBeVisible({ timeout: 10000 });
  await expect(banner).toContainText(RETROSPECTIVE_NOTICE);
  await expect(banner.getByTestId('standing-alert-dismiss')).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-REP-06 — Populated success state
// ---------------------------------------------------------------------------

test('SC-REP-06: populated success shows summary, independence note, FX caption, and a badged results table', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockReplayRun(page, replayRunResponse({ trades: [SAMPLE_TRADE, SAMPLE_TRADE_RISKOFF, SAMPLE_TRADE_ACTUAL_EXIT] }));
  await gotoReplay(page);
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await page.getByTestId('replay-date-to').fill('2026-06-30');
  await page.getByTestId('replay-run-button').click();

  await expect(page.getByTestId('replay-retrospective-banner')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('replay-summary-trade-count')).toHaveText('3');
  await expect(page.getByTestId('replay-independence-note')).toContainText('replayed independently');
  await expect(page.getByTestId('replay-fx-basis-caption')).toContainText("entry exchange rate");

  const table = page.getByTestId('replay-results-table');
  await expect(table).toBeVisible();
  const stopRow = page.getByTestId(`replay-result-row-${SAMPLE_TRADE.trade_id}`);
  await expect(stopRow).toContainText('NVDA');
  await expect(stopRow).toContainText('+£89.63');
  const stopBadge = stopRow.locator('span', { hasText: 'Stop' });
  await expect(stopBadge).toHaveClass(/bg-red-600/);

  const riskOffRow = page.getByTestId(`replay-result-row-${SAMPLE_TRADE_RISKOFF.trade_id}`);
  const riskOffBadge = riskOffRow.locator('span', { hasText: 'Risk-Off' });
  await expect(riskOffBadge).toHaveClass(/bg-amber-600/);
  await expect(riskOffRow).toContainText('−£15.72');

  // "Actual Exit" is deliberately not in the badge map -- rendered as plain text.
  const actualExitRow = page.getByTestId(`replay-result-row-${SAMPLE_TRADE_ACTUAL_EXIT.trade_id}`);
  await expect(actualExitRow).toContainText('Actual Exit');
  await expect(actualExitRow.locator('span.bg-red-600, span.bg-amber-600')).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-REP-07 / 08 — Zero-trade success states
// ---------------------------------------------------------------------------

test('SC-REP-07: zero trades with no skips shows only the empty-result text, no summary or table', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockReplayRun(page, replayRunResponse({ trades: [] }));
  await gotoReplay(page);
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await page.getByTestId('replay-date-to').fill('2026-06-30');
  await page.getByTestId('replay-run-button').click();

  await expect(page.getByTestId('replay-retrospective-banner')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('replay-empty-result')).toHaveText('No closed trades in the selected range/set.');
  await expect(page.getByTestId('replay-results-table')).toHaveCount(0);
  await expect(page.getByTestId('replay-skipped-notice')).toHaveCount(0);
});

test('SC-REP-08: zero trades WITH skips shows the empty-result text AND the skipped notice', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockReplayRun(page, replayRunResponse({
    trades: [],
    skipped: [{ trade_id: 'x', reason: 'price_data_unavailable' }, { trade_id: 'y', reason: 'price_data_unavailable' }],
  }));
  await gotoReplay(page);
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await page.getByTestId('replay-date-to').fill('2026-06-30');
  await page.getByTestId('replay-run-button').click();

  await expect(page.getByTestId('replay-empty-result')).toBeVisible({ timeout: 10000 });
  const notice = page.getByTestId('replay-skipped-notice');
  await expect(notice).toBeVisible();
  await expect(notice).toContainText('2 trades');
  await expect(notice).toContainText('price data unavailable');
});

test('SC-REP-09: the skipped notice also shows alongside a populated result', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockReplayRun(page, replayRunResponse({
    trades: [SAMPLE_TRADE],
    skipped: [{ trade_id: 'z', reason: 'insufficient_history' }],
  }));
  await gotoReplay(page);
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await page.getByTestId('replay-date-to').fill('2026-06-30');
  await page.getByTestId('replay-run-button').click();

  await expect(page.getByTestId('replay-results-table')).toBeVisible({ timeout: 10000 });
  const notice = page.getByTestId('replay-skipped-notice');
  await expect(notice).toBeVisible();
  await expect(notice).toContainText('1 trade');
  await expect(notice).toContainText('insufficient price history');
});

// ---------------------------------------------------------------------------
// SC-REP-10 — Failure state
// ---------------------------------------------------------------------------

test('SC-REP-10: failure shows the fixed wording banner and the selector remains usable', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockReplayRun(page, { status: 'error', message: 'boom', code: 'replay_failed' }, 500);
  await gotoReplay(page);
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await page.getByTestId('replay-date-to').fill('2026-06-30');
  await page.getByTestId('replay-run-button').click();

  const failureBanner = page.getByTestId('replay-failure-banner');
  await expect(failureBanner).toBeVisible({ timeout: 10000 });
  await expect(failureBanner).toHaveText("Couldn't run the replay. Try again.");

  // Selector remains usable: switch tabs, still no crash / still interactive.
  await page.getByTestId('replay-mode-tab-trade-set').click();
  await expect(page.getByTestId('replay-trade-set-controls')).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-REP-11 — No write-capable control (negative assertion)
// ---------------------------------------------------------------------------

test('SC-REP-11: the output view contains no write-capable control (button/link)', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await mockReplayRun(page, replayRunResponse({ trades: [SAMPLE_TRADE, SAMPLE_TRADE_RISKOFF] }));
  await gotoReplay(page);
  await page.getByTestId('replay-date-from').fill('2026-03-01');
  await page.getByTestId('replay-date-to').fill('2026-06-30');
  await page.getByTestId('replay-run-button').click();

  const outputView = page.getByTestId('replay-output-view');
  await expect(outputView).toBeVisible({ timeout: 10000 });
  await expect(outputView.locator('button')).toHaveCount(0);
  await expect(outputView.locator('a')).toHaveCount(0);
  await expect(outputView.locator('input')).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-REP-12 — Trade Set list
// ---------------------------------------------------------------------------

test('SC-REP-12: Trade Set tab lists the user\'s own closed trades as checkboxes (ticker, exit date)', async ({ page }) => {
  await mockFallback(page);
  await mockTrades(page);
  await gotoReplay(page);
  await page.getByTestId('replay-mode-tab-trade-set').click();

  for (const t of CLOSED_TRADES) {
    const checkbox = page.getByTestId(`replay-trade-checkbox-${t.id}`);
    await expect(checkbox).toBeVisible({ timeout: 10000 });
    await expect(checkbox).toHaveAttribute('aria-checked', 'false');
  }
  await expect(page.getByText('NVDA')).toBeVisible();
  await expect(page.getByText(/exited 2026-05-12/)).toBeVisible();

  await page.getByTestId(`replay-trade-checkbox-${CLOSED_TRADES[0].id}`).click();
  await expect(page.getByTestId(`replay-trade-checkbox-${CLOSED_TRADES[0].id}`)).toHaveAttribute('aria-checked', 'true');
});
