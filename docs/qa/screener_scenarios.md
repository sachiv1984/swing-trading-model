**Owner:** QA & Testing Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-30
**Cycle:** 2026-04-29__release-v3.1 (ST-10)

---

# Screener Scenario Library

## Purpose

This library defines structured test scenarios for the Momentum Screener. Each scenario specifies the filter inputs, expected behaviour, and pass/fail criteria. Use this library for manual QA runs and as the reference for future automation.

Related protocol: `docs/qa/screener_accuracy_protocol.md` (ST-09)

---

## Scenarios

### SCN-01 — Normal results (mixed UK/US)

| Field | Value |
|-------|-------|
| Name | Normal results — mixed UK/US |
| Filters | Default filters (ATR ≥1%, signal score ≥0.4, all sectors, both markets) |
| Expected behaviour | Results returned for both UK and US tickers; UK tickers displayed without `.L` suffix; market badges show "UK" and "US" correctly |
| Pass criteria | ≥1 UK result; ≥1 US result; no `.L` visible in ticker column; market badges present |

---

### SCN-02 — Zero results (all filters too tight)

| Field | Value |
|-------|-------|
| Name | Zero results — filters too restrictive |
| Filters | ATR ≥ 50%, signal score ≥ 0.99, sector = "Uncategorised" |
| Expected behaviour | No results returned; screener displays "No tickers match your current filters" message; no crash; no spinner stuck |
| Pass criteria | Empty state message visible; no JS error; page remains functional; subsequent filter relaxation returns results |

---

### SCN-03 — Maximum results (all filters open)

| Field | Value |
|-------|-------|
| Name | Maximum results — all filters open |
| Filters | ATR ≥ 0%, signal score ≥ 0.0, all sectors, both markets, all regimes |
| Expected behaviour | All available screener results returned (up to configured limit); page renders without performance degradation; scroll works |
| Pass criteria | Results count matches `GET /screener/results` total_count; no layout overflow; table scrolls |

---

### SCN-04 — Single-sector sweep

| Field | Value |
|-------|-------|
| Name | Single sector filter |
| Filters | Sector = "Technology"; all other filters default |
| Expected behaviour | Only tickers with sector = "Technology" appear in results |
| Pass criteria | All returned tickers have sector badge "Technology"; no tickers from other sectors visible |

---

### SCN-05 — Conflicting filter combinations

| Field | Value |
|-------|-------|
| Name | Conflicting filters — regime gate conflict |
| Filters | Market = US only; regime = Risk-Off only; all ATR/signal defaults |
| Expected behaviour | If regime is currently Risk-On for US market, results return 0 tickers in Risk-Off filter; or vice versa; no crash |
| Pass criteria | Results consistent with live regime status from `GET /health/detailed`; no error state; zero-result message shown if applicable |

---

### SCN-06 — Ticker with missing data

| Field | Value |
|-------|-------|
| Name | Missing data graceful handling |
| Filters | Default filters |
| Expected behaviour | Tickers with missing ATR, sector, or price data are excluded from results or shown with N/A where appropriate; no crash |
| Pass criteria | No blank/broken cells; no JS errors; affected tickers either absent or display "—" in missing fields |

---

### SCN-07 — UK-only market filter

| Field | Value |
|-------|-------|
| Name | UK-only market filter |
| Filters | Market = UK only; all other filters default |
| Expected behaviour | Only UK tickers returned; all displayed without `.L` suffix; Market badge = "UK" for all rows |
| Pass criteria | No US tickers in results; no `.L` in ticker column; market badge = UK for all |

---

### SCN-08 — US-only market filter

| Field | Value |
|-------|-------|
| Name | US-only market filter |
| Filters | Market = US only; all other filters default |
| Expected behaviour | Only US tickers returned; Market badge = "US" for all rows |
| Pass criteria | No UK tickers in results; market badge = US for all |

---

### SCN-09 — Watchlist promotion from screener results

| Field | Value |
|-------|-------|
| Name | Watchlist promotion — UK ticker |
| Filters | Market = UK; select any UK result for watchlist promotion |
| Expected behaviour | Popover shows ticker without `.L`; POST to `/watchlist` sends ticker without `.L`; "Added" indicator appears after success |
| Pass criteria | Header shows ticker without `.L`; network request body confirms ticker without `.L`; "Added" checkmark appears |

---

### SCN-10 — Screener re-run triggers fresh data

| Field | Value |
|-------|-------|
| Name | Re-run produces fresh results |
| Filters | Default filters |
| Expected behaviour | Clicking "Run Screener" / triggering a new run posts to `POST /screener/run`; results table refreshes; `last_run_at` timestamp updates |
| Pass criteria | `last_run_at` in results is newer than previous run; at least one result returned (market hours); no stale-cache display |

---

## Maintenance

Add new scenarios when:
- A new filter parameter is added to the screener
- A new failure mode is identified in production
- A new market or ticker type is introduced

Each scenario must include name, filters, expected behaviour, and pass criteria. QA & Testing Owner approves additions.

---

## Acceptance

- Accepted by: QA & Testing Owner
- Date: 2026-04-30
