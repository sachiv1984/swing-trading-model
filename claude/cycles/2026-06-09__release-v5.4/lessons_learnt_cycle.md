Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-06-10
Cycle: 2026-06-09__release-v5.4

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-06-09__release-v5.4
**Section anchor:** `## Phase 3`
**Filed:** 2026-06-10
**Reviewed by:** PMO Lead
**Prior cycle Phase 3 checked:** claude/cycles/2026-06-08__release-v5.3/lessons_learnt_cycle.md — found; v5.3 Phase 3 items reviewed.

**Prior cycle deferred items check:**
- v5.3 deferred item: "git stash required at branch switch — incomplete prior session left unstaged work on EPIC branch. Monitor for recurrence in v5.4." — **Recurrence confirmed**: v5.4 also required git stash when switching from main to EPIC-02 branch (stashed backlog.md, execution_state.json, qa_evidence_EPIC-02.md). See recurrence notes below.
- v5.3 "Stale pr_status on resume" monitor: **Recurrence confirmed** — v5.4 had EPIC-02 pr_status as "open" in execution_state.json after merge. Corrected at sprint close STEP 5.0A.

**prompt_change_log.md deferred patch check:**
No v5.3 deferred patches requiring prompt_change_log.md entries. All v5.3 process improvements were action-now or monitoring-only.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| ST-03 date gate within Sprint 1 scope required PO-authorised sprint close rather than holding sprint open 11 days. Sprint was correctly designed to execute ST-03 after 2026-06-21 but at sprint open this required a scope decision (return to backlog vs wait). | Phase 3 | B | defer | Advisory: when stories with within-sprint date gates are planned, mark them in the sprint backlog with a `Status at sprint open: conditional — gate <date>` field at planning time. This makes the return-to-backlog path explicit rather than requiring a PO decision at sprint start. Consider adding this advisory to sprint_planning_prompt.md. | Head of Specs Team | v5.5 |
| qa_evidence file committed to EPIC branch AFTER PR was already opened — CI verify_governance check failed because the file was on main (unstaged) not on the branch. Required stash → checkout EPIC-02 → commit → push cycle. | Phase 3 | B | defer | Advisory: always commit qa_evidence_EPIC-xx.md to the EPIC branch before opening the PR, not after. The execution_prompt.md §3.2.A already requires this (sign-off block must be complete before PR opens per §3.2.B pre-condition). Operator error this cycle. Monitor for recurrence. | PMO Lead | v5.5 |
| git stash at branch switch (second recurrence v5.3→v5.4): main had unstaged changes (backlog.md, execution_state.json, qa_evidence) when switching to EPIC-02 branch. Second consecutive occurrence. | Phase 3 | B | action-now | Second recurrence: escalating from monitor to advisory. Sprint close artefacts (backlog.md, execution_state.json, qa_evidence changes made on main) should be committed to main BEFORE any branch-switching operations during sprint close. Process note added to sprint_close.md header guidance: "Write all sprint close artefacts to main before any git checkout commands." No prompt edit required — this is execution practice. | PMO Lead | — |
| EPIC-02 branch behind main (DIRTY/CONFLICTING) at merge gate — after EPIC-01 and EPIC-03 merged, EPIC-02 diverged. Required git merge origin/main resolution before PR could merge. | Phase 3 | E | action-now | Expected pattern per CLAUDE.md §8 merge order advisory. Resolved correctly (took branch qa_evidence version). No process change needed — merge order advisory already covers this. | Sprint Execution Engine | — |
| BLG-GOV-19 autonomous class sign-off correctly applied to all 3 EPICs — 14th–16th consecutive correct applications. | Phase 3 | E | action-now | Positive: BLG-GOV-19 qualification logic stable. No process change needed. | Sprint Execution Engine | — |

**Recurrence Notes:**
- "git stash at branch switch" (v5.3 first, v5.4 second recurrence): Now escalated to action-now advisory. Sprint close artefacts must be committed to main before any checkout to an EPIC branch.
- "Stale pr_status in execution_state.json" (v5.3 first, v5.4 second recurrence): STEP 5.0A sync is correctly catching this at sprint close. Consider whether the execution_state.json write after PR open should set pr_status based on the actual gh pr view response rather than assuming "open". Monitor for third occurrence.
