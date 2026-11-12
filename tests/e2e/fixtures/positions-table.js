/**
 * Positions decision-first table helpers (ST-01, BLG-FE-260, EPIC-01, v9.17).
 *
 * From ST-01 the Positions Table view shows six data columns by default; Entry
 * price, Initial stop, Shares, P&L (GBP), Days held, State, Grace, Earnings,
 * Alerts, Last reviewed and the stop provenance line live in an expanded row
 * (positions.md v2.25 §Decision-First Table, §Expanded Row). Specs that assert
 * on those fields open the row first with these helpers.
 *
 * Not a spec file: holds no test() calls.
 */

'use strict';

/** Open the expanded row for one ticker; returns the detail row locator. */
async function expandPositionRow(page, ticker) {
  const chevron = page.getByRole('button', { name: `Show details for ${ticker}`, exact: true });
  await chevron.waitFor({ state: 'visible', timeout: 8000 });
  if ((await chevron.getAttribute('aria-expanded')) !== 'true') {
    await chevron.click();
  }
  const controls = await chevron.getAttribute('aria-controls');
  const detail = page.locator(`[id="${controls}"]`);
  await detail.waitFor({ state: 'visible', timeout: 5000 });
  return detail;
}

/**
 * Open every row's expanded details. Waits briefly for the rows; when the table
 * renders no rows (empty or error state) it returns without failing, so the
 * calling spec's own assertions decide the outcome.
 */
async function expandAllPositionRows(page) {
  const chevrons = page.locator('[data-testid="position-expand"][aria-expanded="false"]');
  const appeared = await page
    .locator('[data-testid="position-expand"]')
    .first()
    .waitFor({ state: 'visible', timeout: 5000 })
    .then(() => true, () => false);
  if (!appeared) return;
  let n = await chevrons.count();
  while (n > 0) {
    await chevrons.first().click();
    const next = await chevrons.count();
    if (next >= n) break;
    n = next;
  }
}

/** The detail row for a ticker (open it first). */
function positionDetail(page, ticker) {
  return page.locator(`[data-testid="position-detail"][data-detail-for="${ticker}"]`);
}

// ---------------------------------------------------------------------------
// Decision-first position fixtures and the Positions page route stub, shared by
// positions-decision-first.spec.js (ST-01) and positions-decision-cards.spec.js
// (ST-02) so both views are tested against the same urgency order.
// ---------------------------------------------------------------------------

const TODAY = new Date().toISOString();

function makePosition(overrides = {}) {
  return {
    id: 'pos-x',
    ticker: 'XXX',
    market: 'US',
    entry_price: 100,
    current_price: 120,
    current_price_native: 120,
    current_trailing_stop: 100,
    current_trailing_stop_native: 100,
    stop_price: 90,
    stop_price_native: 90,
    initial_stop: 90,
    shares: 10,
    pnl: 200,
    pnl_percent: 20,
    holding_days: 30,
    grace_period: false,
    grace_days_remaining: null,
    status: 'open',
    entry_date: TODAY,
    risk_off_exit: false,
    lifecycle_state: 'PROFITABLE',
    position_state: 'PROFITABLE',
    days_in_state: 10,
    tags: null,
    last_reviewed_at: TODAY,
    ...overrides,
  };
}

// Tier 4 (other): 16.7% from the stop.
const OTHER = makePosition({ id: 'pos-oth', ticker: 'OTHR' });
// Tier 1 (exit condition met): risk-off regime.
const RISK_OFF = makePosition({ id: 'pos-rof', ticker: 'RISK', risk_off_exit: true });
// Tier 2 (stop reached): post-grace, price at or below the trailing stop.
const BREACH = makePosition({
  id: 'pos-brc', ticker: 'BRCH', current_price: 98, current_price_native: 98, pnl: -20, pnl_percent: -2,
  lifecycle_state: 'LOSING', position_state: 'LOSING',
});
// Tier 3 (near stop): 4.0% from the stop. R = (104 − 100) ÷ (100 − 90) = 0.4R.
const NEAR = makePosition({
  id: 'pos-nea', ticker: 'NEAR', current_price: 104, current_price_native: 104, pnl: 40, pnl_percent: 4,
});
// In grace with the price below the stop: never tiers 2–3, so tier 4.
const GRACE_BREACH = makePosition({
  id: 'pos-gbr', ticker: 'GRCB', current_price: 95, current_price_native: 95, pnl: -50, pnl_percent: -5,
  grace_period: true, grace_days_remaining: 1, holding_days: 9,
  lifecycle_state: 'GRACE', position_state: 'GRACE',
});
// Tier 4, 10% from the stop: amber band.
const WARN = makePosition({
  id: 'pos-wrn', ticker: 'WARN', current_price: 111.11, current_price_native: 111.11, pnl: 111, pnl_percent: 11.1,
});

const ALL = [OTHER, GRACE_BREACH, WARN, NEAR, BREACH, RISK_OFF];

async function stubPositionsPage(page, positions) {
  const json = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance') || url.includes('/grace-period-alerts') || url.includes('/gap-risk')) {
      return route.continue();
    }
    return route.fulfill(json(positions));
  });
  await page.route('**/positions/*/gap-risk', (route) =>
    route.fulfill(json({ status: 'ok', data: { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false } }))
  );
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

/**
 * ST-03 (BLG-FE-262, v9.17): the drawdown, concentration, grace and staleness
 * warnings render inside the Positions warning strip, collapsed. Open one
 * entry ("drawdown" | "concentration" | "grace" | "staleness") before asserting
 * on its content; returns the expanded content locator.
 */
async function openPositionsWarning(page, kind) {
  const entry = page.getByTestId(`warning-entry-${kind}`);
  const button = entry.getByRole('button', { name: /^(Show|Hide) details$/ });
  await button.waitFor({ state: 'visible', timeout: 8000 });
  if ((await button.getAttribute('aria-expanded')) !== 'true') await button.click();
  const detail = page.locator(`#warning-detail-${kind}`);
  await detail.waitFor({ state: 'visible', timeout: 5000 });
  return detail;
}

const DECISION_FIXTURES = { OTHER, RISK_OFF, BREACH, NEAR, GRACE_BREACH, WARN, ALL };

module.exports = {
  expandPositionRow, expandAllPositionRows, positionDetail,
  makePosition, stubPositionsPage, DECISION_FIXTURES, openPositionsWarning,
};
