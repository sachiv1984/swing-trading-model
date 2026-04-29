**Version:** 1.0
**Date:** 2026-04-29
**Author:** Head of UX & Design
**Approved by:** Product Owner — 2026-04-29
**Story:** ST-08 — Earnings Calendar frontend (DS-04)
**Design gate:** 2026-04-29__release-v3.1

---

# UX Decision Record — Earnings Calendar Frontend (ST-08)

## Purpose

Surface upcoming earnings dates for tickers across three existing pages: Screener Results, Watchlist, and Open Positions. The goal is to give the user early visibility of earnings proximity so they can make informed entry/exit decisions.

Data source: `GET /earnings/{ticker}` — returns `{ ticker, next_earnings_date, days_until_earnings, fiscal_quarter, data_source }` or null if unavailable.

---

## Screener Results Page — New Earnings Column

### Placement

New column added to the screener results table between the **Sector** and **Entry Zone** columns.

Updated column order:
Ticker | Market | Price | ATR | Regime | Signal | Sector | **Earnings** | Entry Zone | News

### Display Format

| Condition | Display | Style |
|-----------|---------|-------|
| `days_until_earnings` ≤ 5 | `{N}d` | Red badge — earnings imminent |
| `days_until_earnings` 6–30 | `{N}d` | Amber badge — earnings approaching |
| `days_until_earnings` > 30 | `—` | Em dash (muted) — not near term |
| Data unavailable (`null` response) | `—` | Em dash (muted) |

- Badge format: compact pill, e.g. `5d`, `12d`.
- The `—` (em dash) for distant or unavailable earnings must not show as an empty cell or zero — always render the dash.
- Responsive behaviour: on narrow viewport, the Earnings column collapses along with Sector and Entry Zone (same breakpoint rule as existing hidden columns).

### Tooltip

On hover over an Earnings badge: show tooltip with `"Next earnings: {fiscal_quarter} — {next_earnings_date}"` (ISO date format). If data unavailable: no tooltip.

---

## Watchlist Page — Earnings Column

### Placement

New **Earnings** column added to the Watchlist Table, between **Stop (Current)** and **Actions**.

Updated columns:
Ticker | Market | Entry Signal | Target Entry | Stop (Initial) | Stop (Current) | **Earnings** | Actions

### Display Format

Same badge logic as screener:
| Condition | Display | Style |
|-----------|---------|-------|
| `days_until_earnings` ≤ 5 | `{N}d` | Red badge |
| `days_until_earnings` 6–30 | `{N}d` | Amber badge |
| `days_until_earnings` > 30 | `—` | Em dash (muted) |
| Data unavailable | `—` | Em dash (muted) |

- Data is fetched per ticker via `GET /earnings/{ticker}`. Requests are made in parallel for all watchlist tickers on page load; failures are handled gracefully (display `—`).

---

## Positions Page — Earnings Proximity Warning (Table View)

### Placement

Earnings proximity is displayed as an **inline badge within the Ticker cell** in the Table View only. The badge appears below the ticker symbol on a second line within the same cell.

Example cell content:
```
BARC
[EPS 3d]
```

- Grid View and Journal View: earnings data is not shown (out of scope for v3.1).

### Display Format

| Condition | Display | Style |
|-----------|---------|-------|
| `days_until_earnings` ≤ 5 | `EPS {N}d` | Red badge — proximity warning |
| `days_until_earnings` 6–7 | `EPS {N}d` | Amber badge — approaching |
| `days_until_earnings` > 7 | Not shown | No badge displayed |
| Data unavailable | Not shown | No badge displayed |

- The badge is display-only. No action or modal is triggered by clicking it.
- Rationale for 7-day threshold: within one week of earnings, the user may want to review their position. The 5-day threshold is the hard "warning" level per the AC; 6–7 days is an advisory level.

---

## Null / Unavailable Handling (All Pages)

- If `GET /earnings/{ticker}` returns null or errors: display `—` (screener/watchlist) or show nothing (positions). Never show a broken display or empty column.
- Earnings data may not be available for all tickers, particularly newer listings or non-standard reporting schedules. The `—` state is the expected default for a portion of tickers.

---

## API Notes

- Screener results: the screener batch endpoint may return earnings data inline (if ST-07 backend includes it in the screener response). If not, front-end fetches `GET /earnings/{ticker}` per result row. Confirm with backend at ST-08 implementation time.
- Watchlist: fetch per ticker on page load (parallel).
- Positions: fetch per open position on page load (parallel).

---

## Spec Updates Required

- `docs/specs/frontend/pages/screener_results.md` §4: add Earnings column specification
- `docs/specs/frontend/pages/watchlist.md`: add Earnings column to Watchlist Table
- `docs/specs/frontend/pages/positions.md`: add Earnings proximity warning to Table View §
