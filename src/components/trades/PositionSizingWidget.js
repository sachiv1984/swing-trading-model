import { useState, useEffect, useRef } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Loader2, Ruler, AlertTriangle } from "lucide-react";
import { cn } from "../../lib/utils";
import { useSessionRiskPercent, useDebouncedSizing } from "../../hooks/usePositionSizingFetch";

// ST-05 (BLG-FEAT-91): exported for reuse verbatim by WhatIfSizingPreview.js
// (trade_plan.md §5d.3 — "same AMBER_MESSAGES / SYSTEM_MESSAGES conventions
// as §10.7"), rather than a second, potentially-drifting copy.
export const SYSTEM_MESSAGES = {
  INVALID_STOP_DISTANCE: "Stop price must be below entry price",
  NO_PORTFOLIO_VALUE_SNAPSHOT: "Portfolio snapshot unavailable",
};

// DEF-002 / DEF-003 fix: user input invalid conditions render amber, not grey
export const AMBER_MESSAGES = {
  INVALID_RISK_PERCENT: "Risk % must be greater than 0",
  INVALID_ENTRY_PRICE: "Enter a valid entry price above zero",
  INVALID_STOP_PRICE: "Enter a valid stop price above zero",
};

// DEF-006 fix: persist Risk % across navigation using sessionStorage.
// On mount, reads the last-used session value first. Falls back to
// defaultRiskPercent (from settings) only when no session value exists.
// Cleared automatically when the browser tab is closed.
// ST-06 (v9.1, BLG-TECH-14): session-persistence + debounced-fetch
// boilerplate shared with WhatIfSizingPreview.js via usePositionSizingFetch.js.
const SESSION_KEY = "widget_risk_percent";

export default function PositionSizingWidget({
  entryPrice,
  stopPrice,
  market,
  fxRate,
  shares,
  onSharesChange,
  defaultRiskPercent,
  ticker,
}) {
  const [riskPercent, setRiskPercent] = useSessionRiskPercent(SESSION_KEY, defaultRiskPercent);
  const [usedSuggestion, setUsedSuggestion] = useState(false);

  // Use a ref to read current shares inside async timeout without stale closure
  const sharesRef = useRef(shares);
  useEffect(() => {
    sharesRef.current = shares;
  }, [shares]);

  // Debounced API call — fires 300ms after entryPrice, stopPrice, market, fxRate, or riskPercent change
  const { sizingResult, sizingLoading } = useDebouncedSizing(
    () => !(entryPrice === "" || entryPrice == null || stopPrice === "" || stopPrice == null),
    () => {
      const body = {
        entry_price: entryPrice,
        stop_price: stopPrice,
        risk_percent: parseFloat(riskPercent) || 0,
        market,
      };
      if (market === "US" && fxRate) {
        body.fx_rate = fxRate;
      }
      // ST-04 (BLG-BE-104): pass ticker to enable concentration-aware sizing
      if (ticker) {
        body.ticker = ticker;
      }
      return body;
    },
    [entryPrice, stopPrice, market, fxRate, riskPercent, ticker],
    {
      onResult: (response) => {
        setUsedSuggestion(false);
        // Auto-fill shares only when valid + cash sufficient + shares field is empty
        if (response.valid && response.cash_sufficient) {
          if (!sharesRef.current || sharesRef.current === "") {
            onSharesChange(String(response.suggested_shares));
          }
        }
      },
    }
  );

  const handleUseSuggested = () => {
    if (sizingResult?.suggested_shares != null) {
      onSharesChange(String(sizingResult.suggested_shares));
      setUsedSuggestion(true);
    }
  };

  // Derived display values
  const isValid = sizingResult?.valid;
  const cashSufficient = sizingResult?.cash_sufficient;
  const suggestedShares = sizingResult?.suggested_shares;

  const getSuggestedDisplay = () => {
    if (sizingLoading) return null;
    if (!isValid || suggestedShares == null) return "—";
    return suggestedShares.toFixed(4);
  };

  const getStatus = () => {
    if (sizingLoading || !sizingResult) return null;

    if (isValid) {
      if (!cashSufficient) {
        return {
          type: "grey",
          text: `Max affordable: ${sizingResult.max_affordable_shares?.toFixed(4)} shares`,
        };
      }
      // Valid + sufficient cash + shares already filled + user hasn't clicked "use"
      if (shares && shares !== "" && !usedSuggestion) {
        return { type: "button" };
      }
      return null;
    }

    // Invalid — user input conditions (amber) take priority over system conditions (grey)
    if (AMBER_MESSAGES[sizingResult.reason]) {
      return { type: "amber", text: AMBER_MESSAGES[sizingResult.reason] };
    }
    const msg = SYSTEM_MESSAGES[sizingResult.reason];
    return msg ? { type: "grey", text: msg } : null;
  };

  const suggestedDisplay = getSuggestedDisplay();
  const status = getStatus();

  return (
    <div className="rounded-xl bg-slate-800/50 border border-slate-700/50 p-4 space-y-3">
      <div className="flex items-center gap-2">
        <Ruler className="w-4 h-4 text-slate-400" />
        <span className="text-sm font-medium text-slate-300">Position Sizing</span>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-1.5">
          <Label className="text-slate-600 dark:text-slate-400 text-xs">Risk %</Label>
          <Input
            type="number"
            step="0.01"
            min="0.01"
            max="100"
            value={riskPercent}
            onChange={(e) => setRiskPercent(e.target.value)}
            className="bg-slate-900/60 border-slate-700 text-white h-9 text-sm"
          />
        </div>
        <div className="space-y-1.5">
          <Label className="text-slate-600 dark:text-slate-400 text-xs">Suggested Shares</Label>
          <div
            className={cn(
              "h-9 px-3 rounded-md border bg-slate-900/60 border-slate-700 flex items-center",
              isValid && !cashSufficient && "opacity-60"
            )}
          >
            {sizingLoading ? (
              <Loader2 className="w-4 h-4 text-slate-400 animate-spin" />
            ) : (
              <span
                className={cn(
                  "text-sm font-medium",
                  isValid && cashSufficient && "text-cyan-400",
                  (!isValid || !cashSufficient) && "text-slate-600 dark:text-slate-400",
                  isValid && !cashSufficient && "line-through"
                )}
              >
                {suggestedDisplay ?? "—"}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* ST-04 (BLG-BE-104): concentration reason — re-evaluates on every debounced
          recalculation, no dismiss affordance (design_record.md §2) */}
      {isValid && sizingResult?.concentration_reason && (
        <p className="flex items-start gap-1.5 text-amber-600 dark:text-amber-400 text-xs">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
          <span>{sizingResult.concentration_reason}</span>
        </p>
      )}

      {status?.type === "amber" && (
        <p className="text-amber-400 text-xs">{status.text}</p>
      )}
      {status?.type === "grey" && (
        <p className="text-slate-600 dark:text-slate-400 text-xs">{status.text}</p>
      )}
      {status?.type === "button" && (
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={handleUseSuggested}
          className="w-full bg-slate-700/50 border-slate-600 text-slate-300 hover:bg-slate-700 hover:text-white text-xs h-8"
        >
          Use suggested shares
        </Button>
      )}
    </div>
  );
}
