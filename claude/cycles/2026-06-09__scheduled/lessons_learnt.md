**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-09__scheduled

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled run
Run: 2026-06-09__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-09
Prior cycle checked: 2026-06-08__scheduled (claude/cycles/2026-06-08__scheduled/lessons_learnt.md — found; 1 Type D friction item; DP-1 OVERDUE resolved, DP-2 carry-1 → action-now via meta-review)

---

## What Worked Well

- **DP-1 overdue patch applied cleanly.** idea_intake_prompt.md v2.4→v2.5 — §2.0 step 5 backlog scope advisory added. The overdue detection at STEP -1.5 correctly surfaced and blocked progress until the patch was applied. No downstream artefacts were affected.
- **Meta-review fired on schedule.** 3 cycles since 2026-06-02__scheduled — trigger condition met. Aggregate analysis confirmed the Type D recurring pattern and produced the DP-2 action-now upgrade, resolving both outstanding deferred patches in a single session.
- **Parked-cycle-2 terminal resolution clean.** All 12 IW-20260607-01 items resolved: 4 Rejected with clear rationale (trigger conditions not met, no friction evidence), 8 Promoted-Backlog (all gate-conditional with specific gate criteria documented). No vague re-parks attempted.
- **BLG-ID assignment collision-free.** Despite adding 8 new backlog items across 5 series, no ID collisions occurred. New DP-2 advisory (v6.9) will make this even more systematic going forward.
- **STEP 8.1 Option (a) fired cleanly.** v5.4 Now section added with a well-defined theme and candidate scope list. Release planning can proceed directly.

---

## Friction Log

No friction items this cycle. All process steps executed as expected. DP-1 overdue was a known carry from prior cycle — not new friction.

| # | Type | Description | Blast radius | Patch |
|---|------|-------------|-------------|-------|
| — | — | No friction items this cycle | — | — |

---

## Deferred Patches

None outstanding post meta-review.

| # | File | Section | Change | Owner | Target | Status |
|---|------|---------|--------|-------|--------|--------|
| — | — | — | — | — | — | All prior patches resolved this cycle |

---

## Outstanding Actions

None. No escalations.

---

## Process Observations (Not Friction)

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-01 | **17 ideas are now at Parked-cycle-2 (IW-20260608-01).** At the next scheduled rebalance, PO must actively Advance, Reject, or Backlog (gate-conditional) all 17 — re-parking to cycle-3 is not permitted. Most are scope-premature (SI-05 in-app, compliance metrics, retrospective analyses) but PO must explicitly decide. | PMO Lead | Highlight at next rebalance STEP 4. |
| LL-02 | **Time-sensitive v5.4 items.** BLG-OPS-59, BLG-GOV-112, and BLG-GOV-115 all gate on the 2026-07-04 SI-05 effectiveness review. v5.4 sprint planning should seal before 2026-06-30 to allow story completion before the review. PMO Lead should flag this timing dependency at sprint planning. | PMO Lead | Flag at plan release v5.4 + sprint planning as timing dependency. |
| LL-03 | **v5.3 carry-forward (git stash monitor) forwarded.** Sprint Planning should include a reminder: after every EPIC merge, verify no uncommitted state on the EPIC branch. No prompt change needed unless recurrence confirmed in v5.4. | PMO Lead | Note in v5.4 sprint planning STEP 0 carry-forward advisory. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-06-09__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-06-09T16:00:00Z",
  "friction_item_count": 0,
  "action_now_count": 2,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
