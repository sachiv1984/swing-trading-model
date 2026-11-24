// Fixture (ST-21): GracePeriodAlertContent from src/pages/Positions.js at 99f16e6d, the only component
// the collision check reads for this diff's SC-LBG-03 case. The rest of the file is omitted.
function GracePeriodAlertContent({ alerts, isLoading }) {
  // Dismissals made this session, plus any already in sessionStorage. Read at
  // render, so an alert dismissed before a reload stays dismissed whenever the
  // entry is opened.
  const [dismissed, setDismissed] = useState({});
  const isDismissed = (positionId) =>
    dismissed[positionId] === true || Boolean(sessionStorage.getItem(GRACE_DISMISS_KEY(positionId)));

  const dismiss = (positionId) => {
    sessionStorage.setItem(GRACE_DISMISS_KEY(positionId), "1");
    setDismissed((prev) => ({ ...prev, [positionId]: true }));
  };

  if (isLoading) {
    return <p className="text-sm text-app-muted">Loading grace period alerts…</p>;
  }

  const visible = alerts.filter((a) => !isDismissed(a.position_id));
  // ST-03 (BLG-FE-262, v9.17): the warning strip's grace entry expands to this
  // content, so it no longer returns null or announces itself (role="alert"
  // removed, positions.md §Warning Strip). ST-04 replaces it with GracePeriodView.
  if (visible.length === 0) {
    return (
      <p className="text-sm text-app-muted">
        No position is within 2 days of the end of its grace period.
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {visible.map((alert) => {
        // ST-12 (BLG-FE-196, v9.10) / ST-14 (BLG-BE-147, v9.11): every grace reading
        // comes from grace_days_remaining (calendar days since entry, §6.2), never
        // days_in_state. Day number: min(grace + 1 − grace_days_remaining, grace), entry day = Day 1.
        const daysLeft = alert.grace_days_remaining;
        const dayNumber = daysLeft != null ? Math.min(GRACE_PERIOD_DAYS + 1 - daysLeft, GRACE_PERIOD_DAYS) : null;
        const bodyText = daysLeft === 0
          ? "Grace period has ended. Your position will transition to LOSING or PROFITABLE on next refresh."
          : daysLeft != null
            ? `Your grace period ends in ${daysLeft} day${daysLeft !== 1 ? "s" : ""}. Review your original thesis before the window closes.`
            : "Your grace period is ending. Review your original thesis before the window closes.";
        const tp = alert.trade_plan_summary;

        return (
          <div
            key={alert.position_id}
            className="rounded-xl border-l-4 border-amber-500 bg-amber-500/10 px-4 py-3"
            style={{ borderLeftColor: "#D97706" }}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2 text-amber-300 font-semibold text-sm">
                <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                Grace Period Alert — {alert.ticker}
                {dayNumber != null && (
                  <span className="text-xs font-medium text-amber-400 bg-amber-500/20 px-1.5 py-0.5 rounded" data-testid="grace-alert-day-label">
                    Day {dayNumber} of {GRACE_PERIOD_DAYS}
                  </span>
                )}
              </div>
              <button
                onClick={() => dismiss(alert.position_id)}
                aria-label={`Dismiss grace period alert for ${alert.ticker}`}
                className="text-amber-400/60 hover:text-amber-300 flex-shrink-0"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <p className="text-sm text-amber-200/80 mt-1">{bodyText}</p>
            {tp ? (
              <div className="mt-2 text-xs text-slate-300 space-y-0.5">
                {tp.setup_thesis && <div><span className="text-slate-600 dark:text-slate-400">Thesis: </span>"{tp.setup_thesis.slice(0, 120)}{tp.setup_thesis.length > 120 ? "…" : ""}"</div>}
                {tp.stop_level != null && <div><span className="text-slate-600 dark:text-slate-400">Stop: </span>{tp.stop_level}</div>}
                {tp.r_target != null && <div><span className="text-slate-600 dark:text-slate-400">R-target: </span>{tp.r_target}R</div>}
              </div>
            ) : (
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">No trade plan linked. Consider adding a plan for context.</p>
            )}
            {alert.trade_plan_id && (
              <Link
                to={`/TradePlan?edit=${alert.trade_plan_id}&ticker=${alert.ticker}`}
                className="inline-block mt-2 text-xs text-amber-400 hover:text-amber-300 underline"
              >
                View Trade Plan →
              </Link>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// ST-03 (IT-03) — Trail Stop modal
// ST-10 (BLG-BE-159, v9.12): read-only. The Strategy Rules & System Intent Owner
// ruled (ESC-EXEC-20261013-06, Branch B) that a user may not set or raise a stop
// manually, so the modal compares the stored stop with the ATR trail and offers no
// apply action. It never proposes a lower stop (strategy_rules.md §7.3).
// Spec: positions.md v2.18 §Trail Stop Action.
// ---------------------------------------------------------------------------

