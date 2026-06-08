**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__scheduled

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled run
Run: 2026-06-08__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-08
Prior cycle checked: 2026-06-07__scheduled (claude/cycles/2026-06-07__scheduled/lessons_learnt.md — found; 0 OAs, 1 deferred patch DP-1)

---

## What Worked Well

- **BLG-QA numbering collision caught at write time.** BLG-QA-50 was discovered to already exist (added at v5.2 post-ship closure) when appending to backlog.md. The collision was corrected before commit; IDs shifted to BLG-QA-51–54 and the DL-040 table was updated accordingly. The discrepancy was caught within the write pass — no downstream artefacts were affected.
- **Challenger Type-A counter-arguments were substantive.** The Arc 6 data audit Candidate 11 debate produced a genuine cost/benefit argument (PO accepted — 1 of 20 candidates parked post-debate). The STEP 8.6 guardrail was satisfied by both conditions independently.
- **Idea intake (IW-20260608-01) executed cleanly.** All 22 eligible agents submitted 2 net-new ideas. Parked queue §2.0 pre-check prevented any backlog-overlap submissions. 0 stale ideas (Parked-cycle-2 count was 0 going in; 12 at Parked-cycle-2 exiting).
- **v5.3 candidate scope is well-defined.** STEP 8.1 Option (a) fired for the second consecutive cycle; the v5.3 section now exists with a clear P1/P2 priority-ordered candidate list. The next release planning kickoff can proceed directly.

---

## Friction Log

| # | Type | Description | Blast radius | Patch |
|---|------|-------------|-------------|-------|
| F-01 | Type D (tooling gap) | BLG-ID collision: BLG-QA-50 was allocated in DL-040 before discovering it already existed in backlog.md (added at v5.2 post-ship closure). The roadmap engine does not verify existing BLG IDs before assigning new ones — the check only happens when writing to backlog.md. | Low — corrected within same run before commit. DL-040 table, cycle_summary.md, and current_roadmap.md all updated to BLG-QA-51–54. No downstream artefact was misprinted in a committed state. | Deferred: consider adding a "verify next available BLG-ID for each series" advisory step to the roadmap engine's STEP 8.5.B write plan construction. Specifically: before assigning new BLG-IDs in STEP 5 debate summaries, grep backlog.md for the highest existing ID in each series. Low-priority — occurs rarely (when an ID is added to backlog.md between the rebalance date and the rebalance run). |

---

## Deferred Patches

| # | File | Section | Change | Owner | Target |
|---|------|---------|--------|-------|--------|
| 1 | claude/system/idea_intake_prompt.md | §2.0 Parked Queue Pre-Check | Add advisory: "Before generating new submissions, briefly scan active backlog.md items for scope overlap with planned submissions." Advisory only — not a hard gate. | Head of Specs Team | v5.3+ prompt review |
| 2 | claude/system/roadmap_prompt.md | STEP 8.5.B Write Plan | Add advisory: "Before assigning new BLG-IDs in debate summaries, grep backlog.md for the highest existing ID in each series to prevent collision." Advisory only. | Head of Specs Team | v5.3+ prompt review |

*Note: DP-1 (idea_intake_prompt.md §2.0) is carry-2 of the patch first filed at 2026-06-07__scheduled. It will become OVERDUE if not addressed by the next scheduled rebalance.*

---

## Outstanding Actions

None. No escalations.

---

## Process Observations (Not Friction)

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-01 | 12 ideas are now at Parked-cycle-2 (will expire at cycle 3 if not advanced/rejected). These are primarily SI-05 in-app, compliance sparkline, P&L retrospectives, and Arc 4 pre-specs that are genuinely gate-blocked (BLG-FE-45, SI-02 frontend activation, BLG-FEAT-20). At the next rebalance, PO must actively Advance, Reject, or Backlog (gate-conditional) all 12 — re-parking is not permitted at Parked-cycle-3. | PMO Lead | Highlight at next rebalance STEP 4. |
| LL-02 | **Meta-review is due next cycle.** Last meta-review: 2026-06-02__scheduled. Completed cycles since: 2 (2026-06-07__scheduled + 2026-06-08__scheduled). One more cycle triggers the 3-cycle meta-review requirement. PMO Lead should prepare by loading lessons learnt from 2026-06-07__scheduled and 2026-06-08__scheduled for aggregation. | PMO Lead | Conduct meta-review at next scheduled rebalance. |
| LL-03 | **Gate-conditional items BLG-GOV-113/114 are time-sensitive.** Both must complete before 2026-07-01 (3 days before the SI-05 effectiveness review on 2026-07-04). If v5.3 sprint planning does not seal before 2026-07-01, these items need to be actioned outside the sprint. | PMO Lead; Director of Quality | Flag at v5.3 sprint planning as pre-sprint-seal requirement. |
| LL-04 | BLG-GOV-106 (PT-04 gate re-verification) is P1 and must complete before v5.3 sprint planning seals. The current trade count (6 as of v4.6) is stale; if the gate has cleared, PT-04 should enter v5.3 scope. | PMO Lead | Surface in plan release v5.3 STEP -1. |
| LL-05 | DP-1 (idea_intake_prompt.md §2.0 backlog scan advisory) is at carry-2 after this run. It becomes OVERDUE at the next scheduled rebalance. Head of Specs Team must apply or formally defer with a new target date before then. | Head of Specs Team | Apply at v5.3+ prompt review or escalate if not possible. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-06-08__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-06-08T10:30:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 2,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
