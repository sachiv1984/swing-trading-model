Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05 (updated SC-RD-27 result; DEV-ST03-12 filed)

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

**Scenario Execution Log (2026-03-05)**

| Scenario | Result | Notes |
|----------|--------|-------|
| SC-RD-01 | **PASS** | Nav entry confirmed present and functional. UX observation: heat gauge and label feel visually squashed; legend overlaps label area. Cosmetic only — no spec requirement violated. Noted for v1.9 polish. |
| SC-RD-02 | NOT EXECUTED | Test environment gap — no mechanism to load specific `portfolio_heat_percent` values into test backend. See note below. |
| SC-RD-03 | NOT EXECUTED | Test environment gap — as above. |
| SC-RD-04 | NOT EXECUTED | Test environment gap — as above. |
| SC-RD-05 | NOT EXECUTED | Test environment gap — as above. |
| SC-RD-06 | NOT EXECUTED | Test environment gap — as above. |
| SC-RD-07 | NOT EXECUTED | Test environment gap — requires position with `grace_days_remaining = 1`. |
| SC-RD-08 | NOT EXECUTED | Test environment gap — requires position with `grace_days_remaining = 1` (red boundary). |
| SC-RD-09 | NOT EXECUTED | Test environment gap — requires position with `grace_days_remaining = 2`. |
| SC-RD-10 | NOT EXECUTED | Test environment gap — requires position with `grace_days_remaining = 4`. |
| SC-RD-11 | NOT EXECUTED | Test environment gap — requires position with `grace_days_remaining = 5`. |
| SC-RD-12 | NOT EXECUTED | Test environment gap — requires grace period day 10 + expired position. |
| SC-RD-13 | **PASS** | Grace Period Panel empty state renders correctly: amber shield badge, "Grace Period" label, "No positions in grace period" in muted smaller text. No table rows. No count badge. Matches spec §5.5. |
| SC-RD-14 | **PASS (partial — live data, new deviation observed)** | Live data: LOSING (TER, STX) before PROFITABLE (MU, SNDK, WDC). No GRACE positions in live dataset. Primary group sort correct ✓. Secondary within-group sort tightest first ✓ (consistent with DEV-ST03-03 — visually matches spec even with different sort logic). Entry prices display in USD ($) for US positions; spec §6.2 requires GBP — NEW deviation DEV-ST03-11 filed. |
| SC-RD-15 | NOT EXECUTED | Test environment gap — requires no open positions to render empty state. |
| SC-RD-16 | NOT EXECUTED | Test environment gap — no live backend connection available to drive prospective heat endpoint; same root cause as Group A/B gaps (no data injection / API state control). |
| SC-RD-17 | NOT EXECUTED | Test environment gap — as above. |
| SC-RD-18 | NOT EXECUTED | Test environment gap — as above. |
| SC-RD-19 | **PASS** | Prospective Heat panel renders collapsed by default. Heading and expand chevron visible. No form shown until expanded. Matches spec §7.2. |
| SC-RD-20 | **PASS** | GET /portfolio failure: Heat Gauge renders error state correctly. |
| SC-RD-21 | **PASS** | GET /portfolio failure: Drawdown Summary renders error state correctly. |
| SC-RD-22 | **PASS (v1.8 actual — DEV-ST03-02 confirmed)** | GracePeriodPanel shows "No positions in grace period" on API failure — indistinguishable from empty state. Matches v1.8 expected per scenario doc. DEV-ST03-02 behaviour confirmed in live execution. |
| SC-RD-23 | **PASS (v1.8 actual — DEV-ST03-02 confirmed)** | PositionRiskTable shows "No open positions to display" on API failure — indistinguishable from empty state. Matches v1.8 expected per scenario doc. DEV-ST03-02 behaviour confirmed in live execution. |
| SC-RD-24 | NOT EXECUTED | Test environment gap — requires no open positions. |
| SC-RD-25 | NOT EXECUTED | Test environment gap — requires no open positions and portfolio_heat_percent = 0.0; cannot seed backend state in v1.8. |
| SC-RD-26 | **PASS** | Browser console confirmed clean on page load — no errors. Matches spec §10 (implicit). |
| SC-RD-27 | **PASS (new defect DEV-ST03-12)** | API response: `current_drawdown_percent: -9.2069` → UI displays "-9.2%" ✓ (rounding only, not recalculation). All server-provided metric values confirmed passed through directly. New defect: `current_stop` returned in native USD for US positions while `current_price` is in GBP — Stop Distance % display derivation `(current_price_GBP − current_stop_USD) / current_price_GBP` mixes currencies. DEV-ST03-12 (P2) filed in `risk_dashboard.md §11` v0.1.5. PO acceptance pending. |

**DEV-ST03-10:** RESOLVED — navigation fixed (index.js). Code defect DEF-RD-API-01 also fixed (RiskDashboard.js line 28, commit 24d8e5e to main). Both fixes applied 2026-03-05.

**DEF-RD-API-02:** RESOLVED — ProspectiveHeatPanel.js hardcoded `fetch('/api/portfolio/prospective-heat?...')` replaced with `api.portfolio.prospectiveHeat()` from base44Client.js. Fix commit e7caaa9 to main 2026-03-05. SC-RD-16/17/18 awaiting retest post-deploy.

**SC-RD-01 UX observation (not a spec failure):** HeatGauge gauge arc and percentage label feel visually squashed; the colour legend overlaps the label area. The spec (§3) does not prescribe precise layout dimensions, so this does not constitute a spec violation in v1.8. Recommended for v1.9 UX polish.

**SC-RD-02 through SC-RD-06 — test environment gap:**
Group A scenarios require specific `portfolio_heat_percent` values (0.0, 9.9%, 10.0%, 20.0%, 30.0%, 35.0%) to be returned by `GET /portfolio`. No test data injection mechanism or isolated test backend exists in v1.8. Without the ability to seed a specific portfolio state, these boundary threshold scenarios cannot be executed live.

Mitigation applied: threshold boundary logic was verified by code review of `HeatGauge.js` — `getColor()` uses `>=` comparisons in correct precedence order (confirmed in prior QA sign-off). This does not substitute for live execution but provides reasonable confidence in correctness for v1.8.

**Test infrastructure gap — formal recommendation (Director of Quality):**
17 of 27 scenarios (SC-RD-02–06, SC-RD-07–12, SC-RD-15, SC-RD-16–18, SC-RD-24–25) cannot be executed in v1.8 due to the absence of a test data injection mechanism and live backend state control. All 17 require specific backend state (portfolio heat %, holding days, position counts, empty positions, or live prospective heat API call) that cannot be loaded without either: (a) a seeded test database, (b) a mock/stub API layer, or (c) a test data management UI. This gap was observed independently across Groups A, B, C (empty state), D (prospective heat), and F, strongly indicating it will recur across any scenario-heavy QA cycle.

**Backlog recommendation:** Add a test environment with seeded data capability to the v1.9 backlog as a QA infrastructure story. Priority: P2. Without this, acceptance test execution coverage will remain structurally limited to empty/live-data states only.

**QA sign-off block:** (Director of Quality completes this)
- [x] ST-04 scenario document approved — `risk_dashboard_scenarios.md` v1.0.1 (signed off 2026-03-05)
- [x] Heat gauge colour at boundary values verified — HeatGauge.js getColor() uses `>=` comparisons in correct precedence order; 10%=Moderate (#f59e0b), 20%=High (#f97316), 30%=Extreme (#ef4444)
- [x] No client-side recalculation of metric values confirmed — heat and drawdown values passed directly from API; Stop Distance % is permitted display arithmetic (spec §6.2)
- [ ] All acceptance criteria verified against canonical spec — INCOMPLETE: 12/27 executed (SC-RD-01/13/14 PASS; SC-RD-16–18 fix applied, retest pending; 11 NOT EXECUTED test env gap; SC-RD-19–27 pending)
- [x] No unresolved P0 or P1 deviations — DEV-ST03-10 RESOLVED; DEV-ST03-11 P2 awaiting PO acceptance; all others P2/P3 accepted v1.8
- [ ] Regression areas checked — partially complete (code review + live execution for loaded/empty states; Group A/B boundary and error state scenarios blocked by test env gap)
- Signed off by: Director of Quality
- Date: 2026-03-05
- Comments: SC-RD-01 PASS (DEV-ST03-10 resolved). SC-RD-13 PASS. SC-RD-14 PASS (partial — DEV-ST03-11 P2 filed, PO acceptance pending). SC-RD-16/17/18 NOT EXECUTED — test environment gap (no live backend state control for prospective heat). SC-RD-19 PASS (collapsed default). SC-RD-20–23 PASS (API error states). SC-RD-26 PASS (console clean). SC-RD-27 PASS — network tab confirmed no client-side recalculation; drawdown -9.2069 → -9.2% (rounding only). DEV-ST03-12 (P2) found — current_stop in USD vs current_price in GBP; Stop Distance % calculation mixes currencies; filed in risk_dashboard.md §11 v0.1.5, PO acceptance pending. 17/27 scenarios not executable due to systematic test infrastructure gap — documented as formal QA recommendation (P2 backlog story for v1.9). All executed scenarios PASS. No P0/P1 deviations. All P2/P3 deviations filed.
