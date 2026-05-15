**Owner:** API Contracts & Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-05-15
**Story:** ST-08 (EPIC-03, v3.3) — BLG-SPEC-25
**Cross-reference:** `docs/specs/data_provenance/research_view_provenance.md`
**Regression test anchor:** `docs/qa/acceptance_protocols/research_view_regression_protocol.md`
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# API Contract — Research Endpoint

## GET /research/{ticker}

Aggregated pre-trade research snapshot for a ticker. Combines live price, signal, market regime, sector, screener presence, earnings proximity, and news into a single response.

**Implementation:** `backend/routers/research.py`

**§13 compliance:** Display-only. No automated recommendation or action generated. Human reviews data and decides independently.

---

## Request

### Path Parameters

| Parameter | Type | Required | Format | Description |
|-----------|------|----------|--------|-------------|
| `ticker` | string | Yes | `AAPL`, `BARC.L` | Ticker symbol. UK tickers end with `.L`. |

### Query Parameters

| Parameter | Type | Default | Allowed values | Description |
|-----------|------|---------|----------------|-------------|
| `market` | string | Auto-detected | `US`, `UK` | Market code. If omitted, inferred from ticker: `.L` suffix → `UK`, otherwise `US`. |

### Market Auto-Detection

If `market` is not provided, the server applies:
```
if ticker.upper().endswith(".L") → market = "UK"
else → market = "US"
```

---

## Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "ticker": "AAPL",
    "market": "US",
    "price": 178.50,
    "price_change_pct": 0.0142,
    "market_cap": 2800000000000,
    "signal": {
      "signal_id": "uuid-string",
      "direction": "long",
      "signal_date": "2026-05-08",
      "status": "active",
      "rank": 1,
      "atr": 4.20,
      "entry_price": 178.50,
      "stop_price": 172.00,
      "r_target": 2.5
    },
    "regime": {
      "label": "risk_on",
      "spy_risk_on": true,
      "ftse_risk_on": true
    },
    "sector": {
      "sector": "Technology",
      "industry": "Consumer Electronics"
    },
    "screener": {
      "in_latest_results": true,
      "latest_run_timestamp": "2026-05-09T06:00:00Z",
      "score": 85,
      "atr_pct": 0.023
    },
    "earnings": {
      "next_earnings_date": "2026-07-25",
      "days_until_earnings": 76,
      "fiscal_quarter": "Q3 2026",
      "data_source": "yfinance"
    },
    "news_headlines": [
      {
        "title": "Apple reports record iPhone sales",
        "url": "https://example.com/article-1",
        "source": "Reuters",
        "published_at": "2026-05-09T10:30:00Z"
      }
    ]
  }
}
```

### Top-Level Response Fields

| Field | Type | Nullable | Source | Description |
|-------|------|----------|--------|-------------|
| `status` | string | No | internal | Always `"ok"` on success |
| `data.ticker` | string | No | path param | Normalised uppercase ticker |
| `data.market` | string | No | query param / auto | `"US"` or `"UK"` |
| `data.price` | number | Yes | Yahoo Finance | Current market price in native currency. UK: GBP (pence converted). Null if YF unavailable. |
| `data.price_change_pct` | number | Yes | Yahoo Finance | 1-day price change as decimal (0.0142 = +1.42%). Null if unavailable. |
| `data.market_cap` | number | Yes | yfinance.Ticker.info | Market cap in USD. Null for many UK tickers. |
| `data.signal` | object | Yes | Internal signals DB | Latest screener signal for the ticker (current portfolio). Null if no signal on file. |
| `data.regime` | object | Yes | SPY/FTSE 200-day MA check | Market regime classification. Null if market data unavailable. |
| `data.sector` | object | No | Yahoo Finance sector info | Always returned; fields may be null. |
| `data.screener` | object | Yes | Internal screener results cache | Null if ticker not in latest screener run. |
| `data.earnings` | object | Yes | yfinance | Null if no upcoming earnings found. |
| `data.news_headlines` | array | No | News service | Empty array if no headlines. Never null. |

### `signal` Object Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `signal_id` | string (UUID) | No | Internal signal ID |
| `direction` | string | Yes | `"long"` (only supported direction) |
| `signal_date` | string (date) | No | ISO date the signal was generated |
| `status` | string | No | `"active"`, `"watch"`, `"entered"`, `"dismissed"`, `"expired"`, `"already_held"` |
| `rank` | integer | Yes | Screener rank (1 = highest) |
| `atr` | number | Yes | ATR value at signal date |
| `entry_price` | number | Yes | Suggested entry price |
| `stop_price` | number | Yes | Suggested initial stop price |
| `r_target` | number | Yes | Target R-multiple for the trade |

### `regime` Object Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `label` | string | No | `"risk_on"`, `"risk_off"`, `"mixed"` |
| `spy_risk_on` | boolean | Yes | SPY above 200-day MA |
| `ftse_risk_on` | boolean | Yes | FTSE 100 index above 200-day MA |

### `sector` Object Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `sector` | string | Yes | Yahoo Finance sector (e.g. `"Technology"`) |
| `industry` | string | Yes | Yahoo Finance industry (e.g. `"Consumer Electronics"`) |

### `screener` Object Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `in_latest_results` | boolean | No | Always `true` when screener object is present |
| `latest_run_timestamp` | string (ISO datetime) | Yes | Timestamp of the screener run |
| `score` | number | Yes | Screener score (0–100) |
| `atr_pct` | number | Yes | ATR as percentage of price |

### `earnings` Object Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `next_earnings_date` | string (date) | Yes | ISO date of next scheduled earnings |
| `days_until_earnings` | integer | Yes | Calendar days from today |
| `fiscal_quarter` | string | Yes | e.g. `"Q3 2026"` |
| `data_source` | string | Yes | Always `"yfinance"` currently |

### `news_headlines` Array Items

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `title` | string | No | Headline text |
| `url` | string | Yes | Article URL (may be null if source doesn't provide) |
| `source` | string | Yes | Publisher name |
| `published_at` | string (ISO datetime) | Yes | Publication timestamp |

---

## Best-Effort Sourcing

**No sub-source failure causes a non-2xx response.** Each field group is independent:
- If Yahoo Finance is unavailable: `price`, `price_change_pct`, `market_cap`, `sector.sector`, `sector.industry` return `null`
- If the signal DB query fails: `signal` returns `null`
- If the regime check times out: `regime` returns `null`
- If the screener cache is empty: `screener` returns `null`
- If yfinance earnings lookup fails: `earnings` returns `null`
- If the news service fails: `news_headlines` returns `[]`

---

## Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| 500 | Unhandled exception in the aggregation handler itself (not sub-source failures) |

Note: 404 (ticker not found) and 503/429 (source unavailable) are not currently surfaced as distinct HTTP codes — the endpoint returns 200 with null fields for all sub-source failures. This is a known deviation (DEV-v33-02, filed v3.3).

**Known Deviation — DEV-v33-02**

| Field | Detail |
|-------|--------|
| Description | AC specified distinct HTTP error codes (404 ticker-not-found, 503 source-unavailable, 429 rate-limited); implementation always returns 200 with null sub-fields on sub-source failure |
| Canonical requirement | ST-08 acceptance criteria (sprint_backlog.md v3.3): "404 returned when ticker does not exist in any source; 503 returned for critical source failure; 429 returned when rate limit is hit" |
| Priority | P3 — current behaviour is safe and documented; clients must handle null sub-fields regardless |
| Target resolution release | v3.4 (or v4.x — non-blocking) |
| Owner | API Contracts & Documentation Owner |
| Backlog reference | BLG-SPEC-27 — Research endpoint: surface per-source error codes as distinct HTTP responses |

---

## Rate Limiting

| Source | Limit | Behaviour on breach |
|--------|-------|---------------------|
| Yahoo Finance (price) | Informal — no documented limit | 0.3s sleep injected before each call; `null` returned on error |
| Yahoo Finance (yfinance.info) | Informal | `null` returned on error |
| Internal DB (signals, screener) | No rate limit | N/A |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-05-15 | ST-10 (EPIC-03, v3.5) — Added regression test anchor cross-reference to `research_view_regression_protocol.md`. |
| 1.0 | 2026-05-10 | Initial creation — ST-08 (EPIC-03, v3.3). Full response schema, source attribution, error codes, rate limit policy. |
