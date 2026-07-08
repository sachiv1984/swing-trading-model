import { useQuery } from "@tanstack/react-query";
import { AlertCircle, Loader2, TrendingUp } from "lucide-react";
import { cn } from "../../lib/utils";
import { api } from "../../api/base44Client";

const SEVERITY_ORDER = { high: 0, moderate: 1, low: 2, unknown: 3 };

const SEVERITY_STYLES = {
  high: "bg-rose-500/20 text-rose-400 border-rose-500/30",
  moderate: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  low: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  unknown: "bg-slate-500/20 text-slate-600 dark:text-slate-400 border-slate-500/30",
};

function SeverityBadge({ severity }) {
  const key = severity || "unknown";
  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border",
        SEVERITY_STYLES[key] || SEVERITY_STYLES.unknown
      )}
    >
      {key.charAt(0).toUpperCase() + key.slice(1)}
    </span>
  );
}

// Market Correlation panel — §18 of analytics.md v1.7 (ST-01, EPIC-01, v2.8)
// Source: GET /analytics/market-correlation
export default function MarketCorrelationSection() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["market-correlation"],
    queryFn: () => api.analytics.marketCorrelation(),
    staleTime: 8 * 60 * 60 * 1000,
    retry: 1,
  });

  const correlations = data?.correlations ?? [];
  const portfolioCorr = data?.portfolio_correlation ?? null;

  const sortedCorrelations = [...correlations].sort((a, b) => {
    const aOrd = SEVERITY_ORDER[a.severity] ?? 3;
    const bOrd = SEVERITY_ORDER[b.severity] ?? 3;
    if (aOrd !== bOrd) return aOrd - bOrd;
    if (a.correlation == null) return 1;
    if (b.correlation == null) return -1;
    return b.correlation - a.correlation;
  });

  const noPositions = !isLoading && !error && correlations.length === 0;

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 space-y-4">
      <div className="flex items-center gap-2">
        <div className="p-2 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-500/20">
          <TrendingUp className="w-4 h-4 text-cyan-400" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-white">Market Correlation</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400">Per-position Pearson correlation vs benchmark</p>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-5 h-5 animate-spin text-slate-500" />
        </div>
      ) : error ? (
        <div className="flex items-center gap-2 text-rose-400 text-sm py-4">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>Unable to load correlation data. Please try again later.</span>
        </div>
      ) : noPositions ? (
        <p className="text-slate-600 dark:text-slate-400 text-sm py-4">No open positions to correlate.</p>
      ) : (
        <>
          {portfolioCorr && (
            <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-slate-900/50 border border-slate-700/30">
              <div className="flex-1">
                <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-1">Portfolio Weighted Average</p>
                <div className="flex items-center gap-2">
                  <span className="text-xl font-bold text-white">
                    {portfolioCorr.value != null ? portfolioCorr.value.toFixed(2) : "N/A"}
                  </span>
                  {portfolioCorr.severity && portfolioCorr.value != null && (
                    <SeverityBadge severity={portfolioCorr.severity} />
                  )}
                </div>
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-400 text-right max-w-[140px]">
                High correlation signals clustered risk
              </p>
            </div>
          )}

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700/50">
                  <th className="text-left py-2 pr-4 text-xs text-slate-600 dark:text-slate-400 font-medium uppercase tracking-wider">Ticker</th>
                  <th className="text-left py-2 pr-4 text-xs text-slate-600 dark:text-slate-400 font-medium uppercase tracking-wider">Correlation</th>
                  <th className="text-left py-2 pr-4 text-xs text-slate-600 dark:text-slate-400 font-medium uppercase tracking-wider">Severity</th>
                  <th className="text-left py-2 text-xs text-slate-600 dark:text-slate-400 font-medium uppercase tracking-wider">vs. Market</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {sortedCorrelations.map((row) => (
                  <tr key={row.ticker} className="hover:bg-slate-700/20 transition-colors">
                    <td className="py-2.5 pr-4 font-mono text-white font-medium">{row.ticker?.toUpperCase()}</td>
                    <td className="py-2.5 pr-4 text-slate-300">
                      {row.correlation != null ? row.correlation.toFixed(2) : "N/A"}
                    </td>
                    <td className="py-2.5 pr-4">
                      {row.correlation != null ? (
                        <SeverityBadge severity={row.severity} />
                      ) : (
                        <span className="text-slate-600 dark:text-slate-400 text-xs">—</span>
                      )}
                    </td>
                    <td className="py-2.5 text-slate-600 dark:text-slate-400 text-xs">{row.benchmark ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
