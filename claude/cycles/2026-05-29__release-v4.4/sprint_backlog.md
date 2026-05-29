**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4
**Release:** v4.4
**Sprint Goal:** Apply all 5 governance patches carried forward from v4.3 and produce the SI-02 pre-planning artefacts that unlock the Behavioural Drift Detection implementation sprint.
**Backlog Slice Source:** original — `claude/cycles/2026-05-29__release-v4.4/stage4_backlog_slice.md`

# Sprint Backlog — 2026-05-29__release-v4.4

---

## Sprint Scope

### Merge Order

**Sprint 1:** EPIC-01 → EPIC-04

**Sprint 2:** EPIC-02 → EPIC-03

**execution_state.json owner:** EPIC-01 (first in execution order). EPIC-02, EPIC-03, and EPIC-04 must check for file existence before creating — append their section rather than overwrite.

**Shared file advisory:**
- `claude/system/OPERATIONAL_GUIDE.md` — modified by both EPIC-01 and EPIC-04. EPIC-04 must rebase onto main after EPIC-01 merges before finalising its changes.
- `claude/system/prompt_change_log.md` — same as above; EPIC-04 rebases after EPIC-01.
- `docs/specs/si02/` — modified by EPIC-02 and EPIC-03 (different files; no conflict expected; advisory only).

---

## Sprint 1

### EPIC-01 — Governance Prompt Patches

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Estimated effort:** ~2.5 hrs (5 × XS)
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Apply BLG-GOV-71: roadmap_prompt.md STEP 8.1 advisory for empty Now horizon

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** 3rd recurrence (v4.1/v4.2/v4.3). Carry-forward item from v4.3 lessons_learnt_closure.md. RISK-01 applies — governance edit checklist (CLAUDE.md §6) required in commit.

**Staging-only ACs:** None

---

#### ST-02 — Apply BLG-GOV-72: sprint_planning_prompt.md frontend classification fast-path

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (independent of ST-01)

**Notes:** 3rd consecutive sprint (v4.1/v4.2/v4.3 EPIC-04 misclassified). Carry-forward item from v4.3 lessons_learnt_closure.md. Must be committed before Sprint 2 EPIC-03 stories execute (though classification of Sprint 2 stories is unaffected — see sprint_planning_notes.md carry-forward advisory).

**Staging-only ACs:** None

---

#### ST-03 — Apply BLG-GOV-73: execution_prompt.md auto-set deviations_filed on delegation clearance

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None (independent of ST-01/02)

**Notes:** RISK-01 applies — governance edit checklist required. execution_prompt.md v3.32 → v3.33.

**Staging-only ACs:** None

---

#### ST-04 — Apply BLG-GOV-69 + BLG-GOV-74: qa_evidence_template.md delegated_qa sign-off format

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None (independent of ST-01/02/03)

**Notes:** Dual-source: BLG-GOV-69 (v4.3 delivery verification) + BLG-GOV-74 (v4.3 post-ship). Template update only — no enforcement change.

**Staging-only ACs:** None

---

#### ST-05 — Apply release_planning_prompt.md STEP 7 RESUME PRECHECK patch

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None (independent)

**Notes:** Source: v4.3 lessons_learnt.md LL-2 (no separate BLG item). release_planning_prompt.md v2.31 → v2.32. RISK-01 applies.

**Staging-only ACs:** None

---

### EPIC-04 — Ops Documentation Hardening

**Maps to:** S2-04
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** ~0.5 hrs (1 × XS)
**Risk IDs:** RISK-04
**Execution sequence:** 2 (after EPIC-01 merges; must rebase on OPERATIONAL_GUIDE.md changes)

#### ST-13 — Staging URL disambiguation in OPERATIONAL_GUIDE §7 (BLG-OPS-43)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None (independent of EPIC-01 content; branch must rebase after EPIC-01 merges to avoid OPERATIONAL_GUIDE.md conflict)

**Notes:** RISK-04 (thin EPIC — merge early). OPERATIONAL_GUIDE is Class 6; governance edit checklist (CLAUDE.md §6) applies. EPIC-04 branch must be rebased onto main after EPIC-01 merges before opening PR.

**Staging-only ACs:** None

---

## Sprint 2

### EPIC-02 — SI-02 Backend Pre-Planning

**Maps to:** S2-02
**Owner:** Head of Backend Engineering; Head of Engineering
**Estimated effort:** ~24–32 hrs (2 × M + 1 × S + 1 × S conditional)
**Risk IDs:** RISK-02
**Execution sequence:** 3

#### ST-06 — SI-02 drift detection query pre-design (BLG-BE-17)

**Owner:** Head of Backend Engineering
**Estimated effort:** M (~8–12 hrs)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None (first in EPIC-02 sequence)

**Notes:** Output: `backend/docs/si02_query_predesign.md` (or equivalent under `docs/specs/si02/`). Gate input for ST-09. RISK-02 applies — if pre-design reveals scope gaps, ST-09 may be blocked.

**Staging-only ACs:** None

---

#### ST-07 — Arc 5 backend architecture review for SI query patterns (BLG-BE-18)

**Owner:** Head of Engineering; Head of Backend Engineering
**Estimated effort:** M (~8–12 hrs)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None (may proceed in parallel with ST-06)

**Notes:** Output: `docs/specs/si02/arc5_backend_architecture_review.md` (or equivalent). ADR filed if background layer recommended. Gate input for ST-09.

**Staging-only ACs:** None

---

#### ST-08 — SI-02 query index pre-assessment (BLG-BE-23)

**Owner:** Head of Engineering; Head of Backend Engineering
**Estimated effort:** S (~4–6 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** BLG-GOV-51 ✅ shipped v4.1 (EXPLAIN ANALYZE results available)

**Notes:** Output: `docs/specs/si02/si02_index_preassessment.md` (or equivalent). Uses BLG-GOV-51 results — external dependency confirmed shipped.

**Staging-only ACs:** None

---

#### ST-09 — SI-02 background job architecture design (BLG-BE-20) *(Conditional)*

**Owner:** Head of Backend Engineering; Head of Engineering
**Estimated effort:** S (~4–6 hrs)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** ST-06 (BLG-BE-17) and ST-07 (BLG-BE-18) outputs available; SI-02 sprint scope beginning to crystallise

**gate_condition:** ST-06 + ST-07 outputs reviewed before commencing

**Notes:** Output: `docs/specs/si02/si02_background_job_adr.md` (or equivalent). CONDITIONAL — only proceeds after gate condition met. If gate condition met mid-sprint, invoke amendment cycle to formally add to backlog (do not add informally). Gate input for ST-12.

**Staging-only ACs:** None

---

### EPIC-03 — SI-02 Frontend & QA Pre-Planning

**Maps to:** S2-03
**Owner:** Frontend Specs & UX Documentation Owner; QA & Testing Owner; Director of Quality
**Estimated effort:** ~12–18 hrs (3 × S; ST-12 conditional)
**Risk IDs:** RISK-03
**Execution sequence:** 4 (after EPIC-02; ST-10 before ST-11; ST-12 conditional on ST-09)

#### ST-10 — SI-02 drift detection result component pre-design (BLG-FE-52)

**Owner:** Base44 Frontend; Frontend Specs & UX Documentation Owner
**Estimated effort:** S (~4–6 hrs)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None (first in EPIC-03; gate: SI-02 sprint planning imminent ✅)

**Notes:** Output: `docs/specs/si02/si02_fe_component_predesign.md` (or equivalent). Must complete before ST-11 starts. RISK-03 applies.

**Staging-only ACs:** None

---

#### ST-11 — SI-02 drift detection interaction spec (BLG-FE-53)

**Owner:** Frontend Specs & UX Documentation Owner
**Estimated effort:** S (~4–6 hrs)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** ST-10 (BLG-FE-52) — component interface output required before spec can be authored

**Notes:** Output: `docs/specs/si02/si02_fe_interaction_spec.md` (or equivalent). Hard sequential dependency on ST-10. RISK-03 applies.

**Staging-only ACs:** None

---

#### ST-12 — SI-02 Playwright scenario pre-design (BLG-QA-31) *(Conditional)*

**Owner:** QA & Testing Owner; Director of Quality
**Estimated effort:** S (~4–6 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** ST-09 (BLG-BE-20) architecture output; ST-10 and ST-11 drift surfaces defined

**gate_condition:** ST-09 architecture output reviewed before commencing

**Notes:** Output: `docs/qa/si02_playwright_predesign.md` (or equivalent). CONDITIONAL — only proceeds after gate condition met. If gate met mid-sprint, invoke amendment cycle. Director of Quality must record confirmation in delivery note (AC-03).

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (2 sprints) | ~40–60 hrs |
| Total estimated effort (Sprint 1) | ~3 hrs |
| Total estimated effort (Sprint 2) | ~36–50 hrs |
| Total estimated effort (all in-scope) | ~39–53 hrs |
| Utilisation | ~80–90% of 2-sprint envelope |
| Over-allocation | No (within 2-sprint envelope); Sprint 2 alone is at capacity boundary |

---

## Items Deferred This Sprint

No items deferred — all 13 backlog slice stories are included (2 conditional):

| Item | EPIC | Status |
|------|------|--------|
| ST-09 (BLG-BE-20) | EPIC-02 | Conditional — gate: ST-06+07 outputs |
| ST-12 (BLG-QA-31) | EPIC-03 | Conditional — gate: ST-09 + ST-10/11 |

---

## Deferred Execution Blockers Accepted

*(Section omitted — `deferred_execution_blockers` was empty in state.json)*

---

## Outstanding Actions at Planning Seal

| # | Action | Owner | Blocker? |
|---|--------|-------|---------|
| OA-1 | Populate `design_gate_bypass_authority` and `design_gate_bypass_reason` in `.claude_current_state.json` | Head of UX & Design + Product Owner | Resolved — 2026-05-29 |
| OA-2 | Explicit Product Owner acknowledgement of capacity WARN | Product Owner | Resolved — 2026-05-29 |
| OA-3 | Product Owner sprint goal confirmation and full sprint backlog sign-off | Product Owner | Resolved — 2026-05-29 |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — 13 stories / 4 EPICs / 2 sprints (2 conditional: ST-09, ST-12)
**Capacity confirmed:** Confirmed — WARN acknowledged; Sprint 2 heavy but within 2-sprint envelope
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-05-29
