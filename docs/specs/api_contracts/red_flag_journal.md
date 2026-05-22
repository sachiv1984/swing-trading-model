# red_flag_journal.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0.0
**Last Updated:** 2026-05-22
**Shipped:** v3.9 — ST-07, EPIC-03, cycle 2026-05-21__release-v3.9
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines the **Red Flag Journal** endpoint — the Arc 5 Strategy Integrity audit log for strategy deviation events (SI-03).

The Red Flag Journal is a display-only audit log. It records instances where the operator acknowledged a pre-entry validation override, dismissed a strategy checklist, or dismissed a stop/drawdown prompt. No automated decisions are derived from journal entries.

**§13 compliance:** This endpoint is display-only. It does not produce recommendations, trigger alerts, or gate any action. Its sole purpose is retrospective review of operator overrides.

**Decision record:** `docs/product/decisions/` (SI-03 §13 review, v3.9)

**Backend implementation:** `backend/routers/red_flag_journal.py`

Global response envelopes, error shape, and defaults are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /portfolio/red-flag-journal](#get-portfoliored-flag-journal)

---

## GET /portfolio/red-flag-journal

**Purpose**

Returns a paginated log of strategy deviation events. Events are written when the operator:
- Acknowledges a pre-entry validation override (rule status `fail` or `warn`) via the SI-01 advisory panel
- Dismisses a strategy checklist prompt (`checklist_skipped`)
- Dismisses a stop loss prompt (`stop_prompt_dismissed`)
- Dismisses a drawdown prompt (`drawdown_prompt_dismissed`)

**Method & Path**

- `GET /portfolio/red-flag-journal`

**Idempotency**

- Safe and idempotent. Read-only. Each call returns the current state of the journal filtered by the supplied parameters.

### Request

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number (min: 1) |
| page_size | integer | No | 20 | Items per page (min: 1, max: 100) |
| event_type | string | No | — | Filter by event type. See Event Types. |
| ticker | string | No | — | Filter by ticker symbol (case-insensitive) |
| since | string | No | — | ISO 8601 date/datetime — return events created on or after this value |

#### Event Types

| Value | Trigger |
|-------|---------|
| `pre_entry_override` | Operator acknowledged a `fail` or `warn` result from the SI-01 pre-entry validation panel |
| `checklist_skipped` | Operator dismissed a strategy checklist prompt without completing it |
| `stop_prompt_dismissed` | Operator dismissed a stop loss advisory prompt |
| `drawdown_prompt_dismissed` | Operator dismissed a drawdown advisory prompt |

### Response (200 OK)

```json
{
  "status": "ok",
  "data": {
    "total": 12,
    "page": 1,
    "page_size": 20,
    "items": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "event_type": "pre_entry_override",
        "ticker": "AAPL",
        "position_id": null,
        "context": { "source": "trade_plan", "override_acknowledged": true },
        "created_at": "2026-05-22T10:30:00+00:00"
      }
    ]
  }
}
```

### Response Fields — `data`

| Field | Type | Description |
|-------|------|-------------|
| total | integer | Total matching events across all pages |
| page | integer | Current page number |
| page_size | integer | Number of items per page |
| items | array | Array of event records (see below) |

### Response Fields — `items[]`

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID string | No | Unique event ID |
| event_type | string | No | Event type — see Event Types table |
| ticker | string | No | Ticker symbol (stored and returned uppercase) |
| position_id | UUID string | Yes | Linked open position ID at time of event, if available |
| context | object | Yes | JSON snapshot of relevant context at event time (varies by event_type) |
| created_at | ISO 8601 string | No | Event timestamp with timezone offset |

#### `context` field structure by event type

The `context` field is a free-form JSONB object. Common fields by event type:

| event_type | Typical context fields |
|------------|----------------------|
| `pre_entry_override` | `source` (e.g. `"trade_plan"`), `override_acknowledged: true` |
| `checklist_skipped` | `source`, `checklist_id` (if available) |
| `stop_prompt_dismissed` | `source`, `position_id` |
| `drawdown_prompt_dismissed` | `source`, `drawdown_pct` (if available) |

Context is informational; callers must not depend on specific context fields for logic.

### Errors

| Code | Condition |
|------|-----------|
| 500 | Database error — detail string provided in response body |

### Notes

- Events are returned in reverse chronological order (`created_at DESC`).
- An empty `items` array is a valid response when no events match the filter.
- `position_id` may be null when the event was not associated with an open position (e.g. pre-entry override before position entry).
- The `since` filter is inclusive — events with `created_at == since` are included.
- Ticker filtering is case-insensitive — `aapl` and `AAPL` return the same results.

### Write Path (Internal)

The `create_red_flag_event` function in `backend/database.py` is the only authorised write path. It is invoked by SI-01 (pre-entry override acknowledgement) and any strategy prompt dismissal handlers. This endpoint has no write surface; it is GET-only.

---

## Data Model

The Red Flag Journal is backed by the `red_flag_events` table:

```sql
CREATE TABLE red_flag_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL,
    ticker TEXT NOT NULL,
    position_id UUID,
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

Indexes: `event_type`, `UPPER(ticker)`, `created_at DESC`.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-05-22 | Initial contract authored — spec debt closure for SI-03 (shipped v3.9). Content extracted from portfolio_endpoints.md §GET /portfolio/red-flag-journal and expanded with data model, context field notes, and write path documentation. BLG-SPEC-33. Authority: API Contracts & Documentation Owner (OA-02, 2026-05-22__scheduled). |
