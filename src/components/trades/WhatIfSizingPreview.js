import { useState, useEffect, useRef } from "react";
import { api } from "../../api/base44Client";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Loader2, Sliders, AlertTriangle, ChevronDown, ChevronUp } from "lucide-react";
import { AMBER_MESSAGES, SYSTEM_MESSAGES } from "./PositionSizingWidget";

// ST-05 (BLG-FEAT-91, EPIC-02, v8.9) — Pre-commit "what-if" sizing/risk
// simulator on the trade-plan form.
// Design source: docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md
// Spec: docs/specs/frontend/pages/trade_plan.md §5d
//
// §13: display-only, advisory preview of a deterministic sizing calculation.
// No automated action, no write. Nothing here gates or modifies plan
// submission (§5d, design_record.md §3).
//
// Session-local storage key is deliberately distinct from
// PositionSizingWidget's own `widget_risk_percent` key (§5d.2 — "panel keeps
// its own to avoid cross-page coupling").
const SESSION_KEY = "what_if_preview_risk_percent";

export default function WhatIfSizingPreview({ ticker, market, stopLevel, fxRate, defaultRiskPercent }) {
  const [collapsed, setCollapsed] = useState(false);
  const [plannedEntryPrice, setPlannedEntryPrice] = useState("");
  const [riskPercent, setRiskPercent] = useState(() => {
    const stored = sessionStorage.getItem(SESSION_KEY);
    return stored !== null ? parseFloat(stored) : (defaultRiskPercent ?? 1.0);
  });
  const [sizingResult, setSizingResult] = useState(null);
  const [sizingLoading, setSizingLoading] = useState(false);

  useEffect(() => {
    sessionStorage.setItem(SESSION_KEY, String(riskPercent));
  }, [riskPercent]);

  useEffect(() => {
    if (defaultRiskPercent != null && sessionStorage.getItem(SESSION_KEY) === null) {
      setRiskPercent(defaultRiskPercent);
    }
  }, [defaultRiskPercent]);

  const parsedEntry = plannedEntryPrice === "" ? null : parseFloat(plannedEntryPrice);
  const parsedStop = stopLevel === "" || stopLevel == null ? null : parseFloat(stopLevel);
  // §5d.1: hidden entirely (no placeholder) until both inputs have valid positive values.
  const hasValidInputs = parsedEntry != null && parsedEntry > 0 && parsedStop != null && parsedStop > 0;

  // Debounced 300ms, matches PositionSizingWidget's existing debounce (§5d.3).
  useEffect(() => {
    if (!hasValidInputs) {
      setSizingResult(null);
      setSizingLoading(false);
      return;
    }

    setSizingLoading(true);

    const timer = setTimeout(async () => {
      try {
        const body = {
          entry_price: parsedEntry,
          stop_price: parsedStop,
          risk_percent: parseFloat(riskPercent) || 0,
          market,
        };
        if (market === "US" && fxRate) {
          body.fx_rate = fxRate;
        }
        if (ticker) {
          body.ticker = ticker;
        }

        const response = await api.portfolio.size(body);
        setSizingResult(response ?? null);
      } catch {
        setSizingResult(null);
      } finally {
        setSizingLoading(false);
      }
    }, 300);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [parsedEntry, parsedStop, market, fxRate, riskPercent, ticker, hasValidInputs]);

  const isValid = sizingResult?.valid;
  const suggestedShares = sizingResult?.suggested_shares;

  // §5d.3: "R at Risk" is derived client-side from the response's
  // suggested_shares and the known inputs — not a new backend field.
  const rAtRisk =
    isValid && suggestedShares != null && parsedEntry != null && parsedStop != null
      ? (parsedEntry - parsedStop) * suggestedShares
      : null;

  const heatImpact = isValid ? sizingResult?.heat_impact_percent : null;

  const getStatusMessage = () => {
    if (sizingLoading || !sizingResult) return null;
    if (isValid) return null;
    if (AMBER_MESSAGES[sizingResult.reason]) {
      return { type: "amber", text: AMBER_MESSAGES[sizingResult.reason] };
    }
    const msg = SYSTEM_MESSAGES[sizingResult.reason];
    return msg ? { type: "grey", text: msg } : null;
  };

  const status = getStatusMessage();

  // §5d.1 presence gate — implementation note: the spec's literal wording
  // ("hidden entirely until both Planned Entry Price and Stop Level have
  // valid positive values") is self-contradictory as written, since Planned
  // Entry Price is itself an input *inside* this panel (§5d.2) — a panel
  // hidden until its own field is filled can never be filled by normal use.
  // Resolved here by gating panel visibility on Stop Level alone (an
  // existing, external form field, §5.1/planned_stop_price) — once the
  // trader has set a stop, the panel appears with an empty Planned Entry
  // Price input; the *calculation/output* section (below) still only
  // renders once both inputs are valid, preserving the spec's intent that
  // no result is shown from a single input alone.
  const stopLevelValid = parsedStop != null && parsedStop > 0;
  if (!stopLevelValid) {
    return null;
  }

  return (
    <div
      data-testid="what-if-sizing-preview-panel"
      className="rounded-xl border border-slate-700/50 bg-slate-800/30 overflow-hidden"
    >
      <button
        type="button"
        data-testid="what-if-panel-toggle"
        className="w-full flex items-center justify-between px-4 py-3"
        onClick={() => setCollapsed((c) => !c)}
      >
        <div className="flex items-center gap-2">
          <Sliders className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-xs font-medium text-slate-300 uppercase tracking-wide">What-If Sizing Preview</span>
        </div>
        {collapsed ? <ChevronDown className="w-4 h-4 text-slate-500" /> : <ChevronUp className="w-4 h-4 text-slate-500" />}
      </button>

      {!collapsed && (
        <div className="px-4 pb-4 space-y-3 border-t border-slate-700/50 pt-3">
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <Label className="text-slate-600 dark:text-slate-400 text-xs">Planned Entry Price</Label>
              <Input
                type="number"
                step="0.01"
                data-testid="what-if-entry-price-input"
                value={plannedEntryPrice}
                onChange={(e) => setPlannedEntryPrice(e.target.value)}
                placeholder="e.g. 150.00"
                className="bg-slate-900/60 border-slate-700 text-white h-9 text-sm"
              />
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-600 dark:text-slate-400 text-xs">Risk %</Label>
              <Input
                type="number"
                step="0.01"
                min="0.01"
                max="100"
                data-testid="what-if-risk-percent-input"
                value={riskPercent}
                onChange={(e) => setRiskPercent(e.target.value)}
                className="bg-slate-900/60 border-slate-700 text-white h-9 text-sm"
              />
            </div>
          </div>

          {!hasValidInputs ? (
            <p className="text-slate-600 dark:text-slate-400 text-xs">
              {parsedStop == null || parsedStop <= 0
                ? "Set a Planned Stop Price above to preview sizing."
                : "Enter a valid planned entry price to preview sizing."}
            </p>
          ) : (
            <div className="space-y-2">
              <div className="grid grid-cols-3 gap-3">
                <div className="space-y-1">
                  <Label className="text-slate-600 dark:text-slate-400 text-xs">Suggested Size</Label>
                  <div className="text-sm font-medium text-white" data-testid="what-if-suggested-shares">
                    {sizingLoading ? (
                      <Loader2 className="w-4 h-4 text-slate-400 animate-spin" />
                    ) : isValid && suggestedShares != null ? (
                      `${suggestedShares} shares`
                    ) : (
                      "—"
                    )}
                  </div>
                </div>
                <div className="space-y-1">
                  <Label className="text-slate-600 dark:text-slate-400 text-xs">R at Risk</Label>
                  <div className="text-sm font-medium text-white" data-testid="what-if-r-at-risk">
                    {sizingLoading ? (
                      <Loader2 className="w-4 h-4 text-slate-400 animate-spin" />
                    ) : rAtRisk != null ? (
                      rAtRisk.toFixed(2)
                    ) : (
                      "—"
                    )}
                  </div>
                </div>
                <div className="space-y-1">
                  <Label className="text-slate-600 dark:text-slate-400 text-xs">Portfolio Heat Impact</Label>
                  <div className="text-sm font-medium text-white" data-testid="what-if-heat-impact">
                    {sizingLoading ? (
                      <Loader2 className="w-4 h-4 text-slate-400 animate-spin" />
                    ) : heatImpact != null ? (
                      `${heatImpact >= 0 ? "+" : ""}${heatImpact.toFixed(1)}% heat`
                    ) : (
                      "—"
                    )}
                  </div>
                </div>
              </div>

              {/* ST-04 (§10.7) concentration reason — same amber inline-note treatment. */}
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
            </div>
          )}

          <p className="text-slate-600 dark:text-slate-400 text-[11px]">
            Preview only — not saved with this plan.
          </p>
        </div>
      )}
    </div>
  );
}
