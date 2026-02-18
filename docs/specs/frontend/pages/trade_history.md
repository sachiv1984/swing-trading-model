# trade_history.md

**Owner:** Frontend Specifications & UX Documentation Owner  
**Status:** Canonical  
**Version:** 1.0
**Last Updated:** February 18, 2026

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
- Days held  
- Exit reason  

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
