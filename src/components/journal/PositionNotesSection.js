import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { TrendingUp, TrendingDown, ChevronDown, ChevronUp, Search, Tag, X, Calendar, NotebookPen, Plus } from "lucide-react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import DataState from "../ui/DataState";
import OnwardLink from "../ui/OnwardLink";
import { cn } from "../../lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { api, base44 } from "../../api/base44Client";
import { formatCurrency, formatPercent } from "../../lib/format";
import { tickerMatches } from "../../lib/journalFilter";

// Journal → Position notes section (journal.md v1.1 §4; ST-05, BLG-FE-258,
// EPIC-02, v9.17). The former Positions Journal View (positions.md §Journal
// View), moved here. Open positions come from GET /positions (open only);
// closed positions from GET /trades, which carries entry_note, exit_note and
// tags (trade_endpoints.md) — user ruling 2026-11-16, journal.md v1.1.
// Both `pnl` fields are GBP (position_service.py, trade_endpoints.md), so the
// P&L badge is formatted in GBP for every market. GET /positions returns UK
// tickers without ".L" (position_service display_ticker) and GET /trades with
// it, so closed cards drop ".L" too and one stock reads the same on both.

function toOpenEntry(p) {
  return { ...p, key: `open-${p.id}`, status: "open" };
}

function toClosedEntry(t) {
  return {
    ...t,
    key: `closed-${t.id}`,
    ticker: String(t.ticker ?? "").replace(/\.L$/i, ""),
    status: "closed",
    pnl_percent: t.pnl_percent ?? t.pnl_pct,
    tags: Array.isArray(t.tags) ? t.tags : [],
  };
}

export default function PositionNotesSection({ ticker = "", onCount, onClearTicker }) {
  // Shared caches: ['positions'] with the Positions page (and its
  // invalidations), ['trades'] with Trade History and Reflections.
  const positionsQuery = useQuery({
    queryKey: ["positions"],
    queryFn: () => base44.entities.Position.list("-entry_date"),
  });
  const tradesQuery = useQuery({
    queryKey: ["trades"],
    queryFn: () => api.trades.list(),
  });

  const isLoading = positionsQuery.isLoading || tradesQuery.isLoading;
  const isError = positionsQuery.isError || tradesQuery.isError;

  const positions = useMemo(() => {
    const open = (Array.isArray(positionsQuery.data) ? positionsQuery.data : []).map(toOpenEntry);
    const closed = (tradesQuery.data?.trades || []).map(toClosedEntry);
    // Most recently entered first (positions.md §Journal View).
    return [...open, ...closed].sort((a, b) => String(b.entry_date || "").localeCompare(String(a.entry_date || "")));
  }, [positionsQuery.data, tradesQuery.data]);

  const availableTags = useMemo(
    () => [...new Set(positions.flatMap((p) => p.tags || []))].sort(),
    [positions]
  );

  const [searchText, setSearchText] = useState("");
  const [selectedTags, setSelectedTags] = useState([]);
  const [showTagDropdown, setShowTagDropdown] = useState(false);
  const [winLossFilter, setWinLossFilter] = useState("all");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [expandedEntry, setExpandedEntry] = useState(null);

  // Filter positions (the shared ticker filter applies on top, AND)
  const filteredPositions = positions.filter(pos => {
    if (!tickerMatches(pos.ticker, ticker)) return false;

    // Text search in notes
    if (searchText) {
      const searchLower = searchText.toLowerCase();
      const hasInEntry = pos.entry_note?.toLowerCase().includes(searchLower);
      const hasInExit = pos.exit_note?.toLowerCase().includes(searchLower);
      if (!hasInEntry && !hasInExit) return false;
    }

    // Tag filter
    if (selectedTags.length > 0) {
      if (!pos.tags || !selectedTags.some(tag => pos.tags.includes(tag))) {
        return false;
      }
    }

    // Win/Loss filter
    if (winLossFilter === "win" && (pos.pnl || 0) < 0) return false;
    if (winLossFilter === "loss" && (pos.pnl || 0) >= 0) return false;

    // Date range
    if (dateFrom && pos.entry_date < dateFrom) return false;
    if (dateTo && pos.entry_date > dateTo) return false;

    return true;
  });

  const loaded = !isLoading && !isError;
  useEffect(() => {
    onCount?.(loaded ? filteredPositions.length : null);
  }, [loaded, filteredPositions.length, onCount]);

  const clearFilters = () => {
    setSearchText("");
    setSelectedTags([]);
    setWinLossFilter("all");
    setDateFrom("");
    setDateTo("");
    onClearTicker?.();
  };

  const handleTagToggle = (tag) => {
    setSelectedTags(prev => 
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  if (isLoading || isError) {
    return (
      <DataState
        loading={isLoading}
        error={isError}
        onRetry={() => {
          positionsQuery.refetch();
          tradesQuery.refetch();
        }}
        errorHeading="Unable to load position notes"
        errorBody="Please try again."
      />
    );
  }

  if (positions.length === 0) {
    return (
      <div
        data-testid="notes-empty"
        className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center"
      >
        <NotebookPen className="w-10 h-10 text-slate-600 mx-auto mb-3" />
        <p className="text-slate-600 dark:text-slate-400 mb-4">
          No positions yet. Notes and tags you add to a position appear here.
        </p>
        <Link to="/TradeEntry">
          <Button className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0">
            <Plus className="w-4 h-4 mr-2" />
            Enter a position
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-4 space-y-4">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <Input
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="Search in notes..."
            aria-label="Search in notes"
            className="bg-slate-800/50 border-slate-700 text-white pl-10"
          />
        </div>

        <div className="flex flex-col gap-3">
          {/* Tag Filter */}
          {availableTags?.length > 0 && (
            <div className="relative">
              <button
                onClick={() => setShowTagDropdown(!showTagDropdown)}
                className="w-full flex items-center gap-2 px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white hover:bg-slate-800 transition-colors"
              >
                <Tag className="w-4 h-4 text-violet-400" />
                <span className="text-sm">
                  {selectedTags.length === 0 
                    ? "All tags" 
                    : `${selectedTags.length} selected`}
                </span>
              </button>
              
              {showTagDropdown && (
                <div className="absolute z-10 w-full mt-1 bg-slate-800 border border-slate-700 rounded-lg shadow-xl max-h-64 overflow-auto">
                  {availableTags.map((tag) => (
                    <button
                      key={tag}
                      onClick={() => handleTagToggle(tag)}
                      className={cn(
                        "w-full px-4 py-2.5 text-left text-sm transition-colors flex items-center justify-between",
                        selectedTags.includes(tag)
                          ? "bg-cyan-500/20 text-cyan-400"
                          : "text-slate-300 hover:bg-slate-700"
                      )}
                    >
                      <span>{tag}</span>
                      {selectedTags.includes(tag) && <span>✓</span>}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-3">
            {/* Win/Loss Filter */}
            <select
              aria-label="Winners or losers"
              value={winLossFilter}
              onChange={(e) => setWinLossFilter(e.target.value)}
              className="px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white text-sm"
            >
              <option value="all">All Trades</option>
              <option value="win">Winners</option>
              <option value="loss">Losers</option>
            </select>

            {/* Date Range — stacks below sm so two native date inputs fit at
                375 px without page-level horizontal scroll (journal.md JA-20). */}
            <div className="flex flex-col sm:flex-row gap-2 flex-1 min-w-0">
              <div className="relative flex-1 min-w-0">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  type="date"
                  aria-label="Entry date from"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="bg-slate-800/50 border-slate-700 text-white pl-10"
                  placeholder="From"
                />
              </div>
              <div className="relative flex-1 min-w-0">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  type="date"
                  aria-label="Entry date to"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  className="bg-slate-800/50 border-slate-700 text-white pl-10"
                  placeholder="To"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Selected Tags Pills */}
        {selectedTags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {selectedTags.map((tag) => (
              <button
                key={tag}
                onClick={() => handleTagToggle(tag)}
                className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/30 transition-colors"
              >
                {tag}
                <X className="w-3 h-3" />
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Timeline */}
      <div className="space-y-3">
        {filteredPositions.length === 0 ? (
          <div
            data-testid="notes-no-match"
            className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center"
          >
            <p className="text-slate-600 dark:text-slate-400">No positions match your filters.</p>
            <Button variant="outline" size="sm" className="mt-3" onClick={clearFilters}>
              Clear filters
            </Button>
          </div>
        ) : (
          filteredPositions.map((position) => {
            // Both sources return pnl and pnl_percent; the old native-currency
            // fallback is dropped so the GBP badge never shows a native figure.
            const pnl = position.pnl ?? 0;
            const pnlPercent = position.pnl_percent ?? 0;
            const isClosed = position.status === "closed";
            const isExpanded = expandedEntry === position.key;

            return (
              <motion.div
                key={position.key}
                data-testid="position-note-card"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-5"
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-lg font-bold text-white">{position.ticker}</h3>
                        <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-700">
                          {position.market}
                        </span>
                        {isClosed && (
                          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-600 dark:text-slate-400">
                            CLOSED
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">
                        {position.entry_date ? format(new Date(position.entry_date), "MMM d, yyyy") : "—"}
                      </p>
                    </div>
                  </div>
                  
                  <div className={cn(
                    "px-3 py-1 rounded-lg border flex items-center gap-1.5 font-medium",
                    pnl > 0
                      ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
                      : pnl < 0
                        ? "bg-rose-500/20 text-rose-400 border-rose-500/30"
                        : "bg-slate-700/30 text-slate-300 border-slate-600/30"
                  )}>
                    {pnl >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    <span>{formatCurrency(pnl, { signed: true })}</span>
                    <span className="text-xs opacity-70">({formatPercent(pnlPercent)})</span>
                  </div>
                </div>

                {/* Entry Note */}
                {position.entry_note && (
                  <div className="mb-3">
                    <h4 className="text-xs font-medium text-cyan-400 mb-2">Entry Note</h4>
                    <p className="text-sm text-slate-300 whitespace-pre-wrap bg-slate-800/50 p-3 rounded-lg border border-slate-700/30">
                      {position.entry_note}
                    </p>
                  </div>
                )}

                {/* Tags */}
                {position.tags?.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-3">
                    {position.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-3 py-1 text-xs rounded-full bg-violet-500/20 text-violet-400 border border-violet-500/30"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                {/* Exit Details (for closed positions) */}
                {isClosed && position.exit_note && (
                  <div className="border-t border-slate-700/50 pt-3 mt-3">
                    <button
                      onClick={() => setExpandedEntry(isExpanded ? null : position.key)}
                      className="flex items-center gap-2 text-sm font-medium text-slate-300 hover:text-white transition-colors w-full"
                    >
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      Exit Details
                      {position.exit_date && (
                        <span className="text-xs text-slate-600 dark:text-slate-400 ml-auto">
                          {format(new Date(position.exit_date), "MMM d, yyyy")}
                        </span>
                      )}
                    </button>
                    
                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="overflow-hidden"
                        >
                          <div className="mt-3">
                            <h4 className="text-xs font-medium text-rose-400 mb-2">Exit Note</h4>
                            <p className="text-sm text-slate-300 whitespace-pre-wrap bg-slate-800/50 p-3 rounded-lg border border-slate-700/30">
                              {position.exit_note}
                            </p>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                )}

                {/* journal.md §4: an open position links back to its row on
                    Positions; a closed one has no item link. */}
                {!isClosed && (
                  <div className="mt-3">
                    <OnwardLink
                      to={`/Positions?position=${encodeURIComponent(position.id)}`}
                      label="Open position"
                      testId="note-open-position"
                      className="text-xs"
                    />
                  </div>
                )}
              </motion.div>
            );
          })
        )}
      </div>

      {filteredPositions.length > 0 && (
        <p className="text-center text-sm text-slate-600 dark:text-slate-400">
          Showing {filteredPositions.length} of {positions.length} entries
        </p>
      )}
    </div>
  );
}
