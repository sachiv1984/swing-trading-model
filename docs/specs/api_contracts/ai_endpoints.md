**Owner:** API Contracts & Documentation Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.2
**Last Updated:** 2026-05-28
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Endpoints — API Contract

This document specifies AI-powered endpoints for the Momentum Trading Assistant.

All AI output is **display-only** and must NOT be used as input to any signal, scoring, compliance, or recommendation calculation. This constraint is mandated by SRB-v1.7 (2026-03-02) and is a hard architectural rule.

---

## Table of Contents

- [POST /ai/journal-summary](#post-aijournal-summary)
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

## Known Deviations

None at v1.2.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.2 | 2026-05-28 | ST-07 (EPIC-03, v4.2): Added `GET /ai/claude-audit-log` — immutable Claude API audit trail query endpoint (BLG-GOV-63). |
| 1.1 | 2026-05-27 | ST-09 (EPIC-03, v4.1): Added `POST /ai/check-daily-cost` — Claude API daily cost threshold alert endpoint (BLG-OPS-34). |
| 1.0 | 2026-04-18 | ST-07 (EPIC-04, v2.8): Initial specification for `POST /ai/journal-summary`. Conditionally compliant per SRB-v1.7. API Contracts & Documentation Owner. |
