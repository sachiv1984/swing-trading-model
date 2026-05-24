**Owner:** Head of Security / PMO Lead
**Class:** Security Review (Class 3)
**Status:** Complete
**Review Date:** 2026-05-24
**Reviewed By:** Sprint Execution Engine (ST-06, EPIC-02, v4.0)
**Endpoint:** `GET /portfolio/red-flag-journal`

# Security Review — GET /portfolio/red-flag-journal

## Scope

ST-06 (BLG-GOV-37, v4.0 EPIC-02): API key authentication check and PII review of the Red Flag Journal endpoint.

---

## 1. Authentication

**Finding: PASS**

The application applies `api_key_middleware` globally (registered in `backend/main.py:151`). All requests to `GET /portfolio/red-flag-journal` are subject to this middleware before the handler runs.

Middleware behaviour:
- If `API_KEY` env var is unset → all requests pass (local dev mode, acceptable).
- If `API_KEY` is set → requests must supply `X-API-Key: <key>` header; any missing or incorrect key returns `401 Unauthorized`.
- `GET /health` and `OPTIONS` are the only exempted paths. `/portfolio/red-flag-journal` is not exempted.

No per-route auth dependency is needed; the middleware covers this endpoint correctly.

**No action required.**

---

## 2. PII Review

**Finding: PASS with advisory note**

Data stored in `red_flag_events` table:

| Field | Type | PII Classification |
|---|---|---|
| `id` | UUID | No — internal identifier |
| `event_type` | TEXT | No — event category string |
| `ticker` | TEXT | No — stock ticker symbol |
| `position_id` | UUID | No — internal position reference |
| `context` | JSONB | See below |
| `created_at` | TIMESTAMP WITH TIME ZONE | No — event timestamp |

**`context` JSONB field:** The context payload is caller-controlled. Current callers:
- `backend/routers/trade_plans.py` sets `context = {"source": "trade_plan", "override_acknowledged": True}` — no PII.
- Future callers must not write user-identifiable data (email, name, IP, user ID) into the context field.

**Advisory:** No user identity column exists in the schema. The application is single-user (personal trading tool with API key auth), so there is no multi-user PII risk. No names, emails, or IP addresses are stored.

**No immediate action required.** Advisory filed as governance note: future callers adding to `red_flag_events.context` must be reviewed to ensure no PII fields are introduced.

---

## 3. Data Exposure via Query Parameters

**Finding: PASS**

Query parameters accepted: `page`, `page_size`, `event_type`, `ticker`, `since`.

These are passed to `get_red_flag_events()` in `database.py:1270`. Parameterised queries (`%s` placeholders) are used throughout — no SQL injection risk.

`ticker` parameter is uppercased in the database function. No raw string interpolation into SQL.

---

## 4. Response Leakage

**Finding: PASS**

The `_serialize_event` function in `red_flag_journal.py:13` converts datetime objects to ISO strings and UUIDs to strings. It does not filter fields — all table columns are returned.

This is acceptable: no sensitive columns exist in the schema.

---

## 5. Rate Limiting / Abuse

**Finding: Advisory**

No rate limiting is applied to this endpoint. The `page_size` parameter is capped at 100 per request (FastAPI `le=100` constraint). Sustained high-frequency polling is not a material risk for a single-user personal trading tool.

Advisory: if the application ever moves to multi-user, rate limiting should be applied to all `/portfolio/**` endpoints.

---

## Summary

| Check | Result |
|---|---|
| API key authentication | PASS — global middleware covers endpoint |
| PII in stored data | PASS — no user-identifiable data in current schema |
| SQL injection | PASS — parameterised queries throughout |
| Response field leakage | PASS — no sensitive columns exposed |
| Rate limiting | Advisory — not required for single-user deployment |

**Overall: PASS. No blocking findings. No code changes required for this endpoint.**

---

*Filed per ST-06 (BLG-GOV-37) acceptance criteria. Findings documented here as authoritative security review record.*
