Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-17
Cycle: 2026-05-16__release-v3.6

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-05-16__release-v3.6
**Section anchor:** `## Phase 3`
**Filed:** 2026-05-17
**Reviewed by:** PMO Lead

**Prior cycle checked:** 2026-05-15__release-v3.5 — Phase 3 section absent from lessons_learnt_cycle.md (STEP 5.4 was not executed at v3.5 sprint close). Cross-cycle Phase 3 recurrence check not possible. Phase 4 section from v3.5 loaded — deferred items checked below.

**Prior cycle (v3.5 Phase 4) deferred items status:**
- "deviations_filed semantics: set to true after check completes (guidance to §3.1.A step 10)" → ✅ RESOLVED in ST-10 AC-01 (pre-met: guidance present in execution_prompt.md v3.21 §3.1.A step 10). However, the flag was still omitted during story execution for 4 items this sprint — engine followed the deviation check but did not set the flag. Noted as recurrence below.
- "verification readiness statement three-field block (§5.3 template)" → ✅ RESOLVED in ST-10 AC-02 (pre-met: block present in execution_prompt.md v3.21 §5.3). Verified as present and complete in sprint_close.md this cycle.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `deviations_filed = false` on 4 autonomous items (ST-01, ST-02, ST-06, ST-07) at sprint close, despite deviation check completed with finding "No deviation." The prompt guidance added in v3.6 EPIC-04 (§3.1.A step 10: "set deviations_filed = true after step 10 regardless of outcome") was not followed during story execution — flag was deferred or omitted. Auto-corrected at STEP 5.1. **Recurrence** from v3.5 Phase 4 deferred action (guidance added but engine execution still misses the flag-set). | Phase 3 | Type B | defer | Add explicit sub-step 10a in execution_prompt.md §3.1.A: "10a. Immediately after step 10 deviation check: write `deviations_filed: true` to execution_state.json for this ST item. Do not defer." Make the write atomic with the deviation check. Owner: Head of Specs Team. | Head of Specs Team | v3.7 |
| BLG-GOV-19 autonomous class applied to EPIC-03 and EPIC-01 despite both EPICs containing observable frontend changes (ST-07 error message display, ST-08 lozenge fix, ST-02 Entry Delta row). Criteria 2 and 3 explicitly exclude observable UI changes from the autonomous class. Playwright coverage was present and CI passed — substance correct, form incorrect. The sign-off form risk: a future EPIC with inadequate Playwright coverage could pass the same form check. | Phase 3 | Type A | defer | Update qa_evidence_template.md BLG-GOV-19 section: add explicit criterion 3 fail-path — "If any story has observable AC → autonomous class does not apply regardless of Playwright coverage. Use standard DoQ sign-off block and record Playwright test file references in DoQ comments." Owner: Director of Quality. | Director of Quality | v3.7 |
| Prior cycle (v3.5) lessons_learnt_cycle.md has no Phase 3 section — STEP 5.4 was not executed at v3.5 sprint close, preventing cross-cycle Phase 3 recurrence detection. This is the third consecutive sprint where Phase 3 lessons were either absent or incomplete (v3.4 Phase 3: not checked). | Phase 3 | Type C | defer | No retroactive fix. PMO Lead to confirm STEP 5.4 is included in every sprint close checklist at pre-seal verification. Facilitator to enforce. | PMO Lead | v3.7 |
| Fully autonomous sprint (7 stories, 0 delegated, 0 blocked) — all CI gates green on first push. Proactive database stub fix (BLG-QA-20, BLG-OPS-16) filed and patched in-session without blocking sprint progress. Efficient single-session execution with no escalations. | Phase 3 | Type E | action-now | Positive pattern — record for future sprint planning. High autonomous ratio is achievable when spec is locked before execution starts. No action required. | PMO Lead | — |

**Recurrence Notes:**
- `deviations_filed = false` recurrence: v3.5 Phase 4 deferred action (guidance patch) applied in v3.6 EPIC-04, but the flag omission recurred. The guidance is present in the prompt; execution discipline is the remaining gap. The sub-step 10a addition (above) is the proposed resolution.
- BLG-GOV-19 misapplication: first occurrence this sprint; no prior recurrence detected.
- Missing Phase 3 lessons: third consecutive cycle affected; escalation threshold approaching (per shared_standards.md §3.7 — recurrence in same item across two cycles triggers escalation to Head of Specs Team if the third recurrence occurs).
