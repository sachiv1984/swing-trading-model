import { useQuery } from "@tanstack/react-query";
import { Eye } from "lucide-react";
import { api } from "../../../../api/base44Client";
import DashboardCard from "../DashboardCard";

export default function ExitZoneCard() {
  const { data: alerts = [], isLoading: alertsLoading, error: alertsError } = useQuery({
    queryKey: ["morning-grace-alerts"],
    queryFn: () => api.positions.gracePeriodAlerts(),
    retry: 1,
  });

  const { data: positions = [], isLoading: posLoading } = useQuery({
    queryKey: ["morning-positions"],
    queryFn: () => api.positions.list(),
    retry: 1,
  });

  const alertIds = new Set((Array.isArray(alerts) ? alerts : []).map(a => a.position_id));
  const allGrace = Array.isArray(positions) ? positions.filter(p => p.grace_period === true) : [];
  const exitZone = allGrace.filter(p => alertIds.has(p.id));
  const inGrace = allGrace.filter(p => !alertIds.has(p.id));
  const exitZoneCount = exitZone.length;
  const graceCount = inGrace.length;
  const total = exitZoneCount + graceCount;

  const parts = [];
  if (exitZoneCount > 0) parts.push(`${exitZoneCount} exit zone`);
  if (graceCount > 0) parts.push(`${graceCount} in grace`);
  const subtext = parts.join(", ");

  return (
    <DashboardCard
      title="Positions to Watch"
      to="/Positions"
      isLoading={alertsLoading || posLoading}
      error={alertsError}
      empty={total === 0}
      emptyIcon={<Eye className="w-8 h-8 text-slate-600" />}
      emptyHeading="No positions to watch"
      emptyBody="Positions nearing exit zone or grace will show here."
    >
      <p className="text-4xl font-bold text-amber-400 mb-2">{total}</p>
      <p className="text-sm text-slate-600 dark:text-slate-400">{subtext}</p>
    </DashboardCard>
  );
}
