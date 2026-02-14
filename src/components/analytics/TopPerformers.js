import { TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "../../lib/utils";

export default function TopPerformers({ topWinners, topLosers }) {
  const TradeList = ({ title, trades, isWinner, icon: Icon, iconColor }) => (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <div className="flex items-center gap-3 mb-6">
        <div className={cn("p-2 rounded-lg", isWinner ? "bg-emerald-500/20" : "bg-rose-500/20")}>
          <Icon className={cn("w-5 h-5", iconColor)} />
        </div>
        <h3 className="text-lg font-semibold text-white">{title}</h3>
      </div>
      <div className="space-y-3">
        {trades.map((trade, idx) => (
          <div key={idx} className="p-4 rounded-lg bg-slate-900/50 border border-slate-700/30 hover:bg-slate-900/80 transition-colors">
            <div className="flex items-start justify-between mb-2">
              <div>
                <p className="font-semibold text-white">{trade.ticker}</p>
                <p className="text-xs text-slate-400 mt-1">{trade.entryDate}</p>
              </div>
              <div className="text-right">
                <p className={cn(
                  "font-bold text-lg",
                  isWinner ? "text-emerald-400" : "text-rose-400"
                )}>
                  {isWinner ? "+" : "-"}£{Math.abs(trade.pnl).toFixed(2)}
                </p>
                <p className={cn(
                  "text-sm",
                  isWinner ? "text-emerald-400" : "text-rose-400"
                )}>
                  {isWinner ? "+" : ""}{trade.pnlPercent.toFixed(1)}%
                </p>
              </div>
            </div>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>{trade.daysHeld} days</span>
              <span className="capitalize">{trade.exitReason.replace(/_/g, ' ')}</span>
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
        iconColor="text-emerald-400"
      />
      <TradeList
        title="Top 5 Losing Trades"
        trades={topLosers}
        isWinner={false}
        icon={TrendingDown}
        iconColor="text-rose-400"
      />
    </div>
  );
}
