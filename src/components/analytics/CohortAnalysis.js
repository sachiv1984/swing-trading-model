import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Loader2, CalendarRange } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { cn } from "../../lib/utils";
import { api } from "../../api/base44Client";
import { formatCurrency, formatPercent, formatR } from "../../lib/format";

export default function CohortAnalysis() {
  const [period, setPeriod] = useState("month");

  const { data, isLoading, error } = useQuery({
    queryKey: ["cohort-analysis", period],
    queryFn: () => api.analytics.cohort(period),
    retry: 1,
  });

  return (
    <div className="rounded-2xl bg-app-raised border border-app-line backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-app-line flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500 to-fuchsia-600">
            <CalendarRange className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-app-fg">Cohort Analysis</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">Closed trade performance grouped by entry period</p>
          </div>
        </div>
        <Select value={period} onValueChange={setPeriod}>
          <SelectTrigger aria-label="Cohort period" className="w-36 bg-app-raised border-slate-200 dark:border-slate-700 text-app-fg text-sm">
            <SelectValue />
          </SelectTrigger>
          <SelectContent className="bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700">
            <SelectItem value="month">Monthly</SelectItem>
            <SelectItem value="quarter">Quarterly</SelectItem>
            <SelectItem value="year">Yearly</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="p-6">
        {isLoading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="w-5 h-5 animate-spin text-app-muted" />
          </div>
        ) : error ? (
          <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-lg">
            <p className="text-sm text-app-negative">Failed to load cohort data.</p>
          </div>
        ) : data?.has_enough_data === false ? (
          <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
            <p className="text-sm text-app-warning">
              Not enough closed trades to show {period} cohorts (need at least 3 periods).
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-app-raised rounded-lg">
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">Period</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">Trades</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">Win Rate</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">Avg R-Multiple</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">Net P&L (GBP)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-700/30">
                {(data?.cohorts ?? []).map((row, idx) => {
                  const rColor =
                    row.avg_r_multiple == null
                      ? "text-slate-600 dark:text-slate-400"
                      : row.avg_r_multiple >= 1
                      ? "text-app-positive"
                      : row.avg_r_multiple >= 0.5
                      ? "text-app-warning"
                      : "text-app-negative";

                  return (
                    <tr key={idx} className="hover:bg-slate-100 dark:hover:bg-slate-800/20 transition-colors">
                      <td className="px-4 py-3 text-sm font-medium text-slate-800 dark:text-slate-200">{row.period_label}</td>
                      <td className="px-4 py-3 text-right text-sm text-slate-700 dark:text-slate-300">{row.trade_count}</td>
                      <td className="px-4 py-3 text-right text-sm">
                        <span
                          className={cn(
                            "font-medium",
                            row.win_rate >= 50 ? "text-app-positive" : "text-app-negative"
                          )}
                        >
                          {formatPercent(row.win_rate)}
                        </span>
                      </td>
                      <td className={cn("px-4 py-3 text-right text-sm font-medium", rColor)}>
                        {row.avg_r_multiple != null ? formatR(row.avg_r_multiple) : "—"}
                      </td>
                      <td
                        className={cn(
                          "px-4 py-3 text-right text-sm font-semibold",
                          row.total_pnl > 0 ? "text-app-positive" : row.total_pnl < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300"
                        )}
                      >
                        {formatCurrency(row.total_pnl, { signed: true })}
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
