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

**Spec reference:** `docs/ops/api_performance_baseline.md#18`  
**Commit SHA:** bf56a296  
**Classification:** delegated_backend  

**What was built:** §18 added to `docs/ops/api_performance_baseline.md`. 16 read endpoints measured on production with 7 samples each. 7 write operations documented as excluded per methodology. 4 high-latency flags raised (concentration-status p95=5,917ms, behavioural-drift p95=3,798ms, red-flag-journal p95=3,200ms, research p95=4,601ms). BLG-OPS-62/63/64 filed. BLG-OPS-22 gate cleared.

**Acceptance criteria:**
- [x] All 24 BLG-OPS-13 scope endpoints actioned (16 measured + 7 write-op exclusions per methodology + 1 AI inference exclusion)
- [x] p50/p95/p99 measurements recorded for all eligible read endpoints
- [x] Infrastructure & Operations Owner sign-off — cleared §18.4

**Result:** Pass  
**Deviations:** None

---

## ST-07 — v5.1–v5.4 endpoint baseline extension

**Spec reference:** `docs/ops/api_performance_baseline.md#19`  
**Commit SHA:** bf56a296  
**Classification:** delegated_backend  

**What was built:** §19 added to `docs/ops/api_performance_baseline.md`. GET /watchlist p50=488ms/p95=540ms and GET /portfolio/gate-metrics p50=543ms/p95=581ms measured on production. POST /digest/si05/send excluded — Telegram API dependency causes client-side timeout; documented as external-dependency exclusion.

**Acceptance criteria:**
- [x] v5.1–v5.4/v5.5 endpoints added with measurements
- [x] Infrastructure & Operations Owner sign-off — cleared §19.2

**Result:** Pass  
**Deviations:** None

---

## ST-08 — POST /digest/si05/send to api_performance_baseline.md

**Spec reference:** `docs/ops/api_performance_baseline.md#19`  
**Commit SHA:** bf56a296  
**Classification:** delegated_backend  

**What was built:** POST /digest/si05/send documented in §19.1 as an external-dependency exclusion — the endpoint blocks on Telegram Bot API and times out from any external measurement client. Consistent with generate-thesis exclusion in §15 and §18.2.

**Acceptance criteria:**
- [x] POST /digest/si05/send present in baseline document with disposition noted
- [x] Infrastructure & Operations Owner sign-off — cleared §19.2

**Result:** Pass (trivially complete — covered by ST-07 §19)  
**Deviations:** None

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
| ST-06 | api_performance_baseline.md#18 | §18: 16 endpoints measured on production; BLG-OPS-62/63/64 filed | 24 scope endpoints actioned; I&O sign-off | Pass | None |
| ST-07 | api_performance_baseline.md#19 | §19: GET /watchlist + GET /portfolio/gate-metrics measured | v5.1–v5.5 endpoints added; I&O sign-off | Pass | None |
| ST-08 | api_performance_baseline.md#19 | §19.1: POST /digest/si05/send documented as external-dependency exclusion | Row present with disposition; I&O sign-off | Pass | None |

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
