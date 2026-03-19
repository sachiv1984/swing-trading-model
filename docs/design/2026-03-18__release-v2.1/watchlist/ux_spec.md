**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner
**Approved date:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Items:** ST-10
**Frontend spec target:** docs/specs/frontend/pages/watchlist.md (new)

---

# UX Spec — Watchlist UI (ST-10)

## 1. Purpose & User Goal

The user monitors tickers that are not yet active positions but may become entries. The watchlist surface gives them a pre-trade view: entry signal status, target entry price, and stop fields for each candidate.

**User goal:** Quickly assess whether a monitored ticker has entered a favourable entry signal state, and move it to a position entry when ready.

---

## 2. Navigation & Placement

- Accessible from the main navigation as **"Watchlist"**.
- Route: `/watchlist`
- Page title: **"Watchlist"**

---

## 3. Layout

### 3.1 Page Header
- H1: **"Watchlist"**
- Right-aligned: **"+ Add Ticker"** button (primary action).

### 3.2 Watchlist Table

A table of monitored tickers. One row per watchlist entry. Default sort: by entry signal status (active signals first), then alphabetically by ticker.

**Columns:**

| Column | Description | Notes |
|--------|-------------|-------|
| Ticker | Stock ticker symbol | Uppercase. Clickable to open edit modal. |
| Market | UK or US | Badge pill: "UK" / "US" |
| Entry Signal | Current signal status for this ticker | Sourced from backend signal integration. Values: "Active", "Watch", "No Signal". Colour-coded: Active = green, Watch = amber, No Signal = muted grey. |
| Target Entry | User-defined target entry price | Native currency. User-editable inline or via modal. Shown as "—" if not set. |
| Stop (Initial) | User-defined initial stop price | Native currency. Shown as "—" if not set. |
| Stop (Current) | User-defined current stop price | Native currency. Shown as "—" if not set. |
| Actions | Row actions | "Add to Position" button + "Remove" icon |

### 3.3 Signal Status Values
- **Active** — entry conditions met; this ticker is ready for a position entry decision
- **Watch** — ticker is on the watchlist but conditions not yet met
- **No Signal** — signal system returns no active signal for this ticker

Signal status is read-only — it is surfaced from the backend, not user-editable.

### 3.4 Add Ticker Modal

Triggered by **"+ Add Ticker"** button.

**Fields:**
- Ticker symbol (text input, uppercase enforcement)
- Market (UK / US radio)
- Target Entry Price (optional; numeric, native currency)
- Initial Stop Price (optional; numeric, native currency)
- Current Stop Price (optional; numeric, native currency)

**Validation:**
- Ticker symbol: required; alphanumeric; 1–10 characters
- If ticker already on watchlist: inline error "This ticker is already on your watchlist."

**Actions:** "Add to Watchlist" (primary) | "Cancel" (secondary)

### 3.5 Edit Ticker
- Clicking the ticker name in the table opens the same modal pre-populated with current values.
- All fields editable. Ticker symbol is read-only in edit mode (cannot rename a watchlist entry).
- "Save Changes" (primary) | "Cancel" (secondary) | "Remove from Watchlist" (destructive, bottom of modal).

### 3.6 Add to Position
- The **"Add to Position"** button in the row opens the existing position entry modal (from the Positions page), pre-populated with the watchlist entry's ticker, market, target entry price, and stop fields.
- On successful position entry: the ticker is automatically removed from the watchlist and added to active positions.
- If the position entry is cancelled: the watchlist entry remains unchanged.

### 3.7 Remove from Watchlist
- Available via the "Remove" icon in the row or from the edit modal.
- Confirmation prompt: `"Remove [TICKER] from your watchlist?"` with "Remove" (destructive) | "Cancel".

---

## 4. States

### 4.1 Loading State
- Skeleton table rows (3–5 rows) while watchlist loads from API.

### 4.2 Empty State
- No watchlist entries:
> **"Your watchlist is empty."**
> "Add tickers you're monitoring for entry opportunities."
- **"+ Add Ticker"** button shown in the empty state body (in addition to the page header).

### 4.3 Error State
- If watchlist cannot be loaded: full-width error panel with "Unable to load watchlist. Please refresh." and a retry button.

---

## 5. Constraints

- Signal status is read from the backend signal integration — no client-side signal computation.
- All price fields are displayed in native currency per the ticker's market (GBP for UK, USD for US); no FX conversion displayed on this page.
- The watchlist is not a trading order — it is a monitoring list only. No execution actions beyond routing to the position entry modal.

---

## 6. UX Decisions Recorded

| Decision | Rationale |
|----------|-----------|
| Default sort: Active signals first | The highest-value view is tickers with active entry signals — these require a decision today |
| Signal status as read-only display | Signal computation is canonical backend responsibility; the watchlist surface only shows the result |
| Inline "Add to Position" button per row | One-click routing to position entry reduces friction; the most natural next step from an Active signal |
| Auto-remove from watchlist on position entry | Once a ticker becomes a position, it no longer belongs in the monitoring list |
| Optional price fields at add time | Users may want to monitor a ticker before deciding on target and stop levels |
| Confirmation on remove | Destructive action; one-click accidental removal of a carefully configured entry would be disruptive |
