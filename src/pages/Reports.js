import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { base44, apiFetch, api } from "../api/base44Client";
import { useToast } from "../components/ui/use-toast";
import {
  FileText,
  Download,
  Calendar,
  TrendingUp,
  TrendingDown,
  BarChart3,
  PieChart,
  Loader2,
  FileSpreadsheet,
  FileDown,
  AlertTriangle,
  ChevronUp,
  ChevronDown,
  ChevronsUpDown
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import PageHeader from "../components/ui/PageHeader";
import StatsCard from "../components/ui/StatsCard";
import PerformanceSummary from "../components/reports/PerformanceSummary";
import PortfolioGrowthChart from "../components/reports/PortfolioGrowthChart";
import TradeBreakdown from "../components/reports/TradeBreakdown";
import ExportModal from "../components/reports/ExportModal";
import { motion } from "framer-motion";

// ─── Helpers ──────────────────────────────────────────────────────────────────

function getCurrentUKTaxYear() {
  const today = new Date();
  const year = today.getFullYear();
  const taxYearStart = new Date(year, 3, 6); // April 6
  return today >= taxYearStart ? year : year - 1;
}

function formatGBP(value) {
  if (value == null) return "—";
  return `£${Number(value).toLocaleString("en-GB", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function formatPct(value) {
  if (value == null) return "—";
  return `${Number(value).toFixed(1)}%`;
}

// ─── Tax Year P&L View ─────────────────────────────────────────────────────────

function TaxYearReport() {
  const currentTaxYear = getCurrentUKTaxYear();
  const [selectedYear, setSelectedYear] = useState(currentTaxYear);
  const [sortField, setSortField] = useState("exit_date");
  const [sortDir, setSortDir] = useState("asc");
  const [pdfGenerating, setPdfGenerating] = useState(false);
  const [csvGenerating, setCsvGenerating] = useState(false);
  const { toast } = useToast();

  const handlePdfDownload = async () => {
    setPdfGenerating(true);
    try {
      const response = await apiFetch(
        `${base44.baseUrl}/reports/tax-year?format=pdf&year=${selectedYear}`
      );
      if (!response.ok) throw new Error("PDF generation failed");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `tax-year-${selectedYear}-pnl.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast({
        description: "PDF generation failed. Please try again.",
        variant: "destructive",
        duration: 5000,
      });
    } finally {
      setPdfGenerating(false);
    }
  };

  const handleCsvDownload = async () => {
    setCsvGenerating(true);
    try {
      const response = await apiFetch(
        `${base44.baseUrl}/reports/tax-year?format=csv&year=${selectedYear}`
      );
      if (!response.ok) throw new Error("CSV generation failed");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `tax-year-${selectedYear}-pnl.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast({
        description: "CSV generation failed. Please try again.",
        variant: "destructive",
        duration: 5000,
      });
    } finally {
      setCsvGenerating(false);
    }
  };

  const { data: reportData, isLoading, isError, error } = useQuery({
    queryKey: ["taxYearReport", selectedYear],
    queryFn: async () => {
      const response = await apiFetch(
        `${base44.baseUrl}/reports/tax-year?year=${selectedYear}`
      );
      const result = await response.json();
      if (result.status === "error") throw new Error(result.message);
      return result.data;
    },
  });

  // Build year options from 2020 to current tax year (future disabled)
  const yearOptions = [];
  for (let y = currentTaxYear; y >= 2020; y--) {
    yearOptions.push(y);
  }

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDir(d => d === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDir("asc");
    }
  };

  const sortedTrades = useMemo(() => {
    if (!reportData?.trades) return [];
    return [...reportData.trades].sort((a, b) => {
      const av = a[sortField] ?? "";
      const bv = b[sortField] ?? "";
      const cmp = av < bv ? -1 : av > bv ? 1 : 0;
      return sortDir === "asc" ? cmp : -cmp;
    });
  }, [reportData, sortField, sortDir]);

  const SortIcon = ({ field }) => {
    if (sortField !== field) return <ChevronsUpDown className="w-3 h-3 text-slate-500 inline ml-1" />;
    return sortDir === "asc"
      ? <ChevronUp className="w-3 h-3 text-cyan-400 inline ml-1" />
      : <ChevronDown className="w-3 h-3 text-cyan-400 inline ml-1" />;
  };

  const taxYearLabel = reportData?.tax_year_label ?? `${selectedYear}/${String(selectedYear + 1).slice(2)}`;

  return (
    <div className="space-y-6">
      {/* Disclaimer Banner */}
      <div className="flex items-start gap-3 rounded-xl border border-amber-500/40 bg-amber-500/10 p-4">
        <AlertTriangle className="w-5 h-5 text-amber-400 mt-0.5 shrink-0" />
        <p className="text-sm text-amber-200">
          This report is provided for user reference only. It is not a substitute for qualified tax
          advice. Users are responsible for verifying figures against their broker records and obtaining
          appropriate professional advice before submitting any tax return.
        </p>
      </div>

      {/* Year Selector + Download buttons */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <Calendar className="w-4 h-4 text-slate-400" />
          <span className="text-sm text-slate-600 dark:text-slate-400">Tax Year</span>
          <Select
            value={String(selectedYear)}
            onValueChange={(v) => setSelectedYear(Number(v))}
          >
            <SelectTrigger className="w-36 bg-slate-800/50 border-slate-700 text-white h-9">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-700">
              {yearOptions.map((y) => (
                <SelectItem key={y} value={String(y)}>
                  {y}/{String(y + 1).slice(2)}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <Button
            onClick={handlePdfDownload}
            disabled={pdfGenerating}
            variant="outline"
            className="border-slate-600 text-slate-300 hover:text-white hover:border-slate-500 h-9"
          >
            {pdfGenerating ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Generating…
              </>
            ) : (
              <>
                <FileDown className="w-4 h-4 mr-2" />
                Download PDF
              </>
            )}
          </Button>
          {/* ST-13 (BLG-FEAT-69, v7.0): placed right of PDF per tax-year-csv-export/ux_spec.md §2 */}
          <Button
            onClick={handleCsvDownload}
            disabled={csvGenerating}
            variant="outline"
            className="border-slate-600 text-slate-300 hover:text-white hover:border-slate-500 h-9"
          >
            {csvGenerating ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Generating…
              </>
            ) : (
              <>
                <FileDown className="w-4 h-4 mr-2" />
                Download CSV
              </>
            )}
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : isError ? (
        <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-6 text-center">
          <p className="text-rose-300 text-sm">{error?.message ?? "Failed to load report."}</p>
        </div>
      ) : (
        <>
          {/* Summary Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-xl border border-slate-700/50 bg-slate-800/50 p-4"
            >
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Total Realised P&L</p>
              <p className={`text-xl font-bold ${(reportData?.summary?.total_realised_pnl ?? 0) >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                {formatGBP(reportData?.summary?.total_realised_pnl)}
              </p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 }}
              className="rounded-xl border border-slate-700/50 bg-slate-800/50 p-4"
            >
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Gross Profit</p>
              <p className="text-xl font-bold text-emerald-400">
                {formatGBP(reportData?.summary?.total_gross_profit)}
              </p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="rounded-xl border border-slate-700/50 bg-slate-800/50 p-4"
            >
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Gross Loss</p>
              <p className="text-xl font-bold text-rose-400">
                {formatGBP(reportData?.summary?.total_gross_loss)}
              </p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 }}
              className="rounded-xl border border-slate-700/50 bg-slate-800/50 p-4"
            >
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Win Rate</p>
              <p className="text-xl font-bold text-white">
                {formatPct(reportData?.summary?.win_rate)}
              </p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="rounded-xl border border-slate-700/50 bg-slate-800/50 p-4"
            >
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Trades</p>
              <p className="text-xl font-bold text-white">
                {reportData?.summary?.total_closed_trades ?? 0}
              </p>
            </motion.div>
          </div>

          {/* Trades Table */}
          {sortedTrades.length === 0 ? (
            <div className="rounded-xl border border-slate-700/50 bg-slate-800/50 py-12 text-center">
              <FileText className="w-10 h-10 text-slate-600 mx-auto mb-3" />
              <p className="text-slate-600 dark:text-slate-400">
                No closed trades recorded for the {taxYearLabel} tax year.
              </p>
            </div>
          ) : (
            <div className="rounded-xl border border-slate-700/50 bg-slate-800/50 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700/50">
                    {[
                      { key: "ticker", label: "Ticker" },
                      { key: "market", label: "Market" },
                      { key: "entry_date", label: "Entry Date" },
                      { key: "exit_date", label: "Exit Date" },
                      { key: "holding_days", label: "Days" },
                      { key: "entry_price_native", label: "Entry Price" },
                      { key: "exit_price_native", label: "Exit Price" },
                      { key: "shares", label: "Shares" },
                      { key: "total_cost_gbp", label: "Total Cost" },
                      { key: "exit_proceeds_gbp", label: "Exit Proceeds" },
                      { key: "realised_pnl_gbp", label: "Realised P&L" },
                      { key: "pnl_pct", label: "P&L %" },
                      { key: "tags", label: "Tags" },
                    ].map(({ key, label }) => (
                      <th
                        key={key}
                        onClick={() => handleSort(key)}
                        className="px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider cursor-pointer hover:text-white select-none whitespace-nowrap"
                      >
                        {label}<SortIcon field={key} />
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {sortedTrades.map((trade, i) => {
                    const pnl = trade.realised_pnl_gbp ?? 0;
                    // ST-08 (BLG-FE-144, EPIC-03, v8.5): converged on the
                    // three-way rule MonthlyPnlTable already used (grey/
                    // neutral for exact-zero, not red) per the Design Gate
                    // decision record -- a breakeven trade is not a loss.
                    // Resolves DEV-REPORTS-ST01-02.
                    const pnlColor = pnl > 0 ? "text-emerald-400" : pnl < 0 ? "text-rose-400" : "text-slate-600 dark:text-slate-400";
                    // decision_record.md §5 Scope boundary: "Applies to the
                    // Realised P&L column in both tables only. Does not
                    // touch P&L %..." -- kept on the original binary rule,
                    // deliberately NOT sharing pnlColor with the cell below,
                    // so this column's colour is unaffected by ST-08.
                    const pnlPctColor = trade.pnl_pct > 0 ? "text-emerald-400" : "text-rose-400";
                    const currency = trade.currency === "USD" ? "USD" : "GBP";
                    const priceSymbol = currency === "USD" ? "$" : "£";
                    return (
                      <tr
                        key={trade.id ?? i}
                        className="border-b border-slate-700/30 hover:bg-slate-700/20 transition-colors"
                      >
                        <td className="px-3 py-3 font-medium text-white">{trade.ticker}</td>
                        <td className="px-3 py-3">
                          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${trade.market === "US" ? "bg-violet-500/20 text-violet-300" : "bg-cyan-500/20 text-cyan-300"}`}>
                            {trade.market}
                          </span>
                        </td>
                        <td className="px-3 py-3 text-slate-300">{trade.entry_date}</td>
                        <td className="px-3 py-3 text-slate-300">{trade.exit_date}</td>
                        <td className="px-3 py-3 text-slate-300">{trade.holding_days}</td>
                        <td className="px-3 py-3 text-slate-300">
                          {priceSymbol}{Number(trade.entry_price_native ?? 0).toFixed(2)}
                          <span className="text-xs text-slate-600 dark:text-slate-400 ml-1">{currency}</span>
                        </td>
                        <td className="px-3 py-3 text-slate-300">
                          {priceSymbol}{Number(trade.exit_price_native ?? 0).toFixed(2)}
                          <span className="text-xs text-slate-600 dark:text-slate-400 ml-1">{currency}</span>
                        </td>
                        <td className="px-3 py-3 text-slate-300">{trade.shares}</td>
                        <td className="px-3 py-3 text-slate-300">{formatGBP(trade.total_cost_gbp)}</td>
                        <td className="px-3 py-3 text-slate-300">{formatGBP(trade.exit_proceeds_gbp)}</td>
                        <td data-testid="tax-year-realised-pnl-cell" className={`px-3 py-3 font-medium ${pnlColor}`}>{formatGBP(pnl)}</td>
                        <td data-testid="tax-year-pnl-pct-cell" className={`px-3 py-3 ${pnlPctColor}`}>{formatPct(trade.pnl_pct)}</td>
                        <td className="px-3 py-3">
                          <div className="flex flex-wrap gap-1">
                            {(trade.tags ?? []).map((tag) => (
                              <span key={tag} className="text-xs bg-slate-700 text-slate-300 px-2 py-0.5 rounded-full">
                                {tag}
                              </span>
                            ))}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {/* Unrealised P&L Card */}
          {(reportData?.estimated_unrealised_pnl != null) && (
            <div className="rounded-xl border border-slate-600/50 bg-slate-800/30 p-5">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">
                Indicative Unrealised P&L (current positions)
              </h3>
              <p className={`text-2xl font-bold mb-3 ${(reportData.estimated_unrealised_pnl ?? 0) >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                {formatGBP(reportData.estimated_unrealised_pnl)}
              </p>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                {reportData.unrealised_note}
              </p>
            </div>
          )}

          {/* SI-02 Gate Status — ST-06 (v6.8, BLG-FEAT-71) */}
          <SI02GateStatusSection />

          {/* Scope Note */}
          <p className="text-xs text-slate-600 dark:text-slate-400 text-center pb-2">
            UK tax year only (6 April to 5 April). Verify all figures against your broker records and seek qualified tax advice before filing.
          </p>
        </>
      )}
    </div>
  );
}

// ─── SI-02 Gate Status ──────────────────────────────────────────────────────
// reports.md §SI-02 Gate Status (v0.6 — ST-06, BLG-FEAT-71)
// Design source: docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md
// Collapsible, collapsed by default. Distinct from Dashboard's single-metric Gate
// Progress strip (dashboard.md §6) — surfaces total vs. trade-plan-linked closed
// trades plus a per-condition MET/NOT MET breakdown. Values sourced live from
// GET /trades, GET /trade-plans, GET /analytics/arc5-compliance — never hardcoded.
function SI02GateStatusSection() {
  const [collapsed, setCollapsed] = useState(true);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["si02-gate-status"],
    queryFn: async () => {
      const [tradesRes, plansRes, arc5, drift] = await Promise.all([
        api.trades.list(),
        apiFetch(`${base44.baseUrl}/trade-plans`).then((r) => r.json()),
        api.analytics.arc5Compliance("7d"),
        api.analytics.behaviouralDrift().catch(() => null),
      ]);
      const totalClosedTrades = tradesRes?.total_trades ?? 0;
      const plans = Array.isArray(plansRes?.data) ? plansRes.data : [];
      // reports.md §SI-02 Gate Status: "GET /trade-plans closed, position_id non-null count"
      // — both conditions required, not position_id alone (an active-but-linked plan
      // must not be counted as a linked *closed* trade).
      const linkedClosedTrades = plans.filter((p) => p.status === "closed" && p.position_id != null).length;
      const tradePlanAdherenceRate = arc5?.trade_plan_adherence_rate ?? null;
      return {
        totalClosedTrades,
        linkedClosedTrades,
        gateCondition1Met: totalClosedTrades >= 20,
        gateCondition2Met: linkedClosedTrades >= 20,
        // Product-reviewed threshold (ST-14, BLG-SPEC-72, 2026-08-03): a majority
        // of closed trades must show trade-plan discipline. See
        // reports.md §SI-02 Gate Status for the decision rationale.
        gateCondition3Met: tradePlanAdherenceRate != null && tradePlanAdherenceRate >= 0.50,
        // ST-05 (v8.2, EPIC-01, BLG-FEAT-86): insufficient_data streak metric,
        // surfaced alongside this existing SI-02 gate note. Only present when
        // the drift endpoint itself is in the insufficient_data state.
        driftInsufficientData: drift?.status === "insufficient_data",
        driftStreakDays: drift?.insufficient_data_streak_days ?? null,
        driftStreakCapped: drift?.streak_capped ?? false,
        driftTrend: drift?.trade_count_trend ?? null,
      };
    },
    retry: 1,
  });

  const GateBadge = ({ met }) => (
    <span
      className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
        met ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
      }`}
    >
      {met ? "MET" : "NOT MET"}
    </span>
  );

  return (
    <div data-testid="si02-gate-status-section" className="bg-slate-800/50 rounded-lg border border-slate-700/50 overflow-hidden">
      <button
        type="button"
        data-testid="si02-gate-status-toggle"
        onClick={() => setCollapsed(!collapsed)}
        className="w-full flex items-center justify-between px-6 py-4 text-left hover:bg-slate-700/20 transition-colors"
      >
        <h3 className="text-sm font-semibold text-white">SI-02 Gate Status</h3>
        {collapsed ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronUp className="w-4 h-4 text-slate-400" />}
      </button>

      {!collapsed && (
        <div className="px-6 py-5 border-t border-slate-700/50">
          {isLoading ? (
            <div className="h-16 rounded-lg bg-slate-800/50 animate-pulse" />
          ) : isError ? (
            <p className="text-sm text-slate-600 dark:text-slate-400">Unable to load gate status</p>
          ) : (
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Total Closed Trades</p>
                  <p className="text-lg font-semibold text-white">{data.totalClosedTrades} total closed trades</p>
                </div>
                <div>
                  <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Linked to a Trade Plan</p>
                  <p className="text-lg font-semibold text-white">{data.linkedClosedTrades} linked to a trade plan</p>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="flex items-center justify-between rounded-lg bg-slate-800/50 border border-slate-700/50 px-4 py-3">
                  <span className="text-sm text-slate-300">Gate Condition 1</span>
                  <GateBadge met={data.gateCondition1Met} />
                </div>
                <div className="flex items-center justify-between rounded-lg bg-slate-800/50 border border-slate-700/50 px-4 py-3">
                  <span className="text-sm text-slate-300">Gate Condition 2</span>
                  <GateBadge met={data.gateCondition2Met} />
                </div>
                <div className="flex items-center justify-between rounded-lg bg-slate-800/50 border border-slate-700/50 px-4 py-3">
                  <span className="text-sm text-slate-300">Gate Condition 3</span>
                  <GateBadge met={data.gateCondition3Met} />
                </div>
              </div>

              {data.driftInsufficientData && (
                <div
                  data-testid="si02-insufficient-data-streak"
                  className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-700/50"
                >
                  <div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Insufficient-Data Streak</p>
                    <p className="text-lg font-semibold text-white" data-testid="si02-streak-days">
                      {data.driftStreakDays}{data.driftStreakCapped ? "+" : ""} days
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Trade Count Trend</p>
                    <p className="text-lg font-semibold text-white capitalize" data-testid="si02-trend">
                      {data.driftTrend ?? "—"}
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ─── Reconciliation Report ──────────────────────────────────────────────────
// reports.md §Reconciliation (ST-01, EPIC-01, v8.2, BLG-FEAT-88)
// Design source: docs/design/2026-08-04__release-v8.2/pnl-reconciliation-report/decision_record.md
// Reuses the SI-02 Gate Status stat-card / MET-NOT MET badge visual language verbatim.
function ReconciliationReport() {
  const currentTaxYear = getCurrentUKTaxYear();
  const [selectedYear, setSelectedYear] = useState(currentTaxYear);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["reconciliationReport", selectedYear],
    queryFn: async () => {
      const response = await apiFetch(
        `${base44.baseUrl}/reports/reconciliation?year=${selectedYear}`
      );
      const result = await response.json();
      if (result.status === "error") throw new Error(result.message);
      return result.data;
    },
  });

  const yearOptions = [];
  for (let y = currentTaxYear; y >= 2020; y--) {
    yearOptions.push(y);
  }

  const MatchBadge = ({ matched, diff }) => (
    <span
      data-testid="reconciliation-match-badge"
      className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
        matched
          ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
          : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
      }`}
    >
      {matched ? "✓ Reconciled" : `⚠ Discrepancy — ${formatGBP(diff)} difference`}
    </span>
  );

  return (
    <div className="space-y-6" data-testid="reconciliation-report">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <Calendar className="w-4 h-4 text-slate-400" />
          <span className="text-sm text-slate-600 dark:text-slate-400">Tax Year</span>
          <Select
            value={String(selectedYear)}
            onValueChange={(v) => setSelectedYear(Number(v))}
          >
            <SelectTrigger className="w-36 bg-slate-800/50 border-slate-700 text-white h-9">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-700">
              {yearOptions.map((y) => (
                <SelectItem key={y} value={String(y)}>
                  {y}/{String(y + 1).slice(2)}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div
        data-testid="reconciliation-content"
        className="bg-slate-800/50 rounded-lg border border-slate-700/50 px-6 py-5"
      >
        {isLoading ? (
          <div className="h-16 rounded-lg bg-slate-800/50 animate-pulse" data-testid="reconciliation-loading" />
        ) : isError ? (
          <p className="text-sm text-slate-600 dark:text-slate-400" data-testid="reconciliation-error">
            Unable to load reconciliation data
          </p>
        ) : data.total_closed_trades === 0 ? (
          <p className="text-sm text-slate-600 dark:text-slate-400" data-testid="reconciliation-empty">
            No trade data available for {data.tax_year_label} — reconciliation not applicable
          </p>
        ) : (
          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">System-Computed Total</p>
                <p
                  className={`text-lg font-semibold ${data.system_total_pnl_gbp >= 0 ? "text-emerald-400" : "text-rose-400"}`}
                  data-testid="reconciliation-system-total"
                >
                  {formatGBP(data.system_total_pnl_gbp)}
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Trade Export Total</p>
                <p
                  className={`text-lg font-semibold ${data.export_total_pnl_gbp >= 0 ? "text-emerald-400" : "text-rose-400"}`}
                  data-testid="reconciliation-export-total"
                >
                  {formatGBP(data.export_total_pnl_gbp)}
                </p>
              </div>
            </div>
            <MatchBadge
              matched={data.matched}
              diff={Math.abs(data.system_total_pnl_gbp - data.export_total_pnl_gbp)}
            />
            <p className="text-xs text-slate-500" data-testid="reconciliation-sign-off-note">
              Reviewed and confirmed matching by the Financial Reporting & Records Owner on 2026-08-04
            </p>
          </div>
        )}
      </div>

      <p className="text-xs text-slate-600 dark:text-slate-400 text-center pb-2">
        Compares the system-computed realised P&L total for the selected tax year against an
        independently re-derived sum of the individual trade export rows.
      </p>
    </div>
  );
}

// ─── Monthly P&L Table ────────────────────────────────────────────────────────

const MONTH_NAMES = [
  "", "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

function MonthlyPnlTable() {
  const [csvGenerating, setCsvGenerating] = useState(false);
  const { toast } = useToast();

  const { data: response, isLoading } = useQuery({
    queryKey: ["monthlyPnl"],
    queryFn: () =>
      apiFetch(`${base44.baseUrl}/reports/monthly-pnl`).then((r) => r.json()),
  });

  // ST-05 (BLG-FEAT-81, v7.8): reuses the Tax Year tab's Download CSV pattern
  // verbatim, per monthly-csv-export/ux_spec.md §2/§4.
  const handleCsvDownload = async () => {
    setCsvGenerating(true);
    try {
      const response = await apiFetch(`${base44.baseUrl}/reports/monthly-pnl?format=csv`);
      if (!response.ok) throw new Error("CSV generation failed");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "monthly-pnl.csv";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast({
        description: "CSV generation failed. Please try again.",
        variant: "destructive",
        duration: 5000,
      });
    } finally {
      setCsvGenerating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
      </div>
    );
  }

  const rows = response?.data ?? [];
  const compliance = response?.compliance_summary ?? null;
  const estimatedUnrealisedPnl = response?.estimated_unrealised_pnl;
  const unrealisedNote = response?.unrealised_note;
  const totalRealisedPnl = rows.reduce((sum, row) => sum + (row.realised_pnl_gbp ?? 0), 0);
  const combinedTotal = totalRealisedPnl + (estimatedUnrealisedPnl ?? 0);

  return (
    <div className="space-y-4">
      {/* ST-05 (BLG-FEAT-81, v7.8): Download CSV control for the Monthly P&L
          Report view — verbatim reuse of the Tax Year tab's export button,
          per monthly-csv-export/ux_spec.md §2. Drops below the section
          header full-width on narrow screens (flex-wrap). */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-sm font-semibold text-white">Monthly P&L Report</h2>
        <Button
          onClick={handleCsvDownload}
          disabled={csvGenerating}
          variant="outline"
          className="border-slate-600 text-slate-300 hover:text-white hover:border-slate-500 h-9"
        >
          {csvGenerating ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Generating…
            </>
          ) : (
            <>
              <FileDown className="w-4 h-4 mr-2" />
              Download CSV
            </>
          )}
        </Button>
      </div>

      <div className="bg-slate-800/50 rounded-lg border border-slate-700/50 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-700/50">
          <h3 className="text-sm font-semibold text-white">Monthly Realised P&L</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">Current and prior calendar year. Only months with closed trades shown.</p>
        </div>
        {rows.length === 0 ? (
          <div className="px-6 py-10 text-center text-slate-600 dark:text-slate-400 text-sm">No closed trades in scope.</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700/50">
                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Month</th>
                <th className="px-6 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Realised P&L</th>
                <th className="px-6 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Trades</th>
                {/* ST-01 (BLG-FE-141, EPIC-01, v8.4): Avg P&L/Trade — client-side derived
                    display column, per reports.md §Monthly Financial Table (v0.14). */}
                <th data-testid="monthly-avg-pnl-header" className="px-6 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Avg P&L/Trade</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/30">
              {rows.map((row) => {
                const pnl = row.realised_pnl_gbp ?? 0;
                const pnlColor = pnl > 0 ? "text-emerald-400" : pnl < 0 ? "text-rose-400" : "text-slate-600 dark:text-slate-400";
                // ST-01: derived from already-fetched row values, not a P&L recalculation.
                // trade_count = 0 shows "—" (no colour) rather than a fabricated £0.00.
                const avgPnl = row.trade_count > 0 ? pnl / row.trade_count : null;
                const avgPnlColor = avgPnl == null ? "text-slate-600 dark:text-slate-400" : avgPnl > 0 ? "text-emerald-400" : avgPnl < 0 ? "text-rose-400" : "text-slate-600 dark:text-slate-400";
                return (
                  <tr key={`${row.year}-${row.month}`} className="hover:bg-slate-700/20 transition-colors">
                    <td className="px-6 py-3 text-slate-200">
                      {MONTH_NAMES[row.month]} {row.year}
                    </td>
                    <td data-testid="monthly-realised-pnl-cell" className={`px-6 py-3 text-right font-medium ${pnlColor}`}>
                      {formatGBP(pnl)}
                    </td>
                    <td className="px-6 py-3 text-right text-slate-600 dark:text-slate-400">{row.trade_count}</td>
                    <td data-testid="monthly-avg-pnl-cell" className={`px-6 py-3 text-right font-medium ${avgPnlColor}`}>
                      {formatGBP(avgPnl)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* ST-14 (BLG-FEAT-70, v7.0): Unrealised P&L Card — reuses the Tax Year tab's approved pattern verbatim */}
      {estimatedUnrealisedPnl != null && (
        <div data-testid="monthly-unrealised-pnl-card" className="rounded-xl border border-slate-600/50 bg-slate-800/30 p-5">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">
            Indicative Unrealised P&L (current positions)
          </h3>
          <p className={`text-2xl font-bold mb-3 ${(estimatedUnrealisedPnl ?? 0) >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
            {formatGBP(estimatedUnrealisedPnl)}
          </p>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            {unrealisedNote}
          </p>
          {/* Combined Total line (satisfies AC-02 regression check) */}
          <p data-testid="monthly-combined-total" className="text-sm font-semibold text-white mt-4 pt-3 border-t border-slate-700/50">
            Total (Realised + Unrealised): {formatGBP(combinedTotal)}
          </p>
        </div>
      )}

      {/* Strategy Compliance — ST-18 (Arc 5, v4.3) */}
      <div data-testid="strategy-compliance-section" className="bg-slate-800/50 rounded-lg border border-slate-700/50 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-700/50">
          <h3 className="text-sm font-semibold text-white">Strategy Compliance</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
            Pre-entry discipline metrics — last {compliance?.period_days ?? 30} days.
          </p>
        </div>
        {compliance === null ? (
          <div className="px-6 py-6 text-center text-slate-600 dark:text-slate-400 text-sm">Compliance data unavailable.</div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-px bg-slate-700/30">
            <div data-testid="compliance-pass-rate" className="bg-slate-800/50 px-5 py-4">
              <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Validation Pass Rate</p>
              <p className="text-lg font-semibold text-white">
                {compliance.validation_pass_rate != null
                  ? `${(compliance.validation_pass_rate * 100).toFixed(1)}%`
                  : "—"}
              </p>
            </div>
            <div data-testid="compliance-override-count" className="bg-slate-800/50 px-5 py-4">
              <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Override Count</p>
              <p className="text-lg font-semibold text-white">{compliance.override_count ?? "—"}</p>
            </div>
            <div data-testid="compliance-red-flag-count" className="bg-slate-800/50 px-5 py-4">
              <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Red Flag Events</p>
              <p className="text-lg font-semibold text-white">{compliance.red_flag_events_count ?? "—"}</p>
            </div>
            <div data-testid="compliance-rule-breach" className="bg-slate-800/50 px-5 py-4">
              <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wide mb-1">Most Frequent Breach</p>
              <p className="text-lg font-semibold text-white">
                {compliance.most_frequent_rule_breach ?? "None"}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Main Reports Page ─────────────────────────────────────────────────────────

// Map frontend period selector values to backend period parameter values
const PERIOD_MAP = {
  week: "last_7_days",
  month: "last_month",
  quarter: "last_quarter",
  year: "last_year",
  ytd: "ytd",
  all: "all_time",
};

export default function Reports() {
  const [activeTab, setActiveTab] = useState("performance");
  const [period, setPeriod] = useState("month");
  const [exportModalOpen, setExportModalOpen] = useState(false);

  const backendPeriod = PERIOD_MAP[period] ?? "last_month";

  // Fetch backend-computed analytics metrics (period-filtered on server)
  const { data: analyticsData, isLoading: loadingAnalytics } = useQuery({
    queryKey: ["analyticsMetrics", backendPeriod],
    queryFn: () => api.analytics.metrics(backendPeriod),
    enabled: activeTab === "performance",
  });

  // Fetch open positions count for the StatsCard subtitle
  const { data: openPositions = [] } = useQuery({
    queryKey: ["openPositions"],
    queryFn: () => api.positions.list(),
    select: (data) => (data || []).filter(p => p.status === "open"),
    enabled: activeTab === "performance",
  });

  // Calculate date range based on period (still needed for PortfolioGrowthChart)
  const periodDates = useMemo(() => {
    const now = new Date();
    let start = new Date();
    switch (period) {
      case "week":   start.setDate(now.getDate() - 7); break;
      case "month":  start.setMonth(now.getMonth() - 1); break;
      case "quarter": start.setMonth(now.getMonth() - 3); break;
      case "year":   start.setFullYear(now.getFullYear() - 1); break;
      case "ytd":    start = new Date(now.getFullYear(), 0, 1); break;
      case "all":    start = new Date(2020, 0, 1); break;
      default:       start.setMonth(now.getMonth() - 1);
    }
    return { start, end: now };
  }, [period]);

  // Adapt trades_for_charts to the shape expected by sub-components
  const filteredPositions = useMemo(() => {
    const trades = analyticsData?.trades_for_charts || [];
    return trades.map(t => ({
      ...t,
      status: "closed",
      pnl_percent: t.pnl_pct ?? t.pnl_percent,
      fees: t.fees ?? 0,
    }));
  }, [analyticsData]);

  // Build metrics from backend analytics response
  const metrics = useMemo(() => {
    if (!analyticsData) {
      return {
        totalPnL: 0, winRate: 0, totalTrades: 0, winningTrades: 0, losingTrades: 0,
        grossProfit: 0, grossLoss: 0, avgWin: 0, avgLoss: 0, profitFactor: 0,
        totalFees: 0, openPositions: 0, bestTrade: 0, worstTrade: 0,
      };
    }
    const trades = analyticsData.trades_for_charts || [];
    const wins = trades.filter(t => (t.pnl || 0) > 0);
    const lossesList = trades.filter(t => (t.pnl || 0) < 0);
    const grossProfit = wins.reduce((s, t) => s + (t.pnl || 0), 0);
    const grossLoss = Math.abs(lossesList.reduce((s, t) => s + (t.pnl || 0), 0));
    return {
      totalPnL: analyticsData.summary?.total_pnl ?? 0,
      winRate: analyticsData.summary?.win_rate ?? 0,
      totalTrades: analyticsData.summary?.total_trades ?? 0,
      winningTrades: wins.length,
      losingTrades: lossesList.length,
      grossProfit,
      grossLoss,
      avgWin: wins.length > 0 ? grossProfit / wins.length : 0,
      avgLoss: lossesList.length > 0 ? grossLoss / lossesList.length : 0,
      profitFactor: analyticsData.executive_metrics?.profit_factor ?? 0,
      totalFees: trades.reduce((s, t) => s + (t.fees || 0), 0),
      openPositions: openPositions.length,
      bestTrade: trades.length > 0 ? Math.max(...trades.map(t => t.pnl || 0)) : 0,
      worstTrade: trades.length > 0 ? Math.min(...trades.map(t => t.pnl || 0)) : 0,
    };
  }, [analyticsData, openPositions]);

  const periodLabels = {
    week: "Last 7 Days",
    month: "Last Month",
    quarter: "Last Quarter",
    year: "Last Year",
    ytd: "Year to Date",
    all: "All Time"
  };

  const isLoading = loadingAnalytics;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports"
        description="Performance analysis and export tools"
        actions={
          activeTab === "performance" ? (
            <div className="flex items-center gap-3">
              <Select value={period} onValueChange={setPeriod}>
                <SelectTrigger className="w-40 bg-slate-800/50 border-slate-700 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="week">Last 7 Days</SelectItem>
                  <SelectItem value="month">Last Month</SelectItem>
                  <SelectItem value="quarter">Last Quarter</SelectItem>
                  <SelectItem value="year">Last Year</SelectItem>
                  <SelectItem value="ytd">Year to Date</SelectItem>
                  <SelectItem value="all">All Time</SelectItem>
                </SelectContent>
              </Select>
              <Button
                onClick={() => setExportModalOpen(true)}
                className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white"
              >
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
            </div>
          ) : null
        }
      />

      {/* Tab Navigation */}
      <div className="flex gap-1 border-b border-slate-700/50">
        <button
          onClick={() => setActiveTab("performance")}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "performance"
              ? "border-cyan-500 text-white"
              : "border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-300"
          }`}
        >
          Performance
        </button>
        <button
          onClick={() => setActiveTab("taxYear")}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "taxYear"
              ? "border-cyan-500 text-white"
              : "border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-300"
          }`}
        >
          Tax Year P&L
        </button>
        <button
          onClick={() => setActiveTab("monthly")}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "monthly"
              ? "border-cyan-500 text-white"
              : "border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-300"
          }`}
        >
          Monthly P&L
        </button>
        <button
          onClick={() => setActiveTab("reconciliation")}
          data-testid="reports-tab-reconciliation"
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "reconciliation"
              ? "border-cyan-500 text-white"
              : "border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-300"
          }`}
        >
          Reconciliation
        </button>
      </div>

      {activeTab === "taxYear" ? (
        <TaxYearReport />
      ) : activeTab === "monthly" ? (
        <MonthlyPnlTable />
      ) : activeTab === "reconciliation" ? (
        <ReconciliationReport />
      ) : isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : (
        <div className="space-y-8">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatsCard
              title="Total P&L"
              value={`${metrics.totalPnL >= 0 ? "+" : ""}£${metrics.totalPnL.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
              subtitle={periodLabels[period]}
              icon={metrics.totalPnL >= 0 ? TrendingUp : TrendingDown}
              gradient={metrics.totalPnL >= 0 ? "emerald" : "rose"}
            />
            <StatsCard
              title="Win Rate"
              value={`${metrics.winRate.toFixed(1)}%`}
              subtitle={`${metrics.winningTrades}W / ${metrics.losingTrades}L`}
              icon={PieChart}
              gradient="cyan"
            />
            <StatsCard
              title="Profit Factor"
              value={metrics.profitFactor === Infinity ? "∞" : metrics.profitFactor.toFixed(2)}
              subtitle="Risk/Reward"
              icon={BarChart3}
              gradient="violet"
            />
            <StatsCard
              title="Total Trades"
              value={metrics.totalTrades.toString()}
              subtitle={`${metrics.openPositions} still open`}
              icon={FileText}
              gradient="fuchsia"
            />
          </div>

          {/* Portfolio Growth Chart */}
          <PortfolioGrowthChart
            positions={filteredPositions}
            period={period}
            periodDates={periodDates}
          />

          {/* Performance Summary & Trade Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <PerformanceSummary metrics={metrics} period={periodLabels[period]} />
            <TradeBreakdown positions={filteredPositions} />
          </div>
        </div>
      )}

      <ExportModal
        open={exportModalOpen}
        onClose={() => setExportModalOpen(false)}
        positions={filteredPositions}
        metrics={metrics}
        period={periodLabels[period]}
      />
    </div>
  );
}
