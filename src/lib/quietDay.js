// Quiet-day collapse (dashboard.md v4.4 §3A; ST-09, BLG-UX-11, EPIC-02, v9.18;
// design record docs/design/2026-11-18__release-v9.18/dashboard-quiet-day §2).
//
// Below the Today list, an element whose data has loaded and is empty folds:
// it is not rendered, and its name joins one "Nothing to show: …" line. The
// test for "empty" is the element's existing `empty` condition; this module
// only decides when an element counts as folded and in what order the line
// lists the names.

// Table order of dashboard.md §3A. `to` is the line entry's link; `disclosure`
// entries have no page and reveal their card in place instead.
export const QUIET_DAY_ITEMS = [
  { key: "screener-hits", name: "Screener hits", to: "/Screener" },
  { key: "positions-to-watch", name: "Positions to watch", to: "/Positions?grace=open" },
  { key: "red-flags", name: "Red flags", to: "/Journal?section=red-flags" },
  { key: "earnings", name: "Earnings", to: "/Positions" },
  { key: "compliance", name: "Compliance", to: "/Performance?section=compliance" },
  { key: "ai-briefing", name: "AI briefing", disclosure: true },
  { key: "open-positions", name: "Open positions", to: "/Positions" },
  { key: "portfolio-heat", name: "Portfolio heat", to: "/RiskDashboard" },
  { key: "in-grace", name: "In grace", to: "/Positions?grace=open" },
  { key: "recent-activity", name: "Recent activity", to: "/TradeHistory" },
  { key: "whats-new", name: "What's new", disclosure: true },
];

// The elements that share a container: the briefing panel (five Morning
// Briefing cards and the AI briefing) and the Cards 1–3 row.
export const BRIEFING_PANEL_KEYS = ["screener-hits", "positions-to-watch", "red-flags", "earnings", "compliance", "ai-briefing"];
export const MORNING_BRIEFING_KEYS = ["screener-hits", "positions-to-watch", "red-flags", "earnings", "compliance"];
export const STATUS_ROW_KEYS = ["open-positions", "portfolio-heat", "in-grace"];

// An element folds only once it has loaded without error and is empty. A
// loading element shows its own skeleton; a failed one shows its error in
// place (an error is not empty).
export function isFolded({ isLoading, error, empty }) {
  return !isLoading && !error && empty === true;
}

// The line's entries: the folded items in table order. A revealed disclosure
// entry stays in the line (its button reads aria-expanded="true") even while
// its card is loading or has data, so the button the user pressed never moves.
export function foldedItems(foldedKeys, revealedKeys) {
  const set = foldedKeys instanceof Set ? foldedKeys : new Set(foldedKeys || []);
  const revealed = revealedKeys instanceof Set ? revealedKeys : new Set(revealedKeys || []);
  return QUIET_DAY_ITEMS.filter((item) => set.has(item.key) || (item.disclosure && revealed.has(item.key)));
}

// How many of `keys` are still shown (not folded, or folded and revealed).
export function shownCount(keys, foldedKeys, revealedKeys = new Set()) {
  return keys.filter((k) => !foldedKeys.has(k) || revealedKeys.has(k)).length;
}

// Static class names so Tailwind keeps them: a grid with n shown cards uses n
// equal columns from md up, so a folded card leaves no gap.
const MD_GRID_COLS = {
  1: "md:grid-cols-1",
  2: "md:grid-cols-2",
  3: "md:grid-cols-3",
  4: "md:grid-cols-4",
  5: "md:grid-cols-5",
};

export function mdGridCols(n) {
  return MD_GRID_COLS[n] || MD_GRID_COLS[1];
}
