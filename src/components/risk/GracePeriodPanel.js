import { Clock, ShieldAlert } from "lucide-react";
import { format } from "date-fns";
import { cn } from "../../lib/utils";

function daysColor(days) {
  if (days <= 1) return "text-rose-400 bg-rose-500/10 border-rose-500/30";
  if (days <= 4) return "text-amber-400 bg-amber-500/10 border-amber-500/30";
  return "text-emerald-400 bg-emerald-500/10 border-emerald-500/30";
}

export default function GracePeriodPanel({ positions = [] }) {
  const gracePosts = [...positions]
    .filter((p) => p.grace_period)
    .sort((a, b) => (a.grace_days_remaining ?? 999) - (b.grace_days_remaining ?? 999));

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-gradient-to-br from-amber-500/30 to-orange-500/30">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
        </div>
        <h3 className="text-sm font-medium text-slate-300">Grace Period</h3>
        {gracePosts.length > 0 && (
          <span className="ml-auto text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
            {gracePosts.length} position{gracePosts.length > 1 ? "s" : ""}
          </span>
        )}
      </div>

      {gracePosts.length === 0 ? (
        <p className="text-sm text-slate-500 italic">No positions in grace period.</p>
      ) : (
        <div className="space-y-2">
          {gracePosts.map((p) => {
            const days = p.grace_days_remaining ?? null;
            return (
              <div
                key={p.id}
                className="flex items-center justify-between px-3 py-2.5 rounded-lg bg-slate-800/40 border border-slate-700/30"
              >
                <div className="flex items-center gap-3">
                  <span className="font-semibold text-white">{p.ticker}</span>
                  <span className="text-xs text-slate-500">
                    {p.entry_date ? format(new Date(p.entry_date), "dd MMM yy") : "—"}
                  </span>
                </div>
                <div className={cn("flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full border", daysColor(days ?? 999))}>
                  <Clock className="w-3 h-3" />
                  {days === null ? "N/A" : `${days}d remaining`}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
