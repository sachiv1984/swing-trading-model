**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Version:** 1.0
**Last Updated:** 2026-03-17
**Cycle:** 2026-03-17__release-v2.0

---

# Sprint Close Record — 2026-03-17__release-v2.0

---

## Sprint Goal

Ship the v2.0 core product scope: fix the P1 portfolio response defect, deliver the UK tax-year P&L report endpoint and frontend view, and expose the signal exposure controls — making all three production-ready in a single sprint.

**Net outcome vs sprint goal: MET IN FULL.** All three core deliverables shipped. Both stretch items (ST-13, ST-20) also completed.

---

## Items Done

| ST Item | Title | Commit SHA | Branch | Spec References |
|---------|-------|------------|--------|-----------------|
| ST-01 | Author signals page frontend spec | 5483f84 | EPIC-01 | docs/specs/frontend/pages/signals.md v0.1; docs/specs/Specs_Index.md §3.5 |
| ST-02 | Implement top_n and lookback_days controls on signals page | 3ef82f7 | EPIC-01 | docs/specs/frontend/pages/signals.md v0.1; docs/specs/api_contracts/signal_endpoints.md |
| ST-03 | Author tax-year P&L report spec (pre-completed) | 3fc5ead | EPIC-04 (pre-sprint) | docs/specs/api_contracts/reports_endpoints.md v0.1 |
| ST-04 | Implement GET /reports/tax-year endpoint | dde5664 | EPIC-02 | docs/specs/api_contracts/reports_endpoints.md v0.1; docs/specs/data_model.md §3 |
| ST-05 | Frontend: tax-year P&L report view | 04b765f | EPIC-02 | docs/specs/frontend/pages/reports.md v0.1 |
| ST-11 | QA: notification delivery test scenarios (pre-completed) | — | — | claude/cycles/2026-03-17__release-v2.0/qa_notification_planning.md |
| ST-12 | Fix GET /portfolio missing 4 fields (P1) | 04ed5e8 | EPIC-04 | docs/specs/api_contracts/portfolio_endpoints.md; docs/testing/v1.7-qa-scenario-gaps.md — GAP-03 |
| ST-13 | Spec + implement GET /portfolio/prospective-heat (stretch) | 279e832 | EPIC-04 | docs/specs/api_contracts/portfolio_endpoints.md v2.0.0 |
| ST-14 | Production Deployment Runbook | b59d551 | EPIC-05 | docs/ops/production_deployment_runbook.md |
| ST-15 | Positions Table Data Dictionary | 923f7c8 | EPIC-05 | docs/specs/data_model_positions_dictionary.md |
| ST-16 | Database Migration Governance Standard | b411a06 | EPIC-05 | docs/ops/database_migration_governance.md |
| ST-17 | Spec Coverage Inventory | 8ce92ba | EPIC-05 | docs/specs/spec_coverage_inventory.md |
| ST-18 | Roadmap stage document consolidation (BLG-GOV-01) | 7858d91 | EPIC-06 | claude/system/roadmap_prompt.md v4.0; OPERATIONAL_GUIDE.md v3.24 |
| ST-19 | Ideas register (BLG-GOV-02) | a236678 | EPIC-06 | claude/system/idea_intake_prompt.md v2.0; claude/ideas/ideas_register.md |
| ST-20 | CohortAnalysis backend integration regression scenarios (stretch) | 4adbe21 | EPIC-04* | docs/testing/analytics_scenarios.md v1.0 |

*ST-20 committed on EPIC-04 branch — cross-branch process deviation (P3); content correct; documented in qa_evidence_EPIC-04.md.

---

## Post-Merge Hotfix

| Commit | Description | Reason |
|--------|-------------|--------|
| bb66b69 | Fix base44.baseUrl undefined — expose API_BASE_URL on base44 object | `Reports.js` used `base44.baseUrl` which was not exposed on the export; caused `undefined/reports/tax-year` URL on production. Identified during DoQ staging verification (ST-05). |

---

## Items Returned to Backlog

None. All sprint items completed.

---

## Items Deferred This Sprint

| ST Item | EPIC | Reason |
|---------|------|--------|
| ST-06 | EPIC-03 | EPIC-03 deferred to v2.1 — no async notification infrastructure (BLG-TECH-08 prerequisite) |
| ST-07 | EPIC-03 | Same |
| ST-08 | EPIC-03 | Same |
| ST-09 | EPIC-03 | Same |
| ST-10 | EPIC-03 | Same |

---

## QA Evidence Logs Produced

| EPIC | Evidence Log | DoQ Sign-off |
|------|-------------|--------------|
| EPIC-01 | claude/cycles/2026-03-17__release-v2.0/qa_evidence_EPIC-01.md | ✅ 2026-03-17 |
| EPIC-02 | claude/cycles/2026-03-17__release-v2.0/qa_evidence_EPIC-02.md | ✅ 2026-03-17 |
| EPIC-04 | claude/cycles/2026-03-17__release-v2.0/qa_evidence_EPIC-04.md | ✅ 2026-03-17 |
| EPIC-05 | claude/cycles/2026-03-17__release-v2.0/qa_evidence_EPIC-05.md | ✅ 2026-03-17 |
| EPIC-06 | claude/cycles/2026-03-17__release-v2.0/qa_evidence_EPIC-06.md | ✅ 2026-03-17 |

---

## Deviations Filed This Sprint

| Deviation | Spec File | Priority | Status |
|-----------|-----------|----------|--------|
| ST-20 cross-branch commit (committed on EPIC-04 instead of EPIC-05) | qa_evidence_EPIC-04.md | P3 — process only | Documented; content correct |
| base44.baseUrl not exposed (ST-05 production bug) | src/api/base44Client.js | P1 — production defect | Fixed in hotfix bb66b69 on 2026-03-17 |

---

## Open Escalations

None.

---

## Staging Verification Outcomes (DoQ)

| Item | Result | Evidence Method |
|------|--------|----------------|
| ST-02 — Signals controls (top_n, lookback_days, debounce) | Pass | Live test on sachiv1984.github.io/swing-trading-model (production) — 2026-03-17 |
| ST-05 — Tax year P&L view (tab, banner, API call) | Pass | Live test on sachiv1984.github.io/swing-trading-model (production) — 2026-03-17; base44.baseUrl hotfix applied |
| ST-12 — GET /portfolio 4 missing fields | Pass | Integration tests (TestGetPortfolioFieldContract, TestGetPortfolioEmpty) |
| ST-13 — GET /portfolio/prospective-heat | Pass | Integration tests (TestProspectiveHeat — 7 tests) |
| ST-04 — GET /reports/tax-year | Pass | Integration tests (29 tests — test_reports_integration.py) |

---

## Post-Merge Outstanding Actions

| Action | Owner | Status |
|--------|-------|--------|
| Director of Quality staging verification of GET /reports/tax-year post-deployment | Director of Quality | Complete — ST-05 pass confirmed 2026-03-17 |
| EPIC-06 functional regression at next `run roadmap` invocation | Head of Specs Team | Deferred — accepted |

---

## Verification Readiness Statement

- All spec references populated: **Yes**
- All deviations filed: **Yes**
- QA evidence logs complete: **Yes** (5 EPICs, all DoQ sign-off complete)
- Post-merge hotfix documented: **Yes** (bb66b69)
- Ready for `run delivery verification`: **Yes**
