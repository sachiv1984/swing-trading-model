Owner: Product Owner
Class: Operational Record (Class 3)
Status: Filed
Report Date: 2026-07-21
Cycle: 2026-07-21__release-v7.7

# Lessons Learnt — Release Planning — v7.7

## What worked well

- The live SI-02 gate re-check (production API, `GET /trades`, `GET /trade-plans`, `GET /analytics/behavioural-drift`) cleanly disqualified `BLG-FEAT-73` from firm scope before any sprint-planning-time surprise — the LP-05 flag on the roadmap did exactly its intended job of forcing reconfirmation rather than silent inclusion.
- Full-capacity scan of the backlog surfaced two aged P1 items (`BLG-OPS-108`, `BLG-GOV-28`) that had gone unpicked for 3+ release cycles despite explicit "pick this up next `plan release`" language in their own backlog text — this cycle closes that gap for both.

## Friction Log

### Friction Item 1

**Classification:** Type B — Process Friction (no rule violated, but the routine's own convenience was limited)

**What happened:** No `scored_initiatives.md` file exists in the repository, so the ST-14 Effort Band Lookup fell through to Tier 3 (inline STEP 4 estimate) for all 11 EPICs with no advisory required. This is compliant behaviour per `shared_standards.md §16.7`, but it means every release cycle to date has estimated effort from scratch rather than building on a durable scoring record.

**Where in the routine:** STEP 0 (scored_initiatives.md load) / STEP 4.5 (Capacity Feasibility Sense Check)

**Suggested fix:** No action required this cycle (Tier 3 is a fully compliant path). Noted for awareness only — if a future roadmap rebalance begins populating `scored_initiatives.md`, Release Planning's capacity estimates would become more consistent across cycles.

**Target:** Advisory only — no backlog item filed.

## Monitoring Carried Forward

- Design Gate required for EPIC-01 through EPIC-04 (`BLG-FEAT-75`, `BLG-FE-114`, `BLG-FE-113`, `BLG-FE-120`) — run `run design-gate --cycle 2026-07-21__release-v7.7` before `plan sprint`. EPIC-05 through EPIC-11 have no Design Gate dependency.
- SI-02 gate: 9th consecutive unchanged reading (2026-07-12 through 2026-07-21) — still NOT MET on conditions (1) and (3); condition (2) unconfirmed either way. `BLG-FEAT-73` excluded from this cycle's scope as a direct consequence; carried forward as a standing cross-cycle watch item.
- `BLG-FEAT-74` (PO-05 Lightweight Replay Mode) excluded pending a §13 determinism pre-clearance review that does not yet exist on record. Recommend Strategy Rules & System Intent Owner / Head of Specs Team schedule this review independently of any specific release cycle, so future release planning has a clean input rather than re-discovering the same gap.
- 2 carry-forward items from `2026-07-20__release-v7.6/lessons_learnt_closure.md` reviewed at STEP -1 (bounded reopen path for Published cycles; empty-Now-horizon scope-selection confirmation step) — both are process-improvement suggestions for Head of Specs Team, not actioned by this cycle (out of Release Planning's write scope / not blocking).

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-21__release-v7.7",
  "phase": "Release",
  "filed_utc": "2026-07-21T09:40:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
