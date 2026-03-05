Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# QA Evidence Log — EPIC-01: Risk Dashboard Page

**EPIC:** EPIC-01 — Risk Dashboard Page
**Cycle:** 2026-03-04__release-v1.8
**Sprint goal:** Ship a fully functional Risk Dashboard page giving the trader daily visibility into portfolio heat, drawdown, grace period status, and per-position risk.
**Test scenarios used:** `docs/testing/risk_dashboard_scenarios.md` v1.0.0 (created by ST-04, commit f261f0f)

---

## Per-Story Evidence

---

### ST-01 — Frontend Spec: Risk Dashboard Page

**Spec references:** `docs/specs/frontend/pages/risk_dashboard.md` v0.1.0

**Status:** ✅ COMPLETE — Delivered at Design Gate 2026-03-04. Spec locked at v0.1.0.

**Deviation check:** No deviations. Spec delivered as required.

---

### ST-02 — Backend: Confirm Heat Calculation Availability

**Spec references:** `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio`, `docs/specs/metrics_definitions.md#Portfolio Heat`

**Status:** ✅ COMPLETE — Head of Engineering implemented (DEL-20260305-01 Unblocked).

**Commit SHA:** 6b1bee9

**What was built:** `portfolio_heat_percent` and `position_risks[]` added to `GET /portfolio` response. Formula uses entry stop (initial stop at position entry), FX adjustment = 1/stored_fx_rate for US positions, 1.0 for UK positions. Matches `metrics_definitions.md §Portfolio Heat` formula exactly. Prospective heat endpoint approach: `GET /portfolio/prospective-heat` with query params (ticker, shares, entry_price, stop_price).

**Deviation check:** No deviations from `metrics_definitions.md §Portfolio Heat` formula.

---

### ST-03 — Frontend: Risk Dashboard Page Implementation

**Spec references:** `docs/specs/frontend/pages/risk_dashboard.md` v0.1.1

**Status:** ✅ COMPLETE — Implemented and accepted by Product Owner (ESC-EXEC-20260305-02 Resolved).

**Commit SHA:** 7b08fa7 (latest of 8 commits to main: 0d319b4, b1bb3d2, 2182b9d, ccbd645, ba6131c, b034d29, 3e4d143, 7b08fa7)

**What was built:** Full Risk Dashboard page at `/risk`. Components: HeatGauge (SVG arc gauge, threshold colours correct), DrawdownSummary, GracePeriodPanel (sorted ascending by days remaining, colour-coded), PositionRiskTable (GRACE→LOSING→PROFITABLE sort, stop distance derived), ProspectiveHeatPanel (collapsible, server-side calc, input validation). Route registered in Layout.js and pages.config.js.

**Deviation check:** 8 deviations identified; all accepted for v1.8 by Product Owner. Filed in `risk_dashboard.md §11` v0.1.1. See DEV-ST03-01 through DEV-ST03-08. No P0 or P1 deviations.

---

### ST-04 — QA: Risk Dashboard Acceptance Test Scenarios

**Spec references:** `docs/testing/risk_dashboard_scenarios.md` v1.0.0, `docs/specs/metrics_definitions.md#Portfolio Heat`

**Status:** ✅ COMPLETE — Director of Quality sign-off completed 2026-03-05.

**Commit SHA:** f261f0f

**Scenarios file:** `docs/testing/risk_dashboard_scenarios.md` v1.0.0 — Class 1 Canonical

**What was built:** 27 acceptance test scenarios in 7 groups:
- Group A (6 scenarios): Heat gauge threshold boundaries — 0%, 9.9%, 10%, 20%, 30%, 35%. All expected values derived from `metrics_definitions.md §Portfolio Heat Display Thresholds` v1.6.0. Concrete test data with formula derivations provided.
- Group B (7 scenarios): Grace Period Panel — day 1 (red), day 2 (amber lower), day 4 (amber upper), day 5 (green), day 10 (in grace), expired exclusion, empty state.
- Group C (2 scenarios): Position Risk Table — all 3 states simultaneously with sort verification, empty state.
- Group D (4 scenarios): Prospective Heat — threshold crossing (15%→21%), input validation, result display, collapsed default.
- Group E (5 scenarios): Independent API error states per component.
- Group F (1 scenario): Full empty state (no open positions).
- Group G (2 scenarios): Non-functional — no console errors, no client-side recalculation.

5 known v1.8 deviations (DEV-ST03-01 through DEV-ST03-05) documented in §2 with QA execution guidance.

**Director of Quality approval:** ✅ APPROVED 2026-03-05. Scenario document v1.0.1 signed off. DEV-ST03-09 (P3) identified and filed. See §6 Sign-Off Checklist in risk_dashboard_scenarios.md v1.0.1.

---

## EPIC-Level Consolidation

*(To be completed when all ST items are done)*

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-01 | `risk_dashboard.md` | Frontend spec v0.1.0 (Design Gate) | Spec complete, all 5 sections | Pass ✅ | None |
| ST-02 | `portfolio_endpoints.md`, `metrics_definitions.md` | `portfolio_heat_percent` + `position_risks[]` in GET /portfolio; formula matches spec | Heat endpoint confirmed; formula verified | Pass ✅ | None |
| ST-03 | `risk_dashboard.md` v0.1.1 | Full Risk Dashboard page: 5 components, route registered, all major AC met | Renders, heat thresholds correct, sort, server-side calc, validation | Pass ✅ (with deviations) | DEV-ST03-01 (P2), DEV-ST03-02 (P3), DEV-ST03-03 (P2), DEV-ST03-04 (P2), DEV-ST03-05 (P3), DEV-ST03-06 (P3), DEV-ST03-07 (P3), DEV-ST03-08 (P2) — all accepted v1.8 |
| ST-04 | `risk_dashboard_scenarios.md` | Scenario document v1.0.1: 27 scenarios, 7 groups, all values derived from spec; §2 reference corrected | All scenarios approved by Director of Quality | Pass ✅ | None (DEV-ST03-09 found during review — filed in risk_dashboard.md §11 v0.1.2) |

**QA test coverage:**
- Scenarios run: `docs/testing/risk_dashboard_scenarios.md` (once filed)
- Regression areas checked: frontend rendering, heat calculation, colour thresholds, grace period logic
- Known deviations filed: DEV-ST03-01 (P2), DEV-ST03-02 (P3), DEV-ST03-03 (P2), DEV-ST03-04 (P2), DEV-ST03-05 (P3), DEV-ST03-06 (P3), DEV-ST03-07 (P3), DEV-ST03-08 (P2) — all filed in `risk_dashboard.md §11` v0.1.1; all accepted for v1.8 by Product Owner

**QA sign-off block:** (Director of Quality completes this)
- [x] All acceptance criteria verified against canonical spec (`risk_dashboard.md` v0.1.2)
- [x] No unresolved P0 or P1 deviations — 9 deviations total (DEV-ST03-01 through DEV-ST03-09), all P2 or P3, all accepted for v1.8 by Product Owner
- [x] Regression areas checked: frontend rendering, heat calculation, colour thresholds, grace period logic, sort orders, error handling isolation
- [x] ST-04 scenario document approved — `risk_dashboard_scenarios.md` v1.0.1 (signed off 2026-03-05)
- [x] Heat gauge colour at boundary values verified — HeatGauge.js getColor() uses `>=` comparisons in correct precedence order; 10%=Moderate (#f59e0b), 20%=High (#f97316), 30%=Extreme (#ef4444)
- [x] No client-side recalculation of metric values confirmed — heat and drawdown values passed directly from API; Stop Distance % is permitted display arithmetic (spec §6.2)
- Signed off by: Director of Quality
- Date: 2026-03-05
- Comments: One new deviation identified during review: DEV-ST03-09 (P3) — ProspectiveHeatPanel omits threshold label from result display per spec §7.5. Filed in risk_dashboard.md §11 v0.1.2. Accepted for v1.8. Minor §2 reference error in scenario document corrected (v1.0.1). EPIC-01 QA gate: APPROVED. Recommend opening EPIC-01 PR.
