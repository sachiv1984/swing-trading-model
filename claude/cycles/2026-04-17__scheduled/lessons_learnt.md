**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-04-17__scheduled
**Phase:** Roadmap Rebalance
**Last Updated:** 2026-04-17

---

# Lessons Learnt — Roadmap Rebalance 2026-04-17__scheduled

## Summary

Scheduled Standard-tier rebalance. No active initiatives. 22 stale parked ideas all re-parked with active Product Owner rationale. No ideas advancing, no debates, no decisions except the no-change log entry (DL-020). All prior-cycle CFs (1–4) confirmed resolved. One lifecycle compliance fix: duplicate AI-SUM row removed from initiative_register.md. Run completed cleanly with no friction items.

---

## What Worked Well

### Confirmation 1 — CF Resolution Audit via prompt_change_log

All four prior-cycle CFs were resolved through prompt patches recorded in `claude/system/prompt_change_log.md`. The ability to verify CF resolution by grepping the change log was fast and reliable — no ambiguity about which patches had been applied.

### Confirmation 2 — Stale idea re-park rationale retention

All 22 stale ideas had prior park rationales in the register. The re-park rationales written this cycle are substantive updates to those existing rationales, not repeats. The cycle-count increment via `sed` was reliable (21 cycle-4 rows updated in one command, 1 cycle-8 row updated separately due to different sed pattern).

---

## Friction Log

*No friction items this cycle.*

---

## Recurrence Escalations

None.

---

## Process Improvements Actioned This Run

None. No friction items identified.

---

## New Files Created This Run

| File | Path | Class |
|------|------|-------|
| run_manifest.md | claude/cycles/2026-04-17__scheduled/run_manifest.md | Class 3 |
| cycle_record.md | claude/cycles/2026-04-17__scheduled/cycle_record.md | Class 3 |
| cycle_summary.md | claude/cycles/2026-04-17__scheduled/cycle_summary.md | Class 3 |
| lessons_learnt.md | claude/cycles/2026-04-17__scheduled/lessons_learnt.md | Class 3 |

---

## Outstanding Deferred Patches

None from this cycle.

*Note: 7 carry-forwards from `2026-04-13__release-v2.7/lessons_learnt_closure.md` remain as v2.8 planning inputs — these are release-cycle carry-forwards, not rebalance-cycle deferred patches, and do not appear here.*

---

## Escalations

None.

---

## Carry-Forward

No new carry-forwards generated from this rebalance.

---

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-04-17__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-04-17T00:00:00Z",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
