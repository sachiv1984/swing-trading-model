import { useQuery } from "@tanstack/react-query";
import { api } from "../../../api/base44Client";
import DashboardCard from "./DashboardCard";

export default function OpenPositionsCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["home-open-positions"],
    queryFn: () => api.positions.list(),
    retry: 1,
  });

  const positions = Array.isArray(data) ? data : [];
  const open = positions.filter(p => p.status === "open" || p.status === "ACTIVE" || p.status === "GRACE");
  const profitable = open.filter(p => (p.pnl ?? 0) > 0).length;
  const losing = open.filter(p => (p.pnl ?? 0) < 0).length;
  const grace = open.filter(p => p.grace_days_remaining > 0 || p.status === "GRACE").length;

  return (
    <DashboardCard title="Open Positions" to="/Positions" isLoading={isLoading} error={error}>
      <p className="text-4xl font-bold text-white mb-2">{open.length}</p>
      <div className="flex flex-wrap gap-x-3 gap-y-1 text-sm text-slate-600 dark:text-slate-400">
        {profitable > 0 && <span className="text-emerald-400">{profitable} profitable</span>}
        {losing > 0 && <span className="text-rose-400">{losing} losing</span>}
        {grace > 0 && <span className="text-amber-400">{grace} in grace</span>}
        {open.length === 0 && <span>No open positions</span>}
      </div>
    </DashboardCard>
  );
}
