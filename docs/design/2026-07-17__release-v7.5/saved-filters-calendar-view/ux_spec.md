**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-17
**Approved by:** Product Owner — 2026-07-17
**Story:** ST-04 — Named saved filter presets and a calendar view (EPIC-04, BLG-FE-118)
**Depends on:** `docs/specs/blg_fe_118_pre_implementation_readiness_pass.md` — this artefact adopts that readiness pass's `saved_filters` schema, day-bucketed realised-P&L date sourcing, and realised/unrealised split constraint as its technical baseline
**Cycle:** 2026-07-17__release-v7.5

---

# UX Specification — Saved Filter Presets & Calendar View

## 1. Placement Decision

The backlog AC text ("save a filter combination", "calendar view renders trade plan dates and key dates") does not name a page. The readiness pass grounds both mechanisms in **Trade History** (`trade_history.md`): it has the richest existing filter set (date range, win/loss, market, exit reason, tags — `trade_history.md` §Filters) of any page in the app, and the calendar's date sourcing (`GET /reports/monthly-pnl` / a new day-granularity variant) is built on `trade_history.exit_date`, the same field the page's Exit Date column and default sort already use. Both features are added to Trade History as the single most coherent home, rather than splitting saved filters onto one page and the calendar onto another. This is a Head of UX & Design placement decision, confirmed by Product Owner.

## 2. Saved Filter Presets

### 2.1 Placement

A new control row directly below the existing Filters section (`trade_history.md` §Filters), unchanged otherwise.

### 2.2 Saving a Preset

- **"Save current filters as…"** link/button, visible whenever at least one filter is active (date range, win/loss, market, exit reason, or tag selection — matches the existing filter set exactly, no new filter dimensions introduced).
- Clicking opens an inline name input: `"Preset name"` (text, required, max 100 chars — matches `saved_filters.name VARCHAR(100)`).
- Submit calls `POST /saved-filters` with `{ name, filter_state }` where `filter_state` is the current filter selection serialised to the shape the readiness pass's `filter_state JSONB` column expects.
- **Duplicate name:** if the API returns `400` for a name collision (`UNIQUE (portfolio_id, name)`), show inline error: `"A preset named '{name}' already exists."`

### 2.3 Applying a Preset

A **"Saved filters"** dropdown/select, positioned to the right of the existing filter controls, listing all `GET /saved-filters` rows by name. Selecting one applies its `filter_state` to the current filter controls (overwrites the active selection, matching how the existing filter controls already behave when changed individually). Does not auto-save any subsequent changes back to the preset — the preset remains a named snapshot until explicitly re-saved under the same or a new name.

### 2.4 Deleting a Preset

Each preset in the dropdown has an adjacent delete (×) affordance. Clicking shows inline confirmation: `"Delete preset '{name}'?"` — "Delete" calls `DELETE /saved-filters/{id}`; "Cancel" dismisses. Deleting a preset does not change the currently-active filter selection (per readiness pass AC-04's explicit distinction between the ephemeral active-filter state and the server-side saved preset).

### 2.5 Persistence Distinction (readiness pass AC-04)

Two independent persistence mechanisms coexist and must not be conflated:
- **Currently-active filter state:** ephemeral, device-local, versioned-localStorage-envelope pattern (reusing the existing `BLG-FE-40` pattern already implemented for `RedFlagJournal.js`) — survives a page reload but is not a named preset.
- **Saved presets:** server-side `saved_filters` rows — persist across devices/sessions, independent of the localStorage envelope.

## 3. Calendar View

### 3.1 Placement & Toggle

A view toggle at the top of the Trade History page, alongside the existing filter row: **"Table"** (default, current behaviour, unchanged) / **"Calendar"**. Switching to Calendar view replaces the table and its expandable-row content with the calendar grid; the Filters section, Saved Filters control, and Summary Stats bar remain visible and functional in both views (calendar view respects the same active filters).

### 3.2 Calendar Grid

Standard month-grid (`react-day-picker` `DayPicker`, default single-month mode — no range/multiple selection, per readiness pass AC-02). Prev/next month navigation via the component's built-in nav buttons.

Each day cell shows a compact realised-P&L indicator for trades whose `exit_date` falls on that day:
- A small coloured dot/figure: green if net realised P&L for the day is positive, red if negative, no indicator if no trades exited that day.
- Hovering a day shows a tooltip with the exact figure: `"+£240.50 (3 trades)"` / `"−£85.00 (1 trade)"`.

### 3.3 Day Interaction

Clicking a day cell with 1+ exits navigates to **Table** view with the date range filter set to that single day (reuses the existing Date range filter mechanism — no new detail view is built, per readiness pass AC-02's explicit reuse guidance). Clicking an empty day (no exits) does nothing.

### 3.4 Unrealised P&L (readiness pass AC-03 constraint)

Unrealised P&L is not date-attributable (current-snapshot-only, no historical daily mark-to-market source exists) and is never shown per-day. Instead, a single summary banner above the calendar grid reads: `"Unrealised P&L (as of today): {value}"` — same wording/treatment convention already used on the Monthly P&L and Tax Year reports (`docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`), reused verbatim rather than inventing new copy.

### 3.5 Empty State

A month with zero closed-trade exits (readiness pass AC-06 — confirmed reusable default `DataState`): calendar grid still renders (empty day cells, no indicators); no dedicated empty-state message is needed since the grid itself communicates "nothing here" per day. If **no trades exist in the account at all**, show the standard full-page `DataState` empty state above the grid: heading **"No closed trades yet."**, body `"Your trading calendar will populate as you close trades."`

## 4. §13 Compliance

Both features are read-only presentation/filtering conveniences over existing data (trade history) or user-authored metadata (filter names). No automated decision-making, scoring, or recommendation logic. Not a §13-relevant feature.

## 5. States

| State | Behaviour |
|-------|-----------|
| No presets saved | "Save current filters as…" available; dropdown shows "No saved filters" |
| Preset saved | Appears in dropdown, selectable |
| Preset applied | Filter controls reflect the preset's `filter_state` |
| Table / Calendar toggle | Switches content area; filters/stats bar persist across both |
| Calendar, day with exits | Coloured indicator + tooltip; clickable |
| Calendar, empty day | No indicator; not clickable |
| Calendar, no trades in account | Full-page empty state |

## 6. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-17
- **Product Owner:** Approved — 2026-07-17
