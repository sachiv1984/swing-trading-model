import { motion } from "framer-motion";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { TrendingUp, Plus, Award, CheckCircle2, Lock, XCircle } from "lucide-react";
import { cn } from "../../lib/utils";

export default function SignalCard({ signal, onAddPosition, onDismiss }) {
  const isUS = signal.market === "US";
  const currencySymbol = isUS ? "$" : "£";
  const isNew = signal.status === "new";
  const isEntered = signal.status === "entered";
  const isAlreadyHeld = signal.status === "already_held";
  const isDismissed = signal.status === "dismissed";

  const rankColors = {
    1: "from-yellow-500/20 to-amber-500/20 border-yellow-500/50 shadow-yellow-500/10",
    2: "from-slate-300/20 to-slate-400/20 border-slate-400/50 shadow-slate-400/10",
    3: "from-slate-600/20 to-slate-700/20 border-slate-600/40 shadow-slate-600/10",
    4: "from-slate-600/20 to-slate-700/20 border-slate-600/40 shadow-slate-600/10",
    5: "from-slate-600/20 to-slate-700/20 border-slate-600/40 shadow-slate-600/10"
  };

  const statusConfig = {
    new: { 
      label: "New Signal", 
      color: "bg-cyan-500/20 text-cyan-400 border-cyan-500/40" 
    },
    entered: { 
      label: "Entered", 
      color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/40", 
      icon: CheckCircle2 
    },
    already_held: { 
      label: "Already Held", 
      color: "bg-slate-500/20 text-slate-400 border-slate-500/40", 
      icon: Lock 
    },
    dismissed: { 
      label: "Dismissed", 
      color: "bg-red-500/20 text-red-400 border-red-500/40",
      icon: XCircle
    }
  };

  const status = statusConfig[signal.status] || statusConfig.new;
  const StatusIcon = status.icon;

  // Format shares display (show 2 decimal places for fractional)
  const formatShares = (shares) => {
    if (shares % 1 === 0) {
      return shares.toString(); // Whole number
    }
    return shares.toFixed(2); // Fractional with 2 decimals
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={isNew ? { scale: 1.02, y: -4 } : {}}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={cn(
        "p-5 rounded-2xl border-2 backdrop-blur-sm transition-all",
        !isNew && "opacity-60",
        isNew && "hover:shadow-2xl cursor-pointer",
        `bg-gradient-to-br ${rankColors[signal.rank] || rankColors[5]}`
      )}
    >
      {/* Header: Rank + Ticker + Status */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={cn(
            "flex items-center justify-center w-12 h-12 rounded-xl font-bold text-lg shadow-lg",
            signal.rank === 1 && "bg-gradient-to-br from-yellow-400 to-amber-500 text-slate-900",
            signal.rank === 2 && "bg-gradient-to-br from-slate-300 to-slate-400 text-slate-900",
            signal.rank >= 3 && "bg-slate-700 text-slate-300"
          )}>
            {signal.rank === 1 ? <Award className="w-6 h-6" /> : signal.rank}
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h3 className="text-3xl font-bold text-white">{signal.ticker.replace(".L", "")}</h3>
              <span className="text-2xl">{isUS ? "🇺🇸" : "🇬🇧"}</span>
            </div>
            <p className="text-sm text-slate-400 font-medium">{signal.market} Market</p>
          </div>
        </div>
        <Badge className={cn("border", status.color)}>
          {StatusIcon && <StatusIcon className="w-3 h-3 mr-1" />}
          {status.label}
        </Badge>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <div className="p-3 rounded-lg bg-slate-900/40 border border-slate-700/50">
          <p className="text-xs text-slate-400 mb-1">Momentum</p>
          <div className="flex items-center gap-1">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            <p className="text-lg font-bold text-emerald-400">
              +{signal.momentum_percent.toFixed(1)}%
            </p>
          </div>
        </div>
        <div className="p-3 rounded-lg bg-slate-900/40 border border-slate-700/50">
          <p className="text-xs text-slate-400 mb-1">Price</p>
          <p className="text-lg font-bold text-white">{currencySymbol}{signal.current_price.toFixed(2)}</p>
        </div>
        <div className="p-3 rounded-lg bg-slate-900/40 border border-slate-700/50">
          <p className="text-xs text-slate-400 mb-1">Stop</p>
          <p className="text-lg font-bold text-rose-400">{currencySymbol}{signal.initial_stop.toFixed(2)}</p>
        </div>
      </div>

      {/* Position Details - Only for NEW signals */}
      {isNew && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          className="mb-4"
        >
          <div className="p-4 rounded-xl bg-gradient-to-br from-cyan-500/10 to-violet-500/10 border border-cyan-500/30">
            <p className="text-xs font-semibold text-cyan-400 mb-3">POSITION DETAILS</p>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-slate-400 mb-1">Suggested Shares</p>
                <p className="text-xl font-bold text-white">{formatShares(signal.suggested_shares)}</p>
              </div>
              <div>
                <p className="text-xs text-slate-400 mb-1">Allocation Cost</p>
                <p className="text-xl font-bold text-white">£{signal.total_cost.toFixed(2)}</p>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-700/50">
              <p className="text-sm text-slate-300">
                Buy <span className="font-bold text-cyan-400">{formatShares(signal.suggested_shares)} shares</span> at{" "}
                <span className="font-bold text-white">{currencySymbol}{signal.current_price.toFixed(2)}</span>
              </p>
              <p className="text-xs text-slate-400 mt-1">
                Stop distance: <span className="text-rose-400 font-mono">{currencySymbol}{(signal.current_price - signal.initial_stop).toFixed(2)}</span>
              </p>
            </div>
          </div>
        </motion.div>
      )}

      {/* Action Buttons - Only for NEW signals */}
      {isNew && (
        <div className="flex gap-2">
          <Button
            onClick={() => onAddPosition(signal)}
            className="flex-1 bg-gradient-to-r from-cyan-600 to-violet-600 hover:from-cyan-500 hover:to-violet-500 text-white font-semibold h-11"
          >
            <Plus className="w-5 h-5 mr-2" />
            Add Position
          </Button>
          <Button
            onClick={() => onDismiss(signal.id)}
            variant="outline"
            className="border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800 h-11 px-6"
          >
            Dismiss
          </Button>
        </div>
      )}

      {/* Info messages for non-NEW signals */}
      {isEntered && (
        <div className="text-center py-2 px-4 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
          <p className="text-sm text-emerald-400 font-medium">✓ Position successfully added</p>
        </div>
      )}

      {isAlreadyHeld && (
        <div className="text-center py-2 px-4 rounded-lg bg-slate-700/30 border border-slate-600/30">
          <p className="text-sm text-slate-400">◉ You already hold this position</p>
        </div>
      )}

      {isDismissed && (
        <div className="text-center py-2 px-4 rounded-lg bg-red-500/10 border border-red-500/30">
          <p className="text-sm text-red-400">✗ Signal dismissed</p>
        </div>
      )}
    </motion.div>
  );
}
