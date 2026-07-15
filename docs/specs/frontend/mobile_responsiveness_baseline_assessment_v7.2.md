**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-15
**Story:** ST-01 (BLG-FE-55, EPIC-01, v7.2)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Mobile Responsiveness Baseline Assessment

## 1. Purpose

Establish a baseline read of mobile-viewport readiness across the four highest-traffic surfaces ahead of v7.2's dashboard and trade-plan UX hardening work (EPIC-02 `ST-03`, EPIC-03 `ST-05`/`ST-06`). This is a static-code assessment (structural review of Tailwind breakpoint usage, layout primitives, and component composition) — it does not include live-device or emulator visual verification. Findings that require live-device confirmation are flagged explicitly in §6.

## 2. Gate Condition Note (AC-03)

**Arc 5 completeness gate: not yet met.** Per `run_manifest.md` (this cycle's rebalance carry-forward): "PO-02/PO-04 (Arc 5, out of v7.2 scope) not re-queried." The Arc 5 drift/compliance frontend surfaces (`Arc5ComplianceSection` and related) remain partially unbuilt per `claude/backlog/backlog.md` (BLG-FEAT-44, and the drift-detection frontend gap noted against the v4.6 shipped backend). This assessment proceeds under the Product Owner's explicit priority override recorded in `sprint_backlog.md` — it is **not** a resolution of the Arc 5 gate, and Arc 5 surfaces are out of scope for this assessment.

## 3. Scope Assessed (AC-02)

| Surface | File(s) | Assessed |
|---|---|---|
| Positions | `src/pages/Positions.js` | Yes |
| Screener | `src/pages/Screener.js` | Yes |
| Trade plan form | `src/pages/TradePlan.js` | Yes |
| Trade entry form | `src/pages/TradeEntry.js` | Yes (adjacent surface, shares the linkage risk noted in EPIC-02 `ST-02` AC-07) |
| Red Flag Journal | `src/pages/RedFlagJournal.js` | Yes |
| Dashboard (widget grid) | `src/pages/Dashboard.js`, `src/pages/DashboardHome.js` | Yes |
| App shell / navigation | `src/Layout.js` | Yes (context baseline) |

## 4. Method

For each file: grep-based inventory of Tailwind responsive prefixes (`sm:`/`md:`/`lg:`/`xl:`), table markup and its overflow handling, and grid/flex layout primitives lacking a responsive variant. Cross-referenced against the stated pattern in `docs/specs/frontend/design_system.md` §Responsive Behavior ("Tables collapse into card layouts on mobile"; "Sidebar-style navigation condenses into a mobile menu where applicable").

## 5. Findings

### 5.1 App shell — baseline is sound
`src/Layout.js` implements a working `lg:hidden` mobile hamburger menu (slide-in drawer, backdrop, `Menu` icon trigger). Global navigation is not a gap.

### 5.2 Positions — table view does not follow the documented mobile pattern (Moderate)
`Positions.js` offers two view modes: a `grid` mode (`PositionCard`, laid out `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` — correctly responsive) and a `table` mode (`DataTable`, 14 columns: Ticker, Entry Price, Current Price, Stop, Shares, P&L (GBP), P&L %, Days, State, Grace, Earnings, Alerts, Last Reviewed, Actions).

The `DataTable` primitive (`src/components/ui/DataTable.js`) wraps its `<table>` in `overflow-x-auto`, so the table view does not visually break on narrow viewports — it becomes horizontally scrollable. However:
- No column is hidden or reprioritised at any breakpoint (no `md:table-cell`-style progressive disclosure, unlike `Screener.js` — see 5.3).
- Cell padding (`px-6 py-4` in both `TableHead` and `TableCell`) is sized for desktop density, which lengthens the horizontal scroll distance on mobile.
- `design_system.md` states tables should "collapse into card layouts on mobile" — the card layout exists (`grid` view mode) but is not the default and is not breakpoint-driven; a mobile user landing on `table` mode (e.g. as their last-used preference) gets a 14-column horizontally-scrolling table rather than an automatic card fallback.

### 5.3 Screener — partial progressive disclosure already in place (Low / informational)
`Screener.js`'s results table is wrapped in `overflow-x-auto` (line 824) and uses `md:table-cell` (4 instances) / `lg:table-cell` (2 instances) to progressively reveal columns at wider breakpoints — the better-precedented pattern of the two table surfaces reviewed. Coverage is partial (not every secondary column has a breakpoint-gated cell), but the pattern itself is sound and is the one worth generalising rather than reinventing when EPIC-03's `ST-05`/`ST-06` implementation work begins.

### 5.4 Trade entry / trade plan forms — inconsistent responsive stacking on numeric field pairs (Moderate)
Both forms mix responsive and non-responsive grid layouts for paired fields:
- `TradeEntry.js` lines 240 and 319: `grid grid-cols-2 gap-4` with no responsive prefix — two form-field pairs render side-by-side at all viewport widths, including narrow mobile.
- `TradePlan.js` line 783: `grid grid-cols-2 gap-3` (Planned Entry Price / Planned Stop Price) — same pattern, no mobile stacking fallback.
- By contrast, `TradePlan.js` lines 639 and 668 correctly use `grid-cols-1 md:grid-cols-3` / `grid-cols-1 md:grid-cols-2` — the responsive pattern is present and working elsewhere in the *same file*, making this an inconsistency rather than a missing capability.

Risk: on a ~320–375px viewport, two side-by-side numeric inputs (each with a placeholder like "e.g. 150.00") are prone to label/placeholder truncation and reduced tap-target width. This is directly relevant to EPIC-02 `ST-02` AC-07's flagged regression risk on `TradeEntry.js` validation/submission for the upcoming `ST-03` "Start Trade from Plan" work — the same non-responsive grid instance is in the direct path of that story's UI change.

### 5.5 Red Flag Journal — no structural gap found (Low / informational)
`RedFlagJournal.js` is built almost entirely from `flex` / `flex-wrap` / `flex-col` primitives rather than fixed-column grids (filter bar: `flex flex-wrap gap-3 items-end`; list rows: `flex items-start gap-4`). This composition degrades gracefully by construction — no un-prefixed multi-column grid was found. No action item raised here; recommend confirming with a live-device pass only if capacity allows, not as a required follow-up.

### 5.6 Dashboard — widget grid is responsive; drag-and-drop reorder is an open question (Low, needs live verification)
`Dashboard.js` widget containers use `sm:grid-cols-2` / `lg:grid-cols-4` / `lg:col-span-1` — responsive at the grid level. The dashboard supports drag-and-drop widget reordering via `@hello-pangea/dnd` (`DragDropContext`/`Droppable`/`Draggable`). Drag-and-drop interaction patterns are frequently touch-hostile (accidental scroll-vs-drag conflicts, missing long-press affordance) but this cannot be confirmed or ruled out from static code alone — it depends on runtime touch-sensor configuration not visible in JSX. Flagged for live-device verification, not filed as a defect.

## 6. Items Requiring Live-Device Verification (not resolvable by static review)

1. Dashboard drag-and-drop widget reorder — touch behaviour (§5.6).
2. Actual rendered column count/legibility of the Positions table-view horizontal scroll on a real 375px-class device (§5.2) — static review confirms the mechanism (`overflow-x-auto`) exists but not its felt usability.
3. `RedFlagJournal.js` filter-bar wrap behaviour under real content lengths (§5.5) — low priority.

## 7. Recommendations (informational — no implementation in this item's scope)

- When EPIC-03 `ST-05`/`ST-06` land, prefer generalising `Screener.js`'s `md:`/`lg:table-cell` progressive-disclosure pattern (§5.3) over inventing a new one for other tables.
- When EPIC-02 `ST-03` touches `TradeEntry.js`, apply a responsive prefix (`grid-cols-1 sm:grid-cols-2`) to the two un-prefixed `grid-cols-2` instances (lines 240, 319) while validation/submission behaviour is already under test per `ST-02` AC-07 — bundling the fix avoids a second pass over the same file. Same applies to `TradePlan.js` line 783 if that story's scope touches the planned entry/stop price fields.
- No action recommended for Red Flag Journal or the app shell.

## 8. Known Deviations

None. This is a net-new assessment report; there is no prior canonical spec it could deviate from.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-15 | 1.0 | Initial baseline assessment (ST-01, EPIC-01, v7.2) |
