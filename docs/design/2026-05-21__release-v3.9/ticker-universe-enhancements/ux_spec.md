**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-05-21
**Approved by:** Product Owner — 2026-05-21
**Cycle:** 2026-05-21__release-v3.9
**Stories:** ST-05, ST-06 (EPIC-02)

---

# UX Spec — Ticker Universe Enhancements (ST-05, ST-06)

## Current Page State

The Ticker Universe management page (shipped in v3.8) shows a table of tickers with columns: Ticker Symbol, Market, Status toggle, and Actions (delete).

---

## ST-05 — Strip .L Suffix from Display Labels

### Decision

LSE tickers are stored and sent with `.L` suffix (e.g. `BARC.L`). Strip `.L` from displayed label text only.

### Rules

- Display label: strip `.L` → show `BARC` not `BARC.L`
- API requests (add, delete, toggle URL params and request bodies): unchanged — must include `.L` suffix
- US tickers: unaffected
- Applies to all columns where the ticker symbol appears as a human-readable label

### Playwright Test

- **SC-TU-DISP-01**: LSE ticker row shows label without `.L`; API request for that ticker still sends `.L`

---

## ST-06 — Company Name Column

### Decision

Add `company_name` as a dedicated column in the ticker table, sourced from `GET /ticker-universe` response.

### Column Placement

Insert **Company Name** as the second column (after Ticker Symbol):

| Ticker | Company Name | Market | Status | Actions |

### Display Rules

- `company_name` non-null: display the full string
- `company_name` null: cell is empty — no placeholder text, no error state; ticker-only display is acceptable
- Company name is read-only; no user interaction

### Playwright Test

- **SC-TU-COMP-01**: At least one ticker row shows company name in the Company Name column
