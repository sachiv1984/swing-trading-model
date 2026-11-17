import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Target, Shield, DollarSign, Percent } from "lucide-react";
import { formatCurrency } from "../../lib/format";

// Performance → Analytics (performance.md v1.1 §4): Best / Worst Trade rows
// removed; Best / Worst Trades lists them with detail.
export default function PerformanceSummary({ metrics, period }) {
  const netPnL = metrics.totalPnL - metrics.totalFees;
  const summaryItems = [
    {
      label: "Gross Profit",
      value: formatCurrency(metrics.grossProfit),
      icon: TrendingUp,
      color: "text-app-positive"
    },
    {
      label: "Gross Loss",
      value: formatCurrency(metrics.grossLoss),
      icon: TrendingDown,
      color: "text-app-negative"
    },
    {
      label: "Average Win",
      value: formatCurrency(metrics.avgWin),
      icon: Target,
      color: "text-cyan-700 dark:text-cyan-400"
    },
    {
      label: "Average Loss",
      value: formatCurrency(metrics.avgLoss),
      icon: Shield,
      color: "text-app-warning"
    },
    {
      label: "Total Fees",
      value: formatCurrency(metrics.totalFees),
      icon: DollarSign,
      color: "text-slate-600 dark:text-slate-400"
    },
    {
      label: "Net P&L",
      value: formatCurrency(netPnL),
      icon: Percent,
      color: netPnL > 0 ? "text-app-positive" : netPnL < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300"
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-white dark:bg-gradient-to-br dark:from-slate-900 dark:to-slate-800 border border-app-line p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-app-fg">Performance Summary</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">{period}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {summaryItems.map((item, idx) => {
          const Icon = item.icon;
          return (
            <div 
              key={idx}
              className="flex items-center gap-3 p-3 rounded-xl bg-app-raised border border-slate-200 dark:border-slate-700/30"
            >
              <div className={`p-2 rounded-lg bg-slate-100 dark:bg-slate-700/50 ${item.color}`}>
                <Icon className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400">{item.label}</p>
                <p className={`text-sm font-semibold ${item.color}`}>{item.value}</p>
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
