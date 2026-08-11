import { useQuery } from "@tanstack/react-query";
import { ClipboardCheck, TrendingUp, XCircle, FileQuestion } from "lucide-react";
import { cn } from "../../lib/utils";
import { api } from "../../api/base44Client";
import DataState from "../ui/DataState";

const RATE_GREEN_THRESHOLD = 60;
const RATE_AMBER_THRESHOLD = 40;
const PERCENT_MULTIPLIER = 100;

function rateColour(rate) {
  if (rate >= RATE_GREEN_THRESHOLD) return "text-emerald-400";
  if (rate >= RATE_AMBER_THRESHOLD) return "text-amber-400";
  return "text-rose-400";
}

function SummaryCards({ plansCreated, completionRate, plansAbandoned, abandonedPct }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div className="p-4 rounded-lg bg-slate-900/50 border border-slate-700/30">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 rounded-lg bg-cyan-500/20">
            <ClipboardCheck className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wider">Plans Created</p>
        </div>
        <p className="text-2xl font-bold text-white">{plansCreated}</p>
      </div>

      <div className="p-4 rounded-lg bg-slate-900/50 border border-slate-700/30">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 rounded-lg bg-emerald-500/20">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wider">Completion Rate</p>
        </div>
        <p className={cn("text-2xl font-bold", rateColour(completionRate ?? 0))}>
          {completionRate != null ? `${completionRate.toFixed(1)}%` : "—"}
        </p>
      </div>

      <div className="p-4 rounded-lg bg-slate-900/50 border border-slate-700/30">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 rounded-lg bg-rose-500/20">
            <XCircle className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wider">Plans Abandoned</p>
        </div>
        <p className="text-2xl font-bold text-white">
          {plansAbandoned}{" "}
          <span className="text-sm font-normal text-slate-600 dark:text-slate-400">({abandonedPct}%)</span>
        </p>
      </div>
    </div>
  );
}

export default function TradePlanCompletionRateSection() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["trade-plan-completion-rate"],
    queryFn: () => api.analytics.tradePlanCompletionRate(),
    retry: 1,
  });

  const plansCreated = data?.plans_created ?? 0;
  const plansCompleted = data?.plans_completed ?? 0;
  const plansAbandoned = data?.plans_abandoned ?? 0;
  const completionRate = data?.completion_rate;
  const abandonedPct = plansCreated > 0 ? Math.round((plansAbandoned / plansCreated) * PERCENT_MULTIPLIER) : 0;

  return (
    <div
      data-testid="trade-plan-completion-rate-section"
      className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm"
    >
      <h2 className="text-lg font-semibold text-white mb-4">Trade Plan Completion Rate</h2>
      <DataState
        loading={isLoading}
        error={!!error}
        onRetry={refetch}
        empty={!isLoading && !error && plansCreated === 0}
        emptyIcon={<FileQuestion className="w-10 h-10 text-slate-500" />}
        emptyHeading="No trade plans created yet."
        loadingVariant="skeleton"
        loadingSkeleton={
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="h-24 rounded-lg bg-slate-700/40 animate-pulse" />
            <div className="h-24 rounded-lg bg-slate-700/40 animate-pulse" />
            <div className="h-24 rounded-lg bg-slate-700/40 animate-pulse" />
          </div>
        }
      >
        <SummaryCards
          plansCreated={plansCreated}
          completionRate={completionRate}
          plansAbandoned={plansAbandoned}
          abandonedPct={abandonedPct}
        />
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-4">
          {plansCompleted} of {plansCreated} plans completed
        </p>
      </DataState>
    </div>
  );
}
