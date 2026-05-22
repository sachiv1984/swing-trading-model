**Owner:** Director of Quality
**Class:** Governance Artefact (Class 6)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-05-22

---

## PR Summary

<!-- Brief description of what this PR delivers -->

## Stories in this PR

| Story | Status | Spec Reference |
|-------|--------|----------------|
| [ST-xx] | done | spec link |

## Sprint Goal Reference

<!-- Link to sprint_goal.md for this cycle -->

## QA Evidence

- [ ] QA evidence file exists and DoQ sign-off date is populated before this PR is opened
- [ ] `qa_evidence_EPIC-xx.md` **is committed on this branch** — run `git status` or `git log` to confirm the file exists in this branch's history before opening this PR
- [ ] QA evidence sign-off block `Date:` field is **non-blank** (hard gate — do not open PR without this)
- [ ] DoQ sign-off recorded in evidence log before this PR was opened

> **Branch-commit requirement (v1.1):** The QA evidence file must be committed to this branch BEFORE the PR is opened. Creating or backdating the evidence file after the PR is open is a process deviation (retroactive QA evidence). If the file is not yet committed, close this PR, commit the evidence, then re-open.

## DoQ Sign-Off Confirmation (Hard Gate)

> **This checklist item is mandatory.** A PR opened with a blank `Date:` in `qa_evidence_EPIC-xx.md` violates the DoQ enforcement gate (BLG-GOV-18 / §3.2.B of execution_prompt.md).

- [ ] I confirm `qa_evidence_EPIC-xx.md` is committed on this branch (not created post-PR-open)
- [ ] I confirm `qa_evidence_EPIC-xx.md` sign-off block `Date:` field is non-blank and dated before this PR was opened
- [ ] DoQ sign-off was applied during sprint execution, not retrospectively

## Acceptance Criteria Verification

- [ ] All ST items in this EPIC are `status: done` in `execution_state.json`
- [ ] `acceptance_verified = true` for all done items
- [ ] `deviations_filed = true` for all done items
- [ ] `spec_references` populated for all done items

## Merge Gate Conditions

- [ ] `quality_gate.yml` passing (PR title format `[EPIC-xx] description`)
- [ ] All CI checks green
- [ ] No open P0 deviations
- [ ] Product Owner acceptance recorded (comment below)
- [ ] Director of Quality sign-off recorded (comment below or in `qa_evidence_EPIC-xx.md`)

---

*Cycle:* `<cycle_id>`
*Execution state:* `claude/cycles/<cycle_id>/execution_state.json`
