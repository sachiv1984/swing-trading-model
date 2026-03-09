**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-07

# Prompt Change Log

This file records all changes to governance prompts (Class 6 documents) and related governance artefacts. Append-only.

---

## Changes

| Date | Prompt | Version | Change | Authority |
|------|--------|---------|--------|-----------|
| 2026-03-09 | `shared_standards.md` | v1.4→v1.5 | Friction Item 1 (2026-03-06__release-v1.9 Sprint 1 execution): parallel EPIC branch `execution_state.json` merge conflict pattern documented. Added §12 Parallel EPIC Branch Merge Sequencing — merge ordering convention (dependency order), conflict resolution rule (keep more recent EPIC's version), GOVERNANCE commit protocol after each merge. Prevents 30–60 min CI overhead in multi-EPIC sprints. | Head of Specs Team |
| 2026-03-08 | `release_planning_prompt.md` | v2.12→v2.13 | IMP-05/06/07/08/10: STEP -1.5 (advisory lessons learnt action-now check), STEP -1.6 (hard gate: post_ship_complete + next_cycle_unblocked), STEP -1.7 (advisory prompt change log check). ESCALATION HANDLING SUBROUTINE: inline entry format/SLAs/Accepted Risk replaced with shared_standards.md §4 reference. STEP 3: compact table format requirement added for Execution Plan section; <200 line target for release_plan.md. | Head of Specs Team |
| 2026-03-08 | `sprint_planning_prompt.md` | v1.3→v1.4 | IMP-04: Design gate bypass audit added to STEP -1.3 — entering from Release_Planning_Complete requires design_gate_bypass_authority + design_gate_bypass_reason in .claude_current_state.json. Strict mode halts if absent; standard mode flags and blocks seal. | Head of Specs Team |
| 2026-03-08 | `amendment_cycle_prompt.md` | v1.1→v1.2 | IMP-09: STEP -1.1 atomicity guard — backlog lock acquired with marker AMEND-CHECK:<cycle_id> before sprint_sealed is read; lock released after STEP 5 or on any halt. Governance invariant added. | Head of Specs Team |
| 2026-03-08 | `shared_standards.md` | v1.3→v1.4 | IMP-04/06/10: §10.1 table updated (Release Planning preconditions, Sprint Planning bypass audit, Amendment Cycle lock requirement). §11 Prompt Version Control added. | Head of Specs Team |
| 2026-03-07 | `release_planning_prompt.md` | v2.11→v2.12 | IMP-03: Added `prompt_schema_version: "v2"` to state.json schema template. Fixed §18.1 tracked artifact list to reference `release_plan.md` (was `stage2_scope_extraction.md`, `stage3_execution_plan.md`). Added schema migration table to Drift Detection section. Added inline changelog entries for v2.10 and v2.11 (previously only in prompt_change_log.md). | Head of Specs Team |
| 2026-03-07 | `roadmap_management_prompt.md` | v1.1→v1.2 | IMP-02: Added `last_manage_roadmap_utc` and `last_manage_roadmap_outcome` state write to STEP 6. Added `.claude_current_state.json` to §5 write scope and STEP 6 commit list. | Head of Specs Team |
| 2026-03-07 | `backlog_management_prompt.md` | v1.1→v1.2 | IMP-02: Added `last_groom_backlog_utc` and `last_groom_backlog_outcome` state write to STEP 7. Added `.claude_current_state.json` to §5 write scope and STEP 7 commit list. | Head of Specs Team |
| 2026-03-07 | `post_ship_closure.md` | v1.3→v1.4 | IMP-01: added `closure_state.json` per-cycle state file for reliable resumability. §4 inputs and §5 write scope updated. STEP 0: create-or-resume logic with full JSON schema. STEP 0 through STEP 11: each step writes completion flag and `last_updated_utc` to `closure_state.json`. STEP 11 commit list: `closure_state.json` added. STEP 10: `closure_state.json` set to `status = Closed` + `closure_status` on global state write. | Head of Specs Team |
| 2026-03-07 | `shared_standards.md` | v1.2→v1.3 | IMP-01: §8 Post-Ship Closure resumability note updated — replaced prose-scan of `closure_record.md` with `closure_state.json` structured resume protocol. | Head of Specs Team |
| 2026-03-07 | `release_planning_prompt.md` | v2.10→v2.11 | Intermediate Release Planning artefacts collapsed into `release_plan.md`. Steps 1, 2, 3, 3.5, 4.5, 5.5, 5.7 now write sections into a single consolidated file instead of separate stage files. Final outputs retained separately: scope document, decisions record, stage4_backlog_slice.md. Tracked set in state.json schema updated from `[stage2_scope_extraction, stage3_execution_plan, stage4_backlog_slice, escalations]` to `[release_plan, stage4_backlog_slice, escalations]`. | Head of Specs Team |
| 2026-03-07 | `release_planning_prompt.md` | v2.9→v2.10 | Added Lifecycle Guard (valid from-states: `Closed`) per `shared_standards.md §10`. | Head of Specs Team |
| 2026-03-07 | `sprint_planning_prompt.md` | v1.2→v1.3 | Added Lifecycle Guard (valid from-states: `Design_Gate_Passed`; or `Release_Planning_Complete` when design gate not required). | Head of Specs Team |
| 2026-03-07 | `execution_prompt.md` | v1.5→v1.6 | Added Lifecycle Guard (valid from-states: `Sprint_Planning_Complete`, `Executing` on resume). | Head of Specs Team |
| 2026-03-07 | `delivery_verification_prompt.md` | v1.1→v1.2 | Added Lifecycle Guard (valid from-states: `Sprint_Complete`). | Head of Specs Team |
| 2026-03-07 | `post_ship_closure.md` | v1.2→v1.3 | Added Lifecycle Guard (valid from-states: `Verified`, `Verified_with_deviations`). | Head of Specs Team |
| 2026-03-07 | `design_gate_prompt.md` | v1.0→v1.1 | Added Lifecycle Guard (valid from-states: `Release_Planning_Complete`). | Head of Specs Team |
| 2026-03-07 | `amendment_cycle_prompt.md` | v1.0→v1.1 | Added Lifecycle Guard (valid from-states: `Sprint_Planning_Complete` with `sprint_sealed = false`). | Head of Specs Team |
