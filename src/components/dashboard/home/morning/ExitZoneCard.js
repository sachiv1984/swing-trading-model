import { useQuery } from "@tanstack/react-query";
import { Eye } from "lucide-react";
import { api } from "../../../../api/base44Client";
import DashboardCard from "../DashboardCard";
import { isGraceEndingWithin, isInGrace } from "../../../../lib/positionUrgency";

// "Positions to Watch" (dashboard.md v4.4 §1A Cards table and §4B; ST-10,
// BLG-FE-308, v9.18): the count of in-grace positions by the one grace
// definition, "{n} in grace", plus " · {m} ending within 2 days" when any has
// grace_days_remaining ≤ 2. The "exit zone" wording (a strategy term for
// something else) and the grace-period-alerts query are gone.
export default function ExitZoneCard() {
  const { data: positions = [], isLoading, error } = useQuery({
    queryKey: ["morning-positions"],
    queryFn: () => api.positions.list(),
    retry: 1,
  });

  const inGrace = Array.isArray(positions) ? positions.filter(isInGrace) : [];
  const total = inGrace.length;
  const endingSoon = inGrace.filter((p) => isGraceEndingWithin(p, 2)).length;
  const subtext = `${total} in grace` + (endingSoon > 0 ? ` · ${endingSoon} ending within 2 days` : "");

  return (
    <DashboardCard
      foldKey="positions-to-watch"
      title="Positions to Watch"
      to={total > 0 ? "/Positions?grace=open" : "/Positions"}
      isLoading={isLoading}
      error={error}
      empty={total === 0}
      emptyIcon={<Eye className="w-8 h-8 text-slate-600" />}
      emptyHeading="No positions to watch"
      emptyBody="Positions in their grace period will show here."
    >
      <p className="text-4xl font-bold text-amber-700 dark:text-amber-400 mb-2">{total}</p>
      <p className="text-sm text-slate-600 dark:text-slate-400" data-testid="positions-to-watch-subtext">{subtext}</p>
    </DashboardCard>
  );
}
