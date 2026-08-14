**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-08-14
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v1.2):** docs/design/2026-08-14__release-v8.8/ticker-universe-search-sector-industry-filters/decision_record.md
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
  - **Ticker validation failure (400/422):** display the backend error message verbatim; expected format: "Ticker [SYMBOL] not found — please check the symbol and market"
  - **Other errors:** display generic "Failed to add ticker — please try again"

---

## 9. Empty State

When no tickers in universe: "No tickers in universe. Add a ticker to begin screening."

---

## 10. Filtering — Search, Sector, Industry (v1.2 — ST-15, BLG-FE-163)

Extends the existing Market/Active pill-button filter bar (`data-testid="filter-bar"`) — one continuous row, not a separate section.

| Control | Type | Behaviour |
|---------|------|-----------|
| Search | Text input, placeholder "Search ticker or company…" | Case-insensitive substring match against ticker symbol and company name. 200ms debounce. |
| Sector | `<select>`, default "All Sectors" | Options derived dynamically from distinct `sector` values in the loaded ticker list — no new endpoint. |
| Industry | `<select>`, default "All Industries" | Same derivation pattern, from `industry`. |

**Combination:** all 5 filters (Market, Active, Search, Sector, Industry) AND-combine — narrowing the same client-side `filtered = tickers.filter(...)` chain used by the existing Market/Active filters.

**Clear filters:** shown only when at least one filter is non-default, rendered as `<Badge variant="secondary">Clear filters ×</Badge>`. Clicking resets all 5 filters to default and hides itself.

**Row count:** the existing "Showing {filtered.length} of {tickers.length} tickers" footer requires no change — already reflects any active filter combination.

Design source: `docs/design/2026-08-14__release-v8.8/ticker-universe-search-sector-industry-filters/decision_record.md`.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.2 | 2026-08-14 | v8.8 design gate — §10 Filtering added (ST-15, EPIC-03, BLG-FE-163): search/sector/industry filter controls extend the existing Market/Active pill filter bar, AND-combined; "Clear filters" reset control implemented as `Badge variant="secondary"` — first live call site for that shadcn variant (see also `BLG-FE-160`/ST-17). Design source: `docs/design/2026-08-14__release-v8.8/ticker-universe-search-sector-industry-filters/decision_record.md`. Head of UX & Design + Product Owner confirmed 2026-08-14. |
| 1.1 | 2026-05-23 | v4.0 design gate (ST-05, EPIC-02): §8 Add Ticker — validation error message specified: ticker-not-found 400/422 displays backend error message verbatim; other errors show generic fallback. Design Pre-Approved (extends existing inline-error pattern). Head of UX & Design + Product Owner 2026-05-23. |
| 1.0 | 2026-05-21 | Initial spec. v3.9 design gate — documents v3.8 shipped page + ST-05 (.L suffix strip from display labels, §5) + ST-06 (company_name column, §4). Design source: docs/design/2026-05-21__release-v3.9/ticker-universe-enhancements/ux_spec.md. Approved: Product Owner 2026-05-21. Head of Specs Team confirmed. |
