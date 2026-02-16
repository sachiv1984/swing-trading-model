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

// ✅ NEW: Single API call replaces ALL calculations
const { data: analyticsData, isLoading: analyticsLoading } = useQuery({
  queryKey: ["analytics", timePeriod],
  queryFn: async () => {
    try {
      const response = await fetch(`${API_URL}/analytics/metrics?period=${timePeriod}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Failed to load analytics:', error);
      return null;
    }
  },
  enabled: true,
});

// ✅ Extract data from API response
const summary = analyticsData?.summary || { has_enough_data: false, total_trades: 0, min_required: 10 };
const metrics = analyticsData?.executive_metrics || {};
const advancedMetrics = analyticsData?.advanced_metrics || {};
const hasEnoughTrades = summary.has_enough_data;

  

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

  // Entry/Exit scatter data
  const getEntryExitData = () => {
    return filteredTrades.map(t => ({
      entryPrice: t.entry_price,
      pnl: t.pnl,
      market: t.market,
      ticker: t.ticker
    }));
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
