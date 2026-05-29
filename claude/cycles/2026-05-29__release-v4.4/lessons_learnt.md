**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4
**Phase:** Release

---

# Lessons Learnt — Release Planning v4.4

Feature / Trigger: v4.4 Governance Patches, SI-02 Pre-Planning Sprint & Ops Hardening
Run: 2026-05-29__release-v4.4
Reviewed by: PMO Lead
Date filed: 2026-05-29
Prior cycle checked: 2026-05-29__release-v4.3

---

## What worked well

- **Carry-forward resolution was immediate.** Both carry-forward items from v4.3 lessons_learnt_closure.md (BLG-GOV-71 and BLG-GOV-72) were resolved at STEP 0 without requiring any inline escalation. The backlog items were present and ready.
- **v4.4 roadmap entry was present.** The PO had pre-added the v4.4 section to current_roadmap.md (as noted in the roadmap header: "v4.4 planned release annotation added by Product Owner to unblock release planning"), so STEP -1.2 passed without a gate fire. This is the intended resolution for the STEP -1.2 pattern — BLG-GOV-71 addresses the structural gap.
- **Scope extraction was clean.** 13 stories across 4 EPICs extracted without ambiguity. All SI-02 pre-planning items traceable to backlog. Gate conditions documented clearly.
- **Conditional items handled cleanly.** BLG-BE-20 (ST-09) and BLG-QA-31 (ST-12) gate conditions documented at the story level with sequencing rationale — sprint planning has the information needed to sequence them correctly.

---

## Friction Log

No friction items. Clean run.

---

## Recurrence Escalations

None.

---

## Process improvements actioned this run

None applied this run. All governance patches are deferred to execution (EPIC-01 stories ST-01 through ST-05).

---

## New files created this run

- `claude/cycles/2026-05-29__release-v4.4/run_manifest.md`
- `claude/cycles/2026-05-29__release-v4.4/state.json`
- `claude/cycles/2026-05-29__release-v4.4/release_plan.md`
- `claude/cycles/2026-05-29__release-v4.4/stage4_backlog_slice.md`
- `claude/cycles/2026-05-29__release-v4.4/stage4_issue_manifest.json`
- `claude/cycles/2026-05-29__release-v4.4/backlog_txn.json`
- `claude/cycles/2026-05-29__release-v4.4/roadmap_txn.json`
- `claude/cycles/2026-05-29__release-v4.4/cycle_summary.md`
- `claude/cycles/2026-05-29__release-v4.4/lessons_learnt.md`
- `docs/product/scope/scope--2026-05-29__release-v4.4-governance-patches-si02-preplanning.md`
- `docs/product/decisions/decisions--2026-05-29__release-v4.4.md`

---

## Outstanding deferred patches

None. All v4.3 deferred patches are in scope for v4.4 execution (EPIC-01).

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | BLG-GOV-72 (ST-02 EPIC-01) patches sprint_planning_prompt.md with a frontend classification fast-path. Sprint planning must verify this patch has been applied to sprint_planning_prompt.md before classifying EPIC-03 stories (SI-02 pre-planning includes delegated_frontend stories that could be misclassified without it). | At v4.4 sprint planning: confirm sprint_planning_prompt.md v3.8 (or later) contains the frontend classification fast-path rule before proceeding to story classification. | Sprint Planning |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-05-29__release-v4.4",
  "phase": "Release",
  "filed_utc": "2026-05-29T22:20:00Z",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
