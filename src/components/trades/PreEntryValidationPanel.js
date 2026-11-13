import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { ShieldCheck, ChevronDown, ChevronUp } from "lucide-react";
import { apiFetch } from "../../api/base44Client";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const RULE_LABELS = {
  regime_gate: "Regime Gate",
  cash_constraint: "Cash Constraint",
  sector_concentration: "Sector Concentration",
  earnings_proximity: "Earnings Proximity",
  sizing_validity: "Sizing Validity",
};

const STATUS_ICON = { pass: "✓", warn: "⚠", fail: "✗", skipped: "—" };
const STATUS_COLOR = {
  pass: "text-emerald-700 dark:text-emerald-400",
  warn: "text-amber-700 dark:text-amber-400",
  fail: "text-red-700 dark:text-red-400",
  skipped: "text-slate-600 dark:text-slate-400",
};
const ADVISORY_BADGE = {
  pass: "bg-emerald-500/20 text-emerald-800 dark:text-emerald-400 border-emerald-500/30",
  warn: "bg-amber-500/20 text-amber-800 dark:text-amber-400 border-amber-500/30",
  fail: "bg-red-500/20 text-red-800 dark:text-red-400 border-red-500/30",
};

/**
 * strategy_rules.md §4.2 pre-entry checks (GET /portfolio/pre-entry-validation).
 * Shared by the Trade Plan form (trade_plan.md) and Trade Entry
 * (position_form.md v1.13 §Pre-Entry Checks, ST-01, BLG-FE-244, v9.15).
 *
 * - showWaiting: render the header with "Enter shares to run the pre-entry
 *   checks." while no quantity is entered (Trade Entry). Without it the panel
 *   renders nothing until a quantity exists (Trade Plan, unchanged).
 * - onWarningsChange(bool): called with true while a WARN/FAIL result needs
 *   acknowledging. An endpoint failure or a pending request reports false, so
 *   it never disables a caller's Submit.
 * - onResultChange(snapshot | null): called with the dated result the panel
 *   holds, shaped as trade_plan.md v1.22 §5e's pre_entry_validation_snapshot
 *   ({captured_at, advisory_status, checks, inputs}), or null while there is no
 *   result (no shares, loading, or endpoint error). ST-05, BLG-FE-271, v9.16.
 * - showAcknowledgementResetNote: render trade_plan.md v1.25 §5e's reset note
 *   under the acknowledgement box. The caller decides when (ST-12, BLG-FE-278,
 *   v9.17: the Trade Plan form only; Trade Entry does not pass it).
 */
export default function PreEntryValidationPanel({
  ticker,
  market,
  quantity,
  entryPrice,
  stopPrice,
  overrideAcknowledged,
  onOverrideChange,
  showWaiting = false,
  onWarningsChange,
  onResultChange,
  showAcknowledgementResetNote = false,
}) {
  const [collapsed, setCollapsed] = useState(false);
  const hasInputs = !!ticker && !!quantity && Number(quantity) > 0;

  const { data, isLoading, isError, dataUpdatedAt } = useQuery({
    queryKey: ["pre-entry-validation", ticker, market, quantity, entryPrice, stopPrice],
    queryFn: async () => {
      const paramObj = { ticker, quantity, market };
      const ep = parseFloat(entryPrice);
      const sp = parseFloat(stopPrice);
      if (!isNaN(ep) && ep > 0) paramObj.entry_price = ep;
      if (!isNaN(sp) && sp > 0) paramObj.stop_price = sp;
      const params = new URLSearchParams(paramObj);
      const r = await apiFetch(`${API_BASE}/portfolio/pre-entry-validation?${params}`);
      const j = await r.json();
      return j.data;
    },
    enabled: hasInputs,
    staleTime: 60000,
  });

  const checks = hasInputs && !isError ? data?.checks || [] : [];
  const hasWarnings = checks.some((c) => c.status === "warn" || c.status === "fail");

  useEffect(() => {
    if (onWarningsChange) onWarningsChange(hasInputs && !isLoading && !isError && hasWarnings);
  }, [onWarningsChange, hasInputs, isLoading, isError, hasWarnings]);

  // ST-05 (BLG-FE-271, v9.16): the dated snapshot the Trade Plan form saves.
  // captured_at is when this result was received (trade_plan.md §5e).
  const hasResult = hasInputs && !isLoading && !isError && !!data?.advisory_status;
  useEffect(() => {
    if (!onResultChange) return;
    if (!hasResult) {
      onResultChange(null);
      return;
    }
    const num = (v) => {
      const n = parseFloat(v);
      return isNaN(n) ? null : n;
    };
    onResultChange({
      captured_at: new Date(dataUpdatedAt || Date.now()).toISOString(),
      advisory_status: data.advisory_status,
      checks: (data.checks || []).map((c) => ({ rule: c.rule, status: c.status, detail: c.detail ?? null })),
      inputs: { quantity: num(quantity), entry_price: num(entryPrice), stop_price: num(stopPrice) },
    });
  }, [onResultChange, hasResult, data, dataUpdatedAt, quantity, entryPrice, stopPrice]);

  if (!hasInputs && !showWaiting) return null;

  const advisory = hasInputs ? data?.advisory_status : null;
  const warnCount = checks.filter((c) => c.status === "warn").length;
  const failCount = checks.filter((c) => c.status === "fail").length;

  return (
    <div data-testid="pre-entry-checks-panel" className="rounded-xl border border-slate-200 dark:border-slate-700/50 bg-slate-100 dark:bg-slate-800/30 overflow-hidden">
      <button
        type="button"
        data-testid="pre-entry-panel-toggle"
        className="w-full flex items-center justify-between px-4 py-3"
        onClick={() => setCollapsed((c) => !c)}
      >
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-3.5 h-3.5 text-slate-600 dark:text-slate-400" />
          <span className="text-xs font-medium text-slate-700 dark:text-slate-300 uppercase tracking-wide">Pre-Entry Checks</span>
          {advisory && (
            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${ADVISORY_BADGE[advisory] || ADVISORY_BADGE.warn}`}>
              {advisory === "pass" ? "Pass" : advisory === "warn" ? "Warn" : "Fail"}
            </span>
          )}
          {collapsed && (advisory === "warn" || advisory === "fail") && (
            <span data-testid="pre-entry-issue-count" className="text-xs text-slate-600 dark:text-slate-400">
              {[failCount > 0 && `${failCount} fail`, warnCount > 0 && `${warnCount} warn`].filter(Boolean).join(", ")}
            </span>
          )}
          {hasInputs && isLoading && <span className="text-xs text-slate-600 dark:text-slate-400">Checking…</span>}
        </div>
        {collapsed ? <ChevronDown className="w-4 h-4 text-slate-500" /> : <ChevronUp className="w-4 h-4 text-slate-500" />}
      </button>
      {!hasInputs && (
        <p data-testid="pre-entry-checks-waiting" className="px-4 pb-3 text-xs text-slate-600 dark:text-slate-400">
          Enter shares to run the pre-entry checks.
        </p>
      )}
      {hasInputs && !collapsed && (
        <div className="px-4 pb-4 space-y-2 border-t border-slate-200 dark:border-slate-700/50 pt-3">
          {isError && <p className="text-xs text-slate-600 dark:text-slate-400">Validation unavailable — proceed with manual checks</p>}
          {!isLoading && !isError && checks.length === 0 && (
            <p className="text-xs text-slate-600 dark:text-slate-400">No checks available</p>
          )}
          {!isLoading && !isError && checks.map((check) => (
            <div key={check.rule} data-testid={`pre-entry-check-${check.rule}`} data-status={check.status} className="flex items-start gap-2 text-xs">
              <span className={`mt-0.5 font-mono w-3 shrink-0 ${STATUS_COLOR[check.status] || "text-slate-600 dark:text-slate-400"}`}>
                {STATUS_ICON[check.status] || "?"}
              </span>
              <div className="flex-1 min-w-0">
                <span className="text-slate-700 dark:text-slate-300">{RULE_LABELS[check.rule] || check.rule}</span>
                {check.detail && (
                  <span className="text-slate-600 dark:text-slate-400"> — {check.detail}</span>
                )}
              </div>
            </div>
          ))}
          {hasWarnings && (
            <label className="flex items-center gap-2 mt-3 cursor-pointer">
              <input
                type="checkbox"
                data-testid="override-acknowledgement-checkbox"
                checked={overrideAcknowledged || false}
                onChange={(e) => onOverrideChange(e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 dark:border-slate-600 bg-slate-100 dark:bg-slate-800 text-amber-500 focus:ring-amber-500/30"
              />
              <span className="text-xs text-amber-700 dark:text-amber-400">I acknowledge the advisory warnings</span>
            </label>
          )}
          {hasWarnings && showAcknowledgementResetNote && !overrideAcknowledged && (
            <p data-testid="acknowledgement-reset-note" className="text-xs text-app-warning">
              The check results changed. Review them and tick again to acknowledge.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
