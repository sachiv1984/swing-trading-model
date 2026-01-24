import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Target, Shield, DollarSign, Percent } from "lucide-react";

export default function PerformanceSummary({ metrics, period }) {
  const summaryItems = [
    {
      label: "Gross Profit",
      value: `£${metrics.grossProfit.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: TrendingUp,
      color: "text-emerald-400"
    },
    {
      label: "Gross Loss",
      value: `£${metrics.grossLoss.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: TrendingDown,
      color: "text-rose-400"
    },
    {
      label: "Average Win",
      value: `£${metrics.avgWin.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: Target,
      color: "text-cyan-400"
    },
    {
      label: "Average Loss",
      value: `£${metrics.avgLoss.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: Shield,
      color: "text-amber-400"
    },
    {
      label: "Best Trade",
      value: `£${metrics.bestTrade.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: TrendingUp,
      color: "text-emerald-400"
    },
    {
      label: "Worst Trade",
      value: `£${metrics.worstTrade.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: TrendingDown,
      color: "text-rose-400"
    },
    {
      label: "Total Fees",
      value: `£${metrics.totalFees.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: DollarSign,
      color: "text-slate-400"
    },
    {
      label: "Net P&L",
      value: `£${(metrics.totalPnL - metrics.totalFees).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: Percent,
      color: metrics.totalPnL - metrics.totalFees >= 0 ? "text-emerald-400" : "text-rose-400"
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-white">Performance Summary</h3>
          <p className="text-sm text-slate-400">{period}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {summaryItems.map((item, idx) => {
          const Icon = item.icon;
          return (
            <div 
              key={idx}
              className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/50 border border-slate-700/30"
            >
              <div className={`p-2 rounded-lg bg-slate-700/50 ${item.color}`}>
                <Icon className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs text-slate-400">{item.label}</p>
                <p className={`text-sm font-semibold ${item.color}`}>{item.value}</p>
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
