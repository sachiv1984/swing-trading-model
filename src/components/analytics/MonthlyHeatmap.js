import { useState, useEffect, useRef } from "react";
import { X } from "lucide-react";
import { cn } from "../../lib/utils";
import { formatCurrency, formatR } from "../../lib/format";
import { exitReasonLabel } from "../../constants/exitReasons";

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
  // ST-01 (BLG-FE-311, v9.18): the month detail is a modal dialog. Focus
  // moves to its close button on open, Tab stays inside it, and focus
  // returns to the tile that opened it on close.
  const modalRef = useRef(null);
  const closeRef = useRef(null);
  const openerRef = useRef(null);

  // Close modal on Escape key; keep Tab inside it. The listener is on the
  // window, not the dialog, so the trap holds even after a click on
  // non-focusable text inside the dialog has moved focus elsewhere.
  useEffect(() => {
    if (!selectedMonth) return;
    const handler = (e) => {
      if (e.key === "Escape") setSelectedMonth(null);
      else trapTab(e);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [selectedMonth]); // eslint-disable-line react-hooks/exhaustive-deps

  const isOpen = !!selectedMonth;
  useEffect(() => {
    if (!isOpen) return undefined;
    closeRef.current?.focus();
    const opener = openerRef.current;
    return () => {
      if (opener && document.contains(opener)) opener.focus();
    };
  }, [isOpen]);

  const trapTab = (e) => {
    if (e.key !== "Tab" || !modalRef.current) return;
    const focusable = Array.from(
      modalRef.current.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
    ).filter((el) => !el.disabled);
    if (focusable.length === 0) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (!modalRef.current.contains(document.activeElement)) {
      e.preventDefault();
      (e.shiftKey ? last : first).focus();
    } else if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  };

  const getColor = (pnl) => {
    // ST-08 (v9.17): tile fills carry white text, so each one meets 4.5:1 in
    // both themes (design_system.md §Coloured Button Fills shades).
    if (pnl > 500) return "bg-emerald-800";
    if (pnl > 100) return "bg-emerald-700";
    if (pnl > -100) return "bg-slate-600";
    if (pnl > -500) return "bg-rose-700";
    return "bg-rose-800";
  };

  const handleTileClick = (month, e) => {
    if (month.trades === 0) return;
    openerRef.current = e?.currentTarget ?? null;
    setSelectedMonth(month);
  };

  // Trades for the selected month, filtered by exit_date
  const modalTrades = selectedMonth
    ? trades.filter(t => t.exit_date && t.exit_date.startsWith(selectedMonth.month))
    : [];
  const modalTotalPnl = modalTrades.reduce((sum, t) => sum + t.pnl, 0);

  return (
    <>
      <div className="rounded-2xl bg-app-raised border border-app-line p-6 backdrop-blur-sm">
        <h3 className="text-lg font-semibold text-app-fg mb-6">Monthly Performance</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {monthlyData.map((month, idx) => {
            const isTopRow = idx < 6;
            const isClickable = month.trades > 0;
            const isSelected = selectedMonth?.month === month.month;
            // ST-01 (BLG-FE-311, v9.18): a tile with trades is a button
            // (Tab, Enter/Space); a tile with none stays static.
            const Tile = isClickable ? "button" : "div";
            return (
              <div
                key={idx}
                className="group relative"
              >
                    <Tile
                      {...(isClickable && {
                        type: "button",
                        "aria-haspopup": "dialog",
                        onClick: (e) => handleTileClick(month, e),
                      })}
                      className={cn(
                        "w-full aspect-square rounded-lg flex flex-col items-center justify-center p-3 transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring",
                        getColor(month.pnl),
                        isClickable
                          ? "hover:scale-105 hover:shadow-lg cursor-pointer"
                          : "cursor-default",
                        isSelected && "ring-2 ring-inset ring-violet-400"
                      )}
                    >
                      <span className="block text-xs font-medium text-white">{month.month}</span>
                      <span className="block text-sm font-bold text-white mt-1">
                        {formatCurrency(month.pnl, { signed: true })}
                      </span>
                      <span className="block text-xs text-white mt-1">{month.trades} trades</span>
                    </Tile>
                <div className={cn(
                  "absolute left-1/2 -translate-x-1/2 hidden group-hover:block group-focus-within:block pointer-events-none z-10",
                  isTopRow ? "top-full mt-2" : "bottom-full mb-2"
                )}>
                  <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-3 text-xs whitespace-nowrap shadow-2xl backdrop-blur-sm animate-in fade-in duration-200">
                    <div className="space-y-0.5">
                      <p className="font-semibold text-app-fg">{month.month}</p>
                      <p className={cn(
                        "font-medium",
                        month.pnl > 0 ? "text-app-positive" : month.pnl < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300"
                      )}>
                        P&L: {formatCurrency(month.pnl, { signed: true })}
                      </p>
                      <p className="text-slate-700 dark:text-slate-300">Trades: {month.trades}</p>
                      <p className="text-slate-700 dark:text-slate-300">Win Rate: {month.winRate}%</p>
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
            ref={modalRef}
            data-testid="heatmap-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="heatmap-modal-title"
            tabIndex={-1}
            className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden shadow-2xl flex flex-col"
            onClick={e => e.stopPropagation()}
          >
            {/* Modal header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-app-line">
              <h2 id="heatmap-modal-title" className="text-lg font-semibold text-app-fg">
                Trades — {formatMonthTitle(selectedMonth.month)}
              </h2>
              <button
                ref={closeRef}
                type="button"
                aria-label="Close"
                data-testid="heatmap-modal-close"
                onClick={() => setSelectedMonth(null)}
                className="p-1.5 rounded-lg text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700/50 transition-colors"
              >
                <X className="w-4 h-4" aria-hidden="true" />
              </button>
            </div>

            {/* Summary line */}
            <div className="px-6 py-3 border-b border-slate-200 dark:border-slate-700/30 bg-slate-50 dark:bg-slate-800/40">
              <p className="text-sm text-slate-700 dark:text-slate-300">
                <span className="font-medium text-app-fg">{modalTrades.length}</span> trade{modalTrades.length !== 1 ? "s" : ""}
                {" · "}Total P&L:{" "}
                <span className={cn(
                  "font-medium",
                  modalTotalPnl > 0 ? "text-app-positive" : modalTotalPnl < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300"
                )}>
                  {formatCurrency(modalTotalPnl, { signed: true })}
                </span>
              </p>
            </div>

            {/* Trade table */}
            {/* ST-12 (BLG-FE-94, EPIC-04, v8.5): overflow-x-auto added --
                per analytics.md's "All tables support horizontal scroll on
                small screens" spec, missing here (4 sibling table
                components already had it). */}
            <div
              className="overflow-y-auto overflow-x-auto flex-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring"
              tabIndex={0}
              role="region"
              aria-label={`Trades closed in ${formatMonthTitle(selectedMonth.month)}`}
            >
              <table className="w-full">
                <thead className="bg-slate-50 dark:bg-slate-800/70 sticky top-0">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">Ticker</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">Exit Date</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">P&L</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">R-Multiple</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase">Exit Reason</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-700/30">
                  {modalTrades.map((trade, idx) => {
                    const r = calcRMultiple(trade);
                    return (
                      <tr key={idx} className="hover:bg-slate-100 dark:hover:bg-slate-800/30">
                        <td className="px-4 py-3 text-sm font-medium text-app-fg">{trade.ticker?.replace(".L", "")}</td>
                        <td className="px-4 py-3 text-sm text-slate-700 dark:text-slate-300">
                          {new Date(trade.exit_date).toLocaleDateString("en-GB")}
                        </td>
                        <td className={cn(
                          "px-4 py-3 text-sm text-right font-medium",
                          trade.pnl > 0 ? "text-app-positive" : trade.pnl < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300"
                        )}>
                          {formatCurrency(trade.pnl, { signed: true })}
                        </td>
                        <td className="px-4 py-3 text-sm text-right text-slate-700 dark:text-slate-300">
                          {r !== null
                            ? <span className={r > 0 ? "text-app-positive" : r < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300"}>{formatR(r)}</span>
                            : <span className="text-slate-600 dark:text-slate-400">—</span>
                          }
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-700 dark:text-slate-300">
                          {exitReasonLabel(trade.exit_reason)}
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
