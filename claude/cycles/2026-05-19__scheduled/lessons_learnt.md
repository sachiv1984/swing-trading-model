**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Published
**Cycle:** 2026-05-19__scheduled

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: Scheduled rebalance — no completion event
Run: 2026-05-19__scheduled
Reviewed by: PMO Lead
Date filed: 2026-05-19
Prior cycle checked: 2026-05-18__scheduled-2 (no committed lessons_learnt — see friction item #1)

---

## What worked well

- Gate-condition re-check (STEP 4.0) caught IDEA-financial-reporting-20260508-02: planned_entry_price shipped v3.6, park rationale explicitly referenced that deferred item. Mandatory re-evaluation applied correctly; PO re-parked with a new rationale that does not reference the shipped item.
- Park count verification (post-write grep) confirmed all 33 Parked-cycle-N entries consistent with their count columns after bulk Python update.
- Cycle directory and write permission test confirmed clean at STEP -1.4.

---

## Friction Log

### Friction Item #1 — Type D: Prior cycles without committed artefacts

**Description:** Two prior scheduled rebalances (2026-05-18__scheduled and 2026-05-18__scheduled-2) have no committed artefacts. The state file was updated to reference `last_rebalance_cycle: "2026-05-18__scheduled-2"` and incremented `rebalance_cycles_since_meta_review` to 2, but no cycle_record, lessons_learnt, cycle_summary, or decision_log update was committed. Decision log entries DL-031/032 cited in memory records are absent from the file. Ideas_register park counts were not applied for those cycles.

**Root cause:** STEP 12 does not include a precondition that verifies artefact files exist in the cycle directory before updating the state file. The state file can be updated independently (e.g., via a post-ship closure commit), leaving the rebalance in a "completed" state with no evidence.

**Blast radius:** Misleading governance state (state file references a cycle with no evidence). Decision log gap. Ideas_register park counts two cycles behind. `rebalance_cycles_since_meta_review` counter inflated by uncommitted runs.

**Classification:** Type D — Artefact Discipline (process)

**Process patch:** Deferred — see meta_review.md for specific file, section, and one-sentence change.

---

## Recurrence Escalations

None.

---

## Process improvements actioned this run

None. The meta-review finding (STEP 11.4) was classified as a deferred patch with owner and target date.

---

## New files created this run

- `claude/cycles/2026-05-19__scheduled/run_manifest.md`
- `claude/cycles/2026-05-19__scheduled/cycle_record.md`
- `claude/cycles/2026-05-19__scheduled/cycle_summary.md`
- `claude/cycles/2026-05-19__scheduled/lessons_learnt.md`
- `claude/cycles/2026-05-19__scheduled/meta_review.md`

---

## Outstanding deferred patches

| # | Patch | File | Section | Owner | Target |
|---|-------|------|---------|-------|--------|
| 1 | Add artefact existence precondition to STEP 12.1 before state file update | `claude/system/roadmap_prompt.md` | STEP 12.1 Global State Update | Head of Specs Team | Next rebalance |

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Deferred patch: roadmap_prompt.md STEP 12.1 artefact precondition (Type D × 2) | Apply before next rebalance to prevent recurrence | Roadmap |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-05-19__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-05-19T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
