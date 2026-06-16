**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-16
**Cycle:** 2026-06-16__scheduled

---

# Lessons Learnt — Roadmap Rebalance

**Invocation context:**
```
invoking_routine: roadmap_prompt.md
cycle_id: 2026-06-16__scheduled
phase: Roadmap
prior_cycle_id: 2026-06-10__scheduled
```

Feature / Trigger: N/A — scheduled run
Run: 2026-06-16__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-16
Prior cycle checked: 2026-06-10__scheduled (claude/cycles/2026-06-10__scheduled/lessons_learnt.md — found; 0 friction items; LL-01/02 both resolved this run)

---

## Cross-Cycle Recurrence Check (§3.7)

Prior cycle file: `claude/cycles/2026-06-10__scheduled/lessons_learnt.md` — loaded.
Prior friction items: 0 (clean cycle).
Deferred patches carried from prior: None.
Post-ship carry-forwards from v5.5: LL-RP-02 (action-now applied this cycle), LL-P3-03-v55 (deferred), LL-P4-01-v55 (deferred).

**LL-RP-02 recurrence:** Second occurrence of complete-item leakage into candidate lists (v5.4 LL-RP-01 was the first). Prompt_change_log confirms prior patch (v6.9→v7.0) applied. This cycle confirms root cause was compile-time vs presentation-time distinction — STEP 8.0.5 firing only before presentation allowed candidate lists to be compiled with stale data. Action-now applied this cycle (v7.0→v7.1).

**LL-P3-03-v55 / LL-P4-01-v55:** First roadmap cycle carrying these. Not a recurrence escalation. Deferred to v5.6 release planning per planned carry-forward.

---

## What Worked Well

- **All 35 Parked-cycle-1 ideas evaluated systematically.** 5 gate-cleared mandatory re-evaluations surfaced cleanly (BLG-QA-50, BLG-QA-48+54, BLG-SPEC-54 all shipped). Zero vague re-parks — all 29 re-parks had specific, §4.1-valid rationales.
- **LL-RP-02 action-now resolved structurally.** STEP 8.0.5 was upgraded from Advisory → Mandatory at two firing points (STEP 3 + STEP 8.1). Two-cycle pattern broken.
- **BLG-ID collision check caught early.** BLG-OPS-63 was already in the backlog (v5.5 latency investigation); new item assigned BLG-OPS-65 correctly.
- **STEP 8.1 soft gate fired cleanly.** Empty Now horizon identified; v5.6 section added with documented candidate scope.
- **Extended tier check correct.** CPS = 2.85 (arc pipeline artefact) — acknowledged by Strategy Rules & System Intent Owner; no new §13-adjacent items added.

---

## Friction Log

| # | Type | Description | Blast radius | Patch |
|---|------|-------------|-------------|-------|
| 1 | Type B — Process Friction | IW-20260610-01 ideas at Parked-cycle-2; 29 will reach terminal (cycle 3) at the NEXT scheduled rebalance. Rebalance interval may not allow cycle-3 ideas to expire gracefully if the next rebalance is delayed. | Low — ideas reaching terminal cycle 3 is by design; no sprint impact. | Deferred — record LL-P5-01: at next scheduled rebalance, remind PO that all 29 IW-20260610-01 ideas are at cycle-3 terminal. PMO Lead to flag at STEP 4. |

---

## Deferred Patches

| # | File | Section | Change | Owner | Target | Status |
|---|------|---------|--------|-------|--------|--------|
| 1 | `claude/system/release_planning_prompt.md` | STEP 7 (Scope Definition) or STEP 1 (Readiness) | Add advisory: gated stories with within-sprint date gates should be classified as conditional (not firm Sprint 2) at release planning. Pattern observed in v5.4 (ST-03 returned), v5.5 (ST-11–14 returned). If v5.6 repeats, make this mandatory guidance. | PMO Lead | v5.6 release planning (plan release v5.6) | Carry-forward from v5.5 LL-P3-03-v55 + LL-P4-01-v55; first roadmap cycle carrying |

---

## Outstanding Actions

| # | ID | Action | Owner | Target |
|---|----|--------|-------|--------|
| 1 | LL-P5-01 | At next scheduled rebalance STEP 4: flag that all 29 IW-20260610-01 ideas are at Parked-cycle-2 and will reach terminal cycle 3 at that run — PO must actively Advance, Reject, or Backlog (gate-conditional) all; re-parking beyond cycle 3 is not permitted | PMO Lead | 2026-06-16__scheduled (next rebalance STEP 4) |
| 2 | LL-P5-02 | release_planning_prompt.md patch (LL-P3-03-v55/LL-P4-01-v55): apply conditional sprint guidance at v5.6 release planning | PMO Lead + Head of Specs Team | v5.6 release planning |

---

## Process Observations (Not Friction)

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-05 | **v5.6 release planning can proceed immediately.** v5.6 Now section added with candidate scope. `plan release --version v5.6` is the next governed command. BLG-FE-64 gate clears 2026-06-21 — early planning start is recommended to hit gate. | PMO Lead | Inform user. |
| LL-06 | **29 ideas at Parked-cycle-2 (IW-20260610-01).** At the NEXT scheduled rebalance, all 29 reach terminal (cycle 3 hard cap). PO must actively resolve each — re-parking beyond cycle 3 is not permitted. See LL-P5-01. | PMO Lead | Noted as LL-P5-01 outstanding action. |
| LL-07 | **2026-07-04 SI-05 effectiveness review date approaching (18 days).** Multiple gate-conditional items (BLG-GOV-112/113/114/115, BLG-GOV-121, IDEA-product-owner-20260610-02, IDEA-metrics-analytics-20260610-02, etc.) are blocked on this date. Post-review, several ideas may advance from Parked-cycle-2 to Advance at the next rebalance. | PMO Lead | Surface at next rebalance STEP 4 gate-condition re-check. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-06-16__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-06-16T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
