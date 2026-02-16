import { TrendingUp, TrendingDown } from "lucide-react";

const normalizeMetrics = (m) => {
  const safe = m ?? {};
  const best = safe.bestPerformer ?? null;
  const worst = safe.worstPerformer ?? null;

  const num = (v, fallback = 0) => {
    const n = typeof v === "number" ? v : Number(v);
    return Number.isFinite(n) ? n : fallback;
  };

  return {
    totalTrades: num(safe.totalTrades, 0),
    winRate: num(safe.winRate, 0),
    totalPnl: num(safe.totalPnl, 0),
    avgWin: num(safe.avgWin, 0),
    avgLoss: num(safe.avgLoss, 0),
    bestPerformer: best && {
      ticker: best.ticker ?? "N/A",
      pnl: num(best.pnl, 0),
    },
    worstPerformer: worst && {
      ticker: worst.ticker ?? "N/A",
      pnl: num(worst.pnl, 0),
    },
  };
};

export default function MarketComparison({ ukMetrics, usMetrics }) {
  const MarketPanel = ({ title, metrics, gradient }) => {
    const m = normalizeMetrics(metrics);

    return (
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          <div className={`px-3 py-1 rounded-lg bg-gradient-to-r ${gradient} text-white text-xs font-medium`}>
            {m.totalTrades} trades
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-slate-400">Win Rate</span>
            <span className="text-sm font-semibold text-white">{m.winRate}%</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-sm text-slate-400">Total P&amp;L</span>
            <span className={`text-sm font-semibold ${m.totalPnl >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
              {m.totalPnl >= 0 ? "+" : ""}£{m.totalPnl.toFixed(2)}
            </span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-sm text-slate-400">Avg Win</span>
            <span className="text-sm font-semibold text-emerald-400">+£{m.avgWin.toFixed(2)}</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-sm text-slate-400">Avg Loss</span>
            <span className="text-sm font-semibold text-rose-400">
              -£{Math.abs(m.avgLoss).toFixed(2)}
            </span>
          </div>

          <div className="pt-4 border-t border-slate-700/50">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              <span className="text-xs text-slate-400">Best Performer</span>
            </div>

            {m.bestPerformer ? (
              <>
                <p className="text-sm font-semibold text-white">{m.bestPerformer.ticker}</p>
                <p className="text-xs text-emerald-400">+£{m.bestPerformer.pnl.toFixed(2)}</p>
              </>
            ) : (
              <p className="text-sm text-slate-400">No trades yet</p>
            )}
          </div>

          <div className="pt-2">
            <div className="flex items-center gap-2 mb-2">
              <TrendingDown className="w-4 h-4 text-rose-400" />
              <span className="text-xs text-slate-400">Worst Performer</span>
            </div>

            {m.worstPerformer ? (
              <>
                <p className="text-sm font-semibold text-white">{m.worstPerformer.ticker}</p>
                <p className="text-xs text-rose-400">-£{Math.abs(m.worstPerformer.pnl).toFixed(2)}</p>
              </>
            ) : (
              <p className="text-sm text-slate-400">No trades yet</p>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <MarketPanel title="UK Market Performance" metrics={ukMetrics} gradient="from-cyan-500 to-blue-500" />
      <MarketPanel title="US Market Performance" metrics={usMetrics} gradient="from-violet-500 to-purple-500" />
    </div>
  );
}
