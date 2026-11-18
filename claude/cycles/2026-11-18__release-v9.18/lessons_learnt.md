Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-18

---

# Lessons Learnt — Release Planning 2026-11-18__release-v9.18

## Friction Items

**Friction Item 1: the remainder-estimate rule did not reach the first remainder it applied to.** `LL-v9.17-Release-02` (applied at v9.17 post-ship closure, `post_ship_closure.md` v2.48 STEP 3.1) says closure writes a dated remainder estimate under the open item's Effort. The same closure left `BLG-OPS-217` open under case (i), but no note was written: the rule was patched in that run's STEP 8, after STEP 3.1 had already run. This run estimated 0.25d itself and recorded why. Observation: a one-off timing gap, not a rule defect; the next closure applies the rule from the start. No prompt change proposed.

**Friction Item 2: a deferred lessons-learnt action's tracking item can miss step 1a.** v9.17's `lessons_learnt_closure.md` assigns `LL-v9.17-P3-03` to the existing item `BLG-OPS-220`, "v9.18 Release Planning". Step 1a (`ESC-CLOSE-20261103-02`) tests the item's `Source` (must name a Post-Ship Closure STEP 8 `LL-*` action) and its `Provisional-Target` (must be this release). `BLG-OPS-220` was filed earlier from a PR review and reads `TBD`, so it fails both. This run seated it on the rule's purpose and listed it for Product Owner confirmation. Recommendation: when Post-Ship Closure STEP 8 assigns a deferred action to an *existing* item, it sets that item's `Provisional-Target` and appends the `LL-*` ID to its `Source`, as it does for a newly filed item. Deferred to the Head of Specs Team (`post_ship_closure.md` STEP 8).

**Friction Item 3: a roadmap section's committed item outside a programme phase has no §1.4c tier.** The v9.18 section says `BLG-QA-260` is "committed here, so no separate override is needed for seating", but §1.4c seats only P1/P2, step 1a, programme-phase items (step 1b) and the round-robin. A P3 item committed in a Now-horizon section but listed in no phase is reachable only by override. This run recorded an override with the Product Owner's 2026-11-12 date. Recommendation: either §1.4c gains a step for items a rebalance commits to this release's §3 section, or the rebalance lists such items in a programme phase row. Deferred to the Head of Specs Team, with the PMO Lead (`release_planning_prompt.md` §1.4c / `roadmap_prompt.md` STEP 8.1).

## Prompt Change Classification

No action-now patches. Friction Items 2 and 3 are deferred patches. Friction Item 1 is an observation.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-11-18__release-v9.18",
  "phase": "Release",
  "filed_utc": "2026-11-18T09:38:21Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 2,
  "status": "Active"
}
```
