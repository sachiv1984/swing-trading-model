Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Filed
Last Updated: 2026-08-11

---

# Lessons Learnt — Release Planning 2026-08-11__release-v8.6

## Friction Items

None. Preflight, gate-detection, and integrity steps all passed cleanly on the first pass. `scored_initiatives.md` was absent (falls back to inline estimates by design, not a friction item — the three-tier resolution rule exists for exactly this case).

## Carry-Forward

Items: 2 (from `2026-08-08__release-v8.5`'s own `lessons_learnt_closure.md`, reviewed at this cycle's STEP -1.5, out of this routine's write scope):

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Two deferred patches (`check_api_performance_baseline_drift.py` substring-match fix; `execution_prompt.md` test_scenarios roll-up) have now carried 2 consecutive cycles unapplied. | The next Post-Ship Closure (for this cycle) should consider applying both directly as immediate action rather than deferring a 3rd time. | Post-Ship |
| 2 | `reports.md` deviation concentration signal unchanged (2 of the 10-record register); next scheduled re-check not yet due. | No action needed this cycle; re-check at the 3rd deviation consolidation review. | Delivery Verification / Post-Ship |

## Observations From This Run

- The `Provisional-Target: v8.6` field, populated on 20 items during `v8.5`'s own PR-review backlog additions, functioned exactly as intended — it gave this cycle's scope selection a ready-made, pre-vetted continuation set with no re-derivation needed. Worth continuing this practice: filing forward-looking backlog items with a concrete next-release target where the source PR/review already implies one.
- `BLG-FEAT-32` and `BLG-FEAT-56` together were the only ungated, ready-now `Product Feature`-type items in the entire 311-item backlog — the same structural scarcity the `2026-08-11__scheduled` rebalance flagged (Product Value Ratio Alert-tier, 0.110) is directly visible at the release-planning layer, not just the rebalance layer. `BLG-BE-91`'s trade-plan-linkage enforcement (this cycle) is the most direct lever available to widen this pool for future cycles (unblocks `BLG-FEAT-73`'s gate once new linked plans accrue).

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-11__release-v8.6",
  "phase": "Release",
  "filed_utc": "2026-08-11T12:20:00Z",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
