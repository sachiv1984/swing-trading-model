---
Owner: Frontend Specifications & UX Owner + Head of UX & Design
Class: QA Evidence (Class 4)
Status: Pending QA Sign-off
Cycle: 2026-04-11__release-v2.6
EPIC: EPIC-03
Branch: exec/2026-04-11__release-v2.6/EPIC-03
Commit: f862efe
---

# QA Evidence — EPIC-03: Frontend UX Polish

## Story Sign-off Summary

| Story | Title | DoQ | Verification Method |
|-------|-------|-----|---------------------|
| ST-08 | StatsCard Tooltip Prop | Pending | Code review |
| ST-09 | Trade History StatsCard Bar Layout (6-Card Width) | Pending | Code review |
| ST-10 | Trade History Column Header Styling and Formatting | Pending | Code review |
| ST-11 | Flexible Column Sorting Across Trade History Table | Pending | Code review |

**Note:** All 4 stories require observable UI behaviour (layout, hover effects, sort interaction). Full verification requires a local run or staging environment. Code review confirms implementation matches spec. Post-merge staging run is a required post-merge action.

---

## ST-08 — StatsCard Tooltip Prop

**AC target:** Optional `tooltip` prop; ⓘ icon visible when present; Avg Fee Drag card wired

**Evidence:**

### Files changed
- `src/components/ui/StatsCard.js` — `Info` icon imported; `tooltip` prop added to signature; ⓘ rendered adjacent to title when truthy

### AC verification

| AC | Status | Evidence |
|----|--------|----------|
| StatsCard accepts optional tooltip prop | Pass | Prop added to destructuring; no type error when absent |
| When tooltip absent, no ⓘ icon renders | Pass | Conditional `{tooltip && <Info ... />}` — renders nothing when falsy |
| When tooltip present, ⓘ icon visible adjacent to title | Pass | `<Info className="w-3 h-3 ..." title={tooltip} />` renders inline |
| Hover reveals tooltip text | Pass | `title={tooltip}` — native browser tooltip on hover |
| Avg Fee Drag StatsCard wired with canonical tooltip text | Pass | `tooltip="Average Fee Drag = Total exit fees / Gross proceeds × 100. Higher % means a greater proportion of gross proceeds consumed by fees."` |
| No regression to other StatsCard usage | Pass | Prop is optional; all existing StatsCard instances unmodified |

**Unverified AC (requires local run):** Hover behaviour and visual rendering of ⓘ icon. Code review confirms the pattern is correct. Post-merge staging run required.

---

## ST-09 — Trade History StatsCard Bar Layout

**AC target:** grid-cols-7@xl, grid-cols-4@md, all 7 cards readable; card padding md:p-3

**Evidence:**

### Files changed
- `src/pages/TradeHistory.js` — grid updated from `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6` to `grid-cols-2 md:grid-cols-4 xl:grid-cols-7`; Total Trades card added as first card; `className="md:p-3"` on all 7 cards; Avg Fee Drag tooltip wired

### AC verification

| AC | Status | Evidence |
|----|--------|----------|
| Grid is `grid-cols-4` at md | Pass | `md:grid-cols-4` in className |
| Grid is `grid-cols-7` at xl | Pass | `xl:grid-cols-7` in className |
| All 7 cards present | Pass | Total Trades, Win Rate, Total P&L, Avg Winner, Avg Loser, Avg Entry Dev., Avg Fee Drag |
| Card padding reduced at md+ | Pass | `className="md:p-3"` on all 7 StatsCard instances |
| No regression to individual card content | Pass | Card content unchanged; only grid and padding modified |

**Unverified AC (requires local run):** Visual layout at xl and md breakpoints. Code review confirms the responsive classes are correct.

---

## ST-10 — Trade History Column Header Styling

**AC target:** `text-xs font-semibold text-slate-300 uppercase tracking-wide` applied; no change to DataTable.js

**Evidence:**

### Files changed
- `src/components/trades/TradeHistoryTable.js` — `TH_CLASS` constant defined at top of component; all `<TableHead>` elements pass `className={TH_CLASS}` or `className={cn(TH_CLASS, ...)}` for sortable headers

### AC verification

| AC | Status | Evidence |
|----|--------|----------|
| Head of UX target style defined and applied | Pass | `TH_CLASS = "font-semibold text-slate-300 tracking-wide"` merged via `cn()` with DataTable defaults |
| `font-semibold` replaces `font-medium` | Pass | TH_CLASS includes `font-semibold`; tailwind-merge resolves conflict |
| `text-slate-300` replaces `text-slate-400` | Pass | TH_CLASS includes `text-slate-300` |
| `tracking-wide` added | Pass | TH_CLASS includes `tracking-wide` |
| DataTable.js default unchanged | Pass | DataTable.js not modified |
| No regression to other tables using DataTable.js | Pass | Override is in TradeHistoryTable.js only |

---

## ST-11 — Flexible Column Sorting

**AC target:** Entry Date, Exit Date, P&L, P&L%, Days Held sortable; Exit Date default DESC; sort icons consistent

**Evidence:**

### Files changed
- `src/components/trades/TradeHistoryTable.js`:
  - 5 new sort states (`entryDateSort`, `exitDateSort` init SORT_DESC, `pnlSort`, `pnlPctSort`, `daysHeldSort`)
  - `cycle()` helper shared by all new sort handlers
  - `displayTrades` useMemo extended with 5 new sort blocks
  - `SortIcon` component consolidates arrow rendering; existing aliases preserved
  - Days Held column added (header + cell; `trade.holding_days`, null → "—")
  - All headers updated with sort wiring and TH_CLASS
  - `colSpan` bumped from 9 → 10

### AC verification

| AC | Status | Evidence |
|----|--------|----------|
| Entry Date sortable (oldest/newest) | Pass | `entryDateSort` state; `cycle(setEntryDateSort)` on click; date string comparison |
| Exit Date sortable, default DESC | Pass | `exitDateSort` initialized to `SORT_DESC`; `cycle(setExitDateSort)` on click |
| P&L GBP sortable | Pass | `pnlSort` state; `cycle(setPnlSort)` on click; `a.pnl` comparison |
| P&L % sortable | Pass | `pnlPctSort` state; `cycle(setPnlPctSort)` on click; `a.pnl_pct` comparison |
| Days Held sortable; null to end | Pass | `daysHeldSort` state; null guard in sort comparator |
| Days Held column visible | Pass | New `<TableHead>` + `<TableCell>` added with `trade.holding_days` |
| Sort icon treatment consistent | Pass | All columns use `SortIcon` with same SORT_NONE/ASC/DESC states |
| Non-sortable columns: Ticker, Exit Reason | Pass | No onClick on Ticker or Exit Reason headers |
| No regression to Slippage/Fee Drag/R-Multiple sort | Pass | Existing sort logic untouched; only added above it in useMemo chain |

**Unverified AC (requires local run):** Click interactions, default sort visual rendering, Days Held column display. Code review confirms implementation matches spec. Post-merge staging run required.

---

## Post-merge Actions

1. Run Trade History page in browser (local or staging) to verify:
   - 7-card stats bar renders correctly at xl (all in one row) and md (4+3)
   - ⓘ tooltip on Avg Fee Drag shows canonical text on hover
   - Exit Date column shows ↓ sort icon on initial load (default DESC)
   - Days Held column renders holding_days or "—"
   - Column header text is bold/bright vs prior version
2. Open PR and obtain QA sign-off + Product Owner acceptance before merge

---

*Generated by Sprint Execution Engine — 2026-04-11*
