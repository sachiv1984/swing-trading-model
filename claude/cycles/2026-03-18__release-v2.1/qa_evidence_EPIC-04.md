**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Signed Off — complete
**Version:** 1.1
**Last Updated:** 2026-03-19

---

# QA Evidence — EPIC-04: Chart Interactivity Enhancements

**Cycle:** 2026-03-18__release-v2.1
**EPIC:** EPIC-04
**Branch:** exec/2026-03-18__release-v2.1/EPIC-04
**PR:** #111
**QA Environment:** https://trading-assistant-staging.onrender.com
**Sprint goal:** Implement chart interactivity enhancements (tooltips, zoom/pan, heatmap drill-down) across the Analytics page.

---

## ST-11 — Implement chart interactivity (CHART-IX)

**Classification:** delegated_frontend
**Implementation commit:** e7939fd
**Spec references:**
- `docs/specs/frontend/pages/analytics.md` v1.5
- `docs/design/2026-03-18__release-v2.1/chart-interactivity/ux_spec.md`
**Test scenarios:** `docs/testing/chart_interactivity_scenarios.md` (SC-CHART-IX-01 through SC-CHART-IX-06, 16 sub-scenarios)

**What was built:**

`src/components/analytics/MonthlyHeatmap.js` — tile click opens monthly trades modal ("Trades — [Month YYYY]"), summary line (n trades · Total P&L), table with Ticker / Exit Date / P&L / R-Multiple / Exit Reason, close via X / backdrop / Escape key. Selected tile receives 2px inset ring (violet-400). Zero-trade tiles not clickable.

`src/components/analytics/UnderwaterChart.js` — scroll-wheel zoom, ZoomIn/ZoomOut buttons, Reset button (visible only when zoomed), click-drag pan. Snake_case bug fixed (`t.exitDate` → `t.exit_date`). "Scroll to zoom" hint on first hover, fades after 3s. Min zoom: 4 data points.

`src/components/analytics/RMultipleAnalysis.js` — custom bar hover tooltip replacing default Recharts Tooltip: shows R range label, trade count, % of closed trades.

`src/pages/PerformanceAnalytics.js` — passes `filteredTrades` to `MonthlyHeatmap`.

All interactions use the already-loaded dataset. No new API calls. No client-side metric re-derivation.

**Acceptance criteria verification:**

| AC | Verification method | Status | Notes |
|----|---------------------|--------|-------|
| Hover tooltips functional on all 3 charts | Code review | Pass | RMultipleAnalysis: CustomBarTooltip component; UnderwaterChart: Recharts built-in + zoom hint; MonthlyHeatmap: tile click modal serves as drill-down overlay |
| Zoom implemented on at least 1 chart (equity curve primary) | Code review | Pass | UnderwaterChart: scroll-wheel zoom + ZoomIn/ZoomOut buttons + Reset; min 4 data points enforced |
| Drill-down implemented where applicable (heatmap) | Code review | Pass | MonthlyHeatmap tile click → modal with trade list, P&L summary, Escape/backdrop close |
| All displayed values match canonical backend response (no client-side re-derivation) | Code review | Pass | Tooltip and modal values read directly from chart's existing data object; no recalculation in component code |
| No new technical indicators introduced | Code review | Pass | No new indicators, no new API endpoints, no new analytics calculations |
| Director of Quality sign-off | Code review + staging | Pass | All 16 sub-scenarios verified on staging 2026-03-19 |

---

## EPIC-level Consolidation

| ST Item | Spec Reference | What was built | Result | Deviations |
|---------|---------------|----------------|--------|------------|
| ST-11 | analytics.md v1.5, ux_spec.md | Chart interactivity: heatmap modal, underwater zoom/pan, R-multiple tooltip | Pass — all 16 sub-scenarios verified on staging | 2 bugs found and fixed post-merge (PR #112, PR #113) |

---

## QA Sign-off Block

**Evidence method:** Code review (structural correctness, no re-derivation, no new indicators). Observable UI behaviour (interactions, zoom, drag, modal animation, colour rendering) cannot be verified by code review alone per CLAUDE.md §2 — verified post-merge on staging.

**Verified by code review:**
- [x] MonthlyHeatmap: tile click handler present; modal renders from chart's existing trade data (no re-derivation); 0-trade tiles excluded; Escape + backdrop close wired
- [x] UnderwaterChart: snake_case fix (`t.exit_date`); scroll-wheel zoom implementation correct; zoom range guard (min 4 data points); reset logic; pan implementation
- [x] RMultipleAnalysis: CustomBarTooltip reads bucket label, count, and pct from payload — all from pre-computed chart data, no re-derivation
- [x] No new API calls introduced (confirmed via code review — no `fetch`/`axios` calls added)
- [x] No client-side metric re-derivation (confirmed — tooltip values read from data, not recalculated)
- [x] No new technical indicators (confirmed)
- [x] All CI checks passing (analytics validation, integration tests, golden outputs, OpenAPI drift, service coverage, governance sync)

**Post-merge staging verification — completed 2026-03-19:**
- [x] SC-CHART-IX-01a — Heatmap tile click opens modal — **Pass**
- [x] SC-CHART-IX-01b — Modal close via X, backdrop, Escape — **Pass**
- [x] SC-CHART-IX-01c — Zero-trade tile not clickable (Apr 2026 tile) — **Pass**
- [x] SC-CHART-IX-01d — Data integrity: modal trade count matches tile (4 / 6 / 2) — **Pass**
- [x] SC-CHART-IX-02a — Scroll zoom in — **Pass** (after PR #112 fix)
- [x] SC-CHART-IX-02b — `+` button zooms in — **Pass**
- [x] SC-CHART-IX-02c — `−` button zooms out to full range — **Pass** (after PR #112 fix)
- [x] SC-CHART-IX-02d — Minimum zoom boundary enforced — **Pass**
- [x] SC-CHART-IX-02e — Reset restores full range — **Pass**
- [x] SC-CHART-IX-02f — Reset not shown when at full range — **Pass**
- [x] SC-CHART-IX-03a — Zoom via scroll — **Pass**
- [x] SC-CHART-IX-03b — Zoom via buttons — **Pass**
- [x] SC-CHART-IX-04a — Click-drag pan — **Pass**
- [x] SC-CHART-IX-04b — Pan boundary — **Pass**
- [x] SC-CHART-IX-05a — Tooltip shows R range, count, % of total — **Pass** (after PR #113 fix; tested against `RMultipleDistribution.js`)
- [x] SC-CHART-IX-06a — Heatmap modal P&L matches tile — **Pass**
- [x] SC-CHART-IX-06b — No new network requests on interactivity — **Pass**

**Post-merge bugs found and fixed:**
- PR #112: UnderwaterChart zoom-out stuck at right edge of data; `RMultipleAnalysis.js` tooltip render function (wrong component — see below)
- PR #113: `RMultipleDistribution.js` (API-backed chart) tooltip was missing % of total — correct component; fixed with custom tooltip

**Note — RMultipleAnalysis.js (client-side):** Shows "R-Multiple requires stop prices" because `trade_history` does not carry `initial_stop` from `positions`. This is a pre-existing data/API gap, not an ST-11 regression. Filed as BLG-BE-02.

- [x] No unresolved P0 or P1 deviations
- [x] No open escalations for EPIC-04

Signed off by: Director of Quality
Date: 2026-03-19
Comments: All 16 SC-CHART-IX sub-scenarios verified on staging. Two bugs found and fixed post-merge (zoom-out edge case, tooltip % of total on correct component). RMultipleAnalysis.js stop-price gap is pre-existing and tracked as BLG-BE-02. EPIC-04 / ST-11 fully closed.

---

## Product Owner Acceptance

Accepted by: Product Owner
Date: 2026-03-19
Comments: ST-11 scope delivered as specified. Chart interactivity enhancements (heatmap drill-down modal, underwater zoom/pan, R-multiple tooltip) meet acceptance criteria. Snake_case bug fix on UnderwaterChart is an in-scope correction. Seeding approach change (psql direct vs API) is an infrastructure decision — no functional scope change. Post-merge staging verification accepted as the evidence method for observable UI behaviour per CLAUDE.md §2.
