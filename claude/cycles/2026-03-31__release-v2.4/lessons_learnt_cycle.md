Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-04-03
Cycle: 2026-03-31__release-v2.4

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-03-31__release-v2.4
**Section anchor:** `## Phase 3`
**Filed:** 2026-04-03
**Reviewed by:** PMO Lead

**Cross-cycle recurrence check:** Prior cycle `2026-03-24__release-v2.3` `## Phase 3` read. Three recurrences identified (marked below).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| [RECURRENCE-3] Delegation log entries not updated in-flight — DEL-20260401-01/02/03 all Pending at STEP 5.0 hard gate, requiring bulk update before sprint close. Same pattern as v2.3 (13 entries) and v2.2 (10 entries). Action-now patch applied in EPIC-06 ST-16 (execution_prompt.md delegation model update) but delegation log status update substep not yet added to STEP 3.1.A. | Phase 3 | A | action-now | Add explicit "update delegation log entry status to Unblocked/Cancelled after delegation record is resolved" substep to execution_prompt.md STEP 3.1.A after merge confirmation. Third recurrence — must be applied before next sprint. | Head of Specs Team | v2.5 |
| [RECURRENCE-2] QA sign-off blocks incomplete at sprint close — EPIC-01/02 had `[ ] Director of Quality — pending` at STEP 5.1. Same pattern as v2.3 (EPIC-03 blank date field). Action-now patch applied via ST-14 (QA evidence completeness check) but story-level check not preventing accumulation of pending sign-offs. | Phase 3 | A | defer | Strengthen the STEP 3 story done-criteria check: require DoQ sign-off Date field non-blank and checkbox checked before marking story status=done in execution_state.json. Currently the check fires at STEP 5.1 (sprint close) rather than STEP 3 (story close). | Head of Specs Team | v2.5 |
| governance_sync.yml batch push bug — EPIC-06 4-commit push closed only ST-17 (last commit's issue, #164). ST-14/15/16 issues #161/162/163 remained open. Root cause: workflow uses `git log -1` to extract issue number, so only the most recent commit is processed per push event. Manually closed with explanatory comments. Filed BLG-GOV-10. | Phase 3 | B | defer | Fix governance_sync.yml to extract all commit messages in the push (using `git log $BEFORE..$AFTER`) and close every referenced issue — not just the last. BLG-GOV-10 tracks this. | DevOps | v2.5 |
| execution_state.json post-merge lag — EPIC-03 PR #183 was merged 2026-04-02 but execution_state.json showed pr_number=null, pr_status=none at STEP 5 start. Required manual Python correction before sprint close could proceed. Similar to v2.3 EPIC-01/02 lag. | Phase 3 | B | defer | Add a pre-seal pr_status sync step in STEP 5: for each EPIC, call `gh pr view <n> --json state` and update pr_status if MERGED before sealing. Prevents misleading "none" values at sprint close. | Head of Specs Team | v2.5 |
| POST /test/endpoints auth forwarding bug (BLG-OPS-12) — ST-11 performance baseline initially appeared to be serviceable via the System Status page endpoint test runner, but internal calls don't forward X-API-Key. All protected endpoints return 401 (~22–37ms rejection latency). External authenticated measurements were required. System Status page shows misleading 1/17 pass rate. | Phase 3 | C | defer | BLG-OPS-12 tracks the fix. The auth bug pre-dates v2.4 and was discovered during baseline work. No engine process change required — the BLG-OPS-12 fix (forward API key in internal test calls) resolves the root cause. | Backend Engineering | v2.5 |
| Supabase free tier connection overhead — all 20 DB-backed endpoints exceed p95 500ms threshold when measured externally (p50 range 1.1–6s). Root cause: no persistent connection pool on free tier — each HTTP request from external client triggers fresh Supabase connection. Performance threshold (500ms p95) was designed for functional defect detection, not infrastructure characterisation. The threshold was exceeded across the board without indicating any correctness failures. | Phase 3 | D | defer | BLG-BE-07 tracks investigation. Consider calibrating the p95 threshold for external vs internal measurements separately in the next performance baseline version, or documenting that the 500ms threshold applies to internal measurements only. | Infrastructure & Operations Owner | v2.5 |

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-03-31__release-v2.4
**Section anchor:** `## Phase 4`
**Filed:** 2026-04-03
**Reviewed by:** PMO Lead

**Cross-cycle recurrence check:** Prior cycle `2026-03-24__release-v2.3` Phase 4 section read (in lessons_learnt_cycle.md for 2026-03-24__release-v2.3). Two recurrences identified (marked below).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| [RECURRENCE-2] QA evidence log missing at verification preflight — qa_evidence_EPIC-06.md was not filed at sprint close. QA Lead had verbally confirmed pre-met ACs (recorded in sprint_close.md §6) but no formal evidence log was created. Same pattern: v2.3 had EPIC-03/04 blank DoQ sign-off date fields requiring in-session completion. The sprint execution engine STEP 3.2.A requires creating qa_evidence_EPIC-xx.md before the PR, but this check is not enforced as a hard gate at sprint close. | Phase 4 | A | action-now | Strengthen execution_prompt.md STEP 5 sprint close gate: before sealing, verify that qa_evidence_EPIC-xx.md exists and has a non-blank Director of Quality sign-off block for every EPIC in merge_gate.epics_merged. A missing file at sprint close should halt STEP 5 — not be discovered at Phase 4 preflight. | Head of Specs Team | v2.5 |
| EPIC-03 and EPIC-04 QA evidence signed by non-DoQ roles (HoE and QA Lead respectively). The delivery verification prompt requires "Signed off by: Director of Quality" but STEP -1.3 only halts on "blank sign-off" not "wrong authority sign-off." DoQ appended sign-offs at verification preflight. | Phase 4 | A | defer | Clarify delivery_verification_prompt.md STEP -1.3: distinguish between blank sign-off (halt) and non-DoQ sign-off (flag + require DoQ counter-sign before proceeding). Current language is ambiguous — "blank" is interpreted as empty but the intent is likely "not from Director of Quality." | Head of Specs Team | v2.5 |
| sprint_backlog.md never created as a separate file — the stage4_backlog_slice.md serves as the combined planning artefact but the sprint_backlog_path pointer in .claude_current_state.json pointed to a non-existent file. Discovered at delivery verification preflight (STEP -1.4 required file check). Resolved by PMO Lead updating the pointer to stage4_backlog_slice.md. | Phase 4 | B | defer | Sprint planning engine should either: (a) create a sprint_backlog.md from the backlog slice, or (b) update sprint_backlog_path in .claude_current_state.json to the actual slice path at sprint planning close. The current state leaves the pointer stale after release planning. | Head of Specs Team | v2.5 |
| sprint_close.md formal "Verification readiness statement" block absent — the three Yes/No fields (All spec references populated, All deviations filed, QA evidence logs complete) were not present as a formal block. Evidence was available in §6 and §7 but not in the structured format the delivery verification prompt reads at STEP -1.2. | Phase 4 | B | defer | Add the formal verification readiness statement block to the sprint_close.md template in the execution engine. It should be populated at STEP 5 (sprint close) — the engine already checks these conditions, it just does not write the structured block. | Head of Specs Team | v2.5 |
| BLG-FE-01 reference in DEV-ST14-01 was stale — BLG-FE-01 is an archived v2.2 item (EPIC-03 ST-07). The deviation note in slippage_scenarios.md referenced it for the gradient deviation, giving the appearance that a valid backlog tracking item existed when it did not. Required DoQ to create BLG-FE-08 at verification and update the spec backlog reference per LL-CL-v22-01. | Phase 4 | C | defer | When a deviation is first accepted (DoQ sign-off), verify the backlog reference points to an active (non-archived) item. Consider adding a "backlog item active?" check to the deviation acceptance process. | Director of Quality | v2.5 |
| EPIC-06 qa_evidence log created at verification preflight, not at sprint close. The execution engine's STEP 3.2.A guidance says to create qa_evidence_EPIC-xx.md "before the PR" but all EPIC-06 stories were pre-met (no in-sprint development). The pre-met path had no explicit QA evidence creation step — the engine noted pre-met status in execution_state.json but did not create the evidence file. | Phase 4 | A | action-now | Add explicit check in execution_prompt.md STEP 3.1.A pre-met path: even for pre-met items, a qa_evidence_EPIC-xx.md entry must be created confirming the pre-met verification and signed off by DoQ. Pre-met does not mean unverified. | Head of Specs Team | v2.5 |
