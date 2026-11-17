import { TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "../../lib/utils";
import { formatCurrency, formatPercent } from "../../lib/format";

export default function TopPerformers({ topWinners, topLosers }) {
  const TradeList = ({ title, trades, isWinner, icon: Icon, iconColor }) => (
    <div className="rounded-2xl bg-app-raised border border-app-line p-6 backdrop-blur-sm">
      <div className="flex items-center gap-3 mb-6">
        <div className={cn("p-2 rounded-lg", isWinner ? "bg-emerald-500/20" : "bg-rose-500/20")}>
          <Icon className={cn("w-5 h-5", iconColor)} />
        </div>
        <h3 className="text-lg font-semibold text-app-fg">{title}</h3>
      </div>
      <div className="space-y-3">
        {trades.map((trade, idx) => (
          <div key={idx} className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700/30 hover:bg-slate-100 dark:hover:bg-slate-900/80 transition-colors">
            <div className="flex items-start justify-between mb-2">
              <div>
                <p className="font-semibold text-app-fg">{trade.ticker?.replace(".L", "")}</p>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">{trade.entryDate}</p>
              </div>
              <div className="text-right">
                <p className={cn(
                  "font-bold text-lg",
                  isWinner ? "text-app-positive" : "text-app-negative"
                )}>
                  {formatCurrency(trade.pnl, { signed: true })}
                </p>
                <p className={cn(
                  "text-sm",
                  isWinner ? "text-app-positive" : "text-app-negative"
                )}>
                  {formatPercent(trade.pnlPercent, { signed: true })}
                </p>
              </div>
            </div>
            <div className="flex items-center justify-between text-xs text-slate-600 dark:text-slate-400">
              <span>{trade.daysHeld} days</span>
              <span className="capitalize">{trade.exitReason ? trade.exitReason.replace(/_/g, ' ') : '—'}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <TradeList
        title="Top 5 Winning Trades"
        trades={topWinners}
        isWinner={true}
        icon={TrendingUp}
        iconColor="text-app-positive"
      />
      <TradeList
        title="Top 5 Losing Trades"
        trades={topLosers}
        isWinner={false}
        icon={TrendingDown}
        iconColor="text-app-negative"
      />
    </div>
  );
}
