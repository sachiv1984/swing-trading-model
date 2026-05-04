**Owner:** Head of Specs Team
**Class:** Specification (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-04-30
**Cycle:** 2026-04-29__release-v3.1 (ST-07)

---

# Earnings Calendar API Contract

## Purpose

Documents the Earnings Calendar endpoints. Provides next earnings date for tickers sourced from Yahoo Finance. Used to display upcoming earnings proximity on screener, watchlist, and positions pages.

**Data freshness note:** Yahoo Finance earnings dates are generally reliable 2–4 weeks out. Dates further in the future may shift. Null is returned gracefully when no date is available.

---

## Endpoints

## GET /earnings/{ticker}

Returns the next scheduled earnings date for a given ticker.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ticker | string | Yes | Ticker symbol (e.g. `AAPL`, `TSCO` for UK) |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| market | string | `US` | Market: `US` or `UK`. UK tickers are resolved with `.L` suffix for Yahoo Finance. |

### Response

**200 OK**

```json
{
  "ticker": "AAPL",
  "next_earnings_date": "2026-07-29",
  "days_until_earnings": 90,
  "fiscal_quarter": null,
  "data_source": "yahoo_finance"
}
```

**Response when date unavailable:**

```json
{
  "ticker": "TSCO",
  "next_earnings_date": null,
  "days_until_earnings": null,
  "fiscal_quarter": null,
  "data_source": "yahoo_finance"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| ticker | string | The requested ticker symbol (as supplied, without `.L`) |
| next_earnings_date | string \| null | ISO 8601 date string (`YYYY-MM-DD`) or null if unavailable |
| days_until_earnings | integer \| null | Calendar days from today to `next_earnings_date`, or null |
| fiscal_quarter | string \| null | Fiscal quarter identifier if available from Yahoo Finance, otherwise null |
| data_source | string | Always `"yahoo_finance"` |

### Known Limitations

- Yahoo Finance does not provide a reliable `fiscal_quarter` field via `yfinance.Ticker.info`; this field will typically be null.
- Earnings dates beyond ~4 weeks are subject to revision.
- Some tickers (especially smaller UK stocks) may have no earnings date data; null is returned gracefully.

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 0.1 | 2026-04-30 | Initial contract — ST-07 DS-04 |
