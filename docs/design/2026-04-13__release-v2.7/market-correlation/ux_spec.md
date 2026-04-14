**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-04-14
**Cycle:** 2026-04-13__release-v2.7
**Story:** ST-08 — Market Correlation Analysis (BLG-FEAT-17)
**Approved by:** Product Owner

---

# UX Specification — Market Correlation Analysis

## Feature Summary

A new section on the Performance Analytics page displaying per-position and portfolio-level Pearson correlation coefficients versus a market benchmark (SPY for US positions, FTSE for UK positions). Computed over a 252-day default lookback. Results are cached server-side with a TTL of at least one trading day.

---

## Page Placement

Rendered as a new section **§18 — Market Correlation** on the Analytics page, inserted after §17 Discipline & Compliance in the Component Rendering Order.

Section is visible when `has_enough_data = true` and the user has at least one open position.

---

## API Dependency

**Endpoint:** `GET /analytics/market-correlation`

**Query parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `lookback_days` | `252` | Historical lookback window in trading days |

**Response shape (expected):**

```json
{
  "positions": [
    {
      "ticker": "AAPL",
      "market": "US",
      "benchmark": "SPY",
      "correlation": 0.74,
      "severity": "high"
    }
  ],
  "portfolio_average": {
    "weighted_correlation": 0.61,
    "severity": "moderate"
  },
  "lookback_days": 252,
  "cached_at": "<ISO-8601>"
}
```

The frontend must not compute correlation values. All values sourced from backend.

---

## Layout

Section header: **"Market Correlation"**

Sub-header line (muted text): "Pearson correlation vs. benchmark over [lookback_days]-day lookback. Cached daily."

### Correlation Table

A table with one row per open position, sorted by correlation descending (highest first).

**Columns:**

| Column | Source field | Format |
|--------|-------------|--------|
| Ticker | `positions[].ticker` | Uppercase, monospace |
| Market | `positions[].market` | "US" / "UK" |
| Benchmark | `positions[].benchmark` | "SPY" / "FTSE" |
| Correlation | `positions[].correlation` | 2 decimal places (e.g. `0.74`) |
| Severity | `positions[].severity` | Colour-coded badge (see below) |

**Portfolio Average row:**

A visually distinct summary row rendered below the position rows (separated by a full-width divider):

| Column | Value |
|--------|-------|
| Ticker | "Portfolio Average" (italic, muted) |
| Market | — |
| Benchmark | — |
| Correlation | `portfolio_average.weighted_correlation` (2dp) |
| Severity | Colour-coded badge |

---

## Severity Colour Coding

| Severity | Threshold | Badge colour |
|----------|-----------|-------------|
| `high` | correlation > 0.7 | Rose-500 background, white text |
| `moderate` | 0.3 ≤ correlation ≤ 0.7 | Amber-400 background, dark text |
| `low` | correlation < 0.3 | Emerald-500 background, white text |

Severity is determined server-side and returned in the `severity` field. The frontend applies the badge colour based on the `severity` string — it does not re-evaluate the threshold.

---

## Lookback Control

A compact integer input (label: "Lookback (days)") rendered in the section header row (right-aligned). Default: `252`. Minimum: `30`.

- On change: 500ms debounce, then re-fetch `GET /analytics/market-correlation?lookback_days={value}`.
- Invalid input (non-positive, non-integer): resets to `252`.
- Loading indicator shown during fetch.

---

## States

| State | Display |
|-------|---------|
| Loading | Skeleton table rows (3 rows) |
| Loaded | Full table with position rows and portfolio average row |
| No open positions | Muted message: "No open positions to correlate." Section still renders with header. |
| Error (non-500) | Section-level error card: "Correlation data unavailable. [error message from API]" |
| Cached data served on error | If `cached_at` is present in error response: show "Last known data as of [date]" below error message |
| No data / Yahoo Finance unavailable | Graceful error card — not a 500. Same error card as above. |

---

## Interaction Notes

- Correlation values in the table are read-only — no click interaction.
- The portfolio average row is not clickable.
- Table supports horizontal scroll on narrow viewports.

---

## Constraints

- No historical correlation time-series is shown — point-in-time only.
- The frontend must not cache or persist correlation data locally.
- If Yahoo Finance is unavailable, the section shows the error state with cached data if available — it must not cause a page-level error.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-14 | Initial UX spec. ST-08 / BLG-FEAT-17. Design gate: 2026-04-13__release-v2.7. |
