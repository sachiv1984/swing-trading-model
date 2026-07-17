**Owner:** Head of Specs Team
**Status:** Filed
**Release:** v7.4
**Cycle:** 2026-07-17__release-v7.4
**Last Updated:** 2026-07-17

---

# Lessons Learnt — Release Planning v7.4

## Friction Items

1. **`BLG-GOV-248` cost/benefit note was not pre-produced.** The item's own acceptance criteria said "Note produced ahead of the next `plan release v7.4` invocation" but no such note existed in the repo at invocation time. The release planning engine performed the analysis directly at STEP 3 instead of halting/escalating, since the underlying question (bundle vs. split) is squarely within this engine's STEP 3 authority and the analysis was straightforward given the backlog item's own stated facts (no data-model dependency between the 4 items). No escalation was needed, but future governance-input items filed with a "ahead of next invocation" deadline should be tracked with a due-date reminder, not just a `Provisional-Target` field, so gaps like this are caught before the dependent routine runs rather than discovered by it.

2. **User invocation named an already-shipped release version.** The user typed "plan release v7.3" — a cycle already `Verified`/`Closed`/`post_ship_complete`. Caught by a pre-execution state check (reading `.claude_current_state.json` before invoking the engine) and confirmed with the user before proceeding, rather than either blindly re-running planning against a closed cycle or silently substituting the version. Recommend: no prompt change needed — this was a session-level catch outside the engine's own STEP -1.2 (which would have passed either way, since v7.3 *does* still have its historical roadmap section).

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | RISK-05 (`BLG-FE-115`/`BLG-FE-118` missing §13 pre-checks) is a must-resolve-before-sprint-planning-seal item, first surfaced by `BLG-GOV-250`. | Design Gate Engine (`run design-gate --cycle 2026-07-17__release-v7.4`) must explicitly confirm or rule out §13 applicability for both items before `plan sprint` seals. | Design Gate / Sprint Planning |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-17__release-v7.4",
  "phase": "Release",
  "filed_utc": "2026-07-17T12:35:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
