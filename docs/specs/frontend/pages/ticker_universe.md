**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-21
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v1.0):** docs/design/2026-05-21__release-v3.9/ticker-universe-enhancements/ux_spec.md
**API contract:** docs/specs/api_contracts/screener_api_contract.md

---

# ticker_universe.md — Ticker Universe Management Page

**Purpose:** The Ticker Universe management page allows the operator to view, add, remove, and toggle active/inactive status of tickers in the screener universe. Introduced in v3.8 (S2-03). This spec is the canonical UX reference; v1.0 documents the v3.8 shipped state plus v3.9 enhancements (ST-05, ST-06).

---

## 1. Purpose and User Goals

Users should be able to:

- View all tickers in the universe with ticker symbol, company name, market, and active status
- Add new tickers to the universe
- Remove tickers from the universe
- Toggle a ticker's active/inactive status

---

## 2. Navigation and Route

- Route: `/ticker-universe`
- Page title: **"Ticker Universe"**

---

## 3. API Reference

| Endpoint | Purpose |
|----------|---------|
| `GET /ticker-universe` | Fetch all tickers; response includes `company_name`, `market`, `active` |
| `POST /ticker-universe` | Add ticker |
| `DELETE /ticker-universe/{ticker}` | Remove ticker |
| `PUT /ticker-universe/{ticker}` | Toggle active/inactive |

Canonical contract: `docs/specs/api_contracts/screener_api_contract.md`

---

## 4. Column Layout

| Column | Field | Notes |
|--------|-------|-------|
| Ticker | `ticker` | Display label strips `.L` suffix for LSE tickers (see §5) |
| Company Name | `company_name` | If null: cell is empty (no placeholder, no error) |
| Market | `market` | "US" or "UK" |
| Status | `active` | Active/Inactive toggle (see §6) |
| Actions | — | Delete button (see §7) |

**Column ordering is fixed.**

---

## 5. LSE Ticker Display — .L Suffix Strip (ST-05)

LSE-listed tickers are stored and transmitted with `.L` suffix (e.g. `BARC.L`). On this page:

- **Display label**: strip `.L` suffix — show `BARC`, not `BARC.L`
- **API requests** (add, delete, toggle — URL params and request bodies): must include the full `.L` suffix unchanged
- **US tickers**: unaffected

Applies to all columns where the ticker symbol appears as a human-readable label.

---

## 6. Active/Inactive Toggle

- Active (green): ticker is included in screener runs
- Inactive (grey): ticker excluded from screener runs
- Toggle calls `PUT /ticker-universe/{ticker}` (`.L` suffix included for LSE tickers)
- On success: toggle state updates immediately
- On error: toggle reverts; inline error shown

---

## 7. Delete Action

- Each row has a delete button (trash icon or "Remove" label)
- Clicking shows inline confirmation: "Remove {TICKER} from the universe? This cannot be undone."
- On confirm: calls `DELETE /ticker-universe/{ticker}` (`.L` included for LSE)
- On success: row removed from list
- On error: inline error; row not removed

---

## 8. Add Ticker

Add controls at the top of the page:

- Text input: ticker symbol (uppercase)
- "Add" button: calls `POST /ticker-universe` with `{ ticker: <value> }`
- On success: new row appears in list
- On error: inline error below input field

---

## 9. Empty State

When no tickers in universe: "No tickers in universe. Add a ticker to begin screening."

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-21 | Initial spec. v3.9 design gate — documents v3.8 shipped page + ST-05 (.L suffix strip from display labels, §5) + ST-06 (company_name column, §4). Design source: docs/design/2026-05-21__release-v3.9/ticker-universe-enhancements/ux_spec.md. Approved: Product Owner 2026-05-21. Head of Specs Team confirmed. |
