import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useEarnings } from "../hooks/useEarnings";
import { useGapRisk } from "../hooks/useGapRisk";
import { base44, api, apiFetch } from "../api/base44Client";
import {
  LayoutGrid,
  List,
  BookOpen,
  Plus,
  Edit2,
  LogOut,
  TrendingUp,
  TrendingDown,
  FolderOpen,
  AlertTriangle,
  X,
  ArrowUpDown,
  Zap,
  Clock,
  Check,
} from "lucide-react";

import DataState from "../components/ui/DataState";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import PositionCard from "../components/positions/PositionCard";
import PositionModal from "../components/positions/PositionModal";
import ExitModal from "../components/positions/ExitModal";
import JournalView from "../components/positions/JournalView";
import TradeReflectionModal from "../components/trades/TradeReflectionModal";
import ComplianceRecheckModal from "../components/positions/ComplianceRecheckModal";
import TrailingStopExplainerIcon from "../components/positions/TrailingStopExplainerIcon";
import {
  DataTable,
  TableHeader,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
} from "../components/ui/DataTable";
import { cn } from "../lib/utils";
import { friendlyErrorMessage } from "../lib/apiError";
import { differenceInDays } from "date-fns";
import { Link, useNavigate } from "react-router-dom";
import { createPageUrl } from "../utils";
import MetricsStalenessIndicator from "../components/analytics/MetricsStalenessIndicator";
import StrategyCompliancePanel from "../components/positions/StrategyCompliancePanel";
import PaperAccountPanel from "../components/positions/PaperAccountPanel";
import AiChatWidget from "../components/AiChatWidget";
import { toast } from "sonner";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

// ---------------------------------------------------------------------------
// ST-01 (IT-01) — Lifecycle state badge
// ---------------------------------------------------------------------------

const LIFECYCLE_CONFIG = {
  GRACE:      { label: "GRACE",      bg: "bg-blue-600",   tip: "Exits grace when position moves > 0.5 ATR or after 10 trading days" },
  LOSING:     { label: "LOSING",     bg: "bg-red-600",    tip: "Exits when price rises above entry by 0.5 ATR" },
  PROFITABLE: { label: "PROFITABLE", bg: "bg-green-700",  tip: "Advances to Exit Zone when P&L reaches 2R target" },
  "EXIT ZONE":{ label: "EXIT ZONE",  bg: "bg-violet-600", tip: "Position has reached R-target. Review stop or exit." },
  UNKNOWN:    { label: "UNKNOWN",    bg: "bg-gray-500",   tip: "Set a stop and R-target on the linked trade plan to enable lifecycle tracking." },
};

function LifecycleBadge({ state, daysInState }) {
  const cfg = LIFECYCLE_CONFIG[state] || LIFECYCLE_CONFIG.UNKNOWN;
  const label = state === "GRACE" && daysInState != null
    ? `GRACE — ${daysInState}d`
    : cfg.label;
  return (
    <span
      className={cn("inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold text-white whitespace-nowrap", cfg.bg)}
      title={cfg.tip}
      aria-label={`Position state: ${state}${daysInState != null ? `, ${daysInState} days in state` : ""}`}
    >
      {label}
    </span>
  );
}

// ---------------------------------------------------------------------------
// ST-02 (IT-02) — Grace period alert card
// ---------------------------------------------------------------------------

const GRACE_DISMISS_KEY = (positionId) => `grace_alert_dismissed_${positionId}`;

function GracePeriodAlertZone() {
  const { data: alerts = [] } = useQuery({
    queryKey: ["gracePeriodAlerts"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/positions/grace-period-alerts`);
      const json = await res.json();
      return json.data || [];
    },
    staleTime: 60000,
  });

  const [dismissed, setDismissed] = useState(() => {
    const d = {};
    alerts.forEach((a) => {
      if (sessionStorage.getItem(GRACE_DISMISS_KEY(a.position_id))) d[a.position_id] = true;
    });
    return d;
  });

  const dismiss = (positionId) => {
    sessionStorage.setItem(GRACE_DISMISS_KEY(positionId), "1");
    setDismissed((prev) => ({ ...prev, [positionId]: true }));
  };

  const visible = alerts.filter((a) => !dismissed[a.position_id]);
  if (visible.length === 0) return null;

  return (
    <div role="alert" aria-live="polite" className="space-y-3">
      {visible.map((alert) => {
        const daysLeft = 10 - alert.days_in_state;
        const bodyText = alert.days_in_state >= 10
          ? "Grace period has ended. Your position will transition to LOSING or PROFITABLE on next refresh."
          : `Your grace period ends in ${daysLeft} trading day${daysLeft !== 1 ? "s" : ""}. Review your original thesis before the window closes.`;
        const tp = alert.trade_plan_summary;

        return (
          <div
            key={alert.position_id}
            className="rounded-xl border-l-4 border-amber-500 bg-amber-500/10 px-4 py-3"
            style={{ borderLeftColor: "#D97706" }}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2 text-amber-300 font-semibold text-sm">
                <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                Grace Period Alert — {alert.ticker}
                <span className="text-xs font-medium text-amber-400 bg-amber-500/20 px-1.5 py-0.5 rounded">
                  Day {alert.days_in_state} of 10
                </span>
              </div>
              <button
                onClick={() => dismiss(alert.position_id)}
                aria-label={`Dismiss grace period alert for ${alert.ticker}`}
                className="text-amber-400/60 hover:text-amber-300 flex-shrink-0"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <p className="text-sm text-amber-200/80 mt-1">{bodyText}</p>
            {tp ? (
              <div className="mt-2 text-xs text-slate-300 space-y-0.5">
                {tp.setup_thesis && <div><span className="text-slate-600 dark:text-slate-400">Thesis: </span>"{tp.setup_thesis.slice(0, 120)}{tp.setup_thesis.length > 120 ? "…" : ""}"</div>}
                {tp.stop_level != null && <div><span className="text-slate-600 dark:text-slate-400">Stop: </span>{tp.stop_level}</div>}
                {tp.r_target != null && <div><span className="text-slate-600 dark:text-slate-400">R-target: </span>{tp.r_target}R</div>}
              </div>
            ) : (
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">No trade plan linked. Consider adding a plan for context.</p>
            )}
            {alert.trade_plan_id && (
              <Link
                to={`/TradePlan?edit=${alert.trade_plan_id}&ticker=${alert.ticker}`}
                className="inline-block mt-2 text-xs text-amber-400 hover:text-amber-300 underline"
              >
                View Trade Plan →
              </Link>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// ST-03 (IT-03) — Trail Stop modal
// ---------------------------------------------------------------------------

function TrailStopModal({ position, onClose }) {
  const queryClient = useQueryClient();
  const isEligible = position?.lifecycle_state === "PROFITABLE" || position?.lifecycle_state === "EXIT ZONE";
  const hasStop = position?.current_stop != null || position?.stop_price != null;
  const stopValue = position?.current_stop ?? position?.stop_price;

  const currencySymbol = position?.market === "UK" ? "£" : "$";

  const { data: trailData, isLoading, isError } = useQuery({
    queryKey: ["stopTrail", position?.id],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/positions/${position.id}/stop-trail`);
      if (!res.ok) throw new Error("Trail calculation failed");
      const json = await res.json();
      return json.data || json;
    },
    enabled: !!position?.id && isEligible && hasStop,
  });

  const updateStopMutation = useMutation({
    mutationFn: ({ id, stop_price }) =>
      apiFetch(`${API_BASE}/positions/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stop_price }),
      }).then((r) => r.json()),
    onSuccess: (_, vars) => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      toast.success(`Stop updated to ${currencySymbol}${vars.stop_price?.toFixed(2)}`);
      onClose();
    },
    onError: () => {
      toast.error("Failed to update stop. Please try again.");
    },
  });

  const atrTrailStop = trailData?.atr_trail_stop;
  const trailDiff = trailData?.trail_difference;
  const trailR = trailData?.trail_r_terms;
  const isNegativeDiff = trailDiff != null && trailDiff < 0;
  const confirmLabel = atrTrailStop != null
    ? (isNegativeDiff ? `Lower stop to ${currencySymbol}${Number(atrTrailStop).toFixed(2)}` : `Update stop to ${currencySymbol}${Number(atrTrailStop).toFixed(2)}`)
    : "Update stop";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" role="dialog" aria-modal="true">
      <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-700 p-6 space-y-4 mx-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-white">Trail Stop — {position?.ticker}</h2>
            <p className="text-xs text-slate-600 dark:text-slate-400">ATR-based stop trail calculation</p>
          </div>
          <button onClick={onClose} className="text-slate-600 dark:text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
        </div>

        {isLoading && (
          <div className="space-y-3 animate-pulse">
            <div className="h-5 bg-slate-700 rounded w-3/4" />
            <div className="h-5 bg-slate-700 rounded w-2/3" />
            <div className="h-5 bg-slate-700 rounded w-1/2" />
          </div>
        )}

        {isError && (
          <div className="text-sm text-rose-400">Unable to load trail calculation. Please try again.</div>
        )}

        {!isLoading && !isError && trailData && (
          <dl className="space-y-2 text-sm">
            <div className="flex justify-between">
              <dt className="text-slate-600 dark:text-slate-400">Current Stop</dt>
              <dd className="text-white font-medium">{currencySymbol}{Number(trailData.current_stop ?? stopValue ?? 0).toFixed(2)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-600 dark:text-slate-400">ATR Trail Stop</dt>
              <dd className="text-white font-medium">{currencySymbol}{Number(atrTrailStop).toFixed(2)}</dd>
            </div>
            {trailDiff != null && (
              <div className="flex justify-between">
                <dt className="text-slate-600 dark:text-slate-400">Trail Difference</dt>
                <dd className={cn("font-medium", isNegativeDiff ? "text-amber-400" : "text-emerald-400")}>
                  {trailDiff >= 0 ? "+" : "−"}{currencySymbol}{Math.abs(trailDiff).toFixed(2)}
                  {trailR != null && <span className="text-slate-600 dark:text-slate-400 ml-1">({trailR >= 0 ? "+" : ""}{Number(trailR).toFixed(1)}R)</span>}
                </dd>
              </div>
            )}
          </dl>
        )}

        {!isLoading && !isError && trailData && (
          <p className="text-xs text-slate-600 dark:text-slate-400">
            ATR trail stop = current price − (ATR × 2.0). ATR period: 14 days. Multiplier per strategy rules.
          </p>
        )}

        <div className="flex flex-col gap-2 pt-2">
          <Button
            disabled={!trailData || isLoading || updateStopMutation.isPending || !atrTrailStop}
            onClick={() => updateStopMutation.mutate({ id: position.id, stop_price: atrTrailStop })}
            className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 w-full"
          >
            {updateStopMutation.isPending ? "Updating…" : confirmLabel}
          </Button>
          {!updateStopMutation.isPending && (
            <button onClick={onClose} className="text-slate-600 dark:text-slate-400 hover:text-slate-200 text-sm text-center">
              Cancel
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

const LIFECYCLE_BADGE_COLOURS = {
  GRACE: "bg-blue-600",
  PROFITABLE: "bg-green-700",
  LOSING: "bg-red-600",
  "EXIT ZONE": "bg-violet-600",
  UNKNOWN: "bg-gray-500",
};

function DrawdownReviewPrompt() {
  const [dismissed, setDismissed] = useState(false);
  const { data } = useQuery({
    queryKey: ["drawdown-status"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/portfolio/drawdown-status`);
      const json = await res.json();
      return json?.data || {};
    },
    staleTime: 2 * 60 * 1000,
  });

  if (dismissed || !data?.threshold_breached) return null;

  const stateColours = {
    GRACE: "bg-blue-600",
    PROFITABLE: "bg-green-700",
    LOSING: "bg-red-600",
    "EXIT ZONE": "bg-violet-600",
    UNKNOWN: "bg-gray-500",
  };

  const statesByCount = Object.entries(data.positions_by_state || {}).filter(([, count]) => count > 0);

  return (
    <div className="rounded-lg bg-amber-50 border border-amber-300 p-4" role="alert">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-700 flex-shrink-0" aria-hidden="true" />
          <span className="font-semibold text-amber-900">Portfolio Drawdown Review</span>
        </div>
        <button
          onClick={() => setDismissed(true)}
          aria-label="Dismiss drawdown review prompt"
          className="text-amber-700 hover:text-amber-900 transition-colors flex-shrink-0"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
      <div className="mt-3 grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Current Drawdown", value: `${data.current_drawdown_pct?.toFixed(1) ?? "—"}%`, amber: true },
          { label: "Threshold", value: `${data.threshold_pct?.toFixed(1) ?? "—"}%` },
          { label: "Portfolio Heat", value: data.portfolio_heat_pct != null ? `${data.portfolio_heat_pct.toFixed(1)}%` : "—" },
          { label: "Regime", value: data.regime_status || "—" },
        ].map(({ label, value, amber }) => (
          <div key={label} className="bg-amber-100/60 rounded p-2">
            <p className="text-amber-700 text-xs font-medium">{label}</p>
            <p className={`text-sm font-bold mt-0.5 ${amber ? "text-amber-700" : "text-amber-900"}`}>{value}</p>
          </div>
        ))}
      </div>
      {statesByCount.length > 0 && (
        <div className="mt-3 flex flex-wrap items-center gap-2">
          <span className="text-xs text-amber-700 font-medium">Positions by state:</span>
          {statesByCount.map(([state, count]) => (
            <span
              key={state}
              className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs text-white font-medium ${stateColours[state] || "bg-gray-500"}`}
            >
              {state} <span className="opacity-80">{count}</span>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function ConcentrationLimitsWarning() {
  const { data } = useQuery({
    queryKey: ["concentration-status"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/portfolio/concentration-status`);
      const json = await res.json();
      return json?.data || {};
    },
    staleTime: 2 * 60 * 1000,
  });

  if (!data?.any_breach) return null;

  const { breaching_positions = [], breaching_sectors = [] } = data;

  return (
    <div className="rounded-lg bg-amber-50 border border-amber-300 p-4" role="alert">
      <div className="flex items-center gap-2">
        <AlertTriangle className="w-5 h-5 text-amber-700 flex-shrink-0" aria-hidden="true" />
        <span className="font-semibold text-amber-900">Concentration Limits</span>
      </div>
      {breaching_positions.length > 0 && (
        <div className="mt-3">
          <p className="text-xs text-amber-700 font-medium mb-1.5">
            Positions exceeding limit ({data.position_threshold_pct}% of portfolio heat):
          </p>
          <ul className="space-y-1">
            {breaching_positions.map((p) => (
              <li key={p.ticker} className="text-sm text-amber-900">
                <span className="font-semibold">{p.ticker}</span>
                {" — "}{p.heat_pct.toFixed(1)}% of heat{" "}
                <span className="text-amber-700 text-xs">(limit: {p.limit_pct}%)</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {breaching_sectors.length > 0 && (
        <div className="mt-3">
          <p className="text-xs text-amber-700 font-medium mb-1.5">
            Sectors exceeding limit ({data.sector_threshold_pct}% concentration):
          </p>
          <ul className="space-y-1">
            {breaching_sectors.map((s) => (
              <li key={s.sector} className="text-sm text-amber-900">
                <span className="font-semibold">{s.sector}</span>
                {" — "}{s.concentration_pct.toFixed(1)}%{" "}
                <span className="text-amber-700 text-xs">(limit: {s.limit_pct}%)</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      <Link
        to={createPageUrl("Settings")}
        className="mt-3 inline-block text-xs text-amber-700 underline hover:text-amber-900"
        aria-label="Review portfolio concentration limit settings"
      >
        Review Settings
      </Link>
    </div>
  );
}

function PositionEarningsCell({ ticker, market }) {
  const { data, loading } = useEarnings(ticker, market);
  if (loading) return <TableCell><span className="text-slate-600 text-xs">…</span></TableCell>;
  if (!data || data.days_until_earnings == null) return <TableCell><span className="text-slate-600 text-xs">—</span></TableCell>;
  const days = data.days_until_earnings;
  if (days < 0) return <TableCell><span className="text-slate-600 text-xs">—</span></TableCell>;
  if (days === 0) return (
    <TableCell>
      <span className="text-xs font-medium px-2 py-0.5 rounded bg-amber-500/15 text-amber-400 border border-amber-500/25" title={data.next_earnings_date}>
        Today
      </span>
    </TableCell>
  );
  const isNear = days <= 5;
  return (
    <TableCell>
      <span
        className={`text-xs font-medium px-2 py-0.5 rounded ${isNear ? "bg-amber-500/15 text-amber-400 border border-amber-500/25" : "text-slate-600 dark:text-slate-400"}`}
        title={data.next_earnings_date}
      >
        {isNear ? `⚠ ${days}d` : `${days}d`}
      </span>
    </TableCell>
  );
}

// ---------------------------------------------------------------------------
// ST-02 (v6.9, BLG-FEAT-65) — Gap Risk badge, stacked in the Alerts column
// ---------------------------------------------------------------------------

const GAP_RISK_REASON_LABELS = {
  earnings: "Earnings before next session",
  weekend_hold: "Weekend hold (flagged at Friday close)",
};

function GapRiskBadge({ ticker, gapRisk }) {
  const reasonText = (gapRisk.reasons || [])
    .map((r) => GAP_RISK_REASON_LABELS[r] || r)
    .join(" + ");
  const statText = gapRisk.insufficient_history
    ? "insufficient history"
    : `±${gapRisk.avg_gap_pct}% avg (${gapRisk.event_count} events)`;
  const tooltipText = `Gap Risk — ${ticker}\n${reasonText}\nAvg gap: ${statText}`;
  const descId = `gap-risk-desc-${ticker}`;

  return (
    <span
      tabIndex={0}
      title={tooltipText}
      aria-describedby={descId}
      aria-label={`Gap risk flag: ${reasonText}, average gap ${statText}`}
      className="inline-flex items-center w-fit text-xs px-2 py-0.5 rounded-full font-medium text-white"
      style={{ backgroundColor: "#D97706" }}
      data-testid="gap-risk-badge"
    >
      GAP RISK
      <span id={descId} className="sr-only">{tooltipText}</span>
    </span>
  );
}

function AlertsCell({ position }) {
  const { data: gapRisk, loading: gapRiskLoading } = useGapRisk(position.id);
  const riskOffExit = position.risk_off_exit === true;

  // ST-03 (v7.1, BLG-FE-107): spec compliance fix — Table View had drifted to
  // an amber treatment since v6.2 (encoded as expected by the then-passing
  // SC-RO-02); positions.md §Alerts Column always specified blue-800
  // #1E40AF / "RISK OFF", which the v7.0 Grid View badge (PositionCard.js)
  // already correctly uses. Bringing Table View into compliance here
  // restores the hue-separation rationale (RISK OFF blue vs GAP RISK amber)
  // the v7.0 combined-badge differentiation decision record assumed for
  // both views. The unspecified ShieldAlert icon is dropped per the design
  // gate resolution (docs/design/2026-07-14__release-v7.1/table-view-badge-compliance/decision_record.md).
  const riskOffBadge = riskOffExit ? (
    <span
      className="inline-flex items-center w-fit text-xs px-2 py-0.5 rounded-full font-medium text-white"
      style={{ backgroundColor: "#1E40AF" }}
      title="Risk-off regime: index below MA200 — consider exit"
      aria-label="Risk-off exit alert: regime signal indicates exit this position"
      data-testid="risk-off-badge"
    >
      RISK OFF
    </span>
  ) : null;

  const gapBadge = gapRiskLoading ? (
    <span className="inline-block h-4 w-20 rounded bg-slate-700/50 animate-pulse" data-testid="gap-risk-skeleton" />
  ) : gapRisk?.flagged ? (
    <GapRiskBadge ticker={position.ticker} gapRisk={gapRisk} />
  ) : null;

  if (!riskOffBadge && !gapBadge) {
    return <span className="text-slate-600 text-xs">—</span>;
  }

  return (
    <div className="flex flex-col gap-1 items-start">
      {riskOffBadge}
      {gapBadge}
    </div>
  );
}

// ---------------------------------------------------------------------------
// ST-15 (v7.0, BLG-FEAT-68) — Position review cadence nudge
// ---------------------------------------------------------------------------

const REVIEW_STALE_THRESHOLD_DAYS = 14;
const GRACE_SUPPRESSION_DAYS_IN_STATE = 8;

// AC-04: suppress the flagged/amber state when the position is already
// surfaced by the Grace Period Alert Zone or the portfolio-level Drawdown
// Review Prompt. The drawdown prompt has no per-position breakdown (only
// aggregate positions_by_state counts) — while it is active, treat every
// open position as already surfaced by it, per the design intent that this
// is a portfolio-wide review nudge (ux_spec.md §5 rationale: "both existing
// prompts already ask the user to review... for the same position" reads as
// position-scoped for Grace, portfolio-scoped for Drawdown).
function getReviewCadenceState(position, drawdownActive) {
  const lastReviewedAt = position.last_reviewed_at;
  const referenceDate = lastReviewedAt ? new Date(lastReviewedAt) : new Date(position.entry_date);
  const daysSinceReview = differenceInDays(new Date(), referenceDate);

  const state = position.lifecycle_state || position.position_state;
  const isGraceSuppressed = state === "GRACE" && (position.days_in_state ?? 0) >= GRACE_SUPPRESSION_DAYS_IN_STATE;
  const suppressed = isGraceSuppressed || drawdownActive;

  const flagged = !suppressed && daysSinceReview >= REVIEW_STALE_THRESHOLD_DAYS;
  const label = lastReviewedAt ? `Reviewed ${daysSinceReview}d ago` : "Not yet reviewed";
  const ariaLabel = flagged
    ? `Position not reviewed in ${daysSinceReview} days — consider reviewing`
    : `Last reviewed ${daysSinceReview} days ago`;

  return { label, flagged, ariaLabel, daysSinceReview };
}

function useMarkReviewedMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (positionId) =>
      apiFetch(`${API_BASE}/positions/${positionId}/mark-reviewed`, { method: "PATCH" }).then((r) => r.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
    },
    onError: () => {
      toast.error("Failed to mark position as reviewed. Please try again.");
    },
  });
}

function LastReviewedCell({ position, drawdownActive }) {
  const { label, flagged, ariaLabel } = getReviewCadenceState(position, drawdownActive);
  const markReviewed = useMarkReviewedMutation();

  return (
    <TableCell>
      <div className="flex items-center gap-1.5" data-testid="last-reviewed-cell">
        {flagged && <Clock className="w-3 h-3 text-amber-600 dark:text-amber-400 flex-shrink-0" aria-hidden="true" />}
        <span
          className={cn("text-xs", flagged ? "text-amber-600 dark:text-amber-400" : "text-slate-600 dark:text-slate-400")}
          aria-label={ariaLabel}
        >
          {label}
        </span>
        <button
          onClick={() => markReviewed.mutate(position.id)}
          disabled={markReviewed.isPending}
          title="Mark Reviewed"
          aria-label={`Mark ${position.ticker} as reviewed`}
          data-testid="mark-reviewed-button"
          className="text-slate-600 hover:text-emerald-400 disabled:opacity-40 flex-shrink-0"
        >
          <Check className="w-3.5 h-3.5" />
        </button>
      </div>
    </TableCell>
  );
}

export default function Positions() {
  const [viewMode, setViewMode] = useState("grid");
  const [editingPosition, setEditingPosition] = useState(null);
  const [exitingPosition, setExitingPosition] = useState(null);
  const [reflectionTrade, setReflectionTrade] = useState(null);
  const [trailStopPosition, setTrailStopPosition] = useState(null);
  const [recheckingPosition, setRecheckingPosition] = useState(null);

  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // ST-15 (v7.0, BLG-FEAT-68): shares the queryKey with DrawdownReviewPrompt's
  // own useQuery — react-query dedupes identical keys, no extra network cost.
  const { data: drawdownStatus } = useQuery({
    queryKey: ["drawdown-status"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/portfolio/drawdown-status`);
      const json = await res.json();
      return json?.data || {};
    },
    staleTime: 2 * 60 * 1000,
  });
  const drawdownActive = drawdownStatus?.threshold_breached === true;

  const { data: positions, isLoading, isError, refetch } = useQuery({
    queryKey: ["positions"],
    queryFn: async () => {
      const result = await base44.entities.Position.list("-entry_date");
      console.log("Positions query result:", result);
      return result;
    },
  });

  const { data: availableTags = [] } = useQuery({
    queryKey: ["position-tags"],
    queryFn: async () => {
      const positionsList = await base44.entities.Position.list();
      const allTags = positionsList.flatMap((p) => p.tags || []);
      return [...new Set(allTags)].sort();
    },
  });

  // FIXED: Exit mutation now accepts exitData directly from ExitModal
  const exitMutation = useMutation({
    mutationFn: (exitData) => {
      // exitData contains:
      // { position_id, shares, exit_price, exit_date, exit_reason, fx_rate }
      console.log("Exit mutation received:", exitData);

      // Pass the entire exitData object - base44Client handles it
      return base44.entities.Position.exit(exitData);
    },
    onSuccess: async (data) => {
      console.log("Exit successful:", data);

      // Aggressive cache invalidation
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
      queryClient.invalidateQueries({ queryKey: ["trades"] });

      // Optional refetch
      queryClient.refetchQueries({ queryKey: ["positions", "open"] });
      queryClient.refetchQueries({ queryKey: ["portfolio"] });

      setExitingPosition(null);

      // Trigger reflection modal: fetch the most recent trade to get trade ID and backend data
      try {
        const tradesResult = await api.trades.list();
        const trades = tradesResult?.trades || [];
        if (trades.length > 0) {
          setReflectionTrade(trades[0]);
        }
      } catch (e) {
        // Non-critical — skip reflection modal if trade fetch fails
      }
    },
    onError: (error) => {
      console.error("Exit failed:", error);
      alert(`Failed to exit position: ${friendlyErrorMessage(error)}`);
    },
  });

  // ✅ FIXED: Updated handleSave to only update notes and tags
  const handleSave = async (position) => {
    try {
      await base44.entities.Position.updateNote(
        position.id,
        position.entry_note || ""
      );

      await base44.entities.Position.updateTags(position.id, position.tags || []);

      queryClient.invalidateQueries({ queryKey: ["positions"] });
      setEditingPosition(null);
    } catch (error) {
      console.error("Failed to save position:", error);
      alert(`Failed to save changes: ${friendlyErrorMessage(error)}`);
    }
  };

  // FIXED: handleExit passes exitData through to mutation
  const handleExit = (exitData) => {
    console.log("handleExit called with:", exitData);

    if (!exitData.position_id) {
      alert("Invalid position data");
      return;
    }

    if (!exitData.shares || exitData.shares <= 0) {
      alert("Invalid number of shares");
      return;
    }

    if (!exitData.exit_price || exitData.exit_price <= 0) {
      alert("Invalid exit price");
      return;
    }

    exitMutation.mutate(exitData);
  };

  const allPositions = positions || [];
  const openPositions = allPositions.filter((p) => p.status === "open");

  return (
    <div className="space-y-6">
      <PageHeader
        title={viewMode === "journal" ? "Trade Journal" : "Open Positions"}
        description={
          viewMode === "journal"
            ? `${allPositions.length} total entries`
            : `${openPositions.length} active position${
                openPositions.length !== 1 ? "s" : ""
              }`
        }
        actions={
          <div className="flex items-center gap-3">
            <div className="flex items-center rounded-xl bg-slate-800/50 border border-slate-700/50 p-1">
              <Button
                aria-label="Grid view"
                variant="ghost"
                size="sm"
                onClick={() => setViewMode("grid")}
                className={cn(
                  "h-8 w-8 p-0 rounded-lg",
                  viewMode === "grid"
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400"
                    : "text-slate-600 dark:text-slate-400 hover:text-white"
                )}
              >
                <LayoutGrid className="w-4 h-4" />
              </Button>

              <Button
                aria-label="Table view"
                variant="ghost"
                size="sm"
                onClick={() => setViewMode("table")}
                className={cn(
                  "h-8 w-8 p-0 rounded-lg",
                  viewMode === "table"
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400"
                    : "text-slate-600 dark:text-slate-400 hover:text-white"
                )}
              >
                <List className="w-4 h-4" />
              </Button>

              <Button
                aria-label="Journal view"
                variant="ghost"
                size="sm"
                onClick={() => setViewMode("journal")}
                className={cn(
                  "h-8 w-8 p-0 rounded-lg",
                  viewMode === "journal"
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400"
                    : "text-slate-600 dark:text-slate-400 hover:text-white"
                )}
              >
                <BookOpen className="w-4 h-4" />
              </Button>
            </div>

            <Link to={createPageUrl("TradeEntry")}>
              <Button className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25">
                <Plus className="w-4 h-4 mr-2" />
                New Position
              </Button>
            </Link>
          </div>
        }
      />

      {/* ST-02 (BLG-FEAT-09): Metrics staleness indicator — below title, inline with view controls */}
      <MetricsStalenessIndicator />

      {/* IT-04 (Arc 3): Drawdown review prompt — portfolio-level, highest severity */}
      <DrawdownReviewPrompt />

      {/* IT-05 (Arc 3): Concentration limits warning — portfolio-level, structural */}
      <ConcentrationLimitsWarning />

      {/* ST-02 (IT-02): Grace period alert zone — display-only, §13 compliant */}
      <GracePeriodAlertZone />

      {/* ST-12 (BLG-FE-02): DataState standardised loading/empty/error — Table/Grid views */}
      <DataState
        loading={isLoading}
        error={isError}
        onRetry={refetch}
        className="min-h-[300px]"
        empty={!isLoading && !isError && viewMode !== "journal" && openPositions.length === 0}
        emptyIcon={<FolderOpen className="w-10 h-10 text-slate-600" />}
        emptyHeading="No open positions"
        emptyBody="Enter a trade to see your positions here."
        emptyAction={
          <Link to={createPageUrl("TradeEntry")}>
            <Button className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0">
              <Plus className="w-4 h-4 mr-2" />
              Enter First Position
            </Button>
          </Link>
        }
      >
        {viewMode === "journal" ? (
          <JournalView positions={allPositions} availableTags={availableTags} />
        ) : viewMode === "grid" ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {openPositions.map((position) => (
            <PositionCard
              key={position.id}
              position={position}
              onEdit={setEditingPosition}
              onExit={setExitingPosition}
              onRecheck={setRecheckingPosition}
              drawdownActive={drawdownActive}
            />
          ))}
        </div>
      ) : (
        <DataTable>
          <TableHeader>
            <TableHead>Ticker</TableHead>
            <TableHead>Entry Price</TableHead>
            <TableHead>Current Price</TableHead>
            <TableHead title="Initial stop (entry) / Current trailing stop (computed)">
              <span className="inline-flex items-center gap-1">
                Stop
                <TrailingStopExplainerIcon />
              </span>
            </TableHead>
            <TableHead>Shares</TableHead>
            <TableHead className="text-right">P&amp;L (GBP)</TableHead>
            <TableHead className="text-right">P&amp;L %</TableHead>
            <TableHead>Days</TableHead>
            {/* ST-01 (IT-01): Lifecycle state badge column */}
            <TableHead title="Position lifecycle state">State</TableHead>
            <TableHead>Grace</TableHead>
            <TableHead title="Days until next earnings">Earnings</TableHead>
            {/* ST-05 (v6.2) / ST-02 (v6.9): Alerts column — Risk-Off + Gap Risk badges, stacked */}
            <TableHead>Alerts</TableHead>
            {/* ST-15 (v7.0, BLG-FEAT-68): Last Reviewed — position review cadence nudge */}
            <TableHead>Last Reviewed</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>

          <TableBody>
            {openPositions.map((position) => {
              // P&L is already calculated in GBP by backend
              const pnl = position.pnl || 0;
              const pnlPercent = position.pnl_percent || 0;
              const isProfit = pnl >= 0;
              const daysHeld = differenceInDays(
                new Date(),
                new Date(position.entry_date)
              );

              const currencySymbol = position.market === "UK" ? "£" : "$";

              // Use native prices for display
              const displayCurrentPrice =
                position.current_price_native || position.current_price;
              const displayStopPrice =
                position.stop_price_native || position.stop_price;

              // ST-01 (BLG-FEAT-46): trailing stop breach detection
              const trailStop = position.current_trailing_stop;
              const currentPriceGbp = position.current_price;
              const trailBreached =
                trailStop > 0 && currentPriceGbp > 0 && currentPriceGbp <= trailStop;

              return (
                <TableRow key={position.id}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-white">
                        {position.ticker}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-700">
                        {position.market}
                      </span>
                    </div>
                  </TableCell>

                  <TableCell className="text-slate-300">
                    {currencySymbol}
                    {position.entry_price.toFixed(2)}
                  </TableCell>

                  <TableCell className="text-slate-300">
                    {currencySymbol}
                    {displayCurrentPrice?.toFixed(2) || "—"}
                  </TableCell>

                  {/* ST-01 (BLG-FEAT-46): two-line stop cell — initial stop / trailing stop + breach badge */}
                  <TableCell className="text-rose-400 font-medium">
                    <div className="flex flex-col gap-0.5 leading-tight">
                      <span className="text-xs text-slate-600 dark:text-slate-400">
                        Init: {position.initial_stop != null ? `${currencySymbol}${Number(position.initial_stop).toFixed(2)}` : "—"}
                      </span>
                      <div className="flex items-center gap-1.5">
                        <span>
                          {trailStop > 0 ? `${currencySymbol}${trailStop.toFixed(2)}` : (displayStopPrice != null ? `${currencySymbol}${Number(displayStopPrice).toFixed(2)}` : "—")}
                        </span>
                        {/* ST-09 (v7.0, BLG-FE-96): breach badge — visible when price <= trailing stop, spec colour/label */}
                        {trailBreached && (
                          <span
                            className="inline-flex items-center gap-0.5 text-xs px-1.5 py-0.5 rounded-full bg-orange-600 text-white font-medium"
                            title="Trailing stop breach: current price is at or below trailing stop level"
                            aria-label="Trailing stop breach: current price is at or below trailing stop level"
                            data-testid="breach-badge"
                          >
                            ⚠ BREACH
                          </span>
                        )}
                      </div>
                    </div>
                  </TableCell>

                  <TableCell className="text-slate-300">
                    {position.shares}
                  </TableCell>

                  <TableCell className="text-right">
                    <div
                      className={cn(
                        "inline-flex items-center gap-1.5 font-medium",
                        isProfit ? "text-emerald-400" : "text-rose-400"
                      )}
                    >
                      {isProfit ? (
                        <TrendingUp className="w-4 h-4" />
                      ) : (
                        <TrendingDown className="w-4 h-4" />
                      )}
                      £{Math.abs(pnl).toFixed(2)}
                    </div>
                  </TableCell>

                  <TableCell className="text-right">
                    <span
                      className={cn(
                        "text-sm font-medium",
                        isProfit ? "text-emerald-400" : "text-rose-400"
                      )}
                    >
                      {isProfit ? "+" : ""}{pnlPercent.toFixed(1)}%
                    </span>
                  </TableCell>

                  <TableCell className="text-slate-600 dark:text-slate-400">{daysHeld}</TableCell>

                  {/* ST-01 (IT-01): Lifecycle state badge */}
                  <TableCell>
                    {(position.lifecycle_state || position.position_state) ? (
                      <LifecycleBadge
                        state={position.lifecycle_state || position.position_state}
                        daysInState={position.days_in_state}
                      />
                    ) : (
                      <span className="text-slate-600 text-xs">—</span>
                    )}
                  </TableCell>

                  {/* BLG-FEAT-06: Grace Days Remaining */}
                  <TableCell>
                    {position.grace_days_remaining !== null &&
                    position.grace_days_remaining !== undefined ? (
                      <span className="text-xs font-medium px-2 py-1 rounded-lg bg-amber-500/15 text-amber-400 border border-amber-500/25 whitespace-nowrap">
                        Day {(position.holding_days ?? 0) + 1} of 10
                      </span>
                    ) : (
                      <span className="text-slate-600">—</span>
                    )}
                  </TableCell>

                  <PositionEarningsCell ticker={position.ticker} market={position.market} />

                  <TableCell>
                    <AlertsCell position={position} />
                  </TableCell>

                  <LastReviewedCell position={position} drawdownActive={drawdownActive} />

                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
                        onClick={() => setEditingPosition(position)}
                      >
                        <Edit2 className="w-4 h-4" />
                      </Button>

                      <Button
                        variant="ghost"
                        size="icon"
                        title="Trade Plan"
                        className="h-8 w-8 text-cyan-500/70 hover:text-cyan-400 hover:bg-cyan-500/10"
                        onClick={() => navigate(`/TradePlan?position_id=${position.id}&ticker=${position.ticker}&market=${position.market}`)}
                      >
                        <BookOpen className="w-4 h-4" />
                      </Button>

                      {/* ST-03 (IT-03): Trail Stop — shown for PROFITABLE/EXIT ZONE; disabled when no stop */}
                      {(position.lifecycle_state === "PROFITABLE" || position.lifecycle_state === "EXIT ZONE" ||
                        position.position_state === "PROFITABLE" || position.position_state === "EXIT ZONE") && (
                        <Button
                          variant="ghost"
                          size="icon"
                          title={(!position.current_stop && !position.stop_price) ? "No current stop set. Add a stop to use trail management." : "Trail Stop"}
                          disabled={!position.current_stop && !position.stop_price}
                          className="h-8 w-8 text-violet-400 hover:text-violet-300 hover:bg-violet-500/10 disabled:opacity-40"
                          onClick={() => setTrailStopPosition(position)}
                        >
                          <ArrowUpDown className="w-4 h-4" />
                        </Button>
                      )}

                      {/* ST-01 (v6.9, BLG-FEAT-64): Recheck Compliance — on-demand SI-01 recheck */}
                      <Button
                        variant="ghost"
                        size="icon"
                        title="Recheck Compliance"
                        aria-label={`Recheck compliance for ${position.ticker}`}
                        data-testid="recheck-compliance-button"
                        className="h-8 w-8 text-amber-400/80 hover:text-amber-300 hover:bg-amber-500/10"
                        onClick={() => setRecheckingPosition(position)}
                      >
                        <Zap className="w-4 h-4" />
                      </Button>

                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 text-rose-400 hover:text-rose-300 hover:bg-rose-500/10"
                        onClick={() => setExitingPosition(position)}
                      >
                        <LogOut className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </DataTable>
      )}
      </DataState>

      {/* ST-01 (BLG-FEAT-11): Strategy Compliance Panel — Table View only; display-only §13.3 */}
      {viewMode === "table" && openPositions.length > 0 && (
        <StrategyCompliancePanel />
      )}

      {/* ST-03 (IT-06): Paper Account Panel — Table View only; §13 display-only */}
      {viewMode === "table" && <PaperAccountPanel />}

      <PositionModal
        position={editingPosition}
        open={!!editingPosition}
        onClose={() => setEditingPosition(null)}
        onSave={handleSave}
      />

      <ExitModal
        position={exitingPosition}
        open={!!exitingPosition}
        onClose={() => setExitingPosition(null)}
        onConfirm={handleExit}
      />

      <TradeReflectionModal
        trade={reflectionTrade}
        open={!!reflectionTrade}
        onClose={() => setReflectionTrade(null)}
      />

      {/* ST-03 (IT-03): Trail Stop modal */}
      {trailStopPosition && (
        <TrailStopModal
          position={trailStopPosition}
          onClose={() => setTrailStopPosition(null)}
        />
      )}

      {/* ST-01 (v6.9, BLG-FEAT-64): Compliance Recheck modal */}
      <ComplianceRecheckModal
        position={recheckingPosition}
        open={!!recheckingPosition}
        onClose={() => setRecheckingPosition(null)}
      />

      {/* ST-09 (EPIC-02, v6.2): AI Trade Advisor — fixed floating widget, display-only advisory */}
      <AiChatWidget />
    </div>
  );
}
