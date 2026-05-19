Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-19
Cycle: 2026-05-18__release-v3.7

---

# Lessons Learnt Closure Record — 2026-05-18__release-v3.7

**Phase:** Post-Ship Closure
**Cycle:** 2026-05-18__release-v3.7
**Generated:** 2026-05-19
**Records reviewed:** lessons_learnt.md (Release Planning), lessons_learnt_cycle.md §Phase 3 (Sprint Execution), lessons_learnt_cycle.md §Phase 4 (Delivery Verification)

---

## Closure-Phase Observations

1. **Missing v3.6 changelog entry:** `docs/product/changelog.md` Last Updated was 2026-05-15 (v3.5 entry) — no v3.6 entry present. The v3.6 post-ship closure was incomplete (confirmed by memory record project_v36_post_ship.md). The v3.7 entry was added. The v3.6 entry is flagged as an outstanding action — PMO Lead must reconstruct from v3.6 cycle artefacts.

2. **Missing v3.6 velocity row:** `claude/cycles/velocity_metrics.md` had no v3.6 row (last row was v3.5). Row added with best-available data (Planned=7, Completed=7, Velocity=1.00) from memory record and sprint_close context.

3. **Stale validation_system.md governance note:** `docs/operations/validation_system.md` contained a ⚠️ governance note about the "Platform Team" owner field being non-compliant. The owner field was corrected to `Infrastructure & Operations Owner` in v1.9 ST-19 (2026-03-09). The stale note was removed. No functional impact.

4. **qa_evidence_template.md Result column placeholder gap:** Phase 4 LL identified that the Result column placeholder "Pending DoQ" was not updated to "Pass" when retrospective sign-off was applied to EPIC-01. Immediate fix applied (v1.1→v1.2): Result column note added explicitly identifying "Pending DoQ" as a pre-signing placeholder. The existing v1.1 Authoring note covered sign-off block consistency; the new v1.2 note makes the placeholder rule explicit at the column level.

5. **Zero deviation compliance items:** No spec deviations were filed this sprint. STEP 5 deviation compliance check = N/A.

6. **No Phase 4 backlog additions:** Verification report §6 confirmed no test scenario gaps. No new backlog entries required from this closure run.

---

## Lessons Learnt Action Summary

### Records Reviewed

| Record | Actions Reviewed |
|--------|-----------------|
| lessons_learnt.md (Release Planning) | 4 action items |
| lessons_learnt_cycle.md Phase 3 (Sprint Execution) | 2 outstanding actions + 4 friction items (all classified) |
| lessons_learnt_cycle.md Phase 4 (Delivery Verification) | 1 friction item |

---

### Immediate Actions Applied (1)

| # | Action | Document updated | Version bump | Notes |
|---|--------|-----------------|--------------|-------|
| 1 | Add Result column placeholder note to qa_evidence_template.md | claude/system/templates/qa_evidence_template.md | v1.1 → v1.2 | Friction item from Phase 4 LL: "Pending DoQ" pre-signing placeholder must be updated before sign-off block is completed. New column-level note added to Consolidation Block table. |

---

### Deferred to Next Cycle (4)

| # | Action | Owner | Target cycle | Source record |
|---|--------|-------|--------------|---------------|
| 1 | Smoke-tests.yml timeout increase (15→25 min) if CI timeout recurs on a subsequent PR | QA & Testing Owner | v3.8 (if recurrence observed) | Phase 3 LL OA-1 |
| 2 | Enforce DoQ sign-off date recorded before PR merge — consider PR checklist item or pre-merge comment template | Director of Quality | v3.8 | Phase 3 LL OA-2 |
| 3 | Sprint Planning: confirm sub-step 10a present in execution_prompt.md before execution begins | Sprint Planning Engine | v3.8 | RP LL Action-1 (carry-forward; now resolved for v3.7 by ST-07) |
| 4 | Sprint Execution: flag BLG-GOV-19 class eligibility for all observable-AC stories | Sprint Execution Engine | v3.8 | RP LL Action-2 (carry-forward; applied in v3.7 EPIC-03) |

---

### Decision Required (1)

| # | Decision question | Owner | Deadline | Source record |
|---|------------------|-------|----------|---------------|
| 1 | PT-04 gate (20+ closed trades) not met at v3.7 sprint planning (two consecutive conditional defers: v3.6 and v3.7). Evaluate: (a) carry as conditional scope again for v3.8, or (b) formally park PT-04 as "pending gate" until the PO confirms the condition is met, rather than including in every release plan. | Product Owner | 2026-05-22 (72h from post-ship closure) | RP LL Action-4 |

---

## Carry-Forward

| Item | Type | Owner | Target | Notes |
|------|------|-------|--------|-------|
| PT-04 gate decision (park vs conditional) | Decision Required | Product Owner | Before v3.8 release planning opens | 72h deadline from 2026-05-19 |
| DoQ sign-off date enforcement before PR merge | Deferred | Director of Quality | v3.8 | Pre-merge date recording compliance |
| Smoke-tests.yml timeout review | Deferred | QA & Testing Owner | v3.8 if recurrence | Advisory — trigger is recurrence |
| v3.6 changelog entry reconstruction | Outstanding Action | PMO Lead | Before v3.8 closes | From incomplete v3.6 post-ship closure |

---

// ARTEFACT_STATUS
{
  "phase": "Post-Ship Closure",
  "cycle_id": "2026-05-18__release-v3.7",
  "status": "complete",
  "generated_utc": "2026-05-19T00:00:00Z"
}
