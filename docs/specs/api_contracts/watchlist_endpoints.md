**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-07-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint:** 2026-06-08__release-v5.3 — ST-07 (BLG-SPEC-52, EPIC-01)
**Signed off by:** API Contracts & Documentation Owner; Head of Specs Team

---

# Watchlist Endpoints

## Scope

Pre-position ticker monitoring. Watchlist entries track tickers the trader is monitoring before entering a position, with optional price targets.

---

## GET /watchlist

**Purpose**

List all watchlist entries for the portfolio, with computed `signal_status` (whether the ticker is currently on the signals list).

**Method & Path**

- `GET /watchlist`

**Request**

No parameters.

**Response (200)**

```json
{
  "status": "ok",
  "data": [
    {
      "id": "wl-001",
      "portfolio_id": "port-001",
      "ticker": "NVDA",
      "market": "US",
      "target_entry_price": 450.0,
      "initial_stop_price": 420.0,
      "current_stop_price": 435.0,
      "signal_status": "active",
      "created_at": "2026-06-01T10:00:00Z"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | Watchlist entries. Empty array if none. |
| `data[].id` | string (UUID) | Entry identifier |
| `data[].portfolio_id` | string | Portfolio this entry belongs to |
| `data[].ticker` | string | Ticker symbol |
| `data[].market` | string | `US` or `UK` |
| `data[].target_entry_price` | float or null | Target entry price (optional) |
| `data[].initial_stop_price` | float or null | Initial stop loss price (optional) |
| `data[].current_stop_price` | float or null | Current (trailed) stop price (optional) |
| `data[].signal_status` | string or null | Signal list status for this ticker (`active`, `watchlisted`, or `null`) |
| `data[].tags` | array of string | Watchlist tags (v1.1, ST-03/BLG-FE-117) — populated only via `POST /watchlist/bulk-tag`; empty array if none |
| `data[].created_at` | string (ISO 8601) | Entry creation timestamp |

---

## POST /watchlist

**Purpose**

Add a ticker to the watchlist. Returns 409 if the ticker already exists in the portfolio's watchlist.

**Method & Path**

- `POST /watchlist`

**Request Body**

```json
{
  "ticker": "NVDA",
  "market": "US",
  "target_entry_price": 450.0,
  "initial_stop_price": 420.0,
  "current_stop_price": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | Yes | Ticker symbol |
| `market` | string | Yes | `US` or `UK` |
| `target_entry_price` | float | No | Target entry price |
| `initial_stop_price` | float | No | Initial stop loss price |
| `current_stop_price` | float | No | Current trailing stop price |

**Response (201)**

```json
{
  "status": "ok",
  "data": {
    "id": "wl-002",
    "portfolio_id": "port-001",
    "ticker": "NVDA",
    "market": "US",
    "target_entry_price": 450.0,
    "initial_stop_price": 420.0,
    "current_stop_price": null,
    "signal_status": null,
    "created_at": "2026-06-09T00:00:00Z"
  }
}
```

**Error responses**

| Status | Condition |
|--------|-----------|
| 400 | Invalid request body |
| 409 | Ticker already exists in watchlist for this portfolio |
| 500 | Database error |

---

## DELETE /watchlist/{entry_id}

**Purpose**

Remove a watchlist entry by ID. Not idempotent — a second call returns 404.

**Method & Path**

- `DELETE /watchlist/{entry_id}`

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `entry_id` | string (UUID) | Yes | Watchlist entry ID to delete |

**Response (200)**

```json
{
  "status": "ok",
  "data": {
    "deleted": true,
    "entry_id": "wl-001"
  }
}
```

**Error responses**

| Status | Condition |
|--------|-----------|
| 404 | Entry not found or does not belong to this portfolio |
| 500 | Database error |

---

## GET /watchlist/tags

**Purpose**

Return unique tags across all watchlist entries, for the Bulk Tag autocomplete (v1.1, ST-03/BLG-FE-117). Mirrors `GET /trade-plans/tags`.

**Method & Path**

- `GET /watchlist/tags`

**Response (200)**

```json
{
  "status": "ok",
  "data": ["breakout", "momentum"]
}
```

**Error responses**

| Status | Condition |
|--------|-----------|
| 500 | Database error |

---

## POST /watchlist/bulk-tag

**Purpose**

Add tags to each selected watchlist entry's existing tag set (union, not replace). New in v1.1 (ST-03, BLG-FE-117, EPIC-03, v7.5) — see `docs/specs/blg_fe_117_pre_implementation_readiness_pass.md` AC-01 for the batch-mutation pattern.

**Method & Path**

- `POST /watchlist/bulk-tag`

**Request Body**

```json
{
  "ids": ["wl-001", "wl-002"],
  "tags": ["momentum", "breakout"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ids` | array of string (UUID) | Yes | Watchlist entry IDs to tag. Max 100 per call. |
| `tags` | array of string | Yes | Tags to add — lowercase, alphanumeric+hyphen, max 20 chars, max 10 tags per entry (same rules as `trade_plans.trade_tags`). Invalid tags are silently filtered, not rejected. |

**Response (200)**

```json
{
  "status": "ok",
  "data": {
    "succeeded": ["wl-001", "wl-002"],
    "failed": []
  }
}
```

On partial failure, `failed` contains `{id, reason}` objects (e.g. `reason: "not_found"`) — never a single opaque error for the whole batch.

**Error responses**

| Status | Condition |
|--------|-----------|
| 400 | `ids` empty or exceeds the 100-item cap |
| 500 | Database error |

---

## DELETE /watchlist/bulk

**Purpose**

Remove each selected watchlist entry in a single call. New in v1.1 (ST-03, BLG-FE-117, EPIC-03, v7.5).

**Method & Path**

- `DELETE /watchlist/bulk`

**Request Body**

```json
{ "ids": ["wl-001", "wl-002"] }
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ids` | array of string (UUID) | Yes | Watchlist entry IDs to remove. Max 100 per call. |

**Response (200)**

```json
{
  "status": "ok",
  "data": {
    "succeeded": ["wl-001", "wl-002"],
    "failed": []
  }
}
```

**Error responses**

| Status | Condition |
|--------|-----------|
| 400 | `ids` empty or exceeds the 100-item cap |
| 500 | Database error |

---

## PATCH /watchlist/{entry_id}

**Purpose**

Update price fields on an existing watchlist entry. `ticker` and `market` are read-only after creation.

**Method & Path**

- `PATCH /watchlist/{entry_id}`

**Request Body** (all fields optional)

```json
{
  "target_entry_price": 460.0,
  "initial_stop_price": 425.0,
  "current_stop_price": 440.0
}
```

**Response (200)**

```json
{
  "status": "ok",
  "data": { "<updated entry object>" }
}
```

**Error responses**

| Status | Condition |
|--------|-----------|
| 400 | Invalid field values |
| 404 | Entry not found |
| 500 | Database error |

---

## Backend

`backend/routers/watchlist.py`

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-07-17 | ST-03 (BLG-FE-117, EPIC-03, v7.5): Added `## GET /watchlist/tags`, `## POST /watchlist/bulk-tag`, `## DELETE /watchlist/bulk`. New `tags` column on `watchlist` (data_model.md v2.12→v2.13), populated only via bulk-tag. `GET /watchlist` response schema updated with `data[].tags`. Router ordering note: bulk routes declared before `PATCH/DELETE /watchlist/{entry_id}` to avoid wildcard capture. |
| 1.0 | 2026-06-09 | v5.3 ST-07 (BLG-SPEC-52, EPIC-01): Initial contract for GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id}, PATCH /watchlist/{entry_id}. Endpoints shipped in prior cycle; contract gap resolved. test.py entries added for GET, POST, DELETE. API Contracts & Documentation Owner and Head of Specs Team sign-off. |
