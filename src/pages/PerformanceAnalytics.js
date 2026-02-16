import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
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

// ✅ Helper to convert snake_case to camelCase recursively
const toCamelCase = (obj) => {
  if (Array.isArray(obj)) {
    return obj.map(v => toCamelCase(v));
  } else if (obj !== null && obj !== undefined && obj.constructor === Object) {
    return Object.keys(obj).reduce((result, key) => {
      const camelKey = key.replace(/_([a-z])/g, (g) => g[1].toUpperCase());
      result[camelKey] = toCamelCase(obj[key]);
      return result;
    }, {});
  }
  return obj;
};

export default function PerformanceAnalytics() {
  const [timePeriod, setTimePeriod] = useState("last_month");

  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const timePeriodLabels = {
    last_7_days: "Last 7 Days",
    last_month: "Last Month", 
    last_quarter: "Last Quarter",
    last_year: "Last Year",
    ytd: "Year to Date",
    all_time: "All Time"
  };

  // ✅ NEW: Single API call replaces ALL calculations
  const { data: analyticsData, isLoading: analyticsLoading, error: analyticsError } = useQuery({
    queryKey: ["analytics", timePeriod],
    queryFn: async () => {
      try {
        console.log('Fetching analytics from:', `${API_URL}/analytics/metrics?period=${timePeriod}`);
        const response = await fetch(`${API_URL}/analytics/metrics?period=${timePeriod}`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const result = await response.json();
        console.log('Analytics data received (raw):', result);
        
        // Transform snake_case to camelCase
        const camelData = toCamelCase(result.data);
        console.log('Analytics data (camelCase):', camelData);
        
        return camelData;
      } catch (error) {
        console.error('Failed to load analytics:', error);
        throw error;
      }
    },
    enabled: true,
    retry: 1,
  });

  // ✅ Extract data from API response with safe defaults
  const summary = analyticsData?.summary || { 
    hasEnoughData: false, 
    totalTrades: 0, 
    minRequired: 10,
    winRate: 0,
    totalPnl: 0
  };
  
  const metrics = analyticsData?.executiveMetrics || {
    sharpeRatio: 0,
    sharpeMethod: 'insufficient_data',
    maxDrawdown: { percent: 0, amount: 0, date: null },
    recoveryFactor: 0,
    expectancy: 0,
    profitFactor: 0,
    riskRewardRatio: 0
  };
  
  const advancedMetrics = analyticsData?.advancedMetrics || {
    winStreak: 0,
    lossStreak: 0,
    avgHoldWinners: 0,
    avgHoldLosers: 0,
    tradeFrequency: 0,
    capitalEfficiency: 0,
    daysUnderwater: 0
  };
  
  const hasEnoughTrades = summary.hasEnoughData;

  // Default structures for components
  const defaultMarketMetrics = {
    totalTrades: 0,
    winRate: 0,
    totalPnl: 0,
    avgWin: 0,
    avgLoss: 0,
    bestPerformer: { ticker: 'N/A', pnl: 0 },
    worstPerformer: { ticker: 'N/A', pnl: 0 }
  };

  console.log('Current state:', { 
    analyticsLoading, 
    analyticsError, 
    hasEnoughTrades, 
    summary, 
    metrics,
    advancedMetrics 
  });

  const generatePrintReport = () => {
    if (!metrics || !hasEnoughTrades) return;

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
          <div class="subtitle">Generated ${new Date().toLocaleDateString()} • Period: ${timePeriodLabels[timePeriod]} • ${summary.totalTrades} Trades</div>
          
          <div class="section">
            <div class="section-title">Executive Summary</div>
            <div class="metric-grid">
              <div class="metric-card">
                <div class="metric-label">Sharpe Ratio</div>
                <div class="metric-value">${(metrics.sharpeRatio || 0).toFixed(2)}</div>
                <div class="metric-subtitle">Risk-Adjusted Returns</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Max Drawdown</div>
                <div class="metric-value negative">${(metrics.maxDrawdown?.percent || 0).toFixed(1)}%</div>
                <div class="metric-subtitle">£${(metrics.maxDrawdown?.amount || 0).toFixed(0)}</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Recovery Factor</div>
                <div class="metric-value">${(metrics.recoveryFactor || 0).toFixed(2)}</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Expectancy</div>
                <div class="metric-value ${(metrics.expectancy || 0) >= 0 ? 'positive' : 'negative'}">£${(metrics.expectancy || 0).toFixed(2)}</div>
                <div class="metric-subtitle">Per Trade</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Profit Factor</div>
                <div class="metric-value">${(metrics.profitFactor || 0).toFixed(2)}</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">Risk/Reward</div>
                <div class="metric-value">${(metrics.riskRewardRatio || 0).toFixed(2)}:1</div>
              </div>
            </div>
          </div>

          <div class="section">
            <div class="section-title">Key Insights</div>
            <ul class="insight-list">
              ${(metrics.sharpeRatio || 0) > 2 ? `<li class="insight-item">Excellent risk-adjusted returns with a Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)}</li>` : 
                (metrics.sharpeRatio || 0) > 1 ? `<li class="insight-item">Strong risk-adjusted returns with a Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)}</li>` :
                `<li class="insight-item">Risk-adjusted returns need improvement (Sharpe: ${(metrics.sharpeRatio || 0).toFixed(2)})</li>`}
              ${(advancedMetrics.avgHoldWinners || 0) > (advancedMetrics.avgHoldLosers || 0) ? 
                `<li class="insight-item">✅ Great discipline - cutting losers faster (${(advancedMetrics.avgHoldLosers || 0).toFixed(1)} days) than letting winners run (${(advancedMetrics.avgHoldWinners || 0).toFixed(1)} days)</li>` :
                `<li class="insight-item">⚠️ Holding losers too long (${(advancedMetrics.avgHoldLosers || 0).toFixed(1)} days) compared to winners (${(advancedMetrics.avgHoldWinners || 0).toFixed(1)} days)</li>`}
              ${(metrics.profitFactor || 0) > 2 ? `<li class="insight-item">Excellent profit factor of ${metrics.profitFactor.toFixed(2)} means earning £${metrics.profitFactor.toFixed(2)} for every £1 lost</li>` :
                `<li class="insight-item">Profit factor of ${(metrics.profitFactor || 0).toFixed(2)} - earning £${(metrics.profitFactor || 0).toFixed(2)} per £1 lost</li>`}
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
                  <td>${advancedMetrics.winStreak || 0} trades</td>
                  <td>Loss Streak (Max)</td>
                  <td>${advancedMetrics.lossStreak || 0} trades</td>
                </tr>
                <tr>
                  <td>Avg Hold (Winners)</td>
                  <td>${(advancedMetrics.avgHoldWinners || 0).toFixed(1)} days</td>
                  <td>Avg Hold (Losers)</td>
                  <td>${(advancedMetrics.avgHoldLosers || 0).toFixed(1)} days</td>
                </tr>
                <tr>
                  <td>Trade Frequency</td>
                  <td>${(advancedMetrics.tradeFrequency || 0).toFixed(1)} per week</td>
                  <td>Capital Efficiency</td>
                  <td>${(advancedMetrics.capitalEfficiency || 0).toFixed(1)}%</td>
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

  // Show loading state
  if (analyticsLoading) {
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

  // Show error state
  if (analyticsError) {
    return (
      <div>
        <PageHeader
          title="Performance Analytics"
          description="Deep dive into your trading performance and strategy effectiveness"
        />
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <div className="p-4 rounded-full bg-red-900/20 border border-red-700">
                <AlertCircle className="w-12 h-12 text-red-500" />
              </div>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Failed to Load Analytics</h3>
            <p className="text-slate-400 max-w-md mb-4">
              {analyticsError.message || 'Unable to fetch analytics data'}
            </p>
            <p className="text-slate-500 text-sm">
              Check console for details. Is your backend running at {API_URL}?
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Show "not enough data" state
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
              Need at least {summary.minRequired} closed trades to show analytics.
              You currently have {summary.totalTrades} trade{summary.totalTrades !== 1 ? 's' : ''} in the selected period.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Main render - show analytics
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

      <ExecutiveSummaryCards metrics={metrics} advancedMetrics={advancedMetrics} />
      <KeyInsightsCard 
        metrics={metrics} 
        winRate={summary.winRate || 0} 
      />
      <AdvancedMetricsGrid metrics={advancedMetrics} executiveMetrics={metrics} />
      <MonthlyHeatmap monthlyData={analyticsData?.monthlyData || []} />
      <UnderwaterChart trades={analyticsData?.tradesForCharts || []} />
      <MarketComparison 
        ukMetrics={analyticsData?.marketComparison?.UK || defaultMarketMetrics} 
        usMetrics={analyticsData?.marketComparison?.US || defaultMarketMetrics} 
      />
      <ExitReasonTable exitReasonData={analyticsData?.exitReasons || []} />
      <TimeBasedCharts
        dayOfWeekData={analyticsData?.dayOfWeek || []}
        monthlyData={analyticsData?.monthlyData || []}
        holdingPeriodData={analyticsData?.holdingPeriods || []}
        entryExitData={analyticsData?.entryExitScatter || []}
      />
      <RMultipleAnalysis trades={analyticsData?.tradesForCharts || []} />
      <TopPerformers 
        topWinners={analyticsData?.topPerformers?.winners || []}
        topLosers={analyticsData?.topPerformers?.losers || []}
      />
      <ConsistencyMetrics metrics={analyticsData?.consistencyMetrics || {}} />
      <TagPerformance trades={analyticsData?.tradesForCharts || []} />
    </div>
  );
}
