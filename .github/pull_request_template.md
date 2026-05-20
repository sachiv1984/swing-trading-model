**Owner:** Director of Quality
**Class:** Governance Artefact (Class 6)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-19

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

- [ ] `qa_evidence_EPIC-xx.md` exists for this EPIC
- [ ] QA evidence sign-off block `Date:` field is **non-blank** (hard gate — do not open PR without this)
- [ ] DoQ sign-off recorded in evidence log before this PR was opened

## DoQ Sign-Off Confirmation (Hard Gate)

> **This checklist item is mandatory.** A PR opened with a blank `Date:` in `qa_evidence_EPIC-xx.md` violates the DoQ enforcement gate (BLG-GOV-18 / §3.2.B of execution_prompt.md).

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
