import { format } from "date-fns";
import { TrendingUp, TrendingDown } from "lucide-react";
import { DataTable, TableHeader, TableHead, TableBody, TableRow, TableCell } from "../ui/DataTable";
import { cn } from "../../lib/utils";

export default function TradeHistoryTable({ trades }) {
  if (!trades || trades.length === 0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center">
        <p className="text-slate-500">No trade history yet</p>
      </div>
    );
  }

  const exitReasonLabels = {
    stop_hit: "Stop Hit",
    manual: "Manual",
    target: "Target",
    market_regime: "Market Regime"
  };

  const exitReasonColors = {
    stop_hit: "bg-rose-500/20 text-rose-400 border-rose-500/30",
    manual: "bg-violet-500/20 text-violet-400 border-violet-500/30",
    target: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    market_regime: "bg-amber-500/20 text-amber-400 border-amber-500/30"
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
        {trades.map((trade) => {
          const isProfit = trade.pnl >= 0;
          const currencySymbol = trade.market === "UK" ? "£" : "$";
          
          return (
            <TableRow key={trade.id}>
              <TableCell>
                <div className="flex items-center gap-2">
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
                {trade.exit_date ? format(new Date(trade.exit_date), "MMM d, yyyy") : "—"}
              </TableCell>
              <TableCell className="text-right">
                <div className={cn(
                  "inline-flex items-center gap-1.5 font-medium",
                  isProfit ? "text-emerald-400" : "text-rose-400"
                )}>
                  {isProfit ? (
                    <TrendingUp className="w-4 h-4" />
                  ) : (
                    <TrendingDown className="w-4 h-4" />
                  )}
                  {currencySymbol}{Math.abs(trade.pnl || 0).toFixed(2)}
                </div>
              </TableCell>
              <TableCell className="text-right">
                <span className={cn(
                  "font-medium",
                  isProfit ? "text-emerald-400" : "text-rose-400"
                )}>
                  {isProfit ? "+" : ""}{(trade.pnl_percent || 0).toFixed(2)}%
                </span>
              </TableCell>
              <TableCell>
                <span className={cn(
                  "text-xs px-2.5 py-1 rounded-full border",
                  exitReasonColors[trade.exit_reason] || "bg-slate-800 text-slate-400 border-slate-700"
                )}>
                  {exitReasonLabels[trade.exit_reason] || trade.exit_reason}
                </span>
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </DataTable>
  );
}
