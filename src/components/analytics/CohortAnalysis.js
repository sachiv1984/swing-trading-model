import { useState } from "react";
import { Loader2, CalendarRange } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { cn } from "@/lib/utils";

function getPeriodLabel(dateStr, period) {
  const d = new Date(dateStr);
  if (period === "month") {
    return d.toLocaleString("default", { month: "short", year: "numeric" });
  }
  if (period === "quarter") {
    const q = Math.floor(d.getMonth() / 3) + 1;
    return `Q${q} ${d.getFullYear()}`;
  }
  return String(d.getFullYear());
}

function getPeriodKey(dateStr, period) {
  const d = new Date(dateStr);
  if (period === "month") return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
  if (period === "quarter") return `${d.getFullYear()}-Q${Math.floor(d.getMonth() / 3) + 1}`;
  return String(d.getFullYear());
}

function buildCohorts(trades, period) {
  const map = {};

  trades.forEach((t) => {
    if (!t.entry_date) return;
    const key = getPeriodKey(t.entry_date, period);
    const label = getPeriodLabel(t.entry_date, period);
    if (!map[key]) {
      map[key] = { key, label, trades: 0, wins: 0, totalPnl: 0, totalR: 0, rCount: 0 };
    }
    map[key].trades += 1;
    map[key].totalPnl += t.pnl || 0;
    if ((t.pnl || 0) > 0) map[key].wins += 1;

    // R-multiple if stop available
    if (t.stop_price && t.entry_price && t.exit_price) {
      const risk = Math.abs(t.entry_price - t.stop_price);
      if (risk > 0) {
        map[key].totalR += (t.exit_price - t.entry_price) / risk;
        map[key].rCount += 1;
      }
    }
  });

  return Object.values(map)
    .sort((a, b) => b.key.localeCompare(a.key))
    .map((row) => ({
      label: row.label,
      trades: row.trades,
      winRate: row.trades > 0 ? (row.wins / row.trades) * 100 : 0,
      avgR: row.rCount > 0 ? row.totalR / row.rCount : null,
      netPnl: row.totalPnl,
    }));
}

export default function CohortAnalysis({ trades }) {
  const [period, setPeriod] = useState("month");

  const cohorts = buildCohorts(trades, period);
  const insufficientData = cohorts.length < 3;

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-slate-700/50 flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500 to-fuchsia-600">
            <CalendarRange className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">Cohort Analysis</h3>
            <p className="text-sm text-slate-400">Closed trade performance grouped by entry period</p>
          </div>
        </div>
        <Select value={period} onValueChange={setPeriod}>
          <SelectTrigger className="w-36 bg-slate-800/50 border-slate-700 text-white text-sm">
            <SelectValue />
          </SelectTrigger>
          <SelectContent className="bg-slate-800 border-slate-700">
            <SelectItem value="month">Monthly</SelectItem>
            <SelectItem value="quarter">Quarterly</SelectItem>
            <SelectItem value="year">Yearly</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="p-6">
        {insufficientData ? (
          <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
            <p className="text-sm text-amber-400">
              Not enough closed trades to show {period} cohorts (need at least 3 periods).
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-slate-800/50 rounded-lg">
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Period</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">Trades</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">Win Rate</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">Avg R-Multiple</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">Net P&L (GBP)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {cohorts.map((row, idx) => {
                  const isProfit = row.netPnl >= 0;
                  const rColor =
                    row.avgR == null
                      ? "text-slate-500"
                      : row.avgR >= 1
                      ? "text-emerald-400"
                      : row.avgR >= 0.5
                      ? "text-amber-400"
                      : "text-rose-400";

                  return (
                    <tr key={idx} className="hover:bg-slate-800/20 transition-colors">
                      <td className="px-4 py-3 text-sm font-medium text-slate-200">{row.label}</td>
                      <td className="px-4 py-3 text-right text-sm text-slate-300">{row.trades}</td>
                      <td className="px-4 py-3 text-right text-sm">
                        <span
                          className={cn(
                            "font-medium",
                            row.winRate >= 50 ? "text-emerald-400" : "text-rose-400"
                          )}
                        >
                          {row.winRate.toFixed(1)}%
                        </span>
                      </td>
                      <td className={cn("px-4 py-3 text-right text-sm font-medium", rColor)}>
                        {row.avgR != null ? `${row.avgR >= 0 ? "+" : ""}${row.avgR.toFixed(2)}R` : "—"}
                      </td>
                      <td
                        className={cn(
                          "px-4 py-3 text-right text-sm font-semibold",
                          isProfit ? "text-emerald-400" : "text-rose-400"
                        )}
                      >
                        {isProfit ? "+" : ""}£{row.netPnl.toFixed(2)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
