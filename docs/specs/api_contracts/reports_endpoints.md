# reports_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.12
**Last Updated:** 2026-08-07
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines **Reports** domain endpoints.

- Tax-year P&L statement: a structured, server-side generated financial record of all realised gains and losses within a specified UK tax year.
- Monthly P&L summary: month-by-month breakdown of realised P&L for the current and prior calendar year.
- Daily P&L summary: day-by-day breakdown of realised P&L for a single calendar month (Trade History Calendar View, v7.5).

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

> ⚠️ **Disclaimer:** The tax-year P&L report is provided for user reference only. It is not a substitute for qualified tax advice. Users are responsible for verifying the figures against their broker records and obtaining appropriate professional advice before submitting any tax return.

> **Scope constraint:** This report is designed for UK-based trading accounts. The tax-year boundary follows the UK definition (6 April to 5 April). Non-UK tax treatment is out of scope.

---

## Endpoints

- [GET /reports/tax-year](#get-reportstax-year)
- [GET /reports/monthly-pnl](#get-reportsmonthly-pnl)
- [GET /reports/daily-pnl](#get-reportsdaily-pnl)
- [GET /reports/reconciliation](#get-reportsreconciliation)

---

## GET /reports/tax-year

**Purpose**

Returns a structured P&L statement for all **closed trades** whose `exit_date` falls within the specified UK tax year. This is a formal financial record for tax reference purposes — not an analytics view. It is distinct from `GET /analytics/metrics` (which covers all-time performance statistics) and `GET /trades` (which returns all closed trades without tax-year framing or summary structure).

**Method & Path**

- `GET /reports/tax-year`

**Idempotency**

- Safe to refresh (read-only). The `estimated_unrealised_pnl` field reflects live open positions at time of request and may vary between calls.

---

### Request

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `year` | integer | Yes | The start year of the UK tax year. `year=2025` returns the 2025/26 tax year (6 April 2025 to 5 April 2026). Must be a four-digit integer. |
| `format` | string | No | Response format. Omit for JSON (default). Pass `format=pdf` for a PDF download. Pass `format=csv` for a CSV download. Accepted values: `pdf`, `csv`. |

#### Validation rules

- `year` must be a four-digit positive integer (e.g. `2024`, `2025`).
- `year` must not be in the future (tax year whose `tax_year_start` is after today's date).
- If `year` is absent: return `400` — "year parameter is required."
- If `year` is invalid: return `400` — "year must be a valid four-digit integer."
- If `year` is in the future: return `400` — "tax year has not started yet."
- If `format` is present and not `pdf` or `csv`: return `400` — "format must be one of: pdf, csv."

---

### Response (200 — JSON, default)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "tax_year_start": "2025-04-06",
  "tax_year_end": "2026-04-05",
  "tax_year_label": "2025/26",
  "generated_at": "2026-03-17T10:30:00Z",
  "summary": {
    "total_closed_trades": 18,
    "total_realised_pnl": 3240.50,
    "total_gross_profit": 4810.00,
    "total_gross_loss": -1569.50,
    "win_count": 12,
    "loss_count": 6,
    "win_rate": 66.7,
    "estimated_unrealised_pnl": 820.00,
    "unrealised_note": "Reflects current open positions at time of report generation, not positions open during the specified tax year. Indicative only — not a tax liability."
  },
  "trades": [
    {
      "id": "750e8400-e29b-41d4-a716-446655440000",
      "ticker": "NVDA",
      "market": "US",
      "entry_date": "2025-05-12",
      "exit_date": "2025-08-03",
      "holding_days": 83,
      "entry_price_native": 622.00,
      "exit_price_native": 710.50,
      "entry_fx_rate": 1.2650,
      "exit_fx_rate": 1.2830,
      "shares": 10.5,
      "total_cost_gbp": 5162.45,
      "exit_proceeds_gbp": 5817.80,
      "realised_pnl_gbp": 655.35,
      "pnl_pct": 12.69,
      "currency": "USD",
      "tags": ["momentum", "tech"],
      "trade_origin": "Manual"
    }
  ]
}
```

#### Field definitions — `data`

| Field | Type | Description |
|-------|------|-------------|
| `tax_year_start` | string (YYYY-MM-DD) | First day of the specified UK tax year (always 6 April of `year`) |
| `tax_year_end` | string (YYYY-MM-DD) | Last day of the specified UK tax year (always 5 April of `year + 1`) |
| `tax_year_label` | string | Human-readable label e.g. `"2025/26"` |
| `generated_at` | string (ISO 8601) | UTC timestamp at which the report was generated |

#### Field definitions — `summary`

| Field | Type | Description |
|-------|------|-------------|
| `total_closed_trades` | integer | Count of closed trades with `exit_date` within the tax year |
| `total_realised_pnl` | float | Sum of `realised_pnl_gbp` across all trades in the tax year. GBP. Fee-inclusive. |
| `total_gross_profit` | float | Sum of `realised_pnl_gbp` for winning trades only (pnl > 0). GBP. |
| `total_gross_loss` | float | Sum of `realised_pnl_gbp` for losing trades only (pnl ≤ 0). GBP. Negative value or zero. |
| `win_count` | integer | Number of trades with `realised_pnl_gbp > 0` |
| `loss_count` | integer | Number of trades with `realised_pnl_gbp ≤ 0` |
| `win_rate` | float | `win_count / total_closed_trades × 100`. `0.0` when `total_closed_trades = 0`. |
| `estimated_unrealised_pnl` | float | Sum of `pnl` from currently open positions (from `positions` table). GBP. See `unrealised_note`. |
| `unrealised_note` | string | Fixed explanatory note on the provenance and limitations of `estimated_unrealised_pnl` |

#### Field definitions — `trades[]`

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | No | Trade record identifier (`trade_history.id`) |
| `ticker` | string | No | Stock ticker symbol |
| `market` | string | No | `"UK"` or `"US"` |
| `entry_date` | string (YYYY-MM-DD) | No | Date of position entry |
| `exit_date` | string (YYYY-MM-DD) | No | Date of position exit. Determines tax year attribution. |
| `holding_days` | integer | No | Calendar days from entry to exit |
| `entry_price_native` | float | No | Entry price in native currency (GBP for UK stocks, USD for US stocks) |
| `exit_price_native` | float | No | Exit price in native currency |
| `entry_fx_rate` | float | Yes | GBP/USD rate at entry. `null` for UK stocks. |
| `exit_fx_rate` | float | Yes | GBP/USD rate at exit. `null` for UK stocks. |
| `shares` | float | No | Number of shares |
| `total_cost_gbp` | float | No | Entry cost in GBP including entry fees (`trade_history.total_cost`). |
| `exit_proceeds_gbp` | float | No | Exit value in GBP net of exit fees (`trade_history.exit_proceeds`). |
| `realised_pnl_gbp` | float | No | `exit_proceeds_gbp - total_cost_gbp`. GBP. Fee-inclusive. Equivalent to `trade_history.pnl`. |
| `pnl_pct` | float | No | `realised_pnl_gbp / total_cost_gbp × 100` |
| `currency` | string | No | Native currency of the stock (`"GBP"` or `"USD"`) |
| `tags` | array of string | No | Trade tags. Empty array if none. |
| `trade_origin` | string | No | *(v0.12 — ST-31, BLG-FEAT-78)* `"Signal"` if the trade's linked trade plan (if any) has a non-null `signal_id` (momentum screener signal, see `data_model.md §Signals Table`), else `"Manual"`. **Not** a price-alert indicator — `price_alerts` (`BLG-FE-116`) has no schema linkage to any trade and cannot currently be distinguished this way; see `ESC-EXEC-20260807-01` (resolved) for the scoping decision. |

---

### Response (200 — PDF, `format=pdf`)

When `format=pdf` is supplied, the endpoint returns a PDF document instead of the standard JSON envelope.

**Response headers:**

| Header | Value |
|--------|-------|
| `Content-Type` | `application/pdf` |
| `Content-Disposition` | `attachment; filename="tax-year-{year}-pnl.pdf"` |

**PDF content (sourced entirely from the existing JSON response — no new data):**

- Report title: `"Tax Year P&L — {tax_year_label}"`
- Generation timestamp (UTC)
- Summary bar: `total_realised_pnl`, `total_gross_profit`, `total_gross_loss`, `win_rate`, `total_closed_trades`
- Trades table: all columns from `trades[]` array (ticker, market, dates, prices, FX rates, shares, cost/proceeds/P&L in GBP, currency, tags). **Excludes `trade_origin`** (v0.12 — ST-31) — the PDF table's column set is a fixed, hand-maintained list in `build_tax_year_pdf()`, not a dynamic render of every `trades[]` field; adding `trade_origin` to the PDF is out of ST-31's scope (CSV only per its acceptance criteria).
- Disclaimer text verbatim (see Overview section)
- Empty year is valid — PDF renders with summary zeros and no trade rows

**Library:** `reportlab` (pure Python; no system-level dependencies).

---

### Response (200 — CSV, `format=csv`)

When `format=csv` is supplied, the endpoint returns a CSV file instead of the standard JSON envelope.

**Response headers:**

| Header | Value |
|--------|-------|
| `Content-Type` | `text/csv; charset=utf-8` — see Charset note below |
| `Content-Disposition` | `attachment; filename="tax-year-{year}-pnl.csv"` |

**Charset (v0.8 — ST-07, BLG-SPEC-84, AC-01; corrected same-day, see Changelog):** the route handler sets `media_type="text/csv"` with no explicit charset, but the actual response header is `text/csv; charset=utf-8` — Starlette's `Response` class auto-appends `; charset=utf-8` to any `text/*` media type unless charset is explicitly suppressed. Confirmed by direct assertion against the live `TestClient` response (`tests/test_reports_integration.py::TestTaxYearCsvExport::test_ac01_content_type_header`), not inferred from source reading alone — an earlier version of this note claimed no charset was present, which was wrong (source-only inference; the framework's implicit behaviour wasn't accounted for). The body itself is also explicitly UTF-8-encoded (`build_tax_year_csv()`'s output `.encode("utf-8")`), so header and body charset agree.

**CSV structure:**

The file has two sections separated by a blank row: a metadata header block and a trades table.

**Section 1 — Metadata (rows 1–5):**

```
Tax Year,2025/26
Generated At,2026-03-20T10:00:00Z
Total Realised P&L (GBP),3240.50
Total Closed Trades,18
Win Rate (%),66.7
```

Each row is a key/value pair. Five rows, always present. Numeric values use the same precision as the JSON response.

**Section 2 — Trades table (from row 7 onward, after one blank row):**

Row 6 is blank. Row 7 is the column header row. Rows 8+ are trade data rows.

**Column headers and source mapping:**

| CSV Column Header | JSON field | Notes |
|-------------------|-----------|-------|
| `Trade ID` | `id` | UUID |
| `Ticker` | `ticker` | |
| `Market` | `market` | `UK` or `US` |
| `Entry Date` | `entry_date` | `YYYY-MM-DD` |
| `Exit Date` | `exit_date` | `YYYY-MM-DD` |
| `Holding Days` | `holding_days` | integer |
| `Entry Price (Native)` | `entry_price_native` | |
| `Exit Price (Native)` | `exit_price_native` | |
| `Entry FX Rate (GBP/USD)` | `entry_fx_rate` | empty for UK stocks |
| `Exit FX Rate (GBP/USD)` | `exit_fx_rate` | empty for UK stocks |
| `Shares` | `shares` | |
| `Total Cost (GBP)` | `total_cost_gbp` | |
| `Exit Proceeds (GBP)` | `exit_proceeds_gbp` | |
| `Realised P&L (GBP)` | `realised_pnl_gbp` | |
| `P&L %` | `pnl_pct` | |
| `Currency` | `currency` | `GBP` or `USD` |
| `Tags` | `tags` | semicolon-separated if multiple; empty if none |
| `Trade Origin` | `trade_origin` | *(v0.12 — ST-31)* `Signal` or `Manual` — see `trades[]` field definition above |

**Rules:**
- Column order is fixed as listed above.
- All 18 columns always present regardless of market.
- Null / empty values render as empty string (no quotes, no `null` text).
- Numeric values are unquoted. String values containing commas are quoted.
- Tags with multiple values are joined with `; ` (semicolon + space): e.g. `momentum; tech`.
- Empty year is valid — metadata section renders with zero summary values; no trade rows follow the header.
- No trailing newline after the last data row.

**Example (2 trades):**

```
Tax Year,2025/26
Generated At,2026-03-20T10:00:00Z
Total Realised P&L (GBP),3240.50
Total Closed Trades,2
Win Rate (%),100.0

Trade ID,Ticker,Market,Entry Date,Exit Date,Holding Days,Entry Price (Native),Exit Price (Native),Entry FX Rate (GBP/USD),Exit FX Rate (GBP/USD),Shares,Total Cost (GBP),Exit Proceeds (GBP),Realised P&L (GBP),P&L %,Currency,Tags,Trade Origin
750e8400-e29b-41d4-a716-446655440000,NVDA,US,2025-05-12,2025-08-03,83,622.00,710.50,1.2650,1.2830,10.5,5162.45,5817.80,655.35,12.69,USD,momentum,Signal
880e8400-e29b-41d4-a716-446655440001,FRES.L,UK,2025-06-01,2025-09-15,106,8.20,9.45,,,,1025.00,1178.75,153.75,15.00,GBP,,Manual
```

---

### Derivation Notes

**Tax year attribution**
A trade is included in the tax year if and only if `trade_history.exit_date` falls within `[tax_year_start, tax_year_end]` inclusive. The entry date does not affect attribution.

**Fee treatment**
`realised_pnl_gbp` is net of all fees. `total_cost_gbp` includes entry commission and stamp duty (where applicable). `exit_proceeds_gbp` is net of exit commission. No additional fee calculation is performed at report generation time.

**GBP conversion for US trades**
US trade P&L is converted to GBP at the time of trade close using `exit_fx_rate` stored in `trade_history`. The report does not re-apply FX conversion. The GBP values in the report match the values stored at trade close.

**Open positions (unrealised)**
`estimated_unrealised_pnl` is derived from `positions.pnl` for all currently open positions. It is not scoped to the specified tax year — it reflects the current portfolio state at report generation time.

**Empty tax year**
If no trades have `exit_date` within the specified tax year: `total_closed_trades = 0`, all summary numeric fields are `0.0`, and `trades = []`.

**Authentication (v0.8 — ST-07, BLG-SPEC-84, AC-02):** All response formats of this endpoint (JSON, PDF, CSV) require the same `X-API-Key` header as every other endpoint. Enforcement is global — `api_key_middleware` in `backend/main.py` validates the header for every request before route dispatch, with the sole exceptions of `OPTIONS` (CORS preflight) and `GET /health`. There is no separate or weaker auth path for the export formats; a request without a valid key receives `401` before `format=csv`/`format=pdf` handling ever executes, identical to the JSON path. Confirmed by direct code read of `api_key_middleware` — no per-route bypass exists for this or any other financial endpoint.

**Record classification (v0.8 — ST-07, BLG-SPEC-84, AC-03):** The CSV/PDF exports are classified as an **analytics/convenience export**, not a financial record of authority. The canonical, authoritative record of every trade remains `trade_history` in the database — the export is a point-in-time, server-rendered *view* of that data for the user's own reference (see the page-level disclaimer: "This report is provided for user reference only... not a substitute for qualified tax advice"). Consequences of this classification: (a) no retention/archival requirement beyond the underlying `trade_history` rows themselves — the CSV/PDF files are not persisted server-side, only generated on request; (b) no immutability guarantee on the export format — the CSV column set may be extended in a future version without a breaking-change version bump, since it is a read view, not a stored contract; (c) versioning approach: this contract document's own `**Version:**` header is the sole version marker for the CSV/PDF shape (no separate `format_version` field in the response), consistent with how `format=pdf` has always been treated — a schema-breaking column reorder or removal (not an addition) would require a version bump here and a corresponding entry in `Appendix B` of `metrics_definitions.md` style API schema coverage if the fields feed any metric, though none currently do.

---

### Error Responses

Errors use the standard error envelope from **conventions.md §13**.

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `year` parameter absent, non-integer, or invalid format |
| `400` | `year` results in a tax year that has not yet started (future year) |
| `500` | Internal server error |

---

### Example Requests

```
GET /reports/tax-year?year=2025
GET /reports/tax-year?year=2025&format=pdf
```

### Example Response (200 — trades present)

```json
{
  "status": "ok",
  "data": {
    "tax_year_start": "2025-04-06",
    "tax_year_end": "2026-04-05",
    "tax_year_label": "2025/26",
    "generated_at": "2026-03-17T10:30:00Z",
    "summary": {
      "total_closed_trades": 3,
      "total_realised_pnl": 1240.75,
      "total_gross_profit": 1580.25,
      "total_gross_loss": -339.50,
      "win_count": 2,
      "loss_count": 1,
      "win_rate": 66.7,
      "estimated_unrealised_pnl": 420.00,
      "unrealised_note": "Reflects current open positions at time of report generation, not positions open during the specified tax year. Indicative only — not a tax liability."
    },
    "trades": [
      {
        "id": "750e8400-e29b-41d4-a716-446655440000",
        "ticker": "NVDA",
        "market": "US",
        "entry_date": "2025-05-12",
        "exit_date": "2025-08-03",
        "holding_days": 83,
        "entry_price_native": 622.00,
        "exit_price_native": 710.50,
        "entry_fx_rate": 1.2650,
        "exit_fx_rate": 1.2830,
        "shares": 10.5,
        "total_cost_gbp": 5162.45,
        "exit_proceeds_gbp": 5817.80,
        "realised_pnl_gbp": 655.35,
        "pnl_pct": 12.69,
        "currency": "USD",
        "tags": ["momentum"]
      }
    ]
  }
}
```

### Example Response (200 — no trades)

```json
{
  "status": "ok",
  "data": {
    "tax_year_start": "2024-04-06",
    "tax_year_end": "2025-04-05",
    "tax_year_label": "2024/25",
    "generated_at": "2026-03-17T10:30:00Z",
    "summary": {
      "total_closed_trades": 0,
      "total_realised_pnl": 0.0,
      "total_gross_profit": 0.0,
      "total_gross_loss": 0.0,
      "win_count": 0,
      "loss_count": 0,
      "win_rate": 0.0,
      "estimated_unrealised_pnl": 420.00,
      "unrealised_note": "Reflects current open positions at time of report generation, not positions open during the specified tax year. Indicative only — not a tax liability."
    },
    "trades": []
  }
}
```

### Example Response (400 — invalid year)

```json
{
  "status": "error",
  "message": "year must be a valid four-digit integer"
}
```

---

---

## GET /reports/monthly-pnl

**Purpose**

Returns month-by-month realised P&L for the current and prior calendar year. Used by the Financial Reporting section to render a monthly breakdown table alongside the existing annual tax-year report.

**Method & Path**

- `GET /reports/monthly-pnl`

**Idempotency**

- Safe to refresh (read-only).

---

### Request

No query parameters.

---

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

Array of monthly summary objects, sorted descending by year then month. Only months with closed trades are included.

```json
[
  { "year": 2026, "month": 4, "realised_pnl_gbp": 340.50, "trade_count": 3 },
  { "year": 2026, "month": 3, "realised_pnl_gbp": -120.00, "trade_count": 1 },
  { "year": 2025, "month": 12, "realised_pnl_gbp": 875.25, "trade_count": 5 }
]
```

#### Field definitions

| Field | Type | Description |
|-------|------|-------------|
| `year` | integer | Calendar year of the trades |
| `month` | integer | Calendar month (1=January, 12=December) |
| `realised_pnl_gbp` | float | Sum of `pnl` for all closed trades with `exit_date` in this month. GBP. Fee-inclusive. Negative if net loss. |
| `trade_count` | integer | Count of closed trades with `exit_date` in this month |

**Scope:** Returns data for the current calendar year and the prior calendar year only (24 months maximum). Empty array if no closed trades exist in scope.

#### `compliance_summary` schema (ST-03, v4.7)

Object containing Arc 5 pre-entry discipline metrics for the last 30 days. `null` if database is unavailable.

```json
{
  "period_days": 30,
  "validation_pass_rate": 0.82,
  "override_count": 2,
  "red_flag_events_count": 5,
  "most_frequent_rule_breach": "sector_concentration"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `period_days` | integer | Period in days used for the compliance metrics (30) |
| `validation_pass_rate` | float \| null | Overall pass rate across all pre-entry validation rules in the period (0.0–1.0); `null` if no validation log data |
| `override_count` | integer | Count of `pre_entry_override` events in the last 7 days |
| `red_flag_events_count` | integer | Count of all red flag events in the period |
| `most_frequent_rule_breach` | string \| null | Rule type most frequently failing in the period; `null` if none |

Source: `pre_entry_validation_log` and `red_flag_events` tables. See `arc5_compliance_analytics.md` for rule type definitions.

#### `estimated_unrealised_pnl` / `unrealised_note` (v0.7, ST-14 — BLG-FEAT-70)

Top-level siblings of `data`, same field/computation as `GET /reports/tax-year`'s `summary.estimated_unrealised_pnl` — a current-snapshot sum of `pnl` across all currently open positions. Not attributed to any month; shown once, alongside the monthly table, not per row.

```json
{
  "status": "ok",
  "data": [ ... ],
  "estimated_unrealised_pnl": 340.50,
  "unrealised_note": "Reflects current open positions at time of report generation, not positions open during the specified tax year. Indicative only — not a tax liability.",
  "compliance_summary": { ... }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `estimated_unrealised_pnl` | float \| null | Sum of `pnl` across all currently open positions. `null` when there is no portfolio yet. |
| `unrealised_note` | string | Static disclaimer text — same value as the Tax Year report's `unrealised_note`. |

---

### CSV Export (v0.8, ST-05 — BLG-FEAT-81)

`GET /reports/monthly-pnl?format=csv` returns a CSV file download instead of JSON — mirrors `GET /reports/tax-year?format=csv`'s existing handler.

**Request**

```
GET /reports/monthly-pnl?format=csv
```

**Response (200)**

`Content-Type: text/csv`, `Content-Disposition: attachment; filename="monthly-pnl.csv"`.

Exports exactly the rows in the `data` array above (no separate metadata block, unlike the Tax Year CSV — per `monthly-csv-export/ux_spec.md` §3, this is a plain header row + one row per month, matching the on-screen Monthly Financial Table exactly):

```csv
Year,Month,Realised P&L (GBP),Trades
2026,4,340.5,3
2026,3,-120.0,1
2025,12,875.25,5
```

No client-side recalculation — values are identical to the `data` array's `realised_pnl_gbp`/`trade_count` fields, not re-derived.

**Reconciliation note (QA verification, not a response contract item):** both this endpoint and `GET /reports/tax-year`'s CSV export sum the same `trade_history.pnl` column directly (see `get_monthly_pnl()` and the tax-year trade query in `backend/database.py`) — no separate computation path exists for either, so there is no double-counting or drift between them at the ledger level. A literal numeric match between a calendar-year total in this export and a UK-tax-year total in the Tax Year export is not expected for years where the two windows don't align (calendar Jan–Dec vs UK tax year Apr–Apr) — this is an inherent property of the two different groupings, not a defect.

**Invalid format**

`GET /reports/monthly-pnl?format=xml` (or any value other than `csv`) returns `400`:

```json
{ "status": "error", "message": "format must be: csv" }
```

---

### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Internal server error |
| `400` | `format` query parameter is present and not `csv` |

---

### Example Request

```
GET /reports/monthly-pnl
GET /reports/monthly-pnl?format=csv
```

---

## GET /reports/daily-pnl

**Purpose**

Day-granularity sibling of `GET /reports/monthly-pnl` — returns day-by-day realised P&L for a single calendar month, for the Trade History Calendar View (ST-04, BLG-FE-118, v7.5). Same grouping logic as the monthly report, narrower window and finer bucket (readiness pass AC-02).

**Method & Path**

- `GET /reports/daily-pnl?year={year}&month={month}`

**Idempotency**

- Safe to refresh (read-only).

### Request

| Query Parameter | Type | Required | Description |
|------------------|------|----------|-------------|
| `year` | integer | Yes | Calendar year (e.g. `2026`) |
| `month` | integer | Yes | Calendar month, `1`–`12` |

### Response (200)

```json
{
  "status": "ok",
  "data": [
    { "day": 3, "realised_pnl_gbp": 240.50, "trade_count": 3 },
    { "day": 17, "realised_pnl_gbp": -85.00, "trade_count": 1 }
  ],
  "estimated_unrealised_pnl": 340.50,
  "unrealised_note": "Reflects current open positions at time of report generation, not positions open during the specified tax year. Indicative only — not a tax liability."
}
```

#### Field definitions

| Field | Type | Description |
|-------|------|-------------|
| `data[].day` | integer | Day of month (1–31) |
| `data[].realised_pnl_gbp` | float | Sum of `pnl` for closed trades with `exit_date` on this day. GBP. Negative if net loss. |
| `data[].trade_count` | integer | Count of closed trades exiting this day |
| `estimated_unrealised_pnl` | float \| null | Same field/computation as `GET /reports/monthly-pnl` — current-snapshot only, never attributed to any individual day (readiness pass AC-03). `null` when there is no portfolio yet. |
| `unrealised_note` | string | Same static disclaimer text as `GET /reports/monthly-pnl` / `GET /reports/tax-year`. |

**Scope:** Only days with 1+ closed-trade exits are included in `data`. Empty array if no closed trades in the given month.

### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `month` not in range 1–12 |
| `500` | Internal server error |

### Example Request

```
GET /reports/daily-pnl?year=2026&month=7
```

---

## GET /reports/reconciliation

**Purpose**

P&L / tax record reconciliation report (ST-01, EPIC-01, v8.2, BLG-FEAT-88): compares the Tax Year report's system-computed realised P&L total against an independently re-derived export-side sum for the same tax year, and surfaces a pass/fail match indicator to the user. Design source: `docs/design/2026-08-04__release-v8.2/pnl-reconciliation-report/decision_record.md`.

**Method & Path**

- `GET /reports/reconciliation?year={year}`

**Idempotency**

- Safe to refresh (read-only).

### Request

| Query Parameter | Type | Required | Description |
|------------------|------|----------|-------------|
| `year` | integer | Yes | The start year of the UK tax year (e.g. `2025` for 2025/26) |

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "tax_year_label": "2025/26",
    "total_closed_trades": 12,
    "system_total_pnl_gbp": 1500.00,
    "export_total_pnl_gbp": 1500.00,
    "matched": true
  }
}
```

#### Field definitions

| Field | Type | Description |
|-------|------|--------------|
| `tax_year_label` | string | e.g. `"2025/26"` — same format as `GET /reports/tax-year` |
| `total_closed_trades` | integer | Count of closed trades in the tax year — `0` means the empty state applies |
| `system_total_pnl_gbp` | float | Existing Tax Year summary `total_realised_pnl` for the year — unchanged computation |
| `export_total_pnl_gbp` | float | Independently re-derived sum of `trade_history.pnl` for the year, via a separate server-side query path from the one powering the Tax Year report/CSV export, so a divergence is meaningful rather than definitionally impossible |
| `matched` | boolean | `true` when `system_total_pnl_gbp` and `export_total_pnl_gbp` are equal within £0.01 rounding tolerance |

**Scope:** Reconciles realised P&L / trade export only. Unrealised P&L and portfolio `total_pnl` are out of scope (already covered by existing approximate-tie-back notes elsewhere on the Reports page).

### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `year` missing, not a valid four-digit integer, or tax year has not started yet |
| `404` | No portfolio found |
| `500` | Internal server error |

### Example Request

```
GET /reports/reconciliation?year=2025
```

---

## Known Deviations

**`trade_origin` scope (ST-31, BLG-FEAT-78, EPIC-01, v8.4, resolved via `ESC-EXEC-20260807-01`):** The originating backlog item described this field as a "trigger-source" column distinguishing alert-triggered trades from manual ones, gated on `BLG-FE-116` (custom price alerts) shipping. On implementation, no schema linkage was found between `price_alerts` and any trade/position/trade_plan row — firing a price alert only writes a notification, it never tags the resulting trade. That distinction therefore cannot be derived from any existing data. With Product Owner approval, the field was reinterpreted to use the one trigger-shaped field that does exist end-to-end — `trade_plans.signal_id` (the momentum-screener `signals` system, unrelated to price alerts) — and labeled accordingly (`"Signal"` / `"Manual"`), rather than shipping a column whose name would misrepresent what the data actually shows. If genuine price-alert-to-trade provenance is wanted in future, it requires new schema/backend work (linking `price_alerts` to the resulting trade) that does not exist yet — this deviation does not add that; it only avoids fabricating it.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.12 | 2026-08-07 | ST-31 (v8.4, EPIC-01, BLG-FEAT-78): Added `trade_origin` field (`"Signal"` / `"Manual"`) to `GET /reports/tax-year`'s `trades[]` array and its CSV export (`Trade Origin`, 18th/last column — additive, no breaking-change bump per this doc's own analytics/convenience-export versioning note). Derived from `trade_plans.signal_id` via the two-hop `trade_history.position_id = positions.id = trade_plans.position_id` relationship (`data_model.md`). **Scope correction (`ESC-EXEC-20260807-01`, resolved):** the backlog item's original "trigger-source"/alert-triggered framing was found to have no underlying schema linkage — `price_alerts` (`BLG-FE-116`) never tags a resulting trade — so the AC was reinterpreted, with Product Owner approval, to the real, already-wired `signal_id` distinction (momentum-screener signals) rather than shipping a column that would misrepresent trade provenance in a tax-relevant export. Not added to the PDF export (CSV-only per AC). |
| 0.11 | 2026-08-04 | ST-01 (v8.2, EPIC-01, BLG-FEAT-88): Added `## GET /reports/reconciliation` — P&L / tax record reconciliation report comparing the Tax Year report's system total against an independently re-derived export-side sum. Reuses `get_tax_year_report`'s `total_realised_pnl` for the system side; new `get_trade_history_pnl_sum_by_tax_year` DB function (server-side SQL SUM) for the export side, per the design gate's requirement for a genuinely separate query path. |
| 0.10 | 2026-07-26 | ST-05 (v7.8, EPIC-05, BLG-FEAT-81): Added `format=csv` to `GET /reports/monthly-pnl`, mirroring the existing `GET /reports/tax-year?format=csv` handler. CSV export is a plain header row + one row per month (no metadata block, unlike the Tax Year CSV) — `Year,Month,Realised P&L (GBP),Trades`. Invalid `format` values return 400. Reconciliation note added: both CSV exports sum the same `trade_history.pnl` column directly, no double-counting risk, though a literal calendar-year-vs-tax-year numeric match isn't expected given the different window boundaries. |
| 0.9 | 2026-07-20 | ST-04 (v7.5, EPIC-04, BLG-FE-118): Added `## GET /reports/daily-pnl` — day-granularity sibling of `GET /reports/monthly-pnl` for the Trade History Calendar View. Same `estimated_unrealised_pnl`/`unrealised_note` pattern (current-snapshot only, never per-day). |
| 0.8 | 2026-07-14 | v7.1 sprint execution (ST-07, BLG-SPEC-84): CSV export hardening pass — documented and test-verified `Content-Type` charset (AC-01: actual header is `text/csv; charset=utf-8`, Starlette auto-appends charset for `text/*`; corrected in the same edit after a test assertion caught the initial documentation claiming no charset was present), authentication parity confirmation (AC-02, global `api_key_middleware`, no per-route bypass, test-verified with `API_KEY` configured), and financial-record-vs-analytics-export classification with versioning approach (AC-03, export is a read view of `trade_history`, not a stored contract). No response schema/behaviour change. |
| 0.7 | 2026-07-13 | Add `estimated_unrealised_pnl`/`unrealised_note` top-level fields to GET /reports/monthly-pnl response — current-snapshot unrealised P&L, same field/computation as GET /reports/tax-year's `summary.estimated_unrealised_pnl`. `data` array shape unchanged. ST-14 (BLG-FEAT-70) — v7.0 cycle 2026-07-12__release-v7.0. |
| 0.6 | 2026-05-31 | Rename strategy_compliance → compliance_summary in GET /reports/monthly-pnl response (field rename; same schema, canonical name alignment). ST-03 — v4.7 cycle 2026-05-31__release-v4.7. |
| 0.5 | 2026-05-29 | Add strategy_compliance field to GET /reports/monthly-pnl response: 30d Arc 5 compliance metrics. ST-18 — v4.3 cycle 2026-05-29__release-v4.3. |
| 0.4 | 2026-04-30 | Add GET /reports/monthly-pnl endpoint: month-by-month realised P&L for current and prior year. ST-11 — v3.1 release planning cycle 2026-04-29__release-v3.1. |
| 0.3 | 2026-03-20 | Add `format=csv` to GET /reports/tax-year. CSV response schema documented: metadata block (5 rows) + trades table (17 human-readable columns). `format` validation rule tightened — unknown values now return 400. ST-13 — v2.1 release planning cycle 2026-03-18__release-v2.1. |
| 0.2 | 2026-03-19 | Add `format=pdf` query parameter to GET /reports/tax-year. PDF response schema documented. ST-12 — v2.1 release planning cycle 2026-03-18__release-v2.1. |
| 0.1 | 2026-03-17 | Initial version. GET /reports/tax-year. ST-03 — v2.0 release planning cycle 2026-03-17__release-v2.0. |
