Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Complete
Last Updated: 2026-08-14
Cycle: 2026-08-14__release-v8.8

# Lessons Learnt — Release Planning 2026-08-14__release-v8.8

## Carry-Forward

Items: 0 — `2026-08-12__release-v8.7`'s own `lessons_learnt_closure.md` was checked at STEP -1.5/STEP 0 of this run; `action_now_count: 0`, no `## Carry-Forward` section content applicable this cycle.

## Observations From This Run

- **Sizing decision surfaced explicitly, not assumed.** Unlike `v8.7` (where "use full capacity, user features to be prioritised" was a standing user directive carried into the invocation), this cycle had no such directive. Rather than silently defaulting to either a minimal `Provisional-Target`-only scope or an arbitrary full-capacity fill, the choice was surfaced to the Product Owner as an explicit decision (tight ~5.25-day scope vs. widened ~20.5-day scope). Worth carrying forward as the default behaviour whenever `plan release` is invoked without `--capacity`/`--timebox` and the `Provisional-Target`-tagged pool alone would leave significant capacity headroom.
- **A shortlisted item was already complete.** `BLG-GOV-292` matched the "governance correctness fix" theme and passed the gate-detection scan as ungated, but its own `Provisional-Target` field carried a `✅ COMPLETE` marker from a direct resolution 3 days prior, pending archival at the next `groom backlog` pass. The gate-detection script (correctly) only checks for *gate* conditions, not completion status — a reminder that `scan_backlog_gate_conditions.py`'s "ungated" output is necessary but not sufficient confirmation an item is live, unclaimed scope. Recommend: when `groom backlog` next runs, confirm `BLG-GOV-292` archives cleanly (it should have been swept at the last grooming pass but the completion postdates it).
- **The ungated P1/P2 pool is nearly exhausted.** Only 7 ungated P1/P2 items exist across the entire 275-item backlog (`BLG-BE-97`, `BLG-FE-161`, `BLG-FE-162`, `BLG-GOV-105`, `BLG-OPS-143`, `BLG-OPS-144`, `BLG-OPS-145`) — 6 of the 7 were selected into this cycle's scope (`BLG-GOV-105` was the sole exclusion, process-only). This means the next release's P1/P2 scope will be sourced almost entirely from newly-filed items or gate-clearance events, not from an existing backlog of ready high-priority work. Worth flagging to the next scheduled rebalance as a scoping-input signal.

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-14__release-v8.8",
  "phase": "Release",
  "filed_utc": "2026-08-14T15:50:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
