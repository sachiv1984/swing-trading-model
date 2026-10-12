Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-12

---

# Lessons Learnt — Release Planning 2026-10-12__release-v9.12

## Friction Items

**Friction Item 1: a closure action due "before `plan release`" cannot be closed by Release Planning.** v9.11 closure action #8(b) asks for a `release_planning_prompt.md` §1.3a change before this run. Release Planning cannot write `claude/system/` (§7), and no engine with that write scope ran between the closure and this run. So the action arrived open and leaves open, past its deadline, with no route to close it. No AC was affected this time, because no gate had been removed by a Product Owner decision since v9.11. Recommendation: a closure action that needs a prompt change should either be applied at the closure under its deviation-compliance or lessons-learnt carve-out, or be filed as a backlog item with a sprint target, not a deadline of "before `plan release`". Deferred to the Head of Specs Team (`post_ship_closure.md` outstanding-actions guidance).

**Friction Item 2: same-release `Provisional-Target` tags crowd out of an oldest-first round-robin.** 22 of the 31 items tagged `v9.12` were left unselected. Most are v9.11 follow-ups filed on 2026-10-08, so they are the newest in their categories and the round-robin reaches them last. This is the intended result of `ESC-CLOSE-20260923-01` (tags carry no selection weight). The cost is that `groom backlog` will find about 22 stale tags at the v9.12 closure, and the tag keeps signalling a target the method will not honour. Recommendation: when filing a follow-up item, set `Provisional-Target: TBD` unless the release is committed to it on the roadmap. Backlog-hygiene recommendation, no prompt patch.

**Friction Item 3: the STEP 4 calibration changes which items the round-robin selects.** Raising 3 selected items' estimates (+1.35d) changed the final picks: `BLG-FE-210` (0.15d) seated in place of `BLG-FE-208` (1.0d). The calibration check sits in STEP 4, after the §1.4c selection it affects, so a run that follows the prompt in order must calibrate, reselect and recheck. This run calibrated the whole pool before selecting. Recommendation: move the calibration check's instruction into §1.4c as a pre-selection step, or state in STEP 4 that it applies to the ready pool before selection. Deferred to the Head of Specs Team (`release_planning_prompt.md` §1.4c / STEP 4).

## Prompt Change Classification

No action-now patches. Friction Items 1 and 3 are deferred patches (Head of Specs Team). Friction Item 2 is a backlog-hygiene recommendation.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-10-12__release-v9.12",
  "phase": "Release",
  "filed_utc": "2026-10-12T14:51:30Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 2,
  "status": "Active"
}
```
