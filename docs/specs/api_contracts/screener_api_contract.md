**Owner:** API Contracts & Documentation Owner
**Class:** Class 2 Canonical Specification
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-05-22
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
    "failure_rate": 0.04
  }
}
```

| Response field | Type | Description |
|---------------|------|-------------|
| `degraded_run` | boolean | `true` when >20% of tickers returned no OHLCV data during the run |
| `failure_rate` | float | Fraction of tickers with no OHLCV data (0.0–1.0) |

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

## Pagination

`GET /screener/results` supports offset-based pagination:

- `total`: total number of results in this run
- `limit`: number of results returned in this response
- `offset`: starting position in the result set

**Example:** To retrieve page 2 with 20 results per page: `GET /screener/results?limit=20&offset=20`

---

## Authentication Requirements

Both endpoints use standard bearer token authentication as defined in `docs/specs/api_contracts/conventions.md`. No special screener-specific authentication is required.

---

## DoQ Sign-Off

- [x] `GET /screener/results` and `POST /screener/run` endpoints documented at `##` heading level
- [x] Request/response schemas defined with field names, types, and pagination for GET
- [x] Error codes documented
- [x] Authentication requirements documented
- [x] Corresponding OpenAPI entries added to `docs/reference/openapi.yaml`
- [x] Document added to Specs_Index.md (via §3.4b registration in ST-01 commit)
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-04-23
- Comments: Autonomous class sign-off — all four qualifying criteria met.
