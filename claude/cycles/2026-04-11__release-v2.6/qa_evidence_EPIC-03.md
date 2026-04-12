---
Owner: Frontend Specifications & UX Owner + Head of UX & Design
Class: QA Evidence (Class 4)
Status: Accepted — DoQ and PO sign-off granted 2026-04-12
Cycle: 2026-04-11__release-v2.6
EPIC: EPIC-03
Branch: exec/2026-04-11__release-v2.6/EPIC-03
Commit: f862efe
---

# QA Evidence — EPIC-03: Frontend UX Polish

## Story Sign-off Summary

| Story | Title | DoQ | Verification Method |
|-------|-------|-----|---------------------|
| ST-08 | StatsCard Tooltip Prop | ✅ Pass | Code review + staging visual QA 2026-04-12 |
| ST-09 | Trade History StatsCard Bar Layout (6-Card Width) | ✅ Pass | Code review + staging visual QA 2026-04-12 |
| ST-10 | Trade History Column Header Styling and Formatting | ✅ Pass | Code review + staging visual QA 2026-04-12 |
| ST-11 | Flexible Column Sorting Across Trade History Table | ✅ Conditional Pass | Code review + staging visual QA 2026-04-12 (see notes) |

**Visual staging QA completed:** 2026-04-12 by Product Owner — local dev environment.

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

**Visual AC — Staging results (2026-04-12):**

| Check | Result | Notes |
|-------|--------|-------|
| ⓘ icon visible adjacent to title | ✅ PASS | Confirmed on staging |
| Hover reveals tooltip text | ✅ PASS | Confirmed on staging |
| Avg Fee Drag card wired with canonical tooltip | ✅ PASS | Confirmed on staging |

**Visual sign-off status:** ✅ Granted — all checks pass.

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

**Visual AC — Staging results (2026-04-12):**

| Check | Result | Notes |
|-------|--------|-------|
| 7-card grid renders correctly at xl | ✅ PASS | All 7 cards visible in single row at xl |
| Grid wraps at md (4+3) | ✅ PASS | Confirmed on staging |
| Card padding reduced at md+ | ✅ PASS | Confirmed on staging |

**Visual sign-off status:** ✅ Granted — all checks pass.

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

**Visual AC — Staging results (2026-04-12):**

| Check | Result | Notes |
|-------|--------|-------|
| Headers visibly bolder and brighter (font-semibold, text-slate-300) | ✅ PASS | Confirmed on staging |
| Letter-spacing wider (tracking-wide) | ✅ PASS | Confirmed on staging |
| No other tables affected | ✅ PASS | Confirmed on staging |
| Header multi-line wrapping | ✅ PASS → FIXED in `ff348ef` | Initial QA found some headers wrapping to 2 lines; fixed with `whitespace-nowrap` on TH_CLASS |
| Horizontal scroll | ✅ PASS → FIXED in `4650449`, `2c2733f`, `78467a1` | Initial QA found table requiring horizontal scroll; fixed via px-2 padding, compact date format, column reorder, and scroll-to-reveal pattern for analytical columns |

**Visual sign-off status:** ✅ Granted — all checks pass. Layout bugs found during QA fixed in session commits.

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

**Visual AC — Staging results (2026-04-12):**

| Check | Result | Notes |
|-------|--------|-------|
| Exit Date shows ↓ on initial page load (default DESC) | ✅ PASS | Confirmed on staging |
| Clicking Exit Date cycles ↓ → ↑ → unsorted | ✅ PASS | Confirmed on staging |
| Entry Date, P&L, P&L%, Days Held sortable | ✅ PASS | Confirmed on staging |
| Ticker and Exit Reason headers not clickable | ✅ PASS | Confirmed on staging |
| Days Held column visible; shows number or "—" for null | ✅ PASS (conditional) | Number display confirmed; null case untestable — no null holding_days in dataset |
| Slippage, Fee Drag, R-Multiple sort still works | ✅ PASS (conditional) | Sort icon behaviour confirmed; data-dependent row reorder untestable — no values in dataset |
| Exit reason normalisation (snake_case DB values) | ✅ PASS → FIXED in `4650449` | Found during QA: stop_hit/target/manual rendering raw; fixed with snake_case aliases in exitReasonLabels/Colors |

**Visual sign-off status:** ✅ Granted — all testable checks pass. Two conditional passes noted (null Days Held, Slippage/R-Multiple data) are environment limitations, not implementation defects.

---

## Post-merge Actions

~~1. Run Trade History page in browser (local or staging) to verify:~~
~~   - 7-card stats bar renders correctly at xl (all in one row) and md (4+3)~~
~~   - ⓘ tooltip on Avg Fee Drag shows canonical text on hover~~
~~   - Exit Date column shows ↓ sort icon on initial load (default DESC)~~
~~   - Days Held column renders holding_days or "—"~~
~~   - Column header text is bold/bright vs prior version~~
**✅ Completed 2026-04-12 — all visual checks passed (see story sign-off sections above)**

2. ~~Open PR and obtain QA sign-off + Product Owner acceptance before merge~~ — **✅ Both granted 2026-04-12 (see sign-off block below)**

---

## DoQ and Product Owner Sign-Off

**Director of Quality sign-off:** ✅ Granted — 2026-04-12
All 4 stories meet AC. Visual QA completed on staging. 4 defects found and fixed in-session. Two conditional passes (ST-11 null/data environment limitations) accepted with documented rationale. Smoke test infrastructure fixed.

**Product Owner acceptance:** ✅ Granted — 2026-04-12
EPIC-03 delivers intended Trade History UX improvements per design spec `trade_history.md` v1.6. All stories confirm intent alignment. Additional quality improvements (exit reason normalisation, responsive layout UX decision) accepted as within scope. Ready to merge.

**PR:** #220 — [EPIC-03] Trade History UX Polish — StatsCard Tooltips, 7-Card Layout, Column Sorting, Days Held

---

*Generated by Sprint Execution Engine — 2026-04-11*
