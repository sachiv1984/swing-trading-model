import { useQuery } from "@tanstack/react-query";
import { formatDistanceToNow } from "date-fns";
import DashboardCard from "./DashboardCard";

function activityLabel(p) {
  if (p.status === "closed" || p.exit_date) {
    const r = p.r_multiple ?? (p.atr_value && p.entry_price && p.exit_price
      ? ((p.exit_price - p.entry_price) / p.atr_value).toFixed(1)
      : null);
    return {
      label: `Closed ${p.ticker}`,
      detail: r != null ? `(${r > 0 ? "+" : ""}${r}R)` : "",
      date: p.exit_date ?? p.updated_date,
    };
  }
  if (p.stop_updated_date) {
    return { label: `Stop updated on ${p.ticker}`, detail: "", date: p.stop_updated_date };
  }
  return { label: `Opened ${p.ticker}`, detail: "", date: p.entry_date ?? p.created_date };
}

export default function RecentActivityCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["home-recent-activity"],
    queryFn: async () => {
      const res = await fetch("/api/positions?limit=10");
      if (!res.ok) throw new Error(`API error ${res.status}`);
      return res.json();
    },
    retry: 1,
  });

  const positions = Array.isArray(data) ? data : (data?.positions ?? data?.data ?? []);
  const recent = [...positions]
    .sort((a, b) => new Date(b.updated_date ?? b.entry_date) - new Date(a.updated_date ?? a.entry_date))
    .slice(0, 5);

  return (
    <DashboardCard title="Recent Activity" to="/TradeHistory" isLoading={isLoading} error={error}>
      {recent.length === 0 ? (
        <p className="text-sm text-slate-500">No recent activity</p>
      ) : (
        <ul className="space-y-2">
          {recent.map(p => {
            const { label, detail, date } = activityLabel(p);
            const ago = date ? formatDistanceToNow(new Date(date), { addSuffix: true }) : "";
            return (
              <li key={p.id} className="flex items-start justify-between gap-2">
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
