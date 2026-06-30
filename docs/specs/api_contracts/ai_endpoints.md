**Owner:** API Contracts & Documentation Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.5
**Last Updated:** 2026-06-29
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
- [GET /ai/claude-audit-log](#get-aiclaude-audit-log)

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
  "detail": "Rate limit exceeded. Try again later."
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
  "detail": "Rate limit exceeded. Try again later."
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

## GET /ai/claude-audit-log

Returns the most recent entries from the `claude_audit_log` table — the immutable audit trail of all Claude API calls made by the application. Intended for compliance monitoring and cost review (ST-05, ST-07).

**§13 Status:** N/A — operational audit query endpoint. Read-only; no AI output generated.

### Request

```
GET /ai/claude-audit-log?limit=50
```

#### Query parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | Optional | 50 | Maximum number of records to return. Range: 1–200. |

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

## Known Deviations

None at v1.5.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.5 | 2026-06-29 | v6.3 EPIC-01 ST-03: Added per-endpoint rate limiting to `POST /ai/daily-briefing` (10 req/min/IP) and `POST /ai/chat` (30 req/min/IP). 429 + `Retry-After` documented. In-memory sliding-window implementation (`backend/services/rate_limiter.py`). AC-05: rate limit scenario tests added to `backend/routers/test.py`. |
| 1.4 | 2026-06-25 | v6.2 EPIC-02 ST-06/ST-08: Added `POST /ai/daily-briefing` (daily portfolio briefing + action list) and `POST /ai/chat` (stateless conversational advisor). Both endpoints use `claude-sonnet-4-6`, log to `claude_audit_log`, return `advisory: true`. §13 PASS per 2026-06-24 review. Head of Engineering sign-off. |
| 1.3 | 2026-06-09 | v5.3 ST-04 (BLG-SPEC-49, EPIC-01): Added `GET /ai/journal-summary/history` — AI journal summary audit log query endpoint. API Contracts & Documentation Owner sign-off. |
| 1.2 | 2026-05-28 | ST-07 (EPIC-03, v4.2): Added `GET /ai/claude-audit-log` — immutable Claude API audit trail query endpoint (BLG-GOV-63). |
| 1.1 | 2026-05-27 | ST-09 (EPIC-03, v4.1): Added `POST /ai/check-daily-cost` — Claude API daily cost threshold alert endpoint (BLG-OPS-34). |
| 1.0 | 2026-04-18 | ST-07 (EPIC-04, v2.8): Initial specification for `POST /ai/journal-summary`. Conditionally compliant per SRB-v1.7. API Contracts & Documentation Owner. |
