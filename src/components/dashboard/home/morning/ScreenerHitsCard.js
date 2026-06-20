import { useQuery } from "@tanstack/react-query";
import { api } from "../../../../api/base44Client";
import DashboardCard from "../DashboardCard";

export default function ScreenerHitsCard() {
  const { data: signals = [], isLoading, error } = useQuery({
    queryKey: ["morning-screener-hits"],
    queryFn: () => api.signals.list(),
    retry: 1,
  });

  const newHits = Array.isArray(signals) ? signals.filter(s => s.status === "new").length : 0;

  return (
    <DashboardCard title="Screener Hits" to="/Screener" isLoading={isLoading} error={error}>
      <p className="text-4xl font-bold text-indigo-400 mb-2">{newHits}</p>
      <p className="text-sm text-slate-400">
        {newHits === 0 ? "No new signals" : `new signal${newHits !== 1 ? "s" : ""} today`}
      </p>
    </DashboardCard>
  );
}
