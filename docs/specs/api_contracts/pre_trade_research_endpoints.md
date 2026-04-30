# API Contract — Pre-Trade Research Endpoints

**Version:** v0.1
**Status:** Published
**Owner:** API Contracts Documentation Owner
**Last Updated:** 2026-04-30

---

## GET /research/{ticker}

Returns an aggregated pre-trade research snapshot for a given ticker. Combines
signal data, market regime, sector classification, screener presence, and
(where available) earnings proximity into a single response object for use
in the Pre-Trade Research View.

All fields are best-effort. Where a data source is unavailable or returns an
error the corresponding field is `null` — the endpoint never returns a
non-2xx status due to a missing sub-source.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | Yes | Ticker symbol (e.g. `AAPL`, `BARC.L`) |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `market` | string | `"US"` | Market code: `US` or `UK` |

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "ticker": "AAPL",
    "market": "US",
    "signal": {
      "signal_id": "uuid",
      "direction": "long",
      "signal_date": "2026-04-28",
      "status": "active",
      "rank": 1,
      "atr": 2.45,
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
      "latest_run_timestamp": "2026-04-30T06:00:00Z",
      "score": 87.5,
      "atr_pct": 1.38
    },
    "earnings": {
      "next_earnings_date": "2026-07-25",
      "days_until_earnings": 86,
      "fiscal_quarter": "Q3 2026",
      "data_source": "yfinance"
    }
  }
}
```

### Null field examples

Fields are `null` when the sub-source is unavailable:

- `signal: null` — no active signal found for this ticker
- `screener: null` — no screener run has completed, or ticker not in universe
- `earnings: null` — earnings service unavailable or data not returned
- `sector: { "sector": null, "industry": null }` — yfinance did not return sector data

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `signal` | object \| null | Most recent active or queued signal for this ticker; null if none |
| `signal.direction` | string | `"long"` or `"short"` |
| `signal.status` | string | Signal status (e.g. `active`, `pending`, `closed`) |
| `signal.r_target` | number \| null | R-multiple target if set |
| `regime` | object \| null | Current market regime; null if market status check fails |
| `regime.label` | string | `"risk_on"`, `"risk_off"`, or `"mixed"` |
| `sector` | object | Sector/industry classification; individual fields may be null |
| `screener` | object \| null | Most recent screener result for this ticker; null if not present |
| `screener.in_latest_results` | bool | True if ticker appeared in the most recent screener run |
| `screener.score` | number \| null | Composite score from screener engine |
| `earnings` | object \| null | Upcoming earnings data; null if service unavailable |
| `earnings.days_until_earnings` | integer \| null | Calendar days until next earnings date |

### Error Responses

| Status | Condition |
|--------|-----------|
| 500 | Unexpected server error (all sub-source failures return 200 with null fields) |

---

## Sign-off

| Role | Signature | Date |
|------|-----------|------|
| API Contracts Documentation Owner | Sprint Execution Engine | 2026-04-30 |
| Head of Specs Team | Sprint Execution Engine | 2026-04-30 |
