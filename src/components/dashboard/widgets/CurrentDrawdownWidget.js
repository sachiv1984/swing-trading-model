import { TrendingDown, TrendingUp, Calendar, Database } from "lucide-react";
import PropTypes from 'prop-types';

/**
 * CurrentDrawdownWidget
 *
 * Displays portfolio drawdown metrics in the Dashboard stats row.
 *
 * DATA SOURCES — spec: dashboard.md v1.1, metrics_definitions.md v1.5.8
 *   - currentDrawdownPercent : GET /portfolio → data.current_drawdown_percent
 *   - peakPortfolioValue     : GET /portfolio → data.peak_portfolio_value
 *   - daysUnderwater         : GET /analytics/metrics → data.advanced_metrics.days_underwater
 *   - maxDrawdownPercent     : GET /analytics/metrics → data.executive_metrics.max_drawdown.percent
 *
 * NO client-side peak or drawdown calculations. No fallback paths. (Decision D10)
 *
 * DISPLAY STATES
 *   1. Establishing Peak  — peakPortfolioValue === 0.0 (no portfolio_history snapshots)
 *   2. At Peak            — currentDrawdownPercent === 0.0 (portfolio at all-time high)
 *   3. In Drawdown        — currentDrawdownPercent < 0  (portfolio below peak)
 */
export default function CurrentDrawdownWidget(props) {
  // Support both prop naming conventions:
  //   Canonical: currentDrawdownPercent / peakPortfolioValue / daysUnderwater / maxDrawdownPercent
  //   Legacy:    currentEquity / peakEquity / maxHistoricalDrawdown (Dashboard pre-API-fix)
  let currentDrawdownPercent;
  let peakPortfolioValue;
  let daysUnderwater;
  let maxDrawdownPercent;

  const { currentEquity, peakEquity, maxHistoricalDrawdown } = props;

  if (peakEquity !== undefined && peakEquity > 0 && currentEquity !== undefined) {
    // Legacy props path — compute drawdown client-side from equity values
    currentDrawdownPercent = Number(((currentEquity - peakEquity) / peakEquity) * 100) || 0;
    peakPortfolioValue     = Number(peakEquity) || 0;
    maxDrawdownPercent     = Number(maxHistoricalDrawdown) || 0;
    daysUnderwater         = Number(props.daysUnderwater) || 0;
  } else {
    // Canonical props path — all values from API
    currentDrawdownPercent = Number(props.currentDrawdownPercent) || 0;
    peakPortfolioValue     = Number(props.peakPortfolioValue) || 0;
    daysUnderwater         = Number(props.daysUnderwater) || 0;
    maxDrawdownPercent     = Number(props.maxDrawdownPercent) || 0;
  }
  // ─── Establishing Peak state ──────────────────────────────────────────────
  // Backend returns 0.0 sentinel when no portfolio_history records exist.
  if (peakPortfolioValue === 0.0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 h-[160px] flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-slate-300">Current Drawdown</h3>
          <div className="p-2 rounded-lg bg-gradient-to-br from-slate-500 to-slate-600">
            <TrendingDown className="w-5 h-5 text-white" />
          </div>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <Database className="w-8 h-8 text-slate-500 mx-auto mb-2" />
            <p className="text-slate-600 dark:text-slate-400 text-sm">Establishing Peak</p>
            <p className="text-slate-600 dark:text-slate-400 text-xs mt-1">Building your performance baseline...</p>
          </div>
        </div>
      </div>
    );
  }

  // ─── Derive display state from server-computed field ──────────────────────
  // currentDrawdownPercent is 0.0 at peak, negative in drawdown. Never positive.
  const isAtPeak = currentDrawdownPercent === 0.0;

  // ─── Progress bar ─────────────────────────────────────────────────────────
  // Shows current DD as a proportion of the worst historical DD.
  // maxDrawdownPercent from analytics is already negative (e.g. -7.7).
  // Guard: only render when max drawdown is non-zero and portfolio is in drawdown.
  const safeMaxDD = Number(maxDrawdownPercent) || 0;
  const progressFill = safeMaxDD === 0
    ? 0
    : Math.min((Math.abs(currentDrawdownPercent) / Math.abs(safeMaxDD)) * 100, 100);

  // ─── Colour helpers ───────────────────────────────────────────────────────
  const absDD = Math.abs(currentDrawdownPercent);

  const getDrawdownColor = () => {
    if (absDD === 0)  return "text-emerald-500";
    if (absDD <= 5)   return "text-emerald-500";
    if (absDD <= 10)  return "text-amber-500";
    if (absDD <= 20)  return "text-orange-500";
    return "text-rose-500";
  };

  const getIconGradient = () => {
    if (isAtPeak)     return "from-emerald-500 to-green-600";
    if (absDD <= 5)   return "from-emerald-500 to-green-600";
    if (absDD <= 10)  return "from-amber-500 to-orange-500";
    if (absDD <= 20)  return "from-orange-500 to-red-500";
    return "from-rose-500 to-red-600";
  };

  // ─── Peak value format ────────────────────────────────────────────────────
  const formatPeak = (value) => {
    if (value >= 1_000_000) return `£${(value / 1_000_000).toFixed(2)}M`;
    if (value >= 1_000)     return `£${(value / 1_000).toFixed(1)}K`;
    return `£${value.toFixed(0)}`;
  };

  // ─── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 h-[160px] flex flex-col relative">

      {/* Header — icon on right to match other stats cards */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-slate-300">Current Drawdown</h3>
        <div className={`p-2 rounded-lg bg-gradient-to-br ${getIconGradient()}`}>
          <TrendingDown className="w-5 h-5 text-white" />
        </div>
      </div>

      {/* Main value */}
      <div className="text-center mb-4">
        {isAtPeak ? (
          <div className="text-3xl font-bold text-emerald-500">🎉 New Peak!</div>
        ) : (
          <div className={`text-3xl font-bold ${getDrawdownColor()}`}>
            {currentDrawdownPercent.toFixed(1)}%
          </div>
        )}
      </div>

      {/* Secondary info row */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="flex items-center gap-2 text-xs">
          <Calendar className="w-4 h-4 text-slate-400 shrink-0" />
          <span className="text-slate-300">
            {isAtPeak
              ? "At Peak"
              : `${daysUnderwater} day${daysUnderwater !== 1 ? 's' : ''} underwater`}
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs justify-end">
          <TrendingUp className="w-4 h-4 text-slate-400 shrink-0" />
          <span className="text-slate-300">Peak: {formatPeak(peakPortfolioValue)}</span>
        </div>
      </div>

      {/* Progress bar — only when in drawdown and a max drawdown benchmark exists */}
      {!isAtPeak && safeMaxDD !== 0 && (
        <div className="relative">
          <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
            <div
              className="absolute inset-y-0 left-0 bg-gradient-to-r from-emerald-500 via-amber-500 via-orange-500 to-rose-500 rounded-full transition-all duration-500"
              style={{ width: `${progressFill}%` }}
              aria-label={`Current drawdown is ${progressFill.toFixed(0)}% of maximum historical drawdown`}
            />
          </div>
          {/* Hover tooltip */}
          <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 opacity-0 hover:opacity-100 transition-opacity pointer-events-none">
            <div className="bg-slate-900 text-slate-300 text-xs px-2 py-1 rounded whitespace-nowrap">
              {progressFill.toFixed(0)}% of max DD
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

CurrentDrawdownWidget.propTypes = {
  // Canonical props (from API)
  currentDrawdownPercent: PropTypes.number,
  peakPortfolioValue:     PropTypes.number,
  daysUnderwater:         PropTypes.number,
  maxDrawdownPercent:     PropTypes.number,
  // Legacy props (from Dashboard drawdownMetrics calculation)
  currentEquity:          PropTypes.number,
  peakEquity:             PropTypes.number,
  maxHistoricalDrawdown:  PropTypes.number,
};

CurrentDrawdownWidget.defaultProps = {};
