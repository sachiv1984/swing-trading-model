# reports_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.3
**Last Updated:** 2026-03-20
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines **Reports** domain endpoints.

- Tax-year P&L statement: a structured, server-side generated financial record of all realised gains and losses within a specified UK tax year.

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

> ⚠️ **Disclaimer:** The tax-year P&L report is provided for user reference only. It is not a substitute for qualified tax advice. Users are responsible for verifying the figures against their broker records and obtaining appropriate professional advice before submitting any tax return.

> **Scope constraint:** This report is designed for UK-based trading accounts. The tax-year boundary follows the UK definition (6 April to 5 April). Non-UK tax treatment is out of scope.

---

## Endpoints

- [GET /reports/tax-year](#get-reportstax-year)

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
      "tags": ["momentum", "tech"]
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
- Trades table: all columns from `trades[]` array (ticker, market, dates, prices, FX rates, shares, cost/proceeds/P&L in GBP, currency, tags)
- Disclaimer text verbatim (see Overview section)
- Empty year is valid — PDF renders with summary zeros and no trade rows

**Library:** `reportlab` (pure Python; no system-level dependencies).

---

### Response (200 — CSV, `format=csv`)

When `format=csv` is supplied, the endpoint returns a CSV file instead of the standard JSON envelope.

**Response headers:**

| Header | Value |
|--------|-------|
| `Content-Type` | `text/csv` |
| `Content-Disposition` | `attachment; filename="tax-year-{year}-pnl.csv"` |

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

**Rules:**
- Column order is fixed as listed above.
- All 17 columns always present regardless of market.
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

Trade ID,Ticker,Market,Entry Date,Exit Date,Holding Days,Entry Price (Native),Exit Price (Native),Entry FX Rate (GBP/USD),Exit FX Rate (GBP/USD),Shares,Total Cost (GBP),Exit Proceeds (GBP),Realised P&L (GBP),P&L %,Currency,Tags
750e8400-e29b-41d4-a716-446655440000,NVDA,US,2025-05-12,2025-08-03,83,622.00,710.50,1.2650,1.2830,10.5,5162.45,5817.80,655.35,12.69,USD,momentum
880e8400-e29b-41d4-a716-446655440001,FRES.L,UK,2025-06-01,2025-09-15,106,8.20,9.45,,,,1025.00,1178.75,153.75,15.00,GBP,
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

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.3 | 2026-03-20 | Add `format=csv` to GET /reports/tax-year. CSV response schema documented: metadata block (5 rows) + trades table (17 human-readable columns). `format` validation rule tightened — unknown values now return 400. ST-13 — v2.1 release planning cycle 2026-03-18__release-v2.1. |
| 0.2 | 2026-03-19 | Add `format=pdf` query parameter to GET /reports/tax-year. PDF response schema documented. ST-12 — v2.1 release planning cycle 2026-03-18__release-v2.1. |
| 0.1 | 2026-03-17 | Initial version. GET /reports/tax-year. ST-03 — v2.0 release planning cycle 2026-03-17__release-v2.0. |
