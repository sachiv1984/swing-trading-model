// Decision-first urgency order for open positions (ST-01, BLG-FE-260, v9.17).
// Spec: positions.md v2.25 §Decision-First Table (§Urgency Order, §Stop Distance).
// Design: docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md §2.
//
// Display-only (§13): the tiers apply the existing §7/§8 tests from
// exitCondition.js and the Risk Dashboard's existing ≤ 5% stop-distance band
// (risk_dashboard.md §6). No new score, ranking signal or recommendation.
// Used by the Table view, the narrow-screen cards and the Grid view.

import { getExitCondition, isPostGraceStopBreach } from "./exitCondition";

export const URGENCY_TIER = {
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

// (current_price − current_trailing_stop) ÷ current_price × 100, on the GBP
// basis the breach test uses. Negative when the price is below the stop.
export function stopDistancePct(position) {
  const price = toNumber(position?.current_price);
  const stop = toNumber(position?.current_trailing_stop);
  if (price == null || stop == null || !(price > 0) || !(stop > 0)) return null;
  return ((price - stop) / price) * 100;
}

// (current_price_native − current_trailing_stop_native) ÷ (entry_price − initial_stop).
// null when the denominator is ≤ 0 or an input is missing.
export function stopDistanceR(position) {
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
