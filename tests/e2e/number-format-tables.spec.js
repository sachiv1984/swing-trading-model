/**
 * Identical number/currency conventions across Positions, Trade History and Trade Plans
 * (ST-06, EPIC-01, v9.6, BLG-FE-182)
 *
 * Design source: docs/design/2026-09-21__release-v9.6/number-format-convention/decision_record.md §2, §5
 * Spec: docs/specs/frontend/design_system.md v1.21 §Number and Currency Formatting
 *
 * Fixture per table: a gain, a loss, a zero, and a value >= 1,000 (grouping).
 *
 *   SC-NFT-01  Positions table: money is grouped 2 dp, P&L is signed with a typographic minus, % is signed 1 dp
 *   SC-NFT-02  Positions grid cards use the same conventions as the table
 *   SC-NFT-03  Trade History table: P&L, P&L %, slippage, fee drag and Net R use the same conventions
 *   SC-NFT-04  Trade History summary stats (Total P&L, Avg Winner/Loser) use the same conventions
 *   SC-NFT-05  Trade Plans: the user-entered R target is as entered, trimmed and unsigned
 *   SC-NFT-06  Across all three tables: no ASCII hyphen-minus in any signed figure, U+2212 is used; missing is an em dash
 *
 * The unit-level output table is covered by tests/e2e/number-format-helper.spec.js.
 * Infrastructure: Playwright page.route() network interception. HashRouter — navigate via '/#/…'.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const M = '−';
const EM = '—';
const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });
const daysAgo = (n) => new Date(Date.now() - n * 86400000).toISOString();

// ---------------------------------------------------------------------------
// Positions
// ---------------------------------------------------------------------------

function pos(o) {
  return {
    id: `p-${o.ticker}`, market: 'US', shares: 10, status: 'open', entry_date: daysAgo(20), holding_days: 20,
    grace_days_remaining: null, risk_off_exit: false, lifecycle_state: 'PROFITABLE', position_state: 'PROFITABLE',
    days_in_state: 5, tags: null, last_reviewed_at: null, current_trailing_stop: 0,
    stop_price: 90, stop_price_native: 90, ...o,
  };
}
const POSITIONS = [
  pos({ ticker: 'GAIN', market: 'US', entry_price: 1234.5, current_price: 1300, current_price_native: 1300, initial_stop: 1100,
        current_trailing_stop: 1000, current_trailing_stop_native: 1200.5, pnl: 1250, pnl_percent: 4.2 }),
  pos({ ticker: 'LOSS', market: 'UK', entry_price: 100, current_price: 92, current_price_native: 92, initial_stop: 90,
        pnl: -80, pnl_percent: -1.8 }),
  pos({ ticker: 'ZERO', market: 'US', entry_price: 50, current_price: 50, current_price_native: 50, initial_stop: 45,
        pnl: 0, pnl_percent: 0 }),
];

async function stubPositions(page) {
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance') || url.includes('/grace-period-alerts') || url.includes('/gap-risk')) return route.fallback();
    return route.fulfill(json(POSITIONS));
  });
  await page.route('**/positions/*/gap-risk', (route) => route.fulfill(json({ status: 'ok', data: { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false } })));
  await page.route('**/positions/compliance*', (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route('**/positions/grace-period-alerts', (route) => route.fulfill(json({ data: [] })));
  await page.route('**/portfolio/drawdown-status', (route) => route.fulfill(json({ status: 'ok', data: { threshold_breached: false } })));
  await page.route('**/portfolio/concentration-status', (route) => route.fulfill(json({ status: 'ok', data: { any_breach: false } })));
  await page.route('**/portfolio*', (route) => route.fulfill(json({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } })));
  await page.route('**/analytics/**', (route) => route.fulfill(json({ status: 'ok', data: { last_sync_at: null } })));
  await page.route('**/alerts/history**', (route) => route.fulfill(json({ data: { evaluations: [] } })));
  await page.route('**/watchlist**', (route) => route.fulfill(json({ items: [] })));
  await page.route('**/earnings/**', (route) => route.fulfill(json({ next_earnings_date: null, days_until_earnings: null })));
}

async function gotoPositionsTable(page) {
  await stubPositions(page);
  await page.goto('/#/Positions');
  await page.waitForSelector('text=GAIN', { timeout: 10000 });
  await page.locator('[aria-label="Table view"]').click();
  await page.waitForSelector('table', { timeout: 5000 });
}

test('SC-NFT-01: Positions table — grouped 2 dp money, signed P&L with typographic minus, signed 1 dp %', async ({ page }) => {
  await gotoPositionsTable(page);
  const row = (t) => page.locator('tr', { hasText: t }).first();

  const gain = await row('GAIN').innerText();
  expect(gain).toContain('$1,234.50');          // entry: grouped, native currency
  expect(gain).toContain('$1,300.00');          // current
  expect(gain).toContain('Init: $1,100.00');    // initial stop
  expect(gain).toContain('$1,200.50');          // trailing stop (native)
  expect(gain).toContain('+£1,250.00');         // P&L: explicit sign, GBP, grouped
  expect(gain).toContain('+4.2%');              // P&L %: 1 dp, signed

  const loss = await row('LOSS').innerText();
  expect(loss).toContain('£100.00');            // UK position -> £
  expect(loss).toContain(`${M}£80.00`);         // typographic minus BEFORE the symbol
  expect(loss).toContain(`${M}1.8%`);

  const zero = await row('ZERO').innerText();
  expect(zero).toMatch(/£0\.00/);
  expect(zero).not.toMatch(/[+−]£0\.00/);  // zero is unsigned
  expect(zero).toContain('0.0%');
  expect(zero).not.toMatch(/[+−]0\.0%/);
});

test('SC-NFT-02: Positions grid cards follow the same conventions as the table', async ({ page }) => {
  await stubPositions(page);
  await page.goto('/#/Positions'); // grid is the default view
  await page.waitForSelector('text=GAIN', { timeout: 10000 });
  const card = (t) => page.locator('div', { hasText: t }).filter({ hasText: 'Entry' }).last();

  const gain = await card('GAIN').innerText();
  expect(gain).toContain('$1,234.50');
  expect(gain).toContain('$1,300.00');
  expect(gain).toContain('Init: $1,100.00');
  expect(gain).toContain('+4.2%');               // 1 dp (was 2 dp on the card)
  const loss = await card('LOSS').innerText();
  expect(loss).toContain(`${M}1.8%`);
  expect(loss).toContain('£100.00');
});

// ---------------------------------------------------------------------------
// Trade History
// ---------------------------------------------------------------------------

function trade(o) {
  return {
    id: `t-${o.ticker}`, market: 'US', entry_price: 100, exit_price: 110, shares: 10, exit_reason: 'MANUAL',
    entry_date: '2026-08-01', exit_date: '2026-08-15', holding_days: 14, ...o,
  };
}
const TRADES = [
  trade({ ticker: 'TGAIN', pnl: 1250.5, pnl_pct: 4.2, net_r_multiple: 1.5, slippage_pct: 0.35, fee_drag_pct: 0.2 }),
  trade({ ticker: 'TLOSS', pnl: -80, pnl_pct: -1.8, net_r_multiple: -0.5, slippage_pct: -0.35, fee_drag_pct: 0.1 }),
  trade({ ticker: 'TZERO', pnl: 0, pnl_pct: 0, net_r_multiple: 0, slippage_pct: 0, fee_drag_pct: 0 }),
];

async function gotoTradeHistory(page) {
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(/\/trades$/, (route) => route.fulfill(json({
    status: 'ok', data: { trades: TRADES, avg_slippage_pct: -0.35, avg_fee_drag_pct: 0.15 },
  })));
  await page.route(/\/analytics\/metrics/, (route) => route.fulfill(json({ status: 'ok', data: { trades_for_charts: [] } })));
  await page.goto('/#/TradeHistory');
  await page.waitForSelector('text=TGAIN', { timeout: 10000 });
}

test('SC-NFT-03: Trade History table — P&L, P&L %, slippage, fee drag and Net R use the shared conventions', async ({ page }) => {
  await gotoTradeHistory(page);
  const row = (t) => page.locator('tr', { hasText: t }).first();

  const gain = await row('TGAIN').innerText();
  expect(gain).toContain('+£1,250.50');   // signed, grouped
  expect(gain).toContain('+4.2%');        // 1 dp (was 2 dp)
  expect(gain).toContain('+0.35%');       // slippage: small-magnitude cost metric, 2 dp
  expect(gain).toContain('+0.20%');       // fee drag: 2 dp
  expect(gain).toContain('+1.50R');       // Net R: signed 2 dp

  const loss = await row('TLOSS').innerText();
  expect(loss).toContain(`${M}£80.00`);   // was "£80.00" with the sign carried by colour/icon alone
  expect(loss).toContain(`${M}1.8%`);
  expect(loss).toContain(`${M}0.35%`);    // was ASCII "-0.35%"
  expect(loss).toContain(`${M}0.50R`);    // was ASCII "-0.50R"

  const zero = await row('TZERO').innerText();
  expect(zero).not.toMatch(/[+−]£0\.00/);
  expect(zero).toContain('0.00R');
  expect(zero).not.toMatch(/[+−]0\.00R/);
});

test('SC-NFT-04: Trade History summary stats use the shared conventions', async ({ page }) => {
  await gotoTradeHistory(page);
  // Total P&L = 1250.5 - 80 + 0, Avg Winner = 1250.5 (1 winner incl. zero excluded), Avg Loser = 80
  await expect(page.getByText('+£1,170.50', { exact: true })).toBeVisible({ timeout: 10000 });
  await expect(page.getByText(`${M}£80.00`, { exact: true }).first()).toBeVisible();      // Avg Loser
  await expect(page.getByText('+£1,250.50', { exact: true }).first()).toBeVisible();      // Avg Winner
  await expect(page.getByText(`${M}0.35%`, { exact: true }).first()).toBeVisible();       // Avg Entry Dev.
  await expect(page.getByText('+0.15%', { exact: true })).toBeVisible();                  // Avg Fee Drag
});

// ---------------------------------------------------------------------------
// Trade Plans
// ---------------------------------------------------------------------------

test('SC-NFT-05: Trade Plans — the user-entered R target is as entered, trimmed and unsigned', async ({ page }) => {
  const plan = (id, ticker, r) => ({ id, ticker, market: 'US', status: 'draft', position_id: null, r_target: r,
    setup_thesis: 't', created_at: daysAgo(1), updated_at: daysAgo(1) });
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/trade-plans/tags`, (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/trade-plans`, (route) => route.fulfill(json({ status: 'ok', data: [
    plan('a', 'RHALF', 2.5), plan('b', 'RWHOLE', 3), plan('c', 'RQUARTER', 2.25), plan('d', 'RNONE', null),
  ] })));
  await page.goto('/#/TradePlans');
  await page.waitForSelector('text=RHALF', { timeout: 10000 });
  const cell = async (t) => page.locator('tr', { hasText: t }).first().innerText();
  expect(await cell('RHALF')).toContain('2.5R');
  expect(await cell('RWHOLE')).toMatch(/\b3R\b/);
  expect(await cell('RWHOLE')).not.toContain('3.0R');
  expect(await cell('RQUARTER')).toContain('2.25R');
  expect(await cell('RNONE')).toContain(EM);
  expect(await cell('RHALF')).not.toContain('+2.5R');
});

// ---------------------------------------------------------------------------
// Cross-table: identical negative convention
// ---------------------------------------------------------------------------

test('SC-NFT-06: no ASCII hyphen-minus in any signed figure across Positions and Trade History; U+2212 throughout', async ({ page }) => {
  await gotoPositionsTable(page);
  const posText = await page.locator('table').first().innerText();
  const tradeCtx = await page.context().newPage();
  await tradeCtx.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await tradeCtx.route(/\/trades$/, (route) => route.fulfill(json({ status: 'ok', data: { trades: TRADES, avg_slippage_pct: -0.35, avg_fee_drag_pct: 0.15 } })));
  await tradeCtx.route(/\/analytics\/metrics/, (route) => route.fulfill(json({ status: 'ok', data: { trades_for_charts: [] } })));
  await tradeCtx.goto('/#/TradeHistory');
  await tradeCtx.waitForSelector('text=TGAIN', { timeout: 10000 });
  const histText = await tradeCtx.locator('table').first().innerText();

  const asciiNegative = /-[£$\d]/; // a hyphen-minus glued to a figure
  expect(posText).not.toMatch(asciiNegative);
  expect(histText).not.toMatch(asciiNegative);
  expect(posText).toContain(M);
  expect(histText).toContain(M);
  await tradeCtx.close();
});
