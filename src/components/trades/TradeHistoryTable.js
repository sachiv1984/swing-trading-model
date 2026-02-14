import { useState } from "react";
import { format } from "date-fns";
import { TrendingUp, TrendingDown, ChevronDown, ChevronRight } from "lucide-react";
import { DataTable, TableHeader, TableHead, TableBody, TableRow, TableCell } from "../ui/DataTable";
import { cn } from "../../lib/utils";

export default function TradeHistoryTable({ trades }) {
  const [expandedRows, setExpandedRows] = useState(new Set());
  
  if (!trades || trades.length === 0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center">
        <p className="text-slate-500">No trade history yet</p>
      </div>
    );
  }

  // ✅ DEBUG: Log first trade to see structure
  console.log('First trade:', trades[0]);
  console.log('Trades with notes/tags:', trades.filter(t => t.entry_note || t.exit_note || (t.tags && t.tags.length > 0)).length);

  // ✅ NEW: Exit reason styling
  const exitReasonLabels = {
    "Stop Loss Hit": "Stop Hit",
    "Manual Exit": "Manual",
    "Target Reached": "Target",
    "Risk-Off Signal": "Risk Off",
    "Trailing Stop": "Trailing",
    "Partial Profit Taking": "Partial"
  };

  const exitReasonColors = {
    "Stop Loss Hit": "bg-rose-500/20 text-rose-400 border-rose-500/30",
    "Manual Exit": "bg-violet-500/20 text-violet-400 border-violet-500/30",
    "Target Reached": "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    "Risk-Off Signal": "bg-amber-500/20 text-amber-400 border-amber-500/30",
    "Trailing Stop": "bg-cyan-500/20 text-cyan-400 border-cyan-500/30",
    "Partial Profit Taking": "bg-blue-500/20 text-blue-400 border-blue-500/30"
  };

  // ✅ NEW: Toggle row expansion
  const toggleRow = (id) => {
    console.log('Toggling row:', id);
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
      console.log('Collapsed row:', id);
    } else {
      newExpanded.add(id);
      console.log('Expanded row:', id);
    }
    setExpandedRows(newExpanded);
  };

  return (
    <DataTable>
      <TableHeader>
        <TableHead>Ticker</TableHead>
        <TableHead>Entry Date</TableHead>
        <TableHead>Exit Date</TableHead>
        <TableHead className="text-right">P&L</TableHead>
        <TableHead className="text-right">% P&L</TableHead>
        <TableHead>Exit Reason</TableHead>
      </TableHeader>
      <TableBody>
        {trades.map((trade, idx) => {
          const isProfit = trade.pnl >= 0;
          const tradeId = trade.id || idx;
          const isExpanded = expandedRows.has(tradeId);
          const hasNotes = trade.entry_note || trade.exit_note;
          const hasTags = trade.tags && trade.tags.length > 0;
          const hasExpandableContent = hasNotes || hasTags;
          
          return (
            <>
              {/* ✅ Main Row - Clickable if has notes/tags */}
              <TableRow 
                key={tradeId}
                onClick={() => hasExpandableContent && toggleRow(tradeId)}
                className={cn(
                  hasExpandableContent && "cursor-pointer hover:bg-slate-800/50 transition-colors"
                )}
              >
                <TableCell>
                  <div className="flex items-center gap-2">
                    {/* ✅ NEW: Chevron icon if expandable */}
                    {hasExpandableContent && (
                      isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-slate-400" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-slate-400" />
                      )
                    )}
                    <span className="font-medium text-white">{trade.ticker}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                      {trade.market}
                    </span>
                  </div>
                </TableCell>
                <TableCell className="text-slate-400">
                  {format(new Date(trade.entry_date), "MMM d, yyyy")}
                </TableCell>
                <TableCell className="text-slate-400">
                  {format(new Date(trade.exit_date), "MMM d, yyyy")}
                </TableCell>
                <TableCell className="text-right">
                  <div className={cn(
                    "inline-flex items-center gap-1.5 font-medium",
                    isProfit ? "text-emerald-400" : "text-rose-400"
                  )}>
                    {isProfit ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    £{Math.abs(trade.pnl).toFixed(2)}
                  </div>
                </TableCell>
                <TableCell className="text-right">
                  <span className={cn("font-medium", isProfit ? "text-emerald-400" : "text-rose-400")}>
                    {isProfit ? "+" : ""}{trade.pnl_pct.toFixed(2)}%
                  </span>
                </TableCell>
                <TableCell>
                  {/* ✅ NEW: Styled exit reason badges */}
                  <span className={cn(
                    "text-xs px-2.5 py-1 rounded-full border",
                    exitReasonColors[trade.exit_reason] || "bg-slate-800 text-slate-400 border-slate-700"
                  )}>
                    {exitReasonLabels[trade.exit_reason] || trade.exit_reason || "Unknown"}
                  </span>
                </TableCell>
              </TableRow>
              
              {/* ✅ NEW: Expanded Row - Shows notes and tags */}
              {isExpanded && hasExpandableContent && (
                <TableRow key={`${tradeId}-details`} className="bg-slate-800/30">
                  <TableCell colSpan={6} className="p-6">
                    <div className="space-y-4">
                      {/* Entry Note */}
                      {trade.entry_note && (
                        <div className="space-y-2">
                          <h4 className="text-xs font-medium text-cyan-400">Entry Note</h4>
                          <p className="text-sm text-slate-300 whitespace-pre-wrap bg-slate-800/50 p-3 rounded-lg border border-slate-700/30">
                            {trade.entry_note}
                          </p>
                        </div>
                      )}
                      
                      {/* Exit Note */}
                      {trade.exit_note && (
                        <div className="space-y-2">
                          <h4 className="text-xs font-medium text-rose-400">Exit Note</h4>
                          <p className="text-sm text-slate-300 whitespace-pre-wrap bg-slate-800/50 p-3 rounded-lg border border-slate-700/30">
                            {trade.exit_note}
                          </p>
                        </div>
                      )}
                      
                      {/* Tags */}
                      {hasTags && (
                        <div className="space-y-2">
                          <h4 className="text-xs font-medium text-violet-400">Tags</h4>
                          <div className="flex flex-wrap gap-2">
                            {trade.tags.map((tag) => (
                              <span
                                key={tag}
                                className="px-3 py-1 text-xs rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                              >
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
