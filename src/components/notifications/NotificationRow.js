import { ShieldAlert, Clock, TrendingDown, BarChart2 } from "lucide-react";
import { cn } from "../../lib/utils";
import { formatDistanceToNow } from "date-fns";

const ICON_MAP = {
  stop_loss_approach: { Icon: ShieldAlert, color: "text-rose-400", bg: "bg-rose-500/10" },
  grace_period_warning: { Icon: Clock, color: "text-amber-400", bg: "bg-amber-500/10" },
  market_regime_change: { Icon: TrendingDown, color: "text-violet-400", bg: "bg-violet-500/10" },
  daily_portfolio_summary: { Icon: BarChart2, color: "text-cyan-400", bg: "bg-cyan-500/10" },
};

function relativeTime(iso) {
  try {
    return formatDistanceToNow(new Date(iso), { addSuffix: true });
  } catch {
    return iso;
  }
}

export default function NotificationRow({ notification, onMarkRead }) {
  const { Icon, color, bg } = ICON_MAP[notification.alert_type] || {
    Icon: ShieldAlert,
    color: "text-slate-600 dark:text-slate-400",
    bg: "bg-slate-500/10",
  };

  return (
    <div
      className={cn(
        "flex gap-4 px-6 py-5 transition-all",
        !notification.read && "border-l-2 border-cyan-400"
      )}
    >
      {/* Icon */}
      <div className={cn("shrink-0 h-8 w-8 rounded-lg flex items-center justify-center", bg)}>
        <Icon className={cn("w-4 h-4", color)} />
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="text-sm font-medium text-white truncate">{notification.title}</p>
            <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5 truncate">{notification.message}</p>
          </div>
          <span
            className="text-xs text-slate-600 dark:text-slate-400 shrink-0 mt-0.5 cursor-default"
            title={notification.created_at}
          >
            {relativeTime(notification.created_at)}
          </span>
        </div>

        <div className="mt-2 flex items-center gap-3">
          {!notification.read && (
            <button
              onClick={onMarkRead}
              className="text-xs text-cyan-400 hover:text-cyan-300 transition-colors"
            >
              Mark as read
            </button>
          )}
          {notification._error && (
            <span className="text-xs text-rose-400">Failed to mark as read.</span>
          )}
        </div>
      </div>
    </div>
  );
}
