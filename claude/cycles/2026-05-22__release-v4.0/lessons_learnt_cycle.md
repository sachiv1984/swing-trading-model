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
