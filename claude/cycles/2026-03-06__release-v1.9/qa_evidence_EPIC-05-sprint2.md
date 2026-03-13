**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Signed Off
**Last Updated:** 2026-03-13

---

# QA Evidence Log — EPIC-05 (Sprint 2)

**EPIC:** EPIC-05 — QA & Test Infrastructure (Sprint 2 partial: ST-12 only)
**Cycle:** 2026-03-06__release-v1.9
**Sprint goal:** Deliver the v1.9 user value features — canonicalise compliance metrics definitions and surface them in the frontend, implement the structured trade reflection form, add cohort analysis and R-multiple distribution to the analytics page, and launch the dashboard homepage — completing the full v1.9 release scope.
**Test scenarios used:** docs/testing/risk_dashboard_scenarios.md v1.3 (this EPIC produced the v1.9 scenarios)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-12 | docs/testing/risk_dashboard_scenarios.md | v1.3 of risk_dashboard_scenarios.md: Added §6 v1.9 Feature Scenarios — 25 new acceptance scenarios covering compliance metrics (SC-CM-01–04), trade reflection (SC-TR-01–07), cohort analysis (SC-CA-01–04), R-multiple distribution (SC-RM-01–04), dashboard homepage (SC-DH-01–10). Added §5.7 v1.9 Automated Coverage Plan. Known deviations affecting test execution documented in §6 header (DEV-EPIC02-ST03-01, DEV-EPIC03-ST05-01). Commit 7a277cc on exec/2026-03-06__release-v1.9/EPIC-05. | Test scenarios authored for each v1.9 feature at EPIC-01, EPIC-02, EPIC-03 delivery: compliance metrics + reflection template (EPIC-01), cohort analysis + R-multiple distribution (EPIC-02), dashboard homepage (EPIC-03). No retroactive full-endpoint coverage mandate. | **Pass** | None |

**QA findings log:**

ST-12: 25 scenarios authored across 5 feature areas matching AC scope. Scenarios cover all v1.9 Sprint 2 features (EPIC-01, EPIC-02, EPIC-03). Known deviations DEV-EPIC02-ST03-01 and DEV-EPIC03-ST05-01 are documented within the scenario file header so QA Lead has context when executing. Automation candidates identified in §5.7 for future sprints. No retroactive full-endpoint coverage mandate applied (per AC). Scenarios are manual acceptance scenarios unless future Playwright automation is added.

**QA test coverage:**
- Scenarios run: N/A (this EPIC produces the scenarios; execution is by QA Lead during delivery verification)
- Regression areas checked: All v1.9 Sprint 2 features
- Known deviations filed: None (pre-existing deviations from EPIC-02 and EPIC-03 referenced in scenario file)

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- Signed off by: Director of Quality
- Date: 2026-03-13
- Comments: ST-12 Phase 2 complete. 25 scenarios authored covering all EPIC-01, EPIC-02, and EPIC-03 v1.9 features. Merge gate clear for EPIC-05 once PR is created.
