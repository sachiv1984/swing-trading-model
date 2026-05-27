Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-27
Cycle: 2026-05-26__release-v4.1

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-05-26__release-v4.1
**Section anchor:** `## Phase 3`
**Filed:** 2026-05-27
**Reviewed by:** PMO Lead
**Prior cycle Phase 3 checked:** claude/cycles/2026-05-22__release-v4.0/lessons_learnt_cycle.md — found.

**Prior cycle deferred items check:**
- v4.0 deferred item 1 — merge_gate stale on resume (2nd recurrence): **RESOLVED** in v4.1. ST-01 delivered execution_prompt.md v3.27→v3.28 with HARD GATE after every EPIC merge. 2nd-recurrence escalation closed.
- v4.0 deferred item 2 — staging-only AC retrospective designation (2nd recurrence): **RESOLVED** in v4.1. ST-02 delivered sprint_planning_prompt.md v3.6→v3.7 (staging-only AC check at STEP 6.2 sign-off gate) and shared_standards.md v3.3→v3.4 (sprint_backlog.md template [REQUIRED] wording). 2nd-recurrence escalation closed.
- v4.0 deferred item 3 — sprint close not immediately after final EPIC merge: **PATTERN RECURRING.** EPIC-03 was merged via GitHub between sessions (PR #507 merged 2026-05-27T12:24:53Z); sprint close run in re-invocation session per the v4.1 HARD GATE pattern. This is the CORRECT behaviour post-ST-01: user re-invokes `run sprint`, engine detects all_merged=true and executes STEP 5 directly. However, EPIC-03 pr_number was null in execution_state.json (same as v4.0 EPIC-02 null). Second occurrence.
- v4.0 deferred item 4 — EPIC PR number null: **SECOND OCCURRENCE.** EPIC-03 pr_number was null because the PR was merged via GitHub UI without the engine having opened it. Recovered at session resume via git log scan (PR #507 identified). STEP 5.0A EPIC-03 pr_status corrected before seal.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| EPIC PR number null — second recurrence (v4.0 EPIC-02 + v4.1 EPIC-03): engine had completed all story work and QA sign-off but never executed STEP 3.2.B (open PR) before session ended; user merged via GitHub UI. STEP 4 merge-gate re-invocation guard (ST-01) ensures sprint close runs, but the PR is not opened by the engine, leaving pr_number null until session-resume scan. | Phase 3 | C | defer | Add a STEP 5.0A guard: if any EPIC in epics_merged has pr_number null or 0, search GitHub for a matching PR (`gh pr list --search "[EPIC-xx]" --state merged`) before sealing. Record the recovered pr_number. This would automate what this session did manually via git log. | Head of Specs Team | v4.2 |
| Gemini→Claude API switch mid-sprint — ST-07, ST-09, ST-15 all referenced Gemini API; sprint_backlog.md reflected "Gemini" at seal time; mid-sprint switch applied cleanly without amendment (project_api_switch_gemini_to_claude memory record 2026-05-27). No process violation — backlog items were functionally equivalent, only API provider changed. | Phase 3 | E | action-now | Positive pattern: API provider switch that does not change interface shape or AC substance does not require amendment. Engine applied adaptation cleanly. No process change needed — record as validated pattern. | Sprint Execution Engine | — |
| Both 2nd-recurrence escalations (OA-01 merge-gate, OA-02 staging-only AC) resolved in v4.1 as promised — ST-01 and ST-02 both delivered clean. Governance hardening sprint fulfilled its primary mandate on first attempt. | Phase 3 | E | action-now | Positive: 2nd-recurrence escalation resolution working as designed. Escalation mechanism correctly pressured delivery. No change needed. | Sprint Execution Engine | — |
| Agent-mediated sign-off used for 8 stories this cycle (ST-04 through ST-08, ST-12, ST-13, ST-14/15) — pattern consistently smooth, no retries required, no human escalations triggered. | Phase 3 | E | action-now | Positive pattern: agent-mediated sign-off is reliable for spec and operational reviews when criteria are well-defined. Recommend keeping classification as standard practice for AC-verified sign-offs. | Sprint Execution Engine | — |
| ST-11 returned to backlog mid-sprint (not at sprint close) — execution_state.json status was set to returned_to_backlog during EPIC-03 execution, before EPIC was marked done. STEP 5.2 rule is correctly applied prospectively. This is the intended flow, but STEP 5.2 documentation implies it happens at sprint close. | Phase 3 | D | defer | Clarify STEP 5.2 language to confirm that returned_to_backlog is a valid in-flight transition for authorized deferrals (not only a sprint-close action). Current wording implies items reach blocked_* first then are transitioned at close — but PO-authorized deferrals can be applied immediately during execution. | Head of Specs Team | v4.2 |

**Recurrence Notes:**
- **EPIC PR number null:** Second recurrence (v4.0 EPIC-02, v4.1 EPIC-03). Deferred STEP 5.0A guard improvement for v4.2. Recovering correctly via git log scan but this is a manual step.
- **Sprint close after re-invocation (correct pattern):** v4.1 HARD GATE (ST-01) now enforces this. First cycle where the hard gate was active — user correctly re-invoked `run sprint`; sprint close executed in re-invocation session. Pattern working as designed.
- **2nd-recurrence escalations resolved:** Both OA-01 and OA-02 closed. No carry-forward on these items.
