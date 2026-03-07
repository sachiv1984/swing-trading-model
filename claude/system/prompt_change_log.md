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
