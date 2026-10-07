/**
 * Stop Provenance Line and Per-Row Stop Details
 * ST-06 (BLG-FE-193, EPIC-02, v9.10)
 *
 * Design source: docs/design/2026-10-06__release-v9.10/stop-cell-provenance/decision_record.md §5
 * Frontend spec: docs/specs/frontend/pages/positions.md §Stop Provenance Line and Per-Row Stop Details
 *
 * Coverage:
 *   SC-SCP-01  Table View — provenance line shows multiplier + ATR for a profitable (2x) and a losing (5x) row
 *   SC-SCP-02  Focusing a row's stop shows the tooltip: ATR, multiplier state, profitable formula, ratchet, nightly source
 *   SC-SCP-03  Losing row tooltip: 5x formula without the entry floor, "when positions loaded" source, grace line
 *   SC-SCP-04  Null-field row: "ATR unavailable", "not recorded yet", "Not recalculated since recalculation tracking began."
 *   SC-SCP-05  ATR present but multiplier null shows "ATR {atr}"; atr_source fallback/user append "estimated"/"entered"
 *   SC-SCP-06  Grid View — provenance line and stop-details trigger present in the Stop tile
 *   SC-SCP-07  Header explainer no longer claims "recalculated daily"
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Positions'). Grid View
 * is the default; Table View requires clicking [aria-label="Table view"].
 */

'use strict';

const { test, expect } = require('@playwright/test');

function makePosition(overrides = {}) {
  return {
    id: 'pos-scp-01',
    ticker: 'AAPL',
    market: 'US',
    entry_price: 150.00,
    current_price: 155.00,
    current_price_native: 160.00,
    stop_price: 140.00,
    stop_price_native: 145.00,
    shares: 10,
    pnl: 50.00,
    pnl_percent: 3.3,
    holding_days: 30,
    grace_days_remaining: null,
    status: 'open',
    entry_date: new Date().toISOString(),
    initial_stop: 130.00,
    current_trailing_stop: 135.00,
    risk_off_exit: false,
    lifecycle_state: 'PROFITABLE',
    position_state: 'PROFITABLE',
    days_in_state: 20,
    tags: null,
    last_reviewed_at: new Date().toISOString(),
    ...overrides,
  };
}

async function stubPositionsPage(page, positions) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance') || url.includes('/grace-period-alerts') || url.includes('/gap-risk')) {
      return route.continue();
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) });
  });
  await page.route('**/positions/*/gap-risk', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false } }) })
  );
  await page.route('**/positions/compliance*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/positions/grace-period-alerts', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );
  await page.route('**/portfolio/drawdown-status', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { threshold_breached: false } }) })
  );
  await page.route('**/portfolio/concentration-status', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { any_breach: false } }) })
  );
  await page.route('**/portfolio*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null, days_until_earnings: null }) })
  );
}

async function gotoPositionsTable(page, positions) {
  await stubPositionsPage(page, positions);
  await page.goto('/#/Positions');
  const firstTicker = positions[0]?.ticker || 'AAPL';
  await page.waitForSelector(`text=${firstTicker}`, { timeout: 8000 });
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 8000 });
  await tableBtn.click();
  await page.waitForSelector('table', { timeout: 5000 });
}


const PROFITABLE = {
  id: 'pos-scp-aapl', ticker: 'AAPL', market: 'US',
  atr_value: 3.21, active_atr_multiplier: 2, atr_source: 'fetched',
  stop_calculated_at: '2026-10-05T21:15:00', stop_calculation_source: 'nightly', grace_period: false,
};
const LOSING = {
  id: 'pos-scp-msft', ticker: 'MSFT', market: 'US', pnl: -20, pnl_percent: -1.5,
  atr_value: 4.5, active_atr_multiplier: 5, atr_source: 'fetched',
  stop_calculated_at: '2026-10-06T14:30:00', stop_calculation_source: 'on_load', grace_period: true,
  lifecycle_state: 'GRACE', position_state: 'GRACE',
};
const NULLS = {
  id: 'pos-scp-nvda', ticker: 'NVDA', market: 'US',
  atr_value: 0, active_atr_multiplier: null, atr_source: null,
  stop_calculated_at: null, stop_calculation_source: null, grace_period: false,
};

function rowFor(page, ticker) {
  return page.locator('tr', { has: page.getByText(ticker, { exact: true }) });
}

async function openStopDetails(page, ticker) {
  await page.getByRole('button', { name: `Stop calculation details for ${ticker}` }).focus();
  const tip = page.getByTestId('stop-details-tooltip').first();
  await expect(tip).toBeVisible({ timeout: 5000 });
  return tip;
}

test('SC-SCP-01: provenance line shows the multiplier and ATR for profitable and losing rows', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition(PROFITABLE), makePosition(LOSING)]);

  await expect(rowFor(page, 'AAPL').getByTestId('stop-provenance')).toHaveText('2× ATR $3.21');
  await expect(rowFor(page, 'MSFT').getByTestId('stop-provenance')).toHaveText('5× ATR $4.50');
});

test('SC-SCP-02: profitable row tooltip shows ATR, multiplier, floored formula, ratchet and nightly source', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition(PROFITABLE)]);

  const tip = await openStopDetails(page, 'AAPL');
  await expect(tip).toContainText('How this stop was set');
  await expect(tip).toContainText('ATR (14-day): $3.21');
  await expect(tip).toContainText('Multiplier: 2× (profitable, tight)');
  await expect(tip).toContainText('Price − 2× ATR, never below entry (§7.2)');
  await expect(tip).toContainText('A stop never loosens: the stop shown is the highest level reached (§7.3).');
  await expect(tip).toContainText('Last recalculated 5 Oct 2026, 21:15 — nightly update');
  await expect(tip).not.toContainText('Grace period');
});

test('SC-SCP-03: losing row tooltip shows the 5x formula, on-load source and grace line', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition(LOSING)]);

  const tip = await openStopDetails(page, 'MSFT');
  await expect(tip).toContainText('Multiplier: 5× (losing or flat, wide)');
  await expect(tip).toContainText('Price − 5× ATR (§7.2)');
  await expect(tip).not.toContainText('never below entry');
  await expect(tip).toContainText('Last recalculated 6 Oct 2026, 14:30 — when positions loaded');
  await expect(tip).toContainText('Grace period: the stop is tracked but not enforced (§6.3).');
});

test('SC-SCP-04: a row with null fields shows the fallback strings', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition(NULLS)]);

  await expect(rowFor(page, 'NVDA').getByTestId('stop-provenance')).toHaveText('ATR unavailable');
  const tip = await openStopDetails(page, 'NVDA');
  await expect(tip).toContainText('Multiplier: not recorded yet');
  await expect(tip).toContainText('Not recalculated since recalculation tracking began.');
});

test('SC-SCP-05: multiplier-null and ATR-source variants of the provenance line', async ({ page }) => {
  await gotoPositionsTable(page, [
    makePosition({ ...PROFITABLE, active_atr_multiplier: null }),
    makePosition({ ...LOSING, atr_source: 'fallback' }),
    makePosition({ ...NULLS, ticker: 'TSLA', id: 'pos-scp-tsla', atr_value: 7.1, active_atr_multiplier: 2.5, atr_source: 'user' }),
  ]);

  await expect(rowFor(page, 'AAPL').getByTestId('stop-provenance')).toHaveText('ATR $3.21');
  await expect(rowFor(page, 'MSFT').getByTestId('stop-provenance')).toHaveText('5× ATR $4.50 · estimated');
  await expect(rowFor(page, 'TSLA').getByTestId('stop-provenance')).toHaveText('2.5× ATR $7.10 · entered');

  const tip = await openStopDetails(page, 'MSFT');
  await expect(tip).toContainText('(estimated from 2% of entry price)');
});

test('SC-SCP-06: Grid View shows the provenance line and stop-details trigger in the Stop tile', async ({ page }) => {
  await stubPositionsPage(page, [makePosition(PROFITABLE)]);
  await page.goto('/#/Positions');
  await page.waitForSelector('text=AAPL', { timeout: 8000 });

  await expect(page.getByTestId('stop-provenance')).toHaveText('2× ATR $3.21');
  const tip = await openStopDetails(page, 'AAPL');
  await expect(tip).toContainText('nightly update');
});

test('SC-SCP-07: header explainer no longer claims ATR is recalculated daily', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition(PROFITABLE)]);

  await page.getByRole('button', { name: /why is my stop moving/i }).hover();
  await expect(page.getByText(/recalculated when positions load and by a nightly update/i)).toBeVisible({ timeout: 5000 });
  await expect(page.getByText(/recalculated daily/i)).toHaveCount(0);
});
