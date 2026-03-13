import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import DashboardCard from "./DashboardCard";

export default function GracePeriodCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["home-grace-period"],
    queryFn: async () => {
      const res = await fetch("/api/positions");
      if (!res.ok) throw new Error(`API error ${res.status}`);
      return res.json();
    },
    retry: 1,
  });

  const positions = Array.isArray(data) ? data : (data?.positions ?? data?.data ?? []);
  const gracePositions = positions.filter(p => p.grace_days_remaining > 0 || p.grace_end_date);

  const nextExpiry = gracePositions
    .filter(p => p.grace_end_date)
    .sort((a, b) => new Date(a.grace_end_date) - new Date(b.grace_end_date))[0];

  return (
    <DashboardCard title="In Grace Today" to="/RiskDashboard" isLoading={isLoading} error={error}>
      <p className="text-4xl font-bold text-amber-400 mb-2">{gracePositions.length}</p>
      <p className="text-sm text-slate-400">
        {nextExpiry
          ? `Next expiry: ${format(new Date(nextExpiry.grace_end_date), "d MMM")}`
          : gracePositions.length === 0
          ? "No grace positions"
          : "No expiry date set"}
      </p>
    </DashboardCard>
  );
}
