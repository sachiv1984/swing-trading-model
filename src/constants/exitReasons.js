// Shared exit-reason vocabulary (v9.13 ST-03, BLG-FE-227).
// The only frontend source of exit-reason labels, badge colours and
// strategy_rules.md §8 categories. Spec: trade_history.md §Exit Reason Labels
// and Badges; design source docs/design/2026-10-16__release-v9.13/
// exit-reason-badges/decision_record.md. The six stored values and their §8
// category come from data_model.md §3 Exit Reason Values (ST-02, DS-34);
// backend/exit_reasons.py is the backend copy.

export const EXIT_REASON_STOP = "Stop Loss Hit";
export const EXIT_REASON_TRAILING = "Trailing Stop";
export const EXIT_REASON_RISK_OFF = "Risk-Off Signal";
export const EXIT_REASON_MANUAL = "Manual Exit";
export const EXIT_REASON_TARGET = "Target Reached";
export const EXIT_REASON_PARTIAL = "Partial Profit Taking";

export const SECTION_8_STOP_LOSS = "§8.1 Stop-loss trigger";
export const SECTION_8_RISK_OFF = "§8.2 Market risk-off override";
export const SECTION_8_MANUAL = "§8.3 Manual exit";

const BADGE_BASE = "rounded-full border px-2 py-0.5 text-xs font-medium";

// Full class strings so Tailwind's scanner sees every token.
const BADGE_COLOURS = {
  rose: "bg-rose-100 text-rose-800 border-rose-200 dark:bg-rose-500/20 dark:text-rose-400 dark:border-rose-500/30",
  cyan: "bg-cyan-100 text-cyan-800 border-cyan-200 dark:bg-cyan-500/20 dark:text-cyan-400 dark:border-cyan-500/30",
  amber: "bg-amber-100 text-amber-800 border-amber-200 dark:bg-amber-500/20 dark:text-amber-400 dark:border-amber-500/30",
  violet: "bg-violet-100 text-violet-800 border-violet-200 dark:bg-violet-500/20 dark:text-violet-400 dark:border-violet-500/30",
  emerald: "bg-emerald-100 text-emerald-800 border-emerald-200 dark:bg-emerald-500/20 dark:text-emerald-400 dark:border-emerald-500/30",
  blue: "bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-500/20 dark:text-blue-400 dark:border-blue-500/30",
  slate: "bg-slate-100 text-slate-800 border-slate-200 dark:bg-slate-500/20 dark:text-slate-400 dark:border-slate-500/30",
};

// In ExitModal's select order.
export const EXIT_REASONS = {
  [EXIT_REASON_MANUAL]: { label: "Manual Exit", short: "Manual", colour: "violet", category: SECTION_8_MANUAL },
  [EXIT_REASON_STOP]: { label: "Stop Loss Hit", short: "Stop Hit", colour: "rose", category: SECTION_8_STOP_LOSS },
  [EXIT_REASON_TARGET]: { label: "Target Reached", short: "Target", colour: "emerald", category: SECTION_8_MANUAL },
  [EXIT_REASON_RISK_OFF]: { label: "Risk-Off Signal", short: "Risk-Off", colour: "amber", category: SECTION_8_RISK_OFF },
  [EXIT_REASON_TRAILING]: { label: "Trailing Stop", short: "Trailing Stop", colour: "cyan", category: SECTION_8_STOP_LOSS },
  [EXIT_REASON_PARTIAL]: { label: "Partial Profit Taking", short: "Partial", colour: "blue", category: SECTION_8_MANUAL },
};

export const EXIT_REASON_VALUES = Object.keys(EXIT_REASONS);

// Legacy spellings resolve to a stored value before lookup (data_model.md DS-34).
export const EXIT_REASON_ALIASES = {
  stop_hit: EXIT_REASON_STOP,
  manual: EXIT_REASON_MANUAL,
  manual_exit: EXIT_REASON_MANUAL,
  target: EXIT_REASON_TARGET,
  target_reached: EXIT_REASON_TARGET,
  market_regime: EXIT_REASON_RISK_OFF,
  risk_off: EXIT_REASON_RISK_OFF,
  risk_off_signal: EXIT_REASON_RISK_OFF,
  trailing_stop: EXIT_REASON_TRAILING,
  partial: EXIT_REASON_PARTIAL,
  partial_profit_taking: EXIT_REASON_PARTIAL,
};

// Stored value for a stored value or legacy alias; anything else unchanged
// (null/undefined stay null).
export function resolveExitReason(value) {
  if (value == null || value === "") return null;
  if (EXIT_REASONS[value]) return value;
  return EXIT_REASON_ALIASES[value] || value;
}

function entryFor(value) {
  const resolved = resolveExitReason(value);
  return resolved ? EXIT_REASONS[resolved] || null : null;
}

// Full label for text fields, tables and exports. Unknown values are shown as
// stored; null shows "—".
export function exitReasonLabel(value) {
  const entry = entryFor(value);
  if (entry) return entry.label;
  return value == null || value === "" ? "—" : String(value);
}

// Short label for badges.
export function exitReasonShortLabel(value) {
  const entry = entryFor(value);
  if (entry) return entry.short;
  return value == null || value === "" ? "—" : String(value);
}

// Badge classes (light and dark), slate for unknown or null.
export function exitReasonBadgeClass(value) {
  const entry = entryFor(value);
  return `${BADGE_BASE} ${BADGE_COLOURS[entry ? entry.colour : "slate"]}`;
}

// §8 category; null is read as Manual Exit (metrics_definitions.md
// §Exit Condition Category). Unknown values have no category.
export function exitReasonCategory(value) {
  if (value == null || value === "") return SECTION_8_MANUAL;
  const entry = entryFor(value);
  return entry ? entry.category : null;
}

// Grouping key for analytics: the stored value, with null read as Manual Exit.
export function exitReasonGroupKey(value) {
  return resolveExitReason(value) || EXIT_REASON_MANUAL;
}
