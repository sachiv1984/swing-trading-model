import { TrendingUp, BarChart3, Activity } from "lucide-react";

export default function ConsistencyMetrics({ metrics }) {
  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-white mb-6">Consistency Metrics</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-4 rounded-lg bg-slate-900/50 border border-slate-700/30">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-emerald-500/20">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
            </div>
            <div>
              <p className="text-xs text-slate-400">Consecutive Months Profitable</p>
              <p className="text-2xl font-bold text-white mt-1">{metrics.consecutiveProfitableMonths}</p>
            </div>
          </div>
          <p className="text-xs text-slate-500">Current streak: {metrics.currentStreak} months</p>
        </div>

        <div className="p-4 rounded-lg bg-slate-900/50 border border-slate-700/30">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-cyan-500/20">
              <BarChart3 className="w-4 h-4 text-cyan-400" />
            </div>
            <div>
              <p className="text-xs text-slate-400">Win Rate Consistency</p>
              <p className="text-2xl font-bold text-white mt-1">{metrics.winRateStdDev.toFixed(1)}%</p>
            </div>
          </div>
          <p className="text-xs text-slate-500">
            {metrics.winRateStdDev < 10 ? "Very consistent" : metrics.winRateStdDev < 20 ? "Consistent" : "Variable"}
          </p>
        </div>

        <div className="p-4 rounded-lg bg-slate-900/50 border border-slate-700/30">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-violet-500/20">
              <Activity className="w-4 h-4 text-violet-400" />
            </div>
            <div>
              <p className="text-xs text-slate-400">Monthly P&L Volatility</p>
              <p className="text-2xl font-bold text-white mt-1">£{metrics.pnlStdDev.toFixed(0)}</p>
            </div>
          </div>
          <p className="text-xs text-slate-500">Standard deviation of returns</p>
        </div>
      </div>
    </div>
  );
}
