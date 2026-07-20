**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-07-20
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint:** 2026-07-17__release-v7.5 — ST-04 (BLG-FE-118, EPIC-04)
**Signed off by:** API Contracts & Documentation Owner; Head of Specs Team

---

# Saved Filters Endpoints

## Scope

Named, server-side Trade History filter presets (ST-04, BLG-FE-118, EPIC-04, v7.5). A user may create an arbitrary number of presets; each is a named snapshot of a filter selection, reapplied on demand. Distinct from the page's ephemeral, device-local active-filter state (BLG-FE-40 localStorage-envelope pattern) — these rows persist server-side across devices/sessions until explicitly deleted.

**Design source:** `docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md`
**Depends on:** `docs/specs/blg_fe_118_pre_implementation_readiness_pass.md` (`saved_filters` schema, AC-01)
**Data model reference:** `docs/specs/data_model.md §Saved Filters Table`

---

## GET /saved-filters

**Purpose**

List all saved filter presets for the portfolio.

**Method & Path**

- `GET /saved-filters`

**Request**

No parameters.

**Response (200)**

```json
{
  "status": "ok",
  "data": [
    {
      "id": "sf-001",
      "name": "My Winners",
      "filter_state": { "result": "win", "market": "all", "dateFrom": "", "dateTo": "", "tags": [] },
      "created_at": "2026-07-20T10:00:00Z",
      "updated_at": "2026-07-20T10:00:00Z"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | Saved filter presets. Empty array if none. |
| `data[].id` | string (UUID) | Preset identifier |
| `data[].name` | string | Preset name |
| `data[].filter_state` | object | Serialised filter selection — shape owned by the frontend, opaque to the backend |
| `data[].created_at` | string (ISO 8601) | Preset creation timestamp |
| `data[].updated_at` | string (ISO 8601) | Last update timestamp |

**Error responses**

| Status | Condition |
|--------|-----------|
| 500 | Database error |

---

## POST /saved-filters

**Purpose**

Create a named filter preset. Returns 400 if a preset with the same name already exists for this portfolio.

**Method & Path**

- `POST /saved-filters`

**Request Body**

```json
{
  "name": "My Winners",
  "filter_state": { "result": "win", "market": "all", "dateFrom": "", "dateTo": "", "tags": [] }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Preset name, max 100 chars |
| `filter_state` | object | Yes | Current filter selection, opaque to the backend |

**Response (200)**

```json
{
  "status": "ok",
  "data": {
    "id": "sf-001",
    "name": "My Winners",
    "filter_state": { "result": "win", "market": "all", "dateFrom": "", "dateTo": "", "tags": [] },
    "created_at": "2026-07-20T10:00:00Z",
    "updated_at": "2026-07-20T10:00:00Z"
  }
}
```

**Error responses**

| Status | Condition |
|--------|-----------|
| 400 | `name` missing, exceeds 100 chars, or already exists for this portfolio (`"A preset named '{name}' already exists."`) |
| 400 | `filter_state` missing or not an object |
| 500 | Database error |

---

## DELETE /saved-filters/{id}

**Purpose**

Delete a saved filter preset. Does not affect the currently-active filter selection on the page.

**Method & Path**

- `DELETE /saved-filters/{id}`

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string (UUID) | Yes | Saved filter preset ID |

**Response (200)**

Uses the standard DELETE envelope from **conventions.md §12**:

```json
{
  "status": "ok",
  "data": {
    "deleted": true,
    "id": "sf-001"
  }
}
```

**Error responses**

| Status | Condition |
|--------|-----------|
| 404 | Preset not found |
| 500 | Database error |

---

## Backend

`backend/routers/saved_filters.py`

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | ST-04 (v7.5, EPIC-04, BLG-FE-118): Initial contract for GET/POST /saved-filters, DELETE /saved-filters/{id}. API Contracts & Documentation Owner and Head of Specs Team sign-off. |
