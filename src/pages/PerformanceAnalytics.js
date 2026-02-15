import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import PageHeader from "../components/ui/PageHeader";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { AlertCircle, Loader2, Download } from "lucide-react";
import { Button } from "../components/ui/button";
import ExecutiveSummaryCards from "../components/analytics/ExecutiveSummaryCards";
import KeyInsightsCard from "../components/analytics/KeyInsightsCard";
import AdvancedMetricsGrid from "../components/analytics/AdvancedMetricsGrid";
import MonthlyHeatmap from "../components/analytics/MonthlyHeatmap";
import MarketComparison from "../components/analytics/MarketComparison";
import ExitReasonTable from "../components/analytics/ExitReasonTable";
import TimeBasedCharts from "../components/analytics/TimeBasedCharts";
import TopPerformers from "../components/analytics/TopPerformers";
import ConsistencyMetrics from "../components/analytics/ConsistencyMetrics";
import TagPerformance from "../components/analytics/TagPerformance";
import UnderwaterChart from "../components/analytics/UnderwaterChart";
import RMultipleAnalysis from "../components/analytics/RMultipleAnalysis";

export default function PerformanceAnalytics() {
  const [timePeriod, setTimePeriod] = useState("last_month");

  // ✅ PRODUCTION-SAFE: Use environment variable for API URL
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const timePeriodLabels = {
    last_7_days: "Last 7 Days",
    last_month: "Last Month", 
    last_quarter: "Last Quarter",
    last_year: "Last Year",
    ytd: "Year to Date",
    all_time: "All Time"
  };

  const { data: settings } = useQuery({
    queryKey: ["settings"],
    queryFn: () => base44.entities.Settings.list(),
    initialData: [],
  });

  // ✅ PRODUCTION-SAFE: Query /trades endpoint with environment-aware URL
  const { data: tradesData, isLoading } = useQuery({
    queryKey: ["trades"],
    queryFn: async () => {
      try {
        const response = await fetch(`${API_URL}/trades`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const result = await response.json();
        return result.data;
      } catch (error) {
        console.error('Failed to load trades:', error);
        return { trades: [] };
      }
    },
    initialData: { trades: [] },
  });

  // ✅ Step 1: Use Portfolio History (for correct Sharpe)
  const { data: portfolioHistory } = useQuery({
    queryKey: ["portfolioHistory"],
    queryFn: async () => {
      try {
        const response = await fetch(`${API_URL}/portfolio/history?days=365`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const result = await response.json();
        return result.data || [];
      } catch (error) {
        console.error("Failed to load portfolio history:", error);
        return [];
      }
    },
    initialData: [],
  });

  const settingsData = settings?.[0] || { min_trades_for_analytics: 10 };
  const closedTrades = tradesData?.trades || [];

  // Filter by time period
  const getFilteredTrades = () => {
    const now = new Date();
    let startDate = new Date(0);

    switch (timePeriod) {
      case "last_7_days":
        startDate = new Date(now);
        startDate.setDate(startDate.getDate() - 7);
        break;
      case "last_month":
        startDate = new Date(now);
        startDate.setMonth(startDate.getMonth() - 1);
        break;
      case "last_quarter":
        startDate = new Date(now);
        startDate.setMonth(startDate.getMonth() - 3);
        break;
      case "last_year":
        startDate = new Date(now);
        startDate.setFullYear(startDate.getFullYear() - 1);
        break;
      case "ytd":
        startDate = new Date(now.getFullYear(), 0, 1);
        break;
      default:
        return closedTrades;
    }

    return closedTrades.filter(t => new Date(t.exit_date) >= startDate);
  };

  const filteredTrades = getFilteredTrades();
  const hasEnoughTrades = filteredTrades.length >= settingsData.min_trades_for_analytics;

  // Calculate metrics
  const calculateMetrics = () => {
    if (!hasEnoughTrades) return null;

  // ✅ Chronologically sorted trades (oldest → newest by exit date)
    const sortedTrades = [...filteredTrades].sort(
    (a, b) => new Date(a.exit_date) - new Date(b.exit_date)
    );

    const winners = filteredTrades.filter(t => t.pnl > 0);
    const losers = filteredTrades.filter(t => t.pnl < 0);
    const winRate = (winners.length / filteredTrades.length) * 100;
    const avgWin = winners.reduce((sum, t) => sum + t.pnl, 0) / (winners.length || 1);
    const avgLoss = losers.reduce((sum, t) => sum + t.pnl, 0) / (losers.length || 1);
    const grossProfit = winners.reduce((sum, t) => sum + t.pnl, 0);
    const grossLoss = Math.abs(losers.reduce((sum, t) => sum + t.pnl, 0));

    // ✅ Step 4: Fallback for No History (time-weighted trade returns)
    const calculateTradeSharpe = () => {
      if (filteredTrades.length < 10) return 0;

      const weightedReturns = filteredTrades
        .map(t => {
          const holdDays = Math.max(
            1,
            (new Date(t.exit_date) - new Date(t.entry_date)) / (1000 * 60 * 60 * 24)
          );

          const pnlPercent = Number(t.pnl_percent);
          if (!Number.isFinite(pnlPercent)) return null;

          // Annualize return for this holding period
          return (pnlPercent / holdDays) * 252;
        })
        .filter(r => Number.isFinite(r));

      if (weightedReturns.length < 2) return 0;

      const avgReturn = weightedReturns.reduce((a, b) => a + b, 0) / weightedReturns.length;
      const stdDev = Math.sqrt(
        weightedReturns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / weightedReturns.length
      );

      // Already annualized, no √252
      return stdDev > 0 ? avgReturn / stdDev : 0;
    };

    // ✅ Step 2 + 3 + 5: Correct Sharpe using DAILY portfolio returns (with method tracking)
    let sharpeRatio = 0;
    let sharpeMethod = portfolioHistory.length >= 30 ? "portfolio" : "trade";

    if (portfolioHistory.length >= 30) {
      // ✅ Sort by date chronologically
      const sorted = [...portfolioHistory].sort((a, b) =>
        new Date(a.snapshot_date) - new Date(b.snapshot_date)
      );

      // ✅ Calculate daily returns
      const dailyReturns = [];
      for (let i = 1; i < sorted.length; i++) {
        const prevValue = parseFloat(sorted[i - 1].total_value);
        const currValue = parseFloat(sorted[i].total_value);

        if (prevValue > 0 && Number.isFinite(prevValue) && Number.isFinite(currValue)) {
          const dailyReturn = ((currValue - prevValue) / prevValue) * 100;
          dailyReturns.push(dailyReturn);
        }
      }

      if (dailyReturns.length >= 2) {
        // ✅ Average daily return
        const avgDailyReturn =
          dailyReturns.reduce((a, b) => a + b, 0) / dailyReturns.length;

        // ✅ Standard deviation of daily returns
        const variance =
          dailyReturns.reduce((sum, r) => sum + Math.pow(r - avgDailyReturn, 2), 0) /
          dailyReturns.length;

        const stdDev = Math.sqrt(variance);

        // ✅ Annualize with √252 (now correct because we have DAILY returns)
        sharpeRatio = stdDev > 0 ? (avgDailyReturn / stdDev) * Math.sqrt(252) : 0;
        sharpeMethod = "portfolio";
      } else {
        // If portfolio history exists but daily returns are unusable, fallback
        sharpeRatio = calculateTradeSharpe();
        sharpeMethod = "trade";
      }
    } else {
      sharpeRatio = calculateTradeSharpe();
      sharpeMethod = "trade";
    }

    // Max Drawdown
    let peak = 0;
    let maxDrawdown = 0;
    let maxDrawdownDate = "";
    let cumPnl = 0;
    sortedTrades.forEach(t => {
      cumPnl += t.pnl;
      if (cumPnl > peak) peak = cumPnl;
      const drawdown = peak - cumPnl;
      if (drawdown > maxDrawdown) {
        maxDrawdown = drawdown;
        maxDrawdownDate = t.exit_date;
      }
    });
    const maxDrawdownPercent = peak > 0 ? (maxDrawdown / peak) * 100 : 0;

    const totalPnl = filteredTrades.reduce((sum, t) => sum + t.pnl, 0);
    const recoveryFactor = maxDrawdown > 0 ? totalPnl / maxDrawdown : 0;
    const expectancy = (winRate / 100 * avgWin) + ((100 - winRate) / 100 * avgLoss);
    const profitFactor = grossLoss > 0 ? grossProfit / grossLoss : 0;
    const riskRewardRatio = Math.abs(avgLoss) > 0 ? avgWin / Math.abs(avgLoss) : 0;

    // Win/Loss Streaks
    let currentStreak = 0;
    let maxWinStreak = 0;
    let maxLossStreak = 0;
    sortedTrades.forEach(t => {
      if (t.pnl > 0) {
        currentStreak = currentStreak > 0 ? currentStreak + 1 : 1;
        maxWinStreak = Math.max(maxWinStreak, currentStreak);
      } else {
        currentStreak = currentStreak < 0 ? currentStreak - 1 : -1;
        maxLossStreak = Math.max(maxLossStreak, Math.abs(currentStreak));
      }
    });

    // Holding time
    const winnersWithDays = winners.filter(t => t.entry_date && t.exit_date);
    const losersWithDays = losers.filter(t => t.entry_date && t.exit_date);
    const avgHoldWinners = winnersWithDays.length > 0
      ? winnersWithDays.reduce((sum, t) => {
          const days = (new Date(t.exit_date) - new Date(t.entry_date)) / (1000 * 60 * 60 * 24);
          return sum + days;
        }, 0) / winnersWithDays.length
      : 0;
    const avgHoldLosers = losersWithDays.length > 0
      ? losersWithDays.reduce((sum, t) => {
          const days = (new Date(t.exit_date) - new Date(t.entry_date)) / (1000 * 60 * 60 * 24);
          return sum + days;
        }, 0) / losersWithDays.length
      : 0;

    // Trade frequency (per week)
    const firstTrade = sortedTrades[0];
    const lastTrade = sortedTrades[sortedTrades.length - 1];
    const daySpan = firstTrade && lastTrade
      ? (new Date(lastTrade.exit_date) - new Date(firstTrade.entry_date)) / (1000 * 60 * 60 * 24)
      : 0;
    const tradeFrequency = daySpan > 0 ? (filteredTrades.length / daySpan) * 7 : 0;

    // Capital efficiency (simplified - assuming average position size)
    const avgPositionSize = filteredTrades.reduce((sum, t) => sum + (t.entry_price * t.shares), 0) / filteredTrades.length;
    const capitalEfficiency = avgPositionSize > 0 ? (totalPnl / avgPositionSize) * 100 : 0;

    // ✅ NEW: Calculate time underwater
    let runningEquity = 0;
    let peakEquity = 0;
    let peakDate = null;
    let daysUnderwater = 0;
    
    sortedTrades.forEach(trade => {
      runningEquity += trade.pnl;
    
      if (runningEquity >= peakEquity) {
        peakEquity = runningEquity;
        peakDate = trade.exit_date;
        daysUnderwater = 0;
      } else if (peakDate) {
        const daysSincePeak = Math.floor(
          (new Date(trade.exit_date) - new Date(peakDate)) / (1000 * 60 * 60 * 24)
        );
        daysUnderwater = Math.max(daysUnderwater, daysSincePeak);
      }
    });

    return {
      sharpeRatio,
      sharpeMethod,
      maxDrawdown: { percent: maxDrawdownPercent, amount: maxDrawdown, date: maxDrawdownDate },
      recoveryFactor,
      expectancy,
      profitFactor,
      riskRewardRatio,
      winStreak: maxWinStreak,
      lossStreak: maxLossStreak,
      avgHoldWinners,
      avgHoldLosers,
      tradeFrequency,
      capitalEfficiency,
      daysUnderwater,
      peakEquity,
      peakDate
    };
  };

  const metrics = calculateMetrics();

  const generatePrintReport = () => {
    if (!metrics) return;

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
          <div class="subtitle">Generated ${new Date().toLocaleDateString()} • Period: ${timePeriodLabels[timePeriod]} • ${filteredTrades.length} Trades</div>
          
          <div class="section">
            <div class="section-title">Executive Summary</div>
            <div class="metric-grid">
              <div class="metric-card">
                <div class="metric-label">Sharpe Ratio</div>
                <div class="metric-value">${metrics.sharpeRatio.toFixed(2)}</div>
                <div class="metric-subtitle">Risk-Adjusted Returns</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Max Drawdown</div>
                <div class="metric-value negative">${metrics.maxDrawdown.percent.toFixed(1)}%</div>
                <div class="metric-subtitle">£${metrics.maxDrawdown.amount.toFixed(0)}</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Recovery Factor</div>
                <div class="metric-value">${metrics.recoveryFactor.toFixed(2)}</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Expectancy</div>
                <div class="metric-value ${metrics.expectancy >= 0 ? 'positive' : 'negative'}">£${metrics.expectancy.toFixed(2)}</div>
                <div class="metric-subtitle">Per Trade</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Profit Factor</div>
                <div class="metric-value">${metrics.profitFactor.toFixed(2)}</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Risk/Reward</div>
                <div class="metric-value">${metrics.riskRewardRatio.toFixed(2)}:1</div>
              </div>
            </div>
          </div>

          <div class="section">
            <div class="section-title">Key Insights</div>
            <ul class="insight-list">
              ${metrics.sharpeRatio > 2 ? `<li class="insight-item">Excellent risk-adjusted returns with a Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)}</li>` : 
                metrics.sharpeRatio > 1 ? `<li class="insight-item">Strong risk-adjusted returns with a Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)}</li>` :
                `<li class="insight-item">Risk-adjusted returns need improvement (Sharpe: ${metrics.sharpeRatio.toFixed(2)})</li>`}
              ${metrics.avgHoldWinners > metrics.avgHoldLosers ? 
                `<li class="insight-item">✅ Great discipline - cutting losers faster (${metrics.avgHoldLosers.toFixed(1)} days) than letting winners run (${metrics.avgHoldWinners.toFixed(1)} days)</li>` :
                `<li class="insight-item">⚠️ Holding losers too long (${metrics.avgHoldLosers.toFixed(1)} days) compared to winners (${metrics.avgHoldWinners.toFixed(1)} days)</li>`}
              ${metrics.profitFactor > 2 ? `<li class="insight-item">Excellent profit factor of ${metrics.profitFactor.toFixed(2)} means earning £${metrics.profitFactor.toFixed(2)} for every £1 lost</li>` :
                `<li class="insight-item">Profit factor of ${metrics.profitFactor.toFixed(2)} - earning £${metrics.profitFactor.toFixed(2)} per £1 lost</li>`}
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
                  <td>${metrics.avgHoldWinners.toFixed(1)} days</td>
                  <td>Avg Hold (Losers)</td>
                  <td>${metrics.avgHoldLosers.toFixed(1)} days</td>
                </tr>
                <tr>
                  <td>Trade Frequency</td>
                  <td>${metrics.tradeFrequency.toFixed(1)} per week</td>
                  <td>Capital Efficiency</td>
                  <td>${metrics.capitalEfficiency.toFixed(1)}%</td>
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
  };

  if (isLoading) {
    return (
      <div>
        <PageHeader
          title="Performance Analytics"
          description="Deep dive into your trading performance and strategy effectiveness"
        />
        <div className="flex items-center justify-center min-h-[400px]">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      </div>
    );
  }

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
      const reason = t.exit_reason || "manual";
      if (!reasonMap[reason]) {
        reasonMap[reason] = { count: 0, wins: 0, totalPnl: 0 };
      }
      reasonMap[reason].count += 1;
      reasonMap[reason].totalPnl += t.pnl;
      if (t.pnl > 0) reasonMap[reason].wins += 1;
    });

    const reasonLabels = {
      stop_hit: "Stop Loss Hit",
      manual: "Manual Exit",
      target: "Target Reached",
      market_regime: "Risk-Off Signal"
    };

    return Object.entries(reasonMap).map(([reason, data]) => ({
      reason: reasonLabels[reason] || reason,
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
      exitReason: t.exit_reason || "manual"
    }));
    const topLosers = sorted.slice(-5).reverse().map(t => ({
      ticker: t.ticker,
      entryDate: t.entry_date,
      pnl: t.pnl,
      pnlPercent: t.pnl_percent || 0,
      daysHeld: Math.round((new Date(t.exit_date) - new Date(t.entry_date)) / (1000 * 60 * 60 * 24)),
      exitReason: t.exit_reason || "manual"
    }));
    return { topWinners, topLosers };
  };

  // Consistency metrics
  const getConsistencyMetrics = () => {
    const monthlyData = getMonthlyData();
    const profitableMonths = monthlyData.filter(m => m.pnl > 0);
    
    let consecutiveProfitable = 0;
    let currentStreak = 0;
    monthlyData.forEach(m => {
      if (m.pnl > 0) {
        currentStreak++;
        consecutiveProfitable = Math.max(consecutiveProfitable, currentStreak);
      } else {
        currentStreak = 0;
      }
    });

    const winRates = monthlyData.map(m => parseFloat(m.winRate));
    const avgWinRate = winRates.reduce((a, b) => a + b, 0) / winRates.length;
    const winRateStdDev = Math.sqrt(winRates.reduce((sum, wr) => sum + Math.pow(wr - avgWinRate, 2), 0) / winRates.length);

    const pnls = monthlyData.map(m => m.pnl);
    const avgPnl = pnls.reduce((a, b) => a + b, 0) / pnls.length;
    const pnlStdDev = Math.sqrt(pnls.reduce((sum, p) => sum + Math.pow(p - avgPnl, 2), 0) / pnls.length);

    return {
      consecutiveProfitableMonths: consecutiveProfitable,
      currentStreak,
      winRateStdDev,
      pnlStdDev
    };
  };

  if (!hasEnoughTrades) {
    return (
      <div>
        <PageHeader
          title="Performance Analytics"
          description="Deep dive into your trading performance and strategy effectiveness"
          actions={
            <div className="flex gap-2">
              <Select value={timePeriod} onValueChange={setTimePeriod}>
                <SelectTrigger className="w-48 bg-slate-800/50 border-slate-700 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="last_7_days">Last 7 Days</SelectItem>
                  <SelectItem value="last_month">Last Month</SelectItem>
                  <SelectItem value="last_quarter">Last Quarter</SelectItem>
                  <SelectItem value="last_year">Last Year</SelectItem>
                  <SelectItem value="ytd">Year to Date</SelectItem>
                  <SelectItem value="all_time">All Time</SelectItem>
                </SelectContent>
              </Select>
              <Button
                onClick={generatePrintReport}
                variant="outline"
                className="bg-slate-800/50 border-slate-700 text-white hover:bg-slate-700"
                disabled
              >
                <Download className="w-4 h-4 mr-2" />
                Export PDF
              </Button>
            </div>
          }
        />
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <div className="p-4 rounded-full bg-slate-800/50 border border-slate-700">
                <AlertCircle className="w-12 h-12 text-slate-500" />
              </div>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Not Enough Data</h3>
            <p className="text-slate-400 max-w-md">
              Need at least {settingsData.min_trades_for_analytics} closed trades to show analytics.
              You currently have {filteredTrades.length} trade{filteredTrades.length !== 1 ? 's' : ''} in the selected period.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Performance Analytics"
        description="Deep dive into your trading performance and strategy effectiveness"
        actions={
          <div className="flex gap-2">
            <Select value={timePeriod} onValueChange={setTimePeriod}>
              <SelectTrigger className="w-48 bg-slate-800/50 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="last_7_days">Last 7 Days</SelectItem>
                <SelectItem value="last_month">Last Month</SelectItem>
                <SelectItem value="last_quarter">Last Quarter</SelectItem>
                <SelectItem value="last_year">Last Year</SelectItem>
                <SelectItem value="ytd">Year to Date</SelectItem>
                <SelectItem value="all_time">All Time</SelectItem>
              </SelectContent>
            </Select>
            <Button
              onClick={generatePrintReport}
              variant="outline"
              className="bg-slate-800/50 border-slate-700 text-white hover:bg-slate-700"
            >
              <Download className="w-4 h-4 mr-2" />
              Export PDF
            </Button>
          </div>
        }
      />

      <ExecutiveSummaryCards metrics={metrics} />
      <KeyInsightsCard 
        metrics={metrics} 
        winRate={hasEnoughTrades ? (filteredTrades.filter(t => t.pnl > 0).length / filteredTrades.length) * 100 : 0} 
      />
      <AdvancedMetricsGrid metrics={metrics} />
      <MonthlyHeatmap monthlyData={getMonthlyData()} />
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
      <TopPerformers {...getTopPerformers()} />
      <ConsistencyMetrics metrics={getConsistencyMetrics()} />
      <TagPerformance trades={filteredTrades} />
    </div>
  );
}
