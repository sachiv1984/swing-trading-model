**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.2.0
**Last Updated:** 2026-10-30 (ST-22, EPIC-03, v9.14, BLG-BE-163 — POST /trade-plans/{plan_id}/generate-thesis retired (404); this is now the only thesis-generation contract, documenting generate-plan); prior — 2026-10-08 (ST-32, EPIC-05, v9.11, BLG-SPEC-175 — error example corrected to the canonical {status, message} envelope the code returns); prior — 2026-05-28; prior history retained — see prior entries in version control
**Shipped:** v4.0 — ST-12, EPIC-03, cycle 2026-05-22__release-v4.0
**Supersedes:** docs/specs/api_contracts/gemini_thesis_generation.md v2.0.0 (renamed in v4.2 ST-08; the superseded file was deleted in v9.14 ST-22)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Thesis Generation API Contract

## Overview

This document defines the **AI Thesis Generation** endpoints — the Arc 5 AI-assisted trade plan authoring feature (SI-05 Phase 1).

The endpoints call Claude Haiku 4.5 (pinned snapshot `claude-haiku-4-5-20251001`, from `backend/ai_models.py` since ST-09, v9.11; previously the floating alias `claude-haiku-4-5`) via the Anthropic SDK to generate trade plan content. One endpoint is available:

- **`POST /trade-plans/generate-plan`** — generates a full set of plan fields (thesis, entry rationale, confirmation criteria, early exit conditions, regime context, R-target) from a ticker and optional signal data, without requiring an existing plan record.

**Retired endpoint (v9.14, ST-22, BLG-BE-163):** `POST /trade-plans/{plan_id}/generate-thesis` was removed and now returns 404. "Improve with AI" has called `generate-plan` since 2026-05-25 (`f91a718a`), which fills every plan field including the thesis and works before the plan is saved; the TradePlan page's "Generate thesis" button is a deterministic template with no model call (`trade_plan.md` §5b). `generate_setup_thesis()` and its prompt were removed with the route. This file is now the only thesis-generation contract; the superseded `gemini_thesis_generation.md` was merged into it and deleted. Historical `claude_audit_log` / `gemini_audit_log` rows keep the endpoint name `POST /trade-plans/{plan_id}/generate-thesis`.

Generated content is returned to the caller for display and optional inclusion in the trade plan. No automated trade decisions are derived from the output.

**§13 compliance:** This endpoint generates advisory text only. They do not gate trade entry, trigger alerts, or influence position sizing. The operator may use, edit, or discard the generated content. This is a display-only, operator-reviewed output.

**Audit trail:** Each call writes a row to both `gemini_audit_log` (plan_id, model_version, prompt_version, input_hash, output_hash, token usage, estimated cost) and `claude_audit_log` (endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd). The `claude_audit_log` is queryable via `GET /ai/claude-audit-log`. See `backend/services/gemini_service.py`.

**Claude API response fields:** The Anthropic SDK returns a `usage` object with `input_tokens` and `output_tokens` (and optionally `cache_creation_input_tokens` / `cache_read_input_tokens` if prompt caching is enabled). These fields are logged to `claude_audit_log` but are **not** surfaced in the endpoint response — the response returns only `model_version` and `prompt_version` for traceability. To query usage metadata, use `GET /ai/claude-audit-log`.

**Cost tracking:** Token usage is logged with estimated cost at $1.00/1M input tokens and $5.00/1M output tokens (Claude Haiku 4.5 rates). The Anthropic API has no free tier; see `docs/ops/gemini_cost_tracking.md` for monitoring guidance.

**Backend implementation:** `backend/routers/trade_plans.py`, `backend/services/gemini_service.py`

Global response envelopes, error shape, and defaults are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [POST /trade-plans/generate-plan](#post-trade-plansgenerate-plan)

---

## POST /trade-plans/generate-plan

**Purpose**

Generate a full set of trade plan fields from a ticker and optional signal data, without requiring an existing plan record. Uses Claude Haiku 4.5 via the Anthropic SDK (`generate_full_plan()` in `backend/services/gemini_service.py`). Returns all generated fields as a JSON object.

The endpoint always returns HTTP 200 — when the Anthropic API key is absent or the API call fails, the response includes `available: false` with an `error` field.

**Method & Path**

- `POST /trade-plans/generate-plan`

**Idempotency**

- Not idempotent. Each call makes an external Anthropic API request and writes an audit log row. Repeated calls with the same inputs may produce different output.

---

### Request

#### Request Body

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

#### Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ticker | string | Yes | Ticker symbol (e.g. `AAPL`, `BARC.L`) |
| market | string | No | Market — `US` or `UK`. Default: `"US"` |
| setup_type | string | No | Setup classification (nullable). E.g. `"Momentum Continuation"`, `"Breakout"` |
| signal_data | object | No | Structured signal context (nullable). See sub-schema below. |

#### `signal_data` sub-schema

| Field | Type | Description |
|-------|------|-------------|
| signal_type | string | Signal classification (e.g. `"breakout"`, `"pullback"`) |
| momentum_percent | number | Momentum percentage |
| atr_multiple | number | ATR multiple at signal |
| r_target | number | Target R-multiple from signal |
| price_vs_50d_ma | number | Price distance from 50-day MA (%) |
| regime | string | Market regime label (e.g. `"risk_on"`, `"risk_off"`) |
| signal_score | number | Composite signal score (0–100) |

---

### Response (200 — Plan available)

When the Anthropic API key is configured and the API call succeeds:

```json
{
  "available": true,
  "fields": {
    "setup_thesis": "Strong momentum breakout above the 52-week high with confirmed volume surge, supported by Risk On regime.",
    "entry_rationale": "Price holding above the 200 SMA with ATR expanding at 1.8x baseline; momentum at +4.2% with regime firmly Risk On.",
    "confirmation_criteria": "Volume > 1.5x average on breakout candle; RSI below overbought territory; price does not close back below breakout level.",
    "early_exit_conditions": "Close below 200 SMA; regime flips to Risk Off; price retraces more than 1 ATR from entry.",
    "regime_context_at_entry": "risk_on",
    "r_target": 2.5
  },
  "model_version": "claude-haiku-4-5-20251001",
  "prompt_version": "v3.0"
}
```

#### Response schema — available

| Field | Type | Description |
|-------|------|-------------|
| available | boolean | Always `true` when generation succeeded |
| fields | object | Generated plan fields (see sub-schema below) |
| model_version | string | Claude model ID used (e.g. `claude-haiku-4-5-20251001`, pinned in `backend/ai_models.py` — ST-09, v9.11). Matches `MODEL_VERSION` in `gemini_service.py`. |
| prompt_version | string | Internal prompt template version (e.g. `v3.0`) |

**Note on usage fields:** Token counts (`input_tokens`, `output_tokens`) and cost are written to `claude_audit_log`, not returned in this response. Query `GET /ai/claude-audit-log` for per-call usage data.

#### `fields` sub-schema

| Field | Type | Description |
|-------|------|-------------|
| setup_thesis | string | High-level setup thesis (2–3 sentences) |
| entry_rationale | string | Specific entry rationale |
| confirmation_criteria | string | Entry confirmation criteria |
| early_exit_conditions | string | Conditions for early exit |
| regime_context_at_entry | string | Regime label at time of generation |
| r_target | number \| null | Target R-multiple, or null if not determinable |

---

### Response (200 — Plan unavailable)

When the Anthropic API key is absent or the API call fails:

```json
{
  "available": false,
  "error": "ANTHROPIC_API_KEY not configured"
}
```

#### Response schema — unavailable

| Field | Type | Description |
|-------|------|-------------|
| available | boolean | Always `false` when generation failed |
| error | string | Human-readable error description |

**Frontend responsibility:** inspect `available` before attempting to display `fields`. Display a graceful fallback message when `available` is `false`.

---

### Response (500 — Server error)

```json
{
  "status": "error",
  "message": "<exception message>"
}
```

---

### Error Summary

| Condition | HTTP Status | `available` | Notes |
|-----------|-------------|-------------|-------|
| Plan generated successfully | 200 | `true` | Normal path |
| API key not configured | 200 | `false` | Graceful degradation |
| Anthropic API error | 200 | `false` | Graceful degradation |
| Server error | 500 | — | Unexpected failure |

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 2.2.0 | 2026-10-30 | ST-22 (EPIC-03, v9.14, BLG-BE-163): `POST /trade-plans/{plan_id}/generate-thesis` retired: route, `generate_setup_thesis()` and its prompt removed; the path returns 404. Its section is removed; the superseded duplicate `gemini_thesis_generation.md` is merged into this file and deleted, so this is the only thesis-generation contract and documents `POST /trade-plans/generate-plan`. |
| 2.1.2 | 2026-10-08 | ST-32 (EPIC-05, v9.11, BLG-SPEC-175): 404 example corrected to the standard error envelope the route returns. (2.1.1 is EPIC-01's ST-09.) |
| 2.1.1 | 2026-10-08 | ST-09 (EPIC-01, v9.11, BLG-BE-142): Model is the pinned snapshot `claude-haiku-4-5-20251001` from `backend/ai_models.py`, replacing the floating alias `claude-haiku-4-5`. |
| 2.1.0 | 2026-05-28 | ST-08 (EPIC-03, v4.2): Rename gemini_thesis_generation.md → ai_thesis_generation.md. Document Claude API usage fields (input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens) — written to claude_audit_log, not surfaced in response. Clarify model_version description. |
| 2.0.0 | 2026-05-26 | Switch from Gemini Flash to Claude Haiku 4.5 (claude-haiku-4-5) via Anthropic SDK; update env var to ANTHROPIC_API_KEY; update cost rates ($1.00/1M input, $5.00/1M output); update prompt_version to v3.0; add POST /trade-plans/generate-plan endpoint; retitle document to AI Thesis Generation API Contract |
| 1.0.0 | 2026-05-25 | Initial contract — ST-12, EPIC-03, v4.0. POST /trade-plans/{plan_id}/generate-thesis with Gemini Flash |
