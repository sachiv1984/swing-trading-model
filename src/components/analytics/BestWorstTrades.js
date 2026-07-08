import { format } from "date-fns";
import { TrendingUp, TrendingDown, Trophy, AlertTriangle } from "lucide-react";
import { cn } from "../../lib/utils";

// ─────────────────────────────────────────────────────────────────────────────
// BestWorstTrades — Component 11 (BLG-FEAT-04)
// Spec: analytics.md v1.2 §Best / Worst Trades
//
// Source: trades_for_charts from GET /analytics/metrics
// Ranking: R-multiple (frontend-calculated). Formula per metrics_definitions.md v1.5.7.
//   R = (exit_price - entry_price) / (entry_price - stop_price)
//
// Exclusion: trades where stopPrice is null, zero, or <= 0 denom (invalid stop) are excluded.
// Panel size: top 3 / bottom 3. Partial panels rendered when < 3 qualify.
// Empty state: "No trades with stop data available." when zero qualifying trades.
// Placement: below Top Performers (Component 10 in render order).
// ─────────────────────────────────────────────────────────────────────────────

function calcR(trade) {
  const { entryPrice, exitPrice, stopPrice } = trade;
  if (!stopPrice || stopPrice === 0) return null;
  const denom = entryPrice - stopPrice;
  if (denom <= 0) return null;  // invalid stop (at or above entry)
  return (exitPrice - entryPrice) / denom;
}

function formatR(r) {
  const sign = r >= 0 ? "+" : "";
  return `${sign}${r.toFixed(2)}R`;
}

function formatPnL(pnl) {
  const sign = pnl >= 0 ? "+" : "-";
  return `${sign}£${Math.abs(pnl).toFixed(2)}`;
}

function formatDate(dateStr) {
  if (!dateStr) return "—";
  try {
    return format(new Date(dateStr), "MMM d, yyyy");
  } catch {
    return dateStr;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// TradeCard — individual trade card within a panel
// ─────────────────────────────────────────────────────────────────────────────
function TradeCard({ trade, rValue, isBest }) {
  const rText  = formatR(rValue);
  const pnlPos = (trade.pnl ?? 0) >= 0;

  return (
    <div className={cn(
      "p-4 rounded-xl border transition-colors",
      isBest
        ? "bg-emerald-500/5 border-emerald-500/20 hover:bg-emerald-500/10"
        : "bg-rose-500/5 border-rose-500/20 hover:bg-rose-500/10"
    )}>
      {/* Top row: ticker + R-multiple */}
      <div className="flex items-start justify-between mb-3">
        <span className="font-bold text-white text-base">{trade.ticker?.replace(".L", "") || "—"}</span>
        <span className={cn(
          "font-bold text-lg tabular-nums",
          isBest ? "text-emerald-400" : "text-rose-400"
        )}>
          {rText}
        </span>
      </div>

      {/* Secondary row: P&L + exit date */}
      <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
        <span className={cn("font-medium", pnlPos ? "text-emerald-400" : "text-rose-400")}>
          {formatPnL(trade.pnl ?? 0)}
        </span>
        <span>{formatDate(trade.exitDate)}</span>
      </div>

      {/* Exit reason */}
      {trade.exitReason && (
        <div className="mt-1">
          <span className="text-xs text-slate-400 capitalize">
            {trade.exitReason.replace(/_/g, " ")}
          </span>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Panel — one side (best or worst)
// ─────────────────────────────────────────────────────────────────────────────
function Panel({ title, trades, isBest, emptyMessage }) {
  const Icon = isBest ? Trophy : AlertTriangle;

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      {/* Header */}
      <div className="flex items-center gap-3 mb-5">
        <div className={cn(
          "p-2 rounded-lg",
          isBest ? "bg-emerald-500/20" : "bg-rose-500/20"
        )}>
          <Icon className={cn("w-5 h-5", isBest ? "text-emerald-400" : "text-rose-400")} />
        </div>
        <div>
          <h3 className="text-base font-semibold text-white">{title}</h3>
          <p className={cn("text-xs mt-0.5", isBest ? "text-emerald-400/70" : "text-rose-400/70")}>
            By R-Multiple
          </p>
        </div>
      </div>

      {/* Cards or empty state */}
      {trades.length === 0 ? (
        <div className="flex items-center justify-center py-8">
          <p className="text-slate-400 text-sm">{emptyMessage}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {trades.map((item, idx) => (
            <TradeCard
              key={item.trade.id ?? idx}
              trade={item.trade}
              rValue={item.r}
              isBest={isBest}
            />
          ))}
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// BestWorstTrades — exported component
// ─────────────────────────────────────────────────────────────────────────────

/**
 * @param {object[]} tradesForCharts — analyticsData.tradesForCharts
 *   Each entry must carry: id, ticker, entryPrice, exitPrice, stopPrice,
 *   pnl, exitDate, exitReason.
 *   (camelCase — toCamelCase() applied by PerformanceAnalytics before passing data)
 */
export default function BestWorstTrades({ tradesForCharts = [] }) {
  // ── Diagnostic log (remove after F-17 confirmed working) ──────────────────
  console.log('[BestWorstTrades] received', tradesForCharts?.length, 'trades');
  if (tradesForCharts?.length > 0) {
    const t = tradesForCharts[0];
    console.log('[BestWorstTrades] first trade keys:', Object.keys(t));
    console.log('[BestWorstTrades] first trade stopPrice/stop_price:',
      t.stopPrice, '/', t.stop_price,
      '| entryPrice/entry_price:', t.entryPrice, '/', t.entry_price);
  }
  // ──────────────────────────────────────────────────────────────────────────

  // Derive qualifying trades and their R-multiples
  const qualified = (tradesForCharts || []).reduce((acc, trade) => {
    const r = calcR(trade);
    if (r !== null) acc.push({ trade, r });
    return acc;
  }, []);

  // If no qualifying trades exist, render empty state for both panels
  if (qualified.length === 0) {
    const emptyMsg = "No trades with stop data available.";
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Panel title="Best Trades (R-Multiple)"  isBest={true}  trades={[]} emptyMessage={emptyMsg} />
        <Panel title="Worst Trades (R-Multiple)" isBest={false} trades={[]} emptyMessage={emptyMsg} />
      </div>
    );
  }

  // Sort descending by R for best panel (take first 3)
  const sortedDesc = [...qualified].sort((a, b) => b.r - a.r);
  const bestTrades  = sortedDesc.slice(0, 3);

  // Sort ascending by R for worst panel (take first 3 = most negative)
  const sortedAsc  = [...qualified].sort((a, b) => a.r - b.r);
  const worstTrades = sortedAsc.slice(0, 3);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Panel
        title="Best Trades (R-Multiple)"
        isBest={true}
        trades={bestTrades}
        emptyMessage="No qualifying trades."
      />
      <Panel
        title="Worst Trades (R-Multiple)"
        isBest={false}
        trades={worstTrades}
        emptyMessage="No qualifying trades."
      />
    </div>
  );
}
