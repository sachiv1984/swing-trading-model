Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-11

---

# Lessons Learnt — Release Planning 2026-11-11__release-v9.17

## Friction Items

**Friction Item 1: §1.4c step 1b's "earlier, unfinished phase" clause needed a reading on first use.** The ruling (v2.74) worked as intended for Phase 3: its 7 P3 items were seated with no Product Owner override. `BLG-BE-205` needed two judgements. It is named in the Phase 2 row's prose ("waits on `BLG-BE-205`"), not in the row's item list. And Phase 2 is marked ✅ shipped although `BLG-FE-254` stays open for TL-09/TL-10. This run read the row's text as listing the item and treated Phase 2 as unfinished. Recommendation: when post-ship closure marks a phase shipped while a split-achievability remainder is open, the phase row should say "shipped except <item>", and any item the remainder waits on should be in the row's item list. Deferred to the PMO Lead (`post_ship_closure.md` STEP 2 / `roadmap_management_prompt.md` STEP 5.2).

**Friction Item 2: a split-achievability remainder has no effort rule.** `BLG-FE-254` is open for two ACs, but its Effort field still reads L (~3-4 days). The `workforce_capacity.md` precedence rule ("the item's own day figure wins") would charge 3.5d for about 0.5d of work, and would have displaced about 3d of other items. This run used 0.5d and recorded why. Recommendation: when Post-Ship Closure leaves a source item open under split-achievability case (i), it records the remainder's estimate on the item (a dated note under Effort), and Release Planning uses that figure. Deferred to the Head of Specs Team (`post_ship_closure.md` STEP 3.1).

**Friction Item 3: a carry-forward that asks for `run roadmap` first has no enforcement point.** v9.16 Carry-Forward #3 said to run `run roadmap --reason "scheduled"` before `plan release`. The Product Owner named v9.17 directly, so §-1.2 cleared on the §1 line and the advisory was read only at STEP 0. Observation: the Product Owner may legitimately name a release without a rebalance (v9.14, v9.16, v9.17), so a hard gate would be wrong. The open action is carried in `run_manifest.md` and closure §6 row 8. No prompt change is proposed.

## Prompt Change Classification

No action-now patches. Friction Items 1 and 2 are deferred patches. Friction Item 3 is an observation.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-11-11__release-v9.17",
  "phase": "Release",
  "filed_utc": "2026-11-11T20:58:50Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 2,
  "status": "Active"
}
```
