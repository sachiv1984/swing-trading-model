# trade_history.md

**Owner:** Frontend Specifications & UX Documentation Owner  
**Status:** Canonical  
**Version:** 1.1
**Last Updated:** February 22, 2026

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

These values give the user an instant overview of performance quality.

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
- Days held  
- Exit reason

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

## Change Log

| Version | Date | Change |
| --- | --- | --- |
| 1.1 | 2026-02-25 | BLG-FEAT-02: Add R-Multiple column specification. Frontend-only calculation from trades_for_charts. Null handling for missing stop_price. Display format with signed R suffix and profit/loss colour. QWB D2, D2a. |
| 1.0 | 2026-02-18 | Initial version. |
