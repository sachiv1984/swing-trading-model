**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-05-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v0.1):** docs/design/2026-05-19__release-v3.8/ticker-universe-management/ux_spec.md
**Story:** ST-09 (EPIC-04, v3.8) — BLG-FEAT-22

---

# ticker_universe.md — Ticker Universe Management

**Purpose:** The Ticker Universe Management page allows users to add, toggle, and delete tickers from the set used by the screener and signal generation engine. This page replaces the startup `public.tickers` sync — `ticker_universe` is the sole authoritative source for screener and signal generation after v3.8.

---

## 1. Purpose and User Goals

Users should be able to:

- View all tickers in their universe with market, sector, and active status
- Add new tickers (US or UK market)
- Toggle tickers inactive to exclude them from screener and signal runs
- Delete tickers permanently
- Filter the view by market and active status

---

## 2. Navigation and Route

| Route | Purpose |
|-------|---------|
| `/ticker-universe` | Ticker Universe Management page |

- Top-level nav item: **"Ticker Universe"**
- Page title: **"Ticker Universe"**

---

## 3. API Reference

| Endpoint | Purpose |
|----------|---------|
| `GET /ticker-universe` | List all tickers in universe |
| `POST /ticker-universe` | Add ticker |
| `PUT /ticker-universe/{ticker}` | Toggle active/inactive |
| `DELETE /ticker-universe/{ticker}` | Remove ticker permanently |

Canonical contract: to be added to `docs/specs/api_contracts/` and `docs/reference/openapi.yaml` as part of ST-09 implementation.

---

## 4. Page Header

- H1: "Ticker Universe"
- Sub-heading: "Manage which tickers are included in screener and signal generation."
- Right-aligned: **"+ Add Ticker"** button (primary)

---

## 5. Filter Bar

Positioned below the page header, above the ticker table.

| Filter | Type | Options |
|--------|------|---------|
| Market | Button group or Select | All / US / UK |
| Status | Button group or Select | All / Active / Inactive |

Filters apply client-side against the full loaded dataset.

---

## 6. Ticker Table

Default sort: ticker symbol ascending.

| Column | Source | Notes |
|--------|--------|-------|
| Ticker | `ticker` | Uppercase display; UK tickers display without `.L` suffix |
| Market | `market` | "US" or "UK" |
| Sector | `sector` | `—` if null |
| Status | `active` | Toggle pill: "Active" (green) / "Inactive" (grey) — clickable inline |
| Actions | — | "Delete" (red text link with inline confirmation) |

### 6.1 Empty State (no tickers)

- Heading: "No tickers in your universe."
- Body: "Add tickers below to start running the screener and generating signals."
- **"+ Add Ticker"** button

### 6.2 Filtered Empty State

- "No tickers match the selected filters."
- "Clear filters" text link

---

## 7. Add Ticker Flow

### 7.1 Modal

**Title:** "Add Ticker"

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Ticker symbol | Text | Yes | Uppercase-enforced; 1–10 chars; alphanumeric + "." |
| Market | Radio: US / UK | Yes | |

**Actions:**
- **"Add Ticker"** (primary) — `POST /ticker-universe` with `{ticker, market, active: true}`
- **"Cancel"** (secondary) — closes; no change

**Validation:**
- Non-empty ticker
- Duplicate (ticker + market): inline error "This ticker is already in your universe."

### 7.2 Post-Add

Ticker appears in table immediately (optimistic insert or re-fetch). Modal closes on success.

---

## 8. Toggle Active/Inactive

Clicking Status pill: `PUT /ticker-universe/{ticker}` with `{active: <new_state>}`.

- Visual update immediate (optimistic)
- Inactive rows: muted text (opacity 0.6)
- On error: revert row state; toast notification "Failed to update {TICKER}. Please try again."

---

## 9. Delete Ticker

Clicking "Delete": inline confirmation "Delete {TICKER}? This removes it from the screener and signal generation permanently." with "Delete" (red) and "Cancel".

On confirm: `DELETE /ticker-universe/{ticker}`. Row removed immediately on success.

On error: toast "Failed to delete {TICKER}. Please try again."

---

## 10. States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton rows (5); filters disabled |
| Error (load) | "Unable to load ticker universe. Please try again." + Retry button |
| Partial error (toggle) | Toast; row reverts |
| Partial error (delete) | Toast |
| Add conflict | Inline modal error |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-05-19 | Initial spec. v3.8 design gate — ST-09 (EPIC-04). Design source: ticker-universe-management/ux_spec.md. Approved: Product Owner 2026-05-19. |
