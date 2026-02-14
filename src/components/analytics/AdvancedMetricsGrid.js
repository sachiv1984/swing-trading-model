export default function AdvancedMetricsGrid({ metrics }) {
  const gridMetrics = [
    [
      { label: "Profit Factor", value: metrics.profitFactor?.toFixed(2) || "N/A", target: ">1.5" },
      { label: "Risk/Reward Ratio", value: metrics.riskRewardRatio?.toFixed(2) || "N/A", target: ">2.0" }
    ],
    [
      { label: "Win Streak", value: metrics.winStreak || 0, suffix: " trades" },
      { label: "Loss Streak", value: metrics.lossStreak || 0, suffix: " trades" }
    ],
    [
      { label: "Avg Hold Time (Winners)", value: metrics.avgHoldWinners?.toFixed(1) || "N/A", suffix: " days" },
      { label: "Avg Hold Time (Losers)", value: metrics.avgHoldLosers?.toFixed(1) || "N/A", suffix: " days" }
    ],
    [
      { label: "Trade Frequency", value: metrics.tradeFrequency?.toFixed(1) || "N/A", suffix: " per week" },
      { label: "Capital Efficiency", value: metrics.capitalEfficiency?.toFixed(1) || "N/A", suffix: "%" }
    ]
  ];

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-white mb-6">Advanced Metrics</h3>
      <div className="space-y-6">
        {gridMetrics.map((row, rowIdx) => (
          <div key={rowIdx} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {row.map((metric, idx) => (
              <div key={idx} className="p-4 rounded-lg bg-slate-900/50 border border-slate-700/30">
                <p className="text-xs text-slate-400 mb-2">{metric.label}</p>
                <div className="flex items-baseline gap-2">
                  <p className="text-xl font-bold text-white">
                    {metric.value}{metric.suffix || ""}
                  </p>
                  {metric.target && (
                    <span className="text-xs text-slate-500">target {metric.target}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
