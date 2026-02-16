import { TrendingUp, TrendingDown, Target, Zap, Calendar } from "lucide-react";
import { cn } from "../../lib/utils";

export default function ExecutiveSummaryCards({ metrics, advancedMetrics }) {
  // Calculate days underwater color
  const getDaysUnderwaterColor = (days) => {
    if (days === 0) return "from-emerald-500 to-green-500";
    if (days <= 30) return "from-cyan-500 to-blue-500";
    if (days <= 90) return "from-amber-500 to-orange-500";
    return "from-rose-500 to-red-500";
  };

  const cards = [
    {
      title: "Sharpe Ratio",
      subtitle: "Risk-Adjusted Returns",
      value: metrics.sharpeRatio?.toFixed(2) || "N/A",
      icon: TrendingUp,
      gradient: "from-cyan-500 to-blue-500",
      benchmark: metrics.sharpeRatio > 2 ? "Excellent" : metrics.sharpeRatio > 1 ? "Good" : "Needs Improvement"
    },
    {
      title: "Max Drawdown",
      subtitle: "Worst Case Scenario",
      value: metrics.maxDrawdown ? `${metrics.maxDrawdown.percent.toFixed(1)}%` : "N/A",
      subValue: metrics.maxDrawdown ? `£${metrics.maxDrawdown.amount.toFixed(2)}` : "",
      date: metrics.maxDrawdown?.date,
      icon: TrendingDown,
      gradient: "from-rose-500 to-red-500"
    },
    {
      title: "Recovery Factor",
      subtitle: "Resilience Measure",
      value: metrics.recoveryFactor?.toFixed(2) || "N/A",
      icon: Target,
      gradient: "from-violet-500 to-purple-500",
      benchmark: metrics.recoveryFactor > 2 ? "Strong" : "Moderate"
    },
    {
      title: "Expectancy",
      subtitle: "Edge Per Trade",
      value: metrics.expectancy ? `£${metrics.expectancy.toFixed(2)}` : "N/A",
      icon: Zap,
      gradient: "from-emerald-500 to-green-500",
      isPositive: metrics.expectancy > 0
    },
    {
      title: "Time Underwater",
      subtitle: "Current Risk Status",
      value: advancedMetrics?.daysUnderwater === 0 ? "At Peak 🎉" : advancedMetrics?.daysUnderwater ? `${advancedMetrics.daysUnderwater} days` : "No Data",
      subValue: advancedMetrics?.portfolioPeakEquity ? `Peak: £${advancedMetrics.portfolioPeakEquity.toFixed(0)}` : "",
      date: advancedMetrics?.peakDate ? `on ${advancedMetrics.peakDate}` : "",
      icon: Calendar,
      gradient: getDaysUnderwaterColor(advancedMetrics?.daysUnderwater || 0)
    },
    {
      title: "Profit Factor",
      subtitle: "Win/Loss Ratio",
      value: metrics.profitFactor?.toFixed(2) || "N/A",
      icon: Target,
      gradient: "from-amber-500 to-orange-500",
      benchmark: metrics.profitFactor > 2 ? "Excellent" : metrics.profitFactor > 1 ? "Good" : "Poor"
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {cards.map((card, idx) => (
        <div
          key={idx}
          className="relative overflow-hidden rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm"
        >
          <div className={cn("absolute inset-0 opacity-10 bg-gradient-to-br", card.gradient)} />
          <div className="relative z-10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs text-slate-400 uppercase tracking-wider">{card.title}</p>
                <p className="text-xs text-slate-500 mt-1">{card.subtitle}</p>
              </div>
              <div className={cn("p-2 rounded-lg bg-gradient-to-br", card.gradient)}>
                <card.icon className="w-4 h-4 text-white" />
              </div>
            </div>
            <div>
              <p className="text-2xl font-bold text-white mb-1">{card.value}</p>
              {card.subValue && <p className="text-sm text-slate-400">{card.subValue}</p>}
              {card.date && <p className="text-xs text-slate-500 mt-1">{card.date}</p>}
              {card.benchmark && (
                <div className="mt-2">
                  <span className={cn(
                    "text-xs px-2 py-1 rounded-full",
                    card.benchmark.includes("Excellent") || card.benchmark.includes("Strong")
                      ? "bg-emerald-500/20 text-emerald-400"
                      : card.benchmark.includes("Good")
                      ? "bg-cyan-500/20 text-cyan-400"
                      : "bg-slate-500/20 text-slate-400"
                  )}>
                    {card.benchmark}
                  </span>
                </div>
              )}
              {card.isPositive !== undefined && (
                <div className="mt-2">
                  <span className={cn(
                    "text-xs px-2 py-1 rounded-full",
                    card.isPositive
                      ? "bg-emerald-500/20 text-emerald-400"
                      : "bg-rose-500/20 text-rose-400"
                  )}>
                    {card.isPositive ? "Positive Edge" : "Negative Edge"}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
