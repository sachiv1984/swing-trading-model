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
