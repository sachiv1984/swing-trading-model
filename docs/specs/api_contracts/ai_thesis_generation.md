**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.1.0
**Last Updated:** 2026-05-28
**Shipped:** v4.0 — ST-12, EPIC-03, cycle 2026-05-22__release-v4.0
**Supersedes:** docs/specs/api_contracts/gemini_thesis_generation.md v2.0.0 (renamed in v4.2 ST-08)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Thesis Generation API Contract

## Overview

This document defines the **AI Thesis Generation** endpoints — the Arc 5 AI-assisted trade plan authoring feature (SI-05 Phase 1).

The endpoints call Claude Haiku 4.5 (`claude-haiku-4-5`) via the Anthropic SDK to generate trade plan content. Two endpoints are available:

- **`POST /trade-plans/{plan_id}/generate-thesis`** — generates a concise 2–3 sentence setup thesis for an existing trade plan (backward-compatible legacy endpoint).
- **`POST /trade-plans/generate-plan`** — generates a full set of plan fields (thesis, entry rationale, confirmation criteria, early exit conditions, regime context, R-target) from a ticker and optional signal data, without requiring an existing plan record.

Generated content is returned to the caller for display and optional inclusion in the trade plan. No automated trade decisions are derived from the output.

**§13 compliance:** These endpoints generate advisory text only. They do not gate trade entry, trigger alerts, or influence position sizing. The operator may use, edit, or discard the generated content. This is a display-only, operator-reviewed output.

**Audit trail:** Each call writes a row to both `gemini_audit_log` (plan_id, model_version, prompt_version, input_hash, output_hash, token usage, estimated cost) and `claude_audit_log` (endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd). The `claude_audit_log` is queryable via `GET /ai/claude-audit-log`. See `backend/services/gemini_service.py`.

**Claude API response fields:** The Anthropic SDK returns a `usage` object with `input_tokens` and `output_tokens` (and optionally `cache_creation_input_tokens` / `cache_read_input_tokens` if prompt caching is enabled). These fields are logged to `claude_audit_log` but are **not** surfaced in the endpoint response — the response returns only `model_version` and `prompt_version` for traceability. To query usage metadata, use `GET /ai/claude-audit-log`.

**Cost tracking:** Token usage is logged with estimated cost at $1.00/1M input tokens and $5.00/1M output tokens (Claude Haiku 4.5 rates). The Anthropic API has no free tier; see `docs/ops/gemini_cost_tracking.md` for monitoring guidance.

**Backend implementation:** `backend/routers/trade_plans.py`, `backend/services/gemini_service.py`

Global response envelopes, error shape, and defaults are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [POST /trade-plans/{plan_id}/generate-thesis](#post-trade-plansplan_idgenerate-thesis)
- [POST /trade-plans/generate-plan](#post-trade-plansgenerate-plan)

---

## POST /trade-plans/{plan_id}/generate-thesis

**Purpose**

Generate a setup thesis for the specified trade plan via Claude Haiku 4.5. The endpoint reads the plan from the database, constructs a structured prompt, calls the Anthropic API, and returns the generated thesis along with audit metadata.

The endpoint always returns HTTP 200 — when the Anthropic API key is absent or the API call fails, the response includes `available: false` with an `error` field rather than raising an HTTP error. This enables graceful frontend degradation.

**Method & Path**

- `POST /trade-plans/{plan_id}/generate-thesis`

**Idempotency**

- Not idempotent. Each call makes an external Anthropic API request and writes an audit log row. Repeated calls for the same plan may produce different thesis text.

---

### Request

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| plan_id | string (UUID) | Yes | ID of the trade plan to generate a thesis for |

No request body is required.

---

### Response (200 — Thesis available)

When the Anthropic API key is configured and the API call succeeds:

```json
{
  "status": "ok",
  "data": {
    "available": true,
    "thesis": "Strong momentum breakout above the 52-week high with confirmed volume surge. ATR expanding and regime firmly Risk On. Entry justified by price holding above the 200 SMA with RSI below overbought territory.",
    "model_version": "claude-haiku-4-5",
    "prompt_version": "v3.0",
    "input_hash": "a1b2c3d4e5f67890",
    "output_hash": "f0e9d8c7b6a54321"
  }
}
```

#### `data` schema — available

| Field | Type | Description |
|-------|------|-------------|
| available | boolean | Always `true` when thesis is generated |
| thesis | string | Generated thesis text (2–3 sentences, ≤100 words) |
| model_version | string | Claude model ID used (e.g. `claude-haiku-4-5`). Matches `MODEL_VERSION` in `gemini_service.py`. |
| prompt_version | string | Internal prompt template version (e.g. `v3.0`) |
| input_hash | string | SHA-256 hex prefix (16 chars) of the serialised input payload. Used for audit deduplication. |
| output_hash | string | SHA-256 hex prefix (16 chars) of the generated thesis text |

**Note on usage fields:** The Anthropic API returns `usage.input_tokens`, `usage.output_tokens`, and optionally `usage.cache_creation_input_tokens` / `usage.cache_read_input_tokens` (when prompt caching is active). These are written to `claude_audit_log` but are not included in this response. Query `GET /ai/claude-audit-log` for token-level cost data.

---

### Response (200 — Thesis unavailable)

When the Anthropic API key is absent or the API call fails:

```json
{
  "status": "ok",
  "data": {
    "available": false,
    "error": "ANTHROPIC_API_KEY not configured"
  }
}
```

#### `data` schema — unavailable

| Field | Type | Description |
|-------|------|-------------|
| available | boolean | Always `false` when thesis could not be generated |
| error | string | Human-readable error description. Possible values: `"ANTHROPIC_API_KEY not configured"`, `"Anthropic API error: <detail>"` (truncated to 120 chars) |

**Frontend responsibility:** the client must inspect `data.available` before attempting to display `data.thesis`. Display a graceful fallback message when `available` is `false`.

---

### Response (404 — Plan not found)

```json
{
  "detail": "Trade plan not found"
}
```

Returned when `plan_id` does not exist in the current portfolio's trade plans.

---

### Response (500 — Server error)

```json
{
  "status": "error",
  "message": "<exception message>"
}
```

Returned for unexpected server-side failures unrelated to the Anthropic API (e.g. database connection error).

---

### Error Summary

| Condition | HTTP Status | `available` | Notes |
|-----------|-------------|-------------|-------|
| Thesis generated successfully | 200 | `true` | Normal path |
| API key not configured | 200 | `false` | Graceful degradation |
| Anthropic API error | 200 | `false` | Graceful degradation |
| Trade plan not found | 404 | — | Standard HTTP error |
| Server error | 500 | — | Unexpected failure |

---

### Input Construction

The thesis prompt is constructed from the following trade plan fields:

| Plan field | Used in prompt as |
|-----------|-------------------|
| ticker | Ticker symbol |
| market | Market (US / UK) |
| setup_type | Setup type label |
| entry_rationale | Additional context (first 80 chars) |
| confirmation_criteria | Additional context (first 60 chars) |

Signal data is not passed from the router endpoint (signal_data is None at invocation); only plan fields available at the time of the call are used.

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
  "model_version": "claude-haiku-4-5",
  "prompt_version": "v3.0"
}
```

#### Response schema — available

| Field | Type | Description |
|-------|------|-------------|
| available | boolean | Always `true` when generation succeeded |
| fields | object | Generated plan fields (see sub-schema below) |
| model_version | string | Claude model ID used (e.g. `claude-haiku-4-5`). Matches `MODEL_VERSION` in `gemini_service.py`. |
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
| 2.1.0 | 2026-05-28 | ST-08 (EPIC-03, v4.2): Rename gemini_thesis_generation.md → ai_thesis_generation.md. Document Claude API usage fields (input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens) — written to claude_audit_log, not surfaced in response. Clarify model_version description. |
| 2.0.0 | 2026-05-26 | Switch from Gemini Flash to Claude Haiku 4.5 (claude-haiku-4-5) via Anthropic SDK; update env var to ANTHROPIC_API_KEY; update cost rates ($1.00/1M input, $5.00/1M output); update prompt_version to v3.0; add POST /trade-plans/generate-plan endpoint; retitle document to AI Thesis Generation API Contract |
| 1.0.0 | 2026-05-25 | Initial contract — ST-12, EPIC-03, v4.0. POST /trade-plans/{plan_id}/generate-thesis with Gemini Flash |
