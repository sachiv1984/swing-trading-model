'use strict';

import { TrendingUp, BarChart2 } from "lucide-react";
import { cn } from "../../lib/utils";

/**
 * Read-only Signal Context Panel shown in trade plan creation form (§5a, trade_plan.md v0.5).
 * Shown only when a linked watchlisted signal exists for the plan ticker.
 * §13 compliant: display-only, no automated entry.
 */
export default function SignalContextPanel({ signal, market }) {
  if (!signal) return null;

  const isUS = (market || signal.market) === "US";
  const currencySymbol = isUS ? "$" : "£";

  const suggestedStop = signal.initial_stop != null
    ? signal.initial_stop
    : signal.current_price != null && signal.atr_value != null
      ? signal.current_price - 5 * signal.atr_value
      : null;

  const maPercent = signal.price_vs_50d_ma ?? null;
  const showMA = maPercent != null;

  const regimeOn = signal.regime === "on" || signal.regime === true;

  return (
    <div
      className="rounded-xl bg-slate-800/40 border border-slate-700/60 p-4 space-y-3"
      data-testid="signal-context-panel"
      aria-label="Signal Context"
    >
      <h3 className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide flex items-center gap-2">
        <BarChart2 className="w-3.5 h-3.5" />
        Signal Context
      </h3>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        <div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Rank</p>
          <p className="text-sm font-semibold text-white">#{signal.rank}</p>
        </div>

        <div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Momentum</p>
          <p className={cn(
            "text-sm font-semibold flex items-center gap-1",
            signal.momentum_percent >= 0 ? "text-emerald-400" : "text-red-400"
          )}>
            <TrendingUp className="w-3.5 h-3.5" />
            {signal.momentum_percent >= 0 ? "+" : ""}{signal.momentum_percent?.toFixed(1)}%
          </p>
        </div>

        {showMA && (
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">vs 200-day MA</p>
            <p className={cn(
              "text-sm font-semibold",
              maPercent >= 0 ? "text-emerald-400" : "text-amber-400"
            )}>
              {Math.abs(maPercent).toFixed(1)}% {maPercent >= 0 ? "above" : "below"}
            </p>
          </div>
        )}

        {signal.regime != null && (
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Regime</p>
            <span className={cn(
              "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium",
              regimeOn
                ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                : "bg-amber-500/20 text-amber-400 border border-amber-500/40"
            )}>
              {regimeOn ? "On" : "Off"}
            </span>
          </div>
        )}

        {signal.atr_value != null && (
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">ATR (14d)</p>
            <p className="text-sm font-semibold text-white">
              {currencySymbol}{signal.atr_value.toFixed(2)}
            </p>
          </div>
        )}

        {suggestedStop != null && (
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Suggested stop</p>
            <p className="text-sm font-semibold text-rose-400">
              {currencySymbol}{suggestedStop.toFixed(2)}
            </p>
            <p className="text-xs text-slate-600">entry − 5×ATR</p>
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Builds the pre-population strings for the trade plan form based on signal data.
 * Returns { entryRationale, confirmationCriteria } — both user-editable.
 */
export function buildSignalPrePopulation(signal, market) {
  const marketLabel = (market || signal.market) === "US" ? "US" : "UK";
  const maPercent = signal.price_vs_50d_ma ?? null;

  let maPart = "";
  if (maPercent != null) {
    const direction = maPercent >= 0 ? "above" : "below";
    maPart = ` Price ${direction} 200-day MA by ${Math.abs(maPercent).toFixed(1)}%.`;
  }

  const momentumPart = signal.momentum_percent != null
    ? ` ${signal.momentum_percent >= 0 ? "+" : ""}${signal.momentum_percent.toFixed(1)}% momentum.`
    : "";

  const regimeLabel = signal.regime === "on" || signal.regime === true ? "on" : "off";

  const setupThesis =
    `Rank ${signal.rank} ${marketLabel} momentum candidate.${momentumPart}${maPart} Regime ${regimeLabel}.`;

  const entryRationale =
    `Rank ${signal.rank} momentum signal.${maPart} ${marketLabel} regime on.`;

  const confirmationCriteria =
    "Price above 200-day MA at entry. Regime on. Spare cash available.";

  return { setupThesis, entryRationale, confirmationCriteria };
}
