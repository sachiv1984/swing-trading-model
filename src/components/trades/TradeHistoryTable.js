import { useState, useMemo } from "react";
import { format } from "date-fns";
import { TrendingUp, TrendingDown, ChevronDown, ChevronRight, ArrowUpDown, ArrowUp, ArrowDown } from "lucide-react";
import { DataTable, TableHeader, TableHead, TableBody, TableRow, TableCell } from "../ui/DataTable";
import { cn } from "../../lib/utils";
import PlanVsReality from "./PlanVsReality";
import TradeDebrief from "./TradeDebrief";

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
  if (r === null) return "text-slate-600 dark:text-slate-400";
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
  if (pct === null || pct === undefined) return "text-slate-600 dark:text-slate-400";
  if (pct < 0) return "text-emerald-400";
  if (pct > 0) return "text-rose-400";
  return "text-slate-300";
}

// ─────────────────────────────────────────────────────────────────────────────
// Fee Drag helpers
// Spec: ST-09 — fee_drag_pct = exit_fees / gross_proceeds * 100
// Always non-negative. Amber tone — fee drag is always a cost.
// ─────────────────────────────────────────────────────────────────────────────

function formatFeeDrag(pct) {
  if (pct === null || pct === undefined) return "—";
  return `+${pct.toFixed(2)}%`;
}

// ─────────────────────────────────────────────────────────────────────────────

const SORT_NONE = "none";
const SORT_ASC  = "asc";
const SORT_DESC = "desc";

const exitReasonLabels = {
  // Title-case values (position_manager.py)
  "Stop Loss Hit":        "Stop Hit",
  "Manual Exit":          "Manual",
  "Target Reached":       "Target",
  "Risk-Off Signal":      "Risk Off",
  "Trailing Stop":        "Trailing",
  "Partial Profit Taking":"Partial",
  // Snake-case aliases (seed data / legacy DB rows)
  "stop_hit":             "Stop Hit",
  "manual":               "Manual",
  "manual_exit":          "Manual",
  "target":               "Target",
  "target_reached":       "Target",
  "risk_off":             "Risk Off",
  "risk_off_signal":      "Risk Off",
  "market_regime":        "Risk Off",
  "trailing_stop":        "Trailing",
  "partial":              "Partial",
  "partial_profit_taking":"Partial",
};

const exitReasonColors = {
  // Title-case values
  "Stop Loss Hit":        "bg-rose-500/20 text-rose-400 border-rose-500/30",
  "Manual Exit":          "bg-violet-500/20 text-violet-400 border-violet-500/30",
  "Target Reached":       "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  "Risk-Off Signal":      "bg-amber-500/20 text-amber-400 border-amber-500/30",
  "Trailing Stop":        "bg-cyan-500/20 text-cyan-400 border-cyan-500/30",
  "Partial Profit Taking":"bg-blue-500/20 text-blue-400 border-blue-500/30",
  // Snake-case aliases
  "stop_hit":             "bg-rose-500/20 text-rose-400 border-rose-500/30",
  "manual":               "bg-violet-500/20 text-violet-400 border-violet-500/30",
  "manual_exit":          "bg-violet-500/20 text-violet-400 border-violet-500/30",
  "target":               "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  "target_reached":       "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  "risk_off":             "bg-amber-500/20 text-amber-400 border-amber-500/30",
  "risk_off_signal":      "bg-amber-500/20 text-amber-400 border-amber-500/30",
  "market_regime":        "bg-amber-500/20 text-amber-400 border-amber-500/30",
  "trailing_stop":        "bg-cyan-500/20 text-cyan-400 border-cyan-500/30",
  "partial":              "bg-blue-500/20 text-blue-400 border-blue-500/30",
  "partial_profit_taking":"bg-blue-500/20 text-blue-400 border-blue-500/30",
};

/**
 * TradeHistoryTable
 *
 * @param {object[]} trades         — from GET /trades
 * @param {object[]} tradesForCharts — from GET /analytics/metrics → trades_for_charts
 *                                    Used only for R-multiple (stop_price).
 *                                    Optional — column shows "—" for all rows when absent.
 */
// ST-10: Trade History-specific column header class override.
// Applies to all TableHead cells in this file only — DataTable.js default unchanged.
// px-2 overrides DataTable's px-6 to keep 10 columns from requiring horizontal scroll.
// whitespace-nowrap prevents multi-line headers (e.g. "Entry Date ↓").
const TH_CLASS = "font-semibold text-slate-300 tracking-wide px-2 whitespace-nowrap";
// TD_CLASS: matching compact horizontal padding for all data cells in this table.
const TD_CLASS = "px-2";

export default function TradeHistoryTable({ trades, tradesForCharts = [] }) {
  const [expandedRows, setExpandedRows] = useState(new Set());
  // ST-11: New sort states — Entry Date, Exit Date (default DESC), P&L, P&L%, Days Held
  const [entryDateSort, setEntryDateSort] = useState(SORT_NONE);
  const [exitDateSort,  setExitDateSort]  = useState(SORT_DESC);   // default: newest first
  const [pnlSort,       setPnlSort]       = useState(SORT_NONE);
  const [pnlPctSort,    setPnlPctSort]    = useState(SORT_NONE);
  const [daysHeldSort,  setDaysHeldSort]  = useState(SORT_NONE);
  // Existing sort states
  const [rSort, setRSort] = useState(SORT_NONE);
  const [slippageSort, setSlippageSort] = useState(SORT_NONE);
  const [feeDragSort, setFeeDragSort] = useState(SORT_NONE);

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

  const cycleFeeSort = () => {
    setFeeDragSort(prev =>
      prev === SORT_NONE ? SORT_ASC :
      prev === SORT_ASC  ? SORT_DESC :
      SORT_NONE
    );
  };

  // ST-11 cycle helpers
  const cycle = (setter) => setter(prev =>
    prev === SORT_NONE ? SORT_ASC :
    prev === SORT_ASC  ? SORT_DESC :
    SORT_NONE
  );

  // Apply sorts in priority order (last applied wins).
  // Spec (F-12): null/"—" values sort to the end in both directions.
  const displayTrades = useMemo(() => {
    let result = trades;

    // ST-11: Entry Date sort
    if (entryDateSort !== SORT_NONE) {
      result = [...result].sort((a, b) => {
        const cmp = a.entry_date < b.entry_date ? -1 : a.entry_date > b.entry_date ? 1 : 0;
        return entryDateSort === SORT_ASC ? cmp : -cmp;
      });
    }

    // ST-11: Exit Date sort (default SORT_DESC — most recent first)
    if (exitDateSort !== SORT_NONE) {
      result = [...result].sort((a, b) => {
        const cmp = a.exit_date < b.exit_date ? -1 : a.exit_date > b.exit_date ? 1 : 0;
        return exitDateSort === SORT_ASC ? cmp : -cmp;
      });
    }

    // ST-11: P&L GBP sort
    if (pnlSort !== SORT_NONE) {
      result = [...result].sort((a, b) =>
        pnlSort === SORT_ASC ? (a.pnl ?? 0) - (b.pnl ?? 0) : (b.pnl ?? 0) - (a.pnl ?? 0)
      );
    }

    // ST-11: P&L % sort
    if (pnlPctSort !== SORT_NONE) {
      result = [...result].sort((a, b) =>
        pnlPctSort === SORT_ASC
          ? (a.pnl_pct ?? 0) - (b.pnl_pct ?? 0)
          : (b.pnl_pct ?? 0) - (a.pnl_pct ?? 0)
      );
    }

    // ST-11: Days Held sort — null to end
    if (daysHeldSort !== SORT_NONE) {
      result = [...result].sort((a, b) => {
        const da = a.holding_days ?? null;
        const db = b.holding_days ?? null;
        if (da === null && db === null) return 0;
        if (da === null) return 1;
        if (db === null) return -1;
        return daysHeldSort === SORT_ASC ? da - db : db - da;
      });
    }

    // Existing: R-multiple sort
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

    // Existing: Slippage sort
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

    // Existing: Fee Drag sort
    if (feeDragSort !== SORT_NONE) {
      result = [...result].sort((a, b) => {
        const fa = a.fee_drag_pct ?? null;
        const fb = b.fee_drag_pct ?? null;
        if (fa === null && fb === null) return 0;
        if (fa === null) return 1;
        if (fb === null) return -1;
        return feeDragSort === SORT_ASC ? fa - fb : fb - fa;
      });
    }

    return result;
  }, [trades, entryDateSort, exitDateSort, pnlSort, pnlPctSort, daysHeldSort,
      rSort, rMap, slippageSort, feeDragSort]);

  if (!trades || trades.length === 0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center">
        <p className="text-slate-600 dark:text-slate-400">No trade history yet</p>
      </div>
    );
  }

  // Sort icon helper — returns an arrow icon component for a given sort state
  const SortIcon = ({ state, color = "text-cyan-400" }) => {
    if (state === SORT_ASC)  return <ArrowUp   className={`w-3 h-3 ml-1 inline ${color}`} />;
    if (state === SORT_DESC) return <ArrowDown  className={`w-3 h-3 ml-1 inline ${color}`} />;
    return <ArrowUpDown className="w-3 h-3 ml-1 inline text-slate-500" />;
  };

  // Aliases for backwards compatibility with existing sort icons
  const RSortIcon       = () => <SortIcon state={rSort} />;
  const SlippageSortIcon = () => <SortIcon state={slippageSort} />;
  const FeeDragSortIcon  = () => <SortIcon state={feeDragSort} color="text-amber-400" />;

  return (
    <DataTable>
      {/* ST-10: Trade History-specific header override — font-semibold text-slate-300 tracking-wide */}
      <TableHeader>
        <TableHead className={TH_CLASS}>Ticker</TableHead>
        {/* ST-11: Entry Date — sortable */}
        <TableHead
          className={cn(TH_CLASS, "cursor-pointer select-none hover:text-white transition-colors")}
          onClick={() => cycle(setEntryDateSort)}
        >
          Entry Date <SortIcon state={entryDateSort} />
        </TableHead>
        {/* ST-11: Exit Date — sortable, default DESC (newest first) */}
        <TableHead
          className={cn(TH_CLASS, "cursor-pointer select-none hover:text-white transition-colors")}
          onClick={() => cycle(setExitDateSort)}
        >
          Exit Date <SortIcon state={exitDateSort} />
        </TableHead>
        {/* ST-11: P&L GBP — sortable */}
        <TableHead
          className={cn(TH_CLASS, "text-right cursor-pointer select-none hover:text-white transition-colors")}
          onClick={() => cycle(setPnlSort)}
        >
          P&L <SortIcon state={pnlSort} />
        </TableHead>
        {/* ST-11: P&L % — sortable */}
        <TableHead
          className={cn(TH_CLASS, "text-right cursor-pointer select-none hover:text-white transition-colors")}
          onClick={() => cycle(setPnlPctSort)}
        >
          % P&L <SortIcon state={pnlPctSort} />
        </TableHead>
        <TableHead className={TH_CLASS}>Exit Reason</TableHead>
        {/* ST-11: Days Held — analytical, hidden below 2xl */}
        <TableHead
          className={cn(TH_CLASS, "text-right cursor-pointer select-none hover:text-white transition-colors")}
          onClick={() => cycle(setDaysHeldSort)}
        >
          Days <SortIcon state={daysHeldSort} />
        </TableHead>
        {/* ST-14: Slippage column — analytical, hidden below 2xl */}
        <TableHead
          className={cn(TH_CLASS, "text-right cursor-pointer select-none hover:text-white transition-colors")}
          onClick={cycleSlippageSort}
          title="Entry deviation: fill price vs limit price at entry. Null when fill price not recorded."
        >
          Slippage <SlippageSortIcon />
        </TableHead>
        {/* ST-09: Fee Drag % column — analytical, hidden below 2xl */}
        <TableHead
          className={cn(TH_CLASS, "text-right cursor-pointer select-none hover:text-white transition-colors")}
          onClick={cycleFeeSort}
          title="Fee Drag % = Exit fees / Gross proceeds × 100. Measures the proportion of gross sale proceeds consumed by broker exit fees."
        >
          Fee Drag % <FeeDragSortIcon />
        </TableHead>
        {/* BLG-FEAT-02: R-Multiple column — analytical, hidden below 2xl */}
        <TableHead
          className={cn(TH_CLASS, "text-right cursor-pointer select-none hover:text-white transition-colors")}
          onClick={cycleRSort}
        >
          R-Multiple <RSortIcon />
        </TableHead>
        {/* ST-03 (EPIC-02, v6.0): Net R column — visible only when trade has cost data */}
        <TableHead
          className={cn(TH_CLASS, "text-right")}
          title="Net-of-costs R-multiple: (P&L − commission − spread) / initial risk. Only shown when costs recorded."
        >
          Net R
        </TableHead>
      </TableHeader>

      <TableBody>
        {displayTrades.map((trade, idx) => {
          const isProfit  = trade.pnl >= 0;
          const tradeId   = trade.id || idx;
          const isExpanded = expandedRows.has(tradeId);
          const hasNotes  = trade.entry_note || trade.exit_note;
          const hasTags   = trade.tags && trade.tags.length > 0;
          const hasExpandableContent = hasNotes || hasTags || !!trade.id;

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
                <TableCell className={TD_CLASS}>
                  <div className="flex items-center gap-2">
                    {hasExpandableContent && (
                      isExpanded
                        ? <ChevronDown  className="w-4 h-4 text-slate-400" />
                        : <ChevronRight className="w-4 h-4 text-slate-400" />
                    )}
                    <span className="font-medium text-white">{trade.ticker?.replace(".L", "")}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-700">
                      {trade.market}
                    </span>
                  </div>
                </TableCell>

                {/* Entry date */}
                <TableCell className={cn(TD_CLASS, "text-slate-600 dark:text-slate-400")}>
                  {format(new Date(trade.entry_date), "d MMM yy")}
                </TableCell>

                {/* Exit date */}
                <TableCell className={cn(TD_CLASS, "text-slate-600 dark:text-slate-400")}>
                  {format(new Date(trade.exit_date), "d MMM yy")}
                </TableCell>

                {/* P&L */}
                <TableCell className={cn(TD_CLASS, "text-right")}>
                  <div className={cn(
                    "inline-flex items-center gap-1.5 font-medium",
                    isProfit ? "text-emerald-400" : "text-rose-400"
                  )}>
                    {isProfit ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    £{Math.abs(trade.pnl).toFixed(2)}
                  </div>
                </TableCell>

                {/* % P&L */}
                <TableCell className={cn(TD_CLASS, "text-right")}>
                  <span className={cn("font-medium", isProfit ? "text-emerald-400" : "text-rose-400")}>
                    {isProfit ? "+" : ""}{trade.pnl_pct.toFixed(2)}%
                  </span>
                </TableCell>

                {/* Exit reason — primary, always visible */}
                <TableCell className={TD_CLASS}>
                  <span className={cn(
                    "text-xs px-2.5 py-1 rounded-full border",
                    exitReasonColors[trade.exit_reason] || "bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-700"
                  )}>
                    {exitReasonLabels[trade.exit_reason] || trade.exit_reason || "Unknown"}
                  </span>
                </TableCell>

                {/* Days Held — ST-11 — analytical, hidden below 2xl */}
                <TableCell className={cn(TD_CLASS, "text-right")}>
                  <span className="text-slate-600 dark:text-slate-400 tabular-nums">
                    {trade.holding_days != null ? trade.holding_days : "—"}
                  </span>
                </TableCell>

                {/* Slippage — ST-14 — analytical, hidden below 2xl */}
                <TableCell className={cn(TD_CLASS, "text-right")}>
                  <span className={cn("font-medium tabular-nums", slippageColour(trade.slippage_pct))}>
                    {formatSlippage(trade.slippage_pct)}
                  </span>
                </TableCell>

                {/* Fee Drag % — ST-09 — analytical, hidden below 2xl */}
                <TableCell className={cn(TD_CLASS, "text-right")}>
                  <span className={cn(
                    "font-medium tabular-nums",
                    trade.fee_drag_pct != null ? "text-amber-400" : "text-slate-600 dark:text-slate-400"
                  )}>
                    {formatFeeDrag(trade.fee_drag_pct)}
                  </span>
                </TableCell>

                {/* R-Multiple — BLG-FEAT-02 — analytical, hidden below 2xl */}
                <TableCell className={cn(TD_CLASS, "text-right")}>
                  <span className={cn("font-medium tabular-nums", rClass)}>
                    {rText}
                  </span>
                </TableCell>

                {/* Net R — ST-03 (EPIC-02, v6.0) — visible only when cost data present */}
                <TableCell className={cn(TD_CLASS, "text-right")}>
                  {trade.net_r_multiple != null ? (
                    <span className={cn("font-medium tabular-nums", trade.net_r_multiple > 0 ? "text-emerald-400" : trade.net_r_multiple < 0 ? "text-rose-400" : "text-slate-300")}>
                      {(trade.net_r_multiple > 0 ? "+" : "") + trade.net_r_multiple.toFixed(2)}R
                    </span>
                  ) : (
                    <span className="text-slate-600">—</span>
                  )}
                </TableCell>
              </TableRow>

              {/* Expanded journal row — colSpan 11 (ST-03 added Net R column) */}
              {isExpanded && hasExpandableContent && (
                <TableRow key={`${tradeId}-details`} className="bg-slate-900/50 border-t-2 border-slate-700/50">
                  <TableCell colSpan={11} className="!p-0">
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

                      {tradeId && <PlanVsReality tradeId={tradeId} />}
                      {tradeId && <TradeDebrief tradeId={tradeId} />}
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