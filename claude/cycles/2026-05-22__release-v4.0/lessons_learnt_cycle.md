Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-25
Cycle: 2026-05-22__release-v4.0

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-05-22__release-v4.0
**Section anchor:** `## Phase 3`
**Filed:** 2026-05-25
**Reviewed by:** PMO Lead
**Prior cycle Phase 3 checked:** claude/cycles/2026-05-21__release-v3.9/lessons_learnt_cycle.md — found.
- Prior Phase 3 deferred item 1: merge_gate stale on resume — **RECURRENCE.** Same pattern this cycle: all 3 EPICs merged via GitHub UI between sessions; execution_state.json merge_gate remained at epics_merged=[] until STEP 4 sync. Action per v3.9 defer (Head of Specs Team, v3.10) not yet applied — escalating.
- Prior Phase 3 deferred item 2: staging-only AC designation at planning time — **RECURRENCE.** Four staging-only ACs deferred this cycle (BLG-QA-28, BLG-QA-29, BLG-QA-30, BLG-OPS-28). Action per v3.9 defer (Head of Specs Team, v3.10) not yet applied — escalating.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| merge_gate stale on resume — second recurrence (v3.9 + v4.0): all 3 EPICs merged via GitHub UI between sessions; epics_merged remained [] until STEP 4 sync (LL-v3.9-P3-1). STEP 4 sync worked correctly this cycle but the pattern recurs because the user is merging EPICs in GitHub between Claude sessions rather than via `run sprint`. | Phase 3 | C | defer | ESCALATED (second recurrence): Head of Specs Team to add explicit STEP 4 merge-gate re-invocation requirement as a hard gate — either enforce via sprint_close_reminder.yml (already exists but apparently not sufficient) or add a pre-seal check in STEP 5.0A that verifies LL-v3.9-P3-1 sync was run this session. Target: v4.1 execution_prompt.md patch. | Head of Specs Team | v4.1 |
| Staging-only ACs designated retrospectively — second recurrence (v3.9 + v4.0): four staging-only ACs surfaced at execution (ST-02/04, ST-05, ST-09, ST-12) rather than being flagged at sprint planning with "staging-only evidence" designation. This delays backlog item filing to execution sign-off rather than pre-sealing it at planning. | Phase 3 | A | defer | ESCALATED (second recurrence): Head of Specs Team to add "staging-only evidence" AC designation guidance to sprint_backlog.md template and sprint_planning_prompt.md — ACs requiring live API, live keys, or Render deploy must be flagged explicitly at planning with pre-filed BLG references. Target: v4.1 sprint_planning_prompt.md patch. | Head of Specs Team | v4.1 |
| AMD-20260523-01 amendment correctly executed — ST-12 (Gemini base wiring) and ST-13 (starlette upgrade) added as emergency items without disrupting sprint scope. Amendment ratification process (Product Owner + Director of Quality 2026-05-23) was smooth. | Phase 3 | E | action-now | Positive pattern confirmed: amendment cycle for hard prerequisite + emergency security fix operates cleanly. No process change needed — record as validated pattern for future emergency-class additions. | Sprint Execution Engine | — |
| ST-05 delegation (DEL-20260524-01) resolved within same sprint day — Head of Engineering unblocked within hours of delegation. Delegation log entry correctly set to Unblocked at sprint close. | Phase 3 | E | action-now | Positive pattern: delegated_backend resolution same-day when spec is locked and implementation complexity is low. No change needed. | Sprint Execution Engine | — |
| Sprint close executed at delivery verification invocation — sprint close was not run immediately after final EPIC merge (EPIC-03 merged 2026-05-25T14:38:31Z; sprint close run at 2026-05-25T15:00:00Z triggered by `run delivery verification` preflight). This is the expected STEP -1.1 recovery path and worked correctly, but the preferred pattern is STEP 5 immediately after final EPIC merge. | Phase 3 | C | defer | Confirm sprint_close_reminder.yml is firing correctly on EPIC merge (it should post a PR comment reminding the engine to `run sprint`). If the reminder is not working, investigate why the user did not receive the re-invocation prompt after EPIC-03 merge. | PMO Lead | v4.1 |

**Recurrence Notes:**
- **merge_gate stale state on resume:** Second recurrence (v3.9 and v4.0). Prior v3.9 defer (Head of Specs Team, v3.10) was not actioned — escalating to Head of Specs Team with v4.1 target. If recurs in v4.2 without resolution, treat as a systemic process failure requiring CLAUDE.md §2 update.
- **Staging-only AC retrospective designation:** Second recurrence (v3.9 and v4.0). Prior v3.9 defer (Head of Specs Team, v3.10) was not actioned — escalating to Head of Specs Team with v4.1 target. Pattern is consistent: ACs requiring live keys or live environments are only identified as staging-only during execution, not planning.
- **Sprint close delayed past final EPIC merge:** First occurrence. Monitoring — if recurs in v4.1, add to STEP 4 hard gate enforcement.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-05-22__release-v4.0
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-05-25
**Reviewed by:** PMO Lead
**Prior cycle Phase 4 checked:** claude/cycles/2026-05-21__release-v3.9/lessons_learnt_cycle.md — found.
- Prior Phase 4 deferred item 1: staging-only AC retrospective designation (Head of Specs Team, v3.10) → **RECURRENCE.** Same pattern in v4.0 (4 staging-only ACs surfaced at execution, not designated at planning). Action not yet applied by Head of Specs Team — escalating.
- Prior Phase 4 deferred item 2 (positive): BLG-GOV-19 autonomous class and deferred_at_planning traceability both working correctly → confirmed continuing in v4.0.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Sprint close not executed immediately after final EPIC merge — delivery verification invocation triggered the STEP -1.1 recovery path (all EPICs merged; status still Executing). Sprint close created correctly via recovery path but this is the expected fallback, not the preferred pattern. | Phase 4 | C | defer | Confirm sprint_close_reminder.yml PR comment is firing after each EPIC merge. If firing, investigate why user did not re-invoke `run sprint` after EPIC-03 merge (2026-05-25T14:38:31Z). If not firing, fix the workflow. Target: confirm and resolve at v4.1 sprint kickoff. | PMO Lead | v4.1 |
| Staging-only AC retrospective designation — second recurrence Phase 4 (v3.9 + v4.0): four staging-only ACs (BLG-QA-28/29/30, BLG-OPS-28) designated at execution sign-off rather than sprint planning. Prior v3.9 Phase 4 defer (Head of Specs Team, v3.10) not actioned. | Phase 4 | A | defer | ESCALATED (second recurrence — both Phase 3 and Phase 4): Head of Specs Team must action sprint_planning_prompt.md and sprint_backlog.md template update for staging-only AC designation at planning. Failure to action in v4.1 = systemic process failure requiring CLAUDE.md §2 update. | Head of Specs Team | v4.1 |
| EPIC-02 PR number absent from execution_state.json (pr_number: null) at sprint close — PR #488 recovered at STEP 5.0A via gh pr view. No data loss; state corrected before seal. Root cause: EPIC-02 stories_complete status did not include PR opening step (engine did not open the EPIC-02 PR — it was opened and merged by the user directly). | Phase 4 | C | defer | When EPIC reaches stories_complete and the engine has not opened a PR, detect this state at EPIC completion and prompt the user that a PR is required per STEP 3.2.B. Currently the engine silently leaves pr_number null. Consider adding a STEP 5.0A guard: if epics_merged contains any EPIC with pr_number=null, search GitHub for matching PR before sealing. | Head of Specs Team | v4.1 |
| Zero spec deviations, zero QA Fail results — 11/11 firm stories delivered. DoQ sign-off completed before delivery verification invoked (same-day for EPIC-01/02, morning-of for EPIC-03). No coordination friction. | Phase 4 | E | action-now | Positive: DoQ sign-off pipeline working correctly when sprint close is clean. Reclassified-to-autonomous stories (ST-02/04, ST-12) handled correctly with observable AC deferral + backlog items. BLG-QA-28/29 filed before PR opens — CLAUDE.md §2 gate satisfied. No change needed. | Sprint Execution Engine | — |

**Recurrence Notes:**
- **Staging-only AC retrospective designation:** Second recurrence (v3.9 + v4.0, both Phase 3 and Phase 4). Escalated. Head of Specs Team must action v4.1 or this becomes a CLAUDE.md §2 mandated rule.
- **Sprint close delayed past final EPIC merge:** First occurrence (Phase 4 perspective). Sprint_close_reminder.yml behaviour needs investigation.
- **EPIC-02 PR number null:** First occurrence. Not critical — STEP 5.0A gh pr view recovered correctly. Monitoring for v4.1.

**What Went Well (Phase 4):**
- Zero spec deviations across 11 stories — no deviation severity calls required
- DoQ sign-off completed before delivery verification invoked — no coordination delay
- Traceability matrix clean — all spec_references populated (ST-08 corrected at sprint close)
- deferred_at_planning (ST-10/ST-11) traced correctly to BLG-FEAT-25 with cycle reference added
- STEP -1.1 recovery path (sprint close at delivery verification invocation) worked correctly
- TSG table fully dispositioned: TSG-v40-01/03 backlog items, TSG-v40-02 not_applicable
