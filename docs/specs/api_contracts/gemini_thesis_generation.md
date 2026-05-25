**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0.0
**Last Updated:** 2026-05-25
**Shipped:** v4.0 — ST-12, EPIC-03, cycle 2026-05-22__release-v4.0
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Gemini Thesis Generation API Contract

## Overview

This document defines the **Gemini Thesis Generation** endpoint — the Arc 5 AI-assisted trade plan authoring feature (SI-05 Phase 1).

The endpoint calls Gemini Flash to generate a concise 2–3 sentence setup thesis for a trade plan based on the ticker, market, setup type, entry rationale, and confirmation criteria already recorded in the plan. The generated thesis is returned to the caller for display and optional inclusion in the trade plan. No automated trade decisions are derived from the thesis.

**§13 compliance:** This endpoint generates advisory text only. It does not gate trade entry, trigger alerts, or influence position sizing. The operator may use, edit, or discard the generated thesis. This is a display-only, operator-reviewed output.

**Audit trail:** Each call writes a row to `gemini_audit_log` (plan_id, model_version, prompt_version, input_hash, output_hash, token usage, estimated cost). See `backend/services/gemini_service.py`.

**Cost tracking:** Token usage is logged against monthly free-tier limits (1M tokens/month; alert at 800K). Estimated cost computed at $0.075/1M input tokens and $0.30/1M output tokens (Gemini 1.5 Flash rates).

**Backend implementation:** `backend/routers/trade_plans.py`, `backend/services/gemini_service.py`

Global response envelopes, error shape, and defaults are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [POST /trade-plans/{plan_id}/generate-thesis](#post-trade-plansplan_idgenerate-thesis)

---

## POST /trade-plans/{plan_id}/generate-thesis

**Purpose**

Generate a setup thesis for the specified trade plan via Gemini Flash. The endpoint reads the plan from the database, constructs a structured prompt, calls Gemini, and returns the generated thesis along with audit metadata.

The endpoint always returns HTTP 200 — when the Gemini API key is absent or the API call fails, the response includes `available: false` with an `error` field rather than raising an HTTP error. This enables graceful frontend degradation.

**Method & Path**

- `POST /trade-plans/{plan_id}/generate-thesis`

**Idempotency**

- Not idempotent. Each call makes an external Gemini API request and writes an audit log row. Repeated calls for the same plan may produce different thesis text.

---

### Request

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| plan_id | string (UUID) | Yes | ID of the trade plan to generate a thesis for |

No request body is required.

---

### Response (200 — Thesis available)

When the Gemini API key is configured and the API call succeeds:

```json
{
  "status": "ok",
  "data": {
    "available": true,
    "thesis": "Strong momentum breakout above the 52-week high with confirmed volume surge. ATR expanding and regime firmly Risk On. Entry justified by price holding above the 200 SMA with RSI below overbought territory.",
    "model_version": "gemini-1.5-flash",
    "prompt_version": "v1.0",
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
| model_version | string | Gemini model used (e.g. `gemini-1.5-flash`) |
| prompt_version | string | Internal prompt template version (e.g. `v1.0`) |
| input_hash | string | SHA-256 hex prefix (16 chars) of the serialised input payload. Used for audit deduplication. |
| output_hash | string | SHA-256 hex prefix (16 chars) of the generated thesis text |

---

### Response (200 — Thesis unavailable)

When the Gemini API key is absent, the `google-generativeai` package is not installed, or the Gemini API call fails:

```json
{
  "status": "ok",
  "data": {
    "available": false,
    "error": "GEMINI_API_KEY not configured"
  }
}
```

#### `data` schema — unavailable

| Field | Type | Description |
|-------|------|-------------|
| available | boolean | Always `false` when thesis could not be generated |
| error | string | Human-readable error description. Possible values: `"GEMINI_API_KEY not configured"`, `"google-generativeai package not installed"`, `"Gemini API error: <detail>"` (truncated to 120 chars) |

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

Returned for unexpected server-side failures unrelated to the Gemini API (e.g. database connection error).

---

### Error Summary

| Condition | HTTP Status | `available` | Notes |
|-----------|-------------|-------------|-------|
| Thesis generated successfully | 200 | `true` | Normal path |
| API key not configured | 200 | `false` | Graceful degradation |
| Package not installed | 200 | `false` | Graceful degradation |
| Gemini API error | 200 | `false` | Graceful degradation |
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
