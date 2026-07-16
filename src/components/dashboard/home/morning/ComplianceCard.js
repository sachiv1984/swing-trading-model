import { useQuery } from "@tanstack/react-query";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { api } from "../../../../api/base44Client";
import DashboardCard from "../DashboardCard";

function overallScore(data) {
  if (!data) return null;
  const rates = data.validation_pass_rate_by_rule ? Object.values(data.validation_pass_rate_by_rule) : [];
  const passRates = rates.map(r => (typeof r === "number" ? r : r?.pass_rate)).filter(v => v != null);
  if (passRates.length === 0) return data.trade_plan_adherence_rate ?? null;
  const avg = passRates.reduce((s, v) => s + v, 0) / passRates.length;
  return Math.round(avg * 100);
}

export default function ComplianceCard() {
  const { data: data7d, isLoading: loading7d, error: error7d } = useQuery({
    queryKey: ["morning-compliance-7d"],
    queryFn: () => api.analytics.arc5Compliance("7d"),
    retry: 1,
  });

  const { data: data30d, isLoading: loading30d } = useQuery({
    queryKey: ["morning-compliance-30d"],
    queryFn: () => api.analytics.arc5Compliance("30d"),
    retry: 1,
  });

  const score = overallScore(data7d);
  const score30 = overallScore(data30d);

  let trend = "flat";
  if (score != null && score30 != null) {
    if (score > score30 + 1) trend = "up";
    else if (score < score30 - 1) trend = "down";
  }

  const TrendIcon =
    trend === "up" ? TrendingUp :
    trend === "down" ? TrendingDown :
    Minus;

  const trendColor =
    trend === "up" ? "text-emerald-400" :
    trend === "down" ? "text-rose-400" :
    "text-slate-600 dark:text-slate-400";

  return (
    <DashboardCard
      title="Signal Compliance"
      to="/PerformanceAnalytics"
      isLoading={loading7d || loading30d}
      error={error7d}
      empty={score == null}
      emptyIcon={<Minus className="w-8 h-8 text-slate-600" />}
      emptyHeading="No compliance data yet"
      emptyBody="Your score will show here once available."
    >
      <div className="flex items-end gap-2 mb-2">
        <p className="text-4xl font-bold text-emerald-400">{score != null ? `${score}%` : ""}</p>
        <TrendIcon className={`w-5 h-5 mb-1 ${trendColor}`} />
      </div>
      <p className="text-sm text-slate-600 dark:text-slate-400">7-day compliance score</p>
    </DashboardCard>
  );
}
