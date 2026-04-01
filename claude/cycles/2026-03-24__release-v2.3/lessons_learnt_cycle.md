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

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-03-24__release-v2.3
**Section anchor:** `## Phase 4`
**Filed:** 2026-03-30
**Reviewed by:** PMO Lead

**Cross-cycle recurrence check:** Prior cycle `2026-03-21__release-v2.2` `## Phase 4` read. One recurrence identified (marked below).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| [RECURRENCE] spec_references = [] for operational/QA tooling items (ST-03 staging reset, ST-04 seed scripts, ST-05 smoke tests) — same pattern as v2.2 (ST-02 CSP meta tag, ST-11 readiness doc). Deferred action from v2.2 not yet applied. Three traceability gap flags fired at STEP 1. | Phase 4 | A | defer | Apply the v2.2 deferred action: add note to execution_prompt.md §9.1 schema: for operational tooling items and autonomous infrastructure items with no prior canonical spec, spec_references may be left empty with a note field value of "no prior spec applicable." Second recurrence — owner should prioritise for action-now. | Head of Specs Team | v2.4 |
| EPIC-01 test_scenarios field empty in execution_state.json despite Playwright spec files existing (compliance-panel.spec.js SC-COMP-01–07, staleness-indicator.spec.js SC-STALE-01–05). Scenarios ran and passed — field registration was missed. | Phase 4 | B | defer | Add prompt note to execution_prompt.md STEP 3.1.A: when Playwright spec file is created for a story, populate test_scenarios field in execution_state.json with the scenario file path at the same time. This is a registration gap, not a coverage gap. | Head of Specs Team | v2.4 |
| P2 deviation acceptance (DEV-EPIC02-ST05-03) was implicit at verification rather than explicit — Product Owner acceptance was inferred from `run delivery verification` invocation rather than a recorded acceptance in QA evidence. | Phase 4 | C | defer | For P2 deviations filed during execution, add an advisory note in execution_prompt.md STEP 3.1.A deviation filing step: request PO to provide a brief explicit acceptance note in the relevant qa_evidence file at the time of filing, rather than deferring to delivery verification invocation. This makes P2 acceptance explicit and auditable. | Head of Specs Team | v2.4 |
| Post-sign-off CI selector fixes (3 commits on EPIC-02 branch after DoQ sign-off) required a post-sign-off maintenance note to be appended to qa_evidence_EPIC-02.md. The sign-off was not reopened but the maintenance note protocol was ad hoc. | Phase 4 | B | defer | Formalise post-sign-off CI maintenance note protocol in delivery_verification_prompt.md or execution_prompt.md: define when a maintenance note is sufficient (selector/infrastructure fix, no functional change) vs. when a DoQ re-review is required (functional AC change). Current ad hoc approach works but lacks a canonical decision rule. | Head of Specs Team | v2.4 |

**Recurrence Notes:**
- Friction item 1 is a direct recurrence of v2.2 Phase 4 row 2 ("ST-02 and ST-11 spec_references fields empty"). The deferred action was not applied in v2.3. Second recurrence — owner (Head of Specs Team) should prioritise this for action-now in the next available engine patch window.
- v2.2 Phase 4 row 3 (branch discipline / BLG-GOV-07) was resolved: ST-14 in this cycle applied the branch discipline invariant to execution_prompt.md §13. Not a recurrence.
