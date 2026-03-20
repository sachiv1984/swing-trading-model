import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
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
      const response = await fetch(
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
      const response = await fetch(
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
      const response = await fetch(
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
          <span className="text-sm text-slate-400">Tax Year</span>
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
              <p className="text-xs text-slate-400 mb-1">Total Realised P&L</p>
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
              <p className="text-xs text-slate-400 mb-1">Gross Profit</p>
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
              <p className="text-xs text-slate-400 mb-1">Gross Loss</p>
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
              <p className="text-xs text-slate-400 mb-1">Win Rate</p>
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
              <p className="text-xs text-slate-400 mb-1">Trades</p>
              <p className="text-xl font-bold text-white">
                {reportData?.summary?.total_closed_trades ?? 0}
              </p>
            </motion.div>
          </div>

          {/* Trades Table */}
          {sortedTrades.length === 0 ? (
            <div className="rounded-xl border border-slate-700/50 bg-slate-800/50 py-12 text-center">
              <FileText className="w-10 h-10 text-slate-600 mx-auto mb-3" />
              <p className="text-slate-400">
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
                        className="px-3 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:text-white select-none whitespace-nowrap"
                      >
                        {label}<SortIcon field={key} />
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {sortedTrades.map((trade, i) => {
                    const pnl = trade.realised_pnl_gbp ?? 0;
                    const pnlColor = pnl > 0 ? "text-emerald-400" : "text-rose-400";
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
                          <span className="text-xs text-slate-500 ml-1">{currency}</span>
                        </td>
                        <td className="px-3 py-3 text-slate-300">
                          {priceSymbol}{Number(trade.exit_price_native ?? 0).toFixed(2)}
                          <span className="text-xs text-slate-500 ml-1">{currency}</span>
                        </td>
                        <td className="px-3 py-3 text-slate-300">{trade.shares}</td>
                        <td className="px-3 py-3 text-slate-300">{formatGBP(trade.total_cost_gbp)}</td>
                        <td className="px-3 py-3 text-slate-300">{formatGBP(trade.exit_proceeds_gbp)}</td>
                        <td className={`px-3 py-3 font-medium ${pnlColor}`}>{formatGBP(pnl)}</td>
                        <td className={`px-3 py-3 ${pnlColor}`}>{formatPct(trade.pnl_pct)}</td>
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
              <p className="text-xs text-slate-500 leading-relaxed">
                {reportData.unrealised_note}
              </p>
            </div>
          )}

          {/* Scope Note */}
          <p className="text-xs text-slate-500 text-center pb-2">
            UK tax year only (6 April to 5 April). Verify all figures against your broker records and seek qualified tax advice before filing.
          </p>
        </>
      )}
    </div>
  );
}

// ─── Main Reports Page ─────────────────────────────────────────────────────────

export default function Reports() {
  const [activeTab, setActiveTab] = useState("performance");
  const [period, setPeriod] = useState("month");
  const [exportModalOpen, setExportModalOpen] = useState(false);
  const [dateRange, setDateRange] = useState({ start: null, end: null });

  const { data: positions, isLoading: loadingPositions } = useQuery({
    queryKey: ["allPositions"],
    queryFn: () => base44.entities.Position.list("-exit_date"),
  });

  const { data: portfolios } = useQuery({
    queryKey: ["portfolios"],
    queryFn: () => base44.entities.Portfolio.list(),
  });

  const portfolio = portfolios?.[0];

  // Calculate date range based on period
  const periodDates = useMemo(() => {
    const now = new Date();
    let start = new Date();

    switch (period) {
      case "week":
        start.setDate(now.getDate() - 7);
        break;
      case "month":
        start.setMonth(now.getMonth() - 1);
        break;
      case "quarter":
        start.setMonth(now.getMonth() - 3);
        break;
      case "year":
        start.setFullYear(now.getFullYear() - 1);
        break;
      case "ytd":
        start = new Date(now.getFullYear(), 0, 1);
        break;
      case "all":
        start = new Date(2020, 0, 1);
        break;
      default:
        start.setMonth(now.getMonth() - 1);
    }

    return { start, end: now };
  }, [period]);

  // Filter positions by date range
  const filteredPositions = useMemo(() => {
    if (!positions) return [];

    const range = dateRange.start ? dateRange : periodDates;

    return positions.filter(p => {
      const exitDate = p.exit_date ? new Date(p.exit_date) : null;
      const entryDate = new Date(p.entry_date);

      return entryDate <= range.end && (!exitDate || exitDate >= range.start);
    });
  }, [positions, periodDates, dateRange]);

  // Calculate performance metrics
  const metrics = useMemo(() => {
    const closedTrades = filteredPositions.filter(p => p.status === "closed");
    const openTrades = filteredPositions.filter(p => p.status === "open");

    const totalPnL = closedTrades.reduce((sum, p) => sum + (p.pnl || 0), 0);
    const winningTrades = closedTrades.filter(p => (p.pnl || 0) > 0);
    const losingTrades = closedTrades.filter(p => (p.pnl || 0) < 0);

    const grossProfit = winningTrades.reduce((sum, p) => sum + (p.pnl || 0), 0);
    const grossLoss = Math.abs(losingTrades.reduce((sum, p) => sum + (p.pnl || 0), 0));

    const avgWin = winningTrades.length > 0 ? grossProfit / winningTrades.length : 0;
    const avgLoss = losingTrades.length > 0 ? grossLoss / losingTrades.length : 0;

    const winRate = closedTrades.length > 0
      ? (winningTrades.length / closedTrades.length) * 100
      : 0;

    const profitFactor = grossLoss > 0 ? grossProfit / grossLoss : grossProfit > 0 ? Infinity : 0;

    const totalFees = closedTrades.reduce((sum, p) => sum + (p.fees || 0), 0);

    return {
      totalPnL,
      winRate,
      totalTrades: closedTrades.length,
      winningTrades: winningTrades.length,
      losingTrades: losingTrades.length,
      grossProfit,
      grossLoss,
      avgWin,
      avgLoss,
      profitFactor,
      totalFees,
      openPositions: openTrades.length,
      bestTrade: closedTrades.length > 0 ? Math.max(...closedTrades.map(p => p.pnl || 0)) : 0,
      worstTrade: closedTrades.length > 0 ? Math.min(...closedTrades.map(p => p.pnl || 0)) : 0,
    };
  }, [filteredPositions]);

  const periodLabels = {
    week: "Last 7 Days",
    month: "Last Month",
    quarter: "Last Quarter",
    year: "Last Year",
    ytd: "Year to Date",
    all: "All Time"
  };

  const isLoading = loadingPositions;

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
                <SelectContent>
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
              : "border-transparent text-slate-400 hover:text-slate-300"
          }`}
        >
          Performance
        </button>
        <button
          onClick={() => setActiveTab("taxYear")}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "taxYear"
              ? "border-cyan-500 text-white"
              : "border-transparent text-slate-400 hover:text-slate-300"
          }`}
        >
          Tax Year P&L
        </button>
      </div>

      {activeTab === "taxYear" ? (
        <TaxYearReport />
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
        portfolio={portfolio}
      />
    </div>
  );
}
