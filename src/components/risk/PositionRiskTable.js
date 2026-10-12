import { cn } from "../../lib/utils";
import { ArrowDown, AlertCircle, Clock } from "lucide-react";
import { formatCurrency, formatPercent } from "../../lib/format";

const STATUS_ORDER = { GRACE: 0, LOSING: 1, PROFITABLE: 2 };

const statusBadge = {
  GRACE:      "bg-blue-500/20 text-blue-400 border-blue-500/30",
  LOSING:     "bg-rose-500/20 text-rose-400 border-rose-500/30",
  PROFITABLE: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
};

// ST-10 (EPIC-02, v9.11, BLG-BE-154): risk_dashboard.md §6.6.
const STALE_TEXT = "Live price unavailable. Showing the last stored price converted at today's FX rate.";

function StaleMarker() {
  return (
    <span
      className="inline-flex items-center gap-1 ml-1.5 align-middle"
      data-testid="price-stale-marker"
      title={STALE_TEXT}
      aria-label={STALE_TEXT}
    >
      <Clock className="w-3.5 h-3.5 text-amber-400" aria-hidden="true" />
      <span className="text-xs text-amber-400">stale</span>
    </span>
  );
}

// ST-11 (EPIC-02, v9.11, BLG-FE-206): risk_dashboard.md §6.2a.
const GRACE_STOP_TEXT = "Stops are not enforced during the 10-day grace period. See strategy rules §6.";

function NotEnforced() {
  return (
    <span className="text-xs text-slate-600 dark:text-slate-400" data-testid="stop-not-enforced" title={GRACE_STOP_TEXT}>
      Not enforced (grace)
    </span>
  );
}

// ST-13 (EPIC-02, v9.11, BLG-BE-155): Stop Dist % comes from the API, which
// computes it in native currency. The browser no longer derives it from GBP
// figures that mix entry and live FX (risk_dashboard.md §6.2).
function stopDistancePct(pos) {
  return typeof pos.stop_distance_pct === "number" ? pos.stop_distance_pct : null;
}

export default function PositionRiskTable({ positions = [], error }) {
  const sorted = [...positions]
    .filter((p) => p.status === "open")
    .map((p) => ({ ...p, _stopDist: stopDistancePct(p) }))
    .sort((a, b) => {
      const sA = STATUS_ORDER[a.display_status] ?? 9;
      const sB = STATUS_ORDER[b.display_status] ?? 9;
      if (sA !== sB) return sA - sB;
      // ST-11: within GRACE, stop distance does not apply (§6.4) -- fewest grace days first.
      if (a.display_status === "GRACE") {
        return (a.grace_days_remaining ?? Infinity) - (b.grace_days_remaining ?? Infinity);
      }
      // ascending = smallest distance first = most at risk
      return (a._stopDist ?? Infinity) - (b._stopDist ?? Infinity);
    });

  if (error) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
        <div className="p-4 border-b border-slate-700/50 flex items-center gap-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500/30 to-fuchsia-500/30">
            <ArrowDown className="w-5 h-5 text-violet-400" />
          </div>
          <h3 className="text-sm font-medium text-slate-300">Position Risk</h3>
        </div>
        <div className="p-6 flex items-center gap-3 rounded-b-2xl bg-rose-900/10 border-t border-rose-500/20">
          <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
          <p className="text-sm text-rose-300">Unable to load position data</p>
        </div>
      </div>
    );
  }

  if (sorted.length === 0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 p-8 text-center">
        <p className="text-slate-600 dark:text-slate-400 text-sm">No open positions to display.</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-4 border-b border-slate-700/50 flex items-center gap-3">
        <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500/30 to-fuchsia-500/30">
          <ArrowDown className="w-5 h-5 text-violet-400" />
        </div>
        <h3 className="text-sm font-medium text-slate-300">Position Risk</h3>
        <span className="ml-auto text-xs text-slate-600 dark:text-slate-400">{sorted.length} open</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700/30">
              {["Ticker", "State", "Entry (GBP)", "Current (GBP)", "Stop (GBP)", "Stop Dist %", "Held"].map((h) => (
                <th key={h} className="px-4 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((pos, i) => {
              const dist = pos._stopDist;
              const inGrace = pos.display_status === "GRACE";
              const distColor = dist === null ? "text-slate-600 dark:text-slate-400"
                : dist <= 5 ? "text-rose-400"
                : dist <= 15 ? "text-amber-400"
                : "text-slate-300";

              return (
                <tr
                  key={pos.id ?? i}
                  className={cn("border-b border-slate-700/20 hover:bg-slate-800/30 transition-colors", i % 2 === 0 ? "" : "bg-slate-800/10")}
                >
                  <td className="px-4 py-3 font-semibold text-white">{pos.ticker}</td>
                  <td className="px-4 py-3">
                    <span className={cn("text-xs px-2.5 py-1 rounded-full border font-medium", statusBadge[pos.display_status] ?? "bg-slate-700 text-slate-300 border-slate-600")}>
                      {pos.display_status ?? "—"}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-300 tabular-nums">
                    {/* ST-11: GET /portfolio returns entry_price in GBP for every market. */}
                    {pos.entry_price != null ? formatCurrency(pos.entry_price) : "—"}
                  </td>
                  <td className="px-4 py-3 text-slate-300 tabular-nums">
                    {pos.current_price != null ? formatCurrency(pos.current_price) : "—"}
                    {pos.price_is_stale === true && <StaleMarker />}
                  </td>
                  <td className="px-4 py-3 text-slate-300 tabular-nums">
                    {inGrace ? <NotEnforced /> : pos.current_stop ? formatCurrency(pos.current_stop) : "—"}
                  </td>
                  <td className={cn("px-4 py-3 tabular-nums font-medium", inGrace ? "" : distColor)}>
                    {inGrace ? <NotEnforced /> : dist === null ? "—" : formatPercent(dist)}
                  </td>
                  <td className="px-4 py-3 text-slate-600 dark:text-slate-400 tabular-nums">
                    {pos.holding_days != null ? `${pos.holding_days}d` : "—"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
