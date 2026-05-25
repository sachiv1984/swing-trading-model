**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-25
**Cycle:** 2026-05-22__release-v4.0
**Produced by:** Post-Ship Closure Engine (lessons_learnt_prompt.md §3.5)

---

# Lessons Learnt Closure Record — 2026-05-22__release-v4.0

## Purpose

This record consolidates all lessons learnt across the v4.0 release cycle — Release Planning, Sprint Execution, Delivery Verification, and Amendment phases — and documents the classification and disposition of every action item. It is the governance record of process learning applied (or carried forward) at cycle close.

---

## Records Reviewed

| Record | File | Phase(s) | Items Identified |
|--------|------|----------|-----------------|
| Release Planning lessons | `claude/cycles/2026-05-22__release-v4.0/lessons_learnt.md` | Release Planning | 2 observations (LP-01, LP-02); 0 carry-forward actions |
| Sprint Execution + Verification lessons | `claude/cycles/2026-05-22__release-v4.0/lessons_learnt_cycle.md` | Phase 3 + Phase 4 | 5 Phase 3 items (3 type C/A deferred, 2 type E action-now); 4 Phase 4 items (2 type C/A deferred, 1 type C deferred, 1 type E action-now) |

Prior cycle closure record checked: `claude/cycles/2026-05-21__release-v3.9/lessons_learnt_closure.md` — not found (v3.9 post-ship was executed from hotfix branch, closure record may have been on that branch). No prior closure recurrence check possible — noted.

---

## Action Item Classification

### Release Planning (lessons_learnt.md)

| ID | Observation | Classification | Disposition |
|----|-------------|----------------|-------------|
| LP-01 | v3.9 post-ship artefacts stranded on unmerged hotfix branch — caused STEP -1.6 hard gate at v4.0 planning; resolved by git archaeology | action-now | Positive advisory: always verify `git log --oneline origin/main | head -3` confirms closure commit landed before ending session. No template change needed — advisory only. |
| LP-02 | Both hotfix and main branches independently claimed OPERATIONAL_GUIDE v4.00 — version collision resolved by §8 union rule | action-now | Positive: §8 union rule validated. No process change needed — confirms existing policy works. |

Both Release Planning items are observations requiring no deferred action or template patch.

### Sprint Execution — Phase 3 (lessons_learnt_cycle.md)

| friction_item | type | classification | Disposition |
|---------------|------|----------------|-------------|
| merge_gate stale on resume (2nd recurrence v3.9+v4.0) — epics_merged remained [] until STEP 4 sync after user merges via GitHub UI between sessions | C | defer → ESCALATED | **Deferred.** Head of Specs Team to add STEP 4 merge-gate re-invocation requirement as hard gate in execution_prompt.md. v4.1 target. Outstanding action OA-01. |
| Staging-only AC designation retrospective (2nd recurrence v3.9+v4.0) — 4 staging-only ACs surfaced at execution (ST-02/04, ST-05, ST-09, ST-12) rather than at sprint planning | A | defer → ESCALATED | **Deferred.** Head of Specs Team to add staging-only evidence AC designation guidance to sprint_planning_prompt.md + sprint_backlog.md template. v4.1 target. Outstanding action OA-02. |
| AMD-20260523-01 amendment cleanly executed — ST-12 prereq + ST-13 emergency CVE fix added without scope disruption | E | action-now | No change — validated pattern recorded. |
| ST-05 delegation (DEL-20260524-01) resolved same sprint day | E | action-now | No change — validated pattern recorded. |
| Sprint close not executed immediately after EPIC-03 merge — STEP -1.1 recovery path triggered at delivery verification invocation | C | defer | **Deferred.** PMO Lead to confirm sprint_close_reminder.yml PR comment is firing after each EPIC merge. v4.1 target. Consolidated into OA-03. |

### Delivery Verification — Phase 4 (lessons_learnt_cycle.md)

| friction_item | type | classification | Disposition |
|---------------|------|----------------|-------------|
| Sprint close not executed immediately after final EPIC merge (same pattern as Phase 3 item above) | C | defer | **Deferred.** Consolidated with Phase 3 OA-03. PMO Lead, v4.1. |
| Staging-only AC retrospective designation — Phase 4 recurrence (same as Phase 3 item above) | A | defer → ESCALATED | **Deferred.** Consolidated with Phase 3 OA-02. Head of Specs Team, v4.1. |
| EPIC-02 PR number null at sprint close (pr_number: null) — recovered via gh pr view at STEP 5.0A | C | defer | **Deferred.** Head of Specs Team to add STEP 5.0A guard: if epics_merged contains EPIC with pr_number=null, search GitHub for matching PR before sealing. v4.1 target. Outstanding action OA-04. |
| Zero spec deviations, zero QA Fail results — DoQ sign-off completed before delivery verification; reclassified-to-autonomous ACs handled correctly | E | action-now | No change — validated delivery pattern recorded. |

---

## Consolidated Action Summary

**Immediate actions applied: 0**

All friction items with process change requirements are deferred — none can be applied without Head of Specs Team sign-off and targeted prompt updates that require the next sprint planning context to validate.

**Deferred to next cycle: 4**

| OA # | Action | Owner | Target |
|------|--------|-------|--------|
| OA-01 | execution_prompt.md patch: add STEP 4 merge-gate re-invocation as hard gate (STEP 5.0A guard) — 2nd recurrence escalation | Head of Specs Team | v4.1 |
| OA-02 | sprint_planning_prompt.md + sprint_backlog.md template: add staging-only evidence AC designation at planning for ACs requiring live API/keys/Render — 2nd recurrence escalation | Head of Specs Team | v4.1 |
| OA-03 | Confirm sprint_close_reminder.yml PR comment fires after each EPIC merge; investigate why user did not re-invoke `run sprint` after EPIC-03 merge | PMO Lead | v4.1 |
| OA-04 | delivery_verification_prompt.md STEP 5.0A: if epics_merged contains EPIC with pr_number=null, search GitHub for matching PR before sealing execution_state.json | Head of Specs Team | v4.1 |

**Escalated for decision: 0**

---

## Closure-Phase Observations

**Document closure friction:** Minimal. All required files were present and locatable. The amended backlog slice was correctly identified as the authoritative slice (both .claude_current_state.json and execution_state.json agree).

**Lessons learnt action application rate:** 0/4 deferred items were immediately actionable (all require Head of Specs Team sign-off and multi-file prompt patches). 0 immediate actions applied. This is appropriate — forced-now application of unreviewed prompt patches is a higher risk than carrying them forward.

**Closure steps revealing earlier gaps:** The endpoint coverage drift check (STEP 6) identified BLG-OPS-29 — GET /analytics/arc5-compliance and POST /trade-plans/{plan_id}/generate-thesis not in api_performance_baseline.md. Filed as backlog item.

The ideas housekeeping check identified 3 Rejected (strong) ideas not yet in rejected_but_strong.md (IDEA-cybersecurity-20260304-01, IDEA-cybersecurity-20260304-02, IDEA-ai-compliance-20260321-01) and 2 ambiguous rows (IDEA-product-owner-20260522-02, IDEA-qa-testing-20260522-01). These are flagged as outstanding actions for PMO Lead disposition.

---

## Carry-Forward

| Item | Owner | Target cycle | Notes |
|------|-------|--------------|-------|
| OA-01: execution_prompt.md merge-gate hard gate (2nd recurrence) | Head of Specs Team | v4.1 | Escalated — if v4.1 misses, treat as systemic failure requiring CLAUDE.md §2 update |
| OA-02: sprint_planning_prompt.md staging-only AC designation (2nd recurrence) | Head of Specs Team | v4.1 | Escalated — if v4.1 misses, treat as CLAUDE.md §2 mandated rule |
| OA-03: sprint_close_reminder.yml investigation | PMO Lead | v4.1 | Confirm workflow fires; investigate why sprint close was delayed in v4.0 |
| OA-04: delivery_verification_prompt.md STEP 5.0A pr_number null guard | Head of Specs Team | v4.1 | First occurrence; monitoring |
| OA-05: Rejected-but-strong register gaps — 3 ideas not in rejected_but_strong.md need PMO Lead disposition | PMO Lead | Before next roadmap run | IDEA-cybersecurity-20260304-01, IDEA-cybersecurity-20260304-02, IDEA-ai-compliance-20260321-01 |
| OA-06: Ambiguous ideas register rows — 2 rows need PMO Lead disposition on archive eligibility | PMO Lead | Before next roadmap run | IDEA-product-owner-20260522-02, IDEA-qa-testing-20260522-01 |
| BLG-OPS-29: api_performance_baseline.md re-run for v4.0 endpoints | Infrastructure & Operations Owner | v4.1 | GET /analytics/arc5-compliance + POST /trade-plans/{plan_id}/generate-thesis unmeasured |
