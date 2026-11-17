/**
 * Populated route stubs for the light-theme axe scans of every routed page
 * (ST-08, EPIC-03, v9.17, BLG-FE-265).
 *
 * Each payload is copied from the page's own spec, where it was built from the
 * writing service's response shape and has run green in CI:
 *   Strategy Benchmark  strategy-benchmark.spec.js (SUMMARY_WITH_ACTUAL, TRADES_RESPONSE, OPEN_POSITIONS_WITH_DATA)
 *   System Status       system-status.spec.js (HEALTH_RESPONSE, a TEST_RESULTS_RESPONSE subset with one failure)
 *   Watchlist           watchlist.spec.js (US_ENTRY, UK_ENTRY)
 *   Ticker Universe     ticker-universe.spec.js (TICKER_LIST)
 *   Screener            screener.spec.js (makeResult, makeScreenerResponse, makeRegimeDistribution)
 *   Trade Plans         trade-plan-stale-marker.spec.js (plan())
 *   Research            research-typography.spec.js (RESEARCH_OK, HEAT_OK)
 *   Journal             journal.spec.js (TRADES, OPEN_POSITIONS, RED_FLAGS)
 *   Performance         performance.spec.js (metricsResponse, MONTHLY)
 *   Risk Dashboard      mocks/portfolio-mock-data.js (TD_02, PROSPECTIVE_HEAT_GENERIC)
 *   Notifications       mocks/smoke-mock-data.js (SMOKE_NOTIFICATIONS)
 *   Signals             signal-card.spec.js (WL_MOCK_SIGNAL, WL_MARKET_STATUS, WL_CASH_SUMMARY)
 *
 * Every helper installs the generic catch-all first, so any other request the
 * page makes gets an empty `{status, data: []}` envelope.
 */
const { TD_02, PROSPECTIVE_HEAT_GENERIC } = require('../mocks/portfolio-mock-data');
const { SMOKE_NOTIFICATIONS } = require('../mocks/smoke-mock-data');

const API = 'http://localhost:8000';
const DAY = 86400000;
const ok = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });
const envelope = (data) => ok({ status: 'ok', data });
const isoDaysAgo = (n) => new Date(Date.now() - n * DAY - 3600000).toISOString();
const dateDaysAgo = (n) => new Date(Date.now() - n * DAY).toISOString().slice(0, 10);

async function catchAll(page) {
  await page.route(new RegExp(`${API}/`), (route) => {
    const url = route.request().url();
    if (url.includes('/market/status')) {
      return route.fulfill(envelope({ spy: { price: 521.0, ma200: 480.0, is_risk_on: true }, ftse: { is_risk_on: false }, fx_rate: 1.27 }));
    }
    if (/\/positions(\?|$)/.test(url)) return route.fulfill(ok([]));
    return route.fulfill(envelope([]));
  });
}

// --- Strategy Benchmark ----------------------------------------------------
const BENCHMARK_SUMMARY = {
  filters: { year: null, market: 'ALL' },
  last_imported_at: '2026-06-30T10:15:00Z',
  available_years: [2023, 2024, 2025, 2026],
  backtest_stats: { total_trades: 40, win_rate_pct: 62.5, avg_pnl_gbp: 210.5, total_pnl_gbp: 8420.0, avg_hold_days: 14.2 },
  actual_stats: { total_trades: 6, win_rate_pct: 66.7, avg_pnl_gbp: 180.3, total_pnl_gbp: 1081.8, avg_hold_days: 11.5 },
  yearly_breakdown: [
    { entry_year: 2025, num_trades: 20, avg_pnl_gbp: 200.0, total_pnl_gbp: 4000.0, avg_hold_days: 13.0, win_rate_pct: 60.0 },
  ],
};
const BENCHMARK_TRADES = {
  filters: { year: null, market: 'ALL' },
  backtest_trades: [
    { id: 1, ticker: 'NVDA', entry_date: '2023-02-28', exit_date: '2023-03-20', holding_days: 20, entry_price: 234.5, exit_price: 268.1, pnl_gbp: 425.3, pnl_pct: 14.33, market: 'US', exit_reason: 'Stop', was_profitable: true, entry_year: 2023 },
    { id: 2, ticker: 'BARC', entry_date: '2023-04-10', exit_date: '2023-04-25', holding_days: 15, entry_price: 150.0, exit_price: 145.0, pnl_gbp: -75.0, pnl_pct: -3.33, market: 'UK', exit_reason: 'Risk-Off', was_profitable: false, entry_year: 2023 },
    { id: 3, ticker: 'MSFT', entry_date: '2023-05-01', exit_date: '2023-05-20', holding_days: 19, entry_price: 300.0, exit_price: 320.0, pnl_gbp: 200.0, pnl_pct: 6.67, market: 'US', exit_reason: 'Rebalance', was_profitable: true, entry_year: 2023 },
  ],
  actual_trades: [
    { ticker: 'AAPL', entry_date: '2024-03-01', exit_date: '2024-03-22', holding_days: 21, entry_price: 175.4, exit_price: 182.1, pnl_gbp: 312.5, pnl_pct: 3.82, market: 'US', exit_reason: 'trailing_stop', was_profitable: true, entry_year: 2024 },
  ],
};
const BENCHMARK_OPEN = {
  filters: { market: 'ALL' },
  open_positions: [
    { ticker: 'TSLA', market: 'US', entry_date: '2026-06-01', entry_price: 210.0, current_price: 228.5, unrealized_pnl_gbp: 18.5, unrealized_pnl_pct: 8.81, days_held: 32 },
  ],
  summary: { count: 1, total_unrealized_pnl_gbp: 18.5 },
};
async function mockStrategyBenchmark(page) {
  await catchAll(page);
  await page.route(/\/strategy\/benchmark\/open-positions/, (r) => r.fulfill(ok(BENCHMARK_OPEN)));
  await page.route(/\/strategy\/benchmark\/summary/, (r) => r.fulfill(ok(BENCHMARK_SUMMARY)));
  await page.route(/\/strategy\/benchmark\/trades/, (r) => r.fulfill(ok(BENCHMARK_TRADES)));
}

// --- System Status ----------------------------------------------------------
async function mockSystemStatus(page) {
  await catchAll(page);
  await page.route(`${API}/health/detailed`, (r) =>
    // checks shape per backend/services/health_service.py (status + details per component),
    // one of each status so every health card style renders.
    r.fulfill(ok({
      status: 'degraded', response_time_ms: 5.2, timestamp: '2026-04-15T10:00:00Z',
      checks: {
        database: { status: 'healthy', details: { connected: true, portfolio_exists: true } },
        yahooFinance: { status: 'degraded', details: { note: 'slow' } },
        services: { status: 'unhealthy', details: { error: 'import failed' } },
        config: { status: 'unknown', details: null },
      },
    })));
  await page.route(`${API}/test/endpoints`, (r) =>
    r.fulfill(ok({
      summary: { total: 4, passed: 3, failed: 1, errors: 0, success_rate: 75.0 },
      results: [
        { endpoint: 'GET /', status: 'pass', status_code: 200, response_time_ms: 3.1 },
        { endpoint: 'GET /analytics/metrics', status: 'pass', status_code: 200, response_time_ms: 12.3 },
        { endpoint: 'GET /positions', status: 'pass', status_code: 200, response_time_ms: 8.1 },
        { endpoint: 'GET /signals', status: 'fail', status_code: 500, response_time_ms: 13.1 },
      ],
    })));
}

// --- Watchlist --------------------------------------------------------------
const WATCHLIST_ENTRY = (id, ticker, market, company, days, extra = {}) => ({
  id, ticker, market, company_name: company, signal_status: 'no_signal', tags: [],
  target_entry_price: null, initial_stop_price: null, current_stop_price: null,
  created_at: isoDaysAgo(days), updated_at: isoDaysAgo(days), added_at: isoDaysAgo(days),
  days_on_watchlist: days, is_stale: false, ...extra,
});
async function mockWatchlist(page) {
  await catchAll(page);
  await page.route(`${API}/watchlist`, (r) =>
    r.fulfill(envelope([
      WATCHLIST_ENTRY('wl-us-001', 'AAPL', 'US', 'Apple Inc.', 5),
      WATCHLIST_ENTRY('wl-uk-001', 'VOD.L', 'UK', 'Vodafone Group', 7),
    ])));
}

// --- Ticker Universe --------------------------------------------------------
async function mockTickerUniverse(page) {
  await catchAll(page);
  await page.route(`${API}/ticker-universe?active_only=false`, (r) =>
    r.fulfill(envelope([
      { ticker: 'AAPL', market: 'US', active: true, sector: 'Technology', industry: 'Software', company_name: 'Apple Inc.' },
      { ticker: 'BATS.L', market: 'UK', active: true, sector: 'Consumer', industry: 'Tobacco', company_name: 'British American Tobacco' },
      { ticker: 'TSLA', market: 'US', active: false, sector: 'Auto', industry: 'EV', company_name: 'Tesla, Inc.' },
    ])));
}

// --- Screener ---------------------------------------------------------------
const screenerResult = (overrides = {}) => ({
  ticker: 'AAPL', market: 'US', price: 175.5, currency: 'USD', atr: 3.2, atr_pct: 1.83,
  regime_status: 'risk_on', signal_score: 0.82, sector: 'Technology',
  proximity_to_entry_zone: 'near_entry', news_headline_count: 3, ...overrides,
});
async function mockScreener(page) {
  await catchAll(page);
  const results = [
    screenerResult(),
    screenerResult({ ticker: 'BARC.L', market: 'UK', price: 150.2, currency: 'GBP', regime_status: 'risk_off', signal_score: 0.41, proximity_to_entry_zone: 'far', news_headline_count: 0 }),
  ];
  await page.route(`${API}/screener/results**`, (r) =>
    r.fulfill(ok({ results, run_id: 'run-001', run_timestamp: isoDaysAgo(0), total: results.length, limit: 200, offset: 0 })));
  await page.route(`${API}/screener/regime-distribution**`, (r) =>
    r.fulfill(ok({ ok: true, data: { window: '30d', run_count: 20, total_observations: 32, risk_on_count: 24, risk_off_count: 8, risk_on_pct: 75.0, risk_off_pct: 25.0 } })));
}

// --- Trade Plans ------------------------------------------------------------
const plan = (id, ticker, status, days) => ({
  id, ticker, market: 'US', status, position_id: null, r_target: 2, setup_thesis: 'thesis',
  created_at: isoDaysAgo(days + 5), updated_at: isoDaysAgo(days),
});
async function mockTradePlans(page) {
  await catchAll(page);
  await page.route(`${API}/trade-plans`, (r) =>
    r.fulfill(envelope([
      plan('a', 'AAA', 'draft', 15),
      plan('b', 'BBB', 'research_pending', 2),
      plan('c', 'CCC', 'entry_conditions_set', 1),
      plan('d', 'DDD', 'active', 3),
      plan('e', 'EEE', 'abandoned', 9),
    ])));
}

// --- Research (ticker view) -------------------------------------------------
async function mockResearch(page, ticker = 'AAPL') {
  await catchAll(page);
  await page.route(`${API}/research/${ticker}`, (r) =>
    r.fulfill(ok({
      status: 'ok',
      data: {
        ticker, market: 'US', price: 182.3, price_change_pct: 0.012, market_cap: 2800000000000,
        updated_at: isoDaysAgo(0),
        signal: { signal_id: 'sig-typ-001', status: 'active', rank: 1, atr: 4.2, entry_price: 178.5, stop_price: 172.0, r_target: 2.5 },
        regime: { label: 'risk_on', spy_risk_on: true, ftse_risk_on: true },
        sector: { sector: 'Technology', industry: 'Consumer Electronics' },
        screener: null,
        earnings: null,
        news_headlines: [{ headline: 'Apple reports record quarterly revenue', source: 'Reuters', published_at: isoDaysAgo(0) }],
      },
    })));
  await page.route(`${API}/portfolio/prospective-heat**`, (r) =>
    r.fulfill(ok({ status: 'ok', data: { valid: true, current_heat_percent: 12.0, prospective_heat_percent: 18.5, incremental_heat_percent: 6.5, prospective_risk_gbp: 650, portfolio_value_gbp: 50000, ticker } })));
}

// --- Risk Dashboard ---------------------------------------------------------
async function mockRiskDashboard(page) {
  await catchAll(page);
  await page.route(`${API}/portfolio`, (r) => r.fulfill(ok(TD_02)));
  await page.route(`${API}/portfolio/prospective-heat*`, (r) => r.fulfill(ok(PROSPECTIVE_HEAT_GENERIC)));
}

// --- Journal ----------------------------------------------------------------
const JOURNAL_TRADES = [
  { id: 't-aapl', ticker: 'AAPL', market: 'US', entry_date: '2026-09-01', exit_date: '2026-09-20', shares: 7, entry_price: 100, exit_price: 110, pnl: 55.12, pnl_pct: 10, pnl_percent: 10, holding_days: 20, exit_reason: 'Target Reached', entry_note: 'Breakout on volume', exit_note: 'Hit the target zone', tags: ['momentum'], net_r_multiple: 1.25 },
  { id: 't-lgen', ticker: 'LGEN.L', market: 'UK', entry_date: '2026-08-04', exit_date: '2026-08-29', shares: 400, entry_price: 2.5, exit_price: 2.35, pnl: -60, pnl_pct: -6, pnl_percent: -6, holding_days: 26, exit_reason: 'Stop Loss', entry_note: 'Dividend run-up', exit_note: null, tags: ['income'], net_r_multiple: -1 },
];
const JOURNAL_POSITIONS = [
  { id: 'p-nvda', ticker: 'NVDA', market: 'US', status: 'open', entry_date: '2026-10-01', entry_price: 500, current_price: 520, shares: 4, pnl: 62.99, pnl_percent: 4, entry_note: 'Earnings gap held', tags: ['momentum'] },
];
const JOURNAL_RED_FLAGS = [
  { id: 'e-1', event_type: 'pre_entry_override', ticker: 'AAPL', position_id: null, context: { source: 'trade_plan', override_acknowledged: true }, created_at: isoDaysAgo(0) },
  { id: 'e-2', event_type: 'checklist_skipped', ticker: 'LGEN.L', position_id: null, context: { unchecked_items: 2, total_items: 6 }, created_at: isoDaysAgo(1) },
];
async function mockJournal(page) {
  await catchAll(page);
  await page.route(/localhost:8000\/trades(\?|$)/, (r) =>
    r.fulfill(envelope({ total_trades: JOURNAL_TRADES.length, trades: JOURNAL_TRADES })));
  // GET /positions is a bare array, as in journal.spec.js.
  await page.route(/localhost:8000\/positions$/, (r) => r.fulfill(ok(JOURNAL_POSITIONS)));
  await page.route(/localhost:8000\/portfolio\/red-flag-journal/, (r) =>
    r.fulfill(envelope({ total: JOURNAL_RED_FLAGS.length, page: 1, page_size: 20, items: JOURNAL_RED_FLAGS })));
}

// --- Performance ------------------------------------------------------------
const PERFORMANCE_TRADES = Array.from({ length: 12 }, (_, i) => {
  const win = i % 3 !== 0;
  return {
    id: `t-${i}`, ticker: ['AAPL', 'MSFT', 'BARC.L'][i % 3], market: i % 3 === 2 ? 'UK' : 'US',
    entry_date: dateDaysAgo(20 + i), exit_date: dateDaysAgo(1 + i), shares: 10, entry_price: 100, exit_price: win ? 110 : 95,
    pnl: win ? 78.74 : -39.37, pnl_pct: win ? 10 : -5, pnl_percent: win ? 10 : -5,
    exit_reason: win ? 'Target Reached' : 'Stop Loss', tags: [], holding_days: 19, fees: 1.5,
  };
});
async function mockPerformance(page) {
  await catchAll(page);
  await page.route(/localhost:8000\/analytics\/metrics/, (r) =>
    r.fulfill(envelope({
      summary: { total_pnl: 551.18, win_rate: 66.7, total_trades: 12, has_enough_data: true, min_required: 10 },
      executive_metrics: { sharpe_ratio: 1.37, sharpe_method: 'trade', max_drawdown: { percent: -4.2, amount: 118.11, date: dateDaysAgo(4) }, recovery_factor: 4.67, expectancy: 45.93, profit_factor: 4.0, risk_reward_ratio: 2.0 },
      advanced_metrics: { win_streak: 4, loss_streak: 1, avg_hold_winners: 19, avg_hold_losers: 19, trade_frequency: 2.3, capital_efficiency: 5.5, days_underwater: 0, portfolio_peak_equity: 551.18, peak_date: dateDaysAgo(1) },
      consistency_metrics: { consecutive_profitable_months: 3, current_streak: 2, win_rate_std_dev: 12.4, pnl_std_dev: 210.55 },
      trades_for_charts: PERFORMANCE_TRADES,
    })));
  await page.route(/localhost:8000\/trades(\?|$)/, (r) => r.fulfill(envelope({ trades: PERFORMANCE_TRADES })));
  await page.route(/localhost:8000\/reports\/monthly-pnl(?!\?format=csv)/, (r) =>
    r.fulfill(ok({
      status: 'ok',
      data: [
        { year: 2026, month: 7, realised_pnl_gbp: 1250.0, trade_count: 4, avg_pnl_per_trade_gbp: 312.5, gross_profit_gbp: 1500.0, gross_loss_gbp: -250.0, total_fees_gbp: 12.5 },
        { year: 2026, month: 8, realised_pnl_gbp: -310.55, trade_count: 3, avg_pnl_per_trade_gbp: -103.52, gross_profit_gbp: 90.0, gross_loss_gbp: -400.55, total_fees_gbp: 9.0 },
      ],
      estimated_unrealised_pnl: null,
      unrealised_note: null,
      compliance_summary: { period_days: 30, validation_pass_rate: 0.82, override_count: 2, red_flag_events_count: 5, most_frequent_rule_breach: 'sector_concentration' },
    })));
  await page.route(/localhost:8000\/analytics\/arc5-compliance/, (r) =>
    r.fulfill(envelope({ events_per_week: 1.2, override_rate: 0.15, top_rule_breach: 'stop_widened', trade_plan_adherence_rate: 0.9, validation_pass_rate_by_rule: [] })));
}

// --- Signals ----------------------------------------------------------------
const SIGNAL = {
  id: 'sig-uuid-0001', ticker: 'AAPL', market: 'US', signal_date: '2026-05-18', rank: 1,
  momentum_percent: 18.5, current_price: 182.3, price_gbp: 143.0, atr_value: 3.45, volatility: 0.012,
  initial_stop: 164.85, suggested_shares: 10, allocation_gbp: 1430.0, total_cost: 1430.0, status: 'new',
};
async function mockSignals(page) {
  await catchAll(page);
  await page.route(`${API}/signals**`, (r) =>
    r.fulfill(envelope([
      SIGNAL,
      { ...SIGNAL, id: 'sig-uuid-0002', ticker: 'VOD.L', market: 'UK', rank: 2, momentum_percent: -2.1, status: 'watchlisted' },
      { ...SIGNAL, id: 'sig-uuid-0003', ticker: 'MSFT', rank: 3, status: 'dismissed' },
      { ...SIGNAL, id: 'sig-uuid-0004', ticker: 'NVDA', rank: 4, status: 'entered' },
    ])));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(envelope({ spy: { price: 521.0, ma200: 480.0, is_risk_on: true }, ftse: { price: 7800.0, ma200: 7200.0, is_risk_on: false }, fx_rate: 1.27 })));
  await page.route(`${API}/cash/summary`, (r) => r.fulfill(ok({ status: 'ok', current_cash: 10000.0 })));
}

// --- Notifications ----------------------------------------------------------
async function mockNotifications(page) {
  await catchAll(page);
  await page.route(/localhost:8000\/notifications\?/, (r) => r.fulfill(ok(SMOKE_NOTIFICATIONS)));
}

module.exports = {
  catchAll,
  mockStrategyBenchmark,
  mockSystemStatus,
  mockWatchlist,
  mockTickerUniverse,
  mockScreener,
  mockTradePlans,
  mockResearch,
  mockRiskDashboard,
  mockJournal,
  mockPerformance,
  mockNotifications,
  mockSignals,
};
