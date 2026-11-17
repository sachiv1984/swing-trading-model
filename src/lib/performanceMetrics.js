// Performance page (performance.md v1.1 §5; ST-06, BLG-FE-259, EPIC-02, v9.17):
// every period-level KPI is read from GET /analytics/metrics, the canonical
// server computation (metrics_definitions.md), not recomputed in the browser.
// This maps the response onto the camelCase props the existing analytics
// components take. A missing field stays null/undefined so the component
// shows its own "N/A"; nothing is derived here.

const num = (v) => (typeof v === "number" && Number.isFinite(v) ? v : null);

// Response shape per analytics_service.py / analytics_endpoints.md:
// summary {total_trades, win_rate, total_pnl, has_enough_data, min_required},
// executive_metrics, advanced_metrics, and a separate consistency_metrics.
export function toMetricsProps(data) {
  const ex = data?.executive_metrics || {};
  const adv = data?.advanced_metrics || {};
  const con = data?.consistency_metrics || {};
  const dd = ex.max_drawdown;
  return {
    // sharpe_method "insufficient_data" comes with sharpe_ratio 0.0: show N/A,
    // not a poor result (metrics_definitions.md §Sharpe Ratio, Failure Behaviour).
    sharpeRatio: ex.sharpe_method === "insufficient_data" ? null : num(ex.sharpe_ratio),
    maxDrawdown: dd ? { percent: num(dd.percent), amount: num(dd.amount), date: dd.date ?? null } : null,
    recoveryFactor: num(ex.recovery_factor),
    expectancy: num(ex.expectancy),
    profitFactor: num(ex.profit_factor),
    riskRewardRatio: num(ex.risk_reward_ratio),
    winStreak: num(adv.win_streak),
    lossStreak: num(adv.loss_streak),
    avgHoldWinners: num(adv.avg_hold_winners),
    avgHoldLosers: num(adv.avg_hold_losers),
    tradeFrequency: num(adv.trade_frequency),
    capitalEfficiency: num(adv.capital_efficiency),
    daysUnderwater: num(adv.days_underwater),
    portfolioPeakEquity: num(adv.portfolio_peak_equity),
    peakDate: adv.peak_date ?? null,
    consecutiveProfitableMonths: num(con.consecutive_profitable_months),
    currentStreak: num(con.current_streak),
    winRateStdDev: num(con.win_rate_std_dev),
    pnlStdDev: num(con.pnl_std_dev),
  };
}

export function toSummary(data) {
  const s = data?.summary || {};
  return {
    totalPnl: num(s.total_pnl),
    winRate: num(s.win_rate),
    totalTrades: num(s.total_trades),
    minRequired: num(s.min_required),
    // has_enough_data is inside summary. A response without it counts as
    // enough only when it actually carries executive metrics, so an empty or
    // malformed body shows "Not enough trades" rather than blank KPIs.
    hasEnoughData:
      s.has_enough_data === true ||
      (s.has_enough_data == null && Object.keys(data?.executive_metrics || {}).length > 0),
  };
}
