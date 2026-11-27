// Trade Plan checklist: system-checked items as status (trade_plan.md v1.30 §6;
// ST-12, BLG-UX-19, EPIC-02, v9.18; design record
// docs/design/2026-11-18__release-v9.18/trade-plan-checklist-status §3–§5).
//
// Two items are not ticked by the trader: "Position size checks" (CHK-02, id
// heat_limit_checked) takes the worst of three existing pre-entry checks, and
// "Stop level defined" (CHK-03, id stop_defined) reads the Stop Level field.
// Both are advisory (strategy_rules.md §4.2.6): they gate nothing.
import { currencyForMarket } from "./format";

export const SIZE_ITEM_ID = "heat_limit_checked";
export const STOP_ITEM_ID = "stop_defined";
export const SYSTEM_ITEM_IDS = [SIZE_ITEM_ID, STOP_ITEM_ID];
export const SIZE_ITEM_LABEL = "Position size checks";

// The pre-entry checks "Position size checks" summarises (§4.2.4, §4.2.2, §4.2.5).
export const SIZE_RULES = ["cash_constraint", "sector_concentration", "sizing_validity"];

const RANK = { pass: 0, warn: 1, fail: 2 };

// "pass" | "warn" | "fail" | null (no result: no snapshot, or all three skipped
// or absent). `skipped` and unknown statuses are ignored.
export function positionSizeStatus(snapshot) {
  const checks = Array.isArray(snapshot?.checks) ? snapshot.checks : [];
  let worst = null;
  for (const c of checks) {
    if (!c || !SIZE_RULES.includes(c.rule) || !(c.status in RANK)) continue;
    if (worst === null || RANK[c.status] > RANK[worst]) worst = c.status;
  }
  return worst;
}

// The Stop Level as a positive number, or null (empty, 0, negative, not a
// number). Parsed exactly as the form saves it (parseFloat) and as
// isStopLevelValid gates What-if sizing, so the three always agree.
export function stopLevel(value) {
  if (value === null || value === undefined || value === "" || typeof value === "boolean") return null;
  const n = typeof value === "number" ? value : parseFloat(value);
  return Number.isFinite(n) && n > 0 ? n : null;
}

// Visible text for each system row (§6.2 status table).
export function positionSizeText(status, { readOnly = false } = {}) {
  if (status === "pass") return "✓ Pass";
  if (status === "warn") return "! Warning — see Pre-Entry Checks";
  if (status === "fail") return "✗ Fail — see Pre-Entry Checks";
  return readOnly ? "Not checked when saved" : "Not checked yet";
}

export function stopText(value, market) {
  const stop = stopLevel(value);
  return stop === null ? "✗ Not set" : `✓ Set: ${stop.toFixed(2)} ${currencyForMarket(market)}`;
}

// Saved form (§6.5): the four entries keep their ids; the two system items
// carry "auto": true and checked = the status (pass / stop set); judgement
// items keep their tick. The system label is the v1.30 one.
export function withSystemStatus(items, { sizeStatus, stopValue }) {
  return (Array.isArray(items) ? items : []).map((item) => {
    if (item?.id === SIZE_ITEM_ID) return { ...item, label: SIZE_ITEM_LABEL, checked: sizeStatus === "pass", auto: true };
    if (item?.id === STOP_ITEM_ID) return { ...item, checked: stopLevel(stopValue) !== null, auto: true };
    return item;
  });
}

// Judgement items only, with their index in the full list (for toggling).
export function judgementItems(items) {
  return (Array.isArray(items) ? items : [])
    .map((item, index) => ({ item, index }))
    .filter(({ item }) => !SYSTEM_ITEM_IDS.includes(item?.id));
}

// checklist_completed: the judgement items are all ticked (ESC-EXEC-20261126-01:
// only judgement items count as skipped). False with no judgement items.
export function judgementComplete(items) {
  const judged = judgementItems(items);
  return judged.length > 0 && judged.every(({ item }) => item.checked === true);
}
