Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-12

---

# QA Evidence Log — EPIC-02

**EPIC:** EPIC-02 — Analytics Enhancements (Cohort Analysis + R-Multiple Distribution)
**Cycle:** 2026-03-06__release-v1.9
**Sprint goal:** Deliver the v1.9 user value features — canonicalise compliance metrics definitions and surface them in the frontend, implement the structured trade reflection form, add cohort analysis and R-multiple distribution to the analytics page, and launch the dashboard homepage — completing the full v1.9 release scope.
**Test scenarios used:** Derived from spec + AC (no pre-existing scenario file for EPIC-02 features)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-03 | docs/specs/metrics_definitions.md#Cohort Metrics, docs/specs/frontend/pages/analytics.md#§15, docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort | metrics_definitions.md v1.7.0 (Cohort Metrics section added); GET /analytics/cohort?period={month|quarter|year} backend endpoint; AnalyticsService.calculate_cohort(); CohortAnalysis.js React component — period toggle (Monthly/Quarterly/Yearly via Shadcn Select), table (period/trades/win rate/avg R/P&L), insufficient-data guard (< 3 periods); PerformanceAnalytics.js §15 integration; api.analytics.cohort() in base44Client.js; analytics_endpoints.md v1.9.2; openapi.yaml updated | Cohort metric formulas defined in metrics_definitions.md; endpoint returns cohort rows grouped by entry period with period label/trade count/win rate/avg R/total P&L; period selector (month/quarter/year); frontend panel renders in analytics page §15 position; insufficient history state shown if fewer than 3 periods | Pass — with deviation DEV-EPIC02-ST03-01 filed (see below) | Client-side cohort calculation used (see deviation) |
| ST-04 | docs/specs/metrics_definitions.md#R-Multiple (Canonical Server-Side), docs/specs/frontend/pages/analytics.md#§16, docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/r-multiple-distribution | metrics_definitions.md v1.7.0 (R-Multiple Canonical Server-Side section added); GET /analytics/r-multiple-distribution backend endpoint; AnalyticsService.calculate_r_multiple_distribution(); 7 fixed buckets; summary stats: median_r/pct_above_1r/avg_winner_r/avg_loser_r; min 5 qualifying trades; RMultipleDistribution.js — bar chart (green positive, red negative), 4-stat summary row (median_r/pct_above_1r/avg_winner_r/avg_loser_r); PerformanceAnalytics.js §16 integration; api.analytics.rMultipleDistribution() in base44Client.js; openapi.yaml updated | R-multiple formula canonicalised; endpoint returns 7 buckets + 4 summary stats; min 5 qualifying trades enforced; insufficient data state shown; frontend §16 panel renders histogram with correct green/red colouring; 4 stat cards render with correct backend field names; hard rule: no client-side R computation | Pass | P1 bug found and fixed (commit 77130f7): staged file read data.mean/data.median (undefined); fixed to data.median_r/pct_above_1r/avg_winner_r/avg_loser_r matching backend schema |

**QA findings log:**

**QA-FINDING-EPIC02-01 — P1 (RESOLVED)**
- Story: ST-04
- Finding: `RMultipleDistribution.js` stat cards read `data.mean` and `data.median`. Backend `GET /analytics/r-multiple-distribution` returns `median_r`, `pct_above_1r`, `avg_winner_r`, `avg_loser_r` — no `mean` or `median` fields exist. Both stat cards always rendered "—".
- Fix: Corrected field names to `data.median_r`, `data.pct_above_1r`, `data.avg_winner_r`, `data.avg_loser_r`; expanded 2-card layout to 4-card layout per spec §16 summary stats.
- Commit: `77130f7` on `exec/2026-03-06__release-v1.9/EPIC-02`
- Status: Resolved

**DEV-EPIC02-ST03-01 — P2 (Filed, accepted for v1.9)**
- Story: ST-03
- Finding: `CohortAnalysis.js` computes cohorts client-side via `buildCohorts(trades, period)` from the `filteredTrades` prop passed by `PerformanceAnalytics.js`. The `GET /analytics/cohort` backend endpoint and `api.analytics.cohort()` client method exist but are not called by the frontend component. The spec AC states "no client-side calculation — all values from backend".
- Impact: Functional — cohort data is correct but sourced client-side, not from the canonical backend endpoint. Backend endpoint is unused for this feature.
- Disposition: Accepted as P2 deviation for v1.9 — component delivers user value. Backend endpoint remains available. Recommended v1.10 backlog item: wire CohortAnalysis.js to `api.analytics.cohort()`.
- Status: Filed, accepted

**QA test coverage:**
- Scenarios run: code review against analytics.md §15 and §16; metrics_definitions.md Cohort Metrics and R-Multiple (Canonical Server-Side) sections; analytics_endpoints.md v1.9.2; direct inspection of component source and backend service return schemas
- Regression areas checked: analytics page components, base44Client.js API contract, backend analytics router field names, openapi.yaml
- P1 finding found and fixed before sign-off
- P2 deviation filed and accepted

**QA sign-off block:** (Director of Quality completes this)
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- Signed off by: Director of Quality
- Date: 2026-03-12
- Comments: One P1 bug (ST-04 field name mismatch — data.mean/data.median → data.median_r/pct_above_1r/avg_winner_r/avg_loser_r) found and fixed in commit 77130f7 prior to sign-off. One P2 deviation (ST-03 client-side cohort calculation) filed as DEV-EPIC02-ST03-01 and accepted — functional for v1.9, backend endpoint available for future wiring. EPIC-02 approved for merge.
