import { formatCurrency, formatPercent } from "../../lib/format";
import { BarChart2 } from "lucide-react";
import DataState from "../ui/DataState";
import EmptyStateAction from "../ui/EmptyStateAction";
import ExecutiveSummaryCards from "../analytics/ExecutiveSummaryCards";
import PerformanceSummary from "../reports/PerformanceSummary";
import AdvancedMetricsGrid from "../analytics/AdvancedMetricsGrid";
import MonthlyHeatmap from "../analytics/MonthlyHeatmap";
import MarketComparison from "../analytics/MarketComparison";
import ExitReasonTable from "../analytics/ExitReasonTable";
import { exitReasonGroupKey, exitReasonLabel } from "../../constants/exitReasons";
import TimeBasedCharts from "../analytics/TimeBasedCharts";
import TopPerformers from "../analytics/TopPerformers";
import ConsistencyMetrics from "../analytics/ConsistencyMetrics";
import TagPerformance from "../analytics/TagPerformance";
import TradePlanTagFilter from "../analytics/TradePlanTagFilter";
import MarketCorrelationSection from "../analytics/MarketCorrelationSection";
import UnderwaterChart from "../analytics/UnderwaterChart";
import RMultipleAnalysis from "../analytics/RMultipleAnalysis";
import BestWorstTrades from "../analytics/BestWorstTrades";
import WinRateByMonth from "../analytics/WinRateByMonth";
import CohortAnalysis from "../analytics/CohortAnalysis";
import RMultipleDistribution from "../analytics/RMultipleDistribution";

export function generatePerformancePrintReport(metrics, periodLabel, tradeCount) {
  if (!metrics) return;
  const fx = (v, d = 2) => (typeof v === "number" ? v.toFixed(d) : "N/A");

  const reportHTML = `
    <!DOCTYPE html>
    <html>
      <head>
        <title>Performance Analytics Report</title>
        <style>
          body { font-family: system-ui, -apple-system, sans-serif; padding: 40px; color: #1e293b; }
          h1 { color: #0f172a; margin-bottom: 8px; font-size: 28px; }
          .subtitle { color: #64748b; margin-bottom: 32px; font-size: 14px; }
          .section { margin-bottom: 32px; page-break-inside: avoid; }
          .section-title { font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 16px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }
          .metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 16px; }
          .metric-card { background: #f8fafc; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; }
          .metric-label { font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
          .metric-value { font-size: 24px; font-weight: 700; color: #0f172a; }
          .metric-subtitle { font-size: 12px; color: #64748b; margin-top: 4px; }
          .positive { color: #16a34a; }
          .negative { color: #dc2626; }
          .neutral { color: #0f172a; }
          .insight-list { list-style: none; padding: 0; }
          .insight-item { background: #fffbeb; padding: 12px 16px; margin-bottom: 8px; border-radius: 6px; border-left: 3px solid #f59e0b; font-size: 14px; }
          table { width: 100%; border-collapse: collapse; margin-top: 16px; }
          th { background: #f1f5f9; padding: 12px; text-align: left; font-size: 12px; text-transform: uppercase; color: #64748b; border-bottom: 2px solid #cbd5e1; }
          td { padding: 12px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
          @media print {
            body { padding: 20px; }
            .section { page-break-inside: avoid; }
          }
        </style>
      </head>
      <body>
        <h1>Performance Analytics Report</h1>
        <div class="subtitle">Generated ${new Date().toLocaleDateString()} • Period: ${periodLabel} • ${tradeCount ?? 0} Trades</div>

        <div class="section">
          <div class="section-title">Executive Summary</div>
          <div class="metric-grid">
            <div class="metric-card">
              <div class="metric-label">Sharpe Ratio</div>
              <div class="metric-value">${fx(metrics.sharpeRatio, 2)}</div>
              <div class="metric-subtitle">Risk-Adjusted Returns</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Max Drawdown</div>
              <div class="metric-value negative">${formatPercent(metrics.maxDrawdown?.percent)}</div>
              <div class="metric-subtitle">${formatCurrency(metrics.maxDrawdown?.amount)}</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Recovery Factor</div>
              <div class="metric-value">${fx(metrics.recoveryFactor, 2)}</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Expectancy</div>
              <div class="metric-value ${metrics.expectancy > 0 ? 'positive' : metrics.expectancy < 0 ? 'negative' : 'neutral'}">${formatCurrency(metrics.expectancy, { signed: true })}</div>
              <div class="metric-subtitle">Per Trade</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Profit Factor</div>
              <div class="metric-value">${fx(metrics.profitFactor, 2)}</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Risk/Reward</div>
              <div class="metric-value">${fx(metrics.riskRewardRatio, 2)}:1</div>
            </div>
          </div>
        </div>

        <div class="section">
          <div class="section-title">Key Insights</div>
          <ul class="insight-list">
            ${metrics.sharpeRatio > 2 ? `<li class="insight-item">Excellent risk-adjusted returns with a Sharpe ratio of ${fx(metrics.sharpeRatio, 2)}</li>` :
              metrics.sharpeRatio > 1 ? `<li class="insight-item">Strong risk-adjusted returns with a Sharpe ratio of ${fx(metrics.sharpeRatio, 2)}</li>` :
              `<li class="insight-item">Risk-adjusted returns need improvement (Sharpe: ${fx(metrics.sharpeRatio, 2)})</li>`}
            ${metrics.avgHoldWinners > metrics.avgHoldLosers ?
              `<li class="insight-item">✅ Great discipline - cutting losers faster (${fx(metrics.avgHoldLosers, 1)} days) than letting winners run (${fx(metrics.avgHoldWinners, 1)} days)</li>` :
              `<li class="insight-item">⚠️ Holding losers too long (${fx(metrics.avgHoldLosers, 1)} days) compared to winners (${fx(metrics.avgHoldWinners, 1)} days)</li>`}
            ${metrics.profitFactor > 2 ? `<li class="insight-item">Excellent profit factor of ${fx(metrics.profitFactor, 2)} means earning ${formatCurrency(metrics.profitFactor)} for every £1 lost</li>` :
              `<li class="insight-item">Profit factor of ${fx(metrics.profitFactor, 2)} - earning ${formatCurrency(metrics.profitFactor)} per £1 lost</li>`}
          </ul>
        </div>

        <div class="section">
          <div class="section-title">Advanced Metrics</div>
          <table>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Metric</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Win Streak (Max)</td>
                <td>${metrics.winStreak} trades</td>
                <td>Loss Streak (Max)</td>
                <td>${metrics.lossStreak} trades</td>
              </tr>
              <tr>
                <td>Avg Hold (Winners)</td>
                <td>${fx(metrics.avgHoldWinners, 1)} days</td>
                <td>Avg Hold (Losers)</td>
                <td>${fx(metrics.avgHoldLosers, 1)} days</td>
              </tr>
              <tr>
                <td>Trade Frequency</td>
                <td>${fx(metrics.tradeFrequency, 1)} per week</td>
                <td>Capital Efficiency</td>
                <td>${formatPercent(metrics.capitalEfficiency)}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </body>
    </html>
  `;

  const printWindow = window.open('', '_blank');
  printWindow.document.write(reportHTML);
  printWindow.document.close();
  setTimeout(() => {
    printWindow.print();
  }, 250);
}

// "Not enough trades" (analytics.md §Page States), shared by the Summary and
// Analytics sections of the Performance page (performance.md v1.1 §6).
export function NotEnoughTrades({ minTrades, tradeCount }) {
  return (
    <DataState
      empty
      emptyIcon={<BarChart2 className="w-10 h-10 text-slate-600" />}
      emptyHeading="Not enough trades"
      emptyBody={`Need at least ${minTrades} closed trades to show analytics. You currently have ${tradeCount} trade${tradeCount !== 1 ? 's' : ''} in the selected period.`}
      emptyAction={<EmptyStateAction variant="button" to="/TradeEntry">Enter Your First Position</EmptyStateAction>}
      className="min-h-[240px]"
    />
  );
}

// Performance → Analytics section (performance.md v1.1 §4; ST-06, BLG-FE-259,
// EPIC-02, v9.17). The former Analytics page body less the KPIs whose home is
// Summary (Profit Factor, Expectancy, Key Insights) and Compliance (§17, §19,
// §21). Period-level KPIs come from GET /analytics/metrics (`metrics`, via
// toMetricsProps); the browser recomputation (calculateMetrics) is removed
// (§5.2). The charts and tables below still group the period's closed trades
// from GET /trades: they are scoped breakdowns, not period-level KPIs.
export default function AnalyticsSection({ trades = [], tradeCount, minTrades, periodLabel, metrics, summaryMetrics, hasEnoughData, metricsLoading = false, metricsError = false, onRetry }) {
  // The charts and tables group the period's closed trades from the same
  // GET /analytics/metrics response (trades_for_charts), so they cover exactly
  // the server's period window, like the KPIs (review finding, ST-06).
  const filteredTrades = trades;

  // Monthly data
  const getMonthlyData = () => {
    const monthlyMap = {};
    filteredTrades.forEach(t => {
      const monthKey = t.exit_date.substring(0, 7);
      if (!monthlyMap[monthKey]) {
        monthlyMap[monthKey] = { pnl: 0, trades: 0, wins: 0 };
      }
      monthlyMap[monthKey].pnl += t.pnl;
      monthlyMap[monthKey].trades += 1;
      if (t.pnl > 0) monthlyMap[monthKey].wins += 1;
    });

    return Object.entries(monthlyMap)
      .map(([month, data]) => ({
        month,
        pnl: data.pnl,
        trades: data.trades,
        winRate: ((data.wins / data.trades) * 100).toFixed(0),
        cumulative: 0
      }))
      .sort((a, b) => a.month.localeCompare(b.month))
      .slice(-12)
      .map((item, idx, arr) => ({
        ...item,
        cumulative: arr.slice(0, idx + 1).reduce((sum, m) => sum + m.pnl, 0)
      }));
  };

  // Market comparison
  const getMarketMetrics = (market) => {
    const marketTrades = filteredTrades.filter(t => t.market === market);
    const winners = marketTrades.filter(t => t.pnl > 0);
    const losers = marketTrades.filter(t => t.pnl < 0);
    const avgWin = winners.length > 0 ? winners.reduce((s, t) => s + t.pnl, 0) / winners.length : 0;
    const avgLoss = losers.length > 0 ? losers.reduce((s, t) => s + t.pnl, 0) / losers.length : 0;
    const sorted = [...marketTrades].sort((a, b) => b.pnl - a.pnl);

    return {
      totalTrades: marketTrades.length,
      winRate: ((winners.length / marketTrades.length) * 100).toFixed(1),
      totalPnl: marketTrades.reduce((s, t) => s + t.pnl, 0),
      avgWin,
      avgLoss,
      bestPerformer: sorted[0] || { ticker: "N/A", pnl: 0 },
      worstPerformer: sorted[sorted.length - 1] || { ticker: "N/A", pnl: 0 }
    };
  };

  // Exit reason data
  const getExitReasonData = () => {
    const reasonMap = {};
    filteredTrades.forEach(t => {
      // Legacy spellings group with their stored value; null reads as Manual Exit.
      const reason = exitReasonGroupKey(t.exit_reason);
      if (!reasonMap[reason]) {
        reasonMap[reason] = { count: 0, wins: 0, totalPnl: 0 };
      }
      reasonMap[reason].count += 1;
      reasonMap[reason].totalPnl += t.pnl;
      if (t.pnl > 0) reasonMap[reason].wins += 1;
    });

    return Object.entries(reasonMap).map(([reason, data]) => ({
      reason: exitReasonLabel(reason),
      count: data.count,
      winRate: (data.wins / data.count) * 100,
      totalPnl: data.totalPnl,
      avgPnl: data.totalPnl / data.count,
      percentage: (data.count / filteredTrades.length) * 100
    }));
  };

  // Day of week data
  const getDayOfWeekData = () => {
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
    const dayMap = days.reduce((acc, day) => ({ ...acc, [day]: { pnl: 0, trades: 0 } }), {});

    filteredTrades.forEach(t => {
      const dayOfWeek = new Date(t.exit_date).getDay();
      const dayName = days[dayOfWeek === 0 ? 6 : dayOfWeek - 1];
      if (dayMap[dayName]) {
        dayMap[dayName].pnl += t.pnl;
        dayMap[dayName].trades += 1;
      }
    });

    return days.map(day => ({
      day,
      avgPnl: dayMap[day].trades > 0 ? dayMap[day].pnl / dayMap[day].trades : 0,
      trades: dayMap[day].trades
    }));
  };

  // Holding period data
  const getHoldingPeriodData = () => {
    const buckets = [
      { label: "1-5 days", min: 1, max: 5 },
      { label: "6-10 days", min: 6, max: 10 },
      { label: "11-20 days", min: 11, max: 20 },
      { label: "21-30 days", min: 21, max: 30 },
      { label: "31+ days", min: 31, max: 9999 }
    ];

    return buckets.map(bucket => {
      const trades = filteredTrades.filter(t => {
        const days = (new Date(t.exit_date) - new Date(t.entry_date)) / (1000 * 60 * 60 * 24);
        return days >= bucket.min && days <= bucket.max;
      });
      const wins = trades.filter(t => t.pnl > 0);
      return {
        period: bucket.label,
        avgPnl: trades.length > 0 ? trades.reduce((s, t) => s + t.pnl, 0) / trades.length : 0,
        trades: trades.length,
        winRate: trades.length > 0 ? ((wins.length / trades.length) * 100).toFixed(0) : 0
      };
    });
  };

  // Entry/Exit scatter data
  const getEntryExitData = () => {
    return filteredTrades.map(t => ({
      entryPrice: t.entry_price,
      pnl: t.pnl,
      market: t.market,
      ticker: t.ticker
    }));
  };

  // Top performers
  const getTopPerformers = () => {
    const sorted = [...filteredTrades].sort((a, b) => b.pnl - a.pnl);
    const topWinners = sorted.slice(0, 5).map(t => ({
      ticker: t.ticker,
      entryDate: t.entry_date,
      pnl: t.pnl,
      pnlPercent: t.pnl_percent || 0,
      daysHeld: Math.round((new Date(t.exit_date) - new Date(t.entry_date)) / (1000 * 60 * 60 * 24)),
      exitReason: exitReasonLabel(exitReasonGroupKey(t.exit_reason))
    }));
    const topLosers = sorted.slice(-5).reverse().map(t => ({
      ticker: t.ticker,
      entryDate: t.entry_date,
      pnl: t.pnl,
      pnlPercent: t.pnl_percent || 0,
      daysHeld: Math.round((new Date(t.exit_date) - new Date(t.entry_date)) / (1000 * 60 * 60 * 24)),
      exitReason: exitReasonLabel(exitReasonGroupKey(t.exit_reason))
    }));
    return { topWinners, topLosers };
  };

  // Consistency metrics

  if (metricsLoading || metricsError) {
    return <DataState loading={metricsLoading} error={metricsError} onRetry={onRetry} className="min-h-[240px]" />;
  }

  if (!hasEnoughData || !metrics) {
    return <NotEnoughTrades minTrades={minTrades} tradeCount={tradeCount ?? 0} />;
  }

  return (
    <div className="space-y-6">
      <ExecutiveSummaryCards metrics={metrics} advancedMetrics={metrics} />
      <AdvancedMetricsGrid metrics={metrics} />
      <PerformanceSummary metrics={summaryMetrics} period={periodLabel} />
      <MonthlyHeatmap monthlyData={getMonthlyData()} trades={filteredTrades} />
      <UnderwaterChart trades={filteredTrades} />
      <MarketComparison
        ukMetrics={getMarketMetrics("UK")}
        usMetrics={getMarketMetrics("US")}
      />
      <ExitReasonTable exitReasonData={getExitReasonData()} />
      <TimeBasedCharts
        dayOfWeekData={getDayOfWeekData()}
        monthlyData={getMonthlyData()}
        holdingPeriodData={getHoldingPeriodData()}
        entryExitData={getEntryExitData()}
      />
      <RMultipleAnalysis trades={filteredTrades} />
      <RMultipleDistribution />
      <WinRateByMonth monthlyData={getMonthlyData()} />
      <TopPerformers {...getTopPerformers()} />
      <BestWorstTrades trades={filteredTrades} />
      <ConsistencyMetrics metrics={metrics} />
      {/* §14a Trade Plan Tag Filter — ST-05 (v6.8, BLG-FEAT-52). */}
      <TradePlanTagFilter />
      <TagPerformance trades={filteredTrades} />
      <CohortAnalysis />
      {/* Component 18 — Market Correlation (analytics.md §18). */}
      <MarketCorrelationSection />
    </div>
  );
}
