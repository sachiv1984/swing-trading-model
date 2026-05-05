**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Filed
**Last Updated:** 2026-05-05
**Cycle:** 2026-04-29__release-v3.1
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Invoking routine:** post_ship_closure.md
**Prior cycle lessons_learnt_closure.md:** claude/cycles/2026-04-25__release-v3.0/lessons_learnt_closure.md — loaded for recurrence check

---

# Lessons Learnt Closure Record — 2026-04-29__release-v3.1

---

## 1. Cross-Cycle Recurrence Check

Prior cycle lessons_learnt_closure.md (2026-04-25__release-v3.0) loaded. Carry-forward items reviewed:

| CF Item | Description | Status in v3.1 |
|---------|-------------|----------------|
| CF-01 | execution_prompt §3.1.A reclassification backfill instruction | ✅ RESOLVED — delivered as ST-13 (EPIC-04, PR #323) |
| CF-02 | execution_prompt STEP 8.5 output target fix | ✅ RESOLVED — delivered as ST-14 (EPIC-04, PR #323) |
| CF-03 | Playwright waitFor pattern (`networkidle` → `waitFor` for CI stability) | ⚠ Not addressed in v3.1 — no Playwright authoring scope this cycle. Carries forward to v3.2. |

**Outcome:** 2/3 carry-forward items resolved. 1 item (CF-03) carries forward.

---

## 2. Closure Phase Observations

**Document closure friction:** None. All required artefacts were located without difficulty. The exception is the scope document (`docs/product/scope/scope--2026-04-29__release-v3.1-arc-2-trade-plan-foundation.md`) which could not be found — flagged as outstanding action in closure_record.md §6. This is a process gap from release planning: scope document was not created at plan time.

**Lessons learnt action application rate:** 0/4 applicable deferred items applied immediately (all deferred to v3.2 as requiring sprint_planning_prompt.md / execution_prompt.md patches). No immediate-class items were identified.

**Closure step gaps detected:** The scope document absence is a gap that should have been caught at release planning STEP 4 (scope document authoring) or sprint planning. Filed as outstanding action OA-01 in closure_record.md.

---

## 3. Consolidated Action Summary (from STEP 8 Lessons Learnt Review)

**Records reviewed:** lessons_learnt.md (Release Planning), lessons_learnt_cycle.md (Phase 3 Sprint Execution + Phase 4 Delivery Verification)

### Immediate actions applied: 0

No immediate-class items identified. Both CF-01 and CF-02 patches from the prior cycle were already delivered as sprint stories (ST-13/ST-14) rather than arising during post-ship closure — this is the correct pattern: governance patches tracked as explicit sprint stories rather than ad-hoc closure fixes.

### Deferred to next cycle: 4

| # | Action | Owner | Target Cycle | Source |
|---|--------|-------|--------------|--------|
| D-01 | Add STEP 0 branch check to sprint_planning_prompt.md: verify current branch is main before committing planning artefacts. Sprint planning was done on an orphaned EPIC branch (exec/2026-04-25__release-v3.0/EPIC-02) — artefacts had to be recovered at sprint close | Head of Specs Team | v3.2 | Phase 3 friction item |
| D-02 | Add runtime check at execution_prompt.md STEP 5.1: verify `deviations_filed = true` for all done items at sprint close; auto-correct if no deviation found and log correction | Head of Specs Team | v3.2 | Phase 3 friction item |
| D-03 | Add post-story execution advisory to execution_prompt.md §3.1.A: after any story that creates test files, populate test_scenarios before moving to next story (RECURRENCE from v3.0 TSG-v30-01) | Head of Specs Team | v3.2 | Phase 4 friction item (recurrence) |
| D-04 | Adopt Playwright `waitFor` pattern in place of `networkidle` for CI stability (carried from v3.0 CF-03) | QA & Testing Owner | v3.2 | Prior cycle carry-forward CF-03 |

### Escalated for decision: 0

None.

---

## 4. Recurrence Analysis

**D-01 (orphaned branch):** New in v3.1 — not a recurrence from v3.0. Root cause: sprint_planning_prompt.md has no branch verification step.

**D-02 (deviations_filed field):** New in v3.1 — not a recurrence from v3.0. Root cause: execution_prompt.md initialises `deviations_filed = false` and has no explicit enforcement at sprint close.

**D-03 (test_scenarios backfill):** RECURRENCE from v3.0 TSG-v30-01. The v3.0 disposition was `not_applicable` (functional tests existed; administrative gap only). v3.1 shows the same pattern for two EPICs (TSG-v31-01 and TSG-v31-03). CF-01 delivery (ST-13) addressed the reclassification path only — the post-story execution path remains unaddressed. This is a recurring process gap warranting a concrete execution_prompt.md patch in v3.2. Not an automatic escalation because v3.0 was not an open outstanding action (it was not_applicable).

**D-04 (Playwright waitFor):** Recurrence from v3.0 CF-03. No Playwright authoring occurred in v3.1 so the opportunity to apply this was absent. Remains carry-forward.

---

## Carry-Forward
Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | sprint_planning_prompt.md has no branch verification step — planning artefacts can be committed to a non-main branch, causing recovery work at sprint close and verification preflight | Sprint Planning Engine should add STEP 0 main-branch check before any artefact commits; prevents orphaned artefact recovery | Sprint Planning |
| 2 | execution_prompt.md §3.1.A post-story advisory for test_scenarios backfill is missing — tests created during story execution are not registered until closure, creating recurring TSG gaps (v3.0 + v3.1) | Sprint Planning and execution prompts should enforce test_scenarios registration as part of story completion, not retrospectively | Sprint Planning |
| 3 | Playwright `waitFor` adoption deferred from v3.0 (CF-03) — `networkidle` pattern remains in existing specs; CI flakiness risk on SDK-heavy pages | At next Playwright authoring or test maintenance session, update all `waitForLoadState('networkidle')` to explicit `waitFor` element conditions | Sprint Planning |
