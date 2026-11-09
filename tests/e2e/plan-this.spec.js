/**
 * "Plan this" from Signals and Screener — ST-07 (BLG-FE-255, EPIC-02, v9.16)
 *
 * Design: docs/design/2026-11-06__release-v9.16/signal-to-plan-flow/decision_record.md §2.1, §6
 * Specs: signals.md v0.9 §"Plan this" Action; screener_results.md v1.11 §11.1;
 *        trade_plan.md v1.22 §2 (route parameters) and §5a.1 (signal_id presence)
 *
 *   SC-PT-01  Signals (new card): one click opens a pre-filled Trade Plan (ticker, market, entry)
 *             with the Signal Context panel; the signal is not changed (no PATCH)
 *   SC-PT-02  Signals: shown on new and watchlisted cards; hidden on dismissed, entered,
 *             already_held and allocation_insufficient
 *   SC-PT-03  Screener row: one click opens a pre-filled Trade Plan with no signal_id and no panel
 *   SC-PT-04  Screener row: the panel shows when a watchlisted signal exists for the ticker
 *   SC-PT-05  A dismissed signal_id falls back to the watchlisted lookup (no panel here)
 * SC-PT-01 and SC-PT-03 run in the dark and light themes.
 *
 * Infrastructure: page.route() network interception — no live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const SIGNAL = {
  id: 'sig-pt-0001', ticker: 'AAPL', market: 'US', signal_date: '2026-11-09', rank: 1,
  momentum_percent: 18.5, current_price: 182.3, price_gbp: 143.0, atr_value: 3.45,
  volatility: 0.012, initial_stop: 164.85, suggested_shares: 10, allocation_gbp: 1430.0,
  total_cost: 1430.0, status: 'new', ma200: 160, regime_on: true,
};

function screenerRow(overrides = {}) {
  return {
    ticker: 'MSFT', market: 'US', price: 410.25, currency: 'USD', atr: 6.1, atr_pct: 1.5,
    regime_status: 'risk_on', signal_score: 0.8, sector: 'Technology',
    proximity_to_entry_zone: 'near_entry', news_headline_count: 0, ...overrides,
  };
}

const ok = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });

/** Catch-all first; later routes take precedence. Returns the list of non-GET /signals calls. */
async function mockApi(page, { signals = [SIGNAL], screener = [] } = {}) {
  const writes = [];
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(ok({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(ok({ status: 'ok', data: { spy: { price: 521, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7200, is_risk_on: true }, fx_rate: 1.27 } }))
  );
  await page.route(`${API}/cash/summary`, (r) => r.fulfill(ok({ status: 'ok', current_cash: 10000 })));
  await page.route(`${API}/positions**`, (r) => r.fulfill(ok([])));
  await page.route(new RegExp(`${API}/signals(\\?.*)?$`), (r) => {
    if (r.request().method() !== 'GET') { writes.push(r.request().method()); return r.fulfill(ok({ status: 'ok' })); }
    const status = new URL(r.request().url()).searchParams.get('status');
    const data = status ? signals.filter((s) => s.status === status) : signals;
    return r.fulfill(ok({ status: 'ok', data }));
  });
  await page.route(new RegExp(`${API}/signals/[^/?]+$`), (r) => { writes.push(r.request().method()); return r.fulfill(ok({ status: 'ok' })); });
  await page.route(`${API}/screener/results**`, (r) =>
    r.fulfill(ok({ results: screener, run_id: 'run-pt', run_timestamp: new Date().toISOString(), total: screener.length, limit: 200, offset: 0 }))
  );
  await page.route(`${API}/screener/regime-distribution**`, (r) =>
    r.fulfill(ok({ ok: true, data: { window: '30d', run_count: 1, total_observations: 1, risk_on_count: 1, risk_off_count: 0, risk_on_pct: 100, risk_off_pct: 0 } }))
  );
  await page.route(`${API}/watchlist`, (r) => r.fulfill(ok({ items: [] })));
  return writes;
}

async function expectTradePlanPrefilled(page, { ticker, entry }) {
  await expect(page).toHaveURL(/#\/TradePlan\?/, { timeout: 8000 });
  await expect(page.getByTestId('planned-entry-price-input')).toHaveValue(entry, { timeout: 8000 });
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible();
  await expect(page.getByText(new RegExp(`${ticker} — US`))).toBeVisible();
}

for (const theme of ['dark', 'light']) {
  test.describe(`Plan this (${theme} theme)`, () => {
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    });

    test(`SC-PT-01 (${theme}): a Signals card opens a pre-filled Trade Plan with Signal Context, without changing the signal`, async ({ page }) => {
      const writes = await mockApi(page);
      await page.goto('/#/Signals');
      const btn = page.getByTestId('signal-plan-this-AAPL');
      await expect(btn).toBeVisible({ timeout: 10000 });
      await expect(btn).toHaveAccessibleName('Plan this: AAPL');
      await btn.click();
      await expectTradePlanPrefilled(page, { ticker: 'AAPL', entry: '182.3' });
      const url = new URL(page.url().replace('#/', ''));
      expect(url.searchParams.get('signal_id')).toBe('sig-pt-0001');
      expect(url.searchParams.get('market')).toBe('US');
      await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 8000 });
      expect(writes).toEqual([]);
    });

    test(`SC-PT-03 (${theme}): a Screener row opens a pre-filled Trade Plan with no signal_id and no panel`, async ({ page }) => {
      await mockApi(page, { signals: [], screener: [screenerRow()] });
      await page.goto('/#/Screener');
      const btn = page.getByTestId('screener-plan-this-MSFT');
      await expect(btn).toBeVisible({ timeout: 10000 });
      await expect(btn).toHaveAccessibleName('Plan this: MSFT');
      await btn.click();
      await expectTradePlanPrefilled(page, { ticker: 'MSFT', entry: '410.25' });
      const url = new URL(page.url().replace('#/', ''));
      expect(url.searchParams.get('signal_id')).toBeNull();
      await expect(page.getByTestId('signal-context-panel')).toHaveCount(0);
    });
  });
}

test('SC-PT-02: Plan this shows on new and watchlisted cards only', async ({ page }) => {
  const statuses = ['new', 'watchlisted', 'dismissed', 'entered', 'already_held', 'allocation_insufficient'];
  const signals = statuses.map((status, i) => ({ ...SIGNAL, id: `sig-${status}`, ticker: `T${i}${status.slice(0, 3).toUpperCase()}`, rank: i + 1, status }));
  await mockApi(page, { signals });
  await page.goto('/#/Signals');
  await expect(page.getByTestId(`signal-plan-this-${signals[0].ticker}`)).toBeVisible({ timeout: 10000 });
  // Dismissed cards may be hidden by the page's own filter; when shown, they carry no Plan this.
  await expect(page.getByTestId(`signal-plan-this-${signals[1].ticker}`)).toBeVisible();
  for (const s of signals.slice(2)) {
    await expect(page.getByTestId(`signal-plan-this-${s.ticker}`)).toHaveCount(0);
  }
});

test('SC-PT-04: a Screener row shows Signal Context when a watchlisted signal exists for the ticker', async ({ page }) => {
  await mockApi(page, { signals: [{ ...SIGNAL, ticker: 'MSFT', status: 'watchlisted' }], screener: [screenerRow()] });
  await page.goto('/#/Screener');
  await page.getByTestId('screener-plan-this-MSFT').click();
  await expectTradePlanPrefilled(page, { ticker: 'MSFT', entry: '410.25' });
  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 8000 });
});

test('SC-PT-05: a dismissed signal_id falls back to the watchlisted lookup', async ({ page }) => {
  await mockApi(page, { signals: [{ ...SIGNAL, status: 'dismissed' }] });
  await page.goto('/#/TradePlan?ticker=AAPL&market=US&entry_price=182.3&signal_id=sig-pt-0001');
  await expect(page.getByTestId('planned-entry-price-input')).toHaveValue('182.3', { timeout: 10000 });
  await expect(page.getByTestId('signal-context-panel')).toHaveCount(0);
});
