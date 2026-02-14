import { Lightbulb } from "lucide-react";

export default function KeyInsightsCard({ metrics, winRate }) {
  const insights = [];

  // 1. Sharpe Ratio assessment
  if (metrics.sharpeRatio !== undefined) {
    if (metrics.sharpeRatio > 2) {
      insights.push(`Excellent risk-adjusted returns with a Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)}`);
    } else if (metrics.sharpeRatio > 1) {
      insights.push(`Strong risk-adjusted returns with a Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)}`);
    } else if (metrics.sharpeRatio > 0.5) {
      insights.push(`Decent risk-adjusted returns with a Sharpe ratio of ${metrics.sharpeRatio.toFixed(2)}`);
    } else {
      insights.push(`Risk-adjusted returns need improvement (Sharpe: ${metrics.sharpeRatio.toFixed(2)})`);
    }
  }

  // 2. Hold time comparison
  if (metrics.avgHoldWinners > 0 && metrics.avgHoldLosers > 0) {
    if (metrics.avgHoldWinners > metrics.avgHoldLosers) {
      insights.push(`✅ Great discipline - cutting losers faster (${metrics.avgHoldLosers.toFixed(1)} days) than letting winners run (${metrics.avgHoldWinners.toFixed(1)} days)`);
    } else {
      insights.push(`⚠️ Holding losers too long (${metrics.avgHoldLosers.toFixed(1)} days) compared to winners (${metrics.avgHoldWinners.toFixed(1)} days) - consider tighter stops`);
    }
  }

  // 3. Profit factor assessment
  if (metrics.profitFactor > 0) {
    if (metrics.profitFactor > 2) {
      insights.push(`Excellent profit factor of ${metrics.profitFactor.toFixed(2)} means earning £${metrics.profitFactor.toFixed(2)} for every £1 lost`);
    } else if (metrics.profitFactor > 1.5) {
      insights.push(`Solid profit factor of ${metrics.profitFactor.toFixed(2)} - earning £${metrics.profitFactor.toFixed(2)} for every £1 lost`);
    } else {
      insights.push(`Profit factor of ${metrics.profitFactor.toFixed(2)} needs improvement - currently earning £${metrics.profitFactor.toFixed(2)} per £1 lost`);
    }
  }

  // 4. Expectancy insight
  if (metrics.expectancy !== undefined) {
    if (metrics.expectancy > 50) {
      insights.push(`Strong positive edge - expecting £${metrics.expectancy.toFixed(2)} profit per trade`);
    } else if (metrics.expectancy > 0) {
      insights.push(`Positive expectancy of £${metrics.expectancy.toFixed(2)} per trade means your strategy has an edge`);
    } else {
      insights.push(`Negative expectancy (£${metrics.expectancy.toFixed(2)} per trade) suggests strategy refinement needed`);
    }
  }

  // 5. Risk/Reward insight
  if (metrics.riskRewardRatio > 0) {
    if (metrics.riskRewardRatio > 2) {
      insights.push(`Strong risk/reward ratio of ${metrics.riskRewardRatio.toFixed(2)}:1 - average wins are ${metrics.riskRewardRatio.toFixed(1)}x larger than losses`);
    } else if (metrics.riskRewardRatio > 1) {
      insights.push(`Positive risk/reward ratio of ${metrics.riskRewardRatio.toFixed(2)}:1`);
    } else {
      insights.push(`Risk/reward ratio of ${metrics.riskRewardRatio.toFixed(2)}:1 is below ideal (target > 2:1)`);
    }
  }

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-br from-amber-500 to-orange-500">
          <Lightbulb className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-lg font-semibold text-white">Key Insights</h3>
      </div>
      <div className="space-y-3">
        {insights.slice(0, 5).map((insight, idx) => (
          <div key={idx} className="flex gap-3">
            <div className="flex-shrink-0 w-1.5 h-1.5 rounded-full bg-amber-400 mt-2" />
            <p className="text-sm text-slate-300 leading-relaxed">{insight}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
