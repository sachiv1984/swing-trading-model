**Owner:** API Contracts & Documentation Owner
**Class:** Class 2 Canonical Specification
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-25
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Implementation:** `backend/routers/ticker_universe.py`, `backend/services/ticker_universe_service.py`

---

# Ticker Universe API Contract

**Purpose:** Defines the canonical API contract for the ticker universe management endpoints (DS-01 / ST-01). These endpoints manage the set of tickers eligible for screener runs.

---

## GET /ticker-universe

Returns the list of active tickers in the screener universe.

**Authentication:** Standard API key authentication (per `docs/specs/api_contracts/conventions.md`).

### Request

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `market` | query | enum(`"UK"`, `"US"`) | NO | Filter by market. Omit for all markets |
| `active_only` | query | boolean | NO | Return only active tickers. Default: `true` |

### Response (HTTP 200)

```json
{
  "status": "ok",
  "data": [
    {
      "ticker": "AAPL",
      "market": "US",
      "active": true,
      "sector": "Technology",
      "industry": "Consumer Electronics",
      "created_at": "2026-04-25T00:00:00Z"
    }
  ]
}
```

### Error Responses

| HTTP status | Description |
|------------|-------------|
| 400 | Invalid `market` value (must be `UK` or `US`) |

---

## POST /ticker-universe

Adds a ticker to the screener universe. Re-activates soft-deleted tickers on conflict.

**Authentication:** Standard API key authentication.

### Request Body

```json
{
  "ticker": "AAPL",
  "market": "US",
  "sector": "Technology",
  "industry": "Consumer Electronics"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | YES | Exchange ticker symbol (e.g. `AAPL`, `HSBA.L`). Normalised to uppercase |
| `market` | enum(`"UK"`, `"US"`) | YES | Market classification |
| `sector` | string | NO | Sector classification |
| `industry` | string | NO | Industry sub-classification |

### Response (HTTP 201)

```json
{
  "status": "ok",
  "data": {
    "ticker": "AAPL",
    "market": "US",
    "active": true,
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "created_at": "2026-04-25T00:00:00Z"
  }
}
```

### Error Responses

| HTTP status | Description |
|------------|-------------|
| 400 | Invalid `market` (must be `UK` or `US`) or blank `ticker` |

---

## DELETE /ticker-universe/{ticker}

Soft-deletes a ticker from the screener universe (sets `active=FALSE`). The ticker remains in the database and can be re-activated via `POST /ticker-universe`.

**Authentication:** Standard API key authentication.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticker` | string | Ticker symbol to deactivate (e.g. `AAPL`, `HSBA.L`) |

### Response (HTTP 200)

```json
{
  "status": "ok"
}
```

### Error Responses

| HTTP status | Description |
|------------|-------------|
| 404 | Ticker not found or already inactive |

---

## Known Deviations

### DEV-EPIC04-ST09-01 — createPageUrl map missing TickerUniverse entry at merge time (Resolved)

- **Description:** `src/utils/index.js` `createPageUrl` map did not include `TickerUniverse: '/TickerUniverse'` at the time EPIC-04 PR #452 merged. Clicking the sidebar "Ticker Universe" nav link resolved to `/` (dashboard) instead of `/TickerUniverse`.
- **Canonical requirement:** "Universe Management page accessible from nav" (ST-09 AC)
- **Priority:** P3 (UX bug; workaround: navigate directly to `/#/TickerUniverse`)
- **Status:** Resolved — fix committed 75b7eda4 on EPIC-01 branch; merged with PR #456 (2026-05-20)
- **Target resolution release:** v3.8 (resolved in same release)
- **Owner:** Head of UX & Design
- **Backlog reference:** No separate item — fix was in pipeline and merged before delivery verification

---

## DoQ Sign-Off

- [x] All three endpoints documented at `##` heading level
- [x] Request/response schemas defined with field names and types
- [x] Error codes documented
- [x] Authentication requirements referenced
- [x] Corresponding OpenAPI entries present in `docs/reference/openapi.yaml`
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-04-25
- Comments: Autonomous class sign-off — all four qualifying criteria met.
