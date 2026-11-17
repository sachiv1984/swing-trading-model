import { useCallback, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useIsFetching, useQuery } from "@tanstack/react-query";
import { Download, TrendingUp, TrendingDown, Minus, PieChart, BarChart3, FileText, Zap } from "lucide-react";
import { api, base44 } from "../api/base44Client";
import PageHeader from "../components/ui/PageHeader";
import DataState from "../components/ui/DataState";
import StatsCard from "../components/ui/StatsCard";
import { Button } from "../components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../components/ui/tabs";
import SectionIndex, { SECTION_SCROLL_MARGIN } from "../components/ui/SectionIndex";
import MetricsStalenessIndicator from "../components/analytics/MetricsStalenessIndicator";
import KeyInsightsCard from "../components/analytics/KeyInsightsCard";
import DisciplineComplianceSection from "../components/analytics/DisciplineComplianceSection";
import Arc5ComplianceSection from "../components/analytics/Arc5ComplianceSection";
import TradePlanCompletionRateSection from "../components/analytics/TradePlanCompletionRateSection";
import PortfolioGrowthChart from "../components/reports/PortfolioGrowthChart";
import ExportModal from "../components/reports/ExportModal";
import { TaxYearReport, MonthlyPnlTable, ReconciliationReport } from "../components/performance/ReportViews";
import AnalyticsSection, { NotEnoughTrades, generatePerformancePrintReport } from "../components/performance/AnalyticsSection";
import Last30DaysCompliance from "../components/performance/Last30DaysCompliance";
import { PAGE_LABELS } from "../lib/pageLabels";
import { formatCurrency, formatPercent } from "../lib/format";
import { toMetricsProps, toSummary } from "../lib/performanceMetrics";

// Performance (performance.md v1.2; ST-06, BLG-FE-259, EPIC-02, v9.17): one
// page for Reports and Analytics. Sections Summary · Reports · Analytics ·
// Compliance with the shared section index (?section=). ?period= drives
// Summary, Analytics and Discipline & Compliance; ?report= picks the Reports
// view. Every period-level KPI has one home (§5) and is read from
// GET /analytics/metrics (§5.2). No new AI call (§8).

const PERIODS = [
  { value: "last_7_days", label: "Last 7 Days" },
  { value: "last_month", label: "Last Month" },
  { value: "last_quarter", label: "Last Quarter" },
  { value: "last_year", label: "Last Year" },
  { value: "ytd", label: "Year to Date" },
  { value: "all_time", label: "All Time" },
];
const PERIOD_KEYS = PERIODS.map((p) => p.value);
const REPORT_VIEWS = [
  { value: "tax-year", label: "Tax year" },
  { value: "monthly", label: "Monthly" },
  { value: "reconciliation", label: "Reconciliation" },
];
const SECTIONS = [
  { id: "summary", label: "Summary" },
  { id: "reports", label: "Reports" },
  { id: "analytics", label: "Analytics" },
  { id: "compliance", label: "Compliance" },
];

function periodDatesFor(period) {
  const now = new Date();
  let start = new Date();
  switch (period) {
    case "last_7_days": start.setDate(now.getDate() - 7); break;
    case "last_quarter": start.setMonth(now.getMonth() - 3); break;
    case "last_year": start.setFullYear(now.getFullYear() - 1); break;
    case "ytd": start = new Date(now.getFullYear(), 0, 1); break;
    case "all_time": start = new Date(2020, 0, 1); break;
    default: start.setMonth(now.getMonth() - 1);
  }
  return { start, end: now };
}

function Section({ id, label, children }) {
  return (
    <section id={id} aria-labelledby={`perf-section-${id}`} className={`space-y-6 ${SECTION_SCROLL_MARGIN}`}>
      <h2
        id={`perf-section-${id}`}
        className="text-lg font-semibold text-app-fg border-b border-app-line pb-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500 rounded-sm"
      >
        {label}
      </h2>
      {children}
    </section>
  );
}

export default function Performance() {
  const [searchParams, setSearchParams] = useSearchParams();
  const period = PERIOD_KEYS.includes(searchParams.get("period")) ? searchParams.get("period") : "last_month";
  const reportView = REPORT_VIEWS.some((r) => r.value === searchParams.get("report")) ? searchParams.get("report") : "tax-year";
  const periodLabel = PERIODS.find((p) => p.value === period).label;
  const [monthlyInitialYear, setMonthlyInitialYear] = useState(null);
  const [exportOpen, setExportOpen] = useState(false);

  const setParam = useCallback(
    (key, value) =>
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev);
          next.set(key, value);
          return next;
        },
        { replace: true }
      ),
    [setSearchParams]
  );

  const { data: analyticsData, isLoading, isError, refetch } = useQuery({
    queryKey: ["analyticsMetrics", period],
    queryFn: () => api.analytics.metrics(period),
  });
  const { data: positions = [] } = useQuery({
    queryKey: ["positions"],
    queryFn: () => base44.entities.Position.list("-entry_date"),
  });
  const { data: settingsRaw } = useQuery({
    queryKey: ["settings"],
    queryFn: () => api.settings.list(),
    initialData: [],
  });
  // One minimum for both empty states: the server's own min_required, else the
  // settings value, else the default 10 (analytics_endpoints.md).
  const settingsMin = ((Array.isArray(settingsRaw) ? settingsRaw[0] : settingsRaw?.data?.[0]) || {}).min_trades_for_analytics;

  const summary = useMemo(() => toSummary(analyticsData), [analyticsData]);
  const minTrades = summary.minRequired ?? settingsMin ?? 10;
  const periodDates = useMemo(() => periodDatesFor(period), [period]);
  // ?section= jumps once nothing on the page is still loading, so sections
  // that fill in later (tax year, charts, compliance) do not move the target.
  const fetching = useIsFetching();
  const [pageSettled, setPageSettled] = useState(false);
  if (!pageSettled && !isLoading && fetching === 0) setPageSettled(true);
  const metrics = useMemo(() => (analyticsData ? toMetricsProps(analyticsData) : null), [analyticsData]);
  const openCount = Array.isArray(positions) ? positions.filter((p) => p.status === "open").length : 0;

  // Chart rows and Performance Summary / Export figures from the same
  // response's trades_for_charts, exactly as Reports computed them.
  const chartTrades = useMemo(
    () =>
      (analyticsData?.trades_for_charts || []).map((t) => ({
        ...t,
        status: "closed",
        pnl_percent: t.pnl_pct ?? t.pnl_percent,
        fees: t.fees ?? 0,
      })),
    [analyticsData]
  );
  const reportMetrics = useMemo(() => {
    const wins = chartTrades.filter((t) => (t.pnl || 0) > 0);
    const losses = chartTrades.filter((t) => (t.pnl || 0) < 0);
    const grossProfit = wins.reduce((s, t) => s + (t.pnl || 0), 0);
    const grossLoss = Math.abs(losses.reduce((s, t) => s + (t.pnl || 0), 0));
    return {
      totalPnL: summary.totalPnl ?? 0,
      winRate: summary.winRate ?? 0,
      totalTrades: summary.totalTrades ?? 0,
      winningTrades: wins.length,
      losingTrades: losses.length,
      grossProfit,
      grossLoss,
      avgWin: wins.length > 0 ? grossProfit / wins.length : 0,
      avgLoss: losses.length > 0 ? grossLoss / losses.length : 0,
      profitFactor: metrics?.profitFactor ?? 0,
      totalFees: chartTrades.reduce((s, t) => s + (t.fees || 0), 0),
      openPositions: openCount,
    };
  }, [chartTrades, summary, metrics, openCount]);

  const enough = !isLoading && !isError && summary.hasEnoughData && metrics;
  // W / L / even from the same rows, so the three add up to the trade count.
  const evenTrades = chartTrades.length - reportMetrics.winningTrades - reportMetrics.losingTrades;
  const winLossLabel = `${reportMetrics.winningTrades}W / ${reportMetrics.losingTrades}L${evenTrades > 0 ? ` / ${evenTrades} even` : ""}`;
  const totalPnl = summary.totalPnl ?? 0;

  return (
    <div className="space-y-6 min-w-0">
      <PageHeader
        title={PAGE_LABELS.Performance}
        description="How your closed trades performed, with tax-year reports and rule compliance."
        onward={{ label: PAGE_LABELS.TradeHistory, to: "/TradeHistory" }}
        actions={
          <div className="flex flex-col sm:flex-row gap-2" data-testid="performance-header-actions">
            <Select value={period} onValueChange={(v) => setParam("period", v)}>
              <SelectTrigger aria-label="Performance period" data-testid="performance-period" className="w-48 bg-app-raised border-app-line text-app-fg">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-app-raised border-app-line text-app-fg">
                {PERIODS.map((p) => (
                  <SelectItem key={p.value} value={p.value}>{p.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button
              data-testid="performance-export"
              onClick={() => setExportOpen(true)}
              className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white"
            >
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
            <Button
              onClick={() => generatePerformancePrintReport(metrics, periodLabel, summary.totalTrades)}
              variant="outline"
              disabled={!enough}
              className="bg-app-raised border-app-line text-app-fg hover:bg-app-surface"
            >
              <Download className="w-4 h-4 mr-2" />
              Export PDF
            </Button>
          </div>
        }
      />

      <MetricsStalenessIndicator />

      <div className="space-y-4 lg:space-y-0 lg:grid lg:grid-cols-[minmax(0,1fr)_12rem] lg:gap-6">
        <SectionIndex sections={SECTIONS} className="lg:order-2" ready={pageSettled} />
        <div className="lg:order-1 min-w-0 space-y-10">
          <Section id="summary" label="Summary">
            {isLoading || isError ? (
              <DataState loading={isLoading} error={isError} onRetry={refetch} className="min-h-[200px]" />
            ) : !(summary.totalTrades > 0) ? (
              // Zero trades in the period: only the empty state, so no "0.0%"
              // win rate is shown for a period with no trades (§6).
              <NotEnoughTrades minTrades={minTrades} tradeCount={0} />
            ) : (
              <>
                {/* BLG-FE-300 (performance.md v1.2 §6): Total P&L, Win Rate and Total
                    Trades always show — a sum, a percentage and a count need no
                    sample minimum. Profit Factor, Expectancy, the growth chart and
                    Key Insights wait for enough trades. Order per §4. */}
                <div
                  className={`grid grid-cols-1 gap-4 ${enough ? "sm:grid-cols-2 xl:grid-cols-5" : "sm:grid-cols-3"}`}
                  data-testid="performance-summary-cards"
                >
                  <StatsCard
                    title="Total P&L"
                    value={formatCurrency(totalPnl, { signed: true })}
                    subtitle={periodLabel}
                    icon={totalPnl > 0 ? TrendingUp : totalPnl < 0 ? TrendingDown : Minus}
                    gradient={totalPnl > 0 ? "emerald" : totalPnl < 0 ? "rose" : "cyan"}
                  />
                  <StatsCard
                    title="Win Rate"
                    value={formatPercent(summary.winRate)}
                    subtitle={winLossLabel}
                    icon={PieChart}
                    gradient="cyan"
                  />
                  <StatsCard
                    title="Total Trades"
                    value={String(summary.totalTrades ?? 0)}
                    subtitle={`${openCount} still open`}
                    icon={FileText}
                    gradient="fuchsia"
                  />
                  {enough && (
                    <>
                      <StatsCard
                        title="Profit Factor"
                        value={metrics.profitFactor == null ? "N/A" : metrics.profitFactor.toFixed(2)}
                        subtitle="Gross profit / gross loss"
                        icon={BarChart3}
                        gradient="violet"
                      />
                      <StatsCard
                        title="Expectancy"
                        value={metrics.expectancy == null ? "N/A" : formatCurrency(metrics.expectancy, { signed: true })}
                        subtitle="Edge per trade"
                        icon={Zap}
                        gradient={metrics.expectancy > 0 ? "emerald" : metrics.expectancy < 0 ? "rose" : "cyan"}
                      />
                    </>
                  )}
                </div>
                {enough ? (
                  <>
                    <PortfolioGrowthChart positions={chartTrades} period={period} periodDates={periodDates} />
                    <KeyInsightsCard metrics={metrics} winRate={summary.winRate ?? 0} />
                  </>
                ) : (
                  <NotEnoughTrades minTrades={minTrades} tradeCount={summary.totalTrades ?? 0} />
                )}
              </>
            )}
          </Section>

          <Section id="reports" label="Reports">
            <Tabs
              value={reportView}
              onValueChange={(v) => {
                // As on the old Reports page: choosing Monthly from the tabs opens the
                // current tax year; only the Tax year notice link carries a year across.
                if (v === "monthly") setMonthlyInitialYear(null);
                setParam("report", v);
              }}
              className="space-y-4"
            >
              <TabsList
                aria-label="Report"
                data-testid="performance-report-tabs"
                className="flex h-auto w-full max-w-full justify-start overflow-x-auto gap-1 rounded-xl border border-app-line bg-app-raised p-1 sm:w-auto sm:inline-flex"
              >
                {REPORT_VIEWS.map((r) => (
                  <TabsTrigger
                    key={r.value}
                    value={r.value}
                    data-testid={`performance-report-tab-${r.value}`}
                    className="shrink-0 rounded-lg px-3 py-1.5 text-app-muted hover:text-app-fg data-[state=active]:bg-app-surface data-[state=active]:text-app-fg focus-visible:ring-cyan-500 focus-visible:ring-offset-0"
                  >
                    {r.label}
                  </TabsTrigger>
                ))}
              </TabsList>
              <TabsContent value="tax-year" className="mt-0">
                <TaxYearReport
                  onViewMonthly={(year) => {
                    setMonthlyInitialYear(year);
                    setParam("report", "monthly");
                  }}
                />
              </TabsContent>
              <TabsContent value="monthly" className="mt-0">
                <MonthlyPnlTable initialYear={monthlyInitialYear} />
              </TabsContent>
              <TabsContent value="reconciliation" className="mt-0">
                <ReconciliationReport />
              </TabsContent>
            </Tabs>
          </Section>

          <Section id="analytics" label="Analytics">
            <AnalyticsSection
              trades={chartTrades}
              tradeCount={summary.totalTrades ?? 0}
              minTrades={minTrades}
              periodLabel={periodLabel}
              metrics={enough ? metrics : null}
              summaryMetrics={reportMetrics}
              hasEnoughData={summary.hasEnoughData}
              metricsLoading={isLoading}
              metricsError={isError}
              onRetry={refetch}
            />
          </Section>

          <Section id="compliance" label="Compliance">
            <DisciplineComplianceSection period={period} />
            <Arc5ComplianceSection />
            <Last30DaysCompliance />
            <TradePlanCompletionRateSection />
          </Section>
        </div>
      </div>

      <ExportModal
        open={exportOpen}
        onClose={() => setExportOpen(false)}
        positions={chartTrades}
        metrics={reportMetrics}
        period={periodLabel}
      />
    </div>
  );
}
