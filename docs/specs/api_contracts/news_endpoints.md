**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-06-09
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint:** 2026-06-08__release-v5.3 — ST-06 (BLG-SPEC-51, EPIC-01)

---

# News Endpoints

## Scope

Display-only news headlines for tickers. No sentiment scoring or trading recommendations. UK tickers return an empty headlines list (Alpaca news data is US-only). Per BLG-GOV-16 §13 review.

---

## GET /news/{ticker}

**Purpose**

Fetch up to 10 recent news headlines for a given ticker from Alpaca. Display-only — no automated action on headlines.

**Method & Path**

- `GET /news/{ticker}`

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | Yes | Ticker symbol (e.g. `AAPL`, `NVDA`). Normalised to uppercase. |

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `market` | string | No | `US` | `US` or `UK`. UK returns empty headlines. |
| `limit` | integer (1–10) | No | `10` | Number of headlines to return. |

**Response (200)**

```json
{
  "ok": true,
  "data": {
    "ticker": "AAPL",
    "market": "US",
    "headlines": [
      {
        "headline": "Apple reports record Q1 earnings",
        "source": "Reuters",
        "url": "https://...",
        "published_at": "2026-06-01T09:00:00Z"
      }
    ],
    "count": 1
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Ticker as passed (uppercased) |
| `market` | string | Market as passed (uppercased) |
| `headlines` | array | News items, newest first. Empty array if no news or UK market. |
| `count` | integer | Number of headlines returned |
| `headlines[].headline` | string | Article headline text |
| `headlines[].source` | string | News source name |
| `headlines[].url` | string | Article URL |
| `headlines[].published_at` | string (ISO 8601) | Publication timestamp |

**Constraints**

- Display-only: no sentiment scoring, no trading signal generation
- UK tickers always return `headlines: [], count: 0` — Alpaca news is US-only
- `limit` hard cap is 10 regardless of request value

**Error responses**

| Status | Condition |
|--------|-----------|
| 500 | Upstream Alpaca API error |

**Backend:** `backend/routers/news.py` (`get_ticker_news`)
**Data source:** Alpaca Markets News API (US equities only)

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-09 | v5.3 ST-06 (BLG-SPEC-51, EPIC-01): Initial contract for `GET /news/{ticker}`. Endpoint shipped in prior cycle; contract gap resolved. API Contracts & Documentation Owner sign-off. |
