# positions.md

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
3. **Journal View** – All positions displayed with notes and tags

Each view replaces the entire main content area.

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
A dedicated journaling interface accessible from the view switcher:

- Shows **all positions** (open and closed)
- Each card includes:  
  - Ticker, market  
  - Entry/exit dates  
  - P&L (with color coding)  
  - Entry note preview (truncated)  
  - Exit note preview (if closed)  
  - Tags  
  - “View Full Journal” button

Filtering and sorting available:
- Tag filter  
- Open/closed filter  
- Date, P&L, and holding‑period sort options

---

## Key Components Used
- Position cards  
- Positions table  
- Journal cards  
- Exit Position Modal  
- Position Detail Modal (journal editor)  
- Tag pills  
- View switcher control  

---

## States

### Loading State
- Skeleton rows or card placeholders
- During initial load or refresh after exit

### Empty State
Shown when no open positions exist:
- Message explaining there are no active trades  
- Action: “Enter New Position”

### Error State
- Global error banner if positions list fails to load  
- Retry option for re‑fetching data

---

## Responsive Behavior
- Table collapses to cards on smaller screens  
- Grid view reduces card width and stacks vertically  
- Journal cards expand to full width on mobile  
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

---
``
