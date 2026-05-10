**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-10
**Story:** ST-09 (EPIC-03, v3.3) — BLG-SPEC-24
**§13 Compliance:** Confirmed — display-only. No automated recommendation generated. See §8.
**API contract:** docs/specs/api_contracts/research_endpoint.md
**Data provenance:** docs/specs/data_provenance/research_view_provenance.md
**UX spec:** docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md
**Design Source:** docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# research_view.md — Research View

**Purpose:** The Research View (`/research/:ticker`) provides an aggregated pre-trade research snapshot for a single ticker. It consolidates price data, signal information, market regime, sector, screener presence, earnings proximity, and recent news into a single page for pre-entry review.

Shipped in v3.1 (PT-02). Spec formalised in v3.3 (ST-09, EPIC-03).

---

## 1. Purpose and User Goals

Users should be able to:

- Review all available pre-trade research for a given ticker on one page
- Assess market regime context before placing an entry
- See whether the ticker is currently in the screener results
- View upcoming earnings risk
- Read recent news headlines
- Navigate directly to create or view a trade plan for the ticker

---

## 2. Navigation and Routes

| Route | Purpose |
|-------|---------|
| `/research/:ticker` | Research view for the given ticker |
| `/research/:ticker?market=UK` | Research view with explicit market (optional) |

- Accessible from: Screener results ("Research" link), Watchlist ("Research" link), Trade Plan form ("Review research →" link)
- Page title: **"{TICKER} — Research"**

---

## 3. API Reference

| Endpoint | Purpose |
|----------|---------|
| `GET /research/{ticker}` | Aggregated research data |
| `GET /trade-plans?ticker={ticker}` | Active trade plan for the ticker (if any) |
| `GET /portfolio/prospective-heat?ticker={ticker}&...` | Prospective portfolio heat for sizing context |

Canonical API contract: `docs/specs/api_contracts/research_endpoint.md`

---

## 4. Data Fields Displayed

### 4.1 Price Panel

| Field | Source | Format | Null display |
|-------|--------|--------|-------------|
| Current price | `data.price` | Currency symbol + 2dp (USD/GBP) | `—` |
| Daily change % | `data.price_change_pct` | `+1.42%` or `-0.83%` with colour | `—` |
| Market cap | `data.market_cap` | `$2.8T`, `£450M` (abbreviated) | `—` |
| Sector | `data.sector.sector` | Plain text | `—` |
| Industry | `data.sector.industry` | Plain text | `—` |

### 4.2 Signal Panel

Displayed only when `data.signal` is non-null.

| Field | Source | Format |
|-------|--------|--------|
| Signal status | `data.signal.status` | Coloured badge: Active (green), Watch (amber), others (grey) |
| Signal date | `data.signal.signal_date` | `"Signal: {YYYY-MM-DD}"` |
| ATR | `data.signal.atr` | `"{N} ATR"` |
| Entry price | `data.signal.entry_price` | Currency-formatted |
| Stop price | `data.signal.stop_price` | Currency-formatted |
| R-target | `data.signal.r_target` | `"{N}R"` |
| Rank | `data.signal.rank` | `"Rank #{N}"` |

When `data.signal` is null: display "No signal on file" placeholder.

### 4.3 Market Regime Panel

| Field | Source | Format |
|-------|--------|--------|
| Regime label | `data.regime.label` | Badge: "Risk On" (green), "Risk Off" (red), "Mixed" (amber) |
| SPY status | `data.regime.spy_risk_on` | Inline: "SPY ✓" or "SPY ✗" |
| FTSE status | `data.regime.ftse_risk_on` | Inline: "FTSE ✓" or "FTSE ✗" |

When `data.regime` is null: display "Regime unavailable".

### 4.4 Screener Panel

| State | Display |
|-------|---------|
| `data.screener` non-null | Score, ATR%, last run timestamp |
| `data.screener` null | "Not in latest screener results" |

### 4.5 Earnings Panel

| Field | Source | Format |
|-------|--------|--------|
| Next date | `data.earnings.next_earnings_date` | `"Earnings: {YYYY-MM-DD}"` |
| Days until | `data.earnings.days_until_earnings` | `"In {N} days"` |
| Fiscal quarter | `data.earnings.fiscal_quarter` | Plain text |

When `data.earnings` is null: display "No upcoming earnings data".

### 4.6 News Feed

- Up to 5 most recent headlines from `data.news_headlines`
- Each article: headline text (truncated to ~80 chars), source name, relative publication time
- Headline links to article URL (opens in new tab)
- Empty state: "No recent news for {ticker}"

### 4.7 Trade Plan Panel

- Fetched via `GET /trade-plans?ticker={ticker}`
- When active plan exists: shows plan status, stop level, R/R notes, and read-only pre-entry checklist
- When no plan: CTA button "Create Trade Plan" → navigates to `/trade-plans/new?ticker={ticker}`

---

## 5. Data Freshness Policy

| Data type | Max acceptable age | Staleness display |
|-----------|-------------------|--------------------|
| Price, change% | Live (fetched on page load) | Show "(stale)" after 5 min without refresh |
| Market cap | Live | Same as price |
| Regime | Live (recalculated on load) | No staleness indicator |
| Signal | From last screener run | Show screener run timestamp |
| Screener results | From last screener run | Show `latest_run_timestamp` |
| Earnings | Static (yfinance) | No staleness indicator |
| News | Live on load | No staleness indicator |

**Staleness indicator:** After 5 minutes on page without refresh, display a pill or notice: "Data may be stale — Refresh". Clicking triggers re-fetch.

---

## 6. Error States

| Scenario | Display |
|----------|---------|
| `GET /research/{ticker}` 500 | Full-page error: "Unable to load research data." + Retry button |
| Individual field null | Per-field null display per §4 |
| No price data | Price section shows `—` for all price fields |
| All fields null | Full-page degraded state: each section shows its null display; no error page |

---

## 7. Source Attribution

Per `docs/specs/data_provenance/research_view_provenance.md`:
- Each data section displays muted source attribution text beneath the section header
- Format: `Source: {source name} · Updated {HH:MM}` (where timestamp applies)
- Full attribution spec in provenance doc

---

## 8. §13 Compliance

This feature is **§13 compliant — display-only**:
- The system aggregates and presents data from multiple sources
- No automated recommendation, signal, or action is generated by the page itself
- Signal data (when present) originates from a prior screener run and is labelled accordingly
- The human reviews all displayed information and makes all decisions independently

---

## Known Deviations

None.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-10 | Initial creation — ST-09 (EPIC-03, v3.3). Formalises PT-02 (v3.1) shipped feature. Full data fields, freshness policy, error states, §13 confirmation, source attribution references. |
