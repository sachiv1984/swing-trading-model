/**
 * Populated GET /analytics/metrics mock (ST-06, BLG-FE-259, EPIC-02, v9.17).
 *
 * The Performance page reads its period-level KPIs from GET /analytics/metrics
 * (performance.md v1.1 §5.2) and shows "Not enough trades" in Summary and
 * Analytics when has_enough_data is not true. Specs that test an Analytics
 * component (heatmap, charts, market correlation, tag filter …) therefore need
 * a populated response as well as their GET /trades mock. Register it after
 * the spec's own catch-all route, so it takes precedence (Playwright runs the
 * most recently registered matching route first). Shape per
 * analytics_service.py / analytics_endpoints.md: has_enough_data inside
 * summary, consistency_metrics its own object; max_drawdown.percent ≤ 0.
 */
'use strict';

const METRICS = {
  status: 'ok',
  data: {
    summary: { total_pnl: 551.18, win_rate: 66.7, total_trades: 12, has_enough_data: true, min_required: 10 },
    executive_metrics: {
      sharpe_ratio: 1.37, sharpe_method: 'trade',
      max_drawdown: { percent: -4.2, amount: 118.11, date: null },
      recovery_factor: 4.67, expectancy: 45.93, profit_factor: 4.0, risk_reward_ratio: 2.0,
    },
    advanced_metrics: {
      win_streak: 4, loss_streak: 1, avg_hold_winners: 19, avg_hold_losers: 12, trade_frequency: 2.3,
      capital_efficiency: 5.5, days_underwater: 0, portfolio_peak_equity: 551.18, peak_date: null,
    },
    consistency_metrics: { consecutive_profitable_months: 1, current_streak: 1, win_rate_std_dev: 0, pnl_std_dev: 0 },
    trades_for_charts: [],
  },
};

// The Performance page's Analytics charts read trades_for_charts from this
// response (the server's own period window). Pass the spec's /trades fixture
// as `trades` (a bare array, { trades }, or { data: { trades } }) to chart it.
function toChartTrades(trades) {
  const list = Array.isArray(trades) ? trades : trades?.trades ?? trades?.data?.trades ?? (Array.isArray(trades?.data) ? trades.data : []);
  return list.map((t) => ({ ...t, pnl_pct: t.pnl_pct ?? t.pnl_percent }));
}

async function mockAnalyticsMetrics(page, { trades, ...overrides } = {}) {
  const data = { ...METRICS.data, ...overrides };
  if (trades !== undefined) data.trades_for_charts = toChartTrades(trades);
  const body = { ...METRICS, data };
  await page.route(/localhost:8000\/analytics\/metrics/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) })
  );
}

module.exports = { mockAnalyticsMetrics, ANALYTICS_METRICS: METRICS };
