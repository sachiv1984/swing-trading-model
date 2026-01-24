import { motion } from "framer-motion";
import { Activity, TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "../../lib/utils";

export default function RecentTradesWidget({ positions }) {
  const recentTrades = positions
    ?.filter(p => p.status === "closed")
    .sort((a, b) => new Date(b.exit_date) - new Date(a.exit_date))
    .slice(0, 5) || [];

  return (
    <div className="p-6">
      <div className="flex items-center gap-2 mb-4">
        <Activity className="w-5 h-5 text-cyan-400" />
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Recent Trades</h3>
      </div>
      
      {recentTrades.length === 0 ? (
        <div className="text-center py-8 text-slate-500">
          <p>No recent trades</p>
        </div>
      ) : (
        <div className="space-y-3">
          {recentTrades.map((trade, idx) => (
            <motion.div
              key={trade.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.05 }}
              className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 dark:bg-slate-800/50 border border-slate-700/30"
            >
              <div className="flex items-center gap-3">
                <div className={cn(
                  "p-2 rounded-lg",
                  (trade.pnl || 0) >= 0 ? "bg-emerald-500/20 text-emerald-400" : "bg-rose-500/20 text-rose-400"
                )}>
                  {(trade.pnl || 0) >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                </div>
                <div>
                  <p className="font-medium text-slate-900 dark:text-white">{trade.ticker}</p>
                  <p className="text-xs text-slate-500">{trade.exit_date}</p>
                </div>
              </div>
              <div className="text-right">
                <p className={cn(
                  "font-semibold",
                  (trade.pnl || 0) >= 0 ? "text-emerald-400" : "text-rose-400"
                )}>
                  {(trade.pnl || 0) >= 0 ? "+" : ""}£{(trade.pnl || 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                </p>
                <p className="text-xs text-slate-500">{trade.shares} shares</p>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
