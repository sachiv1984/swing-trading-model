/**
 * StandingAlert — shared "standing alert" primitive, distinct from transient
 * toast notifications (ST-04, EPIC-04, v7.7, BLG-FE-120).
 *
 * Design source: docs/design/2026-07-21__release-v7.7/standing-alert-component/ux_spec.md
 * Documented: docs/specs/frontend/design_system.md v1.3 §Shared UI Components → Standing Alert
 *
 * Distinction from toast (sonner): manual/programmatic dismissal only (no
 * auto-dismiss timer), inline banner in document flow (not a floating
 * corner-anchored overlay), parent-owned array (not a global store).
 */
import { X, Info, AlertTriangle, AlertOctagon } from "lucide-react";
import { cn } from "../../lib/utils";

const SEVERITY_CONFIG = {
  info: {
    Icon: Info,
    className: "bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-950 dark:border-blue-800 dark:text-blue-200",
  },
  warning: {
    Icon: AlertTriangle,
    className: "bg-amber-50 border-amber-200 text-amber-800 dark:bg-amber-950 dark:border-amber-800 dark:text-amber-200",
  },
  critical: {
    Icon: AlertOctagon,
    className: "bg-red-50 border-red-200 text-red-800 dark:bg-red-950 dark:border-red-800 dark:text-red-200",
  },
};

/**
 * Single standing alert banner. Full-width, in document flow (not overlaid).
 * Manual dismissal only — no auto-dismiss timer.
 */
export function StandingAlert({ id, severity = "info", message, actionLabel, onAction, onDismiss, className }) {
  const config = SEVERITY_CONFIG[severity] || SEVERITY_CONFIG.info;
  const { Icon } = config;

  return (
    <div
      role="alert"
      aria-live={severity === "critical" ? "assertive" : "polite"}
      data-testid="standing-alert"
      data-severity={severity}
      className={cn(
        "flex items-start gap-3 w-full rounded-lg border px-4 py-3 text-sm",
        config.className,
        className
      )}
    >
      <Icon className="w-4 h-4 shrink-0 mt-0.5" />
      <div className="flex-1 min-w-0">{message}</div>
      {actionLabel && (
        <button
          type="button"
          onClick={() => onAction?.(id)}
          className="shrink-0 font-medium underline underline-offset-2 hover:no-underline"
        >
          {actionLabel}
        </button>
      )}
      <button
        type="button"
        onClick={() => onDismiss?.(id)}
        aria-label="Dismiss alert"
        data-testid="standing-alert-dismiss"
        className="shrink-0 opacity-70 hover:opacity-100 transition-opacity"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}

const VISIBLE_CAP = 3;

/**
 * Stack wrapper — parent owns the active-alerts array and passes it here.
 * Renders newest-first, capped at 3 visible; beyond that a trailing
 * "+N more" summary row expands the rest inline (no modal).
 */
export function StandingAlertStack({ alerts = [], onDismiss, onAction, expanded, onToggleExpanded }) {
  if (!alerts.length) return null;

  const ordered = [...alerts].reverse(); // newest-first
  const visible = expanded ? ordered : ordered.slice(0, VISIBLE_CAP);
  const overflowCount = ordered.length - VISIBLE_CAP;

  return (
    <div data-testid="standing-alert-stack" className="space-y-2 mb-4">
      {visible.map((alert) => (
        <StandingAlert
          key={alert.id}
          id={alert.id}
          severity={alert.severity}
          message={alert.message}
          actionLabel={alert.actionLabel}
          onAction={onAction}
          onDismiss={onDismiss}
        />
      ))}
      {!expanded && overflowCount > 0 && (
        <button
          type="button"
          onClick={onToggleExpanded}
          data-testid="standing-alert-overflow"
          className="text-xs text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
        >
          +{overflowCount} more
        </button>
      )}
    </div>
  );
}
