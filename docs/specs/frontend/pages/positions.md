# positions.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 1.5
**Last Updated:** 2026-05-09
**Design Source (v2.3 additions):** docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md
**Design Source (v3.3 additions):** docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md, docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md, docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.5 | 2026-05-09 | v3.3 design gate: (ST-03) Arc 3 position lifecycle state badge — five-state set (GRACE/LOSING/PROFITABLE/EXIT ZONE/UNKNOWN) with days_in_state inline and next-trigger tooltip; (ST-05) Grace period alert zone at top of page for GRACE positions ≥ day 8; (ST-07) Trail Stop action and guided modal for PROFITABLE/EXIT ZONE positions. Design sources listed above. Approved: Product Owner 2026-05-09. |
| 1.4 | 2026-03-24 | ST-01 (BLG-FEAT-11, v2.3): §Strategy Compliance Panel — collapsible panel below Table View showing per-position ATR compliance data. Display-only. Design source: docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md. Approved: Product Owner 2026-03-24. Design gate: 2026-03-24__release-v2.3. |
| 1.3 | 2026-03-18 | (no change to positions.md — version increment noted for lineage) |
| 1.2 | 2026-02-26 | BLG-FEAT-06 (A-S08): Add `grace_days_remaining` column specification to Table View. Display format, null behaviour, and data source documented. Dependent on `position_endpoints.md` v1.8.3. |
| 1.1 | 2026-02-18 | Add Journal View. Tag filter. Expandable journal cards. View switcher. |
| 1.0 | — | Initial version. |

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
- Status (lifecycle state badge — see §Position Lifecycle State Badge)
- Grace Days Remaining *(BLG-FEAT-06)*
- Tags (as colored pills)
- Actions:
  - **Exit** (opens exit modal)
  - **Trail Stop** (opens trail stop modal — see §Trail Stop Action; visible only for PROFITABLE/EXIT ZONE positions)
  - **View Journal** (opens position detail modal)

---

#### Position Lifecycle State Badge (v3.3 — ST-03 IT-01)

**Design source:** docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md

**Data sources:** `position_state`, `days_in_state` from `GET /positions` (Arc 3 fields).

**Column label:** "Status" (replaces prior GRACE/PROFITABLE/LOSING badge set).

**Badge format:** `STATE — Nd` (e.g. "GRACE — 3d")
- Filled pill, white text on state colour
- Width: content-fit

**State colour scheme:**

| State | Colour | Hex |
|-------|--------|-----|
| GRACE | Blue | `#2563EB` |
| LOSING | Red | `#DC2626` |
| PROFITABLE | Green | `#16A34A` |
| EXIT ZONE | Purple | `#7C3AED` |
| UNKNOWN | Grey | `#6B7280` |

**Tooltip (hover/focus on badge):**

| State | Tooltip |
|-------|---------|
| GRACE | "Exits grace when position moves > 0.5 ATR or after 10 trading days" |
| LOSING | "Exits when price rises above entry by 0.5 ATR" |
| PROFITABLE | "Advances to Exit Zone when P&L reaches 2R target" |
| EXIT ZONE | "Position has reached R-target. Review stop or exit." |
| UNKNOWN | "Set a stop and R-target on the linked trade plan to enable lifecycle tracking." |

**Null handling:** If `position_state` is null (pre-Arc 3 position pending back-fill), display UNKNOWN badge. Never display a dash or empty cell.

**§13 constraint:** Display-only. No automated recommendation generated from state display.

**Accessibility:** Badge has `aria-label="Position state: {STATE}, {N} days in state"`. Colour is never the sole differentiator — state label text is always present.

---

#### Grace Days Remaining Column

**Data source:** `grace_days_remaining` from `GET /positions` (`position_endpoints.md` v1.8.3).

**Display when in grace period** (`grace_days_remaining` is an integer):
Display the string `"Day {holding_days + 1} of 10"`.

Examples:
| `holding_days` | Display |
|----------------|---------|
| 0 | Day 1 of 10 |
| 1 | Day 2 of 10 |
| 5 | Day 6 of 10 |
| 9 | Day 10 of 10 |

**Display when not in grace period** (`grace_days_remaining` is null):
Display a dash (`—`) or leave the cell visually empty. Do not display `"Day 0 of 10"`, `"0"`, or `"null"`.

**Column visibility:** Always present in the Table View for all open positions. The column is not hidden when a position is post-grace — the cell simply shows a dash.

**No sorting required.** This column is informational only; sorting is not required for v1.6.1.

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

---

## Grace Period Alert Zone (v3.3 — ST-05 IT-02)

**Design source:** docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md

**Placement:** Above the View Switcher, at the top of the Positions page. A dedicated Alert Zone with amber background (`#FEF3C7`) and left border (`#D97706`, 4px).

**Trigger:** One or more open positions with `position_state = 'GRACE'` AND `days_in_state ≥ 8`. Data source: `GET /positions/grace-period-alerts`.

**One alert card per qualifying position.** Cards stack vertically in the Alert Zone.

### Alert Card Contents

- Header: "⚠ Grace Period Alert — {TICKER}" + "Day {days_in_state} of 10" sub-label + Dismiss (✕) button
- Body: "Your grace period ends in {10 - days_in_state} trading day(s). Review your original thesis before the window closes."
  - When `days_in_state = 10`: "Grace period has ended. Your position will transition to LOSING or PROFITABLE on next refresh."
- Trade plan context block (when `trade_plan_id` present): Thesis (first 120 chars), Entry zone, Stop, R-target
- "View Trade Plan →" text link (when `trade_plan_id` present)

### Dismiss Behaviour

- Per-position per-session via localStorage key `grace_alert_dismissed_{position_id}`
- Alert reappears on next browser session (no expiry)
- When all cards dismissed: Alert Zone collapses to zero height (no visual gap)

**§13 constraint:** Display-only. No automated recommendation. Human decides action.

**Accessibility:** Alert Zone has `role="alert"` and `aria-live="polite"`.

---

## Trail Stop Action (v3.3 — ST-07 IT-03)

**Design source:** docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md

### Trail Stop Button

- Placement: Actions column, after "Exit", before "View Journal"
- Label: "Trail Stop"
- Style: secondary (outlined)
- **Shown** for positions where `position_state` is `PROFITABLE` or `EXIT ZONE`
- **Disabled** (with tooltip "No current stop set. Add a stop to use trail management.") when `current_stop` is null
- **Hidden** for GRACE, LOSING, UNKNOWN states

### Trail Stop Modal

Opened by clicking enabled "Trail Stop" button. Data source: `GET /positions/{id}/stop-trail`.

**Modal header:** "Trail Stop — {TICKER}"

**Data rows:**

| Label | Source | Format |
|-------|--------|--------|
| Current Stop | `current_stop` | Native currency, 2dp |
| ATR Trail Stop | `atr_trail_stop` | Native currency, 2dp |
| Raise by | `trail_difference` | "+£X.XX" (positive) or "−£X.XX" (amber, negative) |
| Trail in R | `trail_r_terms` | "+X.XR" |

**Footnote (static):** "ATR trail stop = current price − (ATR × 2.0). ATR period: 14 days. Multiplier per strategy rules."

**Confirmation button:** "Update stop to {atr_trail_stop}" — calls `PUT /positions/{id}` with new `stop_price`.

On success: modal closes; position row updates; toast: "Stop updated to {atr_trail_stop}".

**Cancel / Dismiss:** "Cancel" text link; Escape key; ✕ button — no change made.

**§13 constraint:** System presents calculation. Human confirms. No automated stop update.

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
| `GET /positions` | Primary data source for all three views. Returns open positions with live pricing, journal fields, `grace_days_remaining`, `position_state`, `state_entered_at`, `days_in_state`. |
| `GET /positions/tags` | Tag autocomplete source for the Journal View filter dropdown and for the Position Detail Modal's tag editor |
| `GET /positions/compliance` | *(v2.3 — ST-01)* Strategy Compliance Panel data source. Returns ATR-based per-position stop compliance, stop age, and size compliance flags. Display-only; §13.3 constraint applies. |
| `GET /positions/grace-period-alerts` | *(v3.3 — ST-05)* Returns positions in GRACE state with `days_in_state ≥ 8`, including trade plan context. Source for Grace Period Alert Zone. |
| `GET /positions/{id}/stop-trail` | *(v3.3 — ST-07)* Returns ATR trail stop calculation for a single position. Source for Trail Stop Modal. |
| `PUT /positions/{id}` | *(v3.3 — ST-07)* Updates stop price after user confirms trail stop action. |

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

## Strategy Compliance Panel (v2.3 — ST-01 BLG-FEAT-11)

**Design source:** docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md
**Scope constraint (§13.3):** Display-only — no automated notification, alert, or action generated by this panel. Strategy Rules & System Intent Owner DoQ sign-off required at delivery verification.

### Placement

Collapsible panel appended below the Table View only. Hidden in Grid View and Journal View.

Label: **"Strategy Compliance"** with expand/collapse chevron.

### Panel Header

- Overall status badge: **"Compliant"** (green) / **"Needs Attention"** (amber) / **"Review Required"** (red)
- Summary label: "N of M positions fully compliant"
- Default: expanded if any position is non-compliant; collapsed if all compliant

### Per-Position Table

| Column | Source | Display |
|--------|--------|---------|
| Ticker | positions | text |
| Stop Compliance | backend compliance flag | ✅ / ⚠️ |
| Stop Age | days since last stop update | "N days" / "Not set" |
| Size Compliance | backend compliance flag | ✅ / ⚠️ |

### States

- Loading: spinner; panel collapses until data ready
- No positions: panel hidden
- All compliant: green header; collapsed by default
- Non-compliant present: amber/red header; expanded by default

### API Dependency

Backend must provide compliance flags per position (new endpoint or extension to `GET /positions`). openapi.yaml must be updated in same commit as implementation.

---

## UX Notes

- Grace period must be visually clear and distinguishable from normal stop logic
- Tags should be easily scannable and visually grouped
- Exit action should always feel safe — a modal confirmation protects from accidental exits
- Journal editing should feel lightweight, using inline editors where possible
- The user should be able to switch between views without losing filtering or scroll position
- Data should update smoothly after exits or journal edits
- The Journal View is a **reading and reflection experience**, not a live monitoring surface. Layout and density decisions should reflect this: more vertical space per entry, no live price indicators, no stop-level warnings

---

## Known Deviations

### DEV-EPIC02-ST05-03 — Positions Table View: P&L (GBP) column absent

- **Description:** The v2.3 implementation of the Positions Table View renders "P&L %" (percentage uplift) in green for positive positions but does not display the "P&L (GBP)" absolute value column. Only % is visible; the absolute £ value is absent.
- **Canonical requirement:** §Table View column list specifies both "P&L (GBP)" and "P&L %" as separate columns in the Table View.
- **Priority:** P2
- **Target resolution release:** v2.4
- **Owner:** Frontend Specifications & UX Documentation Owner
- **Backlog reference:** BLG-FE-06 (filed delivery verification 2026-03-30, cycle 2026-03-24__release-v2.3)
- **Resolution:** Resolved by ST-04, cycle 2026-03-31__release-v2.4 (shipped 2026-04-03). P&L (GBP) column added. Changelog: docs/product/changelog.md#v24
