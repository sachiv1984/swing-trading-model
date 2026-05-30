**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.6
**BLG ref:** BLG-GOV-41

---

# Sprint Close Reminder Workflow Investigation

## Investigation Scope

Review `.github/workflows/sprint_close_reminder.yml` GitHub Actions run logs for cycle `2026-05-22__release-v4.0` (and surrounding cycles) to identify the root cause of any reported failure and propose resolution.

## Workflow Design

The workflow fires on `pull_request` events with `types: [closed]` targeting the `main` branch. It applies two conditions before posting a sprint-close reminder comment:

1. `github.event.pull_request.merged == true` — only fires on actual merges, not closures without merge
2. `startsWith(github.event.pull_request.head.ref, 'exec/')` — only fires on `exec/**` branches (EPIC PRs)

These conditions are evaluated in the `if:` guard on the `sprint_close_reminder` job. Any PR merging from a non-`exec/` branch results in a `skipped` conclusion (the job condition evaluates to false), not a failure.

## Evidence Reviewed

GitHub Actions run logs for `sprint_close_reminder.yml` were reviewed across the full run history:

| Cycle | EPIC | Conclusion | Date |
|-------|------|-----------|------|
| `2026-05-22__release-v4.0` | EPIC-01 | success | 2026-05-24 |
| `2026-05-22__release-v4.0` | EPIC-02 | success | 2026-05-25 |
| `2026-05-22__release-v4.0` | EPIC-03 | success | 2026-05-25 |
| All other v4.1–v4.5 EPIC PRs | (all) | success | 2026-05-27–30 |
| `hotfix/research-atr-signal-fields` | N/A | skipped | 2026-05-22 |
| `gov/2026-05-21__prompt-compression` | N/A | skipped | 2026-05-21 |
| Multiple other hotfix/gov branches | N/A | skipped | various |

**No failure (`failure` or `cancelled`) status was found in any sprint_close_reminder.yml run.** All `exec/*` EPIC PR merges produced `success` conclusions. All non-`exec/` PR merges produced `skipped` conclusions, which is the expected and correct behavior.

## Root Cause

The item BLG-GOV-41 was filed based on an anticipated or anecdotally-reported failure that could not be reproduced. Two probable explanations:

1. **Observer effect (most likely):** The reminder comment was posted correctly by the workflow, but was missed by the operator because it appeared in a high-volume PR thread after the operator had already moved on. The sprint close was then discovered missing at Phase 4 preflight, which was attributed to workflow failure rather than operator oversight.

2. **Early filing (possible):** BLG-GOV-41 may have been filed proactively when the pattern was first noticed (sprint close being skipped), before it was confirmed whether the automation had fired. The automation did fire; the gap was human, not automation.

## Resolution

**No code change required.** The workflow is functioning as designed:
- Fires and succeeds for all `exec/**` EPIC PR merges
- Correctly skips for hotfix, governance, and feature branches
- Comment content is accurate and actionable

**Action:** This investigation document serves as the gate resolution for BLG-GOV-41. The item is closed.

**Recommendation:** No workflow retirement or modification is warranted at current scale. If the comment continues to be missed in practice, consider adding a `CODEOWNERS` notification or modifying the comment to `@mention` the responsible operator — file as a new backlog item if this recurs.

## Sign-Off

PMO Lead: investigation complete; root cause documented; no workflow defect found; BLG-GOV-41 closed.
Date: 2026-05-30
