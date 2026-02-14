import { TrendingUp, TrendingDown } from "lucide-react";

export default function MarketComparison({ ukMetrics, usMetrics }) {
  const MarketPanel = ({ title, metrics, gradient }) => (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <div className={`px-3 py-1 rounded-lg bg-gradient-to-r ${gradient} text-white text-xs font-medium`}>
          {metrics.totalTrades} trades
        </div>
      </div>
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-sm text-slate-400">Win Rate</span>
          <span className="text-sm font-semibold text-white">{metrics.winRate}%</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-slate-400">Total P&L</span>
          <span className={`text-sm font-semibold ${metrics.totalPnl >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            {metrics.totalPnl >= 0 ? '+' : ''}£{metrics.totalPnl.toFixed(2)}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-slate-400">Avg Win</span>
          <span className="text-sm font-semibold text-emerald-400">+£{metrics.avgWin.toFixed(2)}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-slate-400">Avg Loss</span>
          <span className="text-sm font-semibold text-rose-400">-£{Math.abs(metrics.avgLoss).toFixed(2)}</span>
        </div>
        <div className="pt-4 border-t border-slate-700/50">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            <span className="text-xs text-slate-400">Best Performer</span>
          </div>
          <p className="text-sm font-semibold text-white">{metrics.bestPerformer.ticker}</p>
          <p className="text-xs text-emerald-400">+£{metrics.bestPerformer.pnl.toFixed(2)}</p>
        </div>
        <div className="pt-2">
          <div className="flex items-center gap-2 mb-2">
            <TrendingDown className="w-4 h-4 text-rose-400" />
            <span className="text-xs text-slate-400">Worst Performer</span>
          </div>
          <p className="text-sm font-semibold text-white">{metrics.worstPerformer.ticker}</p>
          <p className="text-xs text-rose-400">-£{Math.abs(metrics.worstPerformer.pnl).toFixed(2)}</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <MarketPanel 
        title="UK Market Performance" 
        metrics={ukMetrics}
        gradient="from-cyan-500 to-blue-500"
      />
      <MarketPanel 
        title="US Market Performance" 
        metrics={usMetrics}
        gradient="from-violet-500 to-purple-500"
      />
    </div>
  );
}
