**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-27
**Cycle:** 2026-07-27__release-v7.9
**Backlog source:** BLG-FEAT-67
**Maps to:** EPIC-02, S2-02

---

# UX Spec — Historical Sector/Regime Exposure Trend

## 1. Problem

`SectorHeatMap` (`risk_dashboard.md` §8a, shipped v6.1 — not v6.2 as the backlog item's problem statement states; corrected below) and regime status displays (`dashboard.md` §Signal Status) show only the current point-in-time snapshot. There is no way to see whether sector concentration or regime exposure has been drifting over recent months.

## 2. Placement Correction (resolved at this design gate)

**Backlog item as filed states:** "trend chart added alongside the existing `SectorHeatMap` ... on the Positions or Reports page." This is factually incorrect against the shipped codebase — `SectorHeatMap` (`src/components/risk/SectorHeatMap.js`) is rendered on the **Risk Dashboard** page (`src/pages/RiskDashboard.js`, route `/risk`), specified at `risk_dashboard.md` §8a "Sector Concentration Heat Map". It does not appear on Positions or Reports.

**Decision:** place the new trend chart on the **Risk Dashboard** page, as a new §8b immediately following the existing §8a Sector Concentration Heat Map — this satisfies the item's actual intent ("alongside the existing SectorHeatMap") using the component's real location rather than the backlog text's stated one. Product Owner confirms this placement correction; no scope change beyond correcting the page reference — the AC's substance (a historical trend view of already-captured data) is unaffected.

## 3. Data

- **Backend:** aggregate existing `portfolio_history` rows plus the sector-weight data already computed for §8a (`GET /portfolio/sector-weights`) and regime data already computed for the Dashboard's Signal Status (`GET /market/status`) into a rolling time series — weekly buckets, consistent with the existing `portfolio_history` write cadence (nightly job, resampled weekly for the trend view to keep the chart readable over a multi-month window).
- **New endpoint:** `GET /portfolio/sector-regime-trend?weeks={N}` (default 12 weeks) — returns `{ weeks: [{ week_start, sectors: [{sector_name, exposure_pct}], regime_us, regime_uk }] }`. No new inputs — purely a historical view of data already captured by existing nightly jobs.
- **API contract:** new entry required in `docs/specs/api_contracts/portfolio_endpoints.md` (or `analytics_endpoints.md`) and `docs/reference/openapi.yaml` in the same commit as implementation (CLAUDE.md non-negotiable).

## 4. Layout

**Section heading:** "Sector & Regime Exposure Trend" — placed directly below the §8a Sector Concentration Heat Map's Section-Level Alert row, above §7 Prospective Heat Indicator (matches the existing page order: heat gauge → drawdown → grace panel → risk table → sector heat map → **[new] exposure trend** → prospective heat indicator).

Two stacked charts, full width:

1. **Sector concentration trend** — stacked area or multi-line chart, one series per sector (top 5 by current exposure; remainder grouped as "Other"), X-axis = week, Y-axis = exposure %. Legend below chart, wraps on narrow screens.
2. **Regime status trend** — dual-row timeline strip (one row for US, one for UK) directly beneath the sector chart, same X-axis (week) for visual alignment. Each week cell: green fill = regime on, amber fill = regime off (same colour convention as the existing Signal Status regime badges, `dashboard.md` §Signal Status).

## 5. Insufficient-History State (AC-03)

When fewer than 8 weeks of `portfolio_history` data exist: render a single inline notice in place of both charts — "Not enough history yet to show a trend (8 weeks of data required; N available)." No partial/truncated chart is shown — an 8-week minimum keeps the chart legible and avoids a near-empty, misleading plot.

## 6. States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton chart placeholder (matches §8a's existing skeleton tile grid convention) |
| Loaded, ≥8 weeks | Both charts render as above |
| Loaded, <8 weeks | Insufficient-history notice (§5) |
| Error | "Unable to load exposure trend." + Retry — does not affect other Risk Dashboard panels (matches §8a's existing error-isolation convention) |

## 7. Compliance Check

No conflict with `strategy_rules.md §13` — display-only historical view of already-captured, already-displayed data (current sector exposure already shown in §8a; current regime already shown on Dashboard). No new computation, prediction, or recommendation.

## 8. Out of Scope

- Any change to §8a's current-snapshot heat map itself (untouched)
- Any change to Dashboard's current-snapshot Signal Status display (untouched)
- Configurable bucket size (fixed weekly this cycle) or configurable lookback window beyond the default 12 weeks

## 9. Sign-off

- **Head of UX & Design:** Approved — 2026-07-27 (including the §2 placement correction)
- **Product Owner:** Approved — 2026-07-27 (confirms placement correction; no AC change)
