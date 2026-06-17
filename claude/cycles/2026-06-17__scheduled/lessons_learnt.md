**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-17
**Cycle:** 2026-06-17__scheduled

---

# Lessons Learnt — Roadmap Rebalance

**Invocation context:**
```
invoking_routine: roadmap_prompt.md
cycle_id: 2026-06-17__scheduled
phase: Roadmap
prior_cycle_id: 2026-06-16__scheduled
```

Feature / Trigger: N/A — scheduled run
Run: 2026-06-17__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-17
Prior cycle checked: 2026-06-16__scheduled (claude/cycles/2026-06-16__scheduled/lessons_learnt.md — found; 1 friction item; 1 deferred patch (LL-P5-02 → OVERDUE this cycle, resolved action-now))

---

## Cross-Cycle Recurrence Check (§3.7)

Prior cycle file: `claude/cycles/2026-06-16__scheduled/lessons_learnt.md` — loaded.
Prior friction items: 1 (Type B — deferred patch targeting passed event; LL-P5-02).
Deferred patches carried from prior: 1 — LL-P5-02 (release_planning_prompt.md within-sprint date gate advisory).

**LL-P5-02 status:** OVERDUE (second consecutive roadmap cycle carrying; target event v5.6 release planning has passed). Action-now applied this cycle: release_planning_prompt.md v2.35→v2.36 STEP 1.4b. **Resolved.**

**LL-P5-01:** Actioned at STEP 4 as planned — all 29 terminal cycle ideas resolved. No recurrence.

---

## What Worked Well

- **Terminal cycle 3 resolution clean and efficient.** All 29 IW-20260610-01 ideas resolved in a single STEP 4 sweep. Gate-condition re-check confirmed 0 mandatory re-evaluations (no gates cleared since 2026-06-16). 28 rejections + 1 Backlog (gate-conditional) — appropriate disposition profile.
- **STEP 8.0.5 compile-time pre-clean functioned correctly.** BLG-QA-50 and BLG-BE-34 identified as COMPLETE and excluded before candidate list presented to PO.
- **STEP 8.1 soft gate fired and resolved without escalation.** PO selected Option (a) immediately — v5.9 Now section added with BLG-FE-64/41 as firm (gate clears in 4 days) and 5 conditional items per STEP 1.4b.
- **New STEP 1.4b rule applied correctly to v5.9 conditional scope.** BLG-GOV-112/113/115/130/BLG-OPS-59 correctly classified as conditional (gate 2026-07-04) per the action-now patch applied earlier in this same run.
- **STEP 8.6 guardrail correctly identified as non-applicable** (zero advancing candidates; empty queue).

---

## Friction Log

| # | Type | Description | Blast radius | Patch |
|---|------|-------------|-------------|-------|
| 1 | Type B — Process Friction | LL-P5-02 deferred patch from 2026-06-16__scheduled had a target ("v5.6 release planning") that had already passed when the deferred patch was filed. Root cause: the patch was carried from v5.5 post-ship cycle (where "v5.6 release planning" was in the future), but by the time it reached the roadmap rebalance cycle (2026-06-16__scheduled), v5.6/v5.7/v5.8 had all shipped. The deferred patch target was stale at the time of filing in the roadmap cycle. | Low — caught by 2-cycle consecutive carry rule; resolved action-now. Blast if uncaught: within-sprint date gate pattern would continue recurring across further releases. | Action-now applied (release_planning_prompt.md v2.35→v2.36 STEP 1.4b). Deferred meta-review patch: roadmap_prompt.md STEP -1.5 — add check: when validating deferred patches, if the target event is a named release (plan release vX.Y), verify that release has not already shipped by checking release summary table in current_roadmap.md; if shipped → classify OVERDUE immediately rather than waiting for 2-cycle consecutive carry rule. Owner: PMO Lead. Target: next scheduled rebalance. |

---

## Deferred Patches

| # | File | Section | Change | Owner | Target | Status |
|---|------|---------|--------|-------|--------|--------|
| 1 | `claude/system/roadmap_prompt.md` | STEP -1.5 (Prior Cycle Outstanding Actions) | Add check: when validating deferred patches targeting a named release event (plan release vX.Y), verify whether that release has already shipped by checking current_roadmap.md release summary table; if shipped → classify OVERDUE immediately. Prevents multi-release stale deferred patches reaching the 2-cycle carry rule. | PMO Lead | Next scheduled rebalance (2026-06-17__scheduled + 1) | New — first cycle carrying |

---

## Outstanding Actions

| # | ID | Action | Owner | Target |
|---|----|--------|-------|--------|
| 1 | LL-P5-03 | Apply roadmap_prompt.md STEP -1.5 patch (stale release target check) at next scheduled rebalance if deferred patch carries | PMO Lead + Head of Specs Team | Next scheduled rebalance |

---

## Process Observations (Not Friction)

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-08 | **v5.9 release planning can proceed immediately.** v5.9 Now section added. BLG-FE-64/41 gates clear 2026-06-21 (4 days). `plan release --version v5.9` is the next governed command. | PMO Lead | Inform user. |
| LL-09 | **2026-07-04 SI-05 effectiveness review approaching (17 days).** Multiple conditional v5.9 items gated on this date. Post-review, BLG-GOV-112/113/115/130/BLG-OPS-59 may activate for firm sprint scope. PT-04/SI-02 trade count gate trajectory also accelerating (~3 more weeks to 20 trades). | PMO Lead | Surface at v5.9 release planning STEP 1.4. |
| LL-10 | **IW-20260610-01 fully resolved.** All 41 ideas from this window are now at terminal status. No open IW-20260610-01 ideas remain. | PMO Lead | Confirmed. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-06-17__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-06-17T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
