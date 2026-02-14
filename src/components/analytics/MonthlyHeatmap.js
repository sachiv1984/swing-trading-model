import { cn } from "../../lib/utils";

export default function MonthlyHeatmap({ monthlyData }) {
  const getColor = (pnl) => {
    if (pnl > 500) return "bg-emerald-500";
    if (pnl > 100) return "bg-emerald-400";
    if (pnl > -100) return "bg-slate-600";
    if (pnl > -500) return "bg-rose-400";
    return "bg-rose-500";
  };

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-white mb-6">Monthly Performance</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
        {monthlyData.map((month, idx) => {
          const isTopRow = idx < 6;
          return (
            <div
              key={idx}
              className="group relative"
            >
              <div className={cn(
                "aspect-square rounded-lg flex flex-col items-center justify-center p-3 transition-all duration-200 hover:scale-105 hover:shadow-lg",
                getColor(month.pnl)
              )}>
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
      <div className="flex items-center justify-center gap-4 mt-6 text-xs text-slate-400">
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
  );
}
