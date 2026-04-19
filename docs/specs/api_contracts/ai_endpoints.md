**Owner:** API Contracts & Documentation Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-04-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Endpoints — API Contract

This document specifies AI-powered endpoints for the Momentum Trading Assistant.

All AI output is **display-only** and must NOT be used as input to any signal, scoring, compliance, or recommendation calculation. This constraint is mandated by SRB-v1.7 (2026-03-02) and is a hard architectural rule.

---

## Table of Contents

- [POST /ai/journal-summary](#post-aijournal-summary)

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

## Known Deviations

None at v1.0.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-18 | ST-07 (EPIC-04, v2.8): Initial specification for `POST /ai/journal-summary`. Conditionally compliant per SRB-v1.7. API Contracts & Documentation Owner. |
