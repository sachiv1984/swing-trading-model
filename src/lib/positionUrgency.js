// Decision-first urgency order for open positions (ST-01, BLG-FE-260, v9.17).
// Spec: positions.md v2.25 §Decision-First Table (§Urgency Order, §Stop Distance).
// Design: docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md §2.
//
// Display-only (§13): the tiers apply the existing §7/§8 tests from
// exitCondition.js and the Risk Dashboard's existing ≤ 5% stop-distance band
// (risk_dashboard.md §6). No new score, ranking signal or recommendation.
// Used by the Table view, the narrow-screen cards and the Grid view.

import { getExitCondition, isPostGraceStopBreach, isSplitPending } from "./exitCondition";

export const URGENCY_TIER = {
  // ST-27 (BLG-BE-223, v9.18): a detected split to confirm (positions.md v2.30
  // §Split Detected State). Above tier 1: the position's stop and exit tests
  // are suppressed until it is confirmed, so it must not sort as healthy.
  SPLIT_TO_CONFIRM: 0,
  EXIT_CONDITION: 1,
  STOP_REACHED: 2,
  NEAR_STOP: 3,
  OTHER: 4,
};

// The risk_dashboard.md §6 rose band. A display band, not a strategy rule.
export const NEAR_STOP_PCT = 5.0;
// The risk_dashboard.md §6 amber band.
export const WARN_STOP_PCT = 15.0;

const toNumber = (v) => (v === null || v === undefined || v === "" ? null : Number(v));

export function isInGrace(position) {
  return position?.grace_period === true;
}

// dashboard.md v4.4 §4B (ST-10, BLG-FE-308, v9.18): one grace definition for
// every Dashboard grace count. A day count is only read for an in-grace
// position, and only when it is a finite number (`GET /positions` sends
// `grace_days_remaining` only while in grace, else null).
export function graceDaysRemaining(position) {
  if (!isInGrace(position)) return null;
  const v = position.grace_days_remaining;
  // A number, or a numeric string; whitespace, booleans and other values are
  // not a day count (Number(" ") is 0 and Number(true) is 1).
  if (typeof v === "number") return Number.isFinite(v) ? v : null;
  if (typeof v === "string" && /^-?\d+(\.\d+)?$/.test(v.trim())) return Number(v);
  return null;
}

// Grace ends today: in grace with 1 day left (Day 10 of 10). The Today list's
// "Grace ends today" group.
export function isGraceEndingToday(position) {
  return graceDaysRemaining(position) === 1;
}

// In grace with between 1 and `days` days left (Positions to Watch: "ending
// within 2 days"). 0 or below means grace has already ended ("Grace period has
// ended" on Card 3), so it is not "ending".
export function isGraceEndingWithin(position, days) {
  const n = graceDaysRemaining(position);
  return n !== null && n >= 1 && n <= days;
}

// The smallest day count among in-grace positions, or null when none has one.
export function minGraceDaysRemaining(positions) {
  const days = (Array.isArray(positions) ? positions : []).map(graceDaysRemaining).filter((d) => d !== null);
  return days.length ? Math.min(...days) : null;
}

// risk_dashboard.md §5.2 and dashboard.md §4 Card 3 (moved here from
// GracePeriodPanel.js, ST-10). grace_days_remaining 1 is the last day of grace
// ("Ends today", Day 10 of 10), so a value n ends in n − 1 days. 0 means grace
// has just ended; the position moves on at the next refresh.
export function nextEndsText(days) {
  if (days === null || days === undefined) return null;
  if (days <= 0) return "Grace period has ended";
  if (days === 1) return "Ends today";
  const n = days - 1;
  return `Next ends in ${n} day${n === 1 ? "" : "s"}`;
}

// (current_price − current_trailing_stop) ÷ current_price × 100, on the GBP
// basis the breach test uses. Negative when the price is below the stop.
export function stopDistancePct(position) {
  // A pending split pauses the stop (§9.1): pre-split stop, post-split price.
  if (isSplitPending(position)) return null;
  const price = toNumber(position?.current_price);
  const stop = toNumber(position?.current_trailing_stop);
  if (price == null || stop == null || !(price > 0) || !(stop > 0)) return null;
  return ((price - stop) / price) * 100;
}

// (current_price_native − current_trailing_stop_native) ÷ (entry_price − initial_stop).
// null when the denominator is ≤ 0 or an input is missing.
export function stopDistanceR(position) {
  if (isSplitPending(position)) return null;
  const price = toNumber(position?.current_price_native);
  const stop = toNumber(position?.current_trailing_stop_native);
  const entry = toNumber(position?.entry_price);
  const initial = toNumber(position?.initial_stop);
  if ([price, stop, entry, initial].some((v) => v == null || Number.isNaN(v))) return null;
  const risk = entry - initial;
  if (!(risk > 0)) return null;
  return (price - stop) / risk;
}

export function getUrgencyTier(position) {
  if (isSplitPending(position)) return URGENCY_TIER.SPLIT_TO_CONFIRM;
  if (getExitCondition(position).riskOff) return URGENCY_TIER.EXIT_CONDITION;
  if (isPostGraceStopBreach(position)) return URGENCY_TIER.STOP_REACHED;
  if (position?.grace_period === false) {
    const pct = stopDistancePct(position);
    if (pct != null && pct <= NEAR_STOP_PCT) return URGENCY_TIER.NEAR_STOP;
  }
  return URGENCY_TIER.OTHER;
}

// The distance used for ordering. In grace the stop is not enforced and the
// cell shows no distance, so it counts as no distance (sorts last in tier 4).
function sortDistance(position) {
  return isInGrace(position) ? null : stopDistancePct(position);
}

function urgencyKey(position) {
  return { tier: getUrgencyTier(position), dist: sortDistance(position), ticker: String(position?.ticker ?? "") };
}

function compareKeys(ka, kb) {
  if (ka.tier !== kb.tier) return ka.tier - kb.tier;
  if (ka.dist == null && kb.dist != null) return 1;
  if (ka.dist != null && kb.dist == null) return -1;
  if (ka.dist != null && kb.dist != null && ka.dist !== kb.dist) return ka.dist - kb.dist;
  return ka.ticker.localeCompare(kb.ticker);
}

// Tier, then stop distance % ascending (no distance last in its tier), then ticker A–Z.
export function compareByUrgency(a, b) {
  return compareKeys(urgencyKey(a), urgencyKey(b));
}

// Works out each position's key once, then sorts.
export function sortByUrgency(positions) {
  return (positions || [])
    .map((position) => ({ position, key: urgencyKey(position) }))
    .sort((x, y) => compareKeys(x.key, y.key))
    .map(({ position }) => position);
}

// Colour class for the "To stop" cell (risk_dashboard.md §6 bands).
export function stopDistanceClass(pct) {
  if (pct == null) return "text-app-muted";
  if (pct <= NEAR_STOP_PCT) return "text-app-negative";
  if (pct <= WARN_STOP_PCT) return "text-app-warning";
  return "text-app-fg";
}

// "{x.x}R · {y.y}%", with "—" for a missing part.
export function formatStopDistance(position) {
  const pct = stopDistancePct(position);
  const r = stopDistanceR(position);
  if (pct == null && r == null) return "—";
  const rText = r == null ? "—" : `${r.toFixed(1)}R`;
  const pctText = pct == null ? "—" : `${pct.toFixed(1)}%`;
  return `${rText} · ${pctText}`;
}
