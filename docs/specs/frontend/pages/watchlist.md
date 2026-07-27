**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.5
**Last Updated:** 2026-07-27
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-18__release-v2.1/watchlist/ux_spec.md
**Design Source (v0.3 research indicator):** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §F
**Design Source (v0.4 bulk actions):** docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md
**Design Source (v0.5 staleness indicator):** docs/design/2026-07-27__release-v7.9/watchlist-staleness-review/ux_spec.md

---

# watchlist.md — Watchlist

## Purpose & User Goals

The Watchlist page lets the user monitor tickers that are not yet active positions. It surfaces entry signal status, target entry price, and stop fields per ticker, allowing the user to track candidates and move them into a position entry when signals become favourable.

Users should be able to:
- View all monitored tickers with current entry signal status
- See target entry and stop prices per ticker
- Add, edit, and remove watchlist entries
- Open the position entry modal pre-populated with a watchlist entry's data

---

## Navigation & Route

- Top-level nav item: **"Watchlist"**
- Route: `/watchlist`
- Page title: **"Watchlist"**

---

## API Reference

- **Endpoint:** `GET /watchlist` — list all watchlist entries
- **Create:** `POST /watchlist`
- **Update:** `PATCH /watchlist/{id}`
- **Delete:** `DELETE /watchlist/{id}`
- **Canonical contract:** `docs/specs/api_contracts/watchlist_endpoints.md`

---

## Page Header

- H1: **"Watchlist"**
- Right-aligned: **"+ Add Ticker"** button (primary action)

---

## Watchlist Table

One row per watchlist entry. Default sort: entry signal status (Active first, then Watch, then No Signal), then alphabetically by ticker within each group.

### Columns

| Column | Source | Notes |
|--------|--------|-------|
| Ticker | `ticker` | Uppercase. Clicking the ticker opens the edit modal. |
| Market | `market` | Badge pill: "UK" / "US" |
| Entry Signal | `signal_status` | See Signal Status Values below. |
| Research | `has_research` | *(v3.3 — BLG-FE-29)* Binary indicator — see §Research Status Indicator |
| Added | `added_at` | *(v7.9 — ST-01, BLG-FEAT-66)* Days on watchlist — see §Staleness Indicator |
| Target Entry | `target_entry_price` | Native currency (GBP for UK, USD for US). Display `—` if null. |
| Stop (Initial) | `initial_stop_price` | Native currency. Display `—` if null. |
| Stop (Current) | `current_stop_price` | Native currency. Display `—` if null. |
| Actions | — | "Research" link + "Add to Position" button + "Remove" icon (trash) |

### Signal Status Values

| Value | Display | Colour |
|-------|---------|--------|
| `active` | **Active** | Green badge |
| `watch` | **Watch** | Amber badge |
| `no_signal` | **No Signal** | Muted grey badge |

Signal status is read-only — sourced from backend signal integration; not user-editable.

---

## Add Ticker Modal

Triggered by **"+ Add Ticker"** button.

### Fields

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Ticker symbol | Text | Yes | Alphanumeric; 1–10 characters; uppercase-enforced on input |
| Market | Radio: UK / US | Yes | — |
| Target Entry Price | Numeric | No | Positive decimal |
| Initial Stop Price | Numeric | No | Positive decimal |
| Current Stop Price | Numeric | No | Positive decimal |

**Duplicate check:** If the submitted ticker already exists on the watchlist, show inline error below the ticker field: `"This ticker is already on your watchlist."`

### Actions
- **"Add to Watchlist"** (primary) — submits `POST /watchlist`
- **"Cancel"** (secondary) — closes modal without saving

---

## Edit Modal

Opened by clicking the ticker name in the table.

- Pre-populated with current values.
- Ticker symbol field is **read-only** in edit mode.
- All price fields are editable.
- Submits `PATCH /watchlist/{id}`.

### Actions
- **"Save Changes"** (primary)
- **"Cancel"** (secondary)
- **"Remove from Watchlist"** (destructive, bottom of modal) — triggers confirmation prompt

### Remove Confirmation Prompt
Inline within the modal (not a separate dialog):
> `"Remove [TICKER] from your watchlist?"`
- **"Remove"** (destructive) — calls `DELETE /watchlist/{id}`; closes modal; removes row from table
- **"Cancel"** — dismisses the confirmation; modal remains open

---

## Add to Position

The **"Add to Position"** button (per table row) opens the existing position entry modal, pre-populated with:
- Ticker symbol
- Market
- Target entry price (as the entry price field)
- Initial stop price (as the initial stop field)
- Current stop price (as the current stop field)

**On successful position entry:**
- The watchlist entry is automatically removed from the watchlist (backend responsibility: `DELETE /watchlist/{id}` or equivalent on position creation).
- The row disappears from the watchlist table.

**On cancelled position entry:**
- Watchlist entry is unchanged.

---

## States

### Loading State
Skeleton table rows (3–5 rows) while the watchlist loads from the API.

### Empty State
Displayed when no watchlist entries exist:
- Heading: **"Your watchlist is empty."**
- Body: `"Add tickers you're monitoring for entry opportunities."`
- **"+ Add Ticker"** button shown in the empty state body (in addition to the page header)

### Error State
Full-width error panel: `"Unable to load watchlist. Please refresh."` with a **"Retry"** button.

### Row Removal Animation
On removal (via Remove or Add to Position): row slides out or fades out before the table re-renders. Duration: ≤200ms.

---

## Constraints

- Signal status is read-only; the watchlist does not compute or derive signals.
- All price fields are in native currency (GBP for UK, USD for US). No FX conversion is shown on this page.
- The watchlist is a monitoring list only — no execution actions beyond routing to the position entry modal.

---

## Research Status Indicator (v3.3 — ST-17 BLG-FE-29)

**Design source:** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §F

**Column label:** "Research" — narrow column, icon only (no text in cell).

| Condition | Icon | Tooltip |
|-----------|------|---------|
| Research record exists (`has_research = true`) | ✅ (green checkmark) | "Research available" |
| No research record (`has_research = false`) | ○ (hollow circle, grey) | "No research yet" |

**Scope:** Binary only — does not indicate freshness or quality.

**Data source:** `has_research` boolean per watchlist entry from `GET /watchlist` response (backend extension required), or batch resolution from frontend after initial load. No blocking dependency on research data — if unavailable, show grey circle.

**Accessibility:** Icon has `aria-label="Research available"` or `"No research for {TICKER}"`.

**Performance:** Must not regress watchlist loading. If fetched separately, use debounced batch request post-render.

---

## Staleness Indicator (v7.9 — ST-01, BLG-FEAT-66)

**Design source:** docs/design/2026-07-27__release-v7.9/watchlist-staleness-review/ux_spec.md

**Column label:** "Added" — placed after "Research", before "Target Entry".

**Data source:** `added_at` (existing field, captured at add time — no backend schema change). `days_on_watchlist` is server-computed, not client-derived.

**Staleness threshold:** 30 days (default, server-configurable constant, not user-editable this cycle).

| Condition | Display | Style |
|-----------|---------|-------|
| Not stale (`days_on_watchlist < 30`) | `"{N}d"` | `text-slate-500 dark:text-slate-400` (existing secondary-text token) |
| Stale (`days_on_watchlist ≥ 30`) | `"{N}d, no action"` + clock icon prefix | `text-amber-600 dark:text-amber-400` |

`aria-label`: `"On watchlist {N} days with no action — consider Keep or Remove"` (stale) / `"Added {N} days ago"` (not stale).

**Legacy rows:** entries with no `added_at` (pre-dating this feature) are treated as added today on first read — never mass-flagged as stale on ship day.

### Stale-Row Actions (AC-03, AC-04)

For stale rows only, the Actions column gains a **"Keep"** button (secondary, outlined), placed before the existing "Research" / "Add to Position" / "Remove" actions:

- **"Keep"** — calls `PATCH /watchlist/{id}` with `{ added_at: now() }`, resetting the staleness clock. No confirmation modal. Toast: `"{TICKER} kept on watchlist."` Row updates optimistically.
- **"Remove"** — existing action, unchanged (§Edit Modal / §Remove Confirmation Prompt).

**No automatic removal (AC-04):** there is no scheduled sweep or silent expiry. The stale badge is advisory only; a human decision (Keep or Remove) is required in all cases.

**Accessibility:** clock icon has no independent meaning — colour + icon + label text together carry the state; label text alone is sufficient (colour is never the sole differentiator).

---

## Research Navigation (v3.2 — ST-04)

Each ticker entry in the watchlist table has a **"Research"** action (text link or secondary button) in the Actions column, adjacent to "Add to Position".

| Attribute | Specification |
|-----------|---------------|
| Label | "Research" |
| Placement | Actions column, first action (before "Add to Position" and "Remove") |
| Target | `/research/{ticker}` |
| Context carry | None |

**Back navigation:** User clicking `← Back` on the research view returns to `/watchlist` via browser back.

**Design source:** `docs/design/2026-05-05__release-v3.2/screener-to-research-navigation/ux_spec.md`

---

## Bulk Actions (v7.5 — ST-03 BLG-FE-117)

**Design source:** docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md
**Depends on:** docs/specs/blg_fe_117_pre_implementation_readiness_pass.md (batch-mutation endpoint pattern, §13 pre-check PASS)

### Row Selection

A checkbox is added as the first column of the Watchlist table (left of Ticker). The header row gains a header checkbox: checked selects all rows currently visible under the active state (no filters exist on this page today, so this selects the full table). Selected rows render with a subtle persistent background tint.

### Bulk-Action Toolbar

Renders above the table only when 1+ rows are selected (no "0 selected" state is designed — the toolbar's presence is itself the indicator). Contains: selected count (`"{N} selected"`), available actions (**Bulk Tag**, **Bulk Remove**), and a **"Clear"** text button that deselects all rows.

### Bulk Tag

Opens an inline expand with the existing Tag Editor autocomplete component (`journal_components.md` §4 / `trade_plan.md` §5c pattern), reusing the same tag validation rules. Tags are added to (not replacing) each selected row's existing tag set. Submits `POST /positions/bulk-tag` with `{ ids, tags }`.

### Bulk Remove

Destructive — shows a confirmation dialog: `"Remove {N} selected watchlist entries?"` — "Remove" calls `DELETE /watchlist/bulk` with `{ ids }`; "Cancel" dismisses (selection retained).

### Partial-Failure Feedback

The batch response returns `{ succeeded: [...], failed: [{id, reason}] }`. All-succeeded: toast `"{N} entries updated."`, rows updated/removed, selection cleared. Partial failure: toast `"{N} succeeded, {M} failed."` with an expandable per-row detail listing failed IDs and reasons — never a single opaque "some failed" message.

### §13 Compliance

User-initiated batch of the same manual mutations already available one row at a time (tag, remove). No new automated decision-making.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.5 | 2026-07-27 | v7.9 design gate — added §Staleness Indicator (ST-01, BLG-FEAT-66): new "Added" column showing days-on-watchlist (`added_at`, existing field); staleness threshold 30 days (fixed, server-side); stale rows get amber "{N}d, no action" text + clock icon and a new "Keep" action (resets clock, `PATCH /watchlist/{id}`); no automatic removal — Keep/Remove remain the only paths off the list. Design source: watchlist-staleness-review/ux_spec.md. Approved: Product Owner 2026-07-27. Design gate: 2026-07-27__release-v7.9. Head of Specs Team confirmed. |
| 0.4 | 2026-07-17 | v7.5 design gate — added §Bulk Actions (ST-03, BLG-FE-117): row checkboxes, bulk-action toolbar (renders only when 1+ selected), Bulk Tag (reuses existing Tag Editor), Bulk Remove (destructive, confirmation required), per-row partial-failure feedback. New `POST /positions/bulk-tag` and `DELETE /watchlist/bulk` endpoints. Design source: bulk-actions-toolbar/ux_spec.md. Approved: Product Owner 2026-07-17. Design gate: 2026-07-17__release-v7.5. Head of Specs Team confirmed. |
| 0.3 | 2026-05-09 | v3.3 design gate — added Research Status Indicator section (BLG-FE-29: binary has_research icon per row); added "Research" column to table. Design source: trade-plan-quick-wins/ux_spec.md §F. Approved: Product Owner 2026-05-09. |
| 0.2 | 2026-05-05 | v3.2 design gate — added Research Navigation section (ST-04); updated Actions column. Design source: screener-to-research-navigation/ux_spec.md. |
| 0.1 | 2026-03-18 | Initial spec. ST-10 — EPIC-03 (Watchlists & Screening). Design gate: 2026-03-18__release-v2.1. Design source: UX spec approved by Product Owner 2026-03-18. |
