**Owner:** Head of Specs Team
**Class:** Specification (Class 2)
**Status:** Active
**Version:** 0.11
**Last Updated:** 2026-08-12 (ST-01/ST-03, EPIC-01, v8.7 — add invalidation_condition, is_ai_draft to POST/PUT /trade-plans request schema); prior — 2026-08-12 (ST-03, EPIC-02, v8.6, BLG-BE-91 — PUT /trade-plans/{id} status='active' now requires a position_id; new Errors section); prior — 2026-08-07 (ST-12, EPIC-03, v8.4, BLG-BE-70 — added thesis_model_version/thesis_prompt_version)
**Cycle:** 2026-04-29__release-v3.1 (ST-01); 2026-05-22__release-v4.0 (ST-12); 2026-07-08__release-v6.8 (ST-05); 2026-07-17__release-v7.5 (ST-03); 2026-07-21__release-v7.7 (ST-07); 2026-08-12__release-v8.7 (ST-01/ST-03)

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
| trade_tags | array of string | No | *(v0.6 — ST-05)* Data-independent tag field on `trade_plans`. Lowercase, alphanumeric+hyphen, max 20 chars per tag, max 10 tags. Invalid entries silently dropped server-side. Default: `[]`. |
| thesis_model_version | string | No | *(v0.9 — ST-12, BLG-BE-70)* AI compliance/audit provenance field. Frontend-passed and persisted without validation — set only when `setup_thesis`/`entry_rationale`/etc. were saved as-received from a prior `POST /trade-plans/generate-plan` or `POST /trade-plans/{id}/generate-thesis` response (see that response's `model_version` field), not user-edited before save. Null when the plan's narrative fields were typed manually. Nullable. No backfill of existing rows. |
| thesis_prompt_version | string | No | *(v0.9 — ST-12, BLG-BE-70)* Companion to `thesis_model_version` — the generate-plan/generate-thesis response's `prompt_version` field, saved the same way. Nullable. |
| invalidation_condition | string | No | *(v0.11 — ST-01, EPIC-01, v8.7, BLG-FEAT-84)* Optional, manually authored "what would prove this thesis wrong?" field. `trade_plan.md` §5.1. Nullable. |
| is_ai_draft | boolean | No | *(v0.11 — ST-03, EPIC-01, v8.7, BLG-BE-95)* AI-origin flag — true when a narrative field was populated via "Improve with AI" and not yet manually edited since. Default: `false`. `trade_plan.md` §10.5. |

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

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` — `status: 'active'` supplied with no `position_id` (ST-03, `BLG-BE-91`, EPIC-02, v8.6) — same rule as `PUT /trade-plans/{id}` below; a plan cannot be created already "active" with nothing backing it.

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

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` — `status: 'abandoned'` supplied without `abandonment_reason` (`BLG-FEAT-21`)
- `400` — `status: 'abandoned'` supplied for a plan linked to an open position (`BLG-FEAT-21`)
- `400` — `status: 'active'` supplied with no `position_id` on either the existing plan or this same update (ST-03, `BLG-BE-91`, EPIC-02, v8.6). `'active'` means "this plan backs a live position" — set this way only to prevent an orphaned active plan; see `data_model.md` DS-12 for the paired DB-level safeguard, and `data_model.md`'s "Trade Plan to Position Linkage" §"Nullability and backfill posture" for why `position_id` is nullable by design.
- `404` — plan not found

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

Generate a setup thesis for an existing trade plan using Claude Haiku 4.5.

Returns a generated thesis when `ANTHROPIC_API_KEY` is configured. Returns a graceful error payload (HTTP 200 with `available: false`) when the key is absent or the API call fails.

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
    "model_version": "claude-haiku-4-5",
    "prompt_version": "v3.0",
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
    "error": "ANTHROPIC_API_KEY not configured"
  }
}
```

### Error Responses

| HTTP status | Description |
|------------|-------------|
| 404 | Trade plan not found |

---

## POST /trade-plans/generate-plan

Generate a full set of trade plan fields from a ticker and optional signal data, without requiring an existing plan record. Uses Claude Haiku 4.5 via the Anthropic SDK.

Returns all fields when `ANTHROPIC_API_KEY` is configured. Returns a graceful error payload (HTTP 200 with `available: false`) when the key is absent or the API call fails.

**Authentication:** Standard API key authentication.

### Request Body

```json
{
  "ticker": "AAPL",
  "market": "US",
  "setup_type": "Momentum Continuation",
  "signal_data": {
    "signal_type": "breakout",
    "momentum_percent": 4.2,
    "atr_multiple": 1.8,
    "r_target": 2.5,
    "price_vs_50d_ma": 3.1,
    "regime": "risk_on",
    "signal_score": 82
  }
}
```

### Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ticker | string | Yes | Ticker symbol |
| market | string | No | `US` or `UK`. Default: `"US"` |
| setup_type | string | No | Setup classification (nullable) |
| signal_data | object | No | Structured signal context (nullable). Fields: `signal_type`, `momentum_percent`, `atr_multiple`, `r_target`, `price_vs_50d_ma`, `regime`, `signal_score` |

### Response (HTTP 200 — key configured, generation successful)

```json
{
  "available": true,
  "fields": {
    "setup_thesis": "Strong momentum breakout above the 52-week high with confirmed volume surge, supported by Risk On regime.",
    "entry_rationale": "Price holding above the 200 SMA with ATR expanding at 1.8x baseline; momentum at +4.2%.",
    "confirmation_criteria": "Volume > 1.5x average on breakout candle; RSI below overbought territory.",
    "early_exit_conditions": "Close below 200 SMA; regime flips to Risk Off.",
    "regime_context_at_entry": "risk_on",
    "r_target": 2.5
  },
  "model_version": "claude-haiku-4-5",
  "prompt_version": "v3.0"
}
```

### Response (HTTP 200 — key absent or API error)

```json
{
  "available": false,
  "error": "ANTHROPIC_API_KEY not configured"
}
```

### Error Responses

| HTTP status | Description |
|------------|-------------|
| 500 | Unexpected server error |

---

## GET /trade-plans/tags

Returns all unique tags used across `trade_plans.trade_tags` for the portfolio. Autocomplete source for the Trade Plan Tag Editor.

**Source:** ST-05, BLG-FEAT-52, v6.8. Mirrors `GET /positions/tags`. Data-independent from the existing position/journal tags (`journal_components.md`).

### Response (200)

```json
{ "status": "ok", "data": ["breakout", "earnings-play", "momentum"] }
```

### Errors

| Code | Condition |
|------|-----------|
| 500 | Database error |

---

## POST /trade-plans/bulk-tag

Add tags to each selected trade plan's existing `trade_tags` (union, not replace). New in v0.7 (ST-03, BLG-FE-117, EPIC-03, v7.5) — see `docs/specs/blg_fe_117_pre_implementation_readiness_pass.md` AC-01 for the batch-mutation pattern.

### Request Body

```json
{ "ids": ["plan-001", "plan-002"], "tags": ["momentum", "breakout"] }
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ids` | array of string (UUID) | Yes | Trade plan IDs to tag. Max 100 per call. |
| `tags` | array of string | Yes | Tags to add — same validation as `POST /trade-plans` (`_validate_trade_tags`: lowercase, alphanumeric+hyphen, max 20 chars, max 10 tags). Invalid tags are silently filtered, not rejected. |

### Response (200)

```json
{ "status": "ok", "data": { "succeeded": ["plan-001", "plan-002"], "failed": [] } }
```

On partial failure, `failed` contains `{id, reason}` objects (e.g. `reason: "not_found"`).

### Errors

| Code | Condition |
|------|-----------|
| 400 | `ids` empty or exceeds the 100-item cap |
| 500 | Database error |

---

## PUT /trade-plans/bulk-archive

Abandon (archive) each selected trade plan — reuses the existing single-plan abandonment transition (§8), not a new status. New in v0.7 (ST-03, BLG-FE-117, EPIC-03, v7.5).

Plans with `status = 'active'` are excluded (mirrors §8.1's single-item hide rule) and reported in `failed` with `reason: "active_status_excluded"`. The abandonment reason is a fixed system string (`"Bulk archived via Trade Plans bulk-action toolbar"`) — the bulk confirmation dialog does not collect a per-plan reason (`bulk-actions-toolbar/ux_spec.md` §2.5 defines no reason field for this flow, unlike the single-item Abandon modal's required reason textarea, §8.2).

### Request Body

```json
{ "ids": ["plan-001", "plan-002"] }
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ids` | array of string (UUID) | Yes | Trade plan IDs to archive. Max 100 per call. |

### Response (200)

```json
{ "status": "ok", "data": { "succeeded": ["plan-001"], "failed": [{"id": "plan-002", "reason": "active_status_excluded"}] } }
```

### Errors

| Code | Condition |
|------|-----------|
| 400 | `ids` empty or exceeds the 100-item cap |
| 500 | Database error |

---

## DELETE /trade-plans/bulk

Delete each selected trade plan in a single call. New in v0.7 (ST-03, BLG-FE-117, EPIC-03, v7.5).

### Request Body

```json
{ "ids": ["plan-001", "plan-002"] }
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ids` | array of string (UUID) | Yes | Trade plan IDs to delete. Max 100 per call. |

### Response (200)

```json
{ "status": "ok", "data": { "succeeded": ["plan-001", "plan-002"], "failed": [] } }
```

### Errors

| Code | Condition |
|------|-----------|
| 400 | `ids` empty or exceeds the 100-item cap |
| 500 | Database error |

---

## GET /trade-plans/setup-quality-score

Returns a 0–100 setup quality score derived from closed trade history for a given ticker.

**Source:** ST-08, EPIC-04, v6.1. Gate: ≥20 closed trades required.

**§13 Compliance:** Retroactively reviewed and confirmed PASS — see `docs/product/decisions/decisions--2026-07-21__release-v7.7--PT-04-section13-review.md` (ST-07, EPIC-07, v7.7). Deterministic, read-only, display-only historical-reference score; no automated action, no write path, no gating power over any trade or position workflow.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ticker | string | Yes | Ticker symbol (case-insensitive; echoed uppercase) |

### Response (200) — gate not met

```json
{ "status": "ok", "data": { "gate_not_met": true, "min_trades_required": 20, "current_trades": 15 } }
```

### Response (200) — gate met

```json
{
  "status": "ok",
  "data": {
    "gate_not_met": false,
    "ticker": "AAPL",
    "score": 70,
    "matching_trades": 25,
    "win_rate": 64.0,
    "average_pnl_pct": 8.5,
    "score_explanation": "Based on 25 closed trades: 64.0% win rate, 8.5% average return. Score = win_rate×0.6 + max(avg_return,0)×0.4."
  }
}
```

### Response fields

| Field | Type | Description |
|-------|------|-------------|
| gate_not_met | boolean | `true` when fewer than 20 closed trades exist |
| min_trades_required | integer | Always 20 |
| current_trades | integer | Present when `gate_not_met: true` — current closed trade count |
| ticker | string | Echoed from query parameter (uppercase). Present when `gate_not_met: false` |
| score | integer | 0–100 setup quality score. Present when `gate_not_met: false` |
| matching_trades | integer | Total closed trades used in calculation |
| win_rate | number | % of closed trades with pnl > 0 (1 dp) |
| average_pnl_pct | number | Average pnl_pct across all closed trades (2 dp) |
| score_explanation | string | Human-readable breakdown of the score |

### Score formula

```
score = clamp(round(win_rate × 0.6 + max(average_pnl_pct, 0) × 0.4), 0, 100)
```

### Errors

| Code | Condition |
|------|-----------|
| 500 | Database error |

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 0.11 | 2026-08-12 | ST-01/ST-03 (EPIC-01, v8.7, BLG-FEAT-84/BLG-BE-95): Add `invalidation_condition` (optional manual textarea) and `is_ai_draft` (AI-origin flag, default false) to POST/PUT /trade-plans request schema. `trade_plan.md` §5.1, §10.5. |
| 0.10 | 2026-08-12 | ST-03 (EPIC-02, v8.6, BLG-BE-91): `PUT /trade-plans/{id}` — `status: 'active'` now requires a `position_id` (either already on the plan, or supplied in this same update); 400 if neither. New Errors section documents this alongside the pre-existing (previously undocumented) abandonment-rule 400s and 404. DB-level backstop: `docs/specs/data_model.md` DS-12. |
| 0.9 | 2026-08-07 | ST-12 (EPIC-03, v8.4, BLG-BE-70): Add `thesis_model_version`/`thesis_prompt_version` to POST/PUT /trade-plans request schema — AI compliance provenance fields, frontend-passed, persisted only when the narrative fields were saved as-received from a generate-plan/generate-thesis response. Nullable, no backfill. Authority: AI Compliance & Governance Officer. |
| 0.8 | 2026-07-24 | ST-07 (EPIC-07, v7.7, BLG-GOV-28): Retroactive §13 boundary review of GET /trade-plans/setup-quality-score — PASS. No contract/behaviour change; added §13 Compliance reference to the endpoint section. See `docs/product/decisions/decisions--2026-07-21__release-v7.7--PT-04-section13-review.md`. |
| 0.7 | 2026-07-17 | ST-03 (BLG-FE-117, EPIC-03, v7.5): Add POST /trade-plans/bulk-tag, PUT /trade-plans/bulk-archive, DELETE /trade-plans/bulk — bulk-actions toolbar. `succeeded`/`failed` per-row response shape per readiness pass AC-01. Bulk-archive excludes `status='active'` plans (mirrors §8.1 single-item hide rule) and applies a fixed system abandonment reason (no per-plan reason field in the bulk confirmation flow). |
| 0.6 | 2026-07-09 | ST-05 (EPIC-02, v6.8, BLG-FEAT-52): Add GET /trade-plans/tags (tag autocomplete source); add `trade_tags` field to POST/PUT /trade-plans request schema. Data-independent from trade_annotations/PO-02 and from the existing position/journal tags. |
| 0.5 | 2026-06-23 | ST-08 (EPIC-04, v6.1): Add GET /trade-plans/setup-quality-score — 0–100 score from closed trade history, gate_not_met response when <20 trades. |
| 0.4 | 2026-05-26 | Switch generate-thesis from Gemini Flash to Claude Haiku 4.5; replace GEMINI_API_KEY with ANTHROPIC_API_KEY; update model_version in examples; add POST /trade-plans/generate-plan endpoint |
| 0.3 | 2026-05-24 | ST-12 (BLG-BE-19, v4.0 EPIC-03): Add POST /trade-plans/{plan_id}/generate-thesis — Gemini Flash thesis generation |
| 0.2 | 2026-05-20 | Add pre_entry_override_acknowledged to POST/PUT schemas — ST-03 EPIC-01 v3.8 |
| 0.1 | 2026-04-30 | Initial contract — ST-01 EPIC-01 v3.1 |

---

## Sign-off

- Data Model Domain & Schema Owner: Accepted — 2026-04-30
- Head of Specs Team: Accepted — 2026-04-30
