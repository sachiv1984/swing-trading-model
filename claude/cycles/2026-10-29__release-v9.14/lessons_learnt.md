Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-29

---

# Lessons Learnt — Release Planning 2026-10-29__release-v9.14

## Friction Items

**Friction Item 1: deferred lessons-learnt patches targeted at a release have no place in §1.4c.** v9.13's closure deferred three patches (`BLG-QA-238`, `BLG-GOV-397`, `BLG-GOV-398`) to the "v9.14 sprint". They are P3, filed 2026-10-29, so the oldest-first round-robin never reaches them. But if v9.14 ships without them, `roadmap_prompt.md` STEP -1.5's stale-release-target rule makes them OVERDUE at once and halts the next rebalance. Seating them took a Product Owner override this run. Recommendation: add a §1.4c tier after P1/P2 for backlog items that track a deferred lessons-learnt patch targeted at this release, with the same standing as roadmap-committed items. Deferred to the Head of Specs Team (`release_planning_prompt.md` §1.4c).

**Friction Item 2: gates on roadmap feature IDs are invisible to the gating-item-shipped check.** `BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23` and `BLG-GOV-26` are gated only on "PT-04 shipped", which happened at v6.1 (2026-06-23). `BLG-FEAT-26` adds a further limb. The scan detects only `BLG-*` IDs, so these items have sat gated for 18 releases, and §1.3a gives this run no authority to dispose of them. Recommendation: extend `scan_backlog_gate_conditions.py` to treat a roadmap feature ID (PT-xx, SI-xx, PO-xx) as shipped when `current_roadmap.md` marks it ✅ Shipped. Until then, `groom backlog` should clear these six. Deferred to the Head of Specs Team (scan script) and the PMO Lead (groom).

**Friction Item 3: planning on stale rebalance diagnostics.** No rebalance ran between v9.13's closure and this run, although the even cycle count (90) advised one (DL-087 allowed skipping it). The Skill-Silo and PVR readings this plan relies on are from DL-086, two releases old. PO-02's 6-month AI-journal precondition probably passed around 2026-10-20, but nobody has verified it, and that is a roadmap-level question. Observation: run `run roadmap --reason "scheduled"` before `plan release v9.15`.

**Friction Item 4: "archive at groom" items persist across groom runs.** `BLG-GOV-142` and `BLG-GOV-360` (5th carry), `BLG-FE-195` (3rd), `BLG-GOV-374` (2nd) and `BLG-GOV-361` were again flagged for archiving. `GROOM-20261029-01` ran the same day and archived 41 items, but not these. Recommendation: `groom backlog` should read the latest Release Planning `run_manifest.md`'s "archive at `groom backlog`" items as an input list. Deferred to the PMO Lead (`backlog_management_prompt.md`).

## Prompt Change Classification

No action-now patches. Friction Items 1, 2 and 4 are deferred patches. Friction Item 3 is an observation for the next rebalance.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-10-29__release-v9.14",
  "phase": "Release",
  "filed_utc": "2026-10-29T12:54:53Z",
  "friction_item_count": 4,
  "action_now_count": 0,
  "deferred_count": 3,
  "status": "Active"
}
```
