/**
 * PlanVsReality — Plan vs Reality comparison section for Trade Journal
 *
 * Renders inside the Trade History expandable row as a 5th section (after Strategy Tags).
 * Lazy-fetches GET /trades/{id}/plan-vs-reality only when mounted (row expanded).
 * Hidden when: no plan (404), trade still open, or network error.
 *
 * Spec: docs/ux_specs/plan-vs-reality/ux_spec.md v1.0
 * ST-06, EPIC-02, v3.5; ST-02, EPIC-01, v3.6 (entry_delta_pct)
 */
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../../api/base44Client";
import { cn } from "../../lib/utils";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// ─── Lifecycle state badge config (mirrored from Positions.js §ST-01) ─────────
const LIFECYCLE_CONFIG = {
  GRACE:       { label: "GRACE",       bg: "bg-blue-600"   },
  LOSING:      { label: "LOSING",      bg: "bg-red-600"    },
  PROFITABLE:  { label: "PROFITABLE",  bg: "bg-green-700"  },
  "EXIT ZONE": { label: "EXIT ZONE",   bg: "bg-violet-600" },
  UNKNOWN:     { label: "UNKNOWN",     bg: "bg-gray-500"   },
};

function StateBadge({ state }) {
  const cfg = LIFECYCLE_CONFIG[state] || LIFECYCLE_CONFIG.UNKNOWN;
  return (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold text-white whitespace-nowrap", cfg.bg)}>
      {cfg.label}
    </span>
  );
}

// ─── R colour coding (spec §3.2: green ≥ target, amber ≥ 80%, red < 80%) ─────
function rColourClass(rAchieved, rTarget) {
  if (rAchieved == null) return "text-slate-300";
  if (rTarget == null)   return "text-slate-300";
  if (rAchieved >= rTarget)              return "text-emerald-400";
  if (rAchieved >= rTarget * 0.8)        return "text-amber-400";
  return "text-rose-400";
}

// ─── Skeleton loader ───────────────────────────────────────────────────────────
function Skeleton() {
  return (
    <div className="space-y-2 animate-pulse" data-testid="pvr-skeleton">
      <div className="h-3 bg-slate-700 rounded w-1/2" />
      <div className="h-3 bg-slate-700 rounded w-3/4" />
    </div>
  );
}

// ─── Comparison row ────────────────────────────────────────────────────────────
function CompRow({ label, planned, actual, actualClass }) {
  return (
    <div className="grid grid-cols-3 gap-2 text-xs items-baseline">
      <span className="text-slate-400 font-medium">{label}</span>
      <span className="text-slate-400 truncate">{planned ?? "—"}</span>
      <span className={cn("font-semibold truncate", actualClass || "text-slate-200")}>{actual ?? "—"}</span>
    </div>
  );
}

// ─── Plan adherence badge ──────────────────────────────────────────────────────
function AdherenceBadge({ flag }) {
  const config = {
    on_plan:         { label: "On Plan",      cls: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
    entry_deviation: { label: "Entry Deviation", cls: "bg-amber-500/20 text-amber-300 border-amber-500/30" },
    stop_deviation:  { label: "Stop Deviation",  cls: "bg-amber-500/20 text-amber-300 border-amber-500/30" },
    early_exit:      { label: "Early Exit",      cls: "bg-rose-500/20 text-rose-300 border-rose-500/30"    },
  };
  const c = config[flag] || { label: flag || "—", cls: "bg-slate-500/20 text-slate-300 border-slate-500/30" };
  return (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border", c.cls)}>
      {c.label}
    </span>
  );
}

// ─── Main component ────────────────────────────────────────────────────────────
export default function PlanVsReality({ tradeId }) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["planVsReality", tradeId],
    queryFn: async () => {
      const res = await apiFetch(`${API_URL}/trades/${tradeId}/plan-vs-reality`);
      if (res.status === 404) return null;
      if (!res.ok) return null;
      const json = await res.json();
      if (!json || json.data?.status === "trade_open") return null;
      return json.data || null;
    },
    retry: false,
    staleTime: 60_000,
  });

  // Hidden: loading, error, no plan, or trade open
  if (isLoading) {
    return (
      <div className="space-y-2.5">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-blue-400" />
          <h4 className="text-xs font-semibold uppercase tracking-wider text-blue-400">Plan vs Reality</h4>
        </div>
        <div className="w-full bg-slate-800/50 rounded-xl p-4 border border-blue-600/20 shadow-lg">
          <Skeleton />
        </div>
      </div>
    );
  }

  if (isError || !data) return null;

  const { r_achieved, r_target, r_delta, entry_delta_pct, exit_reason_actual, exit_reason_planned,
          lifecycle_state_at_exit, plan_adherence_flag, deviation_note } = data;

  const rClass = rColourClass(r_achieved, r_target);
  const rAchievedLabel = r_achieved != null ? `${r_achieved >= 0 ? "+" : ""}${r_achieved.toFixed(2)}R` : "—";
  const rTargetLabel   = r_target   != null ? `Target: ${r_target.toFixed(2)}R` : "No R target set";

  return (
    <div className="space-y-2.5" data-testid="plan-vs-reality-section">
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-blue-400" />
        <h4 className="text-xs font-semibold uppercase tracking-wider text-blue-400">Plan vs Reality</h4>
        <AdherenceBadge flag={plan_adherence_flag} />
      </div>

      <div className="w-full bg-slate-800/50 rounded-xl border-l-4 border-l-[#2563EB] border border-slate-700/30 shadow-lg">
        <div className="p-4 space-y-3">
          {/* Column headers */}
          <div className="grid grid-cols-3 gap-2 text-xs text-slate-400 font-medium pb-1 border-b border-slate-700/30">
            <span>Metric</span>
            <span>Planned</span>
            <span>Actual</span>
          </div>

          {/* R Achieved vs R Target */}
          <CompRow
            label="R Achieved"
            planned={rTargetLabel}
            actual={rAchievedLabel}
            actualClass={rClass}
          />

          {/* Exit Alignment */}
          <CompRow
            label="Exit Alignment"
            planned={exit_reason_planned ? `Planned: ${exit_reason_planned}` : "No exit conditions recorded"}
            actual={exit_reason_actual ? `Actual: ${exit_reason_actual}` : "—"}
          />

          {/* Entry Delta — AC-01: signed % with colour; AC-02: null → historical placeholder */}
          {entry_delta_pct != null ? (
            <CompRow
              label="Entry Delta"
              planned="—"
              actual={`${entry_delta_pct >= 0 ? "+" : ""}${entry_delta_pct.toFixed(2)}%`}
              actualClass={entry_delta_pct <= 0 ? "text-emerald-400" : "text-rose-400"}
            />
          ) : (
            <div className="grid grid-cols-3 gap-2 text-xs items-baseline" data-testid="entry-delta-historical">
              <span className="text-slate-400 font-medium">Entry Delta</span>
              <span className="col-span-2 text-slate-400 italic">data not available for historical trades</span>
            </div>
          )}

          {/* Lifecycle State at Exit */}
          <div className="grid grid-cols-3 gap-2 text-xs items-center">
            <span className="text-slate-400 font-medium">State at Exit</span>
            <span />
            <span>
              <StateBadge state={lifecycle_state_at_exit || "UNKNOWN"} />
            </span>
          </div>

          {/* R delta summary */}
          {r_delta != null && (
            <div className="pt-2 border-t border-slate-700/30 text-xs text-slate-400">
              R delta:{" "}
              <span className={r_delta >= 0 ? "text-emerald-400 font-semibold" : "text-rose-400 font-semibold"}>
                {r_delta >= 0 ? "+" : ""}{r_delta.toFixed(2)}R vs target
              </span>
            </div>
          )}

          {/* Deviation note (user-authored via future ST-06 annotation flow) */}
          {deviation_note && (
            <div className="pt-2 border-t border-slate-700/30 text-xs text-slate-300 italic">
              Note: {deviation_note}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
