Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-05
Cycle: 2026-04-29__release-v3.1

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-04-29__release-v3.1
**Section anchor:** `## Phase 3`
**Filed:** 2026-05-05
**Reviewed by:** PMO Lead

**Prior cycle checked:** 2026-04-25__release-v3.0 (Phase 4 section loaded — recurrence check complete)

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Sprint planning artefacts (sprint_backlog.md, sprint_goal.md, stage4_backlog_slice.md, release_plan.md, state.json) were committed to an orphaned execution branch (exec/2026-04-25__release-v3.0/EPIC-02) rather than to main. Sprint execution started from main without these files present. Sprint close (STEP 5) could not run until artefacts were restored via git checkout from the orphaned branch. | Phase 3 | Type D — Process Gap: sprint planning commit was made on a stale EPIC branch rather than on main; the planning engine did not verify it was on main before committing | defer | Sprint planning engine should verify current branch is main (or a clean governance branch) before committing planning artefacts. Add STEP 0 branch check to sprint_planning_prompt.md: if not on main, checkout main before committing. | Head of Specs Team | v3.2 |
| execution_state.json `deviations_filed` field remained `false` for all stories after sprint completion. QA evidence confirmed no deviations were found, but the administrative field was never updated from its initial state. This caused a minor inconsistency that required correction at sprint close. | Phase 3 | Type D — Process Gap: execution_prompt.md §3.1.A step 10 sets `deviations_filed = true` but this was not enforced during this sprint's execution; the field initialises to `false` and requires explicit update | defer | Add runtime check at STEP 5.1 (Acceptance Summary) to verify `deviations_filed = true` for all done items; if false and notes confirm no deviation found, auto-correct and note the correction in sprint_close.md | Head of Specs Team | v3.2 |
| CF-01 and CF-02 deferred governance patches from v3.0 were correctly actioned as ST-13/ST-14 this sprint. Both `execution_prompt.md` updates (reclassification backfill + output target) were delivered and merged. This confirms the carry-forward mechanism works when items are formally tracked as sprint stories. | Phase 3 | Type E — Positive pattern | action-now | No action required — confirmed as working pattern; continue tracking governance patches as explicit sprint stories | PMO Lead | — |

**Recurrence Notes:**

Prior cycle (2026-04-25__release-v3.0) Phase 4 friction items reviewed:
- Deferred item 1 (execution_prompt.md §3.1.A reclassification backfill): RESOLVED — delivered as ST-13/CF-01 this sprint ✅
- Deferred item 2 (execution_prompt.md STEP 8.5 output target): RESOLVED — delivered as ST-14/CF-02 this sprint ✅
- Sprint planning artefacts on orphaned branch: NEW friction item this cycle — sprint planning was done on an EPIC branch instead of main. Not a recurrence from v3.0.
- `deviations_filed = false` administrative gap: NEW friction item — not seen in prior cycles.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-04-29__release-v3.1
**Section anchor:** `## Phase 4`
**Filed:** 2026-05-05
**Reviewed by:** PMO Lead

**Prior cycle checked:** 2026-04-25__release-v3.0 (Phase 4 section present — recurrence check complete)

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Sprint planning artefacts missing from main at verification preflight — required git checkout restore from orphaned branch before STEP -1.4 could pass. Same root cause as Phase 3 friction item 1. | Phase 4 | Type D — Process Gap: planning artefacts committed to wrong branch; verification preflight required manual recovery step | defer | Sprint planning prompt STEP 0 branch check (deferred from Phase 3 — same action). | Head of Specs Team | v3.2 |
| `test_scenarios` fields in execution_state.json under-populated for EPIC-01 and EPIC-03 despite Playwright tests existing (trade-plan.spec.js SC-TP-01–07; earnings-calendar.spec.js SC-EARN-01–09; screener-uk-suffix.spec.js SC-UK-01–04). Tests were created but not registered. Two TSG backlog items created. | Phase 4 | Type D — Process Gap: execution_prompt.md CF-01 backfill instruction applied to test_scenarios at reclassification time, but tests created during story execution (not reclassification) were not backfilled | defer | Add post-story execution advisory to execution_prompt.md §3.1.A: after any story that creates test files, populate test_scenarios with the new file paths before moving to next story. | Head of Specs Team | v3.2 |
| Verification proceeded smoothly with no hard blocks, no deviations, no open escalations. All 14 stories verified in a single run. QA evidence from 2026-04-30 remained current and accurate at verification on 2026-05-05. | Phase 4 | Type E — Positive pattern | action-now | No action required — clean sprint + clean verification is the target state. | PMO Lead | — |

**Recurrence Notes:**

Prior cycle (2026-04-25__release-v3.0) Phase 4 friction items reviewed:
- TSG administrative gap (test_scenarios not populated): RECURRENCE — same gap appeared in v3.0 and v3.1. CF-01 addressed the reclassification path; the post-story-execution path remains unaddressed. Filed as new Phase 4 friction item above.
- Phase 3 lessons appended to wrong file: RESOLVED in this cycle (CF-02 delivered as ST-14) ✅
- Planning artefacts on orphaned branch: NEW in this cycle (Phase 3 + Phase 4 both flag this) — target v3.2.
