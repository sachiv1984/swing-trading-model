**Owner:** PMO Lead
**Class:** Process Record (Class 3)
**Status:** Active
**Last Updated:** 2026-04-10
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Lessons Learnt — Cycle 2026-04-05__release-v2.5

---

## Phase 3 — 2026-04-05__release-v2.5

### Friction Table

| Date | Area | What happened | Correct approach | Prompt change? |
|------|------|--------------|-----------------|----------------|
| 2026-04-10 | Governance sync / commit IDs | ST-03 and ST-05/ST-06 were committed under another story's commit message. governance_sync.yml only parsed HEAD commit message, so GitHub issues didn't auto-close. Multi-commit multi-story pushes compounded this. | All ST IDs that land in a commit must appear in the commit message: `[EPIC-xx][ST-xx][ST-yy]`. governance_sync.yml was fixed (ST-10) to parse the full push range, but that only helps when IDs appear in the messages. CLAUDE.md §2 updated. | Added to CLAUDE.md §2 commit format rule and .claude/skills/lessons_learnt.md cross-skill table. |
| 2026-04-10 | Role ownership check | ST-06 (owned by Head of Engineering) was initially actioned as Head of Specs Team. User noticed the mismatch. Wasted one pass before re-reading the correct agent charter. | Always check the Owner field on the story/delegation record before picking up work. If role doesn't match, flag explicitly and ask for confirmation. | Existing feedback_role_ownership_check.md memory entry covers this. No prompt change needed. |
| 2026-04-10 | qa_evidence_EPIC-01.md not pushed before PR merge | The DoQ sign-off commit (78dd783) was created locally on EPIC-01 branch but not pushed before the PR was raised and merged. At sprint close, qa_evidence_EPIC-01.md was missing from main. Required a cherry-pick onto main. | Push QA evidence commits before or immediately after the PR is raised, not after the merge. Alternatively: always check `git status` on the exec branch before opening a PR to confirm all committed files are pushed. | No prompt change — operational discipline. |
| 2026-04-10 | execution_state.json on EPIC branch, not main | execution_state.json was created on EPIC-03 branch. When EPIC-02 was merged after EPIC-03, it had a stale version (EPIC-03 still "not_started", EPIC-02 "in_progress"). Required conflict resolution at EPIC-02 merge. | execution_state.json should ideally live on a dedicated tracking branch or on main from the start. As-is: the last EPIC to merge always resolves the add/add conflict. The §8 conflict resolution rules in CLAUDE.md handle this correctly. | No change needed — §8 conflict resolution in CLAUDE.md is the correct protocol. |
| 2026-04-10 | DataTable.js TableHead onClick silent drop | TableHead only destructured `{children, className}`, silently dropping onClick, title, and all other props. Sort was broken for all three sortable columns in Trade History. Not caught in visual testing script until V-FD-04. | When adding interactive behaviour (onClick, onKeyDown, ARIA props) to a wrapper component, always use `{...props}` spread to ensure future callers can pass arbitrary attributes. Discovered and fixed in staging (e65e023). | Caught by staging visual test script — process worked. |

### Summary Assessment

- **Delegation patterns:** ST-06 (delegated_backend) was the only delegation. Completed within the same session by Head of Engineering. No SLA breach.
- **GitHub integration friction:** governance_sync.yml single-commit parser was the root cause of multiple manual issue closures (ST-03, ST-07, ST-08, ST-05). ST-10 fix resolves this going forward.
- **Acceptance criteria quality:** All AC was clear and executable. No `delegated_decision` items were needed.
- **Governance gates:** STEP -1 delivery verification gate fired because state was `Sprint_Planning_Complete` (not `Sprint_Complete`) — execution STEP 5 (Sprint Close) had not been run. Resolved by running sprint close before re-invoking delivery verification. Sprint planning was the last engine state because all sprints executed within the same session without intermediate close. Lesson: always run `run sprint` after the final EPIC merge to trigger STEP 5 in the same session.

### Net Sprint Assessment

Velocity: 13/13 (1.00). All stories delivered. No items returned to backlog. One delegation (DEL-01) resolved within the cycle. Three P3 UX observations filed as backlog items. One process improvement applied mid-sprint (CLAUDE.md commit format rule).

---

## Phase 4 — 2026-04-05__release-v2.5

### Friction Table

| Date | Area | What happened | Correct approach | Prompt change? |
|------|------|--------------|-----------------|----------------|
| 2026-04-10 | Sprint Close not run before delivery verification | Delivery verification invoked while status was `Sprint_Planning_Complete` (not `Sprint_Complete`). STEP -1 hard gate fired. Sprint Close (STEP 5) had not been executed because the session ended after EPICs were merged without re-invoking `run sprint`. | Always invoke `run sprint --cycle <cycle_id>` immediately after the final EPIC merge. The hard gate (LL-v2.2-EX-02) requires this in the same session. | No prompt change — hard gate already exists in execution_prompt.md STEP 4. Friction was in not following it. |
| 2026-04-10 | qa_evidence_EPIC-01.md missing from main at sprint close | The DoQ sign-off commit was created locally on EPIC-01 branch but the branch wasn't pushed before the PR was merged. File required cherry-pick onto main at sprint close. | Always push the exec branch after every commit (especially QA sign-off commits) before the PR is merged. Alternatively: `git log --not origin/<branch>` check before opening a PR. | No prompt change needed — operational discipline. |
| 2026-04-10 | fee-drag-scenarios.md referenced in qa_evidence but never created | qa_evidence_EPIC-03.md consolidation section referenced docs/testing/fee-drag-scenarios.md as "authored 2026-04-06" but the file was never created. BLG-QA-07 was the backlog item for it. The qa_evidence reference was inaccurate. | If a test scenario file is planned but not yet created, reference the backlog item (BLG-QA-07) in the qa_evidence, not the future file path. Do not write file paths for artefacts that don't exist. | No prompt change — documentation accuracy discipline. |
| 2026-04-10 | Deviation severity gate — TSG-V25-01 not_applicable | ATR/dedup/stop_price scenarios were listed in EPIC-01 test_scenarios but they cover v2.4 algorithmic AC, not v2.5 endpoint availability AC. Correctly assessed as not_applicable at verification. | When populating test_scenarios in execution_state.json, ensure the scenarios are relevant to the EPIC's own AC, not adjacent stories. ST-13 created these scenarios for v2.4 correctness — they shouldn't be listed under v2.5 EPIC-01. No material gap, but creates confusion at verification. | Low priority — consider whether test_scenarios field should note "for future execution" vs "ran this sprint". |

### Net Phase 4 Assessment

Gate sequencing worked as designed — STEP -1 caught the `Sprint_Planning_Complete` status correctly. Deviation severity calls were straightforward — no ambiguous P1/P2 cases. Test scenario coverage gap (TSG-V25-02) correctly identified and actioned. Sign-off coordination smooth — both DoQ and PO able to sign off in the same session. Overall: delivery verification process is functioning well; friction was upstream (sprint close not triggered) rather than in the verification process itself.
