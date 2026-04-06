import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, apiFetch } from "../api/base44Client";
import { Loader2, Filter, TrendingUp, TrendingDown, Calendar, Tag, X, Download } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { cn } from "../lib/utils";
import PageHeader from "../components/ui/PageHeader";
import StatsCard from "../components/ui/StatsCard";
import TradeHistoryTable from "../components/trades/TradeHistoryTable";
import { motion } from "framer-motion";

export default function TradeHistory() {
  const [filters, setFilters] = useState({
    market: "all",
    result: "all",
    dateFrom: "",
    dateTo: "",
  });
  const [selectedTags, setSelectedTags] = useState([]);
  const [showTagDropdown, setShowTagDropdown] = useState(false);
  const [csvExporting, setCsvExporting] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  // ── Primary trades query ────────────────────────────────────────────────────
  const { data: tradesData, isLoading } = useQuery({
    queryKey: ["trades"],
    queryFn: () => api.trades.list(),
  });

  // ── BLG-FEAT-02: Analytics metrics for R-multiple join ──────────────────────
  // Provides trades_for_charts carrying stop_price per trade (D2a).
  // Non-blocking: if this call fails the trade table still renders,
  // R-multiple column degrades to "—" for all rows (R-05).
  const { data: analyticsMetrics } = useQuery({
    queryKey: ["analyticsMetrics"],
    queryFn: async () => {
      try {
        const response = await apiFetch(`${API_URL}/analytics/metrics`);
        if (!response.ok) {
          console.warn("Analytics metrics unavailable for R-multiple column:", response.status);
          return null;
        }
        const result = await response.json();
        return result.data || null;
      } catch (error) {
        console.error("Failed to load analytics metrics (R-multiple will show —):", error);
        return null;
      }
    },
    staleTime: 5 * 60 * 1000,
    retry: false,
  });

  const trades = tradesData?.trades || [];

  // trades_for_charts: source for R-multiple join by trade id.
  // Safe-defaults to [] so TradeHistoryTable always receives a valid array.
  const tradesForCharts = analyticsMetrics?.trades_for_charts ?? [];

  // ── Tag helpers ─────────────────────────────────────────────────────────────
  const availableTags =
    Array.isArray(trades)
      ? trades
          .flatMap((t) => t.tags || [])
          .filter((tag, i, self) => self.indexOf(tag) === i)
          .sort()
      : [];

  const handleTagToggle = (tag) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  // ── Filter logic ─────────────────────────────────────────────────────────────
  const filteredTrades = trades.filter((trade) => {
    if (filters.market !== "all" && trade.market?.toUpperCase() !== filters.market) return false;
    if (filters.result === "win" && trade.pnl < 0) return false;
    if (filters.result === "loss" && trade.pnl >= 0) return false;
    if (filters.dateFrom && trade.exit_date < filters.dateFrom) return false;
    if (filters.dateTo && trade.exit_date > filters.dateTo) return false;
    if (selectedTags.length > 0) {
      if (!trade.tags || !selectedTags.some((tag) => trade.tags.includes(tag))) return false;
    }
    return true;
  });

  // ── Summary stats ─────────────────────────────────────────────────────────
  const totalPnL = filteredTrades.reduce((sum, t) => sum + (t.pnl || 0), 0);
  const winningTrades = filteredTrades.filter((t) => t.pnl >= 0);
  const losingTrades = filteredTrades.filter((t) => t.pnl < 0);
  const winRate =
    filteredTrades.length > 0 ? (winningTrades.length / filteredTrades.length) * 100 : 0;
  const avgWin =
    winningTrades.length > 0
      ? winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length
      : 0;
  const avgLoss =
    losingTrades.length > 0
      ? losingTrades.reduce((sum, t) => sum + t.pnl, 0) / losingTrades.length
      : 0;

  // ── BLG-FEAT-07: CSV Export ─────────────────────────────────────────────────
  // Spec: trade_history.md v1.1 §CSV export button; trade_endpoints.md v1.8.4
  // Triggers GET /trades/export/csv — browser-native download via anchor injection.
  // No client-side CSV generation (F-29 requirement, old ExportModal.js prototype discarded).
  const handleCsvExport = async () => {
    if (csvExporting) return;
    setCsvExporting(true);
    try {
      const response = await apiFetch(`${API_URL}/trades/export/csv`, {
        method: "GET",
        headers: { Accept: "text/csv" },
      });

      if (!response.ok) {
        const errText = await response.text().catch(() => "Unknown error");
        console.error("CSV export failed:", response.status, errText);
        alert(`Export failed (${response.status}). Please try again.`);
        return;
      }

      // Read the CSV blob and trigger a browser-native download.
      // Content-Disposition: attachment; filename="trade_history.csv" is set
      // by the server, but we set the filename explicitly here as a fallback.
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "trade_history.csv";
      document.body.appendChild(anchor);
      anchor.click();
      document.body.removeChild(anchor);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("CSV export error:", error);
      alert("Export failed. Check your connection and try again.");
    } finally {
      setCsvExporting(false);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Trade History"
        description="Review your closed positions and performance"
        actions={
          /* BLG-FEAT-07: CSV Export button in page header area (F-28).
             Spec: triggers GET /trades/export/csv, browser-native download. */
          <Button
            onClick={handleCsvExport}
            disabled={csvExporting}
            variant="outline"
            className="bg-slate-800/50 border-slate-700 text-white hover:bg-slate-700 disabled:opacity-50"
          >
            {csvExporting ? (
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Download className="w-4 h-4 mr-2" />
            )}
            {csvExporting ? "Exporting…" : "Export CSV"}
          </Button>
        }
      />

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : (
        <>
          {/* Summary stats row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
            <StatsCard
              title="Total P&L"
              value={`${totalPnL >= 0 ? "+" : ""}£${totalPnL.toFixed(2)}`}
              trend={totalPnL >= 0 ? "up" : "down"}
              icon={totalPnL >= 0 ? TrendingUp : TrendingDown}
              gradient={totalPnL >= 0 ? "emerald" : "rose"}
            />
            <StatsCard
              title="Win Rate"
              value={`${winRate.toFixed(1)}%`}
              subtitle={`${winningTrades.length}W / ${losingTrades.length}L`}
              trend={winRate >= 50 ? "up" : "down"}
              icon={winRate >= 50 ? TrendingUp : TrendingDown}
              gradient={winRate >= 50 ? "emerald" : "rose"}
            />
            <StatsCard
              title="Avg Winner"
              value={`+£${avgWin.toFixed(2)}`}
              trend="up"
              icon={TrendingUp}
              gradient="emerald"
            />
            <StatsCard
              title="Avg Loser"
              value={`-£${Math.abs(avgLoss).toFixed(2)}`}
              trend="down"
              icon={TrendingDown}
              gradient="rose"
            />
            <StatsCard
              title="Avg Entry Dev."
              value={
                tradesData?.avg_slippage_pct != null
                  ? `${tradesData.avg_slippage_pct > 0 ? "+" : ""}${tradesData.avg_slippage_pct.toFixed(2)}%`
                  : "—"
              }
              trend={tradesData?.avg_slippage_pct != null ? (tradesData.avg_slippage_pct <= 0 ? "up" : "down") : "neutral"}
              icon={tradesData?.avg_slippage_pct != null ? (tradesData.avg_slippage_pct <= 0 ? TrendingUp : TrendingDown) : TrendingUp}
              gradient={tradesData?.avg_slippage_pct != null ? (tradesData.avg_slippage_pct <= 0 ? "emerald" : "rose") : "violet"}
            />
            <StatsCard
              title="Avg Fee Drag"
              value={
                tradesData?.avg_fee_drag_pct != null
                  ? `+${tradesData.avg_fee_drag_pct.toFixed(2)}%`
                  : "—"
              }
              subtitle="Exit fees / gross proceeds"
              icon={TrendingDown}
              gradient="amber"
            />
          </div>

          {/* Filters panel */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 space-y-4"
          >
            <div className="flex items-center gap-2 text-slate-400">
              <Filter className="w-4 h-4" />
              <span className="text-sm font-medium">Filters</span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Select
                value={filters.market}
                onValueChange={(value) => setFilters({ ...filters, market: value })}
              >
                <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white">
                  <SelectValue placeholder="Market" />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="all">All Markets</SelectItem>
                  <SelectItem value="UK">UK</SelectItem>
                  <SelectItem value="US">US</SelectItem>
                </SelectContent>
              </Select>

              <Select
                value={filters.result}
                onValueChange={(value) => setFilters({ ...filters, result: value })}
              >
                <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white">
                  <SelectValue placeholder="Result" />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="all">All Results</SelectItem>
                  <SelectItem value="win">Winners</SelectItem>
                  <SelectItem value="loss">Losers</SelectItem>
                </SelectContent>
              </Select>

              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  type="date"
                  value={filters.dateFrom}
                  onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white pl-10"
                  placeholder="From"
                />
              </div>

              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  type="date"
                  value={filters.dateTo}
                  onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white pl-10"
                  placeholder="To"
                />
              </div>
            </div>

            {/* Tag filter */}
            {availableTags.length > 0 && (
              <div className="space-y-2">
                <div className="relative">
                  <button
                    onClick={() => setShowTagDropdown(!showTagDropdown)}
                    className="flex items-center gap-2 text-sm text-slate-400 hover:text-slate-200 transition-colors"
                  >
                    <Tag className="w-4 h-4" />
                    Filter by tag
                    {selectedTags.length > 0 && (
                      <span className="px-1.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-400 text-xs">
                        {selectedTags.length}
                      </span>
                    )}
                  </button>
                  {showTagDropdown && (
                    <div className="absolute top-full left-0 mt-1 z-10 min-w-48 rounded-xl bg-slate-800 border border-slate-700 shadow-xl p-2">
                      {availableTags.map((tag) => (
                        <button
                          key={tag}
                          onClick={() => handleTagToggle(tag)}
                          className={cn(
                            "w-full text-left px-3 py-2 rounded-lg text-sm transition-colors",
                            selectedTags.includes(tag)
                              ? "bg-cyan-500/20 text-cyan-400"
                              : "text-slate-300 hover:bg-slate-700"
                          )}
                        >
                          {tag}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                {selectedTags.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {selectedTags.map((tag) => (
                      <span
                        key={tag}
                        className="inline-flex items-center gap-1.5 px-3 py-1 text-xs rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                      >
                        {tag}
                        <button onClick={() => handleTagToggle(tag)}>
                          <X className="w-3 h-3" />
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>
            )}
          </motion.div>

          {/* Trade table — BLG-FEAT-02: tradesForCharts passed for R-multiple join */}
          <TradeHistoryTable trades={filteredTrades} tradesForCharts={tradesForCharts} />

          {filteredTrades.length > 0 && (
            <p className="text-center text-sm text-slate-500">
              Showing {filteredTrades.length} of {trades.length} trades
            </p>
          )}
        </>
      )}
    </div>
  );
}
