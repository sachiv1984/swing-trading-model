**Owner:** API Contracts & Documentation Owner
**Class:** Class 2 Canonical Specification
**Status:** Active
**Version:** 1.3
**Last Updated:** 2026-08-10 (ST-21, BLG-FEAT-29, v8.5 — added GET /screener/regime-distribution); prior — 2026-06-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Schema reference:** docs/specs/screener_results_schema.md

---

# Screener Internal API Contract

**Purpose:** Defines the canonical API contract for the internal screener endpoints served by this system's backend. These endpoints expose the Arc 1 Strategy-Rules Screener Engine (DS-01) outputs to the frontend and to the screener results page (DS-02).

---

## GET /screener/results

Returns screener result records from the latest completed screener run (or a specified run).

**Authentication:** Standard API key authentication (per `docs/specs/api_contracts/conventions.md`).

### Request

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `limit` | query | integer | NO | Number of results to return. Default: 50. Maximum: 200 |
| `offset` | query | integer | NO | Pagination offset. Default: 0 |
| `market` | query | enum(`"US"`, `"UK"`, `"all"`) | NO | Filter by market. Default: `"all"` |
| `run_id` | query | string (UUID) | NO | Return results from a specific run. Omit for latest completed run |

### Response (HTTP 200)

```json
{
  "ok": true,
  "data": {
    "results": [ ...ScreenerResultRecord... ],
    "run_id": "3f2a1b4c-...",
    "run_timestamp": "2026-04-23T08:00:00Z",
    "total": 12,
    "limit": 50,
    "offset": 0,
    "degraded_run": false,
    "failure_rate": 0.04,
    "tickers_requested": 500,
    "tickers_loaded": 480,
    "tickers_failed": ["BBBY", "SVFAU"],
    "run_quality": "FULL",
    "last_full_run_utc": "2026-06-19T08:00:00Z"
  }
}
```

| Response field | Type | Description |
|---------------|------|-------------|
| `degraded_run` | boolean | `true` when >20% of tickers returned no OHLCV data during the run |
| `failure_rate` | float | Fraction of tickers with no OHLCV data (0.0–1.0) |
| `tickers_requested` | int | Number of tickers the screener attempted to evaluate in this run |
| `tickers_loaded` | int | Number of tickers that successfully returned OHLCV data |
| `tickers_failed` | list\<string\> | Tickers that failed to load OHLCV data. Empty list when `run_quality = FULL` |
| `run_quality` | string | `FULL` (≤20% failure), `DEGRADED` (>20% failure), or `FAILED` (no tickers loaded) |
| `last_full_run_utc` | string \| null | ISO-8601 timestamp of most recent FULL run. `null` if no FULL run recorded yet |

**ScreenerResultRecord fields:** See `docs/specs/screener_results_schema.md §1.1`.

**Ordering:** Results are ordered by `signal_score` descending (highest momentum first) by default. This default must be preserved when no sort parameter is provided.

### Error Responses

| HTTP status | Code | Description |
|------------|------|-------------|
| 404 | `NO_RESULTS` | No completed screener run found (no runs have been executed yet) |
| 400 | `INVALID_PARAMS` | Invalid query parameters (e.g. `limit` exceeds 200) |

---

## POST /screener/run

Triggers a new screener run. The run executes asynchronously; results are available via `GET /screener/results?run_id={run_id}` once complete.

**Authentication:** Standard API key authentication.

### Request Body (optional JSON)

```json
{
  "ticker_universe": ["NVDA", "AAPL", "MSFT"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker_universe` | array\<string\> | NO | Override the default ticker universe for this run. If omitted, the configured default ticker list is used |

### Response (HTTP 202 — Accepted)

```json
{
  "ok": true,
  "data": {
    "run_id": "3f2a1b4c-...",
    "status": "accepted"
  }
}
```

**`run_id`** is the UUID assigned to this run. Use it to poll for results.

### Error Responses

| HTTP status | Code | Description |
|------------|------|-------------|
| 409 | `RUN_IN_PROGRESS` | A screener run is already in progress. Wait for it to complete before triggering another |
| 400 | `INVALID_TICKER` | One or more tickers in `ticker_universe` are invalid (malformed symbol) |

---

## GET /screener/regime-distribution

Returns the aggregate market regime (risk-on / risk-off) distribution over screener run history, for the requested rolling window. ST-21 (BLG-FEAT-29, EPIC-06, v8.5) — "Regime History" panel, Screener Results page. Design source: `docs/design/2026-08-08__release-v8.5/regime-distribution-panel/decision_record.md`.

**Authentication:** Standard API key authentication (per `docs/specs/api_contracts/conventions.md`).

### Request

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `window` | query | enum(`"30d"`, `"60d"`, `"all"`) | NO | Rolling window over `screener_runs.run_timestamp`. Default: `"30d"` |

### Response (HTTP 200)

```json
{
  "ok": true,
  "data": {
    "window": "30d",
    "run_count": 28,
    "total_observations": 56,
    "risk_on_count": 41,
    "risk_off_count": 15,
    "risk_on_pct": 73.2,
    "risk_off_pct": 26.8
  }
}
```

| Response field | Type | Description |
|---------------|------|-------------|
| `window` | string | Echoes the requested window |
| `run_count` | int | Number of `screener_runs` rows within the window (regardless of whether either market's regime resolved) |
| `total_observations` | int | Total per-market regime observations counted (`risk_on_count + risk_off_count`) — up to 2 per run (one for US, one for UK), fewer if a market's regime failed to resolve for a given run (`regime_us`/`regime_uk` NULL) |
| `risk_on_count` / `risk_off_count` | int | Count of per-market observations in each regime, summed across US and UK |
| `risk_on_pct` / `risk_off_pct` | float \| null | Percentage of `total_observations` in each regime, rounded to 1 decimal place. Both `null` when `total_observations = 0` (no runs in window, or all runs had unresolved regimes) — the frontend renders `DataState`'s `empty` branch in this case, per the design decision record, rather than a misleading `0%/0%` split |

**Aggregation note:** Sourced from `screener_runs.regime_us`/`regime_uk` (one row per run), not `screener_results` (one row per ticker) — using the per-ticker table would weight the distribution by how many tickers happened to be evaluated in each market on a given day, not by how often each market has actually been in each regime. Each run contributes one observation per market that has a non-null regime value.

### Error Responses

| HTTP status | Code | Description |
|------------|------|-------------|
| 400 | `INVALID_PARAMS` | `window` is not one of `30d`, `60d`, `all` |

---

## Pagination

`GET /screener/results` supports offset-based pagination:

- `total`: total number of results in this run
- `limit`: number of results returned in this response
- `offset`: starting position in the result set

**Example:** To retrieve page 2 with 20 results per page: `GET /screener/results?limit=20&offset=20`

---

## Authentication Requirements

All three endpoints use standard bearer token authentication as defined in `docs/specs/api_contracts/conventions.md`. No special screener-specific authentication is required.

---

## DoQ Sign-Off

- [x] `GET /screener/results`, `POST /screener/run`, and `GET /screener/regime-distribution` endpoints documented at `##` heading level
- [x] Request/response schemas defined with field names, types, and pagination for GET
- [x] Error codes documented
- [x] Authentication requirements documented
- [x] Corresponding OpenAPI entries added to `docs/reference/openapi.yaml`
- [x] Document added to Specs_Index.md (via §3.4b registration in ST-01 commit)
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-04-23
- Comments: Autonomous class sign-off — all four qualifying criteria met.

**v1.3 addendum (2026-08-10, ST-21, BLG-FEAT-29, EPIC-06, v8.5):** Added `GET /screener/regime-distribution`. Same DoQ checklist re-confirmed for the new endpoint: documented at `##` level, request/response schema and error codes defined, authentication requirements unchanged, OpenAPI entry added in the same commit, endpoint test suite registration added in the same commit (`backend/routers/test.py`).
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-10
