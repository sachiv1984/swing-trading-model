# trade_history.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.13
**Last Updated:** 2026-09-04 (v9.1 ST-07, BLG-SPEC-99: added §Keyboard Navigation Requirements)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v2.8 AI Journal Summary):** docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md
**Design Source (v2.6 UX polish):** docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md
**Design Source (v2.1 slippage):** docs/design/2026-03-18__release-v2.1/slippage-tracking/ux_spec.md
**Design Source (v3.5 additions):** docs/ux_specs/plan-vs-reality/ux_spec.md
**Design Source (v1.11 saved filters & calendar view):** docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md

## Purpose & User Goals
The Trade History page provides a complete record of all **closed trades**, allowing users to review past performance, analyze decisions, and learn from journal entries.

Users should be able to:
- Understand their long‑term trading performance  
- Review each closed trade in detail  
- Filter by tags, dates, outcomes, and markets  
- Read entry/exit notes using an expandable journal view  
- Compare winning vs losing trades  
- Identify behavioral or strategic patterns  

---

## Layout Structure

### Summary Stats
A row of key metrics:
- Total trades
- Win rate (%)
- Total P&L (GBP)
- Average winner
- Average loser
- **Avg Slippage** (new — v2.1, ST-14)
- **Avg Fee Drag** (new — v2.5, ST-09)

These values give the user an instant overview of performance quality.

#### Avg Slippage (Summary Stat)

| Property | Value |
|----------|-------|
| Label | **Avg Slippage** |
| Source | Backend-provided `avg_slippage_pct` (computed across all trades with Fill Price captured) |
| Format | Signed percentage to 2dp: e.g. `–0.05%`, `+0.12%`, `0.00%` |
| Colour | Negative (favourable) = green tone; Positive (unfavourable) = red tone; Zero = neutral |
| Null / no data | Display `—`; tooltip: `"No Fill Price data available yet."` |
| Placement | Second-rightmost stat in the summary row (Avg Fee Drag follows); wraps to second row on narrow screens |

#### Avg Fee Drag (Summary Stat — new v2.5, ST-09)

| Property | Value |
|----------|-------|
| Label | **Avg Fee Drag** |
| Source | Backend-provided `avg_fee_drag_pct` from GET /trades response envelope (mean of `fee_drag_pct` across all trades with `gross_proceeds > 0`) |
| Format | Always-positive percentage with `+` prefix: `+X.XX%` (e.g. `+0.42%`) |
| Colour | Amber/orange tone — fee drag is always a cost; not binary green/red |
| Null / no data | Not applicable — always populated when trades exist |
| Tooltip (ⓘ) | "Average Fee Drag = Total exit fees / Gross proceeds × 100" / "Higher % means a greater proportion of gross proceeds consumed by fees." |
| Placement | Rightmost stat in the summary row (after Avg Slippage); wraps to second row on narrow screens |
| Naming constraint | Label is "Avg Fee Drag" or "Fee Drag" — never "slippage" |
| Design source | `docs/design/2026-04-05__release-v2.5/fee-drag/ux_spec.md` |

#### Summary Stats Bar Layout (v2.6, ST-09)

| Breakpoint | Grid Columns | Behaviour |
|------------|-------------|-----------|
| Below `md` (<768px) | Stacked | Existing responsive behaviour unchanged |
| `md` (≥768px) | `grid-cols-4` | 4 cards in row 1, 3 cards in row 2 |
| `xl` (≥1280px) | `grid-cols-7` | All 7 cards in single row |

Card padding at `md`–`xl`: `px-3 py-3` (reduced from default to improve fit).  
No horizontal scroll. All 7 cards readable and unstacked at `xl` (≥1280px).  
Design source: `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md`

---

### Filters
A flexible filtering system allowing users to narrow down the list of trades.

**Available filters:**
- Date range  
- Win / Loss  
- Market (US / UK)  
- Exit reason  
- Tag filter (multi‑select)  
  - Shows all available tags  
  - Selected tags appear as removable pills  
  - Filtering uses OR logic (any trade containing at least one selected tag)

When no trades have tags, the tag filter does not appear.

---

### AI Journal Summary (v2.8 — ST-08, EPIC-04)

**Design source:** `docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md`

**Placement:** Collapsible section positioned above the Trade History table, below the filter bar.

**SRB compliance:** CONDITIONALLY COMPLIANT under SRB-v1.7 (2026-03-02). AI output is display-only; must NOT be used as input to any signal, scoring, compliance, or recommendation calculation.

#### Section Header

- Title: "AI Journal Summary"
- Subtitle: "AI-generated themes across your journal entries."
- Expand/collapse toggle (chevron icon); **collapsed by default** on page load.
- Session-only state (not persisted to localStorage).

#### When Collapsed (default)

Header row only visible. No API call made until the user expands.

#### When Expanded

**Disclaimer label (mandatory):**
> *"AI-generated summary — for reference only. Not a trading recommendation."*

- Displayed in a muted amber/info banner style above the summary text.
- Cannot be dismissed. Always visible whenever the summary is shown.
- No user interaction required to display it.

**Generate / Refresh button:**

| Property | Value |
|----------|-------|
| Label (first time) | "Generate Summary" |
| Label (after load) | "Refresh Summary" |
| Action | `POST /ai/journal-summary` with current filter context (date range and trade IDs from visible trades) |
| Placement | Section header row, right side (inline with title) |
| Disabled | While loading |

**Summary text panel:**

| Property | Value |
|----------|-------|
| Source | `summary` field from `POST /ai/journal-summary` response |
| Background | Distinct card — e.g. slate-800 or subtle differentiation from raw journal entries |
| Font | Regular body size; not journal-entry styling |
| Overflow | Max-height with scroll if content is long |

#### States

| State | Behaviour |
|-------|-----------|
| Not yet generated | Placeholder: "Click 'Generate Summary' to get an AI overview of your journal entries." |
| Loading | Spinner inside summary panel; button disabled |
| Loaded | Disclaimer above; summary text rendered |
| Error / Unavailable | "Summary unavailable. Please try again later." — muted; no error icon or technical message |

#### Hard Rules

- Section **collapsed by default** — opt-in per session; user must expand and click Generate.
- No auto-generation on page load.
- Filter context: summary covers the same trade scope as the currently visible filtered list. Pass trade IDs or date range to `POST /ai/journal-summary`.
- Disclaimer label is mandatory and must appear whenever the summary is shown — not dismissible.
- AI summary is display-only. It must NOT feed into any signal, scoring, compliance, or recommendation logic.
- **Strategy Rules owner sign-off required before merge** (AC in ST-08).

---

### Trade History Table
The main content area displays all closed trades in a table format.  
Columns include:

- Ticker
- Market flag
- Entry date
- Exit date
- Shares (fractional display)
- Entry price (native currency)
- Exit price (native currency)
- P&L (GBP)
- P&L %
- R-Multiple
- **Slippage** (new — v2.1, ST-14; positioned after P&L %)
- **Fee Drag %** (new — v2.5, ST-09; positioned after Slippage)
- Days held
- Exit reason

#### Slippage Column

**Formula (canonical):** `Slippage = (Fill Price − Market Price) / Market Price`

**Source field:** Backend-provided `slippage_pct` per trade (computed from Fill Price and Market Price at entry). The frontend does not calculate slippage.

**Display format:** Signed percentage to 2dp:
- `–0.08%` — filled below market (favourable, green tone per design system)
- `+0.12%` — filled above market (unfavourable, red tone per design system)
- `0.00%` — neutral (no colour treatment)

**Null handling:** If `slippage_pct` is null (Fill Price not captured — applicable to trades entered before v2.1): display `—` (em dash, muted, no colour).

**Column header tooltip:** An info icon (ⓘ) adjacent to the "Slippage" header. Hover:
> `"Slippage = (Fill Price − Market Price) / Market Price"`
> `"Negative slippage = filled below market price (favourable). Positive = above (unfavourable)."`

**Sortable:** Yes — ascending and descending. Null values sort to end.

**Historical trades:** Pre-v2.1 trades without Fill Price show `—`. The column is still rendered; it is not hidden when historical trades are present.

---

#### Fee Drag % Column (new — v2.5, ST-09)

**Formula (canonical):** `Fee Drag % = exit_fees / gross_proceeds × 100` (rounded to 2dp)

**Source field:** Backend-provided `fee_drag_pct` per trade from GET /trades response. The frontend does not calculate fee drag.

**Display format:** Always-positive percentage with `+` prefix:
- `+0.38%`, `+1.20%`, `+0.05%`
- Decimal precision: 2dp

**Colour treatment:** Amber/neutral tone — fee drag is always a cost; do NOT use green/red (reserved for P&L direction). Consistent with Avg Fee Drag StatsCard.

**Column header tooltip:** An info icon (ⓘ) adjacent to the "Fee Drag %" header. Hover:
> `"Fee Drag % = Exit fees / Gross proceeds × 100"`
> `"Measures the proportion of gross sale proceeds consumed by broker exit fees."`

**Null handling:** Not applicable — always populated for closed trades. No `—` state.

**Sortable:** Yes — ascending and descending. Ascending = lowest fee drag first.

**Naming constraint:** Column header is "Fee Drag %" — never "slippage".

**Design source:** `docs/design/2026-04-05__release-v2.5/fee-drag/ux_spec.md`

---

#### R-Multiple Column

**Calculation:** Frontend-only. Canonical formula (per `metrics_definitions.md` v1.5.7 --- Tier 1, Visualisation-Only):

```
R = (exit_price - entry_price) / (entry_price - stop_price)
```

**Data source:** `trades_for_charts` array from `GET /analytics/metrics`. Fields used:

-   `entry_price`
-   `exit_price`
-   `stop_price`

> **Note:** The Trade History table is currently sourced from `GET /trades`. R-multiple requires `stop_price`, which is not present in `GET /trades` (confirmed D2a --- absent from direct response). The R-multiple column reads from `trades_for_charts` via `GET /analytics/metrics` and is joined to the trade table by trade `id`. The page must call both endpoints when this column is visible.

**Null handling:** If a trade has no matching entry in `trades_for_charts`, or if `stop_price` is null or zero for that trade (denominator would be zero), display `---` (em dash) in the R-multiple cell. Do not show 0 or an error.

**Display format:** Signed to 2 decimal places with "R" suffix.

-   Positive: `+2.31R` (use profit colour --- green tone per design system)
-   Negative: `-0.87R` (use loss colour --- red tone per design system)
-   Zero: `0.00R` (neutral colour)
-   Missing: `---` (muted, no colour treatment)

**Colour treatment:** Follows profit/loss colour convention from `design_system.md`. Positive R is green, negative R is red. Thresholds (green ≤5%, amber ≤10% etc.) defined for the Drawdown widget do **not** apply here --- R-multiple uses binary profit/loss colouring only.

**Column sort:** Sortable ascending / descending. Trades with `---` sort to the end.

**Interaction:**  
- Clicking a row expands it to show the full journal.

---

#### Column Header Styling (v2.6, ST-10)

Trade History-specific override. Applied within the Trade History component (not a DataTable.js base style change — avoids regression to other tables).

Target class string: `text-xs font-semibold text-slate-300 uppercase tracking-wide`

Changes from DataTable.js default (`text-xs font-medium text-slate-400 uppercase`):
- `font-semibold` replaces `font-medium` — improved weight and legibility
- `text-slate-300` replaces `text-slate-400` — improved contrast on dark background
- `tracking-wide` added — improves uppercase character spacing

Design source: `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md`

---

#### Sortable Columns (v2.6, ST-11)

All sortable columns in the Trade History table:

| Column | Sort Behaviour | Status |
|--------|---------------|--------|
| Entry Date | Ascending = oldest first; descending = newest first | New — ST-11 |
| Exit Date | Ascending = oldest first; descending = newest first | New — ST-11 |
| P&L (GBP) | Ascending = worst P&L first | New — ST-11 |
| P&L % | Ascending = worst P&L % first | New — ST-11 |
| Days Held | Ascending = shortest hold first | New — ST-11 |
| Slippage | Ascending = best slippage first; nulls sort to end | Existing |
| Fee Drag % | Ascending = lowest fee drag first | Existing |
| R-Multiple | Ascending = worst R first; nulls sort to end | Existing |

**Default sort:** Exit Date descending (most recent trades first).

**Non-sortable:** Ticker, Market flag, Shares, Entry price, Exit price, Exit reason.

**Sort icon treatment:** Active sort column shows solid ↑ or ↓; hovering over sortable columns shows dimmed indicator. Consistent with existing Slippage/Fee Drag/R-Multiple behaviour.

Design source: `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md`

---

### Expandable Journal Row
The expanded row appears as a full‑width card below the trade’s main table row.

Contains up to four color‑accented sections (five for closed trades with a trade plan):

1. **Entry Analysis**  
   Shows the entry note.  
   Displays “No entry note” if empty.

2. **Exit Reflection**  
   Shows the exit note.  
   Displays “No exit note” if empty.

3. **Strategy Tags**  
   Tags displayed as colored pills.

4. **Plan vs Reality** *(v3.5 — ST-06 PO-01; conditionally rendered — see §Plan vs Reality below)*

5. **Post-Trade Debrief** *(v8.9 — ST-06 BLG-FEAT-90; always rendered for closed trades — see §Post-Trade Debrief below)*

The expandable card uses a clean, visually distinct layout to support long‑form reading.

---

### Plan vs Reality (v3.5 — ST-06 PO-01)

**Design source:** docs/ux_specs/plan-vs-reality/ux_spec.md

**Visibility:** Rendered as the 4th section of the Expandable Journal Row **only for closed trades** where `GET /trades/{id}/plan-vs-reality` returns HTTP 200 with a comparison record. The call is made lazily on row expand. Hidden (no section rendered, no placeholder) when response is 404 or `{“status”: “trade_open”}`.

**Section label:** “Plan vs Reality”

**Left accent border:** Blue (`#2563EB`, 4px) — distinguishes this section from entry/exit analysis sections.

#### Comparison Rows

| Row | Planned (muted) | Actual (bold) | Indicator |
|-----|-----------------|---------------|-----------|
| Entry Timing | “Planned zone: {entry_zone_description}” or “No entry zone recorded” | “Actual entry: {actual_entry_price}” | Pill: `On Time` (green) / `Early` (amber) / `Late` (amber) / `N/A` (grey) |
| Entry Delta | “Planned: {planned_entry_price}” or “—“ | “+X.XX%” / “−X.XX%” (two decimal places, signed) | Green if positive (entry below plan), red if negative (entry above plan). When `entry_delta_pct` is null: row shows “Entry delta: data not available for historical trades” in muted style — planned/actual columns not rendered. |
| R Achieved | “Target: {r_target}R” or “No R target set” | “{r_achieved}R” | Colour: green if ≥ target; amber if ≥ target × 0.8; red if < target × 0.8 |
| Exit Alignment | “Planned: {planned_exit_conditions}” or “No exit conditions” | “Actual: {actual_exit_reason}” | Pill: `Matched` (green) / `Partially Matched` (amber) / `Diverged` (red) |
| State at Exit | — | Lifecycle state badge (reuses Positions page badge design) | Per `positions.md §Position Lifecycle State Badge` colour scheme |

#### Null / Partial Data

- Individual null fields: display “—“ in planned value; show actual without comparative colour.
- Section entirely hidden if no plan vs reality record (404) — no “no plan” message shown.

#### Loading / Error

- On row expand (API in flight): single-line skeleton placeholder for the section.
- On 5xx or timeout: section hidden entirely; other sections unaffected.

#### API Dependency

| Endpoint | Purpose |
|----------|---------|
| `GET /trades/{id}/plan-vs-reality` | Returns plan vs reality comparison record. 404 when no trade plan. Called lazily on row expand. |

---

### Post-Trade Debrief (v8.9 — ST-06 BLG-FEAT-90)

**§13 review (CONDITIONAL, 9 binding conditions):** `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`

**Visibility:** Rendered as a section of the Expandable Journal Row for **every closed trade** (unlike Plan vs Reality, this section is not conditional on a linked trade plan existing). `GET /trades/{id}/debrief` is called lazily on row expand.

**Section label:** “Post-Trade Debrief”, with an “AI-generated” badge.

**Left accent border:** Violet, 4px — visually distinct from Plan vs Reality's blue accent.

#### Empty State (no debrief generated yet — 404)

Shows “No debrief generated yet for this trade.” and a **Generate Debrief** button (`data-testid="generate-debrief-btn"`). Clicking it calls `POST /trades/{id}/debrief` and renders the result on success. **§13 Condition 4:** no other button, link, or affordance may appear in this section — nothing here may auto-adjust strategy parameters, create a trade plan, or modify any other record.

#### Populated State (debrief exists)

- **Summary text:** the deterministic, non-AI factual plan-vs-reality summary — always present.
- **Focus area** (labelled “Focus area”, italic): the one AI-generated pattern-surfacing sentence, shown only when `focus_area_text` is non-null.
- When `focus_area_text` is null: a muted italic message explains why (`generation_status`-dependent — either AI generation was unavailable, or the §13 Condition 9 output-side compliance check failed twice and fell back). The summary still renders.
- A **Regenerate** button (`data-testid="regenerate-debrief-btn"`) re-runs `POST /trades/{id}/debrief`, overwriting the prior debrief.

#### Loading / Error

- On row expand (API in flight): single-line skeleton placeholder for the section.
- On generation failure: an inline error message; the empty-state Generate button remains available to retry.

#### API Dependency

| Endpoint | Purpose |
|----------|---------|
| `GET /trades/{id}/debrief` | Returns the existing debrief, or 404 if none generated yet. Called lazily on row expand. |
| `POST /trades/{id}/debrief` | Generates (or regenerates, overwriting) the debrief on demand. |

---

## Brokerage Cost Capture (v6.0 — ST-03)

**Design source:** `docs/design/2026-06-19__release-v6.0/net-of-costs-tracking/ux_spec.md`

Two new optional fields on the trade record edit form, in a **"Brokerage Costs"** subsection below existing P&L fields:

| Field | Label | Type | Required | Format |
|-------|-------|------|----------|--------|
| `commission_gbp` | **Commission (£)** | Decimal numeric | No | 2dp (e.g. 6.00) |
| `spread_cost_gbp` | **Spread Cost (£)** | Decimal numeric | No | 2dp (e.g. 2.40) |

**Validation:** Non-numeric input → "Enter a number (e.g. 6.00)". Zero is valid. Both fields default to empty (null) — existing trades are unaffected.

---

## Net-of-Costs R-Multiple Display (v6.0 — ST-03)

**Design source:** `docs/design/2026-06-19__release-v6.0/net-of-costs-tracking/ux_spec.md`

Net R is displayed **only when** at least one of `commission_gbp` or `spread_cost_gbp` is non-null and non-zero on the trade record.

### Trade History Table

In the R-Multiple column, when cost data is present:
- Gross R shown in normal weight (existing display; unchanged)
- Net R shown directly below in smaller, muted text: "Net: –0.85R"

When no cost data: column behaves identically to current spec.

### Expanded Trade Row

| Label | Condition |
|-------|-----------|
| Gross R | Always shown (existing behaviour) |
| Net R (after costs) | Shown only when cost data present |

**Net R colour:** Positive → green; Negative → red; Zero → neutral grey. Matches gross R colour convention.

---

## Saved Filter Presets & Calendar View (v7.5 — ST-04 BLG-FE-118)

**Design source:** `docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md`
**Depends on:** `docs/specs/blg_fe_118_pre_implementation_readiness_pass.md` (`saved_filters` schema, day-bucketed realised-P&L date sourcing, realised/unrealised split constraint)

**Placement decision:** Trade History was chosen as the single home for both features — it has the richest existing filter set of any page (§Filters: date range, win/loss, market, exit reason, tags) and the calendar's date sourcing is built on `trade_history.exit_date`, the same field already driving the Exit Date column and default sort.

### Saved Filter Presets

Below the existing §Filters row:

- **"Save current filters as…"** — visible whenever 1+ filters are active. Opens an inline name input (max 100 chars); submits `POST /saved-filters` with `{ name, filter_state }`. Duplicate name (`400`, `UNIQUE (portfolio_id, name)`) shows inline error: `"A preset named '{name}' already exists."`
- **"Saved filters"** dropdown lists all `GET /saved-filters` rows by name; selecting one applies its `filter_state` to the active filter controls (overwrites current selection; does not auto-resave).
- Each preset has a delete (×) affordance with inline confirmation: `"Delete preset '{name}'?"` — calls `DELETE /saved-filters/{id}`. Deleting a preset does not affect the currently-active filter selection.

**Persistence distinction:** the currently-active filter selection remains the existing ephemeral, versioned-localStorage-envelope pattern (reusing the `BLG-FE-40` pattern already implemented for `RedFlagJournal.js`) — independent of saved presets, which are server-side `saved_filters` rows persisting across devices/sessions.

### Calendar View

A **Table** / **Calendar** view toggle at the top of the page, alongside the filter row. Table remains the default and unchanged; Filters, Saved Filters, and Summary Stats remain visible and functional in both views.

Calendar view renders a standard month-grid (`react-day-picker`, single-month mode, prev/next navigation). Each day cell with 1+ trade exits (`exit_date`) shows a compact realised-P&L indicator (green/red dot); hovering shows `"+£240.50 (3 trades)"` style detail. Clicking a day with exits switches to Table view with the date range filter set to that single day (reuses the existing Date range filter — no new detail view). Empty days are not clickable.

**Unrealised P&L:** never shown per-day (not date-attributable — no historical daily mark-to-market source exists). Shown once, in a summary banner above the grid: `"Unrealised P&L (as of today): {value}"` — reuses the exact wording/treatment already used on the Monthly P&L and Tax Year reports.

**Empty state:** a month with zero exits still renders the grid (no indicators). If the account has no closed trades at all, the standard full-page `DataState` empty state is shown above the grid instead: `"No closed trades yet."` / `"Your trading calendar will populate as you close trades."`

### §13 Compliance

Both features are read-only presentation/filtering conveniences over existing trade history data or user-authored filter names. No automated decision-making or recommendation logic.

---

## Key Components Used
- Trade summary cards  
- Filters and tag selector  
- Trade table  
- Expandable journal card  
- Tag pills  

---

## States

### Loading State
- Table skeleton rows while fetching closed trades  
- Summary stats show placeholder values  

### Empty State
Shown when:
- No trades exist  
- Filters hide all results  

Displays:
- Message explaining no trades match the criteria  
- Option to reset filters  

### Error State
- Global error banner for failed trade history fetch  
- Retry button available  

---

## Responsive Behavior
- Table collapses into stacked cards on narrow screens  
- Journal expansion becomes a vertical panel under each card  
- Filters collapse into a drawer or stacked inputs on mobile  
- Tags wrap into multiple lines  

---

## UX Notes
- The journal experience should feel educational and reflective, not cramped  
- Tag filtering helps users spot patterns (e.g., “momentum” trades)  
- P&L values should use clear profit/loss color coding  
- Expandable rows should animate smoothly and feel discoverable  
- Users should be able to navigate back and forth between trades without losing filter context  

---

## Keyboard Navigation Requirements (v1.13 — ST-07, BLG-SPEC-99, EPIC-01, v9.1)

Documentation-only requirements baseline for this table-based page — no implementation change ships with this addition; conformance is verified per-component as each is next touched.

- **Trade History Table:** row order is the DOM/tab order; each row's expand control (Expandable Journal Row) is reachable via Tab and toggles on Enter or Space, exposing its expanded/collapsed state to assistive tech (`aria-expanded` or equivalent).
- **Expandable Journal Row / Plan vs Reality / Post-Trade Debrief:** once a row is expanded, its interactive controls (journal tag editor, Generate/Regenerate Debrief action) follow the row in tab order — a user tabbing through an expanded row never has to tab past the entire remaining table to reach that row's own controls.
- **Filters:** all filter inputs (including Saved Filter Presets) are reachable via Tab and operable via keyboard alone (text entry, select, or button activation — no filter control that requires a mouse-only interaction, e.g. drag).
- **Calendar View:** day cells are reachable via Tab in calendar (row-major) order; Enter or Space on a focused day cell performs the same day-click navigation to Table view filtered to that date as a mouse click.
- **AI Journal Summary:** if interactive (e.g. a regenerate action), it follows the same Tab-reachable / Enter-or-Space-activates rule as other row-level actions above.
- **Focus indicator:** every interactive element above renders a focus indicator meeting design_system.md's "Focus indicator contrast" rule (≥3:1 against adjacent colour, both themes).

---

## Known Deviations

### DEV-ST14-01 — Avg Slippage StatsCard renders without gradient (cosmetic) — Resolved

- **Description:** `TradeHistory.js` passed `color="cyan"` to the Avg Slippage `StatsCard`. The `StatsCard` gradient map has no `"cyan"` key — the card rendered without the expected gradient background. All non-null slippage states (negative/emerald, positive/rose) use colour-coded values at cell level, so this was a cosmetic regression on the summary card only.
- **Canonical requirement:** Avg Slippage `StatsCard` renders with a gradient background consistent with other stat cards on the page.
- **Priority:** P3
- **Status:** ✅ Resolved — v2.5 (2026-04-06)
- **Resolution:** Fixed in two stages: commit `8650223` ([EPIC-03][ST-07]) changed to `gradient="violet"`; commit `67d7285` ([EPIC-05][ST-12]) updated to conditional `gradient={avg_slippage_pct <= 0 ? "emerald" : "rose"}` for the data-present state. Current code uses valid gradient keys for all states (emerald/rose when data present, violet when null). Full detail: `docs/testing/slippage_scenarios.md#DEV-ST14-01`.
- **Owner:** Frontend Specifications & UX Documentation Owner
- **Backlog reference:** BLG-FE-08 — Fix Avg Slippage StatsCard gradient rendering *(supersedes BLG-FE-01, archived)*
- **Acceptance record:** Director of Quality 2026-03-20 (original finding); Director of Quality 2026-04-06 (resolution confirmed).
- **Consolidation note (ST-12, EPIC-04, v8.1, 2026-08-03):** This entry was found still marked unresolved here despite `docs/testing/slippage_scenarios.md`'s sibling entry recording resolution since 2026-04-06 — a spec/QA-doc resolution-status drift, corrected by this update. See `docs/governance/deviation_consolidation_review_2026-08-03.md` Finding 3.

---

## Change Log

| Version | Date | Change |
| --- | --- | --- |
| 1.13 | 2026-09-04 | v9.1 ST-07 (BLG-SPEC-99, EPIC-01): added §Keyboard Navigation Requirements — documentation-only baseline covering Trade History Table row/expand tab order, Expandable Journal Row / Plan vs Reality / Post-Trade Debrief control tab order, Filters (incl. Saved Filter Presets), Calendar View day-cell keyboard activation, and focus-indicator contrast. No implementation change. |
| 1.12 | 2026-08-20 | v8.9 (ST-06, EPIC-02, BLG-FEAT-90): Post-Trade Debrief section added to Expandable Journal Row — 5th section, rendered for every closed trade (not conditional on a linked plan, unlike Plan vs Reality); deterministic summary text always shown, one AI-generated pattern-surfacing "focus area" sentence shown when present; on-demand Generate/Regenerate action (`POST /trades/{id}/debrief`) since generation is not hooked into the live trade-close event path; §13 review CONDITIONAL (9 binding conditions) — Condition 4 requires no other action affordance in this section. Design decision documented directly in this spec (no separate ux_spec.md — component mirrors the existing Plan vs Reality precedent closely enough that a dedicated design artefact was not required). Approved: Product Owner 2026-08-20 (agent-mediated). |
| 1.11 | 2026-07-17 | v7.5 design gate — added §Saved Filter Presets & Calendar View (ST-04, BLG-FE-118): named saved filter presets (new `saved_filters` table, server-side, distinct from the existing ephemeral localStorage active-filter state), Table/Calendar view toggle, month-grid with day-level realised-P&L indicators sourced from `exit_date`, day-click navigates to Table view filtered to that date, unrealised P&L shown once as a summary banner (never per-day). Design source: saved-filters-calendar-view/ux_spec.md. Approved: Product Owner 2026-07-17. Design gate: 2026-07-17__release-v7.5. Head of Specs Team confirmed. |
| 1.10 | 2026-06-19 | v6.0 design gate — Brokerage Cost Capture section added: two new optional trade edit form fields (commission_gbp, spread_cost_gbp) in "Brokerage Costs" subsection. Net-of-Costs R-Multiple Display section added: Net R shown below Gross R in table and expanded row when cost data present; absent when no cost data (backward-compatible). Design source: net-of-costs-tracking/ux_spec.md. Approved: Product Owner 2026-06-19. Head of Specs Team confirmed. |
| 1.9 | 2026-05-16 | v3.6 design gate (ST-02, EPIC-01): Entry Delta row added to Plan vs Reality comparison table — displays `entry_delta_pct` as signed percentage (+X.XX%/−X.XX%) with green/red colouring; null state shows "Entry delta: data not available for historical trades" in muted style. API source: `GET /trades/{id}/plan-vs-reality` `entry_delta_pct` field (added in ST-01). Head of UX & Design confirmed 2026-05-16. |
| 1.8 | 2026-05-15 | v3.5 design gate: (ST-06 PO-01) Plan vs Reality section added to Expandable Journal Row — 4th section, conditionally rendered for closed trades with a trade plan; displays entry timing accuracy, R achieved vs R target (colour-coded), exit alignment badge, lifecycle state at exit badge; lazy-loaded on row expand via `GET /trades/{id}/plan-vs-reality`; hidden entirely when 404 (no plan). Design source: docs/ux_specs/plan-vs-reality/ux_spec.md. Approved: Product Owner 2026-05-15. |
| 1.7 | 2026-04-17 | v2.8 design gate (ST-08, EPIC-04): AI Journal Summary section added — collapsible section above trade table (below filters), collapsed by default, disclaimer always visible when expanded, Generate/Refresh button calls `POST /ai/journal-summary` with filter context, 4 states (not-generated/loading/loaded/error). SRB-v1.7 conditional compliance constraints documented. Strategy Rules sign-off required before merge. Design source: `docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md`. Head of Specs Team confirmed compliant. |
| 1.6 | 2026-04-11 | v2.6 design gate: (ST-09) Summary Stats Bar Layout spec added — `grid-cols-7` at `xl`, `grid-cols-4` at `md`, 7-card row; (ST-10) Column Header Styling spec added — Trade History-specific override (`text-xs font-semibold text-slate-300 uppercase tracking-wide`); (ST-11) Sortable Columns section added — 8 sortable columns, Exit Date descending as default sort. Design source: `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md`. Head of Specs Team confirmed compliant. |
| 1.5 | 2026-04-06 | v2.5 design gate (ST-09): Avg Fee Drag StatsCard added to Summary Stats section (after Avg Slippage). Fee Drag % column added to Trade History Table columns list (after Slippage). Fee Drag % Column spec section added. Design source: `docs/design/2026-04-05__release-v2.5/fee-drag/ux_spec.md`. Head of Specs Team confirmed compliant. |
| 1.4 | 2026-04-04 | OA-2 closure (v2.4): DEV-ST14-01 entry updated — Target resolution release v2.2→v2.5 (not resolved in v2.2/v2.3/v2.4; carried forward as delegated_frontend constraint); backlog reference BLG-FE-01→BLG-FE-08; DoQ acceptance reconfirmed at v2.4 verification. Head of Specs Team action per verification_report.md §5 and closure_record.md OA-2. |
| 1.3 | 2026-03-21 | Post-ship closure: Known Deviations section added. DEV-ST14-01 (StatsCard gradient cosmetic) filed per post_ship_closure STEP 5 — deviation compliance. |
| 1.2 | 2026-03-18 | v2.1 slippage tracking (ST-14, BLG-FEAT-03): Slippage column added to trade history table (after P&L %, before R-Multiple). Avg Slippage stat added to summary stats bar. Column header info tooltip specced. Null handling for pre-v2.1 trades (show `—`). Lifecycle headers upgraded to Class 1 compliant format. Design source: docs/design/2026-03-18__release-v2.1/slippage-tracking/ux_spec.md. Design gate: 2026-03-18__release-v2.1. |
| 1.1 | 2026-02-25 | BLG-FEAT-02: Add R-Multiple column specification. Frontend-only calculation from trades_for_charts. Null handling for missing stop_price. Display format with signed R suffix and profit/loss colour. QWB D2, D2a. |
| 1.0 | 2026-02-18 | Initial version. |
