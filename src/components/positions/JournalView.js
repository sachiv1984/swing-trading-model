import { useState } from "react";
import { format } from "date-fns";
import { TrendingUp, TrendingDown, ChevronDown, ChevronUp, Search, Tag, X, Calendar } from "lucide-react";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";

export default function JournalView({ positions, availableTags }) {
  const [searchText, setSearchText] = useState("");
  const [selectedTags, setSelectedTags] = useState([]);
  const [showTagDropdown, setShowTagDropdown] = useState(false);
  const [winLossFilter, setWinLossFilter] = useState("all");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [expandedEntry, setExpandedEntry] = useState(null);

  // Filter positions
  const filteredPositions = positions.filter(pos => {
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

  const handleTagToggle = (tag) => {
    setSelectedTags(prev => 
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

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
              value={winLossFilter}
              onChange={(e) => setWinLossFilter(e.target.value)}
              className="px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white text-sm"
            >
              <option value="all">All Trades</option>
              <option value="win">Winners</option>
              <option value="loss">Losers</option>
            </select>

            {/* Date Range */}
            <div className="flex gap-2 flex-1">
              <div className="relative flex-1">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="bg-slate-800/50 border-slate-700 text-white pl-10"
                  placeholder="From"
                />
              </div>
              <div className="relative flex-1">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  type="date"
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
          <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center">
            <p className="text-slate-500">No journal entries found</p>
          </div>
        ) : (
          filteredPositions.map((position) => {
            const pnl = position.pnl || ((position.current_price || position.entry_price) - position.entry_price) * position.shares;
            const pnlPercent = position.pnl_percent || ((position.current_price || position.entry_price) - position.entry_price) / position.entry_price * 100;
            const isProfit = pnl >= 0;
            const isClosed = position.status === "closed";
            const isExpanded = expandedEntry === position.id;
            const currencySymbol = position.market === "UK" ? "£" : "$";

            return (
              <motion.div
                key={position.id}
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
                        <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                          {position.market}
                        </span>
                        {isClosed && (
                          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-400">
                            CLOSED
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-slate-400">
                        {format(new Date(position.entry_date), "MMM d, yyyy")}
                      </p>
                    </div>
                  </div>
                  
                  <div className={cn(
                    "px-3 py-1 rounded-lg border flex items-center gap-1.5 font-medium",
                    isProfit 
                      ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
                      : "bg-rose-500/20 text-rose-400 border-rose-500/30"
                  )}>
                    {isProfit ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    <span>{currencySymbol}{Math.abs(pnl).toFixed(2)}</span>
                    <span className="text-xs opacity-70">({pnlPercent.toFixed(1)}%)</span>
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
                      onClick={() => setExpandedEntry(isExpanded ? null : position.id)}
                      className="flex items-center gap-2 text-sm font-medium text-slate-300 hover:text-white transition-colors w-full"
                    >
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      Exit Details
                      {position.exit_date && (
                        <span className="text-xs text-slate-500 ml-auto">
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
              </motion.div>
            );
          })
        )}
      </div>

      {filteredPositions.length > 0 && (
        <p className="text-center text-sm text-slate-500">
          Showing {filteredPositions.length} of {positions.length} entries
        </p>
      )}
    </div>
  );
}
