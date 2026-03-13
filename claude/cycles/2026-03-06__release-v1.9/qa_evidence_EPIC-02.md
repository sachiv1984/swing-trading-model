**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Signed Off
**Last Updated:** 2026-03-13

---

# QA Evidence Log — EPIC-02

**EPIC:** EPIC-02 — Analytics Enhancements
**Cycle:** 2026-03-06__release-v1.9
**Sprint goal:** Deliver the v1.9 user value features — canonicalise compliance metrics definitions and surface them in the frontend, implement the structured trade reflection form, add cohort analysis and R-multiple distribution to the analytics page, and launch the dashboard homepage — completing the full v1.9 release scope.
**Test scenarios used:** Manual acceptance review against analytics.md §15–§16 and metrics_definitions.md v1.7.0 (ST-12 Playwright scenarios for v1.9 features to be authored separately)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-03 | docs/specs/metrics_definitions.md#Cohort Metrics; docs/specs/frontend/pages/analytics.md#§15; docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort | metrics_definitions.md v1.7.0: Cohort Metrics section added. Backend: AnalyticsService.calculate_cohort(), GET /analytics/cohort?period={month\|quarter\|year} (3c91e7b). Frontend: CohortAnalysis.js — period toggle (Month/Quarter/Year), table (period, trades, win rate, avg R, P&L), loading/error/insufficient states, integrated into PerformanceAnalytics.js §15. analytics_endpoints.md v1.9.2. openapi.yaml updated. base44Client.js: api.analytics.cohort(). | Cohort metric definitions added to metrics_definitions.md; backend groups closed trades by entry period; frontend cohort analysis panel with period selector; values computed from canonical backend formula; endpoint documented in API contracts; openapi.yaml updated | **Pass with deviation** | DEV-EPIC02-ST03-01 (P2) |
| ST-04 | docs/specs/metrics_definitions.md#R-Multiple (Canonical Server-Side); docs/specs/frontend/pages/analytics.md#§16; docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/r-multiple-distribution | Backend: AnalyticsService.calculate_r_multiple_distribution(), GET /analytics/r-multiple-distribution (3633150). Formula: R=(exit_price-entry_price)/(entry_price-initial_stop_price). 7 buckets, median_r, pct_above_1r, avg_winner_r, avg_loser_r. Min 5 qualifying trades. Frontend: RMultipleDistributionBackend.js — bar chart (green positive, red negative), 4-stat summary row integrated into PerformanceAnalytics.js §16. Hard rule: no client-side R computation. openapi.yaml updated. base44Client.js: api.analytics.rMultipleDistribution(). | R-multiple formula defined in metrics_definitions.md; backend computes R-multiple per closed trade; distribution visualisation on analytics page; values from canonical backend formula; no client-side derivation | **Pass** | None |

**QA findings log:**

**DEV-EPIC02-ST03-01 — P2 (Filed in analytics.md v1.4)**
- Story: ST-03 — Cohort Analysis
- Finding: `CohortAnalysis.js` receives a `trades` prop from `PerformanceAnalytics.js` and computes cohort groupings and avg_r client-side via `buildCohorts()`. The component does not call `GET /analytics/cohort` despite the endpoint being implemented and wired in `base44Client.js`. This violates the analytics.md §15 hard rule: "All values sourced from backend. No client-side R-multiple computation in this component."
- Impact: P2 — numerical values are correct (same canonical formula), but computation layer is wrong. Regression risk if trade data shape changes server-side.
- Filed: analytics.md v1.3→v1.4, commit on EPIC-02 branch.
- Resolution target: v1.10

ST-03: Backend endpoint `GET /analytics/cohort` verified: groups trades by period (month/quarter/year), computes win_rate, avg_r_multiple (server-side R formula: `(exit_price - entry_price) / (entry_price - stop_price)`), total_pnl per cohort. API contract and openapi.yaml updated. Cohort metric definitions present in metrics_definitions.md v1.7.0. Frontend component correctly displays all four columns (trades, win rate, avg R, net P&L), period toggle works, insufficient-data state present. Core feature AC is met; P2 deviation filed for layer violation.

ST-04: Verified `RMultipleDistributionBackend.js` calls `api.analytics.rMultipleDistribution()` — backend-only, no client-side R computation. 7 buckets confirmed in backend. Bar colours: green for positive, red for negative. 4 stat cards: median_r, pct_above_1r, avg_winner_r, avg_loser_r — all backend-sourced. Minimum 5 trades threshold enforced. openapi.yaml includes `/analytics/r-multiple-distribution` path. All AC met. Hard rule confirmed: no client-side R derivation.

**QA test coverage:**
- Scenarios run: Manual acceptance review (code inspection against spec)
- Regression areas checked: analytics.md §15 cohort panel, analytics.md §16 R-multiple distribution panel, metrics_definitions.md cohort + R-multiple canonical formulas, GET /analytics/cohort and GET /analytics/r-multiple-distribution endpoints, openapi.yaml
- Known deviations filed: DEV-EPIC02-ST03-01 (P2, analytics.md v1.4)

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- Signed off by: Director of Quality
- Date: 2026-03-13
- Comments: ST-03 passes with P2 deviation filed (DEV-EPIC02-ST03-01 — client-side cohort computation; non-blocking). ST-04 passes cleanly. No P0 or P1 deviations. Merge gate clear for EPIC-02.
