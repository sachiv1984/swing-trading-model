import { Button } from "../ui/button";
import { TrendingUp, DollarSign, Target, CheckCircle2, XCircle, Circle } from "lucide-react";
import { cn } from "../../lib/utils";

export default function SignalCard({ signal, onAddPosition, onDismiss }) {
  const currencySymbol = signal.market === "US" ? "$" : "£";
  
  // Determine status badge
  const getStatusBadge = () => {
    if (signal.status === "entered") {
      return (
        <div className="flex items-center gap-1 px-2 py-1 rounded-md bg-emerald-500/20 border border-emerald-500/30">
          <CheckCircle2 className="w-3 h-3 text-emerald-400" />
          <span className="text-xs font-medium text-emerald-400">Position Entered</span>
        </div>
      );
    }
    
    if (signal.status === "dismissed") {
      return (
        <div className="flex items-center gap-1 px-2 py-1 rounded-md bg-red-500/20 border border-red-500/30">
          <XCircle className="w-3 h-3 text-red-400" />
          <span className="text-xs font-medium text-red-400">Dismissed</span>
        </div>
      );
    }
    
    if (signal.status === "already_held") {
      return (
        <div className="flex items-center gap-1 px-2 py-1 rounded-md bg-slate-700/50 border border-slate-600">
          <Circle className="w-3 h-3 text-slate-400 fill-slate-400" />
          <span className="text-xs font-medium text-slate-300">Already Held</span>
        </div>
      );
    }
    
    // New signal
    return (
      <div className="flex items-center gap-1 px-2 py-1 rounded-md bg-cyan-500/20 border border-cyan-500/30">
        <TrendingUp className="w-3 h-3 text-cyan-400" />
        <span className="text-xs font-medium text-cyan-400">New Signal</span>
      </div>
    );
  };

  const isActionable = signal.status === "new";
  
  // Format shares display (show 2 decimal places for fractional)
  const formatShares = (shares) => {
    if (shares % 1 === 0) {
      return shares.toString(); // Whole number
    }
    return shares.toFixed(2); // Fractional with 2 decimals
  };

  return (
    <div className="group relative overflow-hidden rounded-xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-6 hover:border-cyan-500/50 transition-all duration-300">
      {/* Gradient overlay on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-violet-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h3 className="text-2xl font-bold text-white">
                {signal.ticker.replace(".L", "")}
              </h3>
              <span className="px-2 py-0.5 rounded-md bg-slate-700/50 text-xs font-mono text-slate-300">
                #{signal.rank}
              </span>
            </div>
            <p className="text-sm text-slate-400">
              {signal.market === "US" ? "🇺🇸 United States" : "🇬🇧 United Kingdom"}
            </p>
          </div>
          {getStatusBadge()}
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              <p className="text-xs text-slate-400">Momentum</p>
            </div>
            <p className="text-lg font-bold text-emerald-400">
              +{signal.momentum_percent.toFixed(1)}%
            </p>
          </div>

          <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
            <div className="flex items-center gap-2 mb-1">
              <DollarSign className="w-4 h-4 text-cyan-400" />
              <p className="text-xs text-slate-400">Current Price</p>
            </div>
            <p className="text-lg font-bold text-white">
              {currencySymbol}{signal.current_price.toFixed(2)}
            </p>
          </div>

          <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
            <div className="flex items-center gap-2 mb-1">
              <Target className="w-4 h-4 text-red-400" />
              <p className="text-xs text-slate-400">Initial Stop</p>
            </div>
            <p className="text-lg font-bold text-red-400">
              {currencySymbol}{signal.initial_stop.toFixed(2)}
            </p>
          </div>

          {isActionable && (
            <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
              <div className="flex items-center gap-2 mb-1">
                <DollarSign className="w-4 h-4 text-violet-400" />
                <p className="text-xs text-slate-400">Allocation</p>
              </div>
              <p className="text-lg font-bold text-white">
                £{signal.total_cost.toFixed(2)}
              </p>
            </div>
          )}
        </div>

        {/* Position Details (only for actionable signals) */}
        {isActionable && (
          <div className="mb-4 p-3 rounded-lg bg-slate-900/50 border border-slate-700/30">
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-400">Suggested Shares</span>
              <span className="text-sm font-mono font-semibold text-white">
                {formatShares(signal.suggested_shares)}
              </span>
            </div>
            <div className="flex justify-between items-center mt-2">
              <span className="text-sm text-slate-400">Stop Distance</span>
              <span className="text-sm font-mono font-semibold text-red-400">
                {currencySymbol}
                {(signal.current_price - signal.initial_stop).toFixed(2)}
              </span>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        {isActionable && (
          <div className="flex gap-2">
            <Button
              onClick={() => onAddPosition(signal)}
              className="flex-1 bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white font-semibold"
            >
              Add Position
            </Button>
            <Button
              onClick={() => onDismiss(signal.id)}
              variant="outline"
              className="border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800"
            >
              Dismiss
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
