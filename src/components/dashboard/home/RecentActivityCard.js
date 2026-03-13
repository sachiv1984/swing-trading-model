import { useQuery } from "@tanstack/react-query";
import { formatDistanceToNow } from "date-fns";
import { api } from "@/api/base44Client";
import DashboardCard from "./DashboardCard";

function activityLabel(t) {
  if (t.exit_date || t.status === "closed") {
    const r = t.r_multiple != null ? t.r_multiple : null;
    return {
      label: `${t.ticker} closed`,
      detail: r != null ? `(${r > 0 ? "+" : ""}${Number(r).toFixed(1)}R)` : "",
      date: t.exit_date ?? t.updated_date,
    };
  }
  if (t.stop_updated_date) {
    return { label: `Stop updated on ${t.ticker}`, detail: "", date: t.stop_updated_date };
  }
  return { label: `${t.ticker} opened`, detail: "", date: t.entry_date ?? t.created_date };
}

export default function RecentActivityCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["home-recent-activity"],
    queryFn: () => api.trades.list(),
    retry: 1,
  });

  const trades = Array.isArray(data) ? data : (data?.trades ?? data?.data ?? []);
  const recent = [...trades]
    .sort((a, b) => new Date(b.exit_date ?? b.updated_date ?? b.entry_date) - new Date(a.exit_date ?? a.updated_date ?? a.entry_date))
    .slice(0, 5);

  return (
    <DashboardCard title="Recent Activity" to="/TradeHistory" isLoading={isLoading} error={error}>
      {recent.length === 0 ? (
        <p className="text-sm text-slate-500">No recent trade activity</p>
      ) : (
        <ul className="space-y-2">
          {recent.map((t, i) => {
            const { label, detail, date } = activityLabel(t);
            const ago = date ? formatDistanceToNow(new Date(date), { addSuffix: true }) : "";
            return (
              <li key={t.id ?? i} className="flex items-start justify-between gap-2">
                <span className="text-sm text-slate-200 truncate">
                  {label} <span className="text-slate-400">{detail}</span>
                </span>
                <span className="text-xs text-slate-500 whitespace-nowrap shrink-0">{ago}</span>
              </li>
            );
          })}
        </ul>
      )}
    </DashboardCard>
  );
}
