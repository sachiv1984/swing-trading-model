import { useQuery } from "@tanstack/react-query";
import { Inbox } from "lucide-react";
import { api } from "../../../api/base44Client";
import DashboardCard from "./DashboardCard";
import { isInGrace } from "../../../lib/positionUrgency";

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
  // dashboard.md v4.4 §4B (ST-10, BLG-FE-308): the one grace definition, over
  // the same GET /positions rows Card 3 and Positions to Watch count (that
  // endpoint returns open positions only).
  const grace = positions.filter(isInGrace).length;

  return (
    <DashboardCard
      foldKey="open-positions"
      title="Open Positions"
      to="/Positions"
      isLoading={isLoading}
      error={error}
      empty={open.length === 0}
      emptyIcon={<Inbox className="w-8 h-8 text-slate-600" />}
      emptyHeading="No open positions"
      emptyBody="Open a position to see it here."
    >
      <p className="text-4xl font-bold text-slate-900 dark:text-white mb-2">{open.length}</p>
      <div className="flex flex-wrap gap-x-3 gap-y-1 text-sm text-slate-600 dark:text-slate-400">
        {profitable > 0 && <span className="text-emerald-700 dark:text-emerald-400">{profitable} profitable</span>}
        {losing > 0 && <span className="text-rose-700 dark:text-rose-400">{losing} losing</span>}
        {grace > 0 && <span className="text-amber-700 dark:text-amber-400">{grace} in grace</span>}
      </div>
    </DashboardCard>
  );
}
