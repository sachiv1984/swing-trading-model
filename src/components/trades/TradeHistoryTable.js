import { useState, useMemo } from "react";
import { format } from "date-fns";
import { TrendingUp, TrendingDown, ChevronDown, ChevronRight, ArrowUpDown, ArrowUp, ArrowDown } from "lucide-react";
import { DataTable, TableHeader, TableHead, TableBody, TableRow, TableCell } from "../ui/DataTable";
import { cn } from "../../lib/utils";

// ─────────────────────────────────────────────────────────────────────────────
// R-multiple helpers
// Spec: trade_history.md v1.1; metrics_definitions.md v1.5.7 (Tier 1, Visualisation-Only)
// Formula: R = (exit_price - entry_price) / (entry_price - stop_price)
// Returns null when stop_price is absent or zero (denominator would be zero).
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Calculate R-multiple for a single trade chart entry.
 * @param {object} t — entry from trades_for_charts
 * @returns {number|null}
 */
function calcR(t) {
  if (!t) return null;
  const { entry_price, exit_price, stop_price } = t;
  if (!stop_price || stop_price === 0) return null;
  const denom = entry_price - stop_price;
  if (denom === 0) return null;
  return (exit_price - entry_price) / denom;
}

/**
 * Format R-multiple for display.
 * @param {number|null} r
 * @returns {string} e.g. "+2.31R" / "-0.87R" / "0.00R" / "—"
 */
function formatR(r) {
  if (r === null) return "—";
  const sign = r > 0 ? "+" : "";
  return `${sign}${r.toFixed(2)}R`;
}

/**
 * Colour class for an R-multiple value.
 * Binary profit/loss — drawdown thresholds do NOT apply here.
 */
function rColour(r) {
  if (r === null) return "text-slate-500";
  if (r > 0)  return "text-emerald-400";
  if (r < 0)  return "text-rose-400";
  return "text-slate-300";
}

// ─────────────────────────────────────────────────────────────────────────────
// Slippage helpers
// Spec: ST-14 — slippage_pct = (fill_price − entry_price) / entry_price * 100
// Negative = filled below market (favourable).
// ─────────────────────────────────────────────────────────────────────────────

function formatSlippage(pct) {
  if (pct === null || pct === undefined) return "—";
  const sign = pct > 0 ? "+" : "";
  return `${sign}${pct.toFixed(2)}%`;
}

function slippageColour(pct) {
  if (pct === null || pct === undefined) return "text-slate-500";
  if (pct < 0) return "text-emerald-400";
  if (pct > 0) return "text-rose-400";
  return "text-slate-300";
}

// ─────────────────────────────────────────────────────────────────────────────

const SORT_NONE = "none";
const SORT_ASC  = "asc";
const SORT_DESC = "desc";

const exitReasonLabels = {
  "Stop Loss Hit":        "Stop Hit",
  "Manual Exit":          "Manual",
  "Target Reached":       "Target",
  "Risk-Off Signal":      "Risk Off",
  "Trailing Stop":        "Trailing",
  "Partial Profit Taking":"Partial",
};

const exitReasonColors = {
  "Stop Loss Hit":        "bg-rose-500/20 text-rose-400 border-rose-500/30",
  "Manual Exit":          "bg-violet-500/20 text-violet-400 border-violet-500/30",
  "Target Reached":       "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  "Risk-Off Signal":      "bg-amber-500/20 text-amber-400 border-amber-500/30",
  "Trailing Stop":        "bg-cyan-500/20 text-cyan-400 border-cyan-500/30",
  "Partial Profit Taking":"bg-blue-500/20 text-blue-400 border-blue-500/30",
};

/**
 * TradeHistoryTable
 *
 * @param {object[]} trades         — from GET /trades
 * @param {object[]} tradesForCharts — from GET /analytics/metrics → trades_for_charts
 *                                    Used only for R-multiple (stop_price).
 *                                    Optional — column shows "—" for all rows when absent.
 */
export default function TradeHistoryTable({ trades, tradesForCharts = [] }) {
  const [expandedRows, setExpandedRows] = useState(new Set());
  const [rSort, setRSort] = useState(SORT_NONE);
  const [slippageSort, setSlippageSort] = useState(SORT_NONE);

  // Build a lookup map: trade id → R-multiple value (or null)
  // Joined by trade id, as spec requires (D2a).
  const rMap = useMemo(() => {
    const map = new Map();
    (tradesForCharts || []).forEach(t => {
      if (t.id != null) map.set(String(t.id), calcR(t));
    });
    return map;
  }, [tradesForCharts]);

  const toggleRow = (id) => {
    setExpandedRows(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const cycleRSort = () => {
    setRSort(prev =>
      prev === SORT_NONE ? SORT_ASC :
      prev === SORT_ASC  ? SORT_DESC :
      SORT_NONE
    );
  };

  const cycleSlippageSort = () => {
    setSlippageSort(prev =>
      prev === SORT_NONE ? SORT_ASC :
      prev === SORT_ASC  ? SORT_DESC :
      SORT_NONE
    );
  };

  // Apply R-multiple sort, then slippage sort.
  // Spec (F-12): "—" values sort to the end in both directions.
  const displayTrades = useMemo(() => {
    let result = trades;

    if (rSort !== SORT_NONE) {
      result = [...result].sort((a, b) => {
        const ra = rMap.get(String(a.id ?? ""));
        const rb = rMap.get(String(b.id ?? ""));
        if (ra === null && rb === null) return 0;
        if (ra === null) return 1;
        if (rb === null) return -1;
        return rSort === SORT_ASC ? ra - rb : rb - ra;
      });
    }

    if (slippageSort !== SORT_NONE) {
      result = [...result].sort((a, b) => {
        const sa = a.slippage_pct ?? null;
        const sb = b.slippage_pct ?? null;
        if (sa === null && sb === null) return 0;
        if (sa === null) return 1;
        if (sb === null) return -1;
        return slippageSort === SORT_ASC ? sa - sb : sb - sa;
      });
    }

    return result;
  }, [trades, rSort, rMap, slippageSort]);

  if (!trades || trades.length === 0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center">
        <p className="text-slate-500">No trade history yet</p>
      </div>
    );
  }

  // Sort icon helpers
  const RSortIcon = () => {
    if (rSort === SORT_ASC)  return <ArrowUp   className="w-3 h-3 ml-1 inline text-cyan-400" />;
    if (rSort === SORT_DESC) return <ArrowDown  className="w-3 h-3 ml-1 inline text-cyan-400" />;
    return <ArrowUpDown className="w-3 h-3 ml-1 inline text-slate-500" />;
  };

  const SlippageSortIcon = () => {
    if (slippageSort === SORT_ASC)  return <ArrowUp   className="w-3 h-3 ml-1 inline text-cyan-400" />;
    if (slippageSort === SORT_DESC) return <ArrowDown  className="w-3 h-3 ml-1 inline text-cyan-400" />;
    return <ArrowUpDown className="w-3 h-3 ml-1 inline text-slate-500" />;
  };

  return (
    <DataTable>
      <TableHeader>
        <TableHead>Ticker</TableHead>
        <TableHead>Entry Date</TableHead>
        <TableHead>Exit Date</TableHead>
        <TableHead className="text-right">P&L</TableHead>
        <TableHead className="text-right">% P&L</TableHead>
        {/* ST-14: Slippage column — sortable, "—" to end */}
        <TableHead
          className="text-right cursor-pointer select-none hover:text-slate-200 transition-colors"
          onClick={cycleSlippageSort}
          title="Entry deviation: fill price vs limit price at entry. Null when fill price not recorded."
        >
          Slippage <SlippageSortIcon />
        </TableHead>
        {/* BLG-FEAT-02: R-Multiple column — sortable, "—" to end */}
        <TableHead
          className="text-right cursor-pointer select-none hover:text-slate-200 transition-colors"
          onClick={cycleRSort}
        >
          R-Multiple <RSortIcon />
        </TableHead>
        <TableHead>Exit Reason</TableHead>
      </TableHeader>

      <TableBody>
        {displayTrades.map((trade, idx) => {
          const isProfit  = trade.pnl >= 0;
          const tradeId   = trade.id || idx;
          const isExpanded = expandedRows.has(tradeId);
          const hasNotes  = trade.entry_note || trade.exit_note;
          const hasTags   = trade.tags && trade.tags.length > 0;
          const hasExpandableContent = hasNotes || hasTags;

          // R-multiple for this row
          const rVal    = rMap.get(String(tradeId)) ?? null;
          const rText   = formatR(rVal);
          const rClass  = rColour(rVal);

          return (
            <>
              <TableRow
                key={tradeId}
                onClick={() => hasExpandableContent && toggleRow(tradeId)}
                className={cn(hasExpandableContent && "cursor-pointer hover:bg-slate-800/50 transition-colors")}
              >
                {/* Ticker + market */}
                <TableCell>
                  <div className="flex items-center gap-2">
                    {hasExpandableContent && (
                      isExpanded
                        ? <ChevronDown  className="w-4 h-4 text-slate-400" />
                        : <ChevronRight className="w-4 h-4 text-slate-400" />
                    )}
                    <span className="font-medium text-white">{trade.ticker}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                      {trade.market}
                    </span>
                  </div>
                </TableCell>

                {/* Entry date */}
                <TableCell className="text-slate-400">
                  {format(new Date(trade.entry_date), "MMM d, yyyy")}
                </TableCell>

                {/* Exit date */}
                <TableCell className="text-slate-400">
                  {format(new Date(trade.exit_date), "MMM d, yyyy")}
                </TableCell>

                {/* P&L */}
                <TableCell className="text-right">
                  <div className={cn(
                    "inline-flex items-center gap-1.5 font-medium",
                    isProfit ? "text-emerald-400" : "text-rose-400"
                  )}>
                    {isProfit ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    £{Math.abs(trade.pnl).toFixed(2)}
                  </div>
                </TableCell>

                {/* % P&L */}
                <TableCell className="text-right">
                  <span className={cn("font-medium", isProfit ? "text-emerald-400" : "text-rose-400")}>
                    {isProfit ? "+" : ""}{trade.pnl_pct.toFixed(2)}%
                  </span>
                </TableCell>

                {/* Slippage — ST-14 */}
                <TableCell className="text-right">
                  <span className={cn("font-medium tabular-nums", slippageColour(trade.slippage_pct))}>
                    {formatSlippage(trade.slippage_pct)}
                  </span>
                </TableCell>

                {/* R-Multiple — BLG-FEAT-02 */}
                <TableCell className="text-right">
                  <span className={cn("font-medium tabular-nums", rClass)}>
                    {rText}
                  </span>
                </TableCell>

                {/* Exit reason */}
                <TableCell>
                  <span className={cn(
                    "text-xs px-2.5 py-1 rounded-full border",
                    exitReasonColors[trade.exit_reason] || "bg-slate-800 text-slate-400 border-slate-700"
                  )}>
                    {exitReasonLabels[trade.exit_reason] || trade.exit_reason || "Unknown"}
                  </span>
                </TableCell>
              </TableRow>

              {/* Expanded journal row — colSpan bumped to 7 */}
              {isExpanded && hasExpandableContent && (
                <TableRow key={`${tradeId}-details`} className="bg-slate-900/50 border-t-2 border-slate-700/50">
                  <TableCell colSpan={8} className="!p-0">
                    <div className="w-full px-6 py-5 space-y-5">
                      <div className="flex items-center gap-2 pb-3 border-b border-slate-700/50">
                        <div className="w-1 h-4 bg-gradient-to-b from-cyan-500 to-violet-500 rounded-full" />
                        <h3 className="text-sm font-semibold text-slate-300">Trade Journal</h3>
                      </div>

                      {trade.entry_note && (
                        <div className="space-y-2.5">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-cyan-400" />
                            <h4 className="text-xs font-semibold uppercase tracking-wider text-cyan-400">Entry Analysis</h4>
                          </div>
                          <div className="w-full bg-slate-800/50 rounded-xl p-4 border border-slate-700/30 shadow-lg">
                            <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{trade.entry_note}</p>
                          </div>
                        </div>
                      )}

                      {trade.exit_note && (
                        <div className="space-y-2.5">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-rose-400" />
                            <h4 className="text-xs font-semibold uppercase tracking-wider text-rose-400">Exit Reflection</h4>
                          </div>
                          <div className="w-full bg-slate-800/50 rounded-xl p-4 border border-slate-700/30 shadow-lg">
                            <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{trade.exit_note}</p>
                          </div>
                        </div>
                      )}

                      {hasTags && (
                        <div className="space-y-2.5">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-violet-400" />
                            <h4 className="text-xs font-semibold uppercase tracking-wider text-violet-400">Strategy Tags</h4>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {trade.tags.map((tag) => (
                              <span
                                key={tag}
                                className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-gradient-to-r from-cyan-500/10 to-violet-500/10 text-cyan-300 border border-cyan-500/30 hover:border-cyan-400/50 transition-colors"
                              >
                                <span className="w-1 h-1 rounded-full bg-cyan-400" />
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </>
          );
        })}
      </TableBody>
    </DataTable>
  );
}