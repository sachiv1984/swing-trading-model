**Owner:** API Contracts & Documentation Owner
**Class:** Class 2 Canonical Specification
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-23
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Screener schema reference:** docs/specs/screener_results_schema.md

---

# Alpaca Integration Contract

**Purpose:** Defines the authoritative integration contract between this system and the Alpaca Markets API. All backend code calling Alpaca APIs must conform to this contract. DS-05 (Alpaca US Market Data Integration) and DS-06 (Alpaca News Panel) are governed by this document.

**Scope:** US market tickers only. UK tickers continue to use Yahoo Finance. No UK market data is fetched from Alpaca.

---

## API Version

**Alpaca Data API v2** is the canonical API version for this integration.

- Base URL: `https://data.alpaca.markets`
- API version: `v2` (for market data), `v1beta1` (for news — Alpaca's stable news endpoint at time of this contract)
- Authentication: API Key + Secret Key headers (`APCA-API-KEY-ID`, `APCA-API-SECRET-KEY`)

**Version pin:** This contract is pinned to Alpaca Data API v2. Any migration to a future version requires a new contract version and Head of Specs Team sign-off before deployment.

---

## Authentication

All requests to `data.alpaca.markets` must include:

| Header | Value |
|--------|-------|
| `APCA-API-KEY-ID` | Alpaca API key (from `ALPACA_API_KEY` environment variable) |
| `APCA-API-SECRET-KEY` | Alpaca API secret (from `ALPACA_API_SECRET` environment variable) |

Credentials must be read from environment variables at runtime. They must never be hard-coded or committed to version control.

---

## GET /v2/stocks/{symbol}/bars

Fetches historical OHLCV (Open, High, Low, Close, Volume) price bars for a US ticker.

**Usage in this system:** DS-05 — replaces Yahoo Finance as the OHLCV data source for US tickers. Used for ATR calculation, regime gate evaluation (via SPY), and signal generation inputs.

**Request:**

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `symbol` | path | string | YES | Ticker symbol (e.g. `NVDA`, `AAPL`) |
| `timeframe` | query | string | YES | Bar timeframe. Use `"1Day"` for daily bars |
| `limit` | query | integer | NO | Number of bars to return. Use 30 for ATR calculation safety margin (14 periods + buffer) |
| `adjustment` | query | string | NO | Price adjustment. Use `"raw"` (default) |
| `feed` | query | string | NO | Data feed. Use `"iex"` or omit for default SIP data |

**Response (HTTP 200):**

```json
{
  "bars": [
    {
      "t": "2026-04-22T04:00:00Z",
      "o": 880.0,
      "h": 895.0,
      "l": 875.0,
      "c": 890.0,
      "v": 12000000,
      "vw": 886.5,
      "n": 85000
    }
  ],
  "symbol": "NVDA",
  "next_page_token": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `bars[].t` | ISO-8601 string | Bar open timestamp (UTC) |
| `bars[].o` | number | Open price (USD) |
| `bars[].h` | number | High price (USD) |
| `bars[].l` | number | Low price (USD) |
| `bars[].c` | number | Close price (USD) |
| `bars[].v` | integer | Volume |
| `bars[].vw` | number | Volume-weighted average price |
| `bars[].n` | integer | Trade count |
| `next_page_token` | string \| null | Pagination token. Null = final page |

**Error responses:**

| HTTP status | Meaning | Action |
|------------|---------|--------|
| 200 | Success | Use bars data |
| 403 | Invalid or missing credentials | Check ALPACA_API_KEY / ALPACA_API_SECRET env vars |
| 404 | Symbol not found | Treat as no data available; apply fallback |
| 422 | Invalid request parameters | Log error; do not retry; skip ticker |
| 429 | Rate limit exceeded | Retry with exponential backoff (see §Rate Limits) |
| 5xx | Server error | Retry with exponential backoff (see §Retry Strategy) |

---

## GET /v1beta1/news

Fetches recent news headlines for one or more US tickers.

**Usage in this system:** DS-06 — news headlines displayed in the ticker-level news panel on screener results and watchlist. Display-only per BLG-GOV-16 §13 review (`docs/product/decisions/sec13_review_DS-06_alpaca_news_panel.md`).

**Request:**

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `symbols` | query | string | YES | Comma-separated ticker symbols (e.g. `NVDA,AAPL`) |
| `limit` | query | integer | NO | Maximum headlines per symbol. Default: 10. Maximum: 50 |
| `sort` | query | string | NO | `"desc"` (newest first, default) or `"asc"` |
| `start` | query | string | NO | ISO-8601 start date (UTC). Omit for recent news |

**Response (HTTP 200):**

```json
{
  "news": [
    {
      "id": 10001,
      "headline": "NVIDIA Reports Record Data Centre Revenue",
      "author": "Reuters",
      "created_at": "2026-04-22T10:30:00Z",
      "updated_at": "2026-04-22T10:30:00Z",
      "summary": "NVIDIA quarterly results exceed analyst expectations.",
      "url": "https://example.com/nvda-results",
      "symbols": ["NVDA"],
      "source": "reuters"
    }
  ],
  "next_page_token": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `news[].id` | integer | Alpaca news item ID |
| `news[].headline` | string | Headline text (verbatim) |
| `news[].author` | string \| null | Author or source name |
| `news[].created_at` | ISO-8601 string | Publication timestamp (UTC) |
| `news[].updated_at` | ISO-8601 string | Last update timestamp (UTC) |
| `news[].summary` | string \| null | Short summary (may be null) |
| `news[].url` | string \| null | Source URL (may be null) |
| `news[].symbols` | array\<string\> | Tickers mentioned |
| `news[].source` | string \| null | News source identifier |
| `next_page_token` | string \| null | Pagination token |

**§13 compliance:** This endpoint is used for display-only headline surfacing. No sentiment scoring, no sentiment labels, and no advisory generation from news content. See `docs/product/decisions/sec13_review_DS-06_alpaca_news_panel.md`.

**Error responses:**

| HTTP status | Meaning | Action |
|------------|---------|--------|
| 200 | Success | Use news data |
| 403 | Invalid credentials | Check env vars |
| 404 | No news for symbol | Return `news_headline_count: 0`, `news_headlines: []` |
| 429 | Rate limit exceeded | Retry with backoff; serve empty news panel on failure |
| 5xx | Server error | Return empty news panel; do not block screener results |

---

## Rate Limits

Alpaca rate limits vary by subscription tier. Conservative defaults for this integration:

| Tier | Requests per minute |
|------|-------------------|
| Free / paper | 200 req/min |
| Paid (unlimited data) | 10,000 req/min |

**Implementation rule:** Do not exceed 200 requests per minute in any batch screener run. For screener runs covering a large ticker universe, implement pacing with a configurable delay between calls (default: 50ms between requests). This is conservative and leaves headroom for other API calls.

---

## Retry Strategy

| Condition | Strategy |
|-----------|----------|
| HTTP 429 | Exponential backoff: wait `2^attempt × 1s`, max 5 retries, max wait 32s |
| HTTP 5xx | Exponential backoff: wait `2^attempt × 0.5s`, max 3 retries |
| Network timeout | Single retry after 2s; on second failure apply fallback |
| HTTP 403 | Do not retry — credentials error; log and apply fallback for the affected ticker |
| HTTP 404, 422 | Do not retry — permanent or data error; apply fallback |

---

## Fallback Strategy

When Alpaca returns a non-retriable error, is unavailable, or returns empty bars for a US ticker, the fallback strategy is:

**OHLCV data (DS-05):** Fall back to **Yahoo Finance** for the affected ticker.
- Use the same `calculate_atr()` / `get_current_price()` logic in `backend/utils/pricing.py`.
- Log the fallback event at `WARNING` level: `"Alpaca unavailable for {ticker} — falling back to Yahoo Finance"`.
- Do not silently swallow the fallback; it must be logged.

**News data (DS-06):** Do **not** fall back to another news source. Return `news_headline_count: 0` and `news_headlines: []` for the affected ticker.
- The news panel shows an empty state. This is acceptable behaviour per §13 compliance (display-only; no news is not an error state).

**Explicit error vs silent fallback:** The fallback is automatic but **always logged**. A ticker that returns Yahoo Finance data instead of Alpaca data after fallback must be distinguishable in logs. No silent fallback that appears identical to a successful Alpaca call.

---

## Implementation Notes

- **US tickers only.** Alpaca does not serve UK market data. The `market` field on a screener result determines which data source to use. UK tickers (`.L` suffix) must never be sent to Alpaca.
- **API version pin.** All calls must use the versions specified in the API Version section. Do not auto-discover or upgrade API versions at runtime.
- **Environment variables.** `ALPACA_API_KEY` and `ALPACA_API_SECRET` must be present in the runtime environment. The service must fail fast at startup if these are missing.
- **Test harness.** In CI, the Alpaca API is mocked by the `tests/mock_harness/` harness (BLG-QA-08 / ST-09). No live API calls are made in CI.

---

## DoQ Sign-Off

- [x] All DS-05 Alpaca endpoints documented at `##` heading level with request/response schemas
- [x] Rate limits documented
- [x] Error codes documented
- [x] Retry strategy documented
- [x] Fallback strategy explicitly defined (Yahoo Finance fallback for OHLCV; empty panel for news)
- [x] API version pinned
- [x] Corresponding OpenAPI entries added to `docs/reference/openapi.yaml` (external APIs section)
- [x] Document added to Specs_Index.md (via §3.4b registration)
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-04-23
- Comments: Autonomous class sign-off — all four qualifying criteria met.
