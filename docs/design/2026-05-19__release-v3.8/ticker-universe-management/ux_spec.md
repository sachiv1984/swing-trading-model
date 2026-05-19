**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-19__release-v3.8
**Story:** ST-09 (EPIC-04) — Ticker Universe Management Page
**Sources:** BLG-FEAT-22; strategy_rules.md §13 (no recommendation generated — admin config only)
**Approved by:** Product Owner
**Approved date:** 2026-05-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Ticker Universe Management Page

This spec defines the frontend design for the Ticker Universe Management page. The page replaces the startup `public.tickers` sync, making `ticker_universe` the sole authoritative source for screener and signal generation. Users manage which tickers the system tracks.

---

## 1. Route and Navigation

- **Route:** `/ticker-universe`
- **Nav item:** "Ticker Universe" (top-level nav, under Settings group or standalone)
- **Page title:** "Ticker Universe"

---

## 2. Page Layout

### 2.1 Page Header

- H1: "Ticker Universe"
- Sub-heading: "Manage which tickers are included in screener and signal generation."
- Right-aligned: **"+ Add Ticker"** button (primary)

### 2.2 Filter Bar

Positioned below the page header, above the table.

| Filter | Type | Options |
|--------|------|---------|
| Market | Button group / Select | All / US / UK |
| Status | Button group / Select | All / Active / Inactive |

Filters apply client-side (all tickers loaded in one call).

### 2.3 Ticker Table

One row per ticker. Default sort: ticker symbol ascending.

| Column | Source | Notes |
|--------|--------|-------|
| Ticker | `ticker` | Uppercase; UK tickers display without `.L` suffix in this column but the internal value retains it |
| Market | `market` | "US" or "UK" |
| Sector | `sector` | `—` if null |
| Status | `active` | Toggle: "Active" (green pill) / "Inactive" (grey pill) — clickable to toggle inline |
| Actions | — | "Delete" (red text link with confirmation) |

### 2.4 Empty State

- Heading: "No tickers in your universe."
- Body: "Add tickers below to start running the screener and generating signals."
- **"+ Add Ticker"** button

### 2.5 Filtered Empty State

- "No tickers match the selected filters."
- "Clear filters" text link

---

## 3. Add Ticker Flow

### 3.1 Trigger

Clicking **"+ Add Ticker"** opens an inline form or modal (implementer's choice — modal preferred for atomic submission).

### 3.2 Add Ticker Modal

**Title:** "Add Ticker"

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Ticker symbol | Text | Yes | Uppercase-enforced; strip `.L` on display, accept with or without `.L` for UK |
| Market | Radio: US / UK | Yes | Determines exchange and display conventions |

**Actions:**
- **"Add Ticker"** (primary) — `POST /ticker-universe` with `{ticker, market, active: true}`
- **"Cancel"** (secondary) — closes modal; no change

**Validation:**
- Ticker: non-empty, 1–10 chars, alphanumeric + "." allowed
- Duplicate ticker + market combination: inline error "This ticker is already in your universe."

### 3.3 Post-Add Behaviour

- Ticker appears immediately in the table (optimistic insert or re-fetch)
- Modal closes on success

---

## 4. Toggle Active/Inactive

Clicking the Status pill in the table toggles `active` state:
- `PUT /ticker-universe/{ticker}` with `{active: <new_state>}`
- Visual update immediate (optimistic); revert on error with toast notification
- Inactive tickers: row rendered with muted text (opacity 0.6) to distinguish from active rows

---

## 5. Delete Ticker

Clicking "Delete":
- Inline confirmation prompt (no full modal needed): "Delete {TICKER}? This removes it from the screener and signal generation permanently." with "Delete" (red) and "Cancel" buttons
- On confirm: `DELETE /ticker-universe/{ticker}`
- Row removed immediately on success

---

## 6. States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton rows (5); filters disabled |
| Error (load) | "Unable to load ticker universe. Please try again." + Retry |
| Partial error (toggle) | Toast: "Failed to update {TICKER}. Please try again." — row reverts |
| Partial error (delete) | Toast: "Failed to delete {TICKER}. Please try again." |
| Add conflict | Inline modal error: "This ticker is already in your universe." |

---

## 7. API Summary

| Endpoint | Purpose |
|----------|---------|
| `GET /ticker-universe` | List all tickers in universe |
| `POST /ticker-universe` | Add ticker |
| `PUT /ticker-universe/{ticker}` | Toggle active/inactive |
| `DELETE /ticker-universe/{ticker}` | Remove ticker permanently |

These endpoints are defined in the backend contract for ST-09. API contract owner to register in `docs/specs/api_contracts/` and `docs/reference/openapi.yaml`.

---

## 8. Playwright Coverage Requirements

| Scenario | Description |
|----------|-------------|
| Add ticker | Open modal → fill ticker + market → submit → row appears in table |
| Toggle inactive | Click Status pill → row becomes inactive (muted styling) |
| Toggle back active | Click Status pill again → row becomes active |
| Delete ticker | Click Delete → confirm → row removed |
| Filter by market | Select "UK" → only UK rows shown |
| Filter by active status | Select "Inactive" → only inactive rows shown |
