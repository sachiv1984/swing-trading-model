// Trade History rules filter (trade_history.md v1.18 §Rules Filter; ST-13,
// BLG-FE-320, EPIC-02, v9.18). Reads the server-computed rules_followed /
// rules_broken on GET /trades (metrics_definitions.md §Rules Followed); the
// browser decides nothing about what counts.

export const RULES_OPTIONS = [
  { value: "all", label: "All" },
  { value: "followed", label: "Followed" },
  { value: "broken", label: "Broken" },
  { value: "unknown", label: "Not known" },
];
const VALUES = new Set(RULES_OPTIONS.map((o) => o.value));

// Same labels as the Journal's Red flags tab (RedFlagsSection.js).
export const RULE_REASON_LABELS = {
  pre_entry_override: "Pre-Entry Override",
  checklist_skipped: "Checklist Skipped",
  stop_prompt_dismissed: "Stop Prompt Dismissed",
  drawdown_prompt_dismissed: "Drawdown Prompt Dismissed",
};

// The ?rules= value, or "all" for a missing or unknown one.
export function parseRulesParam(value) {
  return VALUES.has(value) ? value : "all";
}

// "followed" | "broken" | "unknown": anything but a real true/false is not known.
export function rulesState(trade) {
  if (trade?.rules_followed === true) return "followed";
  if (trade?.rules_followed === false) return "broken";
  return "unknown";
}

export function matchesRules(trade, option) {
  return option === "all" || !VALUES.has(option) || rulesState(trade) === option;
}

export function rulesCounts(trades) {
  const counts = { followed: 0, broken: 0, unknown: 0 };
  for (const t of Array.isArray(trades) ? trades : []) counts[rulesState(t)] += 1;
  return counts;
}

// The expanded row's "Rules" line.
export function rulesLine(trade) {
  const state = rulesState(trade);
  if (state === "followed") return "Followed";
  if (state === "unknown") return "Not known (no entry check recorded)";
  const reasons = (Array.isArray(trade.rules_broken) ? trade.rules_broken : []).map((r) => RULE_REASON_LABELS[r] || r);
  return reasons.length ? `Broken: ${reasons.join(", ")}` : "Broken";
}
