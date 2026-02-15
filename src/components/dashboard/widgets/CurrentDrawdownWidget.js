import { TrendingDown, TrendingUp, Calendar, Database } from "lucide-react";
import PropTypes from 'prop-types';

/**
 * CurrentDrawdownWidget - Displays portfolio drawdown metrics
 * 
 * CALCULATION METHODOLOGY:
 * - Peak Equity: Highest portfolio value from historical snapshots + current
 * - Current Drawdown: Percentage below peak (negative value)
 * - Days Underwater: Days since last peak was achieved
 * - Max Historical DD: Largest peak-to-trough decline ever recorded
 * 
 * DATA SOURCES:
 * - portfolio_history: Best (accurate historical tracking)
 * - estimated: Good (from closed trades when no history)
 * - default: Fallback (safe defaults when no data)
 */
export default function CurrentDrawdownWidget({ 
  currentEquity, 
  peakEquity, 
  peakDate, 
  maxHistoricalDrawdown,
  dataSource = 'portfolio_history'
}) {
  // ✅ Input Validation
  const safeCurrentEquity = Number(currentEquity) || 0;
  const safePeakEquity = Number(peakEquity) || 0;
  const safeMaxDD = Number(maxHistoricalDrawdown) || 0;
  
  // ✅ Edge Case: No peak established yet
  if (safePeakEquity === 0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 h-[160px] flex flex-col">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-lg bg-gradient-to-br from-slate-500 to-slate-600">
            <TrendingDown className="w-5 h-5 text-white" />
          </div>
          <h3 className="text-sm font-medium text-slate-300">Current Drawdown</h3>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <Database className="w-8 h-8 text-slate-500 mx-auto mb-2" />
            <p className="text-slate-400 text-sm">Establishing Peak</p>
            <p className="text-slate-500 text-xs mt-1">Recording portfolio history...</p>
          </div>
        </div>
      </div>
    );
  }
  
  // ✅ Calculate if at peak (with small tolerance for floating point errors)
  const isAtPeak = safeCurrentEquity >= (safePeakEquity - 0.01);
  
  // ✅ Calculate current drawdown percentage
  // Formula: ((Current - Peak) / Peak) × 100
  // Result is negative when below peak, 0 when at peak
  const drawdownPercent = isAtPeak 
    ? 0 
    : ((safeCurrentEquity - safePeakEquity) / safePeakEquity) * 100;
  
  // ✅ Calculate days underwater
  // Days since the peak was last achieved
  const daysUnderwater = isAtPeak ? 0 : calculateDaysUnderwater(peakDate);
  
  /**
   * Helper: Calculate days between peak date and today
   */
  function calculateDaysUnderwater(peakDateStr) {
    if (!peakDateStr) return 0;
    
    try {
      const peak = new Date(peakDateStr);
      const today = new Date();
      
      // Validate dates
      if (isNaN(peak.getTime()) || isNaN(today.getTime())) {
        return 0;
      }
      
      // Calculate difference in days
      const diffMs = today - peak;
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      
      // Return 0 if peak is in future (shouldn't happen, but safe)
      return Math.max(0, diffDays);
    } catch (error) {
      console.error('Error calculating days underwater:', error);
      return 0;
    }
  }
  
  /**
   * Determine color scheme based on drawdown severity
   * Green: 0-5% (healthy)
   * Amber: 6-10% (cautionary)
   * Orange: 11-20% (concerning)
   * Red: 20%+ (severe)
   */
  const getDrawdownColor = () => {
    const absDrawdown = Math.abs(drawdownPercent);
    if (absDrawdown === 0) return "text-emerald-500";
    if (absDrawdown <= 5) return "text-emerald-500";
    if (absDrawdown <= 10) return "text-amber-500";
    if (absDrawdown <= 20) return "text-orange-500";
    return "text-rose-500";
  };

  /**
   * Gradient colors for icon background
   */
  const getIconColor = () => {
    const absDrawdown = Math.abs(drawdownPercent);
    if (absDrawdown === 0) return "from-emerald-500 to-green-600";
    if (absDrawdown <= 5) return "from-emerald-500 to-green-600";
    if (absDrawdown <= 10) return "from-amber-500 to-orange-500";
    if (absDrawdown <= 20) return "from-orange-500 to-red-500";
    return "from-rose-500 to-red-600";
  };

  /**
   * Calculate progress bar fill percentage
   * Shows current DD relative to max historical DD
   * Capped at 100% to prevent overflow
   */
  const progressFill = safeMaxDD === 0 
    ? 0 
    : Math.min((Math.abs(drawdownPercent) / Math.abs(safeMaxDD)) * 100, 100);

  /**
   * Format peak equity for display
   */
  const formatPeakEquity = (value) => {
    if (value >= 1000000) {
      return `£${(value / 1000000).toFixed(2)}M`;
    } else if (value >= 1000) {
      return `£${(value / 1000).toFixed(1)}K`;
    } else {
      return `£${value.toFixed(0)}`;
    }
  };

  /**
   * Get data source indicator for debugging
   */
  const getDataSourceBadge = () => {
    const badges = {
      'portfolio_history': { text: 'Live', color: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40' },
      'estimated': { text: 'Est', color: 'bg-amber-500/20 text-amber-400 border-amber-500/40' },
      'default': { text: 'Init', color: 'bg-slate-500/20 text-slate-400 border-slate-500/40' }
    };
    
    const badge = badges[dataSource] || badges.default;
    
    // Only show in development
    if (process.env.NODE_ENV !== 'development') {
      return null;
    }
    
    return (
      <div className={`absolute top-2 right-2 px-2 py-0.5 rounded text-xs border ${badge.color}`}>
        {badge.text}
      </div>
    );
  };

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 h-[160px] flex flex-col relative">
      {/* Data Source Badge (dev only) */}
      {getDataSourceBadge()}
      
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
            {isAtPeak ? "At Peak" : `${daysUnderwater} day${daysUnderwater !== 1 ? 's' : ''} underwater`}
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs justify-end">
          <TrendingUp className="w-4 h-4 text-slate-400" />
          <span className="text-slate-300">
            Peak: {formatPeakEquity(safePeakEquity)}
          </span>
        </div>
      </div>

      {/* Progress Bar - Shows current DD relative to max historical DD */}
      {!isAtPeak && safeMaxDD !== 0 && (
        <div className="relative">
          {/* Background track */}
          <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
            {/* Fill with gradient showing severity */}
            <div 
              className="absolute inset-y-0 left-0 bg-gradient-to-r from-emerald-500 via-amber-500 via-orange-500 to-rose-500 rounded-full transition-all duration-500"
              style={{ width: `${progressFill}%` }}
              aria-label={`Current drawdown is ${progressFill.toFixed(0)}% of maximum historical drawdown`}
            />
          </div>
          
          {/* Optional: Show percentage on hover */}
          <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 opacity-0 hover:opacity-100 transition-opacity">
            <div className="bg-slate-900 text-slate-300 text-xs px-2 py-1 rounded whitespace-nowrap">
              {progressFill.toFixed(0)}% of max DD
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ✅ PropTypes for type checking
CurrentDrawdownWidget.propTypes = {
  currentEquity: PropTypes.number.isRequired,
  peakEquity: PropTypes.number.isRequired,
  peakDate: PropTypes.string.isRequired,
  maxHistoricalDrawdown: PropTypes.number.isRequired,
  dataSource: PropTypes.oneOf(['portfolio_history', 'estimated', 'default'])
};

CurrentDrawdownWidget.defaultProps = {
  dataSource: 'portfolio_history'
};
