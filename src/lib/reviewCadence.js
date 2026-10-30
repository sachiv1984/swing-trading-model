// Position review cadence nudge (ST-15, v7.0, BLG-FEAT-68): the Last Reviewed
// flag for the Positions table and grid views. Spec: positions.md §Last
// Reviewed Column. One helper for both views (ST-14, v9.14, BLG-SPEC-192), so
// the two cannot drift.
import { differenceInDays } from "date-fns";
import { GRACE_PERIOD_DAYS } from "../constants/strategy";

export const REVIEW_STALE_THRESHOLD_DAYS = 14;
// ST-14 (BLG-BE-147, v9.11): the same predicate as the Grace Period Alert
// trigger — 2 or fewer calendar days of grace left — not days_in_state.
export const GRACE_SUPPRESSION_DAYS_REMAINING = 2;

// True while the Grace Period Alert Zone shows the position: stored GRACE with
// 2 or fewer days left, or (ST-14, v9.14) stored GRACE with grace_days_remaining
// null and holding_days >= 10, the ended-grace case the Alert Zone shows as
// "Grace period has ended". holding_days is the calendar-day count GET /positions
// uses for grace_days_remaining, never days_in_state.
export function isGraceAlertSuppressed(position) {
  const state = position.lifecycle_state || position.position_state;
  if (state !== "GRACE") return false;
  const daysLeft = position.grace_days_remaining;
  if (daysLeft != null) return daysLeft <= GRACE_SUPPRESSION_DAYS_REMAINING;
  return position.holding_days != null && position.holding_days >= GRACE_PERIOD_DAYS;
}

// AC-04: suppress the flagged/amber state when the position is already
// surfaced by the Grace Period Alert Zone or the portfolio-level Drawdown
// Review Prompt. The drawdown prompt has no per-position breakdown (only
// aggregate positions_by_state counts) — while it is active, treat every
// open position as already surfaced by it, per the design intent that this
// is a portfolio-wide review nudge (ux_spec.md §5 rationale: "both existing
// prompts already ask the user to review... for the same position" reads as
// position-scoped for Grace, portfolio-scoped for Drawdown).
export function getReviewCadenceState(position, drawdownActive) {
  const lastReviewedAt = position.last_reviewed_at;
  const referenceDate = lastReviewedAt ? new Date(lastReviewedAt) : new Date(position.entry_date);
  const daysSinceReview = differenceInDays(new Date(), referenceDate);

  const suppressed = isGraceAlertSuppressed(position) || drawdownActive;

  const flagged = !suppressed && daysSinceReview >= REVIEW_STALE_THRESHOLD_DAYS;
  const label = lastReviewedAt ? `Reviewed ${daysSinceReview}d ago` : "Not yet reviewed";
  const ariaLabel = flagged
    ? `Position not reviewed in ${daysSinceReview} days — consider reviewing`
    : `Last reviewed ${daysSinceReview} days ago`;

  return { label, flagged, ariaLabel, daysSinceReview };
}
