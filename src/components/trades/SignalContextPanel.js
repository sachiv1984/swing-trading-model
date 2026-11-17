'use strict';

import { TrendingUp, BarChart2 } from "lucide-react";
import { cn } from "../../lib/utils";
import { formatCurrency, formatPercent, currencyForMarket } from "../../lib/format";
import { INITIAL_ATR_MULTIPLIER, ATR_PERIOD_DAYS } from "../../constants/strategy";

const toNumber = (v) => (v == null || v === "" ? null : Number.isFinite(Number(v)) ? Number(v) : null);

/**
 * The signal's ATR in the signal's own (native) currency.
 *
 * GET /signals stores `atr_value` in GBP for both markets (signal_service.py:
 * `atr_gbp = native_atr / live_fx_rate` for US), while `current_price` and
 * `initial_stop` are native (USD for US). So:
 * - When `initial_stop` is present (both markets): derived from the native stop the
 *   signal was built with, `(current_price − initial_stop) / INITIAL_ATR_MULTIPLIER`.
 *   This also matches the stop exactly at the signal's price, where mixing the 4 dp
 *   `atr_value` with the 2 dp price would not (UK rounding).
 * - Otherwise UK `atr_value` (already in pounds); otherwise null. The GBP
 *   `atr_value` is never used against a USD price.
 * ST-14 follow-up (PR #2260 review P2 and re-review; BLG-FE-296), v9.17.
 */
export function getSignalAtr(signal) {
  if (!signal) return null;
  const price = toNumber(signal.current_price);
  const initialStop = toNumber(signal.initial_stop);
  if (price != null && initialStop != null && price > initialStop) {
    return (price - initialStop) / INITIAL_ATR_MULTIPLIER;
  }
  if (signal.market === "UK") {
    const atr = toNumber(signal.atr_value);
    return atr != null && atr > 0 ? atr : null;
  }
  return null;
}

/**
 * The signal's suggested stop, as the panel shows it (trade_plan.md §5a.3):
 * the signal's initial_stop when present, otherwise
 * current_price − INITIAL_ATR_MULTIPLIER × the signal's native ATR (getSignalAtr);
 * null when neither is known.
 * ST-14 (BLG-FE-282, v9.17): shared with the Trade Plan form's Stop pre-fill so the
 * two cannot disagree.
 */
export function getSuggestedStop(signal) {
  if (!signal) return null;
  const initialStop = toNumber(signal.initial_stop);
  if (initialStop != null) return initialStop;
  const price = toNumber(signal.current_price);
  const atr = getSignalAtr(signal);
  return price != null && atr != null ? price - INITIAL_ATR_MULTIPLIER * atr : null;
}

/**
 * Read-only Signal Context Panel shown in trade plan creation form (§5a, trade_plan.md v0.5).
 * Shown only when a linked watchlisted signal exists for the plan ticker.
 * §13 compliant: display-only, no automated entry.
 */
export default function SignalContextPanel({ signal, market }) {
  if (!signal) return null;

  const panelCurrency = currencyForMarket(market || signal.market);

  const suggestedStop = getSuggestedStop(signal);
  const signalAtr = getSignalAtr(signal);

  const maPercent = signal.price_vs_50d_ma ?? null;
  const showMA = maPercent != null;

  const regimeOn = signal.regime === "on" || signal.regime === true;

  return (
    <div
      className="rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60 p-4 space-y-3"
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
          <p className="text-sm font-semibold text-app-fg">#{signal.rank}</p>
        </div>

        <div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Momentum</p>
          <p className={cn(
            "text-sm font-semibold flex items-center gap-1",
            signal.momentum_percent >= 0 ? "text-app-positive" : "text-red-700 dark:text-red-400"
          )}>
            <TrendingUp className="w-3.5 h-3.5" />
            {formatPercent(signal.momentum_percent, { signed: true })}
          </p>
        </div>

        {showMA && (
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">vs 200-day MA</p>
            <p className={cn(
              "text-sm font-semibold",
              maPercent >= 0 ? "text-app-positive" : "text-app-warning"
            )}>
              {formatPercent(Math.abs(maPercent))} {maPercent >= 0 ? "above" : "below"}
            </p>
          </div>
        )}

        {signal.regime != null && (
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Regime</p>
            <span className={cn(
              "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium",
              regimeOn
                ? "bg-emerald-500/20 text-emerald-800 dark:text-emerald-400 border border-emerald-500/40"
                : "bg-amber-500/20 text-amber-800 dark:text-amber-400 border border-amber-500/40"
            )}>
              {regimeOn ? "On" : "Off"}
            </span>
          </div>
        )}

        {signalAtr != null && (
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">ATR ({ATR_PERIOD_DAYS}d)</p>
            <p className="text-sm font-semibold text-app-fg" data-testid="signal-context-atr">
              {formatCurrency(signalAtr, { currency: panelCurrency })}
            </p>
          </div>
        )}

        {suggestedStop != null && (
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Suggested stop</p>
            <p className="text-sm font-semibold text-app-negative">
              {formatCurrency(suggestedStop, { currency: panelCurrency })}
            </p>
            <p className="text-xs text-app-muted">entry − {INITIAL_ATR_MULTIPLIER}×ATR</p>
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
    maPart = ` Price ${direction} 200-day MA by ${formatPercent(Math.abs(maPercent))}.`;
  }

  const momentumPart = signal.momentum_percent != null
    ? ` ${formatPercent(signal.momentum_percent, { signed: true })} momentum.`
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
