# positions.md

**Owner:** Frontend Specifications & UX Documentation Owner  
**Status:** Canonical  
**Version:** 1.2  
**Last Updated:** February 18, 2026

---

## Purpose & User Goals
The Positions page provides an overview of all **open positions**, including their performance, stop levels, days held, and journal information.  
Its primary purpose is to help users:

- Monitor active trades  
- Identify positions requiring attention (e.g., approaching stops, in grace period)  
- Access entry/exit workflows  
- Review or edit journal notes and tags  
- Switch between different views depending on the task (table, grid, journal)

---

## Layout Structure

### View Switcher
A three‑way toggle enabling users to switch between:

1. **Grid View** – Card‑based layout showing key metrics  
2. **Table View** – Detailed, sortable table of positions  
3. **Journal View** – All positions displayed with notes, tags, and filters for reflection

Each view replaces the entire main content area. Switching views does not trigger a new data fetch — the same position data drives all three views.

---

### Table View (default)
Displays each open position as a row with:

- Ticker  
- Market flag (US / UK)  
- Entry price (native currency)  
- Current price (native currency)  
- Stop price  
  - Shows £0.00 / $0.00 during grace period  
- Shares (supports fractional values)  
- P&L (GBP)  
- P&L %  
- Days held  
  - Grace period indicator if under minimum hold days  
- Status badge (GRACE / PROFITABLE / LOSING)  
- Tags (as colored pills)  
- Actions:  
  - **Exit** (opens exit modal)  
  - **View Journal** (opens position detail modal)

---

### Grid View
Cards show a summarized snapshot of each position including:

- Ticker & market  
- Entry vs current price  
- P&L  
- Stop level  
- Days held  
- Tags  
- Quick links to exit or view notes

Designed for readability and scannability.

---

### Journal View

The Journal View is a dedicated reflection interface accessible from the view switcher. It exists to support trade review, pattern recognition, and learning — the user's goal here is different from the Table and Grid views. They are not monitoring live positions; they are reading their own documented reasoning and outcomes.

#### Scope
- Shows **all positions** — both open and closed — unlike Table and Grid views which show only open positions.
- No live price refresh is needed. The data is sourced from the same position dataset already held by the page.

#### Filter Bar
The filter bar appears above the timeline and contains four independent filters that combine (AND logic — a position must satisfy all active filters):

| Filter | Type | Behaviour |
|--------|------|-----------|
| **Search** | Text input | Searches entry note and exit note content. Case-insensitive. Hides positions with no match in either note field |
| **Tag filter** | Multi-select dropdown | Selecting one or more tags hides positions that do not have at least one of the selected tags. Selected tags appear as dismissible pills below the dropdown |
| **Win / Loss** | Single-select (All / Winners / Losers) | Winners: P&L ≥ 0. Losers: P&L < 0. Defaults to All |
| **Date range** | From / To date inputs | Filters on entry date. Either bound is optional |

Active tag selections persist as dismissible pills below the filter row, allowing users to see and clear individual tag selections without reopening the dropdown.

Clearing all filters returns the full position list. Filters do not persist across view switches or page reloads.

#### Position Cards (Timeline Layout)
Positions are displayed as a vertical timeline of cards, ordered with the most recently entered position first.

Each card always shows:
- **Ticker** and market badge  
- **CLOSED** badge (for closed positions only)  
- **Entry date**  
- **P&L badge** — profit/loss amount with percentage, color-coded (green / red). For open positions, reflects current unrealised P&L. For closed positions, reflects realised P&L  
- **Entry note** — displayed in full if present. No truncation in this view; the Journal View is a reading experience  
- **Tags** — all tags displayed as pills

For **closed positions only**, an expand control appears at the bottom of the card if an exit note exists:
- Label: "Exit Details" with chevron icon and the exit date shown on the right  
- Clicking expands to reveal the exit note beneath  
- The section collapses and expands with animation  
- Only one position's exit details can be expanded at a time  

#### Empty States
Two distinct empty states:

- **No positions at all**: Shown when the user has no positions of any kind. The card should explain the view is empty and offer a path to enter a position.  
- **No results match current filters**: Shown when positions exist but none match the active filter combination. The message should indicate filters are hiding results and make it easy to clear them. Does not offer a "enter new position" action — the user is in a review context, not an entry context.

---

## Key Components Used
- Position cards  
- Positions table  
- Journal cards (see `journal_components.md` — Expandable Journal Card)  
- Exit Position Modal  
- Position Detail Modal (journal editor)  
- Tag pills (see `journal_components.md` — Tag List)  
- Tag editor with autocomplete (see `journal_components.md` — Tag Editor)  
- View switcher control  

---

## States

### Loading State
- Skeleton rows or card placeholders  
- During initial load or refresh after exit

### Empty State
Shown when no open positions exist (Table / Grid views):
- Message explaining there are no active trades  
- Action: "Enter New Position"

For Journal View empty states, see the Journal View section above.

### Error State
- Global error banner if positions list fails to load  
- Retry option for re‑fetching data

---

## API Dependencies

| Endpoint | Purpose |
|----------|---------|
| `GET /positions` | Primary data source for all three views. Returns open positions with live pricing and journal fields. Journal View uses the same data but also displays any closed positions held in the dataset |
| `GET /positions/tags` | Tag autocomplete source for the Journal View filter dropdown and for the Position Detail Modal's tag editor |

> For full dependency behaviour rules, see `patterns/api_dependencies.md`.

---

## Responsive Behavior
- Table collapses to cards on smaller screens  
- Grid view reduces card width and stacks vertically  
- Journal cards expand to full width on mobile  
- Filter bar stacks vertically on narrow screens; tag pills wrap  
- Action buttons move below card content on mobile  
- Tags wrap gracefully on narrow screens  

---

## UX Notes
- Grace period must be visually clear and distinguishable from normal stop logic  
- Tags should be easily scannable and visually grouped  
- Exit action should always feel safe — a modal confirmation protects from accidental exits  
- Journal editing should feel lightweight, using inline editors where possible  
- The user should be able to switch between views without losing filtering or scroll position  
- Data should update smoothly after exits or journal edits  
- The Journal View is a **reading and reflection experience**, not a live monitoring surface. Layout and density decisions should reflect this: more vertical space per entry, no live price indicators, no stop-level warnings