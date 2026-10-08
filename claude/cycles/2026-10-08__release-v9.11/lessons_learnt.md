Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-08

---

# Lessons Learnt — Release Planning 2026-10-08__release-v9.11

## Friction Items

**Friction Item 1: gates that name a shipped backlog item are never re-read.** §1.3a's scripted procedure reports date-lapsed gates and resolution banners. A gate whose condition is "`BLG-X` shipped/complete" stays gated after `BLG-X` ships, because nothing checks it. A script check this run found 26 gated items whose gate names only items no longer in the active backlog:
- `BLG-OPS-179` was genuinely ready.
- `BLG-FE-195` had already been delivered by v9.10 ST-01.
- `BLG-OPS-53` and `BLG-GOV-121` were also on the date-lapsed list.
- The other 22 were not read individually. Most have a second, unmet limb.

Recommendation: extend `scan_backlog_gate_conditions.py` with a "gating item shipped — verify" list, mirroring the date-lapsed list, and add it to §1.3a's read-before-fixing-the-pool step. Backlog/tooling item, not a prompt patch this cycle.

**Friction Item 2: §1.3a's in-place gate edits come before the STEP 3.9 backlog lock.** Since v2.60, §1.3a writes `backlog.md` at STEP 1, but the backlog lock is acquired only at STEP 3.9 for the slice write. In a single-session run this is harmless, but a concurrent backlog writer could interleave with STEP 1's edits. Recommendation: acquire the backlog lock before the first §1.3a edit, or move the edits to STEP 4. Deferred to the Head of Specs Team (`release_planning_prompt.md` §1.3a / STEP 3.9; target 2026-10-20).

**Friction Item 3: several gate-cleared items still carry "verify the gate" ACs.** `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FE-84` and `BLG-FEAT-63` each keep an AC about a gate the Product Owner removed on 2026-10-05, and `BLG-SPEC-174`'s AC would edit that removed gate. All were restated in the slice. This is the same pattern as v9.10 Friction Item 3: clearing a gate does not clean up the ACs that referred to it. §1.3a bound 5 now handles this for date-lapsed items. Gates removed by a Product Owner decision outside Release Planning have no equivalent step.

## Prompt Change Classification

No action-now patches. Friction Item 2 is a deferred patch (Head of Specs Team, 2026-10-20). Friction Items 1 and 3 are tooling and backlog recommendations.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-10-08__release-v9.11",
  "phase": "Release",
  "filed_utc": "2026-10-08T09:04:49Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 1,
  "status": "Active"
}
```
