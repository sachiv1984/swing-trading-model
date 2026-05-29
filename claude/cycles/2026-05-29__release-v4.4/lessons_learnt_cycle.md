Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-30
Cycle: 2026-05-29__release-v4.4

---

# Lessons Learnt — 2026-05-29__release-v4.4

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-05-29__release-v4.4
**Section anchor:** `## Phase 3`
**Filed:** 2026-05-30
**Reviewed by:** PMO Lead
**Prior cycle Phase 3 checked:** claude/cycles/2026-05-29__release-v4.3/lessons_learnt_cycle.md — found.

**Prior cycle deferred items check:**
- v4.3 deferred item 1 — Wrong staging URL: **RESOLVED** in v4.4 ST-13. OPERATIONAL_GUIDE.md v4.19 §7.9 added — "Staging URL Disambiguation" subsection distinguishes frontend SPA URL from backend API URL for health checks and performance baselines.
- v4.3 deferred item 2 — frontend classification fast-path: **RESOLVED** in v4.4 ST-02. sprint_planning_prompt.md v3.8 adds frontend fast-path: (a) bug fix in prop/state threading, (b) variable rename in React code, (c) new section/component against locked spec — all default to `autonomous`.
- v4.3 deferred item 3 — deviations_filed=False for delegation stories: **RESOLVED** in v4.4 ST-03. execution_prompt.md v3.33 §5.3 Protocol step 5 updated: delegated story + cleared + no DEV-* → deviations_filed=true auto-set.
- v4.3 deferred item 4 — DoQ sign-off format for delegated_qa stories: **RESOLVED** in v4.4 ST-04. qa_evidence_template.md v1.4 documents both sign-off format variants (individual delegated_qa + aggregate DoQ consolidation).
- v4.3 deferred item 5 — release_planning_prompt.md RESUME PRECHECK: **RESOLVED** in v4.4 ST-05. release_planning_prompt.md v2.32 STEP 7 now includes RESUME PRECHECK note per v4.3 LL-2 carry-forward.
- v4.3 Phase 4 deferred item — empty spec_references for doc-creation stories: **Still deferred** (target v4.5 per prior record). Not addressed in v4.4. Not a recurrence yet; tracking continues.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| All 5 v4.3 Phase 3 deferred items resolved in v4.4 (6 governance patches across ST-01/02/03/04/05/13). OA-to-story-to-patch pipeline completed within one cycle of filing for all items. Third consecutive sprint with 100% carry-forward resolution rate. | Phase 3 | E | action-now | Positive: carry-forward resolution mechanism is working reliably. No process change needed. | Sprint Execution Engine | — |
| DEL-20260529-05 terminal status was incomplete at session close: delegation log showed "ST-11 agent invoked" without the final commit SHA for ST-11 (6061bcca). The entry was updated in the next session (STEP 5.0 delegation log outcome check) but was not atomic with the story status update at the time of delivery. Minor process friction. | Phase 3 | A | defer | Enforce §5.3 terminal-commit write at delegation sign-off step: when recording sign_off_record.status = "cleared" for a delegated story, write the commit SHA to the delegation log entry in the same atomic operation. Currently the delegation log update is listed as a hard gate but the SHA may not be available at sign-off time if the engine invokes the agent before pushing the commit. Consider splitting: (a) record "agent sign-off cleared" at sign-off, (b) update commit SHA at push step. | Head of Specs Team | v4.5 |
| EPIC-03 execution_state.json stale at sprint resume: EPIC-03 pr_number was null and ST-12 had acceptance_verified: false + deviations_filed: false despite EPIC-03 having been merged (PR #564, 2026-05-29T23:18:38Z). The previous session's QA evidence commit (fed601fc) updated ST-11/12 story fields but did not update EPIC-03.pr_number or EPIC-03.status from "done" to "merged". Detected and corrected at STEP 4 merge gate sync on resume. | Phase 3 | A | defer | Add an explicit EPIC pr_status sync step to the EPIC completion flow (STEP 3.2.B): after opening the PR and recording pr_number, run `gh pr view <pr_number> --json state` immediately and update pr_status. At QA evidence commit time, also update EPIC.status from "done" to "merged" if the PR was merged before the QA evidence commit. This prevents the stale pr_status pattern that requires merge gate sync on resume. | Head of Specs Team | v4.5 |
| All 5 delegated stories (ST-06/07/09/10/11) completed via agent-mediated sign-off (§5.3) within the sprint session — zero actual human delegation occurred. The agent-mediated sign-off protocol is working well for pre-planning design artefacts: engine produces the document, agent role evaluates against charter criteria, sign-off recorded atomically. | Phase 3 | E | action-now | Positive: §5.3 agent-mediated sign-off pattern validated for pre-planning/architecture doc cycles. No process change needed. | Sprint Execution Engine | — |
| Empty spec_references for doc-creation stories (ST-06/07/08/09/10/11/12): all 7 SI-02 pre-planning stories have "no prior spec applicable" exemption. The v4.3 Phase 4 deferred item targets v4.5. This is the second consecutive cycle where doc-creation stories generate empty spec_references. | Phase 3 | A | defer | Track with v4.3 Phase 4 deferred item (target v4.5). If v4.5 also involves doc-creation stories with empty spec_references, escalate to recurrence at that point. | Head of Specs Team | v4.5 |

**Recurrence Notes:**
- **Carry-forward resolution 100%:** Third consecutive sprint with full OA resolution. Stable positive pattern.
- **DEL terminal status incomplete:** New this cycle. Minor. Defer; no escalation.
- **EPIC pr_status stale at resume:** New this cycle. Minor. Defer; no escalation.
- **Agent-mediated sign-off effectiveness:** New pattern validated this cycle (first all-agent-mediated sprint). Positive.
- **Empty spec_references:** Second occurrence for doc-creation cycles. Still within deferred trajectory (target v4.5). Not yet a recurrence escalation.
