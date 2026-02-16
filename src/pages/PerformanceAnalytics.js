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
          <div class="subtitle">Generated ${new Date().toLocaleDateString()} • Period: ${timePeriodLabels[timePeriod]} • ${summary.total_trades} Trades</div>
          
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
              ${(metrics.avgHoldWinners || 0) > (metrics.avgHoldLosers || 0) ? 
                `<li class="insight-item">✅ Great discipline - cutting losers faster (${(metrics.avgHoldLosers || 0).toFixed(1)} days) than letting winners run (${(metrics.avgHoldWinners || 0).toFixed(1)} days)</li>` :
                `<li class="insight-item">⚠️ Holding losers too long (${(metrics.avgHoldLosers || 0).toFixed(1)} days) compared to winners (${(metrics.avgHoldWinners || 0).toFixed(1)} days)</li>`}
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
                  <td>${metrics.winStreak || 0} trades</td>
                  <td>Loss Streak (Max)</td>
                  <td>${metrics.lossStreak || 0} trades</td>
                </tr>
                <tr>
                  <td>Avg Hold (Winners)</td>
                  <td>${(metrics.avgHoldWinners || 0).toFixed(1)} days</td>
                  <td>Avg Hold (Losers)</td>
                  <td>${(metrics.avgHoldLosers || 0).toFixed(1)} days</td>
                </tr>
                <tr>
                  <td>Trade Frequency</td>
                  <td>${(metrics.tradeFrequency || 0).toFixed(1)} per week</td>
                  <td>Capital Efficiency</td>
                  <td>${(metrics.capitalEfficiency || 0).toFixed(1)}%</td>
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
              Need at least {summary.min_required} closed trades to show analytics.
              You currently have {summary.total_trades} trade{summary.total_trades !== 1 ? 's' : ''} in the selected period.
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
        winRate={summary.win_rate || 0} 
      />
      <AdvancedMetricsGrid metrics={advancedMetrics} />
      <MonthlyHeatmap monthlyData={analyticsData?.monthly_data || []} />
      <UnderwaterChart trades={analyticsData?.trades_for_charts || []} />
      <MarketComparison 
        ukMetrics={analyticsData?.market_comparison?.UK || {}} 
        usMetrics={analyticsData?.market_comparison?.US || {}} 
      />
      <ExitReasonTable exitReasonData={analyticsData?.exit_reasons || []} />
      <TimeBasedCharts
        dayOfWeekData={analyticsData?.day_of_week || []}
        monthlyData={analyticsData?.monthly_data || []}
        holdingPeriodData={analyticsData?.holding_periods || []}
        entryExitData={analyticsData?.entry_exit_scatter || []}
      />
      <RMultipleAnalysis trades={analyticsData?.trades_for_charts || []} />
      <TopPerformers 
        topWinners={analyticsData?.top_performers?.winners || []}
        topLosers={analyticsData?.top_performers?.losers || []}
      />
      <ConsistencyMetrics metrics={analyticsData?.consistency_metrics || {}} />
      <TagPerformance trades={analyticsData?.trades_for_charts || []} />
    </div>
  );
}
