import { useState, useEffect } from "react";
import { X } from "lucide-react";
import { cn } from "../../lib/utils";

const EXIT_REASON_LABELS = {
  stop_hit: "Stop Hit",
  manual: "Manual",
  target: "Target",
  market_regime: "Risk-Off",
};

const calcRMultiple = (trade) => {
  if (!trade.stop_price || !trade.entry_price || !trade.exit_price) return null;
  const risk = Math.abs(trade.entry_price - trade.stop_price);
  if (risk === 0) return null;
  return (trade.exit_price - trade.entry_price) / risk;
};

const formatMonthTitle = (monthStr) => {
  const [year, month] = monthStr.split("-");
  return new Date(year, parseInt(month, 10) - 1, 1)
    .toLocaleDateString("en-GB", { month: "short", year: "numeric" });
};

export default function MonthlyHeatmap({ monthlyData, trades = [] }) {
  const [selectedMonth, setSelectedMonth] = useState(null);

  // Close modal on Escape key
  useEffect(() => {
    if (!selectedMonth) return;
    const handler = (e) => { if (e.key === "Escape") setSelectedMonth(null); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [selectedMonth]);

  const getColor = (pnl) => {
    if (pnl > 500) return "bg-emerald-500";
    if (pnl > 100) return "bg-emerald-400";
    if (pnl > -100) return "bg-slate-600";
    if (pnl > -500) return "bg-rose-400";
    return "bg-rose-500";
  };

  const handleTileClick = (month) => {
    if (month.trades === 0) return;
    setSelectedMonth(month);
  };

  // Trades for the selected month, filtered by exit_date
  const modalTrades = selectedMonth
    ? trades.filter(t => t.exit_date && t.exit_date.startsWith(selectedMonth.month))
    : [];
  const modalTotalPnl = modalTrades.reduce((sum, t) => sum + t.pnl, 0);

  return (
    <>
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
        <h3 className="text-lg font-semibold text-white mb-6">Monthly Performance</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {monthlyData.map((month, idx) => {
            const isTopRow = idx < 6;
            const isClickable = month.trades > 0;
            const isSelected = selectedMonth?.month === month.month;
            return (
              <div
                key={idx}
                className="group relative"
              >
                <div
                  className={cn(
                    "aspect-square rounded-lg flex flex-col items-center justify-center p-3 transition-all duration-200",
                    getColor(month.pnl),
                    isClickable
                      ? "hover:scale-105 hover:shadow-lg cursor-pointer"
                      : "cursor-default",
                    isSelected && "ring-2 ring-inset ring-violet-400"
                  )}
                  onClick={() => handleTileClick(month)}
                >
                  <p className="text-xs font-medium text-white/90">{month.month}</p>
                  <p className="text-sm font-bold text-white mt-1">
                    {month.pnl >= 0 ? "+" : ""}£{month.pnl.toFixed(0)}
                  </p>
                  <p className="text-xs text-white/70 mt-1">{month.trades} trades</p>
                </div>
                <div className={cn(
                  "absolute left-1/2 -translate-x-1/2 hidden group-hover:block pointer-events-none z-10",
                  isTopRow ? "top-full mt-2" : "bottom-full mb-2"
                )}>
                  <div className="bg-slate-900 border border-slate-700 rounded-lg p-3 text-xs whitespace-nowrap shadow-2xl backdrop-blur-sm animate-in fade-in duration-200">
                    <div className="space-y-0.5">
                      <p className="font-semibold text-white">{month.month}</p>
                      <p className={cn(
                        "font-medium",
                        month.pnl >= 0 ? "text-emerald-400" : "text-rose-400"
                      )}>
                        P&L: {month.pnl >= 0 ? "+" : ""}£{month.pnl.toFixed(2)}
                      </p>
                      <p className="text-slate-300">Trades: {month.trades}</p>
                      <p className="text-slate-300">Win Rate: {month.winRate}%</p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        <div className="flex items-center justify-center gap-4 mt-6 text-xs text-slate-600 dark:text-slate-400">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-emerald-500" />
            <span>&gt;£500</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-emerald-400" />
            <span>£100-500</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-slate-600" />
            <span>±£100</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-rose-400" />
            <span>-£100 to -£500</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-rose-500" />
            <span>&lt;-£500</span>
          </div>
        </div>
      </div>

      {/* Monthly Trades Modal */}
      {selectedMonth && (
        <div
          data-testid="heatmap-backdrop"
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedMonth(null)}
        >
          <div
            data-testid="heatmap-modal"
            className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden shadow-2xl flex flex-col"
            onClick={e => e.stopPropagation()}
          >
            {/* Modal header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-700/50">
              <h2 className="text-lg font-semibold text-white">
                Trades — {formatMonthTitle(selectedMonth.month)}
              </h2>
              <button
                data-testid="heatmap-modal-close"
                onClick={() => setSelectedMonth(null)}
                className="p-1.5 rounded-lg text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-700/50 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Summary line */}
            <div className="px-6 py-3 border-b border-slate-700/30 bg-slate-800/40">
              <p className="text-sm text-slate-300">
                <span className="font-medium text-white">{modalTrades.length}</span> trade{modalTrades.length !== 1 ? "s" : ""}
                {" · "}Total P&L:{" "}
                <span className={cn(
                  "font-medium",
                  modalTotalPnl >= 0 ? "text-emerald-400" : "text-rose-400"
                )}>
                  {modalTotalPnl >= 0 ? "+" : ""}£{modalTotalPnl.toFixed(2)}
                </span>
              </p>
            </div>

            {/* Trade table */}
            {/* ST-12 (BLG-FE-94, EPIC-04, v8.5): overflow-x-auto added --
                per analytics.md's "All tables support horizontal scroll on
                small screens" spec, missing here (4 sibling table
                components already had it). */}
            <div className="overflow-y-auto overflow-x-auto flex-1">
              <table className="w-full">
                <thead className="bg-slate-800/70 sticky top-0">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">Ticker</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">Exit Date</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">P&L</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">R-Multiple</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">Exit Reason</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/30">
                  {modalTrades.map((trade, idx) => {
                    const r = calcRMultiple(trade);
                    return (
                      <tr key={idx} className="hover:bg-slate-800/30">
                        <td className="px-4 py-3 text-sm font-medium text-white">{trade.ticker?.replace(".L", "")}</td>
                        <td className="px-4 py-3 text-sm text-slate-300">
                          {new Date(trade.exit_date).toLocaleDateString("en-GB")}
                        </td>
                        <td className={cn(
                          "px-4 py-3 text-sm text-right font-medium",
                          trade.pnl >= 0 ? "text-emerald-400" : "text-rose-400"
                        )}>
                          {trade.pnl >= 0 ? "+" : ""}£{trade.pnl.toFixed(2)}
                        </td>
                        <td className="px-4 py-3 text-sm text-right text-slate-300">
                          {r !== null
                            ? <span className={r >= 0 ? "text-emerald-400" : "text-rose-400"}>{r.toFixed(2)}R</span>
                            : <span className="text-slate-600 dark:text-slate-400">—</span>
                          }
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-300">
                          {EXIT_REASON_LABELS[trade.exit_reason] || trade.exit_reason || "Manual"}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
