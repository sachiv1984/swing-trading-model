**Owner:** Head of Specs Team
**Class:** Specification (Class 2)
**Status:** Active
**Version:** 0.4
**Last Updated:** 2026-11-24 (ST-33, EPIC-06, v9.18, BLG-FE-294 — data_status: ok | unavailable tells a failed lookup from no upcoming date); prior — 2026-11-13 (ST-15, EPIC-06, v9.17, BLG-OPS-217 — next_earnings_date is the earliest upcoming Yahoo earnings date, not the last report; funds skip the calendar lookup); prior — 2026-11-04 (ST-22, EPIC-03, v9.15, BLG-BE-174/BLG-BE-204 — next_earnings_date is the America/New_York date and days_until_earnings counts from the US market date); prior history retained — see prior entries in version control
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
  "data_source": "yahoo_finance",
  "data_status": "ok"
}
```

**Response when Yahoo has no upcoming date** (`data_status: "ok"`):

```json
{
  "ticker": "TSCO",
  "next_earnings_date": null,
  "days_until_earnings": null,
  "fiscal_quarter": null,
  "data_source": "yahoo_finance",
  "data_status": "ok"
}
```

**Response when the lookup failed** (`data_status: "unavailable"`, v0.4):

```json
{
  "ticker": "AAPL",
  "next_earnings_date": null,
  "days_until_earnings": null,
  "fiscal_quarter": null,
  "data_source": "yahoo_finance",
  "data_status": "unavailable"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| ticker | string | The requested ticker symbol (as supplied, without `.L`) |
| next_earnings_date | string \| null | ISO 8601 date string (`YYYY-MM-DD`) or null if unavailable. A timestamp from the data source is dated in America/New_York, so an after-close release (e.g. 21:00 ET) is that ET day (v0.2, ST-22, BLG-BE-174). It is the earliest of Yahoo's `earningsDate`, `earningsTimestampStart`, `earningsTimestampEnd` and `earningsTimestamp` that is on or after the current US market date; a release today is kept (`days_until_earnings` 0). When every date Yahoo gives is in the past, it is null (v0.3, ST-15, BLG-OPS-217: after a report, `earningsTimestamp` keeps the past date while `earningsTimestampStart` holds the next one, e.g. AAPL on 2026-11-13: 2026-11-02 and 2027-01-28; before v0.3 the past date was returned with a negative `days_until_earnings`). Only when Yahoo gives no date at all is `Ticker.calendar` read, and not for funds and indices (`quoteType` ETF, MUTUALFUND, INDEX and similar), which have no earnings. |
| days_until_earnings | integer \| null | Calendar days from the current US market date (America/New_York) to `next_earnings_date`, or null. `0` throughout ET day D for a release on D, whatever the UTC date (v0.2, BLG-BE-204; was counted from the server date) |
| fiscal_quarter | string \| null | Fiscal quarter identifier if available from Yahoo Finance, otherwise null |
| data_source | string | Always `"yahoo_finance"` |
| data_status | string | *(v0.4, ST-33, BLG-FE-294)* `"ok"` when Yahoo answered: a usable `Ticker.info` (one carrying `quoteType`), a cached answer, or a calendar date. `next_earnings_date` may still be null (no upcoming date, a fund, only past dates). `"unavailable"` when the lookup failed: an exception, no free lookup slot within 30 seconds, or a throttled answer with no `quoteType` and no date. The frontend shows "Unknown" for `unavailable`, holds it for 60 seconds and never caches it for the session, so the first render after that retries (Product Owner ruling 2026-11-24, DEV-EPIC06-ST33-01); `GET /positions/{position_id}/gap-risk` passes it on as its own `data_status`. An `unavailable` answer is never cached here either (Known Limitations, Caching). |

### Known Limitations

- Yahoo Finance does not provide a reliable `fiscal_quarter` field via `yfinance.Ticker.info`; this field will typically be null.
- Earnings dates beyond ~4 weeks are subject to revision.
- Some tickers (especially smaller UK stocks) may have no earnings date data; null is returned gracefully with `data_status: "ok"`.
- Yahoo often keeps only the last report date for UK tickers until it publishes the next one, so a UK ticker shortly after its report returns null (v0.3).
- **Caching (v0.3, ST-15, BLG-OPS-217).** Results are cached per Yahoo symbol for 12 hours after a usable Yahoo answer (one that carries `quoteType`), so a new or rescheduled date can take up to 12 hours to appear. A failed or throttled lookup is not cached. `days_until_earnings` is counted on every call, and a cached date that has passed is looked up again. The `Ticker.info` answer is shared with the sector lookup and the research market cap (`backend/utils/yahoo_info.py`), and at most 4 Yahoo lookups run at once across the server; a request that waits more than 30 seconds for a slot returns the null response with `data_status: "unavailable"` (v0.4). Production evidence: on 2026-11-09 15:37–15:38 a page firing one lookup per row made 471 Yahoo calls in two minutes and 418 failed.

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 0.4 | 2026-11-24 | ST-33 (EPIC-06, v9.18, BLG-FE-294): new `data_status` (`ok` \| `unavailable`), so a failed lookup is distinguishable from a successful lookup with no upcoming date (both return a null date). Additive. The Screener makes no lookup for UK rows (`screener_results.md` v1.12). Also fixed: the `Ticker.calendar` fallback read only the old DataFrame shape, but the pinned yfinance 1.7.0 returns a dict of dates, so the fallback never found a date; both shapes are read now, so an equity whose `Ticker.info` has no earnings fields can now get a date from its calendar (and, for a US position, a gap-risk flag). |
| 0.3 | 2026-11-13 | ST-15 (EPIC-06, v9.17, BLG-OPS-217): results cached 12 hours per symbol after a usable answer, and at most 4 Yahoo lookups at once (Known Limitations). `next_earnings_date` is the earliest upcoming of `earningsDate`, `earningsTimestampStart`, `earningsTimestampEnd` and `earningsTimestamp`, or null when all are past. Before v0.3 it was `earningsTimestamp`, which keeps the past report after it happens, so the badge (which hides negative days) and the `strategy_rules.md` §4.2.3 pre-entry check missed the next report. Funds skip the calendar fallback, whose two 404 calls counted as provider failures. No shape change. |
| 0.2 | 2026-11-04 | ST-22 (EPIC-03, v9.15, BLG-BE-174) and BLG-BE-204 (PR #2190 review): `next_earnings_date` from a timestamp is its America/New_York date, and `days_until_earnings` counts from the US market date, so both share one basis. The server-date count gave `-1` on the evening of an ET-evening release before it happened, which turned the `strategy_rules.md` §4.2.3 pre-entry earnings check from WARN to PASS. No shape change. |
| 0.1 | 2026-04-30 | Initial contract — ST-07 DS-04 |
