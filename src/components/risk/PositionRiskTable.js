import { cn } from "../../lib/utils";
import { format } from "date-fns";
import { ArrowDown } from "lucide-react";

const STATUS_ORDER = { GRACE: 0, LOSING: 1, PROFITABLE: 2 };

const statusBadge = {
  GRACE:      "bg-amber-500/20 text-amber-400 border-amber-500/30",
  LOSING:     "bg-rose-500/20 text-rose-400 border-rose-500/30",
  PROFITABLE: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
};

function stopDistancePct(pos) {
  if (!pos.current_price || !pos.current_stop || pos.current_price === 0) return null;
  return ((pos.current_price - pos.current_stop) / pos.current_price) * 100;
}

export default function PositionRiskTable({ positions = [] }) {
  const sorted = [...positions]
    .filter((p) => p.status === "open")
    .map((p) => ({ ...p, _stopDist: stopDistancePct(p) }))
    .sort((a, b) => {
      const sA = STATUS_ORDER[a.display_status] ?? 9;
      const sB = STATUS_ORDER[b.display_status] ?? 9;
      if (sA !== sB) return sA - sB;
      // Within group: higher stop distance = more at risk first
      return (b._stopDist ?? -Infinity) - (a._stopDist ?? -Infinity);
    });

  const currSym = (pos) => pos.market === "UK" ? "£" : "$";

  if (sorted.length === 0) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 p-8 text-center">
        <p className="text-slate-500 text-sm">No open positions to display.</p>
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
        <span className="ml-auto text-xs text-slate-500">{sorted.length} open</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700/30">
              {["Ticker", "Status", "Entry Price", "Current (GBP)", "Stop Dist %", "Held"].map((h) => (
                <th key={h} className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((pos, i) => {
              const dist = pos._stopDist;
              const distColor = dist === null ? "text-slate-400"
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
                    {pos.entry_price != null ? `${currSym(pos)}${Number(pos.entry_price).toFixed(2)}` : "—"}
                  </td>
                  <td className="px-4 py-3 text-slate-300 tabular-nums">
                    {pos.current_price != null ? `£${Number(pos.current_price).toFixed(2)}` : "—"}
                  </td>
                  <td className={cn("px-4 py-3 tabular-nums font-medium", distColor)}>
                    {dist === null ? "—" : `${dist.toFixed(1)}%`}
                  </td>
                  <td className="px-4 py-3 text-slate-400 tabular-nums">
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
