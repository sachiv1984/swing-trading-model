/**
 * GracePeriodView — ST-04 (BLG-FE-257, EPIC-01, v9.17)
 *
 * The only component in the app that renders per-position grace detail. It is
 * the expanded content of the Positions warning strip's grace entry; Dashboard
 * Card 3 and the Risk Dashboard Grace panel show a count and link here
 * (/Positions?grace=open).
 *
 * Spec: docs/specs/frontend/pages/positions.md v2.26 §Grace Period View
 * Design: docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md §5
 *
 * Lists every open position in grace (grace_period === true from GET /positions),
 * joined to GET /positions/grace-period-alerts for the trade plan summary.
 * Order: grace_days_remaining ascending, then ticker A–Z. No dismiss.
 * Display-only (§13): no recommendation; the user decides.
 */

import { Link } from "react-router-dom";
import { cn } from "../../lib/utils";
import { createPageUrl } from "../../utils";
import { GRACE_PERIOD_DAYS } from "../../constants/strategy";
import { isInGrace } from "../../lib/positionUrgency";

const hasDays = (d) => d !== null && d !== undefined;

/**
 * The view's rows: every in-grace position (GET /positions), joined to its
 * grace-period alert for the trade plan summary, plus any alert whose position
 * is not flagged in grace there: a position on its last day whose grace has
 * just ended (grace_days_remaining 0, "Grace period has ended"), or every
 * alert while GET /positions is loading or has failed.
 *
 * `planKnown` is false when no alert row exists for the position. The alerts
 * endpoint returns only positions with grace_days_remaining <= 2, so for the
 * others the view cannot tell whether a plan is linked and shows no plan line
 * (positions.md Known Deviation DEV-EPIC01-ST04-01).
 */
export function graceRows(positions = [], alerts = []) {
  const alertById = new Map(alerts.map((a) => [String(a.position_id), a]));
  const inGrace = positions.filter(isInGrace);
  const seen = new Set(inGrace.map((p) => String(p.id)));
  const fromPositions = inGrace.map((p) => {
    const alert = alertById.get(String(p.id));
    return {
      id: p.id,
      ticker: p.ticker,
      grace_days_remaining: hasDays(p.grace_days_remaining) ? p.grace_days_remaining : alert?.grace_days_remaining ?? null,
      planKnown: Boolean(alert),
      trade_plan_id: alert?.trade_plan_id ?? null,
      trade_plan_summary: alert?.trade_plan_summary ?? null,
    };
  });
  const fromAlertsOnly = alerts
    .filter((a) => !seen.has(String(a.position_id)))
    .map((a) => ({
      id: a.position_id,
      ticker: a.ticker,
      grace_days_remaining: a.grace_days_remaining ?? null,
      planKnown: true,
      trade_plan_id: a.trade_plan_id ?? null,
      trade_plan_summary: a.trade_plan_summary ?? null,
    }));
  const rows = [...fromPositions, ...fromAlertsOnly];
  return rows.sort((a, b) => {
    const da = hasDays(a.grace_days_remaining) ? a.grace_days_remaining : Infinity;
    const db = hasDays(b.grace_days_remaining) ? b.grace_days_remaining : Infinity;
    if (da !== db) return da - db;
    return String(a.ticker).localeCompare(String(b.ticker));
  });
}

// Day {min(11 − grace_days_remaining, 10)} of 10; the entry day is Day 1
// (positions.md §Grace Period Alert Zone convention, carried into this view).
function dayNumber(daysLeft) {
  return hasDays(daysLeft) ? Math.min(GRACE_PERIOD_DAYS + 1 - daysLeft, GRACE_PERIOD_DAYS) : null;
}

function bodyText(daysLeft) {
  if (daysLeft === 0) {
    return "Grace period has ended. Your position will transition to LOSING or PROFITABLE on next refresh.";
  }
  if (hasDays(daysLeft)) {
    return `Your grace period ends in ${daysLeft} day${daysLeft !== 1 ? "s" : ""}. Review your original thesis before the window closes.`;
  }
  return "Your grace period is ending. Review your original thesis before the window closes.";
}

function GraceRow({ row }) {
  const daysLeft = row.grace_days_remaining;
  const day = dayNumber(daysLeft);
  const urgent = hasDays(daysLeft) && daysLeft <= 2;
  const tp = row.trade_plan_summary;
  return (
    <li
      data-testid={`grace-row-${row.ticker}`}
      className={cn(
        "rounded-lg border border-app-line border-l-4 px-4 py-3",
        urgent ? "border-l-amber-500" : "border-l-transparent"
      )}
    >
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
        <Link
          to={`${createPageUrl("Positions")}?position=${encodeURIComponent(row.id)}`}
          className="font-semibold text-app-fg underline-offset-2 hover:underline"
          aria-label={`Open ${row.ticker} on Positions`}
        >
          {row.ticker}
        </Link>
        {day !== null && (
          <span
            data-testid="grace-alert-day-label"
            className={cn("text-xs font-medium", urgent ? "text-app-warning" : "text-app-muted")}
          >
            Day {day} of {GRACE_PERIOD_DAYS}
          </span>
        )}
      </div>
      <p className="text-sm text-app-fg mt-1">{bodyText(daysLeft)}</p>
      {!row.planKnown ? null : tp ? (
        <div className="mt-2 text-xs text-app-fg space-y-0.5" data-testid="grace-row-plan">
          {tp.setup_thesis && (
            <div>
              <span className="text-app-muted">Thesis: </span>
              "{tp.setup_thesis.slice(0, 120)}{tp.setup_thesis.length > 120 ? "…" : ""}"
            </div>
          )}
          {tp.stop_level != null && <div><span className="text-app-muted">Stop: </span>{tp.stop_level}</div>}
          {tp.r_target != null && <div><span className="text-app-muted">R-target: </span>{tp.r_target}R</div>}
        </div>
      ) : (
        <p className="text-xs text-app-muted mt-1">No trade plan linked.</p>
      )}
      {row.trade_plan_id && (
        <Link
          to={`/TradePlan?edit=${encodeURIComponent(row.trade_plan_id)}&ticker=${encodeURIComponent(row.ticker)}`}
          className="inline-block mt-2 text-xs text-app-fg underline hover:no-underline"
        >
          View Trade Plan<span aria-hidden="true"> →</span>
        </Link>
      )}
    </li>
  );
}

export default function GracePeriodView({ rows }) {
  return (
    <ul data-testid="grace-period-view" className="space-y-2">
      {rows.map((row) => <GraceRow key={row.id} row={row} />)}
    </ul>
  );
}
