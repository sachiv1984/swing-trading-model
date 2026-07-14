**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-07-14
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `docs/specs/frontend/pages/reports.md` v0.10 §Page Header Controls / §Download CSV Button States; `docs/specs/api_contracts/reports_endpoints.md` v0.8 §Response (200 — CSV, format=csv)
**Sprint:** 2026-07-14__release-v7.1 — ST-07 (BLG-SPEC-84, AC-06) — closes the gap left by `reports_scenarios.md`'s §4 Out of Scope note ("CSV export correctness — covered by ST-13 Head of Engineering sign-off"), which was never followed up with an actual written scenario document.

---

# Acceptance Test Scenarios — Tax-Year P&L CSV Export

---

## 1. Scope

These scenarios verify the CSV export of the Tax Year P&L report (`GET /reports/tax-year?year=YYYY&format=csv`) against the canonical specification — both the button/interaction behaviour on the Reports page and the exported file's actual structure and content.

> Backend content-assertion coverage exists in `tests/test_reports_integration.py::TestTaxYearCsvExport` (11 tests, added alongside this document — ST-07/AC-05). These scenarios do not duplicate that byte-level assertion coverage; they focus on the end-to-end user-facing download flow and file-opening verification that only a human/browser context can confirm (e.g. does a spreadsheet application actually parse the file correctly).

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| Download CSV button | `docs/specs/frontend/pages/reports.md §Download CSV Button States` |
| CSV response headers/structure | `docs/specs/api_contracts/reports_endpoints.md §Response (200 — CSV, format=csv)` |
| Charset convention | `docs/specs/api_contracts/reports_endpoints.md §Response (200 — CSV, format=csv)` (Charset note) |
| Auth enforcement | `docs/specs/api_contracts/reports_endpoints.md §Derivation Notes` (Authentication note) |
| CSV/export pattern (general) | `docs/specs/api_contracts/backend_engineering_patterns.md §CSV/export response-body pattern` |

---

## 3. Scenarios

---

### SC-CSVX-01 — Download CSV button triggers a file download with correct headers

**Component:** Reports page — Download CSV button
**API:** `GET /reports/tax-year?year=YYYY&format=csv`
**Priority:** P2

#### Preconditions

- User is authenticated and on the Reports page for a tax year with at least one closed trade.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click "Download CSV". | Button enters "Generating…" state (spinner replaces icon), button disabled. `GET /reports/tax-year?year=YYYY&format=csv` fires. |
| 2 | Observe response headers (Network tab). | `Content-Type: text/csv; charset=utf-8`. `Content-Disposition: attachment; filename="tax-year-YYYY-pnl.csv"`. |
| 3 | Observe the browser download. | A file download begins named `tax-year-YYYY-pnl.csv`. No success toast is shown (per spec — silent success). |
| 4 | Observe button state after download completes. | Button returns to "Download CSV" idle state, re-enabled. |

#### Pass criteria

- `Content-Type` and `Content-Disposition` headers match the spec exactly, including the `charset=utf-8` parameter (Starlette auto-appends this — confirm it is actually present, not just assumed).
- Filename includes the correct tax year.
- Button state transitions: idle → generating → idle, matching PDF button's established pattern.

---

### SC-CSVX-02 — Downloaded CSV opens correctly and matches on-screen figures

**Component:** Exported CSV file content
**API:** `GET /reports/tax-year?year=YYYY&format=csv`
**Priority:** P1

#### Preconditions

- Tax year has ≥2 closed trades, including at least one UK and one US trade (to exercise the FX rate columns).
- A spreadsheet application (or text editor) is available to open the downloaded file.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Download the CSV for a tax year with known on-screen summary figures. | File downloads successfully. |
| 2 | Open the file in a spreadsheet application. | File opens without a parse error or "corrupt file" warning. UTF-8 characters (e.g. `£` in header labels) render correctly, not as mojibake. |
| 3 | Compare rows 1–5 (metadata block) against the on-screen summary bar. | Tax Year, Total Realised P&L, Total Closed Trades, Win Rate all match the summary bar exactly — no discrepancy from the on-screen JSON-sourced figures. |
| 4 | Confirm row 6 is blank. | Empty row separates the metadata block from the trades table. |
| 5 | Compare row 7 (column headers) and each subsequent data row against the on-screen trades table. | All 17 columns present in the documented order. Each trade row's values match the corresponding on-screen table row exactly (ticker, dates, prices, realised P&L, tags). |
| 6 | For the UK trade row, confirm the FX rate columns. | Entry/Exit FX Rate columns are empty (UK trades have no FX rate). |
| 7 | For the US trade row, confirm the FX rate columns. | Entry/Exit FX Rate columns are populated with the trade's stored FX rates. |

#### Pass criteria

- File opens cleanly in a standard spreadsheet application with correct character encoding.
- Every metadata and trade-row value matches the on-screen page exactly — the export is not a re-derivation, it is the same data.
- UK vs US trade rows correctly show empty vs populated FX rate columns.

---

### SC-CSVX-03 — Empty tax year — CSV still downloads with valid (metadata-only) structure

**Component:** Exported CSV file content
**API:** `GET /reports/tax-year?year=YYYY&format=csv` returning zero trades
**Priority:** P2

#### Preconditions

- A tax year exists with zero closed trades.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | On a tax year with zero closed trades, click "Download CSV". | Button remains enabled (per spec — valid for empty years) and the download fires normally. |
| 2 | Open the downloaded file. | File contains the 5-row metadata block (all zero values), a blank row, and the 17-column header row — with no trade data rows following it. Not an empty or error file. |

#### Pass criteria

- CSV downloads successfully for a zero-trade year (button not disabled).
- File structure remains valid: metadata block + header row present even with no data rows.

---

### SC-CSVX-04 — CSV export requires authentication (parity with JSON/PDF)

**Component:** `GET /reports/tax-year?format=csv` auth enforcement
**Priority:** P1

#### Preconditions

- Production or staging environment with `API_KEY` configured (this scenario does not apply to local dev with no `API_KEY` set — auth is skipped entirely in that mode, see `api_key_middleware`).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Issue `GET /reports/tax-year?year=YYYY&format=csv` with no `X-API-Key` header. | `401 Unauthorized`, standard error envelope — no CSV content returned. |
| 2 | Issue the same request with an incorrect `X-API-Key` value. | `401 Unauthorized`. |
| 3 | Issue the same request with the correct `X-API-Key` value. | `200`, CSV content returned as normal. |

#### Pass criteria

- `format=csv` is rejected pre-route exactly like the JSON and PDF formats — no separate or weaker auth path for exports.
- Backend equivalent: `tests/test_reports_integration.py::TestTaxYearCsvExport::test_ac02_csv_format_returns_401_without_api_key_when_configured` / `test_ac02_csv_format_returns_200_with_valid_api_key`.

---

## 4. Out of Scope

- PDF export rendering — covered by ST-12 QA evidence (Director of Quality sign-off against staging).
- Backend CSV content structure/byte-level assertions — covered by `tests/test_reports_integration.py::TestTaxYearCsvExport` (11 tests).
- Backend tax year boundary logic — covered by `tests/test_reports_integration.py` (other test classes) and `reports_scenarios.md` SC-TAX-03.
- Multi-user or multi-portfolio attribution — out of scope (single-user deployment).
