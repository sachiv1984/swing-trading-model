Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-11

---

# QA Evidence — EPIC-03: API Baseline & Documentation Clearance

**Cycle:** 2026-06-10__release-v5.5

---

## ST-09 — Formal regression test suite baseline document

**Spec reference:** `docs/qa/regression_test_suite_baseline.md` (deliverable IS the spec)  
**Commit SHA:** e8855d01  
**Classification:** autonomous  

**What was built:** Created `docs/qa/regression_test_suite_baseline.md` — a formal baseline document mapping all 66 entries in `backend/routers/test.py` to features with version history, and listing all 41 `tests/e2e/*.spec.js` files with per-file scenario counts (387 total) and feature mapping. Document also includes coverage by arc and known gap disclosures.

**Acceptance criteria:**
- [x] Formal regression baseline document created in docs/qa/ — `docs/qa/regression_test_suite_baseline.md`
- [x] All backend/routers/test.py entries (66) mapped to features with version history — Part 1 table
- [x] All tests/e2e/*.spec.js files (41) listed with scenario count and feature mapping — Part 2 table
- [x] Director of Quality sign-off — cleared via agent-mediated sign-off (findings applied: total scenario count corrected from 441 to 387)

**Result:** Pass  
**Deviations:** None

---

## ST-10 — User journey map: SI-05 Telegram digest to app action

**Spec reference:** `claude/cycles/2026-06-10__release-v5.5/sprint_backlog.md#ST-10` (AC-defined)  
**Classification:** delegated_qa  
**Assigned to:** Head of UX & Design  
**Delegation record:** DEL-20260611-04  
**Status:** Pending — blocked_qa awaiting Head of UX & Design completion  

**What is needed (for Head of UX & Design):**
Perform a live walkthrough of the SI-05 Telegram digest → app action flow. Produce a user journey map document covering:
1. Entry points: every link or reference in the SI-05 digest that points to an app action
2. Navigation steps: the clicks/taps required to reach the relevant app screen from each entry point
3. Friction findings: any navigation steps that are unclear, broken, or slow
File any significant friction as a separate backlog item. Sign off on the document once complete.

**Acceptance criteria:**
- [ ] User journey map document produced with entry points, navigation steps, friction findings
- [ ] Any significant friction filed as separate backlog items
- [ ] Head of UX & Design sign-off

**Test scenarios to execute:** AC-1 requires live walkthrough of Telegram digest → app navigation. No automated test applicable — this is a manual UX review.

**Result:** Pending  
**Deviations:** N/A (pending)

---

## ST-06 — v2.8–v4.6 endpoint performance baseline re-run (24 endpoints)

**Spec reference:** `docs/ops/api_performance_baseline.md`  
**Classification:** delegated_backend  
**Assigned to:** Infrastructure & Operations Owner  
**Delegation record:** DEL-20260611-01  
**Status:** Pending — blocked_backend awaiting Infrastructure & Operations Owner  

**Acceptance criteria:**
- [ ] All 24 endpoints from v2.8–v4.6 added to docs/ops/api_performance_baseline.md with p50/p95/p99 measurements from live/staging environment
- [ ] Infrastructure & Operations Owner sign-off

**Result:** Pending  
**Deviations:** N/A (pending)

---

## ST-07 — v5.1–v5.4 endpoint baseline extension

**Spec reference:** `docs/ops/api_performance_baseline.md`  
**Classification:** delegated_backend  
**Assigned to:** Infrastructure & Operations Owner  
**Delegation record:** DEL-20260611-02  
**Status:** Pending — blocked_backend awaiting Infrastructure & Operations Owner (sequence after ST-06)  

**Acceptance criteria:**
- [ ] v5.1–v5.4 endpoints added to api_performance_baseline.md with measurements from live environment
- [ ] Infrastructure & Operations Owner sign-off

**Result:** Pending  
**Deviations:** N/A (pending)

---

## ST-08 — POST /digest/si05/send to api_performance_baseline.md

**Spec reference:** `docs/ops/api_performance_baseline.md`  
**Classification:** delegated_backend  
**Assigned to:** Infrastructure & Operations Owner  
**Delegation record:** DEL-20260611-03  
**Status:** Pending — blocked_backend awaiting Infrastructure & Operations Owner (sequence after ST-07)  

**Acceptance criteria:**
- [ ] POST /digest/si05/send present in api_performance_baseline.md with p50/p95/p99 from live/staging environment
- [ ] Infrastructure & Operations Owner sign-off

**Result:** Pending  
**Deviations:** N/A (pending)

---

## EPIC-Level Consolidation Block

*(To be completed when all ST items reach terminal status — pending ST-06/07/08 backend delegation and ST-10 UX delegation.)*

**EPIC:** EPIC-03 — API Baseline & Documentation Clearance  
**Cycle:** 2026-06-10__release-v5.5  
**Sprint goal:** Resolve all three v5.4 governance carry-forwards, deliver visible trade data density tracking, clear the long-outstanding API performance baseline backlog, and package the SI-05 effectiveness review suite ready for post-2026-07-04 gate execution.  
**Test scenarios used:** `docs/qa/regression_test_suite_baseline.md` (ST-09 deliverable)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-09 | docs/qa/regression_test_suite_baseline.md | Regression baseline doc — 66 endpoints, 41 e2e specs | Doc created; all entries mapped; DoQ sign-off | Pass | None |
| ST-10 | sprint_backlog.md#ST-10 | User journey map (pending) | Journey map + friction items + UX sign-off | Pending | N/A |
| ST-06 | docs/ops/api_performance_baseline.md | 24 endpoint rows (pending) | All rows with p50/p95/p99; I&O sign-off | Pending | N/A |
| ST-07 | docs/ops/api_performance_baseline.md | v5.1–v5.4 endpoint rows (pending) | All rows with measurements; I&O sign-off | Pending | N/A |
| ST-08 | docs/ops/api_performance_baseline.md | POST /digest/si05/send row (pending) | Row with measurements; I&O sign-off | Pending | N/A |

**QA test coverage:**
- Scenarios run: Agent-mediated DoQ review for ST-09 (code review + completeness check). ST-06/07/08/10: live environment and manual walkthrough required — pending delegation completion.
- Regression areas checked: Documentation completeness (ST-09 only at this stage)
- Known deviations filed: None

**DoQ Sign-Off Block:**

*(Pending — must be completed when all ST items are done and before PR is opened. Mixed-class EPIC: delegated_backend + autonomous + delegated_qa stories present. Autonomous class (BLG-GOV-19) does not apply.)*

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- Signed off by: Director of Quality
- Date: *[to be completed]*
- Comments: *[to be completed — include reference to story-level sign-offs from Infrastructure & Operations Owner and Head of UX & Design]*
