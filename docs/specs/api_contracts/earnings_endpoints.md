**Owner:** Head of Specs Team
**Class:** Specification (Class 2)
**Status:** Active
**Version:** 0.2
**Last Updated:** 2026-11-04 (ST-22, EPIC-03, v9.15, BLG-BE-174/BLG-BE-204 — next_earnings_date is the America/New_York date and days_until_earnings counts from the US market date); prior — 2026-04-30 (initial contract, ST-07, DS-04); prior history retained — see prior entries in version control
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
| next_earnings_date | string \| null | ISO 8601 date string (`YYYY-MM-DD`) or null if unavailable. A timestamp from the data source is dated in America/New_York, so an after-close release (e.g. 21:00 ET) is that ET day (v0.2, ST-22, BLG-BE-174) |
| days_until_earnings | integer \| null | Calendar days from the current US market date (America/New_York) to `next_earnings_date`, or null. `0` throughout ET day D for a release on D, whatever the UTC date (v0.2, BLG-BE-204; was counted from the server date) |
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
| 0.2 | 2026-11-04 | ST-22 (EPIC-03, v9.15, BLG-BE-174) and BLG-BE-204 (PR #2190 review): `next_earnings_date` from a timestamp is its America/New_York date, and `days_until_earnings` counts from the US market date, so both share one basis. The server-date count gave `-1` on the evening of an ET-evening release before it happened, which turned the `strategy_rules.md` §4.2.3 pre-entry earnings check from WARN to PASS. No shape change. |
| 0.1 | 2026-04-30 | Initial contract — ST-07 DS-04 |
