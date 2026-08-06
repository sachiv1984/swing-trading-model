/**
 * ComplianceRecheckModal — ST-01 (BLG-FEAT-64, v6.9)
 *
 * On-demand re-application of the 5 SI-01 pre-entry deterministic rule checks
 * against an open position's current state (current regime, current signal
 * conditions, current heat/sizing) — not its entry-time snapshot. Reuses the
 * pass/warn/fail visual pattern of PreEntryValidationPanel (src/pages/TradePlan.js).
 * Session-local only — no persisted state, no automation (§13).
 *
 * Spec: docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md
 *       docs/specs/frontend/pages/positions.md §Compliance Recheck Panel
 *
 * Migrated onto the shared Dialog primitive (ST-11, BLG-FE-103, EPIC-03, v8.3) —
 * was a bespoke fixed-overlay div; now uses Radix Dialog/DialogContent for its
 * built-in focus trap, Escape-to-close and (on unmount) focus restoration to the
 * previously-focused element, matching the ExitModal / TradePlan.js Abandon modal
 * convention (`open` + `onClose` controlled from the parent, content guarded on
 * `!position`). No explicit trigger ref is wired here — unlike TradePlan.js's
 * single-trigger Abandon modal, this modal is opened from more than one call site
 * (`Positions.js`'s own recheck button and a position-card callback), so it relies
 * on Radix's default previously-focused-element restoration rather than an
 * explicit `onCloseAutoFocus` override — same restoration objective, no single
 * trigger element to target.
 *
 * Padding/gap note: `DialogContent`'s own base className hardcodes `p-6 gap-4`
 * (`src/components/ui/dialog.js`) and this project's `cn()` (`src/lib/utils.js`)
 * is plain `clsx` with no `tailwind-merge` — a later override class does not
 * reliably beat an earlier base class in the compiled stylesheet. `!p-0 !gap-0`
 * (Tailwind's important-modifier prefix) is used instead of a bare `p-0 gap-0`
 * override so this component's own per-section padding (matching the original
 * bespoke layout) actually takes effect.
 */

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Zap, RotateCw } from "lucide-react";
import { Dialog, DialogContent, DialogTitle } from "../ui/dialog";
import { apiFetch } from "../../api/base44Client";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const RULE_LABELS = {
  regime_gate: "Regime Gate",
  cash_constraint: "Cash Constraint",
  sector_concentration: "Sector Concentration",
  earnings_proximity: "Earnings Proximity",
  sizing_validity: "Sizing Validity",
};

const STATUS_ICON = { pass: "✓", warn: "⚠", fail: "✗", skipped: "—" };
const STATUS_COLOR = {
  pass: "text-emerald-400",
  warn: "text-amber-400",
  fail: "text-red-400",
  skipped: "text-slate-600 dark:text-slate-400",
};
const OVERALL_BADGE = {
  pass: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  warn: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  fail: "bg-red-500/20 text-red-400 border-red-500/30",
};
const OVERALL_LABEL = { pass: "Pass", warn: "Warn", fail: "Fail" };

export default function ComplianceRecheckModal({ position, open, onClose }) {
  const [overrideAcknowledged, setOverrideAcknowledged] = useState(false);

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["compliance-recheck", position?.id],
    queryFn: async () => {
      const r = await apiFetch(`${API_BASE}/positions/${position.id}/compliance-recheck`);
      if (!r.ok) throw new Error("Compliance recheck failed");
      const j = await r.json();
      return j.data;
    },
    enabled: !!position?.id,
  });

  const overallStatus = data?.overall_status;
  const checks = data?.checks || [];
  const hasWarnOrFail = overallStatus === "warn" || overallStatus === "fail";
  const allPassed = overallStatus === "pass";

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent
        className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-700 !p-0 !gap-0"
        data-testid="compliance-recheck-modal"
      >
        {!position ? null : (
          <>
            {/* Header */}
            <div className="flex items-center gap-2 px-5 py-4 border-b border-slate-700/50">
              <Zap className="w-4 h-4 text-cyan-400" />
              <DialogTitle className="!text-sm font-semibold text-white !leading-normal !tracking-wide uppercase">
                Compliance Recheck — {position.ticker}
              </DialogTitle>
              {overallStatus && (
                <span
                  data-testid="compliance-recheck-overall-badge"
                  className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${OVERALL_BADGE[overallStatus] || OVERALL_BADGE.warn}`}
                >
                  {OVERALL_LABEL[overallStatus] || overallStatus}
                </span>
              )}
            </div>

            {/* Context line */}
            <p className="px-5 pt-3 text-xs text-slate-600 dark:text-slate-400">
              Checked against current conditions, not entry-time.
            </p>

            {/* Body */}
            <div className="px-5 py-4 space-y-3">
              {isLoading && (
                <div className="flex items-center justify-center py-6" data-testid="compliance-recheck-loading">
                  <RotateCw className="w-5 h-5 text-slate-500 animate-spin" />
                </div>
              )}

              {!isLoading && isError && (
                <div className="text-center py-4 space-y-3" data-testid="compliance-recheck-error">
                  <p className="text-sm text-rose-400">Recheck unavailable — try again</p>
                  <button
                    onClick={() => refetch()}
                    className="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700"
                  >
                    Retry
                  </button>
                </div>
              )}

              {!isLoading && !isError && checks.map((check) => (
                <div key={check.rule_key} className="flex items-start gap-2 text-sm" data-testid={`compliance-check-${check.rule_key}`}>
                  <span className={`mt-0.5 font-mono w-4 shrink-0 ${STATUS_COLOR[check.status] || "text-slate-600 dark:text-slate-400"}`}>
                    {STATUS_ICON[check.status] || "?"}
                  </span>
                  <div className="flex-1 min-w-0">
                    <span className="text-slate-200">{RULE_LABELS[check.rule_key] || check.rule_key}</span>
                    {check.detail && (
                      <span className="text-slate-600 dark:text-slate-400"> — {check.detail}</span>
                    )}
                  </div>
                </div>
              ))}

              {!isLoading && !isError && hasWarnOrFail && (
                <label className="flex items-center gap-2 mt-4 pt-3 border-t border-slate-700/50 cursor-pointer">
                  <input
                    type="checkbox"
                    data-testid="compliance-recheck-override-checkbox"
                    checked={overrideAcknowledged}
                    onChange={(e) => setOverrideAcknowledged(e.target.checked)}
                    className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500/30"
                  />
                  <span className="text-xs text-amber-400">I acknowledge the advisory result</span>
                </label>
              )}

              {!isLoading && !isError && allPassed && (
                <p
                  data-testid="compliance-recheck-all-pass-note"
                  className="mt-4 pt-3 border-t border-slate-700/50 text-xs text-emerald-400"
                >
                  All 5 checks passed — no action needed.
                </p>
              )}
            </div>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}
