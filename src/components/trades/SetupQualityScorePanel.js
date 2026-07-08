import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/base44Client";
import { ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "../../lib/utils";

const MIN_TRADES = 20;

function qualLabel(score) {
  if (score >= 80) return { text: "Excellent", cls: "text-emerald-400" };
  if (score >= 60) return { text: "Good", cls: "text-cyan-400" };
  if (score >= 40) return { text: "Fair", cls: "text-amber-400" };
  return { text: "Low", cls: "text-rose-400" };
}

function Skeleton({ className }) {
  return <div className={cn("h-4 bg-slate-700/50 rounded animate-pulse", className)} />;
}

export default function SetupQualityScorePanel({ ticker }) {
  const [expanded, setExpanded] = useState(false);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["setup-quality-score", ticker],
    queryFn: () => api.tradePlans.setupQualityScore(ticker),
    enabled: !!ticker,
    retry: false,
  });

  if (!ticker || isError) return null;

  return (
    <div
      data-testid="setup-quality-score-panel"
      className="rounded-xl bg-slate-800/60 border border-slate-700/50 p-4"
    >
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wide">
          Setup Quality Score
        </span>
        {!isLoading && data && !data.gate_not_met && (
          <button
            type="button"
            onClick={() => setExpanded((v) => !v)}
            className="text-slate-600 dark:text-slate-400 hover:text-slate-300 transition-colors"
            aria-label={expanded ? "Collapse details" : "Expand details"}
          >
            {expanded ? (
              <ChevronUp className="w-4 h-4" />
            ) : (
              <ChevronDown className="w-4 h-4" />
            )}
          </button>
        )}
      </div>

      {isLoading && (
        <Skeleton className="w-24 h-6 mt-1" />
      )}

      {!isLoading && data?.gate_not_met && (
        <p
          data-testid="setup-quality-gate-not-met"
          className="text-xs text-slate-600 dark:text-slate-400 mt-1"
        >
          Insufficient trade history (&lt; {MIN_TRADES} trades) — score not yet available
          {data.current_trades != null && (
            <span className="ml-1 text-slate-600 dark:text-slate-400">({data.current_trades}/{MIN_TRADES})</span>
          )}
        </p>
      )}

      {!isLoading && data && !data.gate_not_met && (
        <>
          <div className="flex items-center gap-3 mt-1">
            <span
              data-testid="setup-quality-score-value"
              className="text-2xl font-semibold text-white"
            >
              {data.score}
            </span>
            <span
              data-testid="setup-quality-score-label"
              className={cn("text-sm font-medium", qualLabel(data.score).cls)}
            >
              {qualLabel(data.score).text}
            </span>
          </div>

          {expanded && (
            <div
              data-testid="setup-quality-score-detail"
              className="mt-3 grid grid-cols-3 gap-3 text-xs"
            >
              <div>
                <p className="text-slate-600 dark:text-slate-400 mb-0.5">Trades</p>
                <p className="text-slate-200 font-medium">{data.matching_trades}</p>
              </div>
              <div>
                <p className="text-slate-600 dark:text-slate-400 mb-0.5">Win Rate</p>
                <p className="text-slate-200 font-medium">{data.win_rate}%</p>
              </div>
              <div>
                <p className="text-slate-600 dark:text-slate-400 mb-0.5">Avg Return</p>
                <p className="text-slate-200 font-medium">
                  {data.average_pnl_pct != null ? `${data.average_pnl_pct}%` : "—"}
                </p>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
