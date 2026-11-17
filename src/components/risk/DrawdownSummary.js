import { TrendingDown, Mountain, AlertCircle } from "lucide-react";
import { formatCurrency, formatPercent } from "../../lib/format";

function ErrorCard() {
  return (
    <div className="rounded-2xl bg-rose-900/20 border border-rose-500/40 p-6 flex items-center gap-3">
      <AlertCircle className="w-5 h-5 text-app-negative flex-shrink-0" />
      <p className="text-sm text-rose-800 dark:text-rose-300">Unable to load drawdown data</p>
    </div>
  );
}

export default function DrawdownSummary({ drawdownPercent, peakValue, error }) {
  if (error) return <ErrorCard />;

  const dd = drawdownPercent ?? null;
  const isAtPeak = dd === 0;

  const ddColor =
    dd === null ? "text-slate-600 dark:text-slate-400"
    : isAtPeak ? "text-app-positive"
    : Math.abs(dd) <= 5 ? "text-app-positive"
    : Math.abs(dd) <= 10 ? "text-app-warning"
    : Math.abs(dd) <= 20 ? "text-orange-700 dark:text-orange-400"
    : "text-app-negative";

  return (
    <div className="rounded-2xl bg-white dark:bg-gradient-to-br dark:from-slate-800/50 dark:to-slate-900/50 border border-app-line backdrop-blur-sm p-6 space-y-4">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-gradient-to-br from-rose-500/30 to-orange-500/30">
          <TrendingDown className="w-5 h-5 text-app-negative" />
        </div>
        <h2 className="text-sm font-medium text-slate-700 dark:text-slate-300">Drawdown Summary</h2>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Current Drawdown</p>
          {dd === null ? (
            <p className="text-xl font-bold text-slate-600 dark:text-slate-400">N/A</p>
          ) : isAtPeak ? (
            <p className="text-xl font-bold text-app-positive">🎉 At Peak</p>
          ) : (
            <p className={`text-2xl font-bold ${ddColor}`}>{formatPercent(dd)}</p>
          )}
        </div>
        <div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Peak Portfolio Value</p>
          <div className="flex items-center gap-1.5">
            <Mountain className="w-4 h-4 text-app-muted" />
            <p className="text-lg font-semibold text-slate-800 dark:text-slate-200">
              {peakValue != null ? formatCurrency(peakValue) : "N/A"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
