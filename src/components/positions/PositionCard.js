import { useState } from "react";
import { motion } from "framer-motion";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { TrendingUp, TrendingDown, Edit2, LogOut, Zap, AlertTriangle, Clock, Check } from "lucide-react";
import { Button } from "../ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import { cn } from "../../lib/utils";
import { differenceInDays } from "date-fns";
import { useGapRisk } from "../../hooks/useGapRisk";
import { apiFetch } from "../../api/base44Client";
import { toast } from "sonner";
import TrailingStopExplainerIcon from "./TrailingStopExplainerIcon";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const GAP_RISK_REASON_LABELS = {
  earnings: "Earnings before next session",
  weekend_hold: "Weekend hold (flagged at Friday close)",
};

// ST-02 (v6.9, BLG-FEAT-65) — Gap Risk badge
function GapRiskCardBadge({ gapRisk, ticker, positionId }) {
  const reasonText = (gapRisk.reasons || []).map((r) => GAP_RISK_REASON_LABELS[r] || r).join(" + ");
  const statText = gapRisk.insufficient_history
    ? "insufficient history"
    : `±${gapRisk.avg_gap_pct}% avg (${gapRisk.event_count} events)`;
  const tooltipText = `Gap Risk — ${ticker}\n${reasonText}\nAvg gap: ${statText}`;
  const descId = `gap-risk-card-desc-${positionId}`;

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

// ST-02 (v7.0, BLG-FE-102) — RISK OFF badge, Grid View parity with Table View
function RiskOffCardBadge() {
  return (
    <span
      className="inline-flex items-center w-fit text-xs px-2 py-0.5 rounded-full font-medium text-white"
      style={{ backgroundColor: "#1E40AF" }}
      title="Risk-off regime: index below MA200 — consider exit"
      aria-label="Risk-off exit alert: regime signal indicates exit this position"
      data-testid="risk-off-badge"
    >
      RISK OFF
    </span>
  );
}

// ST-01/ST-02/ST-05 (v7.0) — dedicated alert row: below header, above stat tiles.
// Stacks RISK OFF above GAP RISK per positions.md §Alerts Column "Stacked-state spacing"
// (4px min gap, RISK OFF above GAP RISK) — same rule Table View's AlertsCell already applies.
function PositionCardAlertsRow({ position }) {
  const { data: gapRisk, loading: gapRiskLoading } = useGapRisk(position.id);
  const riskOffExit = position.risk_off_exit === true;
  const showGap = !gapRiskLoading && gapRisk?.flagged;

  if (!riskOffExit && !showGap) return null;

  return (
    <div className="flex flex-col gap-1 mb-3" data-testid="grid-alerts-row">
      {riskOffExit && <RiskOffCardBadge />}
      {showGap && <GapRiskCardBadge gapRisk={gapRisk} ticker={position.ticker} positionId={position.id} />}
    </div>
  );
}

// ST-15 (v7.0, BLG-FEAT-68) — Position review cadence nudge.
// Same computation/suppression rule as Positions.js's Table View — duplicated
// per this codebase's existing card-vs-page convention (e.g. GAP_RISK_REASON_LABELS
// above), not factored into a shared module.
const REVIEW_STALE_THRESHOLD_DAYS = 14;
const GRACE_SUPPRESSION_DAYS_IN_STATE = 8;

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

  return { label, flagged, ariaLabel };
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

function LastReviewedRow({ position, drawdownActive }) {
  const { label, flagged, ariaLabel } = getReviewCadenceState(position, drawdownActive);
  const markReviewed = useMarkReviewedMutation();

  return (
    <div className="flex items-center justify-between gap-2 pb-3 mb-1" data-testid="last-reviewed-row">
      <div className="flex items-center gap-1.5">
        {flagged && <Clock className="w-3 h-3 text-amber-600 dark:text-amber-400 flex-shrink-0" aria-hidden="true" />}
        <span
          className={cn("text-xs", flagged ? "text-amber-600 dark:text-amber-400" : "text-slate-600 dark:text-slate-400")}
          aria-label={ariaLabel}
        >
          {label}
        </span>
      </div>
      <button
        onClick={() => markReviewed.mutate(position.id)}
        disabled={markReviewed.isPending}
        title="Mark Reviewed"
        aria-label={`Mark ${position.ticker} as reviewed`}
        data-testid="mark-reviewed-button"
        className="text-slate-600 hover:text-emerald-400 disabled:opacity-40"
      >
        <Check className="w-3.5 h-3.5" />
      </button>
    </div>
  );
}

export default function PositionCard({ position, onEdit, onExit, onRecheck, drawdownActive }) {
  const [showNoteModal, setShowNoteModal] = useState(false);
  const pnl = position.pnl || 0;
  const pnlPercent = position.pnl_percent || 0;
  const isProfit = pnl >= 0;
  const daysHeld = differenceInDays(new Date(), new Date(position.entry_date));
  const currencySymbol = position.market === "UK" ? "£" : "$";

  // Use native prices for display
  const displayCurrentPrice = position.current_price_native || position.current_price;

  // ST-03 (BLG-FE-97): trailing stop value + breach indicator — same condition logic as Table View
  const trailStop = position.current_trailing_stop;
  const currentPriceGbp = position.current_price;
  const trailBreached = trailStop > 0 && currentPriceGbp > 0 && currentPriceGbp <= trailStop;
  const displayTrailStop = trailStop > 0 ? trailStop : (position.stop_price_native || position.stop_price);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "relative overflow-hidden rounded-2xl border p-5 transition-all",
        "bg-gradient-to-br from-slate-900 to-slate-800 backdrop-blur-sm",
        "border-slate-700/50 hover:border-slate-600/50"
      )}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-lg font-bold text-white">{position.ticker}</h3>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-700">
              {position.market}
            </span>
          </div>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            {daysHeld} days held • {position.shares} shares
          </p>
        </div>
        <div className={cn(
          "flex items-center gap-1.5 px-3 py-1.5 rounded-xl",
          isProfit ? "bg-emerald-500/20" : "bg-rose-500/20"
        )}>
          {isProfit ? (
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          ) : (
            <TrendingDown className="w-4 h-4 text-rose-400" />
          )}
          <span className={cn(
            "text-sm font-semibold",
            isProfit ? "text-emerald-400" : "text-rose-400"
          )}>
            {isProfit ? "+" : ""}{pnlPercent.toFixed(2)}%
          </span>
        </div>
      </div>

      {/* ST-01/ST-02/ST-05 (v7.0): dedicated alert row — RISK OFF stacked above GAP RISK when both apply */}
      <PositionCardAlertsRow position={position} />

      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="p-3 rounded-xl bg-slate-800/50">
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Entry</p>
          <p className="text-sm font-semibold text-white">
            {currencySymbol}{position.entry_price.toFixed(2)}
          </p>
        </div>
        <div className="p-3 rounded-xl bg-slate-800/50">
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Current</p>
          <p className="text-sm font-semibold text-white">
            {currencySymbol}{displayCurrentPrice?.toFixed(2) || "—"}
          </p>
        </div>
        {/* ST-03 (BLG-FE-97): Trail Stop tile — Initial Stop subtext + trailing stop value + breach icon */}
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20">
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-1 flex items-center gap-1">
            <span>Init: {position.initial_stop != null ? `${currencySymbol}${Number(position.initial_stop).toFixed(2)}` : "—"}</span>
            <TrailingStopExplainerIcon />
          </p>
          <p className="text-sm font-semibold text-rose-400 flex items-center gap-1">
            {displayTrailStop != null ? `${currencySymbol}${Number(displayTrailStop).toFixed(2)}` : "—"}
            {trailBreached && (
              <AlertTriangle
                className="w-3.5 h-3.5 flex-shrink-0"
                style={{ color: "#EA580C" }}
                aria-label="Trailing stop breach: current price is at or below trailing stop level"
                data-testid="trail-stop-breach-icon"
              />
            )}
          </p>
        </div>
      </div>

      {/* Note & Tags Preview */}
      {(position.entry_note || position.tags?.length > 0) && (
        <div className="mb-4 p-3 rounded-xl bg-slate-800/30 border border-slate-700/30">
          {position.entry_note && (
            <button
              onClick={() => setShowNoteModal(true)}
              className="w-full text-left mb-2 text-sm text-slate-600 dark:text-slate-400 italic hover:text-slate-300 transition-colors"
            >
              {position.entry_note.length > 80 
                ? `${position.entry_note.substring(0, 80)}...` 
                : position.entry_note}
            </button>
          )}
          {position.tags?.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {position.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-0.5 text-xs rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                >
                  {tag}
                </span>
              ))}
              {position.tags.length > 3 && (
                <span className="px-2 py-0.5 text-xs text-slate-600 dark:text-slate-400">
                  +{position.tags.length - 3} more
                </span>
              )}
            </div>
          )}
        </div>
      )}

      {/* ST-15 (v7.0, BLG-FEAT-68): card footer, after the alert-icon row, before Actions */}
      <div className="pt-4 border-t border-slate-700/50">
        <LastReviewedRow position={position} drawdownActive={drawdownActive} />
      </div>

      <div className="flex items-center gap-2">
        <Button
          variant="ghost"
          size="sm"
          className="flex-1 text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
          onClick={() => onEdit(position)}
        >
          <Edit2 className="w-4 h-4 mr-2" />
          Edit
        </Button>
        {/* ST-01 (v6.9, BLG-FEAT-64): Recheck Compliance — grid card footer action */}
        <Button
          variant="ghost"
          size="sm"
          title="Recheck Compliance"
          aria-label={`Recheck compliance for ${position.ticker}`}
          data-testid="recheck-compliance-button"
          className="flex-1 text-amber-400/80 hover:text-amber-300 hover:bg-amber-500/10"
          onClick={() => onRecheck(position)}
        >
          <Zap className="w-4 h-4 mr-2" />
          Recheck
        </Button>
        <Button
          variant="ghost"
          size="sm"
          className="flex-1 text-rose-400 hover:text-rose-300 hover:bg-rose-500/10"
          onClick={() => onExit(position)}
        >
          <LogOut className="w-4 h-4 mr-2" />
          Exit
        </Button>
      </div>
      
      {/* Subtle glow */}
      <div className={cn(
        "absolute -bottom-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-20",
        isProfit ? "bg-emerald-500" : "bg-rose-500"
      )} />

      {/* Note Modal */}
      <Dialog open={showNoteModal} onOpenChange={setShowNoteModal}>
        <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md">
          <DialogHeader>
            <DialogTitle className="text-cyan-400">Trade Entry Note</DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
              {position.entry_note}
            </p>
            {position.tags?.length > 0 && (
              <div className="mt-4 pt-4 border-t border-slate-700/50">
                <p className="text-xs text-slate-600 dark:text-slate-400 mb-2">Tags:</p>
                <div className="flex flex-wrap gap-2">
                  {position.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 text-xs rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </motion.div>
  );
}
