import { useQuery } from "@tanstack/react-query";
import { BookOpen, Target, BarChart2, AlertCircle, Loader2 } from "lucide-react";
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
          <Loader2 className="w-5 h-5 animate-spin text-slate-500" />
        ) : isError ? (
          <div className="flex items-center gap-2 text-rose-400">
            <AlertCircle className="w-4 h-4" />
            <span className="text-sm">Unable to load</span>
          </div>
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

// Discipline & Compliance panel — §17 of analytics.md (v1.9, ST-01)
// Source: GET /analytics/compliance-metrics (canonical per metrics_definitions.md v1.7.0)
export default function DisciplineComplianceSection({ period }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["compliance-metrics", period],
    queryFn: () => api.analytics.complianceMetrics(period),
    retry: 1,
  });

  const metrics = data?.data;
  const tradeCount = metrics?.trade_count ?? 0;
  const noData = tradeCount === 0;

  // Backend returns percentages (0–100), 1dp for rates, 2dp for position size
  const fmtRate = (val) => (val != null && !noData ? `${val.toFixed(1)}%` : "—");
  const fmtSize = (val) => (val != null && !noData ? `${val.toFixed(2)}%` : "—");

  const tradeSubLabel = tradeCount > 0 ? `last ${tradeCount} trades` : null;
  const sizeSubLabel = tradeCount > 0 ? `of portfolio, last ${tradeCount} trades` : null;

  const cards = [
    {
      title: "Journal Completion Rate",
      value: fmtRate(metrics?.journal_completion_rate),
      subLabel: tradeSubLabel,
      icon: BookOpen,
      gradient: "from-violet-500 to-purple-500",
    },
    {
      title: "Stop-Based Exit Rate",
      value: fmtRate(metrics?.stop_exit_rate),
      subLabel: tradeSubLabel,
      icon: Target,
      gradient: "from-rose-500 to-red-500",
    },
    {
      title: "Average Position Size",
      value: fmtSize(metrics?.avg_position_size_pct),
      subLabel: sizeSubLabel,
      icon: BarChart2,
      gradient: "from-cyan-500 to-blue-500",
    },
  ];

  return (
    <div>
      <h2 className="text-lg font-semibold text-white mb-4">Discipline &amp; Compliance</h2>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
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
