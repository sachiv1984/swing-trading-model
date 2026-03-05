import { TrendingDown, Mountain } from "lucide-react";

export default function DrawdownSummary({ drawdownPercent, peakValue, currency = "£" }) {
  const dd = drawdownPercent ?? null;
  const isAtPeak = dd === 0;

  const ddColor =
    dd === null ? "text-slate-400"
    : isAtPeak ? "text-emerald-400"
    : Math.abs(dd) <= 5 ? "text-emerald-400"
    : Math.abs(dd) <= 10 ? "text-amber-400"
    : Math.abs(dd) <= 20 ? "text-orange-400"
    : "text-rose-400";

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 space-y-4">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-gradient-to-br from-rose-500/30 to-orange-500/30">
          <TrendingDown className="w-5 h-5 text-rose-400" />
        </div>
        <h3 className="text-sm font-medium text-slate-300">Drawdown Summary</h3>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-slate-500 mb-1">Current Drawdown</p>
          {dd === null ? (
            <p className="text-xl font-bold text-slate-400">N/A</p>
          ) : isAtPeak ? (
            <p className="text-xl font-bold text-emerald-400">🎉 At Peak</p>
          ) : (
            <p className={`text-2xl font-bold ${ddColor}`}>{dd.toFixed(1)}%</p>
          )}
        </div>
        <div>
          <p className="text-xs text-slate-500 mb-1">Peak Portfolio Value</p>
          <div className="flex items-center gap-1.5">
            <Mountain className="w-4 h-4 text-slate-400" />
            <p className="text-lg font-semibold text-slate-200">
              {peakValue != null ? `${currency}${Number(peakValue).toLocaleString("en-GB", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}` : "N/A"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
