**Owner:** API Contracts & Documentation Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.13
**Last Updated:** 2026-09-16 (ST-13, BLG-OPS-161, v9.5 — POST /ai/check-endpoint-anomalies latency now real-data (claude_audit_log.latency_ms), not simulated-only); prior — 2026-09-16 (ST-06, BLG-OPS-153, v9.5 — added GET /ai/spend-trend-by-feature); prior — 2026-09-15 (ST-23, BLG-AI-06, v9.4 — documented the generation-time AI output boundary-language sampling hook, not a new endpoint); prior history retained — see prior entries in version control
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Endpoints — API Contract

This document specifies AI-powered endpoints for the Momentum Trading Assistant.

All AI output is **display-only** and must NOT be used as input to any signal, scoring, compliance, or recommendation calculation. This constraint is mandated by SRB-v1.7 (2026-03-02) and is a hard architectural rule.

---

## Table of Contents

- [POST /ai/journal-summary](#post-aijournal-summary)
- [POST /ai/daily-briefing](#post-aidaily-briefing)
- [POST /ai/chat](#post-aichat)
- [POST /ai/check-daily-cost](#post-aicheck-daily-cost)
- [POST /ai/check-endpoint-anomalies](#post-aicheck-endpoint-anomalies)
- [GET /ai/claude-audit-log](#get-aiclaude-audit-log)
- [GET /ai/monthly-cost](#get-aimonthly-cost)
- [GET /ai/monthly-cost-by-feature](#get-aimonthly-cost-by-feature)

---

## POST /ai/journal-summary

Accepts a set of closed trade IDs or a date range, retrieves the associated journal entry/exit notes, and calls an external LLM API to produce a plain-text summary of themes and patterns across those notes. Returns summarised text.

**§13 Status:** CONDITIONALLY COMPLIANT — SRB-v1.7 (2026-03-02). AI output is read-only display; it does not feed into any signal, scoring, or recommendation pipeline.

### Request

```
POST /ai/journal-summary
Content-Type: application/json
```

#### Request body

```json
{
  "trade_ids": [1, 2, 3],
  "date_from": "2026-01-01",
  "date_to": "2026-03-31"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `trade_ids` | array of integers | Optional | Specific closed trade IDs to summarise. If provided, `date_from`/`date_to` are ignored. |
| `date_from` | string (YYYY-MM-DD) | Optional | Start date for trade filter (inclusive). Used when `trade_ids` not provided. |
| `date_to` | string (YYYY-MM-DD) | Optional | End date for trade filter (inclusive). Used when `trade_ids` not provided. |

At least one of `trade_ids` or a date range (`date_from` and/or `date_to`) must be provided. If neither is provided, returns HTTP 422.

Only closed trades (with `exit_date` set) are included in the summary. If no matching trades are found, returns HTTP 200 with `summary: null` and `message` explaining the absence.

### Response — 200 OK

```json
{
  "summary": "Across the selected trades, recurring themes include...",
  "trade_count": 8,
  "model": "claude-haiku-4-5-20251001",
  "cached": false,
  "message": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `summary` | string or null | LLM-generated summary text. `null` if no journal notes found or LLM unavailable. |
| `trade_count` | integer | Number of closed trades whose notes were included. |
| `model` | string | LLM model identifier used. |
| `cached` | boolean | Reserved for future caching; always `false` in v1.0. |
| `message` | string or null | Informational message when `summary` is null (e.g. "No journal notes found for the selected trades."). |

### Response — 503 Service Unavailable (LLM unreachable)

When the external LLM API is unreachable or returns an error, the endpoint returns HTTP 200 with `summary: null` and a `message` field — it does NOT propagate a 500.

```json
{
  "summary": null,
  "trade_count": 0,
  "model": null,
  "cached": false,
  "message": "AI summarisation is currently unavailable. Please try again later."
}
```

### Error responses

| Status | Condition |
|--------|-----------|
| 422 | Neither `trade_ids` nor a date range provided. |
| 401 | Missing or invalid API key. |

### Implementation constraints (hard rules — SRB-v1.7)

- AI summary output **must not** be stored in the database or used as input to any calculation.
- External LLM API key must be read from environment variable `ANTHROPIC_API_KEY`. No secrets in code.
- Default model: `claude-haiku-4-5-20251001`. Override via `AI_MODEL` env var.
- If LLM API is unreachable: return HTTP 200 with `summary: null` and informational `message`. Do not raise HTTP 500.
- Endpoint is read-only: no trade data is modified.

---

## POST /ai/daily-briefing

Assembles a read-only context object from live portfolio state and calls `claude-sonnet-4-6` to produce a plain-English daily summary and ordered action list. Advisory-only — display-only, not integrated with any trade execution path.

**§13 Status:** PASS — SRB-v1.7. LLM output is advisory-only, display-only. Does not modify positions, signals, or trade plans. See `docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`.

**Story:** ST-06 (BLG-FEAT-50, EPIC-02, v6.2)

### Request

```
POST /ai/daily-briefing
Content-Type: application/json
```

No request body required.

### Response — 200 OK

```json
{
  "summary": "Your portfolio has 3 open positions. NVDA is near its trailing stop — monitor closely today. Markets are risk-on with two strong new signals.",
  "actions": [
    { "type": "MONITOR", "ticker": "NVDA", "description": "Within 3% of trailing stop — watch closely." },
    { "type": "ENTER", "ticker": "AAPL", "description": "Rank #1 momentum signal today." }
  ],
  "generated_at": "2026-06-25T08:30:00Z",
  "advisory": true,
  "model": "claude-sonnet-4-6"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `summary` | string or null | Plain-English portfolio summary (2–4 sentences). `null` if LLM unavailable. |
| `actions` | array | Ordered action list. Empty array if no actions or LLM unavailable. |
| `actions[].type` | string | One of: `EXIT`, `ENTER`, `MONITOR`, `HOLD`. |
| `actions[].ticker` | string | Ticker symbol the action applies to. |
| `actions[].description` | string | Human-readable description of the action. |
| `generated_at` | string (ISO 8601) | UTC timestamp of generation. |
| `advisory` | boolean | Always `true`. Client must verify this field; render error if absent or false. |
| `model` | string or null | Model identifier used. `null` if LLM unavailable. |
| `error` | string or null | Error message when LLM unavailable (`summary` will be `null`). |

### Context assembled by backend

- Current portfolio state (cash, open position count)
- Per-position: ticker, market, current price, trailing stop, risk-off flag
- Today's top-5 momentum signals (most recent signal date)
- Market regime: SPY and FTSE MA200 status
- Month-end rebalance check

### Rate limiting

| Limit | Scope | Response |
|-------|-------|----------|
| 10 requests/minute | Per client IP | HTTP 429 with `Retry-After` header |

### Response — 429 Too Many Requests

Returned when the per-IP rate limit is exceeded.

```
HTTP/1.1 429 Too Many Requests
Retry-After: 42
Content-Type: application/json
```

```json
{
  "status": "error",
  "message": "Rate limit exceeded. Try again later."
}
```

| Header | Description |
|--------|-------------|
| `Retry-After` | Seconds until the oldest request in the window expires; client should wait this long before retrying. |

### Error responses

| Status | Condition |
|--------|-----------|
| 200 | Always returns 200 when rate limit not exceeded. LLM errors return `summary: null` with `error` message. |
| 401 | Missing or invalid API key. |
| 429 | Rate limit exceeded (10 req/min/IP). `Retry-After` header present. |

### Implementation constraints (SRB-v1.7)

- Uses `claude-sonnet-4-6` model.
- Token usage logged to `claude_audit_log` via `create_claude_audit_entry`.
- No writes to `positions`, `signals`, `trade_plans`, or any strategy table.
- `advisory: true` is always present in the response.
- Rate limit implementation: in-memory sliding-window (`backend/services/rate_limiter.py`). Limit applies per client IP. Single-process scope; sufficient for single-instance Render deployment.

---

## POST /ai/chat

Accepts a user question with optional context (ticker, position_id) and returns a response grounded in the full live portfolio and signal state. Stateless per request — no session memory stored or returned across calls. Advisory-only, display-only.

**§13 Status:** PASS — SRB-v1.7. LLM output is advisory-only, display-only. No integration with trade execution. See `docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`.

**Story:** ST-08 (BLG-FEAT-51, EPIC-02, v6.2)

### Request

```
POST /ai/chat
Content-Type: application/json
```

#### Request body

```json
{
  "question": "Which of my positions is closest to its trailing stop?",
  "context": {
    "ticker": "NVDA",
    "position_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | The user's question. |
| `context` | object | No | Optional focus: `ticker` (string) and/or `position_id` (UUID). Injected into system prompt context. |

### Response — 200 OK

```json
{
  "response": "NVDA is currently closest to its trailing stop, sitting 2.8% above the stop level of £450.00.",
  "advisory": true,
  "model": "claude-sonnet-4-6"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `response` | string | AI-generated answer grounded in live portfolio state. |
| `advisory` | boolean | Always `true`. |
| `model` | string or null | Model identifier used. |

### Stateless behaviour

Each call is independent — the backend loads fresh portfolio and signal state on every request. No conversation history is stored server-side. In-memory display history in the frontend is cleared on widget close.

### Context injected into system prompt

- Portfolio cash and open position count
- Per-position: ticker, market, current price, trailing stop, risk-off flag, P&L
- Latest top-5 momentum signals
- Optional: focused ticker from `context.ticker`

### Rate limiting

| Limit | Scope | Response |
|-------|-------|----------|
| 30 requests/minute | Per client IP | HTTP 429 with `Retry-After` header |

### Response — 429 Too Many Requests

Returned when the per-IP rate limit is exceeded.

```
HTTP/1.1 429 Too Many Requests
Retry-After: 28
Content-Type: application/json
```

```json
{
  "status": "error",
  "message": "Rate limit exceeded. Try again later."
}
```

| Header | Description |
|--------|-------------|
| `Retry-After` | Seconds until the oldest request in the window expires. |

### Error responses

| Status | Condition |
|--------|-----------|
| 200 | Always returns 200 when rate limit not exceeded. LLM errors return a `response` error string. |
| 422 | `question` field missing. |
| 401 | Missing or invalid API key. |
| 429 | Rate limit exceeded (30 req/min/IP). `Retry-After` header present. |

### Implementation constraints (SRB-v1.7)

- Uses `claude-sonnet-4-6` model.
- Token usage logged to `claude_audit_log` via `create_claude_audit_entry`.
- No writes to any table. Conversation state is not persisted.
- `advisory: true` always present.
- Rate limit implementation: in-memory sliding-window (`backend/services/rate_limiter.py`). Limit applies per client IP. Single-process scope; sufficient for single-instance Render deployment.

---

## POST /ai/check-daily-cost

Checks today's Claude API spend against the configured daily cost threshold. If the threshold is exceeded, sends a Telegram alert. Intended to be called by a daily scheduler (Render cron or external scheduler).

**§13 Status:** N/A — operational monitoring endpoint. No AI output generated; no display surface.

### Request

```
POST /ai/check-daily-cost
Content-Type: application/json
```

No request body required. Threshold is read from the `AI_DAILY_COST_THRESHOLD` environment variable (default: `1.00` USD/day).

### Response — 200 OK

```json
{
  "total_cost_usd": 0.42,
  "request_count": 7,
  "threshold_usd": 1.00,
  "threshold_exceeded": false,
  "alert_sent": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total_cost_usd` | float | Sum of `estimated_cost_usd` in `gemini_audit_log` for today (`generated_at >= CURRENT_DATE`). |
| `request_count` | integer | Number of Claude API requests logged today. |
| `threshold_usd` | float | Configured daily cost threshold (from `AI_DAILY_COST_THRESHOLD` env var). |
| `threshold_exceeded` | boolean | `true` when `total_cost_usd >= threshold_usd`. |
| `alert_sent` | boolean | `true` when threshold exceeded AND Telegram credentials (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) are configured and alert delivery succeeded. |

When `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` is absent, no alert is sent even if the threshold is exceeded (`alert_sent: false`).

### Error responses

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid API key. |

### Implementation constraints

- Daily spend is sourced from `gemini_audit_log` table (tracks Claude API calls).
- Threshold configurable via `AI_DAILY_COST_THRESHOLD` env var; default `1.00` USD.
- Telegram alert format includes: date, daily spend, request count, threshold.
- If Telegram delivery fails (network error), `alert_sent: false`; endpoint still returns 200.
- No write operations: audit log is read-only for this endpoint.

---

## POST /ai/check-endpoint-anomalies

Runs the per-endpoint cost/latency anomaly check across the 6 AI-invoking endpoints (`POST /ai/journal-summary`, `POST /ai/daily-briefing`, `POST /ai/chat`, `POST /trade-plans/generate-plan`, `POST /trade-plans/{plan_id}/generate-thesis`, `POST /trades/{trade_id}/debrief`). Sends a Telegram alert if any endpoint's cost or latency fires. Intended to be called by a daily scheduler (GitHub Actions cron — `.github/workflows/ai-endpoint-anomaly-check.yml`).

**§13 Status:** N/A — operational monitoring endpoint. No AI output generated; no display surface.

### Request

```
POST /ai/check-endpoint-anomalies
Content-Type: application/json
```

No request body required.

### Response — 200 OK

```json
{
  "checked_utc": "2026-09-14T07:00:03+00:00",
  "cost_anomalies": [
    {"endpoint": "POST /ai/chat", "metric": "cost", "is_anomaly": false, "recent_value": 0.11, "baseline_value": 0.10, "multiplier": 1.1, "reason": "within_normal_range"}
  ],
  "latency_anomalies": [],
  "firing_count": 0,
  "alert_sent": false,
  "latency_data_source": "claude_audit_log"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `checked_utc` | string | UTC timestamp the check ran, ISO 8601. |
| `cost_anomalies` | array | One entry per endpoint with `>=1` request in the combined recent+baseline window, from `check_cost_anomaly` (recent 24h avg cost vs trailing 7-day baseline avg cost, per `endpoint` tag in `claude_audit_log`). |
| `latency_anomalies` | array | Entries from `check_latency_anomaly`, sourced from `claude_audit_log.latency_ms` (recent 24h p95 vs trailing 7-day baseline p95, per endpoint — ST-13, BLG-OPS-161, v9.5). One entry per endpoint with `>=1` row carrying a non-null `latency_ms` in the combined window; rows written before this column existed (NULL) are excluded, not treated as 0ms. |
| `firing_count` | integer | Count of entries across both arrays with `is_anomaly: true`. |
| `alert_sent` | boolean | `true` when `firing_count > 0` AND Telegram credentials (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) are configured and delivery succeeded. |
| `latency_data_source` | string | `"claude_audit_log"` — real data via this endpoint (as of v9.5; a caller-supplied `simulated_latency_feed` is not part of this endpoint's public request/response shape — that parameter exists on the underlying service function for tests/dry-runs only, where it would report `"simulated_feed"`). Never silently omitted. |

### Error responses

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid API key. |

### Implementation constraints

- Cost data source: `database.get_claude_endpoint_cost_windows()` — real `claude_audit_log` data, recent 24h vs trailing 7-day baseline, per endpoint. Below `MIN_COST_BASELINE_USD` the ratio is suppressed as noise (see `services/ai_endpoint_anomaly_service.py`).
- Latency data source: `database.get_claude_endpoint_latency_windows()` — real `claude_audit_log.latency_ms` data (ST-13, BLG-OPS-161, v9.5), recent 24h p95 vs trailing 7-day baseline p95, per endpoint. Below `MIN_LATENCY_BASELINE_MS` the ratio is suppressed as noise, same as cost. `latency_ms` is populated by every `create_claude_audit_entry()` call site going forward; historical rows predating this column remain NULL and are excluded from both windows rather than counted as 0ms.
- On any firing anomaly, sends one Telegram message summarising all firing entries (not one message per entry).
- If Telegram delivery fails (network error) or credentials are absent, `alert_sent: false`; endpoint still returns 200.
- No write operations: `claude_audit_log` is read-only for this endpoint.

---

## GET /ai/claude-audit-log

Returns the most recent entries from the `claude_audit_log` table — the immutable audit trail of all Claude API calls made by the application. Intended for compliance monitoring and cost review (ST-05, ST-07).

**§13 Status:** N/A — operational audit query endpoint. Read-only; no AI output generated.

### Request

```
GET /ai/claude-audit-log?limit=50
GET /ai/claude-audit-log?endpoint=POST%20/ai/daily-briefing
GET /ai/claude-audit-log?date_from=2026-07-01&date_to=2026-07-13
GET /ai/claude-audit-log?endpoint=POST%20/ai/daily-briefing&date_from=2026-07-01&date_to=2026-07-13
```

#### Query parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | Optional | 50 | Maximum number of records to return. Range: 1–200. |
| `endpoint` | string | Optional | none | v7.0 — ST-11, BLG-BE-51. Exact-match filter on the `endpoint` field (e.g. `POST /ai/daily-briefing`). Combines with `date_from`/`date_to` (AND). |
| `date_from` | string (`YYYY-MM-DD`) | Optional | none | v7.0 — ST-11, BLG-BE-51. Inclusive lower bound applied to `generated_at`. Combines with `date_to` and `endpoint` (AND). |
| `date_to` | string (`YYYY-MM-DD`) | Optional | none | v7.0 — ST-11, BLG-BE-51. Inclusive upper bound applied to `generated_at` (records through the end of the given day). Combines with `date_from` and `endpoint` (AND). |

Omitting `endpoint`, `date_from`, and `date_to` preserves the original unfiltered behaviour (all records, most recent `limit` rows).

### Response — 200 OK

```json
{
  "ok": true,
  "data": {
    "records": [
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "endpoint": "POST /trade-plans/generate-plan",
        "model_id": "claude-haiku-4-5",
        "prompt_version": "v3.0",
        "input_tokens": 312,
        "output_tokens": 94,
        "cost_usd": 0.00078200,
        "generated_at": "2026-05-28T12:00:00+00:00"
      }
    ],
    "count": 1
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique row identifier. |
| `endpoint` | string | The API endpoint that triggered the Claude call (e.g. `POST /trade-plans/generate-plan`). |
| `model_id` | string | The Claude model ID used (e.g. `claude-haiku-4-5`). |
| `prompt_version` | string | Internal prompt version tag (e.g. `v3.0`). |
| `input_tokens` | integer or null | Prompt token count from Claude usage response. |
| `output_tokens` | integer or null | Completion token count from Claude usage response. |
| `cost_usd` | float or null | Estimated cost in USD at time of call. |
| `generated_at` | string (ISO 8601) | UTC timestamp of the Claude API call. |

Results are ordered `generated_at DESC` (newest first).

### Error responses

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid API key. |
| 422 | `limit` out of range (< 1 or > 200). |

### Implementation constraints

- Read-only endpoint: no writes to any table.
- Returns empty `records` array (not an error) when `claude_audit_log` table is empty.
- `cost_usd` may be `null` if token counts were unavailable at log time.
- No AI-generated content is returned — audit metadata only.

---

## GET /ai/journal-summary/history

**Purpose**

Query the AI journal summary audit log. Returns metadata records for past `POST /ai/journal-summary` calls — no summary text stored, only audit metadata.

**Method & Path**

- `GET /ai/journal-summary/history`

**Request**

| Query Parameter | Type | Required | Description |
|-----------------|------|----------|-------------|
| `trade_id` | integer | No | Filter records where trade_id matches |
| `date_from` | date (ISO 8601) | No | Filter by `invoked_at >= date_from` |
| `date_to` | date (ISO 8601) | No | Filter by `invoked_at <= date_to` |
| `limit` | integer (1–200) | No | Maximum records to return (default: 50) |

**Response (200)**

```json
{
  "ok": true,
  "data": {
    "records": [
      {
        "id": 1,
        "trade_id": 42,
        "invoked_at": "2026-06-01T10:00:00+00:00",
        "model": "claude-sonnet-4-6",
        "cost_usd": 0.0012
      }
    ],
    "count": 1
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `records` | array | Audit log entries, newest first |
| `count` | integer | Length of returned records array |
| `records[].id` | integer | Audit record ID |
| `records[].trade_id` | integer or null | Trade this summary was generated for |
| `records[].invoked_at` | string (ISO 8601) | UTC timestamp of the Claude API call |
| `records[].model` | string | Model identifier used |
| `records[].cost_usd` | float or null | Estimated cost in USD |

**Error responses**

| Status | Condition |
|--------|-----------|
| 422 | `limit` out of range (< 1 or > 200) |

**Backend:** `backend/routers/ai.py` (`journal_summary_history`)
**Data source:** `gemini_audit_log` table (queried via `query_audit_log`)

---

## GET /ai/monthly-cost

Returns the current calendar month's Claude API spend total, aggregated from `claude_audit_log`. Read-only — no side effects, unlike `POST /ai/check-daily-cost`, which sends a Telegram alert as a side effect and is not suitable for a page-load fetch.

Added for ST-07 (EPIC-07, v7.6, BLG-FEAT-77), reframed per `ESC-EXEC-20260720-01`: the story's original AC assumed Gemini and Claude were two separate cost-generating providers; tracing the implementation found this codebase integrates only the Anthropic Claude API (no `google-generativeai` package, no `GEMINI_API_KEY`, `gemini_service.py` calls only `anthropic`). `claude_audit_log` is the immutable audit trail and is the authoritative single-provider cost source.

**§13 Status:** N/A — read-only cost aggregate; no AI output generated.

### Request

```
GET /ai/monthly-cost
```

No parameters.

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "total_cost_usd": 0.0074,
    "request_count": 6
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total_cost_usd` | float | Sum of `cost_usd` across all `claude_audit_log` rows with `generated_at` in the current calendar month (UTC). `0.0` if no calls this month. |
| `request_count` | integer | Count of Claude API calls logged this month. |

### Error responses

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid API key. |
| 500 | Internal failure — returns `{"total_cost_usd": 0.0, "request_count": 0}` rather than propagating the error (matches `get_daily_ai_cost`'s existing fail-safe convention), so this endpoint does not return a 500 body under normal operation. |

### Implementation constraints

- Read-only endpoint: no writes to any table.
- Uses `date_trunc('month', NOW())` (UTC) as the month boundary — not user-timezone-aware.
- Does not send any alert or notification (contrast with `POST /ai/check-daily-cost`).

---

## GET /ai/monthly-cost-by-feature

Returns the current calendar month's Claude API spend, broken down by feature — extends `GET /ai/monthly-cost` (a single total) with a per-feature (`claude_audit_log.endpoint`) breakdown.

Added for ST-14 (BLG-OPS-96, EPIC-03, v9.3). Read-only, sourced from the same `claude_audit_log` table as `GET /ai/monthly-cost`, grouped by the existing `endpoint` tag column rather than a new data-collection mechanism (RISK-03 — reuses the existing logging approach; per-feature tagging already existed on every `create_claude_audit_entry()` caller before this story, this endpoint is the first to surface it as a breakdown).

**§13 Status:** N/A — read-only cost aggregate; no AI output generated.

**Feature tag taxonomy** (current `endpoint` values in use, set by each caller at the `create_claude_audit_entry()` call site — see `backend/database.py`):

| Tag | Feature | Caller |
|-----|---------|--------|
| `POST /ai/daily-briefing` | Daily briefing | `backend/services/ai_service.py` |
| `POST /ai/chat` | AI trade advisor chat | `backend/services/ai_service.py` |
| `POST /trades/{trade_id}/debrief` | Post-trade debrief | `backend/services/debrief_service.py` |
| `POST /trade-plans/generate-plan` | Trade plan generation | `backend/services/gemini_service.py` |
| `POST /trade-plans/{plan_id}/generate-thesis` | Thesis generation | `backend/services/gemini_service.py` |

### Request

```
GET /ai/monthly-cost-by-feature
```

No parameters.

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "features": [
      {"endpoint": "POST /ai/daily-briefing", "total_cost_usd": 0.0041, "request_count": 4},
      {"endpoint": "POST /trade-plans/{plan_id}/generate-thesis", "total_cost_usd": 0.0022, "request_count": 2}
    ]
  }
}
```

| Field | Type | Description |
|-------|------|--------------|
| `features` | array | One entry per distinct `endpoint` tag with at least 1 call this calendar month, ordered by `total_cost_usd` descending. Empty array if no calls this month. |
| `features[].endpoint` | string | The feature tag (see taxonomy table above). |
| `features[].total_cost_usd` | float | Sum of `cost_usd` for this tag, current calendar month (UTC). |
| `features[].request_count` | integer | Count of calls for this tag, current calendar month. |

### Error responses

| Status | Condition |
|--------|-----------|
| 500 | Internal failure — returns `{"features": []}` rather than propagating the error (matches `get_monthly_claude_cost`'s existing fail-safe convention), so this endpoint does not return a 500 body under normal operation. |

### Implementation constraints

- Read-only endpoint: no writes to any table.
- Uses `date_trunc('month', NOW())` (UTC) as the month boundary, same as `GET /ai/monthly-cost`.
- Reporting cycle: this month's data becomes available as soon as the first tagged call is logged — no backfill of pre-existing untagged rows (there are none; every `create_claude_audit_entry()` caller has always passed `endpoint`).

---

## GET /ai/spend-trend

Returns Claude API spend for the last 6 release cycles (oldest to newest), for the Settings page's AI spend trend chart (`settings.md` §6, extends the existing current-month spend card).

Added for ST-06 (EPIC-06, v7.8, BLG-FEAT-82). Sourced from existing `claude_audit_log` data (no new data collection) — bucketed by release-cycle date windows parsed from `docs/product/changelog.md`'s version headings (`## vX.Y — <title> — <date>`). This is a documented implementation choice, not the UX spec's literal first-choice suggestion of `claude/cycles/*/state.json`: that governance-tracking directory is an internal engineering-process artefact with no guarantee of being present in the deployed runtime environment, whereas `changelog.md` is product-facing, already deployed, and already carries a version label plus ship date per release — the UX spec itself allows "an equivalent cycle-boundary source."

**§13 Status:** N/A — read-only cost aggregate; no AI output generated.

### Request

```
GET /ai/spend-trend
```

No parameters.

### Response — 200 OK

```json
{
  "status": "ok",
  "data": [
    { "version": "v7.3", "spend_usd": 4.12 },
    { "version": "v7.4", "spend_usd": 2.87 },
    { "version": "v7.5", "spend_usd": 5.03 },
    { "version": "v7.6", "spend_usd": 3.91 },
    { "version": "v7.7", "spend_usd": 6.20 },
    { "version": "v7.8", "spend_usd": 1.45 }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | One entry per release cycle, oldest to newest (left-to-right chart X-axis order). Contains fewer than 6 entries if fewer release cycles exist in `changelog.md` — no zero-padding. Empty array if `changelog.md` is missing or has no parseable version headings. |
| `data[].version` | string | Bare version number of the release cycle (e.g. `"v7.8"`) — matches the changelog heading's version token. |
| `data[].spend_usd` | float | Sum of `cost_usd` from `claude_audit_log` for this cycle's date window: `[this cycle's ship date, next cycle's ship date)`, or `[this cycle's ship date, now)` for the most recent (open-ended) cycle. Rounded to 2 d.p. |

**Same-day release note:** when two consecutive releases share a ship date (a real occurrence in this changelog — e.g. v7.5 and v7.6 both shipped 2026-07-20), the changelog's own strictly-newest-first document ordering is used as a secondary sort key so the two resolve in correct chronological order despite the date tie.

### Error responses

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid API key. |
| 500 | Not expected under normal operation — internal failures in the DB aggregation step return `0.0` per cycle (matches `GET /ai/monthly-cost`'s fail-safe convention) rather than propagating an error. |

### Implementation constraints

- Read-only endpoint: no writes to any table.
- Cycle boundaries are date-only (`YYYY-MM-DD`, no time-of-day) — matches the granularity available in `changelog.md`.
- Does not send any alert or notification.

---

## GET /ai/spend-trend-by-feature

Returns Claude API spend for the last 6 release cycles (oldest to newest), broken down by feature within each cycle — combines `GET /ai/monthly-cost-by-feature`'s per-feature grouping with `GET /ai/spend-trend`'s multi-cycle window, so "is feature X's spend trending up over recent cycles" is answerable without manually cross-referencing both endpoints across cycles.

Added for ST-06 (BLG-OPS-153, EPIC-02, v9.5), sub-item 2 of 3 (storage projection and silent-purge-failure visibility are the other 2 — see `docs/ops/ai_audit_log_retention_policy.md`). Sourced from the same `claude_audit_log` data as `GET /ai/spend-trend` (no new data collection), same cycle-boundary parsing (`docs/product/changelog.md`).

**§13 Status:** N/A — read-only cost aggregate; no AI output generated.

**Alert-threshold tie-in (considered, not implemented):** `docs/ops/gemini_cost_tracking.md`'s existing $5/month alert threshold applies to current-month *total* spend, a different metric/cadence than this per-cycle, per-feature breakdown — not wired together here.

### Request

```
GET /ai/spend-trend-by-feature
```

No parameters.

### Response — 200 OK

```json
{
  "status": "ok",
  "data": [
    {
      "version": "v9.4",
      "features": [
        { "endpoint": "POST /ai/daily-briefing", "spend_usd": 2.10 },
        { "endpoint": "POST /ai/chat", "spend_usd": 1.05 }
      ]
    },
    {
      "version": "v9.5",
      "features": [
        { "endpoint": "POST /ai/daily-briefing", "spend_usd": 2.40 }
      ]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | One entry per release cycle, oldest to newest. Fewer than 6 entries if fewer cycles exist in `changelog.md` — no zero-padding. Empty array if `changelog.md` is missing or unparseable. |
| `data[].version` | string | Bare version number of the release cycle, e.g. `"v9.5"`. |
| `data[].features` | array | Per-feature spend within this cycle's date window, descending by spend. Only features with at least one `claude_audit_log` row in the window appear — no zero-filling for features with no activity that cycle. |
| `data[].features[].endpoint` | string | Feature tag (`claude_audit_log.endpoint`) — same taxonomy as `GET /ai/monthly-cost-by-feature`. |
| `data[].features[].spend_usd` | float | Sum of `cost_usd` for this feature in this cycle's window. Rounded to 2 d.p. |

### Error responses

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid API key. |
| 500 | Not expected under normal operation — internal failures in the DB aggregation step return `[]` per cycle's `features` (matches `GET /ai/spend-trend`'s fail-safe convention) rather than propagating an error. |

### Implementation constraints

- Read-only endpoint: no writes to any table.
- Same same-day-release tie handling and date-only cycle boundaries as `GET /ai/spend-trend`.
- Does not send any alert or notification.

---

## AI Output Boundary-Language Sampling Hook (ST-23, BLG-AI-06, v9.4)

Not a new endpoint — this is internal instrumentation, not part of this contract's API surface. Documented here per this story's AC (5), which requires the mechanism to be documented in the AI-endpoint contract docs.

**Purpose:** lets `scripts/run_ai_output_boundary_sample_audit.py` draw a genuine, non-illustrative sample of real AI-generated output text for §13.2 boundary-language auditing (`claude/strategy/strategy_rules.md`), rather than the hand-authored illustrative examples used for the Q3 2026 audit (`BLG-GOV-178`, `docs/ops/ai_output_boundary_sample_audit_20260910.md`).

**Mechanism:** `backend/services/ai_output_sampling_service.py::maybe_sample_output(feature, output_text, model_version)` is called immediately after every successful generation call across all 5 real call sites this contract governs plus the two trade-plan generation endpoints (`gemini_service.py`):

| Feature | Call site |
|---------|-----------|
| `POST /ai/journal-summary` | `ai_service.py::summarise_journal_notes()` |
| `POST /ai/daily-briefing` | `ai_service.py::generate_daily_briefing()` |
| `POST /ai/chat` | `ai_service.py::ai_chat()` |
| `POST /trades/{id}/debrief` (`focus_area_text` only — `summary_text` is template-built, not AI-generated) | `debrief_service.py::generate_trade_debrief()` |
| `POST /trade-plans/generate-plan` (`setup_thesis`/`entry_rationale`/`early_exit_conditions`) | `gemini_service.py::generate_full_plan()` |
| `POST /trade-plans/{plan_id}/generate-thesis` (legacy) | `gemini_service.py::generate_setup_thesis()` |

**Gating (AC 1–2):** default **off** — sampling only happens when `AI_OUTPUT_SAMPLING_ENABLED` is explicitly truthy. Even when enabled, only a bounded fraction (`AI_OUTPUT_SAMPLING_RATE`, default `0.1` = 10%, clamped to `[0, 1]`) of calls are actually written — this is not full-content logging of every response.

**Storage:** a new `ai_output_boundary_samples` table (`docs/specs/data_model.md`) stores the actual generated text — unlike `gemini_audit_log` (hashes only) or `claude_audit_log` (no prompt/response representation at all, hash or text). This is a disclosed, narrow exception to `docs/ops/claude_api_log_hygiene_policy.md`'s general text-avoidance principle — see that document's §2.4 for the exception's own governance (90-day retention, opt-in, rate-bounded).

**Consumer path (AC 3):** `scripts/run_ai_output_boundary_sample_audit.py::load_real_samples_from_store()` reads up to 10 rows and `main()` prefers them over the illustrative fallback SAMPLE whenever the store returns at least one row.

**Genuine live sample (AC 4/AC-04) and escalation closure (AC 6) — staging-only, not completed this cycle:** per `sprint_backlog.md` ST-23's own note, drawing and scanning a genuine ≥10-output sample requires production credentials (`ANTHROPIC_API_KEY`, live DB) that this execution environment does not have — the same disclosed constraint as `ESC-EXEC-20260910-01`. This mechanism is built and unit-tested (`tests/test_ai_output_sampling_service.py`, `tests/test_run_ai_output_boundary_sample_audit.py`) so it is ready the moment a staging/production session runs it; `ESC-EXEC-20260910-01` remains **Deferred**, not Resolved, until that actually happens — closing it now would misrepresent AC 4 as met when it is only mechanically capable of being met.

---

## Known Deviations

None at v1.10.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.13 | 2026-09-16 | ST-13 (EPIC-02, v9.5, BLG-OPS-161): `POST /ai/check-endpoint-anomalies` latency is now real-data — `claude_audit_log` gained a `latency_ms` column (populated by every `create_claude_audit_entry()` call site going forward), `latency_data_source` now reports `"claude_audit_log"` instead of `"not_available_pending_BLG-OPS-161"`. No `openapi.yaml` schema change (response shape unchanged, only field-value semantics). Infrastructure & Operations Owner sign-off. |
| 1.12 | 2026-09-16 | ST-06 (EPIC-02, v9.5, BLG-OPS-153): Added `GET /ai/spend-trend-by-feature` (per-feature, per-cycle spend breakdown — sub-item 2 of 3; the other 2 land in `docs/ops/ai_audit_log_retention_policy.md`). `openapi.yaml` and `backend/routers/test.py` updated in the same commit. FinOps & Resource Architect sign-off. |
| 1.11 | 2026-09-15 | ST-23 (EPIC-05, v9.4, BLG-AI-06): Documented the generation-time AI output boundary-language sampling hook (`ai_output_sampling_service.py`, opt-in via `AI_OUTPUT_SAMPLING_ENABLED`, rate-bounded via `AI_OUTPUT_SAMPLING_RATE`) — new `ai_output_boundary_samples` table, wired into all 6 real AI-generation call sites, consumed by `scripts/run_ai_output_boundary_sample_audit.py`. Not a new endpoint; no `openapi.yaml` change. Genuine live sample (AC 4) and `ESC-EXEC-20260910-01` closure (AC 6) remain staging-only — no production credentials in this session. |
| 1.10 | 2026-09-14 | ST-09 (EPIC-03, v9.4, BLG-OPS-151): Added `POST /ai/check-endpoint-anomalies` — wires the existing pure cost/latency anomaly detector (`services/ai_endpoint_anomaly_service.py`, ST-54/v9.2) into a scheduled job (`.github/workflows/ai-endpoint-anomaly-check.yml`, daily) and Telegram alert. Cost checked against real `claude_audit_log` data; latency has no real data source (`claude_audit_log` has no latency column — BLG-OPS-161 filed as the prerequisite gap) and is disclosed as pending via `latency_data_source`, not fabricated. `openapi.yaml` and `docs/ops/api_performance_baseline.md` §44 updated in the same commit. |
| 1.9 | 2026-09-10 | ST-14 (EPIC-03, v9.3, BLG-OPS-96): Added `GET /ai/monthly-cost-by-feature` — current calendar month's Claude API spend broken down by the existing `claude_audit_log.endpoint` feature tag (5 tags documented in the endpoint section's taxonomy table). Reuses existing tagging, no new data collection. `openapi.yaml` updated in the same commit. |
| 1.8 | 2026-07-27 | ST-06 (EPIC-06, v7.8, BLG-FEAT-82): Added `GET /ai/spend-trend` — Claude API spend for the last 6 release cycles, bucketed by date windows parsed from `docs/product/changelog.md` version headings (documented alternative to the UX spec's `claude/cycles/*/state.json` suggestion — see endpoint section for rationale). `openapi.yaml` updated in the same commit. |
| 1.7 | 2026-07-20 | ST-07 (EPIC-07, v7.6, BLG-FEAT-77): Added `GET /ai/monthly-cost` — current calendar month's Claude API spend total, sourced from `claude_audit_log`. Reframed per `ESC-EXEC-20260720-01`: original AC assumed a separate Gemini provider; no such integration exists in this codebase (confirmed: no `google-generativeai`, no `GEMINI_API_KEY`, `gemini_service.py` calls only the Anthropic API). `openapi.yaml` updated in the same commit. |
| 1.6 | 2026-07-13 | v7.0 EPIC-02 ST-11 (BLG-BE-51): Added optional `endpoint` (exact match) and `date_from`/`date_to` (inclusive, `YYYY-MM-DD`, applied to `generated_at`) query filters to `GET /ai/claude-audit-log` — independently or combined, and combinable with `limit`. No new endpoint; existing unfiltered behaviour unchanged when all three are omitted. `openapi.yaml` updated in the same commit. |
| 1.5 | 2026-06-29 | v6.3 EPIC-01 ST-03: Added per-endpoint rate limiting to `POST /ai/daily-briefing` (10 req/min/IP) and `POST /ai/chat` (30 req/min/IP). 429 + `Retry-After` documented. In-memory sliding-window implementation (`backend/services/rate_limiter.py`). AC-05: rate limit scenario tests added to `backend/routers/test.py`. |
| 1.4 | 2026-06-25 | v6.2 EPIC-02 ST-06/ST-08: Added `POST /ai/daily-briefing` (daily portfolio briefing + action list) and `POST /ai/chat` (stateless conversational advisor). Both endpoints use `claude-sonnet-4-6`, log to `claude_audit_log`, return `advisory: true`. §13 PASS per 2026-06-24 review. Head of Engineering sign-off. |
| 1.3 | 2026-06-09 | v5.3 ST-04 (BLG-SPEC-49, EPIC-01): Added `GET /ai/journal-summary/history` — AI journal summary audit log query endpoint. API Contracts & Documentation Owner sign-off. |
| 1.2 | 2026-05-28 | ST-07 (EPIC-03, v4.2): Added `GET /ai/claude-audit-log` — immutable Claude API audit trail query endpoint (BLG-GOV-63). |
| 1.1 | 2026-05-27 | ST-09 (EPIC-03, v4.1): Added `POST /ai/check-daily-cost` — Claude API daily cost threshold alert endpoint (BLG-OPS-34). |
| 1.0 | 2026-04-18 | ST-07 (EPIC-04, v2.8): Initial specification for `POST /ai/journal-summary`. Conditionally compliant per SRB-v1.7. API Contracts & Documentation Owner. |
