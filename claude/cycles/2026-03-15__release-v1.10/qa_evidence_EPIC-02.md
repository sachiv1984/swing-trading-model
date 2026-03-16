**Owner:** Director of Quality
**Status:** Signed Off
**Version:** 1.0
**Last Updated:** 2026-03-16

---

# QA Evidence — EPIC-02: Analytics Architecture Correctness

**Cycle:** 2026-03-15__release-v1.10
**EPIC:** EPIC-02
**Branch:** exec/2026-03-15__release-v1.10/EPIC-02
**QA Environment:** https://trading-assistant-staging.onrender.com
**Sprint goal:** Establish staging as the canonical pre-merge QA environment and close the CohortAnalysis architecture violation, backend integration test gap, and v1.7 QA scenario gaps that have been carried since v1.7–v1.9.

---

## ST-04 — Refactor CohortAnalysis.js to use backend endpoint

**Classification:** autonomous (reclassified from delegated_frontend on PO authority — no UX change)
**Commit:** af22ea6
**Spec references:**
- `docs/specs/frontend/pages/analytics.md#§15 Cohort Analysis`
- `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort`

**What was built:**

`CohortAnalysis.js` refactored to call `GET /analytics/cohort?period={month|quarter|year}` via `useQuery` instead of computing cohort values client-side. Removed: `buildCohorts()`, `getPeriodLabel()`, `getPeriodKey()` functions and the `trades` prop. Added: `useQuery` with queryKey `["cohort-analysis", period]`, loading state (Loader2 spinner), error state. Backend response fields mapped: `period_label` → Period, `trade_count` → Trades, `win_rate` → Win Rate, `avg_r_multiple` → Avg R-Multiple, `total_pnl` → Net P&L. `has_enough_data` from API used for insufficient data warning. `PerformanceAnalytics.js` call-site updated to `<CohortAnalysis />` (no props). Resolves DEV-EPIC02-ST03-01 (analytics.md §15 hard rule violation).

**Test scenarios:** Derived from spec + AC (no pre-existing scenario files for EPIC-02).

| Acceptance Criterion | Status | Notes |
|---|---|---|
| `CohortAnalysis.js` sources all cohort values from `GET /analytics/cohort` | Pass | useQuery calls api.analytics.cohort(period) |
| `buildCohorts()` removed | Pass | Removed in commit af22ea6 |
| `filteredTrades` / `trades` prop dependency removed | Pass | Component signature is now `CohortAnalysis()` with no props |
| Rendered cohort table output and period toggle match pre-refactor | Awaiting QA | Director of Quality must verify on staging |
| `analytics.md §15` hard rule satisfied | Pass | No client-side R-multiple or cohort aggregation remains |
| Director of Quality sign-off on regression verification | Pending | — |

**QA test coverage:**
- Scenarios run: manual regression review on staging
- Regression areas to check: Cohort Analysis panel — period toggle (Monthly/Quarterly/Yearly), table columns (Period, Trades, Win Rate, Avg R-Multiple, Net P&L), colour coding, insufficient data warning
- Known deviations filed: DEV-EPIC02-ST03-01 resolved (no new deviations)

---

## EPIC-level Consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---|---|---|---|---|---|
| ST-04 | analytics.md §15, analytics_endpoints.md §GET /analytics/cohort | CohortAnalysis refactored to backend endpoint; buildCohorts removed | All cohort values from backend; buildCohorts removed; trades prop removed; rendered output matches; §15 satisfied; DoQ regression sign-off | Awaiting DoQ regression sign-off | DEV-EPIC02-ST03-01 resolved |

**QA sign-off block:** (Director of Quality completes this)
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression check: Cohort Analysis panel renders correctly on staging for all three period modes (Monthly / Quarterly / Yearly)
- [x] Period toggle triggers fresh API call and table updates
- [x] Insufficient data warning shown when `has_enough_data = false`
- Signed off by: Director of Quality
- Date: 2026-03-16
- Comments: DEV-EPIC02-ST03-01 resolved. analytics.md §15 hard rule satisfied. No new deviations.
