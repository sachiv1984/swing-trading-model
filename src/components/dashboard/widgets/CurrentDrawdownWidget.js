import { TrendingDown, TrendingUp, Calendar } from "lucide-react";

export default function CurrentDrawdownWidget({ currentEquity, peakEquity, peakDate, maxHistoricalDrawdown }) {
  // Calculate current drawdown
  const isAtPeak = currentEquity >= peakEquity;
  const drawdownPercent = isAtPeak ? 0 : ((currentEquity - peakEquity) / peakEquity) * 100;

  // Calculate days underwater (simplified - would need actual date tracking in real app)
  const daysUnderwater = isAtPeak ? 0 : Math.floor((new Date() - new Date(peakDate)) / (1000 * 60 * 60 * 24));

  // Determine color based on drawdown severity
  const getDrawdownColor = () => {
    const absDrawdown = Math.abs(drawdownPercent);
    if (absDrawdown === 0) return "text-emerald-500";
    if (absDrawdown <= 5) return "text-emerald-500";
    if (absDrawdown <= 10) return "text-amber-500";
    if (absDrawdown <= 20) return "text-orange-500";
    return "text-rose-500";
  };

  const getIconColor = () => {
    const absDrawdown = Math.abs(drawdownPercent);
    if (absDrawdown === 0) return "from-emerald-500 to-green-600";
    if (absDrawdown <= 5) return "from-emerald-500 to-green-600";
    if (absDrawdown <= 10) return "from-amber-500 to-orange-500";
    if (absDrawdown <= 20) return "from-orange-500 to-red-500";
    return "from-rose-500 to-red-600";
  };

  // Calculate progress bar fill
  const progressFill = maxHistoricalDrawdown === 0 ? 0 : Math.min((Math.abs(drawdownPercent) / Math.abs(maxHistoricalDrawdown)) * 100, 100);

  // Handle edge cases
  if (!peakEquity || peakEquity === 0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 h-[160px] flex flex-col">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-lg bg-gradient-to-br from-slate-500 to-slate-600">
            <TrendingDown className="w-5 h-5 text-white" />
          </div>
          <h3 className="text-sm font-medium text-slate-300">Current Drawdown</h3>
        </div>
        <div className="text-center py-4">
          <p className="text-slate-400 text-sm">Establishing Peak</p>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 h-[160px] flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className={`p-2 rounded-lg bg-gradient-to-br ${getIconColor()}`}>
          <TrendingDown className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-sm font-medium text-slate-300">Current Drawdown</h3>
      </div>

      {/* Main Display */}
      <div className="text-center mb-4">
        {isAtPeak ? (
          <div className="text-3xl font-bold text-emerald-500">
            🎉 New Peak!
          </div>
        ) : (
          <div className={`text-3xl font-bold ${getDrawdownColor()}`}>
            {drawdownPercent.toFixed(1)}%
          </div>
        )}
      </div>

      {/* Secondary Info */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="flex items-center gap-2 text-xs">
          <Calendar className="w-4 h-4 text-slate-400" />
          <span className="text-slate-300">
            {isAtPeak ? "At Peak" : `${daysUnderwater} days underwater`}
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs justify-end">
          <TrendingUp className="w-4 h-4 text-slate-400" />
          <span className="text-slate-300">
            Peak: £{peakEquity.toFixed(0)}
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      {!isAtPeak && (
        <div className="relative h-2 bg-slate-700/50 rounded-full overflow-hidden">
          <div 
            className="absolute inset-y-0 left-0 bg-gradient-to-r from-emerald-500 via-amber-500 via-orange-500 to-rose-500 rounded-full transition-all duration-500"
            style={{ width: `${progressFill}%` }}
          />
        </div>
      )}
    </div>
  );
}
