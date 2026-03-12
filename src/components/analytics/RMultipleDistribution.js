import { useQuery } from "@tanstack/react-query";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer, Cell } from "recharts";
import { TrendingUp, Loader2, AlertCircle } from "lucide-react";
import { api } from "@/api/base44Client";

const getBarColor = (range) => {
  if (!range) return "#64748b";
  if (range.startsWith("-")) return "#ef4444";
  if (range.startsWith("0")) return "#64748b";
  return "#10b981";
};

export default function RMultipleDistribution() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["r-multiple-distribution"],
    queryFn: () => api.analytics.rMultipleDistribution(),
    retry: 1,
  });

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">R-Multiple Distribution</h3>
            <p className="text-sm text-slate-400">Canonical metric — server-side computed frequency of R-multiple outcomes</p>
          </div>
        </div>
      </div>

      <div className="p-6">
        {isLoading && (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 p-4 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-400">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <p className="text-sm">Failed to load R-multiple distribution data.</p>
          </div>
        )}

        {!isLoading && !error && (!data?.buckets || data.buckets.length === 0) && (
          <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
            <p className="text-sm text-amber-400">Not enough closed trades for R-multiple distribution.</p>
          </div>
        )}

        {!isLoading && !error && data?.buckets?.length > 0 && (
          <div className="space-y-6">
            {/* Stat cards */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
                <div className="text-xs text-slate-500 mb-1">Mean R</div>
                <div className={`text-2xl font-bold ${(data.mean ?? 0) >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                  {data.mean != null ? `${data.mean >= 0 ? "+" : ""}${data.mean.toFixed(2)}R` : "—"}
                </div>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
                <div className="text-xs text-slate-500 mb-1">Median R</div>
                <div className={`text-2xl font-bold ${(data.median ?? 0) >= 0 ? "text-cyan-400" : "text-rose-400"}`}>
                  {data.median != null ? `${data.median >= 0 ? "+" : ""}${data.median.toFixed(2)}R` : "—"}
                </div>
              </div>
            </div>

            {/* Histogram */}
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={data.buckets} margin={{ top: 8, right: 8, left: 0, bottom: 40 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
                <XAxis
                  dataKey="range"
                  stroke="#64748b"
                  tick={{ fill: "#94a3b8", fontSize: 11 }}
                  angle={-40}
                  textAnchor="end"
                  height={60}
                />
                <YAxis
                  stroke="#64748b"
                  tick={{ fill: "#94a3b8", fontSize: 12 }}
                  allowDecimals={false}
                  label={{ value: "Frequency", angle: -90, position: "insideLeft", fill: "#64748b", fontSize: 11 }}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px" }}
                  labelStyle={{ color: "#e2e8f0" }}
                  itemStyle={{ color: "#94a3b8" }}
                  formatter={(v) => [v, "Trades"]}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {data.buckets.map((entry, i) => (
                    <Cell key={i} fill={getBarColor(entry.range)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}
