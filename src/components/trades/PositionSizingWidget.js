import { useState, useEffect, useRef } from "react";
import { base44 } from "../../api/base44Client";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Loader2, Ruler } from "lucide-react";
import { cn } from "../../lib/utils";

const SYSTEM_MESSAGES = {
  INVALID_ENTRY_PRICE: "Enter a valid entry price",
  INVALID_STOP_PRICE: "Enter a valid stop price",
  INVALID_STOP_DISTANCE: "Stop price must be below entry price",
  NO_PORTFOLIO_VALUE_SNAPSHOT: "Portfolio snapshot unavailable",
};

export default function PositionSizingWidget({
  entryPrice,
  stopPrice,
  market,
  fxRate,
  shares,
  onSharesChange,
  defaultRiskPercent,
}) {
  const [riskPercent, setRiskPercent] = useState(defaultRiskPercent ?? 1.0);
  const [sizingResult, setSizingResult] = useState(null);
  const [sizingLoading, setSizingLoading] = useState(false);
  const [usedSuggestion, setUsedSuggestion] = useState(false);

  // Use a ref to read current shares inside async timeout without stale closure
  const sharesRef = useRef(shares);
  useEffect(() => {
    sharesRef.current = shares;
  }, [shares]);

  // When settings load, initialize risk %
  useEffect(() => {
    if (defaultRiskPercent != null) {
      setRiskPercent(defaultRiskPercent);
    }
  }, [defaultRiskPercent]);

  // Debounced API call — fires 300ms after entryPrice, stopPrice, market, fxRate, or riskPercent change
  useEffect(() => {
    // Mark loading immediately so the user sees feedback
    setSizingLoading(true);

    const timer = setTimeout(async () => {
      if (!entryPrice || !stopPrice) {
        setSizingResult(null);
        setSizingLoading(false);
        return;
      }

      try {
        const body = {
          entry_price: entryPrice,
          stop_price: stopPrice,
          risk_percent: parseFloat(riskPercent) || 0,
          market,
        };
        if (market === "US" && fxRate) {
          body.fx_rate = fxRate;
        }

        const response = await base44.api.post("/portfolio/size", body);

        if (response?.status === "ok") {
          setSizingResult(response.data);
          setUsedSuggestion(false);

          // Auto-fill shares only when valid + cash sufficient + shares field is empty
          if (response.data?.valid && response.data?.cash_sufficient) {
            if (!sharesRef.current || sharesRef.current === "") {
              onSharesChange(String(response.data.suggested_shares));
            }
          }
        } else {
          setSizingResult(null);
        }
      } catch {
        setSizingResult(null);
      } finally {
        setSizingLoading(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [entryPrice, stopPrice, market, fxRate, riskPercent]);

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

    // Invalid
    if (sizingResult.reason === "INVALID_RISK_PERCENT") {
      return { type: "amber", text: "Risk % must be greater than 0" };
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
          <Label className="text-slate-400 text-xs">Risk %</Label>
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
          <Label className="text-slate-400 text-xs">Suggested Shares</Label>
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
                  (!isValid || !cashSufficient) && "text-slate-400",
                  isValid && !cashSufficient && "line-through"
                )}
              >
                {suggestedDisplay ?? "—"}
              </span>
            )}
          </div>
        </div>
      </div>

      {status?.type === "amber" && (
        <p className="text-amber-400 text-xs">{status.text}</p>
      )}
      {status?.type === "grey" && (
        <p className="text-slate-400 text-xs">{status.text}</p>
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
