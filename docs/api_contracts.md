# API Contracts — Momentum Trading Assistant (v1.4.1)

**Status:** Current  
**Last Updated:** February 15, 2026  
**Version:** 1.4.1 (clarifying, non‑breaking)

---

## Overview

This document defines the backend API contracts for the **Momentum Trading Assistant** web application.

The system is a **decision‑support tool**, not a trading bot.  
All strategy logic is **deterministic, server‑side**, and frozen for MVP.

The backend is the **single source of truth**.  
The frontend must never calculate indicators, stops, P&L, or FX conversions.

---

## Design Principles

- Backend is the **single source of truth**
- Frontend must never calculate:
  - ATR
  - Stops
  - Market regime
  - P&L
  - Currency conversions
- APIs return **fully explained decisions**
- Human‑in‑the‑loop: exits must be explicitly confirmed
- Predictability > flexibility
- **Exit prices are always user‑entered** (actual broker executions)

---

## Response Conventions (Normative)

### Success Response (ALL endpoints)

All successful responses **MUST** be wrapped as:

```json
{
  "status": "ok",
  "data": {}
}
```

Rules:
- `data` MUST always be present
- `data` may be an object or an array
- No endpoint may return a raw object or array at the top level

---

### Error Response (ALL endpoints)

All error responses **MUST** be wrapped as:

```json
{
  "status": "error",
  "message": "Human-readable explanation"
}
```

Rules:
- `message` MUST be user‑readable
- Internal error details MUST NOT be exposed
- Errors are deterministic and explain *why* the request failed

---

## Defaults & Optional Fields (Normative)

Unless otherwise stated, the following defaults apply **server‑side**:

| Field | Default Behaviour |
|-----|------------------|
| `exit_reason` | `"Manual Exit"` |
| `exit_date` | Today (UTC) |
| `shares` (exit) | All shares in position |
| `fx_rate` (UK stocks) | `1.0` |
| `stop_price` (entry) | `entry_price - (5 × ATR)` |

Frontend clients **must not** infer or calculate defaults.

---

## Critical: Multi‑Currency & Pricing Rules (Normative)

### Dual‑Currency Guarantee

Any field representing a **price, stop, or valuation** MUST return **both**:

- A **GBP value** (for portfolio calculations)
- A **native currency value** (for display)

#### Required Pattern

| Concept | GBP Field | Native Field |
|------|---------|-------------|
| Current price | `current_price` | `current_price_native` |
| Stop price | `stop_price` | `stop_price_native` |
| Initial stop | `initial_stop` | `initial_stop_native` |

---

### Native‑Currency Stop Stability (Hard Guarantee)

> **Stops are stored, enforced, and trailed in native currency ONLY.**

FX rate changes:
- MUST NOT move stops
- MAY change GBP equivalents for portfolio totals only

This applies to:
- Grace‑period stops
- Trailing stops
- Profitable & losing stop logic
- Partial exits

---

## Idempotency & Side‑Effect Semantics

### Idempotent (Safe to Refresh)

| Endpoint | Notes |
|-------|------|
| `GET /portfolio` | Refreshes live prices |
| `GET /positions` | Always fetches fresh prices |
| `GET /positions/analyze` | Deterministic recomputation |
| `GET /market/status` | Live market data |
| `GET /signals` | No mutation |
| `GET /health*` | No mutation |

---

### Mutating (Non‑Idempotent)

| Endpoint | Behaviour |
|-------|-----------|
| `POST /portfolio/position` | Creates a position |
| `POST /positions/{id}/exit` | Creates trade, updates cash |
| `POST /cash/transaction` | Records deposit/withdrawal |
| `PATCH /positions/{id}/note` | Updates journal |
| `PATCH /positions/{id}/tags` | Updates tags |
| `PATCH /signals/{id}` | Updates signal status |
| `DELETE /signals/{id}` | Permanent deletion |

---

### Snapshot Special Case

| Endpoint | Behaviour |
|-------|-----------|
| `POST /portfolio/snapshot` | **Idempotent upsert** (by portfolio + date) |

---

## Error Semantics (Normative)

| Category | HTTP Status | Description |
|-------|------------|-------------|
| Validation error | 400 | Invalid or missing input |
| Business rule violation | 400 | Valid input, invalid state |
| Resource not found | 404 | Entity does not exist |
| System error | 500 | Internal failure (no internals exposed) |

---

## Position Representations

Different endpoints intentionally return **different shapes**:

| Endpoint | Purpose |
|-------|--------|
| `GET /positions` | Trading screen (live prices, stops, FX context) |
| `GET /positions/{id}` | Deep inspection / diagnostics |
| `GET /trades` | Historical, immutable records |

These representations are **not interchangeable**.

---

## Exit Price & FX Rules (Hard Requirements)

### Exit Price

- Exit price is **ALWAYS user‑provided**
- Live prices are **never fetched** for exits
- Ensures reconciliation with broker statements

### FX Rate (US Stocks)

- FX rate is **ALWAYS user‑provided** for US exits
- Must match broker statement exactly
- Backend MUST reject US exits without FX rate
- Ignored for UK stocks (rate = 1.0)

---

## Frontend Responsibilities (Explicit)

Frontend clients MUST:

- Never calculate ATR, stops, P&L, or FX conversions
- Always submit user‑entered exit prices
- Always submit FX rate for US exits
- Display **native‑currency stops** to users
- Treat empty strings as `null` for notes

---

## Endpoints

### 1. Portfolio Overview  
`GET /portfolio`

Primary working screen with live prices and cash management.

---

### 2. Positions List  
`GET /positions`

Returns all **open positions** with live prices and stop context.

---

### 3. Add Position  
`POST /portfolio/position`

Manual sync with broker executions. Supports fractional shares.

---

### 4. Daily Analysis  
`GET /positions/analyze`

Runs deterministic daily monitoring logic.

---

### 5. Exit Position  
`POST /positions/{position_id}/exit`

User‑confirmed exit using broker execution prices.

---

### 6. Portfolio History  
`POST /portfolio/snapshot`  
`GET /portfolio/history`

---

### 7. Trade History  
`GET /trades`

---

### 8. Cash Management

- `POST /cash/transaction`
- `GET /cash/transactions`
- `GET /cash/summary`

---

### 9. Signal Generation

- `POST /signals/generate`
- `GET /signals`
- `PATCH /signals/{id}`
- `DELETE /signals/{id}`

---

### 10. Market Status  
`GET /market/status`

---

### 11. Health & Diagnostics

- `GET /health`
- `GET /health/detailed`
- `GET /test/endpoints`

---

### 12. Trade Journal

- `PATCH /positions/{id}/note`
- `PATCH /positions/{id}/tags`
- `GET /positions/tags`

---

### 13. Settings  
`GET /settings`

---

## Versioning

- **Contract Version:** 1.4.1  
- **Change Type:** Clarifying, non‑breaking  
- **Client Impact:** None
