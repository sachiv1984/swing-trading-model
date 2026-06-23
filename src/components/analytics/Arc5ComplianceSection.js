import { useQuery } from "@tanstack/react-query";
import { ShieldCheck, Activity, AlertTriangle, ClipboardList } from "lucide-react";
import { cn } from "../../lib/utils";
import { api } from "../../api/base44Client";

function ComplianceCard({ title, value, subLabel, icon: CardIcon, gradient, isLoading, isError }) {
  const Icon = CardIcon;
  return (
    <div className="relative overflow-hidden rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <div className={cn("absolute inset-0 opacity-10 bg-gradient-to-br", gradient)} />
      <div className="relative z-10">
        <div className="flex items-start justify-between mb-4">
          <p className="text-xs text-slate-400 uppercase tracking-wider">{title}</p>
          <div className={cn("p-2 rounded-lg bg-gradient-to-br", gradient)}>
            <Icon className="w-4 h-4 text-white" />
          </div>
        </div>
        {isLoading ? (
          <div className="h-7 w-16 bg-slate-700 rounded animate-pulse" />
        ) : isError ? (
          <p className="text-sm text-rose-400">Unable to load</p>
        ) : (
          <>
            <p className="text-2xl font-bold text-white">{value}</p>
            {subLabel && <p className="text-xs text-slate-400 mt-1">{subLabel}</p>}
          </>
        )}
      </div>
    </div>
  );
}

// Arc 5 Signal Compliance panel — §19 of analytics.md (v4.0, ST-02 + ST-04)
// Source: GET /analytics/arc5-compliance (canonical per metrics_definitions.md §Arc 5 Compliance Metrics)
export default function Arc5ComplianceSection() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["arc5-compliance"],
    queryFn: () => api.analytics.arc5Compliance("7d"),
    retry: 1,
  });

  const metrics = data;

  const fmtRate = (val) => (val != null ? `${(val * 100).toFixed(1)}%` : "—");
  const fmtCount = (val) => (val != null ? val.toFixed(1) : "—");
  const fmtText = (val) => (val != null ? val.replace(/_/g, " ") : "—");

  const cards = [
    {
      title: "Red Flag Events/Week",
      value: fmtCount(metrics?.events_per_week),
      subLabel: "rolling 7 days",
      icon: Activity,
      gradient: "from-orange-500 to-amber-500",
    },
    {
      title: "Override Rate",
      value: fmtRate(metrics?.override_rate),
      subLabel: "overrides / validation attempts",
      icon: AlertTriangle,
      gradient: "from-rose-500 to-red-500",
    },
    {
      title: "Top Rule Breach",
      value: fmtText(metrics?.top_rule_breach),
      subLabel: "most frequent event type",
      icon: ShieldCheck,
      gradient: "from-violet-500 to-purple-500",
    },
    {
      title: "Trade Plan Adherence",
      value: fmtRate(metrics?.trade_plan_adherence_rate),
      subLabel: "trades with plan / total closed trades",
      icon: ClipboardList,
      gradient: "from-emerald-500 to-teal-500",
    },
  ];

  return (
    <div>
      <h2 className="text-lg font-semibold text-white mb-4">Signal Compliance</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((card) => (
          <ComplianceCard
            key={card.title}
            title={card.title}
            value={card.value}
            subLabel={card.subLabel}
            icon={card.icon}
            gradient={card.gradient}
            isLoading={isLoading}
            isError={!!error}
          />
        ))}
      </div>
    </div>
  );
}
