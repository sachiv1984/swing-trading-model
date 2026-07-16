import { useQuery } from "@tanstack/react-query";
import { ShieldCheck } from "lucide-react";
import { api } from "../../../../api/base44Client";
import DashboardCard from "../DashboardCard";

function sevenDaysAgo() {
  const d = new Date();
  d.setDate(d.getDate() - 7);
  return d.toISOString().split("T")[0];
}

export default function RedFlagsCard() {
  const since = sevenDaysAgo();
  const { data, isLoading, error } = useQuery({
    queryKey: ["morning-red-flags", since],
    queryFn: () => api.portfolio.redFlagJournal({ since, page_size: 1 }),
    retry: 1,
  });

  const total = data?.total ?? 0;

  return (
    <DashboardCard
      title="Red Flags"
      to="/RedFlagJournal"
      isLoading={isLoading}
      error={error}
      empty={total === 0}
      emptyIcon={<ShieldCheck className="w-8 h-8 text-slate-600" />}
      emptyHeading="No red flags this week"
      emptyBody="Journal entries flagged for review will show here."
    >
      <p className="text-4xl font-bold text-rose-400 mb-2">{total}</p>
      <p className="text-sm text-slate-600 dark:text-slate-400">
        event{total !== 1 ? "s" : ""} in last 7 days
      </p>
    </DashboardCard>
  );
}
