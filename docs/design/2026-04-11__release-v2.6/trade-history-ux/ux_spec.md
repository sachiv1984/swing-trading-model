**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Active
**Cycle:** 2026-04-11__release-v2.6
**Last Updated:** 2026-04-11
**Approved by:** Product Owner — 2026-04-11

---

# UX Decision Record — Trade History Polish (v2.6)

Stories covered: ST-09, ST-10, ST-11

---

## ST-09 — Summary Stats Bar Layout (7-Card)

### Context

The Trade History summary bar contains 7 stat cards as of v2.5:
Total Trades, Win Rate %, Total P&L, Avg Winner, Avg Loser, Avg Slippage, Avg Fee Drag.

The backlog item (BLG-FE-11) was filed during v2.5 when 6 cards existed. With Avg Fee Drag added in v2.5, the bar is now 7 cards — the crowding concern applies equally and is addressed here.

### Design Decision

**Grid spec:**

| Breakpoint | Grid Columns | Behaviour |
|------------|-------------|-----------|
| Below `md` (<768px) | Stacked | Existing responsive behaviour unchanged |
| `md` (≥768px) | `grid-cols-4` | 4 cards in row 1, 3 cards in row 2 |
| `xl` (≥1280px) | `grid-cols-7` | All 7 cards in single row |

**Card padding at `md`–`xl` range:** `px-3 py-3` (reduced from default `px-4 py-4`) to improve fit in the 4-column layout. No change below `md` or at `xl`+.

**No horizontal scroll.** No overflow patterns. All 7 cards must be readable and unstacked at `xl` breakpoint (≥1280px).

**Acceptance condition:** All 7 cards are readable at a 1280px viewport width without horizontal scroll or stacking.

---

## ST-10 — Column Header Styling

### Context

DataTable.js default header class string: `text-xs font-medium text-slate-400 uppercase`. Observation: weight and contrast are insufficient for the expanded 14-column Trade History table; headers are difficult to distinguish from muted cell content.

### Design Decision

**Trade History table column header override:**

Target class string: `text-xs font-semibold text-slate-300 uppercase tracking-wide`

Changes from default:
- `font-medium` → `font-semibold`: improved weight and legibility
- `text-slate-400` → `text-slate-300`: improved contrast on dark background
- `tracking-wide` added: improves uppercase character spacing for multi-word headers

**Implementation preference:** Trade History-specific override (e.g. pass a `headerClassName` prop to DataTable.js, or apply within the Trade History component's JSX). Do **not** modify DataTable.js base styles globally — this would cause regression to other tables using DataTable.js.

---

## ST-11 — Flexible Column Sorting Strategy

### Context

Currently sortable in Trade History: Slippage, Fee Drag %, R-Multiple (3 of 14 columns). The `DataTable.js TableHead` onClick infrastructure was fixed in v2.5 and is ready for extension.

### Design Decision

**Sorting strategy:** Curated set — all numeric and date columns with analytical value. Categorical and low-signal columns are excluded.

**Sortable columns (post-ST-11):**

| Column | Sort Behaviour | Status |
|--------|---------------|--------|
| Entry Date | Ascending = oldest first; descending = newest first | New — ST-11 |
| Exit Date | Ascending = oldest first; descending = newest first | New — ST-11 |
| P&L (GBP) | Ascending = worst P&L first | New — ST-11 |
| P&L % | Ascending = worst P&L % first | New — ST-11 |
| Days Held | Ascending = shortest hold first | New — ST-11 |
| Slippage | Ascending = best slippage first; nulls sort to end | Existing — retain unchanged |
| Fee Drag % | Ascending = lowest fee drag first | Existing — retain unchanged |
| R-Multiple | Ascending = worst R first; nulls sort to end | Existing — retain unchanged |

**Non-sortable columns:** Ticker, Market flag, Shares, Entry price, Exit price, Exit reason.
Rationale: categorical, binary, or low analytical value from sorting.

**Default sort:** Exit Date descending (most recent trades first). Matches expected user mental model on page load.

**Sort icon treatment:** Active sort column shows solid directional indicator (↑ or ↓); hovering over any sortable column shows a dimmed indicator. Consistent with existing Slippage/Fee Drag/R-Multiple implementation — no change to existing sort behaviour on those columns.

---

## Product Owner Approval

All three design decisions reviewed and approved.

**Approved by:** Product Owner
**Date:** 2026-04-11
**Approval scope:** ST-09 grid spec, ST-10 header style override, ST-11 sort strategy (curated set, Exit Date default) — all approved for implementation.
