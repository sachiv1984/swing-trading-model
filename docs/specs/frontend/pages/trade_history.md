# trade_history.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.5
**Last Updated:** 2026-04-06
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v2.1 slippage):** docs/design/2026-03-18__release-v2.1/slippage-tracking/ux_spec.md

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

### Expandable Journal Row
The expanded row appears as a full‑width card below the trade’s main table row.

Contains three color‑accented sections:

1. **Entry Analysis**  
   Shows the entry note.  
   Displays “No entry note” if empty.

2. **Exit Reflection**  
   Shows the exit note.  
   Displays “No exit note” if empty.

3. **Strategy Tags**  
   Tags displayed as colored pills.

The expandable card uses a clean, visually distinct layout to support long‑form reading.

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

## Known Deviations

### DEV-ST14-01 — Avg Slippage StatsCard renders without gradient (cosmetic)

- **Description:** `TradeHistory.js` passes `color="cyan"` to the Avg Slippage `StatsCard`. The `StatsCard` gradient map has no `"cyan"` key — the card renders without the expected gradient background. All non-null slippage states (negative/emerald, positive/rose) use colour-coded values at cell level, so this is a cosmetic regression on the summary card only.
- **Canonical requirement:** Avg Slippage `StatsCard` renders with a gradient background consistent with other stat cards on the page.
- **Priority:** P3
- **Target resolution release:** v2.5 *(originally v2.2; not resolved in v2.2, v2.3, or v2.4 — carried forward as delegated_frontend styling constraint per v2.4 sprint execution)*
- **Owner:** Frontend Specifications & UX Documentation Owner
- **Backlog reference:** BLG-FE-08 — Fix Avg Slippage StatsCard gradient rendering *(supersedes BLG-FE-01, archived)*
- **Acceptance record:** Director of Quality 2026-03-20 — P3 cosmetic only; slippage logic, values, and sorting correct. Reconfirmed v2.4 delivery verification 2026-04-03 (verification_report.md §4).

---

## Change Log

| Version | Date | Change |
| --- | --- | --- |
| 1.5 | 2026-04-06 | v2.5 design gate (ST-09): Avg Fee Drag StatsCard added to Summary Stats section (after Avg Slippage). Fee Drag % column added to Trade History Table columns list (after Slippage). Fee Drag % Column spec section added. Design source: `docs/design/2026-04-05__release-v2.5/fee-drag/ux_spec.md`. Head of Specs Team confirmed compliant. |
| 1.4 | 2026-04-04 | OA-2 closure (v2.4): DEV-ST14-01 entry updated — Target resolution release v2.2→v2.5 (not resolved in v2.2/v2.3/v2.4; carried forward as delegated_frontend constraint); backlog reference BLG-FE-01→BLG-FE-08; DoQ acceptance reconfirmed at v2.4 verification. Head of Specs Team action per verification_report.md §5 and closure_record.md OA-2. |
| 1.3 | 2026-03-21 | Post-ship closure: Known Deviations section added. DEV-ST14-01 (StatsCard gradient cosmetic) filed per post_ship_closure STEP 5 — deviation compliance. |
| 1.2 | 2026-03-18 | v2.1 slippage tracking (ST-14, BLG-FEAT-03): Slippage column added to trade history table (after P&L %, before R-Multiple). Avg Slippage stat added to summary stats bar. Column header info tooltip specced. Null handling for pre-v2.1 trades (show `—`). Lifecycle headers upgraded to Class 1 compliant format. Design source: docs/design/2026-03-18__release-v2.1/slippage-tracking/ux_spec.md. Design gate: 2026-03-18__release-v2.1. |
| 1.1 | 2026-02-25 | BLG-FEAT-02: Add R-Multiple column specification. Frontend-only calculation from trades_for_charts. Null handling for missing stop_price. Display format with signed R suffix and profit/loss colour. QWB D2, D2a. |
| 1.0 | 2026-02-18 | Initial version. |
