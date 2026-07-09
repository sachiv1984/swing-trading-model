import PropTypes from "prop-types";
import { cn } from "../../lib/utils";
import { useEarnings } from "../../hooks/useEarnings";

const EARNINGS_DUE_SOON_DAYS = 5;
const EARNINGS_UPCOMING_DAYS = 14;

const SIGNAL_BADGE_CONFIG = {
  active: { label: "Active", cls: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
  watch: { label: "Watch", cls: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
  no_signal: { label: "No Signal", cls: "bg-slate-700/50 text-slate-600 dark:text-slate-400 border-slate-600/30" },
};

export function SignalBadge({ status }) {
  const cfg = SIGNAL_BADGE_CONFIG[status] || { label: status, cls: "bg-slate-700/50 text-slate-600 dark:text-slate-400 border-slate-600/30" };
  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border", cfg.cls)}>
      {cfg.label}
    </span>
  );
}
SignalBadge.propTypes = { status: PropTypes.string };

export function MarketBadge({ market }) {
  const cls = market === "UK"
    ? "bg-blue-500/20 text-blue-400 border-blue-500/30"
    : "bg-violet-500/20 text-violet-400 border-violet-500/30";
  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border", cls)}>
      {market}
    </span>
  );
}
MarketBadge.propTypes = { market: PropTypes.string };

export function priceDisplay(value, market) {
  if (value == null) return "—";
  const sym = market === "UK" ? "£" : "$";
  return `${sym}${Number(value).toFixed(2)}`;
}

export function WatchlistEarningsBadge({ ticker, market }) {
  const { data, loading } = useEarnings(ticker, market);
  if (loading) return <span className="text-slate-600 text-xs">…</span>;
  if (!data || data.days_until_earnings == null) return <span className="text-slate-600 text-xs">—</span>;
  const days = data.days_until_earnings;
  if (days < 0) return <span className="text-slate-600 text-xs">—</span>;
  if (days === 0) return <span className="text-amber-400 font-medium text-xs" title={data.next_earnings_date}>Today</span>;
  const cls = days <= EARNINGS_DUE_SOON_DAYS
    ? "text-amber-400 font-medium"
    : days <= EARNINGS_UPCOMING_DAYS
      ? "text-yellow-500"
      : "text-slate-600 dark:text-slate-400";
  return <span className={`text-xs ${cls}`} title={data.next_earnings_date}>{days}d</span>;
}
WatchlistEarningsBadge.propTypes = { ticker: PropTypes.string, market: PropTypes.string };
