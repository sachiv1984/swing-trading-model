**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-17
**Cycle:** 2026-04-17__release-v2.8
**Story:** ST-01 (EPIC-01)
**Approved by:** Product Owner — 2026-04-17

---

# UX Spec — Market Correlation View (ST-01)

## Data Source

`GET /analytics/market-correlation`

Per-position Pearson correlation coefficients + severity classifications + portfolio-level weighted average.
Canonical spec: `docs/specs/api_contracts/analytics_endpoints.md v2.1.0`

---

## Page Placement

**Page:** Performance Analytics (`/analytics`)

**Section position:** §18 — appended after §17 Discipline & Compliance in the rendering order. No existing sections reordered.

**Section title:** "Market Correlation"

---

## Component Layout

### Portfolio-Level Summary (above table)

A single metric card or summary strip at the top of the section showing:

| Element | Source | Display |
|---------|--------|---------|
| Portfolio Weighted Average | `portfolio_weighted_avg_correlation` | Numerical value (2dp) + severity badge |
| Severity badge | `portfolio_correlation_severity` | Colour-coded pill (see severity colours below) |
| Interpretation hint | Static text | e.g. "high correlation signals clustered risk" |

The portfolio metric renders even if all per-position values are null (backend handles partial results).

### Per-Position Table (below summary)

A table with one row per position:

| Column | Source field | Format |
|--------|-------------|--------|
| Ticker | `symbol` | Uppercase |
| Correlation | `pearson_correlation` | Numerical, 2dp (e.g. `0.82`) — "N/A" if null |
| Severity | `severity` | Colour-coded severity badge |
| vs. Market | `benchmark_symbol` | Ticker label (e.g. "SPY") |

Default sort: severity descending (high → moderate → low → N/A last).

---

## Severity Colour Scheme

Consistent with existing risk severity indicators in `risk_dashboard.md`:

| Severity | Colour token | Display |
|----------|-------------|---------|
| `high` | Rose-500 | Red badge |
| `moderate` | Amber-500 | Amber badge |
| `low` | Emerald-500 | Green badge |
| null (N/A) | Slate-500 | Muted grey, no badge — "N/A" text |

---

## Null / Partial Handling

- Position with `pearson_correlation: null` → display "N/A" in correlation cell; no severity badge; row renders at bottom of table (after sorted results).
- Portfolio summary with all nulls → show portfolio metric as "N/A"; table section still renders.

---

## States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton rows (consistent with §15 Cohort Analysis) |
| Loaded | Full table + summary card |
| No positions | "No open positions to correlate." (muted message; no table) |
| Error | Section-level error card (consistent with §15/§16/§17 pattern) |

---

## Hard Rules

- All values sourced from backend. No client-side correlation computation.
- Section does NOT render when `has_enough_data = false` (consistent with other analytics components).
- This section uses the Analytics page's 8h cache TTL — no separate cache control.

---

## Product Owner Approval

Approved: Product Owner — 2026-04-17
Design is consistent with existing analytics page patterns. Analytics page placement confirmed (not Portfolio page).
