import { useQuery } from "@tanstack/react-query";
import { Clock } from "lucide-react";
import { api } from "../../../api/base44Client";
import DashboardCard from "./DashboardCard";
import { isInGrace, minGraceDaysRemaining, nextEndsText } from "../../../lib/positionUrgency";

export default function GracePeriodCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["home-grace-period"],
    queryFn: () => api.positions.list(),
    retry: 1,
  });

  const positions = Array.isArray(data) ? data : [];
  // dashboard.md v4.4 §4B and Card 3 (ST-10, BLG-FE-308): the one grace
  // definition, and the Risk Dashboard grace panel's "next ends" text from the
  // smallest grace_days_remaining. The old line read grace_end_date, which no
  // endpoint returns, so it always said "No expiry date set".
  const gracePositions = positions.filter(isInGrace);
  const nextEnds = nextEndsText(minGraceDaysRemaining(gracePositions));

  return (
    <DashboardCard
      foldKey="in-grace"
      title="In Grace Today"
      // ST-04 (BLG-FE-257, v9.17): the card opens the single grace view
      // (dashboard.md v4.2 Card 3; positions.md §Grace Period View).
      to="/Positions?grace=open"
      isLoading={isLoading}
      error={error}
      empty={gracePositions.length === 0}
      emptyIcon={<Clock className="w-8 h-8 text-slate-600" />}
      emptyHeading="No positions in grace"
      emptyBody="Positions approaching grace deadlines will show here."
    >
      <p className="text-4xl font-bold text-amber-700 dark:text-amber-400 mb-2">{gracePositions.length}</p>
      {nextEnds && (
        <p className="text-sm text-slate-600 dark:text-slate-400" data-testid="dashboard-grace-next-ends">{nextEnds}</p>
      )}
    </DashboardCard>
  );
}
