**Owner:** Head of Specs Team
**Class:** Specification (Class 2)
**Status:** Active
**Version:** 0.3
**Last Updated:** 2026-05-24
**Cycle:** 2026-04-29__release-v3.1 (ST-01); 2026-05-22__release-v4.0 (ST-12)

---

# Trade Plan API Contract

## Purpose

Documents the Trade Plan CRUD endpoints. Trade Plans capture pre-trade reasoning: setup thesis, entry rationale, regime context, R-target, and a structured checklist. They may be linked to a position after entry or created before entry.

**Data model reference:** `docs/specs/data_model.md §DS-04`

---

## Endpoints

## POST /trade-plans

Create a new trade plan.

### Request Body

```json
{
  "ticker": "AAPL",
  "market": "US",
  "position_id": null,
  "setup_type": "Momentum Continuation",
  "setup_thesis": "Strong momentum breakout above 52-week high with volume confirmation",
  "entry_rationale": "Price holding above 200 SMA; ATR expanding; regime Risk On",
  "regime_context_at_entry": "risk_on",
  "r_target": 2.5,
  "early_exit_conditions": "Close below 200 SMA; regime flips Risk Off",
  "confirmation_criteria": "Volume > 1.5x avg on breakout candle; RSI not overbought",
  "checklist_completed": false,
  "checklist_items": [
    {"item": "Regime check", "checked": true},
    {"item": "ATR > 1%", "checked": false}
  ],
  "status": "draft"
}
```

### Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ticker | string | Yes | Ticker symbol |
| market | string | Yes | `US` or `UK` |
| position_id | string (UUID) | No | Link to an existing position |
| setup_type | string | No | Setup classification: `Breakout` \| `Pullback to MA` \| `Momentum Continuation` \| `Mean Reversion` \| `Catalyst-driven` \| `Other`. Nullable. |
| setup_thesis | string | No | High-level setup thesis |
| entry_rationale | string | No | Specific entry rationale |
| regime_context_at_entry | string | No | Regime at plan creation |
| r_target | number | No | Target R-multiple |
| early_exit_conditions | string | No | Conditions for early exit |
| confirmation_criteria | string | No | Entry confirmation criteria |
| checklist_completed | boolean | No | Default: false |
| checklist_items | array | No | `[{item: string, checked: boolean}]` |
| status | string | No | `draft` \| `active` \| `closed` — default: `draft` |
| pre_entry_override_acknowledged | boolean | No | Whether user acknowledged pre-entry advisory warnings. Default: false. |

### Response (201 Created)

```json
{
  "status": "ok",
  "data": {
    "id": "uuid",
    "ticker": "AAPL",
    "market": "US",
    "position_id": null,
    "created_at": "2026-04-30T10:00:00Z",
    "updated_at": "2026-04-30T10:00:00Z",
    "setup_type": "Momentum Continuation",
    "setup_thesis": "...",
    "entry_rationale": "...",
    "regime_context_at_entry": "risk_on",
    "r_target": 2.5,
    "early_exit_conditions": "...",
    "confirmation_criteria": "...",
    "checklist_completed": false,
    "checklist_items": [],
    "status": "draft"
  }
}
```

---

## GET /trade-plans

List all trade plans for the portfolio, optionally filtered by status.

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| status | string | (all) | Filter by `draft`, `active`, or `closed` |

### Response (200 OK)

```json
{
  "status": "ok",
  "data": [ /* array of trade plan objects */ ]
}
```

---

## GET /trade-plans/{id}

Retrieve a single trade plan by ID.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| id | UUID | Trade plan ID |

### Response (200 OK)

```json
{
  "status": "ok",
  "data": { /* trade plan object */ }
}
```

**404:** Trade plan not found.

---

## PUT /trade-plans/{id}

Update an existing trade plan. All fields are optional; only provided fields are updated.

### Request Body

Same fields as POST (all optional for PUT), including `pre_entry_override_acknowledged`.

### Response (200 OK)

```json
{
  "status": "ok",
  "data": { /* updated trade plan object */ }
}
```

---

## DELETE /trade-plans/{id}

Delete a trade plan.

### Response (200 OK)

```json
{
  "status": "ok",
  "message": "Trade plan deleted"
}
```

---

## GET /trade-plans/by-position/{position_id}

Retrieve the trade plan(s) linked to a specific position.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| position_id | UUID | Position ID |

### Response (200 OK)

```json
{
  "status": "ok",
  "data": [ /* array of trade plan objects, typically 0 or 1 */ ]
}
```

## POST /trade-plans/{plan_id}/generate-thesis

Generate a setup thesis for an existing trade plan using Gemini Flash.

Returns a generated thesis when `GEMINI_API_KEY` is configured. Returns a graceful error payload (HTTP 200 with `available: false`) when the key is absent or the API call fails.

**Authentication:** Standard API key authentication.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| plan_id | UUID | Trade plan ID |

### Response (HTTP 200 — key configured, generation successful)

```json
{
  "status": "ok",
  "data": {
    "thesis": "Strong momentum breakout above 52-week high with volume confirmation...",
    "model_version": "gemini-1.5-flash",
    "prompt_version": "v1.0",
    "input_hash": "a3f2c1d4e5b6...",
    "output_hash": "9f8e7d6c5b4a...",
    "available": true
  }
}
```

### Response (HTTP 200 — key absent or API error)

```json
{
  "status": "ok",
  "data": {
    "available": false,
    "error": "GEMINI_API_KEY not configured"
  }
}
```

### Error Responses

| HTTP status | Description |
|------------|-------------|
| 404 | Trade plan not found |

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 0.3 | 2026-05-24 | ST-12 (BLG-BE-19, v4.0 EPIC-03): Add POST /trade-plans/{plan_id}/generate-thesis — Gemini Flash thesis generation |
| 0.2 | 2026-05-20 | Add pre_entry_override_acknowledged to POST/PUT schemas — ST-03 EPIC-01 v3.8 |
| 0.1 | 2026-04-30 | Initial contract — ST-01 EPIC-01 v3.1 |

---

## Sign-off

- Data Model Domain & Schema Owner: Accepted — 2026-04-30
- Head of Specs Team: Accepted — 2026-04-30
