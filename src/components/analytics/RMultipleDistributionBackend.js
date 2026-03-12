import { useQuery } from "@tanstack/react-query";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from "recharts";
import { TrendingUp, AlertCircle, Loader2 } from "lucide-react";
import { api } from "../../api/base44Client";

// Spec: docs/specs/frontend/pages/analytics.md §16
// Endpoint: GET /analytics/r-multiple-distribution
// Canonical server-side R-multiple per metrics_definitions.md v1.7.0
// Hard rule: all values sourced from backend — no client-side computation.

function getBucketColor(range) {
  if (range === "< -2R" || range === "-2R to -1R") return "#ef4444";
  if (range === "-1R to 0R") return "#f97316";
  if (range === "0R to 1R") return "#64748b";
  if (range === "1R to 2R") return "#10b981";
  if (range === "2R to 3R") return "#059669";
  if (range === "> 3R")     return "#047857";
  return "#64748b";
}

export default function RMultipleDistributionBackend() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["analytics-r-multiple-distribution"],
    queryFn: () => api.analytics.rMultipleDistribution(),
    retry: 1,
  });

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">R-Multiple Distribution</h3>
            <p className="text-sm text-slate-400">Canonical server-side computation</p>
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
              Failed to load R-multiple distribution. {error?.message || "Check backend connection."}
            </p>
          </div>
        )}

        {!isLoading && !error && data && !data.has_enough_data && (
          <div className="flex items-center gap-3 p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
            <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0" />
            <p className="text-sm text-amber-300">
              Close at least 5 trades to see R-multiple distribution.{" "}
              {data.total_qualifying_trades > 0
                ? `(${data.total_qualifying_trades} qualifying trade${data.total_qualifying_trades !== 1 ? "s" : ""} found)`
                : ""}
            </p>
          </div>
        )}

        {!isLoading && !error && data && data.has_enough_data && (
          <>
            <div className="mb-6">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data.buckets} margin={{ top: 4, right: 4, bottom: 40, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
                  <XAxis
                    dataKey="range"
                    stroke="#64748b"
                    tick={{ fill: "#94a3b8", fontSize: 11 }}
                    angle={-35}
                    textAnchor="end"
                    height={60}
                  />
                  <YAxis
                    stroke="#64748b"
                    tick={{ fill: "#94a3b8", fontSize: 12 }}
                    allowDecimals={false}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1e293b",
                      border: "1px solid #334155",
                      borderRadius: "8px",
                    }}
                    labelStyle={{ color: "#e2e8f0" }}
                    formatter={(value) => [`${value} trades`, "Count"]}
                  />
                  <Bar dataKey="count">
                    {data.buckets.map((entry, idx) => (
                      <Cell key={idx} fill={getBucketColor(entry.range)} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
                <div className="text-2xl font-bold text-slate-200">
                  {data.median_r !== null ? `${data.median_r >= 0 ? "+" : ""}${data.median_r.toFixed(2)}R` : "—"}
                </div>
                <div className="text-xs text-slate-500 mt-1">Median R</div>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
                <div className="text-2xl font-bold text-cyan-400">
                  {data.pct_above_1r !== null ? `${data.pct_above_1r.toFixed(1)}%` : "—"}
                </div>
                <div className="text-xs text-slate-500 mt-1">Trades &gt; 1R</div>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
                <div className="text-2xl font-bold text-emerald-400">
                  {data.avg_winner_r !== null ? `+${data.avg_winner_r.toFixed(2)}R` : "—"}
                </div>
                <div className="text-xs text-slate-500 mt-1">Avg Winner</div>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
                <div className="text-2xl font-bold text-rose-400">
                  {data.avg_loser_r !== null ? `${data.avg_loser_r.toFixed(2)}R` : "—"}
                </div>
                <div className="text-xs text-slate-500 mt-1">Avg Loser</div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
