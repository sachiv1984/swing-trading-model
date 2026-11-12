import { ShieldAlert, AlertCircle, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";
import { createPageUrl } from "../../utils";
import { isInGrace } from "../../lib/positionUrgency";

// ST-04 (BLG-FE-257, v9.17): grace detail lives only in the Positions grace view
// (positions.md §Grace Period View). This panel shows the heading, the count
// badge, when the next grace period ends, and a link to that view
// (risk_dashboard.md v0.1.16 §5.2). The per-position rows are removed.
// grace_days_remaining 1 is the last day of grace ("Ends today", Day 10 of 10),
// so a value n ends in n − 1 days, matching the Positions strip's "next ends"
// date. 0 means grace has just ended; the position moves on at the next refresh.
function nextEndsText(days) {
  if (days === null) return null;
  if (days <= 0) return "Grace period has ended";
  if (days === 1) return "Ends today";
  const n = days - 1;
  return `Next ends in ${n} day${n === 1 ? "" : "s"}`;
}

export default function GracePeriodPanel({ positions = [], error }) {
  const gracePosts = positions.filter(isInGrace);
  const days = gracePosts
    .map((p) => p.grace_days_remaining)
    .filter((d) => d !== null && d !== undefined);
  const nextEnds = nextEndsText(days.length ? Math.min(...days) : null);

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-gradient-to-br from-amber-500/30 to-orange-500/30">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
        </div>
        <h2 className="text-sm font-medium text-slate-300">Grace Period Positions</h2>
        {!error && gracePosts.length > 0 && (
          <span className="ml-auto text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
            {gracePosts.length} position{gracePosts.length > 1 ? "s" : ""} in grace period
          </span>
        )}
      </div>

      {error ? (
        <div className="flex items-center gap-3 rounded-lg bg-rose-900/20 border border-rose-500/40 px-4 py-3">
          <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
          <p className="text-sm text-rose-300">Unable to load position data</p>
        </div>
      ) : gracePosts.length === 0 ? (
        <p className="text-sm text-slate-600 dark:text-slate-400 italic">No positions currently in grace period.</p>
      ) : (
        <div className="space-y-3">
          {nextEnds && (
            <p className="text-sm text-slate-300" data-testid="grace-panel-next-ends">{nextEnds}</p>
          )}
          <Link
            to={`${createPageUrl("Positions")}?grace=open`}
            data-testid="grace-panel-link"
            className="inline-flex items-center gap-1 text-sm font-medium text-amber-400 hover:text-amber-300 underline-offset-2 hover:underline"
          >
            View grace periods on Positions
            <ChevronRight size={14} className="text-slate-600 dark:text-slate-400" aria-hidden="true" />
          </Link>
        </div>
      )}
    </div>
  );
}
