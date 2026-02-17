# README.md

## Momentum Trading Assistant — API Contracts (v1.5.0)

**Status:** Complete & current  
**Last updated:** 2026-02-17  
**Contract version:** 1.5.0  

This directory contains the **backend API contracts** for the *Momentum Trading Assistant* web application.

The system is a **decision-support tool**, not an automated trading bot. All trading logic is deterministic and executed server-side. The backend is the single source of truth; the frontend is responsible only for display, user input, and orchestration.

---

## Audience

These API contracts are intended for:

- **Frontend engineers** integrating the web UI with the backend APIs
- **Backend engineers** implementing and maintaining API behavior
- **QA and automation engineers** validating contract compliance and deterministic behavior

---

## How to Use This Documentation

1. **Start with `conventions.md`**  
   This file defines global rules that apply to *all* endpoints, including:
   - Authentication and authorization
   - Request and response envelopes
   - Error semantics
   - Pagination, filtering, and versioning
   - Common headers and HTTP status codes

2. **Navigate to the relevant domain file**  
   Each domain-specific file contains only the endpoints for that functional area, making reviews and ownership clear.

3. **Treat these files as contracts**  
   - Frontend clients must not infer or calculate values that are provided by the backend.
   - Backend changes that affect request/response shapes must be reflected here.

---

## Base URLs

- **Production:** `https://api.example.com`
- **Development:** `http://localhost:8000`

---

## Core Design Principles

The following principles apply across all APIs:

- **Backend as single source of truth**
  - All calculations (ATR, stops, P&L, FX conversions, regime detection) are server-side.
  - Frontend must never calculate or derive these values.

- **Human-in-the-loop execution**
  - The system never executes trades automatically.
  - Users must explicitly confirm exits and provide actual broker execution prices.

- **Deterministic behavior**
  - Identical inputs always produce identical outputs.
  - No experiments, A/B testing, or non-deterministic logic.

- **Multi-currency correctness**
  - Monetary values are returned in both GBP and native currency where applicable.
  - Stops are stored, enforced, and trailed **only in native currency**.
  - FX rate changes must never move stop levels.

- **Explainability**
  - Recommendations, stop movements, and exit signals include clear reasoning.

---

## Documentation Structure

The API contracts are split by concern to support incremental review and clear ownership.

### Cross-cutting standards
- **`conventions.md`**  
  Global API rules and conventions that apply to every endpoint.

### Domain-specific endpoints
- **`portfolio_endpoints.md`**  
  Portfolio overview, position creation, daily snapshots, and portfolio history (`GET /portfolio/history`).

- **`position_endpoints.md`**  
  Open positions, daily analysis, exits, notes, tags, and tag discovery.

- **`trade_endpoints.md`**  
  Closed trade history and trade-level statistics.

- **`cash_endpoints.md`**  
  Deposits, withdrawals, cash transactions, and cash summaries.

- **`analytics_endpoints.md`**  
  Comprehensive trading analytics via `GET /analytics/metrics` (executive metrics, advanced metrics, monthly trends, top performers, drawdown, and more), plus `POST /validate/calculations` for smoke-testing metric correctness.

- **`signal_endpoints.md`**  
  Signal generation, signal listing, and signal state updates.

- **`health_endpoints.md`**  
  Health checks, diagnostics, and endpoint test execution.

Each endpoint file follows a consistent structure:
- HTTP method and path
- Purpose and behavior
- Request schema (path, query, body)
- Response schema (success and error)
- Validation rules and constraints
- Example requests and responses

---

## Versioning

- **Current contract version:** 1.5.0
- **Change type:** Non-breaking — analytics contract rewritten to reflect completed implementation; README corrected
- **Previous version:** 1.4.1

### Changelog (Summary)

- **1.5.0 (2026-02-17)**
  - `analytics_endpoints.md` rewritten to reflect the completed implementation:
    - Five planned endpoints replaced by unified `GET /analytics/metrics?period=`
    - Full nested response structure documented
    - `POST /validate/calculations` added
    - Known limitations and backlog items recorded
  - README: `GET /portfolio/history` correctly attributed to `portfolio_endpoints.md` (was incorrectly listed under analytics)
  - README: `analytics_endpoints.md` description updated to reflect actual scope

- **1.4.1 (2026-02-15)**
  - Complete endpoint specifications
  - Full request/response examples
  - Journal and tag endpoints fully documented
  - No breaking changes

- **1.4.0 (2026-02-01)**
  - Trade journal support
  - Position tagging
  - Entry and exit notes

---

## Guiding Rule

If a behavior, field, or calculation is not explicitly documented in these contracts, **clients must not assume it exists**. When in doubt, the backend behavior defined here is authoritative.
