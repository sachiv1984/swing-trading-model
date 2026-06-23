import { useQuery } from "@tanstack/react-query";
import { api } from "../../../api/base44Client";

const GATE_THRESHOLD = 20;

export default function GateProgressStrip() {
  const { data, isError } = useQuery({
    queryKey: ["home-gate-metrics"],
    queryFn: api.portfolio.gateMetrics,
    staleTime: 120_000,
  });

  if (isError || !data) return null;

  const metrics = data ?? {};
  const closed = metrics.closed_trades_count ?? 0;
  const threshold = metrics.gate_threshold ?? GATE_THRESHOLD;
  const gateMet = metrics.gate_met ?? closed >= threshold;
  const progressPct = Math.min((closed / threshold) * 100, 100);

  if (gateMet) {
    return (
      <div
        className="rounded-lg bg-emerald-500/10 border border-emerald-500/30 px-4 py-2 flex items-center gap-2"
        data-testid="gate-progress-strip"
      >
        <span className="text-sm text-emerald-400 font-medium">Quality insights unlocked ✓</span>
        <span className="text-xs text-slate-500">
          {closed} closed trades
        </span>
      </div>
    );
  }

  return (
    <div
      className="rounded-lg bg-slate-900 border border-slate-800 px-4 py-3"
      data-testid="gate-progress-strip"
    >
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-xs text-slate-400">
          {closed}/{threshold} closed trades · {threshold - closed} more to unlock quality insights
        </span>
        <span className="text-xs text-slate-500">{Math.round(progressPct)}%</span>
      </div>
      <div className="h-1.5 rounded-full bg-slate-700 overflow-hidden">
        <div
          className="h-full rounded-full bg-blue-500 transition-all"
          style={{ width: `${progressPct}%` }}
        />
      </div>
    </div>
  );
}
