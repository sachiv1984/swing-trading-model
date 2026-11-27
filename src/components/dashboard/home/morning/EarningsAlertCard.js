import { useQuery, useQueries } from "@tanstack/react-query";
import { Calendar } from "lucide-react";
import { api, apiFetch } from "../../../../api/base44Client";
import DashboardCard from "../DashboardCard";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

export default function EarningsAlertCard() {
  const { data: positions = [], isLoading: posLoading, error: posError } = useQuery({
    queryKey: ["morning-positions"],
    queryFn: () => api.positions.list(),
    retry: 1,
  });

  const posArr = Array.isArray(positions) ? positions : [];

  const earningsQueries = useQueries({
    queries: posArr.map(p => ({
      queryKey: ["morning-earnings", p.ticker, p.market],
      queryFn: async () => {
        const res = await apiFetch(`${API_BASE}/earnings/${encodeURIComponent(p.ticker)}?market=${p.market || "US"}`);
        return res.json();
      },
      enabled: posArr.length > 0,
      retry: 0,
      staleTime: 5 * 60 * 1000,
    })),
  });

  const earningsInWindow = earningsQueries.filter(q => {
    const d = q.data;
    return d && d.days_until_earnings != null && d.days_until_earnings >= 0 && d.days_until_earnings <= 7;
  });

  const count = earningsInWindow.length;
  const tickers = earningsInWindow.map(q => q.data.ticker).slice(0, 2);
  const earningsLoading = posArr.length > 0 && earningsQueries.some(q => q.isLoading);
  // dashboard.md §3A (ST-09): an error is not empty. With no dated earnings in
  // the window, a failed lookup (request error, or `data_status: unavailable`
  // since ST-33) means the card does not know, so it shows its error in place
  // instead of folding into "Nothing to show". What the card shows beside dated
  // results when some lookups fail is BLG-FE-333.
  const lookupFailed = earningsQueries.some(q => q.isError || q.data?.data_status === "unavailable");
  const cardError = posError || (count === 0 && lookupFailed ? new Error("earnings lookup failed") : null);

  const subtext = tickers.join(", ") + (earningsInWindow.length > 2 ? ` +${earningsInWindow.length - 2} more` : "");

  return (
    <DashboardCard
      foldKey="earnings"
      title="Earnings"
      to="/Positions"
      isLoading={posLoading || earningsLoading}
      error={cardError}
      empty={count === 0}
      emptyIcon={<Calendar className="w-8 h-8 text-slate-600" />}
      emptyHeading="No earnings in 7 days"
      emptyBody="Upcoming earnings will show here."
    >
      <p className="text-4xl font-bold text-yellow-700 dark:text-yellow-400 mb-2">{count}</p>
      <p className="text-sm text-slate-600 dark:text-slate-400">{subtext}</p>
    </DashboardCard>
  );
}
