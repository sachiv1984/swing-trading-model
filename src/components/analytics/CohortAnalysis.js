import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { BarChart3, AlertCircle, Loader2 } from "lucide-react";
import { api } from "../../api/base44Client";

// Spec: docs/specs/frontend/pages/analytics.md §15
// Endpoint: GET /analytics/cohort?period={month|quarter|year}
// All values backend-computed per metrics_definitions.md v1.7.0

export default function CohortAnalysis() {
  const [cohortPeriod, setCohortPeriod] = useState("month");

  const { data, isLoading, error } = useQuery({
    queryKey: ["analytics-cohort", cohortPeriod],
    queryFn: () => api.analytics.cohort(cohortPeriod),
    retry: 1,
  });

  const periods = [
    { value: "month",   label: "Month" },
    { value: "quarter", label: "Quarter" },
    { value: "year",    label: "Year" },
  ];

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500 to-purple-600">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">Cohort Analysis</h3>
              <p className="text-sm text-slate-400">Performance grouped by entry period</p>
            </div>
          </div>
          <div className="flex gap-1">
            {periods.map((p) => (
              <button
                key={p.value}
                onClick={() => setCohortPeriod(p.value)}
                className={`px-3 py-1.5 text-sm rounded-lg font-medium transition-colors ${
                  cohortPeriod === p.value
                    ? "bg-violet-600 text-white"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-700/50"
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="p-6">
        {isLoading && (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-6 h-6 animate-spin text-slate-500" />
          </div>
        )}

        {error && (
          <div className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <p className="text-sm text-red-300">
              Failed to load cohort data. {error?.message || "Check backend connection."}
            </p>
          </div>
        )}

        {!isLoading && !error && data && !data.has_enough_data && (
          <div className="flex items-center gap-3 p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
            <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0" />
            <p className="text-sm text-amber-300">
              Not enough closed trades to show {cohortPeriod} cohorts.
            </p>
          </div>
        )}

        {!isLoading && !error && data && data.has_enough_data && (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700/50">
                  <th className="pb-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Period
                  </th>
                  <th className="pb-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Trades
                  </th>
                  <th className="pb-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Win Rate
                  </th>
                  <th className="pb-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Avg R-Multiple
                  </th>
                  <th className="pb-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Total P&L
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {data.cohorts.map((cohort, idx) => (
                  <tr key={idx} className="hover:bg-slate-700/20">
                    <td className="py-3 text-sm font-medium text-slate-200">
                      {cohort.period_label}
                    </td>
                    <td className="py-3 text-right text-sm text-slate-300">
                      {cohort.trade_count}
                    </td>
                    <td className="py-3 text-right text-sm text-slate-300">
                      {cohort.win_rate.toFixed(1)}%
                    </td>
                    <td className="py-3 text-right text-sm font-medium">
                      {cohort.avg_r_multiple !== null ? (
                        <span className={cohort.avg_r_multiple >= 0 ? "text-emerald-400" : "text-rose-400"}>
                          {cohort.avg_r_multiple >= 0 ? "+" : ""}{cohort.avg_r_multiple.toFixed(1)}R
                        </span>
                      ) : (
                        <span className="text-slate-500">—</span>
                      )}
                    </td>
                    <td className="py-3 text-right text-sm font-medium">
                      <span className={cohort.total_pnl >= 0 ? "text-emerald-400" : "text-rose-400"}>
                        {cohort.total_pnl >= 0 ? "+" : ""}£{Math.abs(cohort.total_pnl).toFixed(2)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
