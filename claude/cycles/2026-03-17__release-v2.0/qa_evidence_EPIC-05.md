Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-17

---

# QA Evidence Log — EPIC-05 Documentation & Standards Pack

**EPIC:** EPIC-05 — Documentation & Standards Pack
**Cycle:** 2026-03-17__release-v2.0
**Branch:** exec/2026-03-17__release-v2.0/EPIC-05
**Sprint goal:** Ship the v2.0 core product scope: fix the P1 portfolio response defect, deliver the UK tax-year P&L report endpoint and frontend view, and expose the signal exposure controls — making all three production-ready in a single sprint.

**Note:** ST-20 is `blocked_qa` — this evidence log is partially open. Director of Quality sign-off on ST-20 section required to close EPIC-05.

---

## EPIC-05 Consolidation

**Test scenarios used:**
- `docs/testing/analytics_scenarios.md` — ST-20 (SC-CA-BACKEND-01, SC-CA-BACKEND-02, SC-CA-BACKEND-03)
- Derived from spec + AC for ST-14, ST-15, ST-16, ST-17

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-16 | `docs/ops/database_migration_governance.md` | Migration governance doc + backend_engineering_patterns.md cross-ref | All AC met; Head of Engineering sign-off | Pending QA | None |
| ST-14 | `docs/ops/production_deployment_runbook.md` | Production deployment runbook | All AC met | Pending QA | None |
| ST-15 | `docs/specs/data_model_positions_dictionary.md` | Positions table data dictionary | All AC met | Pending QA | None |
| ST-17 | `docs/specs/spec_coverage_inventory.md` | Spec coverage inventory — 38 docs audited | All AC met; Specs_Index.md §8 registered | Pending QA | None |
| ST-20 | `docs/testing/analytics_scenarios.md` | CohortAnalysis regression scenarios | Scenarios authored; QA sign-off pending | **Pending QA sign-off** | Cross-branch process (see note) |

**ST-16 — Database Migration Governance Standard**

**Commit:** `b411a06` on `exec/2026-03-17__release-v2.0/EPIC-05`

**What was built:** `docs/ops/database_migration_governance.md` created (Class 2 Supporting). Covers: naming convention, required fields, review requirements (second-engineer + schema owner), application procedure, incident procedure. Cross-referenced from `backend_engineering_patterns.md`. Head of Engineering sign-off recorded.

**ST-14 — Production Deployment Runbook**

**Commit:** `b59d551` on `exec/2026-03-17__release-v2.0/EPIC-05`

**What was built:** `docs/ops/production_deployment_runbook.md` created. Covers the full deployment procedure for v2.0.

**ST-15 — Positions Table Data Dictionary**

**Commit:** `923f7c8` on `exec/2026-03-17__release-v2.0/EPIC-05`

**What was built:** `docs/specs/data_model_positions_dictionary.md` created. All positions table fields documented with types, constraints, and business semantics.

**ST-17 — Spec Coverage Inventory**

**Commit:** `8ce92ba` on `exec/2026-03-17__release-v2.0/EPIC-05`

**What was built:** `docs/specs/spec_coverage_inventory.md` produced. 38 docs audited. Each spec section rated covered/partial/gap. 7 gap actions identified and cross-referenced to open backlog items. Review cadence defined. Registered in `Specs_Index.md §8`.

---

## ST-20 — CohortAnalysis Backend Integration Regression Scenario (stretch) ⏳ Awaiting QA sign-off

**Spec references:**
- `docs/specs/frontend/pages/analytics.md §15`
- `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort`
- `docs/testing/analytics_scenarios.md`

**Commit:** `4adbe21` on `exec/2026-03-17__release-v2.0/EPIC-04` *(cross-branch process deviation — item belongs to EPIC-05 but committed on EPIC-04 for convenience. Content is correct. Will land in main via EPIC-04 PR.)*

**What was built:**
`docs/testing/analytics_scenarios.md` created (Class 1 Canonical v1.0). Three scenarios registered:

- **SC-CA-BACKEND-01** (P2): Period toggle (Month/Quarter/Year) fires a new `GET /analytics/cohort?period=X` call; table re-renders; column values match API response fields verbatim (`trade_count`, `win_rate`, `avg_r_multiple`, `total_pnl`).
- **SC-CA-BACKEND-02** (P2): `has_enough_data: false` → "Not enough closed trades to show [period] cohorts" message; no table rows render; period toggles remain active.
- **SC-CA-BACKEND-03** (P1): Column value regression guard — each displayed value must trace to the API response field; `avg_r_multiple: null` renders as "—" not "0.0R".

**TD-CA-01 controlled dataset** defined for SC-CA-BACKEND-03 including a null R-multiple row (Feb 2026).

**Acceptance criteria:**
- [x] SC-CA-BACKEND-01 authored and registered
- [x] SC-CA-BACKEND-02 authored and registered
- [x] SC-CA-BACKEND-03 authored and registered
- [x] Covers: period toggle behaviour, insufficient data state, column value correctness
- [x] Spec references: `analytics.md §15`, `analytics_endpoints.md#GET /analytics/cohort`
- [ ] Director of Quality sign-off required

**QA findings for ST-20:** *(Director of Quality to complete)*

**Disposition for ST-20:** *(Director of Quality: Pass / Pass with notes / Fail)*

---

**QA test coverage (full EPIC-05):**
- Scenarios run: Manual acceptance review for ST-14/15/16/17; `docs/testing/analytics_scenarios.md` for ST-20
- Regression areas checked: DB migration governance, deployment process, data model documentation, spec coverage, analytics CohortAnalysis panel
- Known deviations filed: ST-20 cross-branch process deviation (content correct, committed on EPIC-04 branch — not a spec deviation)

**QA sign-off block:** *(Director of Quality completes this — after ST-20 disposition is recorded above)*
> **Authoring note:** When completing the sign-off block, update all AC table rows from "Pending" to "Pass" or "Pass with notes" in the same edit.
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] ST-20 disposition recorded in section above
- [ ] Regression areas checked
- Signed off by: Director of Quality
- Date:
- Comments:
