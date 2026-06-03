**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-02
**Cycle:** 2026-06-02__scheduled

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled run
Run: 2026-06-02__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-02
Prior cycle checked: 2026-06-01__scheduled (claude/cycles/2026-06-01__scheduled/lessons_learnt.md — found)

---

## What worked well

- **Meta-review executed cleanly.** 3rd cycle since last meta-review triggered correctly; all required lessons learnt files loaded; action-now determination made by Head of Specs Team; patch applied in same session. The meta-review mechanism is functioning as designed.
- **Terminal idea dispositions were clean.** All 4 Parked-cycle-2 ideas at terminal status received appropriate PO dispositions (3 → Promoted-Backlog gate-conditional; 1 → Rejected/merged). No vague re-parks attempted.
- **Zero-sum rule trivially satisfied.** No new roadmap initiatives added (all advancing ideas → backlog pre-work items). STEP 9.0 passed without friction.
- **STEP 8.1 soft gate worked correctly.** The newly added soft gate (BLG-GOV-78, v4.9) fired correctly: both conditions were true (empty Now horizon + no next-release section). PO chose Option (a) and v5.0 scope was established with no ambiguity.
- **STEP 8.6 guardrail satisfied naturally.** Challenger issued one type-A counter-argument (Debate 3 — SI-02 information asymmetry) without needing a pivot loop. The debate produced a meaningful scoping refinement (assessment scope with UX risk evaluation).

---

## Friction Log

*(No friction items identified this cycle. The following observations are process-quality notes.)*

---

## Deferred Patches

| # | File | Section | Change | Owner | Target |
|---|------|---------|--------|-------|--------|
| 1 | claude/system/backlog_management_prompt.md | Archive write verification step | Add post-write grep check to confirm archived items removed from backlog.md | Head of Specs Team | Next groom backlog |

*Note: Deferred Patch 1 from idea_intake_prompt.md (originally filed 2026-06-01__scheduled) was APPLIED this cycle as a meta-review action-now. Remaining deferred patch for backlog_management_prompt.md is carried forward (target: next groom backlog — unchanged from 2026-06-01__scheduled).*

## Outstanding Actions

None. The backlog_management_prompt.md deferred patch has a named owner and target date. No escalations.

---

## Process Observations (Not Friction)

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-01 | CPS stable at 1.15 for four consecutive cycles. No strategic complexity creep during the governance-heavy v4.7–v4.9 period. This is expected for a maintenance-and-hardening phase; monitor when Arc 5 (SI-04, SI-05) and Arc 4 enter active planning. | Strategy Rules & System Intent Owner | Monitor. No action. |
| LL-02 | 30 ideas now at Parked-cycle-2 (up from 4 at start of this cycle). At the next scheduled rebalance, all 30 will be at their terminal park decision point (Parked-cycle-3 threshold). PO should pre-review the list before the next run to reduce STEP 4 burden. PMO Lead to surface this at next rebalance preflight. | PMO Lead | Surface at next rebalance STEP -1.5. |
| LL-03 | v5.0 scope established efficiently in STEP 8.1. The v4.9 BLG-GOV-78 patch (soft gate) is demonstrably working: this is the first rebalance since the patch where the soft gate fired and PO made a formal recorded decision. No ambiguity left in the planning record. | PMO Lead | Mark BLG-GOV-78 resolution confirmed in this cycle. |
| LL-04 | BLG-GOV-73 (scheduled rebalance cadence review) is now gate-eligible: its gate condition is "meta-review cycles_since_meta_review ≥ 3" which was just satisfied. PO should advance this to v5.0 sprint planning for a lightweight cadence review to determine if there's value in a lighter-weight mode for no-change cycles. | PMO Lead | Flag at v5.0 sprint planning. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-06-02__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-06-02T18:00:00Z",
  "friction_item_count": 0,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
