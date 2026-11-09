import { useEffect } from "react";
import { Button } from "../ui/button";
import { Skeleton } from "../ui/skeleton";
import { useDebouncedSizing } from "../../hooks/usePositionSizingFetch";
import { AMBER_MESSAGES, SYSTEM_MESSAGES } from "./PositionSizingWidget";

/**
 * ST-08 (BLG-FE-256, EPIC-02, v9.16): trade_plan.md v1.22 §5f "Suggested Size
 * Before Shares". Shows the deterministic §4.1 size from POST /portfolio/size
 * (debounced 300 ms, settings default risk %, live FX for US plans — no
 * fx_rate is sent) once entry and stop are both valid positive numbers.
 * Advice only: it pre-fills an editable field and never saves or gates
 * anything (§13, as §10.6a).
 *
 * - onPrefill(shares): called with the floored suggestion on a valid,
 *   cash-sufficient result while `sharesTyped` is false.
 * - onUse(shares): the "Use suggested size" button, shown when `shares`
 *   differs from the suggestion.
 */
export default function PlanSuggestedSize({
  ticker,
  market,
  entryPrice,
  stopPrice,
  riskPercent,
  shares,
  sharesTyped,
  onPrefill,
  onUse,
}) {
  const entry = entryPrice === "" || entryPrice == null ? NaN : parseFloat(entryPrice);
  const stop = stopPrice === "" || stopPrice == null ? NaN : parseFloat(stopPrice);
  const hasValidInputs = entry > 0 && stop > 0;
  const risk = Number(riskPercent) || 0;

  const { sizingResult, sizingLoading } = useDebouncedSizing(
    () => hasValidInputs,
    () => {
      const body = { entry_price: entry, stop_price: stop, risk_percent: risk, market };
      if (ticker) body.ticker = ticker;
      return body;
    },
    [entry, stop, risk, market, ticker, hasValidInputs],
    { checkBeforeDebounce: true }
  );

  const isValid = !!sizingResult?.valid;
  const cashSufficient = !!sizingResult?.cash_sufficient;
  const suggested =
    isValid && sizingResult?.suggested_shares != null ? Math.floor(Number(sizingResult.suggested_shares)) : null;
  const usable = hasValidInputs && !sizingLoading && isValid && cashSufficient && suggested != null;

  useEffect(() => {
    if (usable && !sharesTyped && String(shares ?? "") !== String(suggested)) {
      onPrefill(String(suggested));
    }
  }, [usable, suggested, sharesTyped]); // eslint-disable-line react-hooks/exhaustive-deps

  // §5f: before both inputs are valid, no line and no placeholder.
  if (!hasValidInputs) return null;

  if (sizingLoading || !sizingResult) {
    return (
      <div data-testid="plan-suggested-size" aria-busy="true">
        <Skeleton data-testid="plan-suggested-size-loading" className="h-4 w-64 bg-slate-300/60 dark:bg-slate-700/60" />
      </div>
    );
  }

  if (!isValid) {
    const amber = AMBER_MESSAGES[sizingResult.reason];
    const grey = SYSTEM_MESSAGES[sizingResult.reason];
    if (!amber && !grey) return null;
    return (
      <p
        data-testid="plan-suggested-size"
        className={amber ? "text-xs text-amber-700 dark:text-amber-400" : "text-xs text-slate-600 dark:text-slate-400"}
      >
        {amber || grey}
      </p>
    );
  }

  if (!cashSufficient) {
    // Same cash-insufficient line as PositionSizingWidget (§10.6a/§10.7).
    return (
      <p data-testid="plan-suggested-size" className="text-xs text-slate-600 dark:text-slate-400">
        Max affordable: {Number(sizingResult.max_affordable_shares ?? 0).toFixed(4)} shares
      </p>
    );
  }

  const differs = String(shares ?? "") !== String(suggested);
  return (
    <div className="space-y-1">
      <p data-testid="plan-suggested-size" className="text-sm text-slate-800 dark:text-slate-200">
        Suggested size: {suggested} shares (§4.1, {risk}% risk)
      </p>
      {differs && (
        <Button
          type="button"
          variant="outline"
          size="sm"
          data-testid="plan-use-suggested-size"
          onClick={() => onUse(String(suggested))}
          className="h-7 text-xs border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300"
        >
          Use suggested size
        </Button>
      )}
    </div>
  );
}
