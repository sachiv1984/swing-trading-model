Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-03-30
Cycle: 2026-03-24__release-v2.3

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-03-24__release-v2.3
**Section anchor:** `## Phase 3`
**Filed:** 2026-03-30
**Reviewed by:** PMO Lead

**Cross-cycle recurrence check:** Prior cycle `2026-03-21__release-v2.2` `## Phase 3` read. Two recurrences identified (marked below).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| [RECURRENCE] Delegation log entries not updated in-flight — all 13 entries remained "Pending" until sprint close, requiring bulk update at STEP 5.0. Same pattern as v2.2 (10 entries). Deferred action from v2.2 not yet applied. | Phase 3 | A | defer | Apply the v2.2 deferred action: add explicit "update delegation log entry status to Unblocked/Cancelled" substep to execution_prompt.md STEP 3.1.A after merge confirmation. Second recurrence elevates priority — should be action-now in next engine patch window. | Head of Specs Team | v2.4 |
| [RECURRENCE] Sprint close (STEP 5) not triggered after all EPICs merged — delivery verification invoked directly, causing STEP -1.1 hard gate on execution_state.json.sealed=false. Same pattern as v2.2. Deferred advisory note from v2.2 not yet applied. | Phase 3 | C | defer | Apply the v2.2 deferred action: add advisory note to execution_prompt.md STEP 4 merge gate completion block — "When merge_gate.all_merged=true, STEP 5 Sprint Close must be invoked in the same session before delivery verification." Second recurrence elevates priority. | Head of Specs Team | v2.4 |
| Playwright selector fragility: merging main into EPIC-02 mid-sprint (after ST-02 select-none spans + ST-13 nav SVGs landed) introduced 7 strict-mode violations in chart-interactivity.spec.js, requiring 3 fix rounds across 3 commits. | Phase 3 | B | defer | Add note to execution_prompt.md STEP 4 cross-EPIC merge advisory: after pulling main into an EPIC branch, run the full E2E test suite locally before pushing; any strict-mode failures on shared-selector tests should be resolved before CI push. | Head of Specs Team | v2.4 |
| EPIC-03 QA sign-off Date field was blank at sprint close — LL-v2.0-P4-1 gate triggered, required in-line fix at STEP 5.1. QA sign-off checkboxes were also unchecked. | Phase 3 | A | defer | Add a QA evidence completeness check to the story done-criteria in execution_prompt.md STEP 3: sign-off Date field must be non-blank and all checkboxes checked before a story can be marked done. This prevents blank dates accumulating until sprint close. | Head of Specs Team | v2.4 |
| EPIC-01/EPIC-02 pr_status state lag: both PRs merged by Product Owner but execution_state.json still recorded pr_status="open" at seal time, because merge events occurred after the last state write. Documented in sprint_close.md as a state recording artefact. | Phase 3 | B | defer | Consider adding a pre-seal pr_status sync step in Sprint Close STEP 5: for each EPIC, call `gh pr view <n> --json state` and update pr_status if MERGED before sealing. Prevents misleading "open" values in sealed artefacts. | Head of Specs Team | v2.4 |
| Frontend delegation reclassification: 2026-03-26 mid-sprint decision reclassified all delegated_frontend/delegated_qa/delegated_backend stories to autonomous/engine, resulting in 12 of 13 delegation entries being cancelled at sprint close rather than resolved. Delegation log was a near-complete no-op for this sprint. | Phase 3 | D | defer | No engine change required — reclassification was a one-time governance decision. If autonomous reclassification becomes a recurring pattern (≥2 cycles), consider a sprint planning prompt advisory to evaluate autonomous classification eligibility before applying delegated_* labels. | Head of Specs Team | v2.4 |

**Recurrence Notes:**
- Friction items 1 and 2 are direct recurrences of v2.2 Phase 3 rows (originally deferred to v2.3 target date). Both deferred actions were not applied in the v2.3 cycle. Second recurrence — owner (Head of Specs Team) should prioritise these for action-now in the next available engine patch window, ideally before v2.4 sprint planning.
