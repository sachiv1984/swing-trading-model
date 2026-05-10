**Owner:** Head of Specs Team
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-10
**Story:** ST-08 (EPIC-03, v3.3) — BLG-SPEC-26
**Cross-reference:** `docs/specs/api_contracts/research_endpoint.md`
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Data Source Provenance — Research View

This document specifies the data source, retrieval behaviour, timestamp display, and source attribution requirements for each data field in the Research View (`GET /research/{ticker}`).

---

## 1. Field-Level Provenance

### 1.1 Price Data

| Field | API field | Source | Attribution label | Timestamp display |
|-------|-----------|--------|-------------------|-------------------|
| Current price | `data.price` | Yahoo Finance (v8 chart API) | "Yahoo Finance" | Retrieval time shown as "Updated {HH:MM}" beside the price |
| Daily change % | `data.price_change_pct` | Yahoo Finance (v8 chart API) | "Yahoo Finance" | Same timestamp as price |
| Market cap | `data.market_cap` | yfinance.Ticker.info | "Yahoo Finance" | Same timestamp as price |

**Staleness policy:** Price data is fetched live on each `GET /research/{ticker}` call. There is no server-side cache. Display timestamp is the time the frontend received the response.

### 1.2 Signal Data

| Field | API field | Source | Attribution label | Timestamp display |
|-------|-----------|--------|-------------------|-------------------|
| Signal details | `data.signal` | Internal signals table (PostgreSQL) | "Screener" | Signal date from `signal_date` field shown as "Signal: {YYYY-MM-DD}" |

**Staleness policy:** Signals are written by the screener run (`POST /screener/run`). A signal shown on the research view reflects the last screener run that included this ticker. `latest_run_timestamp` from `screener` object should be displayed when available.

### 1.3 Market Regime

| Field | API field | Source | Attribution label | Timestamp display |
|-------|-----------|--------|-------------------|-------------------|
| Regime label | `data.regime.label` | SPY/FTSE-100 200-day MA check via yfinance | "Live" | No explicit timestamp — regime is recalculated on each API call |

**Display:** Label only: "Risk On", "Risk Off", or "Mixed". No numeric values shown. Attribution displayed as small badge or icon tooltip: "Source: Live market data".

### 1.4 Sector / Industry

| Field | API field | Source | Attribution label | Timestamp display |
|-------|-----------|--------|-------------------|-------------------|
| Sector | `data.sector.sector` | Yahoo Finance (yfinance.Ticker.info) | "Yahoo Finance" | No timestamp — classification data; not price-sensitive |
| Industry | `data.sector.industry` | Yahoo Finance (yfinance.Ticker.info) | "Yahoo Finance" | No timestamp |

**Null handling:** Many UK-listed tickers do not have sector/industry in Yahoo Finance. Display as "—" (em dash) when null.

### 1.5 Screener Data

| Field | API field | Source | Attribution label | Timestamp display |
|-------|-----------|--------|-------------------|-------------------|
| Screener presence | `data.screener.in_latest_results` | Internal screener results cache | "Screener" | Run timestamp from `latest_run_timestamp` shown as "Last run: {relative time}" |
| Score | `data.screener.score` | Internal screener results cache | "Screener" | Same timestamp as above |
| ATR% | `data.screener.atr_pct` | Internal screener results cache | "Screener" | Same timestamp as above |

### 1.6 Earnings

| Field | API field | Source | Attribution label | Timestamp display |
|-------|-----------|--------|-------------------|-------------------|
| Next earnings date | `data.earnings.next_earnings_date` | yfinance earnings calendar | "Yahoo Finance" | No timestamp — date data only |
| Days until earnings | `data.earnings.days_until_earnings` | Calculated from next_earnings_date | "Calculated" | Recalculated on each view load |

**Staleness policy:** Earnings dates may lag by 1–2 weeks if yfinance hasn't updated. Display raw date from API; do not attempt freshness indication for earnings data.

### 1.7 News Headlines

| Field | API field | Source | Attribution label | Timestamp display |
|-------|-----------|--------|-------------------|-------------------|
| Headlines | `data.news_headlines` | News service (Alpaca or fallback) | Per headline `source` field | `published_at` shown as relative time (e.g. "3h ago") per article |

---

## 2. Attribution Display Format

### 2.1 Canonical Format

Source attribution is displayed as a small muted label beneath or adjacent to each data section:

```
Source: {source name}  ·  Updated {HH:MM}
```

For sections without a meaningful timestamp (sector, industry), omit the timestamp portion:

```
Source: Yahoo Finance
```

### 2.2 Placement

| Section | Placement |
|---------|-----------|
| Price panel | Beneath the price figure, right-aligned |
| Signal panel | Below the signal status badge |
| Regime badge | Tooltip on hover: "Source: Live market data" |
| Sector/Industry | Below the sector chip, muted text |
| Screener panel | Below the score, with run timestamp |
| Earnings panel | Below the date, no timestamp |
| News panel | Per article: source name as muted text beside publication time |

### 2.3 Visual Format

- Attribution text: `text-xs text-slate-400` (or equivalent muted style)
- Format: plain text, no icon required (icon optional — see UX spec)
- Null/missing attribution: omit the attribution line entirely; do not show "Source: Unknown"

---

## 3. Retrieval Timestamp Policy

- **Display granularity:** HH:MM in the user's local timezone
- **Source:** Frontend records the time the API response was received
- **Not a server timestamp:** The backend does not return a `retrieved_at` field. The frontend shows the time the data arrived in the browser
- **Staleness threshold:** If the research view has been open for > 5 minutes without a refresh, show a staleness indicator: "(stale)" or a refresh prompt. Threshold configurable; 5 minutes is the default

---

## 4. Source Failure Display

When a field is `null` due to source failure:

| Section | Null display |
|---------|-------------|
| Price | `—` with tooltip "Price unavailable" |
| Market cap | `—` |
| Signal | "No signal on file" |
| Regime | "Regime unavailable" label |
| Sector / Industry | `—` |
| Screener | "Not in latest screener results" |
| Earnings | "No upcoming earnings data" |
| News | "No recent news" (empty state) |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-10 | Initial creation — ST-08 (EPIC-03, v3.3). Per-field source attribution, timestamp display policy, failure display. |
