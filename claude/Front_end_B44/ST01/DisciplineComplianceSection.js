import { useQuery } from "@tanstack/react-query";
import { BookOpen, Target, BarChart2, AlertCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

function ComplianceCard({ title, value, icon: CardIcon, gradient, isLoading, isError }) {
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
          <p className="text-2xl font-bold text-white">{value}</p>
        )}
      </div>
    </div>
  );
}

export default function DisciplineComplianceSection({ period }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["compliance-metrics", period],
    queryFn: async () => {
      const res = await fetch(`/api/analytics/compliance-metrics?period=${period}`);
      if (!res.ok) throw new Error(`Compliance metrics API error ${res.status}`);
      return res.json();
    },
    retry: 1,
  });

  const metrics = data?.data;
  const notEnoughData = data?.has_enough_data === false;

  const fmt = (val) =>
    val != null ? `${(val * 100).toFixed(1)}%` : "—";

  const cards = [
    {
      title: "Journal Completion Rate",
      value: notEnoughData ? "Not enough data" : fmt(metrics?.journal_completion_rate),
      icon: BookOpen,
      gradient: "from-violet-500 to-purple-500",
    },
    {
      title: "Stop-Based Exit Rate",
      value: notEnoughData ? "Not enough data" : fmt(metrics?.stop_based_exit_rate),
      icon: Target,
      gradient: "from-rose-500 to-red-500",
    },
    {
      title: "Average Position Size",
      value: notEnoughData ? "Not enough data" : fmt(metrics?.avg_position_size_pct),
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
