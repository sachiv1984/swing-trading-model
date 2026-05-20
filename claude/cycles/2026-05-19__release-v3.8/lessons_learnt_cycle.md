Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-20
Cycle: 2026-05-19__release-v3.8

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-05-19__release-v3.8
**Section anchor:** `## Phase 3`
**Filed:** 2026-05-20
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| DEV-EPIC04-ST09-01: createPageUrl map not updated when ST-09 delegated — frontend delegation checklist did not explicitly require this file as part of pages.config.js/nav registration AC | Phase 3 | A | defer | Add createPageUrl map update requirement to delegation template for new frontend page stories — update docs/specs/api_contracts/ticker_universe_api_contract.md delegation pattern notes | Head of Specs Team | v3.9 |
| QA evidence EPIC-04 created retroactively after PR merge — QA evidence file should precede or accompany PR opening (BLG-GOV-18 pre-condition) | Phase 3 | C | defer | Add QA evidence existence check to PR template checklist; ensure delegation recipients know to create evidence before requesting merge | Director of Quality | v3.9 |
| ST-03 initial classification as delegated_frontend reversed to autonomous — standard React component against fully-specced endpoint is always autonomous; initial classification was overly conservative | Phase 3 | D | action-now | LL-v2.3-EX-02 reclassification applied correctly; no prompt change needed — existing rule covers this; process note: apply autonomous candidate pattern (LL-v1.10-P3-3) earlier in classification loop | Sprint Execution Engine | — |

**Recurrence Notes:**
- DEV-EPIC04-ST09-01 type: new pattern — cross-file dependency in pages.config.js not covered by current delegation checklist. Not seen in prior cycles. Monitor for recurrence if another new page is added via delegation.
- Retroactive QA evidence: recurrence of process gap where PR merges before evidence file is staged. Recommend adding pre-merge check to PR template (BLG-GOV-18 already in execution prompt; gap is in delegation handoff).
- ST-03 reclassification: positive outcome (autonomous delivery faster than delegation) but reflects a systematic tendency to over-classify standard frontend stories when backend is complete and spec is locked. No action-now; watch classification at next sprint with similar story shape.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-05-19__release-v3.8
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-05-20
**Reviewed by:** PMO Lead
**Prior cycle Phase 4 file checked:** claude/cycles/2026-05-18__release-v3.7/lessons_learnt_cycle.md — found. Prior Phase 4 friction: one item (EPIC-01 QA evidence Result column "Pending DoQ" placeholder — deferred to v3.8, owner: Director of Quality + Head of Specs Team).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Retroactive QA evidence creation recurred (EPIC-03 and EPIC-04) — both files explicitly note "created retroactively — PR was merged before this QA evidence file was produced." This was flagged in v3.7 Phase 3 with Outstanding Action #2 (Director of Quality to enforce pre-merge date recording, target: next cycle). Action was not applied — gap carried forward as Phase 3 friction item in this cycle (v3.8) and deferred again to v3.9. | Phase 4 | A | defer | Recurrence escalation: defer action has been open 2 cycles (v3.7 Phase 3 → v3.8 Phase 3 → now Phase 4). Per lessons_learnt_prompt §6.4, a deferred patch carried forward 2+ cycles without a prompt_change_log entry is an automatic escalation. Action: Director of Quality to implement QA evidence existence pre-merge enforcement before v3.9 execution begins — via PR template checklist item or automated check. Target: v3.9 sprint start. | Director of Quality | v3.9 sprint start |
| execution_state.json test_scenarios for EPIC-01 lists pre-trade-research.spec.js alongside trade-plan.spec.js, but no scenarios from pre-trade-research.spec.js were referenced in QA evidence. PreEntryValidationPanel is in the trade plan form, not the research view — the extra spec file reference appears to be a stale entry. Core AC coverage is complete via SC-TP-17–20. | Phase 4 | A | defer | Update execution_state.json population guidance in execution_prompt.md: test_scenarios should only list spec files that contain scenarios exercised for that EPIC's AC; stale cross-file references inflate the scenarios-run traceability check. File: claude/system/execution_prompt.md; Section: story completion record schema note. | Head of Specs Team | v3.9 |
| ST-04/ST-05 planning-deferred items had no traceability in execution_state.json — items in authoritative backlog slice but absent from execution_state.json because they were removed at sprint planning, not during execution. STEP 1 flagged traceability gap; BLG-FEAT-25 added. | Phase 4 | C | defer | Verify that sprint planning engine (sprint_planning_prompt.md) records planning-deferred items in execution_state.json with status deferred_at_planning and gate_condition note, so delivery verification STEP 1 can trace them without a gap. File: claude/system/sprint_planning_prompt.md; Section: execution_state.json initialisation. | Head of Specs Team | v3.9 |
| Prior Phase 4 deferred patch (v3.7): QA evidence Result column "Pending DoQ" placeholder — deferred to v3.8 with owner Director of Quality + Head of Specs Team. Reviewing v3.8 QA evidence: Result column shows "Pass" and "Pass with notes" correctly — no "Pending DoQ" placeholders found. Patch was applied in practice (evidence template improved) though no prompt_change_log entry was found. | Phase 4 | A | action-now | No formal patch needed — gap resolved in practice. Record as closed: v3.8 QA evidence files show correct Result values; qa_evidence_template.md result column note was effective. No prompt_change_log entry required (behaviour corrected without a template change). | Director of Quality | — |

**Recurrence Notes:**
- **Retroactive QA evidence (RECURRENCE — ESCALATION):** This gap first appeared in v3.7 Phase 3 with an Outstanding Action to enforce pre-merge QA evidence. It recurred in v3.8 Phase 3 (deferred again) and now surfaces again at Phase 4. Per lessons_learnt_prompt §6.4, this is a two-cycle carry-forward without a prompt_change_log entry — automatic escalation to Head of Specs Team. The enforcement mechanism (PR template checklist item) must be in place before v3.9 execution begins.
- **ST-04/ST-05 planning deferral traceability:** New pattern for this cycle — not a recurrence. Planning-deferred items leaving no trace in execution_state.json is a gap that will recur whenever EPIC-02 or similar conditional items are deferred at planning. Adding sprint planning guidance to record these items is a medium-priority patch.
- **Prior Phase 4 deferred patch (v3.7 Result column placeholder):** Closed — resolved in practice in v3.8.

**What Went Well (Phase 4):**
- Zero P0/P1/P2 deviations — cleanest delivery register in multiple cycles
- Single P3 deviation already resolved before verification ran — no gate delays
- All three EPIC QA evidence files complete with DoQ sign-off on same day as sprint close — minimal coordination friction
- Known Deviations section added to ticker_universe_api_contract.md during verification (LL-v2.3-CL-03 compliance) — no post-ship correction needed
- BLG-FEAT-25 traceability entry for ST-04/ST-05 added cleanly during STEP 1 without escalation
- Test scenario coverage complete across all observable AC — no TEST-GAP backlog items required
