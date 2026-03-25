Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-25

---

# QA Evidence Log — EPIC-05 (Governance & QA Process)

**Cycle:** 2026-03-24__release-v2.3
**Sprint goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.

---

## ST-14 — BLG-GOV-07: Reinforce Backend Branch Discipline

**Spec reference:** `claude/system/execution_prompt.md#13. Governance Invariants`
**Commit:** c7397cd (main — v2.2 post-ship closure); EPIC-05 branch record commit 5820d29
**Classification:** autonomous (pre-completed)

**What was built:** Backend branch discipline invariant was added to `execution_prompt.md §13 Governance Invariants` as part of the v2.2 post-ship closure (commit c7397cd, LL-v2.2-EX-03). The §6 checklist was fully applied: version bumped to v2.7, OPERATIONAL_GUIDE §14 updated, prompt_change_log.md entry appended. No additional changes required in v2.3.

**Acceptance criteria:**
- [x] `execution_prompt.md` §13 Governance Invariants updated with backend branch discipline guidance — **verified: present at line 932 in v2.7**
- [x] §6 checklist applied: version bumped (v2.7), OPERATIONAL_GUIDE §14 updated (v2.7), phase section header updated (§8 in OG), prompt_change_log.md entry appended — **verified: all four items present**
- [x] One commit per CLAUDE.md §6 checklist — **confirmed: c7397cd**

**Test scenarios:** Governance/documentation change. No runtime scenarios required.

**Deviations:** None.

---

## ST-15 — BLG-QA-03: Canonical Test Execution Report Template

**Spec reference:** No prior canonical spec.
**Commit:** Pending — delegated to QA Lead (DEL-20260325-12)
**Classification:** delegated_qa

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] Template document present and usable in `docs/testing/`
- [ ] Template includes all mandatory fields (scenario list, pass/fail, deviation notes, DoQ block)
- [ ] Template is usable for both manual and automated test runs
- [ ] Template referenced in QA governance documentation

**Test scenarios:** *N/A — documentation artefact.*

**Deviations:** *To be assessed at delivery verification.*

---

## ST-16 — BLG-QA-04: Integration Test Coverage Report

**Spec reference:** `docs/reference/openapi.yaml`
**Commit:** Pending — delegated to Director of Quality (DEL-20260325-13)
**Classification:** delegated_qa

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] CI-generated coverage report against openapi.yaml endpoints
- [ ] Report format: machine-readable or human-readable
- [ ] Coverage gaps visible to DoQ during sign-off
- [ ] Wired into CI

**Test scenarios:** *N/A — tooling/reporting artefact.*

**Deviations:** *To be assessed at delivery verification.*

---

## ST-17 — BLG-GOV-08: Engine Prompt Compression (Conditional)

**Classification:** delegated_decision (conditional stretch)
**Status:** Blocked — ESC-EXEC-20260325-01 filed. Conditional on ST-13 + ST-16 complete and Sprint 3 residual capacity. Does not block v2.3 release.

---

## EPIC-05 Consolidation Block

*(To be completed when all non-conditional ST items are done — pending ST-15 and ST-16)*

**EPIC:** EPIC-05 — Governance & QA Process
**Cycle:** 2026-03-24__release-v2.3
**Sprint goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-14 | execution_prompt.md#13. Governance Invariants | Backend branch discipline invariant in §13 v2.7 | Guidance present, §6 checklist applied | Pass | None |
| ST-15 | N/A (no prior spec) | Test execution report template | Template present, all fields, referenced in governance | Pending | TBD |
| ST-16 | openapi.yaml | CI integration test coverage report | Coverage report generated, gaps visible | Pending | TBD |
| ST-17 | N/A | Engine prompt compression (conditional) | HoST design + capacity gate | Conditional | N/A |

**QA test coverage:**
- Scenarios run: Governance/documentation items — no scenario files required.
- Regression areas checked: execution_prompt.md §13 governance invariants.
- Known deviations filed: None.

**QA sign-off block:** *(Director of Quality completes this when ST-15 and ST-16 are done)*
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction: confirm base URL variable exposed
- Signed off by: Director of Quality
- Date:
- Comments:
