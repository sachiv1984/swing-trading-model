Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Signed Off
Last Updated: 2026-03-13

---

# QA Evidence Log — EPIC-03

**EPIC:** EPIC-03 — Dashboard Homepage
**Cycle:** 2026-03-06__release-v1.9
**Sprint goal:** Deliver the v1.9 user value features — canonicalise compliance metrics definitions and surface them in the frontend, implement the structured trade reflection form, add cohort analysis and R-multiple distribution to the analytics page, and launch the dashboard homepage — completing the full v1.9 release scope.
**Test scenarios used:** Manual acceptance review against dashboard.md v2.0 (ST-12 Playwright scenarios for dashboard homepage to be authored separately)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-05 | docs/specs/frontend/pages/dashboard.md v2.0 | DashboardHome.js page (route `/` root via pages.config.js mainPage); 5 independent card components in src/components/dashboard/home/: OpenPositionsCard, PortfolioHeatCard, GracePeriodCard, SignalStatusCard, RecentActivityCard; shared DashboardCard wrapper; all API calls via api.* (doFetch). pages.config.js mainPage set to 'DashboardHome'. No composite endpoint added (individual calls sufficient per Head of Engineering decision). | DashboardHome route is `/`; 5 data cards render session summary; each card fetches independently; individual card error does not break others; all API calls via api.*; responsive layout (3-card row + 2-card row); click navigation per spec §6 | **Pass with deviation** | DEV-EPIC03-ST05-01 (P3, see below) |

**QA findings log:**

**DEV-EPIC03-ST05-01 — P3 (Filed)**
- Story: ST-05
- Finding: Spec §5 "All endpoints failed: Full page error with 'Retry' button" — implemented as a hidden retry handler in DashboardHome.js (`<div className="hidden" id="dashboard-retry-root">`). Individual card error states display within each card ("Unable to load"). When all 5 endpoints fail simultaneously, the page shows 5 individual card error states rather than a unified full-page overlay with a prominent Retry button.
- Impact: Low — per-card error messages are visible and informative. The `handleRetry()` function exists and correctly invalidates all 5 query keys, but the full-page overlay state detection and display are not surfaced.
- Disposition: P3 — acceptable for v1.9. Recommended v1.10 enhancement: detect all-failed state at DashboardHome level and render full-page error with Retry button.
- Status: Filed and accepted.

ST-05 QA review: Verified `DashboardHome.js` renders 5 card components in correct layout (3-card grid top row, 2-card grid bottom row). Each card uses its own `useQuery` with a unique key — errors in one card do not affect others (confirmed in OpenPositionsCard, PortfolioHeatCard, GracePeriodCard, SignalStatusCard, RecentActivityCard). All API calls route through `api.*` methods (doFetch). `pages.config.js` has `mainPage: "DashboardHome"`. `DashboardCard` wrapper accepts `to` prop for click navigation to linked pages (Positions → `/Positions`, Portfolio Heat → `/RiskDashboard`). No composite endpoint was added — consistent with Head of Engineering decision recorded in execution state. P3 deviation DEV-EPIC03-ST05-01 accepted (no P0 or P1 issues).

**QA test coverage:**
- Scenarios run: Manual acceptance review (code inspection against spec dashboard.md v2.0)
- Regression areas checked: pages.config.js mainPage routing, src/components/dashboard/home/ card isolation, base44Client.js api additions, DashboardHome responsive grid layout
- Known deviations filed: DEV-EPIC03-ST05-01 (P3)

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- Signed off by: Director of Quality
- Date: 2026-03-13
- Comments: ST-05 passes with accepted P3 deviation (DEV-EPIC03-ST05-01 — hidden full-page retry overlay; individual card errors visible and functional). No P0 or P1 deviations. Merge gate clear for EPIC-03 once PR is created.
