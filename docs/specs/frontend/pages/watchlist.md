**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-03-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-18__release-v2.1/watchlist/ux_spec.md

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
| Target Entry | `target_entry_price` | Native currency (GBP for UK, USD for US). Display `—` if null. |
| Stop (Initial) | `initial_stop_price` | Native currency. Display `—` if null. |
| Stop (Current) | `current_stop_price` | Native currency. Display `—` if null. |
| Actions | — | "Add to Position" button + "Remove" icon (trash) |

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

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-18 | Initial spec. ST-10 — EPIC-03 (Watchlists & Screening). Design gate: 2026-03-18__release-v2.1. Design source: UX spec approved by Product Owner 2026-03-18. |
