Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-13

---

# QA Evidence Log — EPIC-03

**EPIC:** EPIC-03 — Dashboard Homepage
**Cycle:** 2026-03-06__release-v1.9
**Sprint goal:** Deliver the v1.9 user value features — canonicalise compliance metrics definitions and surface them in the frontend, implement the structured trade reflection form, add cohort analysis and R-multiple distribution to the analytics page, and launch the dashboard homepage — completing the full v1.9 release scope.
**Test scenarios used:** Derived from spec + AC (no pre-existing scenario file for EPIC-03; docs/testing/risk_dashboard_scenarios.md §5.5 applies for any new E2E scenarios authored by Director of Quality)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-05 | docs/specs/frontend/pages/dashboard.md v2.0 | DashboardHome.js page (route `/` root via pages.config.js mainPage); 5 independent card components in src/components/dashboard/home/: OpenPositionsCard, PortfolioHeatCard, GracePeriodCard, SignalStatusCard, RecentActivityCard; shared DashboardCard wrapper; api.market.getStatus() + api.signals.list() added to base44Client.js | DashboardHome route is `/`; 5 data cards render session summary; each card fetches independently; individual card error does not break others; all API calls via api.*; responsive layout (3-card row + 2-card row); click navigation per spec §6 | Pending QA sign-off | DEV-EPIC03-ST05-01 (P3, see below) |

**QA findings log:**

**DEV-EPIC03-ST05-01 — P3 (Filed)**
- Story: ST-05
- Finding: Spec §5 "All endpoints failed: Full page error with 'Retry' button" — implemented as a hidden retry handler in DashboardHome.js. Individual card error states display within each card ("Unable to load"). When all 5 endpoints fail simultaneously, the page shows 5 individual card error states rather than a unified full-page overlay with a prominent Retry button.
- Impact: Low — per-card error messages are visible and informative. The Retry handler exists (`handleRetry()` invalidates all 5 query keys) but the full-page overlay state detection and display are not implemented.
- Disposition: P3 — acceptable for v1.9. Recommended v1.10 enhancement: detect all-failed state at DashboardHome level and render full-page error with Retry button.
- Status: Filed, pending QA acceptance decision

**QA test coverage:**
- Scenarios run: pending — Director of Quality to run against dashboard.md v2.0
- Regression areas checked: pages.config.js mainPage routing, base44Client.js api.market + api.signals additions, individual card error isolation
- Known deviations filed: DEV-EPIC03-ST05-01 (P3)

**QA sign-off block:** (Director of Quality completes this)
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- Signed off by: Director of Quality
- Date:
- Comments:
