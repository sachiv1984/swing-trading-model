import { motion } from "framer-motion";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { TrendingUp, TrendingDown, Plus, X, ExternalLink, Award, CheckCircle2 } from "lucide-react";
import { cn } from "../../lib/utils";

export default function SignalCard({ signal, onAddPosition, onDismiss }) {
  const isUS = signal.market === "US";
  const currencySymbol = isUS ? "$" : "£";
  const isPositiveMomentum = signal.momentum_percent >= 0;

  const rankColors = {
    1: "from-yellow-500/20 to-amber-500/20 border-yellow-500/50",
    2: "from-slate-400/20 to-slate-500/20 border-slate-400/50",
    3: "from-slate-700/20 to-slate-800/20 border-slate-700/50",
    4: "from-slate-700/20 to-slate-800/20 border-slate-700/50",
    5: "from-slate-700/20 to-slate-800/20 border-slate-700/50"
  };

  const statusConfig = {
    new: { label: "New", color: "bg-blue-500/20 text-blue-400 border-blue-500/30" },
    entered: { label: "Entered", color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30", icon: CheckCircle2 },
    dismissed: { label: "Dismissed", color: "bg-slate-500/20 text-slate-400 border-slate-500/30" },
    expired: { label: "Expired", color: "bg-rose-500/20 text-rose-400 border-rose-500/30" }
  };

  const status = statusConfig[signal.status] || statusConfig.new;
  const StatusIcon = status.icon;
  const isDismissedOrExpired = signal.status === "dismissed" || signal.status === "expired";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "p-4 rounded-xl border-2 backdrop-blur-sm transition-all",
        isDismissedOrExpired ? "opacity-50" : "hover:shadow-lg",
        `bg-gradient-to-br ${rankColors[signal.rank] || rankColors[5]}`
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className={cn(
            "flex items-center justify-center w-10 h-10 rounded-full font-bold",
            signal.rank === 1 && "bg-gradient-to-br from-yellow-400 to-amber-500 text-slate-900",
            signal.rank === 2 && "bg-gradient-to-br from-slate-300 to-slate-400 text-slate-900",
            signal.rank >= 3 && "bg-slate-700 text-slate-300"
          )}>
            {signal.rank === 1 && <Award className="w-5 h-5" />}
            {signal.rank !== 1 && signal.rank}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-2xl font-bold text-white">{signal.ticker}</h3>
              <span className="text-xl">{isUS ? "🇺🇸" : "🇬🇧"}</span>
            </div>
            <p className="text-sm text-slate-400">{signal.market} Market</p>
          </div>
        </div>
        <Badge className={cn("border", status.color)}>
          {StatusIcon && <StatusIcon className="w-3 h-3 mr-1" />}
          {status.label}
        </Badge>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-xs text-slate-400 mb-1">Current Price</p>
          <p className="text-xl font-bold text-white">{currencySymbol}{signal.current_price.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400 mb-1">Momentum</p>
          <div className="flex items-center gap-1">
            {isPositiveMomentum ? (
              <TrendingUp className="w-4 h-4 text-emerald-400" />
            ) : (
              <TrendingDown className="w-4 h-4 text-rose-400" />
            )}
            <p className={cn(
              "text-xl font-bold",
              isPositiveMomentum ? "text-emerald-400" : "text-rose-400"
            )}>
              {isPositiveMomentum ? "+" : ""}{signal.momentum_percent.toFixed(1)}%
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 mb-4 p-3 rounded-lg bg-slate-800/50">
        <div>
          <p className="text-xs text-slate-400">Shares</p>
          <p className="text-sm font-medium text-white">{signal.suggested_shares}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Total Cost</p>
          <p className="text-sm font-medium text-white">£{signal.total_cost.toFixed(0)}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Stop</p>
          <p className="text-sm font-medium text-white">{currencySymbol}{signal.initial_stop.toFixed(2)}</p>
        </div>
      </div>

      <div className="flex gap-2">
        <Button
          onClick={() => onAddPosition(signal)}
          disabled={isDismissedOrExpired}
          className="flex-1 bg-gradient-to-r from-cyan-600 to-violet-600 hover:from-cyan-500 hover:to-violet-500 text-white"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Position
        </Button>
        {signal.status === "new" && (
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onDismiss(signal.id)}
            className="text-slate-400 hover:text-white hover:bg-slate-800"
          >
            <X className="w-4 h-4" />
          </Button>
        )}
      </div>
    </motion.div>
  );
}
