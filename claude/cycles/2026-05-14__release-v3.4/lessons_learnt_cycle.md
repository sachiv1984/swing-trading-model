Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-14
Cycle: 2026-05-14__release-v3.4

---

## Phase 3

**Cycle:** 2026-05-14__release-v3.4
**Filed:** 2026-05-14
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-05-09__release-v3.3 (Phase 3 section present — recurrence check complete)

| # | Area | Observation | Classification | Action | Owner | Target |
|---|------|-------------|----------------|--------|-------|--------|
| 1 | GitHub Integration — Merge Conflicts | Three of four EPICs required manual conflict resolution at merge time (EPIC-03, EPIC-01, EPIC-02). Root cause: `execution_state.json` created on each EPIC branch; `src/pages/Positions.js` modified by three branches (EPIC-03, EPIC-01, EPIC-02). This is a **Recurrence** from v3.3 Phase 3 item #2. | Recurrence | Establish a shared `execution_state.json` early (first EPIC branch creates; others check for existence before creating). Document merge order and shared file ownership explicitly in sprint_backlog.md. Filed BLG-GOV-21 for sprint planning prompt update. | Head of Specs Team | v3.5 |
| 2 | Playwright Test Hardcoding | `system-status.spec.js SC-SS-01b` hardcoded the endpoint placeholder value (`'49'`). When ST-04 updated `SystemStatus.js` to `'55'`, the test was not updated in the same commit, causing CI failure on PR #388. The CLAUDE.md rule ("hardcoded fallback count in SystemStatus.js must also be updated") did not explicitly require updating the Playwright test. | Type D — Process Gap | Add to CLAUDE.md §2: "When updating the SystemStatus.js `totalTests \|\| 'N'` fallback, also update SC-SS-01b in `tests/e2e/system-status.spec.js` in the same commit." Applied as action-now under Head of Specs Team authority. | Head of Specs Team | action-now |
| 3 | Delegation / Classification — Positive | All 14 stories classified `autonomous`; zero delegation records. Prior cycle v3.3 item #1 noted recurring frontend delegation blocks. This sprint's full autonomy confirms the engine-first frontend delivery model (LL-v2.3-CL-01) is effective when UX specs are locked before sprint execution. | Recurrence resolved | No action needed — process improvement from v3.3 realised. | PMO Lead | — |
| 4 | Multi-EPIC Positions.js Conflict Complexity | EPIC-01 (lifecycle/grace/trail), EPIC-02 (drawdown/concentration), and EPIC-03 (earnings display) all modified `src/pages/Positions.js`. The three-way conflict required careful import deduplication (duplicate `const API_BASE` from EPIC-02 misplaced before imports, ES module violation) and correct component stacking order. | Type B — Complexity | When multiple EPICs share a page file, designate one branch as the merge base for that file, or sequence commits so each EPIC's changes are additive. Document component stacking order in the UX spec so conflict resolution has a reference. | Head of Specs Team | v3.5 |
| 5 | QA Evidence Structure — Positive | All four `qa_evidence_EPIC-xx.md` files produced with complete AC tables and non-blank DoQ sign-off dates before PRs opened. No gate delays at merge or sprint close. BLG-GOV-18 Date field requirement (LL-v2.3-EX-01) working correctly. | Type E — Positive | No action needed. | PMO Lead | — |
| 6 | Recurrence Carry-Forward Check | v3.3 Phase 3 item #4 (QA evidence files appearing missing on resume from different branch) — not reproduced this cycle. All branches stayed consistent. v3.3 item #5 (AC error code mismatch on research endpoint) — not applicable this cycle. | Observation | No action. | PMO Lead | — |

**Outstanding Actions:**
- BLG-GOV-21: sprint_planning_prompt.md update — shared execution_state.json ownership rule (P2, v3.5)
- CLAUDE.md §2 update — SystemStatus.js + SC-SS-01b co-update rule (action-now, see below)

**Action-now patch applied this session:**
- CLAUDE.md §2 updated: "hardcoded fallback count in `src/pages/SystemStatus.js` (`Tests {totalTests || 'N'} endpoints`) must also be updated to reflect the new total. **Additionally, update `SC-SS-01b` in `tests/e2e/system-status.spec.js` to match the new fallback value in the same commit.** Omitting either step is a process deviation."
- Authority: Head of Specs Team (execution engine action-now, logged in prompt_change_log.md)

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-05-14__release-v3.4
**Section anchor:** `## Phase 4`
**Filed:** 2026-05-14
**Reviewed by:** PMO Lead

**Prior cycle checked:** 2026-05-09__release-v3.3 (Phase 4 section present — recurrence check complete)

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| BLG-GOV-21 ID conflict: Phase 3 lessons_learnt referenced "BLG-GOV-21" for sprint_planning_prompt.md patch but that ID was already assigned (Arc 4 data requirements capture, DL-025). Corrected to BLG-GOV-22 at delivery verification. No backlog item lost — only ID mismatch. | Phase 4 | Type D — Process Gap | defer | Add ID uniqueness check to lessons_learnt Phase 3 process: before filing new backlog IDs, verify the ID is unoccupied in backlog.md. Add advisory to execution_prompt.md §5.3. (BLG-GOV-22 created with correct ID.) | Head of Specs Team | v3.5 |
| Over-filing deviation: EPIC-02/ST-05/DEV-01 (useState dismiss) was filed as a deviation during sprint execution, but drawdown-review-prompt/ux_spec.md §6 explicitly specifies "in-memory component state." Implementation was spec-compliant. Filing created unnecessary verification overhead. | Phase 4 | Type D — Process Gap | defer | Add guidance to execution_prompt.md §3.1.A step 10: before filing a deviation, verify whether the implementation matches the spec intent, not just the literal wording of an earlier draft. If spec and implementation agree, record as implementation note only — not a deviation. | Head of Specs Team | v3.5 |
| Gate sequencing: all 4 QA evidence logs signed and ready before sprint_close was sealed. STEP -1 passed on first pass with no re-verification required. | Phase 4 | Type E — Positive pattern | action-now | No action required — pattern to preserve. | PMO Lead | — |
| Playwright coverage: all EPICs with observable AC had test scenarios authored before PR merge. Zero coverage gaps requiring TEST-GAP backlog items this cycle. Prior cycle v3.3 Phase 4 item #2 (test protocol checkbox) resolved: TEST-GAP-EPIC-03-v33 closed by EPIC-03 Playwright scenarios. | Phase 4 | Type E — Positive pattern | action-now | No action required. Prior cycle carry-forward resolved ✅ | PMO Lead | — |
| Deviation severity consistency: all 4 deviations correctly P3 — no contest between sprint_close and DoQ assessment. Prior cycle v3.3 Phase 4 item #1 (P2/P3 discrepancy) not recurred. | Phase 4 | Type E — Positive pattern | action-now | No action required. Prior cycle item not recurred ✅ | PMO Lead | — |
| Known Deviations sync (LL-v2.3-CL-03): four spec files required Known Deviations sections this run. Three specs (grace-period-alert, stop-management-workflow, drawdown-review-prompt) had no Known Deviations section at all — sections created at delivery verification rather than at implementation time. This is the intended flow but adds verification overhead. | Phase 4 | Type D — Process Gap | defer | Add advisory to execution_prompt.md §3.1.A step 10: when filing a deviation, also add the Known Deviations section to the canonical spec in the same commit. This shifts the work to execution time rather than verification time. | Head of Specs Team | v3.5 |

**Recurrence Notes:**

Prior cycle (2026-05-09__release-v3.3) Phase 4 items:
- P2/P3 priority discrepancy between sprint_close and DoQ assessment: NOT RECURRED ✅
- Protocol backlog-item checkbox not completed: NOT RECURRED ✅ (TEST-GAP-EPIC-03-v33 closed by v3.4 EPIC-03 Playwright scenarios)

New friction items this cycle:
1. BLG-GOV-21 ID conflict (lessons_learnt Phase 3 backlog ID collision) — first occurrence; deferred to v3.5.
2. Over-filing deviation for spec-compliant implementation (EPIC-02/ST-05) — first occurrence; deferred to v3.5.
3. Known Deviations sections absent from specs at implementation time — pattern noted; defer advisory to v3.5 for execution_prompt.md.
