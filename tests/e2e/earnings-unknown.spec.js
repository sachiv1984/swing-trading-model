/**
 * Earnings Unknown — ST-33 (BLG-FE-294, EPIC-06, v9.18)
 *
 * GET /earnings/{ticker} and GET /positions/{id}/gap-risk gain data_status:
 * "ok" | "unavailable" (earnings_endpoints.md v0.4, position_endpoints.md
 * v2.24.0). A failed lookup shows a muted "Unknown" (Screener, Watchlist,
 * Positions expanded row) or "Earnings: unknown" (Positions Alerts cell and Grid
 * card), is held 60 seconds rather than cached for the session, and never uses
 * the GAP RISK badge's colour or wording. (Product Owner rulings 2026-11-24:
 * the 60-second hold, and "Unknown" in the expanded row, which already has the
 * "Earnings" label.) An ok answer with no date shows
 * nothing ("—", as before). Screener UK rows make no earnings lookup.
 *
 * Specs: docs/specs/frontend/pages/positions.md §Earnings Unknown (v2.30),
 *        docs/specs/frontend/pages/screener_results.md §4 Earnings (v1.12),
 *        docs/specs/frontend/pages/watchlist.md §Earnings Cell (v0.11),
 *        docs/design/2026-11-18__release-v9.18/position-data-states/decision_record.md §4.
 *
 * Scenarios:
 *   SC-EUNK-01  Screener: unavailable shows muted "Unknown" with the tooltip text
 *   SC-EUNK-02  Screener: ok with a null date shows "—", not "Unknown"
 *   SC-EUNK-03  Screener: a UK row makes no earnings lookup and shows "—"
 *   SC-EUNK-04  Watchlist: unavailable shows "Unknown"; ok with a null date shows "—"
 *   SC-EUNK-05  Positions expanded row: unavailable shows "Unknown"; ok null shows "—"
 *   SC-EUNK-06  Positions Alerts cell (table): gap-risk unavailable shows muted
 *               "Earnings: unknown" and no GAP RISK badge; ok shows nothing
 *   SC-EUNK-07  Positions Grid view card: gap-risk unavailable shows "Earnings: unknown"
 *   SC-EUNK-08  An unavailable answer is held 60 s, then retried on the next mount; an ok answer is cached
 *   SC-EUNK-09  A 500 from GET /earnings shows "Unknown" (a failed request is a failed lookup)
 *   SC-EUNK-09b A 500 from GET /positions/{id}/gap-risk shows "Earnings: unknown" in the Alerts cell
 *   SC-EUNK-09c The same 500 for a UK position shows nothing and is held 60 s (no earnings lookup is made; BLG-FE-335)
 *
 * Every "unknown" element is also scanned with axe color-contrast: any violation
 * fails, and any incomplete result fails unless axe gives a background gradient as
 * the reason (the Watchlist table and Grid view card backgrounds; BLG-QA-281).
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const { expandAllPositionRows } = require('./fixtures/positions-table');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const TOOLTIP = 'The earnings date could not be fetched. It will be retried.';

// Shaped as backend/services/earnings_service.py writes them (_empty and the dated answer).
const UNAVAILABLE = {
  ticker: 'AAPL', next_earnings_date: null, days_until_earnings: null,
  fiscal_quarter: null, data_source: 'yahoo_finance', data_status: 'unavailable',
};
const OK_NO_DATE = { ...UNAVAILABLE, data_status: 'ok' };

// Shaped as backend/services/gap_risk_service.py writes them.
const GAP_UNAVAILABLE = {
  flagged: false, reasons: [], avg_gap_pct: null, event_count: 0,
  insufficient_history: false, data_status: 'unavailable',
};
const GAP_OK = { ...GAP_UNAVAILABLE, data_status: 'ok' };

function json(route, body, status = 200) {
  return route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(body) });
}

async function stubCommon(page) {
  await page.route(`${API}/alerts/history**`, (r) => json(r, { data: { evaluations: [] } }));
  await page.route(`${API}/news/**`, (r) => json(r, { headlines: [] }));
}

// earnings: an answer, or a function (ticker) => answer. Returns the list of
// /earnings request paths, in order.
async function stubEarnings(page, earnings) {
  const calls = [];
  await page.route(`${API}/earnings/**`, (route) => {
    const url = new URL(route.request().url());
    calls.push(url.pathname + url.search);
    const ticker = url.pathname.split('/').pop();
    return json(route, typeof earnings === 'function' ? earnings(ticker) : earnings);
  });
  return calls;
}

function screenerRow(overrides = {}) {
  return {
    ticker: 'AAPL', market: 'US', price: 175.5, currency: 'USD', atr: 3.2, atr_pct: 1.83,
    regime_status: 'risk_on', signal_score: 0.82, sector: 'Technology',
    proximity_to_entry_zone: 'near_entry', news_headline_count: 0, ...overrides,
  };
}

async function stubScreener(page, rows) {
  await page.route(`${API}/screener/results**`, (r) => json(r, {
    results: rows, run_id: 'r1', run_timestamp: new Date().toISOString(), total: rows.length, limit: 200, offset: 0,
  }));
  await page.route(`${API}/screener/run`, (r) => json(r, { ok: true, data: { run_id: 'r2', status: 'accepted' } }, 202));
  await page.route(`${API}/screener/regime-distribution**`, (r) => json(r, {
    ok: true, data: { window: '30d', run_count: 1, total_observations: 2, risk_on_count: 2, risk_off_count: 0, risk_on_pct: 100.0, risk_off_pct: 0.0 },
  }));
}

async function stubWatchlist(page, entries) {
  await page.route(`${API}/watchlist`, (route) => (route.request().method() === 'GET'
    ? json(route, { data: entries, items: entries })
    : json(route, { id: 2 }, 201)));
  await page.route(`${API}/portfolio/**`, (r) => json(r, { ok: true, data: {} }));
}

function watchlistEntry(overrides = {}) {
  return {
    id: 1, ticker: 'MSFT', market: 'US', target_entry_price: 380.0, initial_stop_price: 360.0,
    current_stop_price: 362.0, notes: '', added_date: '2026-04-01', ...overrides,
  };
}

function position(overrides = {}) {
  return {
    id: 'pos-eunk-01', ticker: 'NVDA', market: 'US', entry_price: 800.0, current_price: 850.0,
    current_price_native: 850.0, stop_price: 760.0, stop_price_native: 760.0, shares: 10,
    pnl: 500.0, pnl_percent: 6.25, holding_days: 5, grace_days_remaining: null, status: 'open',
    entry_date: '2026-04-01', initial_stop: 760.0, current_trailing_stop: 0, risk_off_exit: false,
    tags: null, ...overrides,
  };
}

async function stubPositions(page, positions, gapRisk) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/positions/compliance')) return json(route, { status: 'ok', data: [] });
    return json(route, positions);
  });
  // gapRisk: an answer, or a route handler for tests that fail the request.
  await page.route('**/positions/*/gap-risk', (r) => (typeof gapRisk === 'function'
    ? gapRisk(r) : json(r, { status: 'ok', data: gapRisk })));
  await page.route('**/portfolio*', (r) => json(r, { status: 'ok', data: { cash: 10000, initial_cash: 50000 } }));
  await page.route('**/analytics/**', (r) => json(r, { status: 'ok', data: { last_sync_at: null } }));
  await page.route('**/compliance/**', (r) => json(r, { status: 'ok', data: [] }));
  await page.route(`${API}/watchlist**`, (r) => json(r, { items: [], data: [] }));
}

async function gotoPositionsTable(page, ticker = 'NVDA') {
  await page.goto('/#/Positions');
  await page.waitForSelector(`text=${ticker}`, { timeout: 8000 });
  await page.locator('[aria-label="Table view"]').click();
  await page.waitForSelector('table', { timeout: 5000 });
  await expandAllPositionRows(page);
}

async function expectMutedUnknown(locator, text) {
  await expect(locator).toBeVisible({ timeout: 8000 });
  await expect(locator).toHaveText(new RegExp(`^${text}`));
  await expect(locator).toHaveAttribute('title', TOOLTIP);
  await expect(locator).toHaveClass(/text-app-muted/);
  await expect(locator).not.toHaveClass(/amber|warning/);
  const descId = await locator.getAttribute('aria-describedby');
  await expect(locator.page().locator(`[id="${descId}"]`)).toHaveText(TOOLTIP);
  // Contrast of the muted text where it renders (each conditional state gets a scan).
  const testId = await locator.getAttribute('data-testid');
  const results = await new AxeBuilder({ page: locator.page() })
    .include(`[data-testid="${testId}"]`).withRules(['color-contrast']).analyze();
  expect(results.violations).toEqual([]);
  // axe cannot decide contrast over a gradient background (the Watchlist table and the
  // Grid view card sit on one; pre-existing, triaged under BLG-QA-281). Any other
  // incomplete reason fails, as does every violation.
  const undecided = results.incomplete.flatMap((r) => r.nodes)
    .map((n) => n.any.map((a) => a.message).join('|'))
    .filter((m) => !/background gradient/.test(m));
  expect(undecided).toEqual([]);
}

// ---------------------------------------------------------------------------
// Screener
// ---------------------------------------------------------------------------

test.describe('Screener — Earnings column', () => {
  test.beforeEach(async ({ page }) => {
    await stubCommon(page);
    await stubWatchlist(page, []);
  });

  test('SC-EUNK-01: an unavailable lookup shows a muted "Unknown" with the tooltip', async ({ page }) => {
    await stubScreener(page, [screenerRow()]);
    await stubEarnings(page, UNAVAILABLE);
    await page.goto('/#/Screener');
    const row = page.getByRole('row', { name: /AAPL/ });
    await expectMutedUnknown(row.getByTestId('earnings-unknown'), 'Unknown');
  });

  test('SC-EUNK-02: an ok answer with no date shows "—", not "Unknown"', async ({ page }) => {
    await stubScreener(page, [screenerRow()]);
    const calls = await stubEarnings(page, OK_NO_DATE);
    await page.goto('/#/Screener');
    const row = page.getByRole('row', { name: /AAPL/ });
    await expect(row).toBeVisible({ timeout: 8000 });
    await expect.poll(() => calls.length).toBeGreaterThan(0);
    await expect(row.getByTestId('earnings-unknown')).toHaveCount(0);
    await expect(row.getByText('…')).toHaveCount(0);
    await expect(row).toContainText('—');
  });

  test('SC-EUNK-03: a UK row makes no earnings lookup and shows "—"', async ({ page }) => {
    await stubScreener(page, [screenerRow(), screenerRow({ ticker: 'BARC', market: 'UK', currency: 'GBP' })]);
    const calls = await stubEarnings(page, UNAVAILABLE);
    await page.goto('/#/Screener');
    const ukRow = page.getByRole('row', { name: /BARC/ });
    await expect(ukRow).toBeVisible({ timeout: 8000 });
    // The US row's lookup proves the column rendered and fetched.
    await expect(page.getByRole('row', { name: /AAPL/ }).getByTestId('earnings-unknown')).toBeVisible({ timeout: 8000 });
    await expect(ukRow.getByTestId('earnings-unknown')).toHaveCount(0);
    await expect(ukRow.getByText('…')).toHaveCount(0);
    expect(calls.filter((c) => c.includes('/earnings/BARC'))).toEqual([]);
    expect(calls.filter((c) => c.includes('/earnings/AAPL')).length).toBeGreaterThan(0);
  });
});

// ---------------------------------------------------------------------------
// Watchlist
// ---------------------------------------------------------------------------

test.describe('Watchlist — Earnings cell', () => {
  test.beforeEach(async ({ page }) => {
    await stubCommon(page);
  });

  test('SC-EUNK-04: unavailable shows "Unknown"; ok with a null date shows "—"', async ({ page }) => {
    await stubWatchlist(page, [watchlistEntry(), watchlistEntry({ id: 2, ticker: 'KO' })]);
    await stubEarnings(page, (ticker) => (ticker === 'MSFT' ? UNAVAILABLE : OK_NO_DATE));
    await page.goto('/#/Watchlist');
    const msft = page.getByRole('row', { name: /MSFT/ });
    const ko = page.getByRole('row', { name: /\bKO\b/ });
    await expectMutedUnknown(msft.getByTestId('earnings-unknown'), 'Unknown');
    await expect(ko).toBeVisible();
    await expect(ko.getByTestId('earnings-unknown')).toHaveCount(0);
    await expect(ko).toContainText('—');
  });
});

// ---------------------------------------------------------------------------
// Positions
// ---------------------------------------------------------------------------

test.describe('Positions — Earnings Unknown', () => {
  test.beforeEach(async ({ page }) => {
    await stubCommon(page);
  });

  test('SC-EUNK-05: the expanded row shows "Unknown" for unavailable and "—" for ok with no date', async ({ page }) => {
    await stubPositions(page, [position(), position({ id: 'pos-eunk-02', ticker: 'KO' })], GAP_OK);
    await stubEarnings(page, (ticker) => (ticker === 'NVDA' ? UNAVAILABLE : OK_NO_DATE));
    await gotoPositionsTable(page);
    const details = page.getByTestId('position-detail');
    await expect(details).toHaveCount(2);
    const nvda = details.filter({ has: page.getByTestId('earnings-unknown') });
    await expect(nvda).toHaveCount(1);
    await expectMutedUnknown(nvda.getByTestId('earnings-unknown'), 'Unknown');
    await expect(nvda.getByTestId('earnings-unknown')).not.toContainText('Earnings');
    const ko = details.filter({ hasNot: page.getByTestId('earnings-unknown') });
    await expect(ko.locator('dd').filter({ hasText: /^—$/ }).first()).toBeVisible();
  });

  test('SC-EUNK-06: a failed gap-risk earnings input shows muted "Earnings: unknown" and no GAP RISK badge', async ({ page }) => {
    await stubPositions(page, [position()], GAP_UNAVAILABLE);
    await stubEarnings(page, OK_NO_DATE);
    await gotoPositionsTable(page);
    await expectMutedUnknown(page.getByTestId('gap-risk-earnings-unknown'), 'Earnings: unknown');
    await expect(page.getByTestId('gap-risk-badge')).toHaveCount(0);
    await expect(page.getByTestId('gap-risk-earnings-unknown')).not.toContainText(/gap risk/i);
  });

  test('SC-EUNK-06b: an ok gap-risk answer with no flag shows nothing in the Alerts cell', async ({ page }) => {
    await stubPositions(page, [position()], GAP_OK);
    const calls = await stubEarnings(page, OK_NO_DATE);
    await gotoPositionsTable(page);
    await expect.poll(() => calls.length).toBeGreaterThan(0);
    await expect(page.getByTestId('gap-risk-skeleton')).toHaveCount(0);
    await expect(page.getByTestId('gap-risk-earnings-unknown')).toHaveCount(0);
    await expect(page.getByTestId('gap-risk-badge')).toHaveCount(0);
  });

  test('SC-EUNK-07: the Grid view card shows "Earnings: unknown" for a failed gap-risk earnings input', async ({ page }) => {
    await stubPositions(page, [position()], GAP_UNAVAILABLE);
    await stubEarnings(page, OK_NO_DATE);
    await page.goto('/#/Positions');
    await page.waitForSelector('text=NVDA', { timeout: 8000 });
    const row = page.getByTestId('grid-alerts-row');
    await expectMutedUnknown(row.getByTestId('gap-risk-earnings-unknown'), 'Earnings: unknown');
    await expect(row.getByTestId('gap-risk-badge')).toHaveCount(0);
  });
});

test.describe('Request failure', () => {
  test.beforeEach(async ({ page }) => {
    await stubCommon(page);
  });

  test('SC-EUNK-09: a 500 from GET /earnings shows "Unknown", not "—"', async ({ page }) => {
    await stubScreener(page, [screenerRow()]);
    await stubWatchlist(page, []);
    await page.route(`${API}/earnings/**`, (r) => json(r, { status: 'error', message: 'boom' }, 500));
    await page.goto('/#/Screener');
    await expectMutedUnknown(page.getByRole('row', { name: /AAPL/ }).getByTestId('earnings-unknown'), 'Unknown');
  });

  test('SC-EUNK-09b: a 500 from GET /positions/{id}/gap-risk shows "Earnings: unknown", not an empty Alerts cell', async ({ page }) => {
    await stubPositions(page, [position()], (r) => json(r, { detail: 'Internal server error' }, 500));
    await stubEarnings(page, OK_NO_DATE);
    await gotoPositionsTable(page);
    await expectMutedUnknown(page.getByTestId('gap-risk-earnings-unknown'), 'Earnings: unknown');
    await expect(page.getByTestId('gap-risk-badge')).toHaveCount(0);
  });

  test('SC-EUNK-09c: a 500 from gap risk for a UK position shows nothing and is held, not re-sent on remount', async ({ page }) => {
    const calls = [];
    await stubPositions(page, [position({ ticker: 'BARC', market: 'UK' })], (r) => {
      calls.push(r.request().url());
      return json(r, { detail: 'Internal server error' }, 500);
    });
    await stubEarnings(page, OK_NO_DATE);
    await gotoPositionsTable(page, 'BARC');
    await expect.poll(() => calls.length).toBe(1);
    await expect(page.getByTestId('gap-risk-skeleton')).toHaveCount(0);
    await expect(page.getByTestId('gap-risk-earnings-unknown')).toHaveCount(0);
    await expect(page.getByTestId('gap-risk-badge')).toHaveCount(0);
    // Remount the Alerts cell (Grid view, then Table again): the failure is held 60 s.
    await page.locator('[aria-label="Grid view"]').click();
    await page.locator('[aria-label="Table view"]').click();
    await page.waitForSelector('table', { timeout: 5000 });
    await page.waitForLoadState('networkidle');
    expect(calls.length).toBe(1);
    await expect(page.getByTestId('gap-risk-earnings-unknown')).toHaveCount(0);
  });
});

// ---------------------------------------------------------------------------
// Not cached
// ---------------------------------------------------------------------------

test.describe('Session cache', () => {
  test.beforeEach(async ({ page }) => {
    await stubCommon(page);
  });

  test('SC-EUNK-08: an unavailable answer is held 60 s, then retried on the next mount; an ok answer is cached', async ({ page }) => {
    await page.clock.install();
    await stubScreener(page, [screenerRow()]);
    await stubWatchlist(page, [watchlistEntry()]);
    let msftAnswer = UNAVAILABLE;
    const calls = await stubEarnings(page, (ticker) => (ticker === 'MSFT' ? msftAnswer : OK_NO_DATE));
    const msftCalls = () => calls.filter((c) => c.includes('/earnings/MSFT')).length;
    const aaplCalls = () => calls.filter((c) => c.includes('/earnings/AAPL')).length;
    const msftRow = () => page.getByRole('row', { name: /MSFT/ });
    const aaplRow = () => page.getByRole('row', { name: /AAPL/ });

    // First visit: MSFT unavailable.
    await page.goto('/#/Watchlist');
    await expect(msftRow().getByTestId('earnings-unknown')).toBeVisible({ timeout: 8000 });
    expect(msftCalls()).toBe(1);

    // In-app navigation keeps the session cache (no reload).
    await page.evaluate(() => { window.location.hash = '#/Screener'; });
    await expect(aaplRow()).toBeVisible({ timeout: 8000 });
    await expect.poll(aaplCalls).toBe(1);

    // Back within 60 s: the unavailable answer is held, so no new request.
    msftAnswer = { ...OK_NO_DATE, ticker: 'MSFT', next_earnings_date: '2026-12-31', days_until_earnings: 21 };
    await page.evaluate(() => { window.location.hash = '#/Watchlist'; });
    await expect(msftRow().getByTestId('earnings-unknown')).toBeVisible({ timeout: 8000 });
    await page.waitForLoadState('networkidle');
    expect(msftCalls()).toBe(1);

    // After the hold: the next mount retries, and the recovered answer replaces "Unknown".
    await page.evaluate(() => { window.location.hash = '#/Screener'; });
    await expect(aaplRow()).toBeVisible({ timeout: 8000 });
    await page.clock.fastForward(61000);
    await page.evaluate(() => { window.location.hash = '#/Watchlist'; });
    await expect(msftRow()).toContainText('21d', { timeout: 8000 });
    await expect(msftRow().getByTestId('earnings-unknown')).toHaveCount(0);
    expect(msftCalls()).toBe(2);

    // The ok AAPL answer was cached for the session: no new request, even after the hold.
    await page.evaluate(() => { window.location.hash = '#/Screener'; });
    await expect(aaplRow()).toBeVisible({ timeout: 8000 });
    await expect(aaplRow().getByText('…')).toHaveCount(0);
    await page.waitForLoadState('networkidle');
    expect(aaplCalls()).toBe(1);
  });
});
