Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-03

---

# Lessons Learnt — Release Planning 2026-11-03__release-v9.15

## Friction Items

**Friction Item 1: §1.4c's P2-first tier cuts across a roadmap programme's phasing.** DL-088 placed the Site Structure & Usability programme's Phase 2/3 items at v9.16/v9.17 as "provisional targets, not commitments". It also filed four of them at P2 (`BLG-FE-255`, `256`, `260`, `264`; 8.5d) with no gate or dependency. §1.4c's P2-first step would therefore seat them in v9.15, ahead of the Phase 1 specs they are sequenced after. The rule cannot tell a provisional programme placement from an ordinary P2. The Product Owner held them to their phases, which needed an override. The same will recur at v9.16 for the Phase 3 P2 (`BLG-FE-260`). Recommendation: when a rebalance records a phased programme, have it either gate each later-phase item on its phase's release ("not before `plan release v9.16`") or record in §1.4c that a DL-recorded programme phase is honoured as a standing override. Deferred to the Head of Specs Team (`release_planning_prompt.md` §1.4c) and the Product Owner (`roadmap_prompt.md` STEP 8.1 programme recording).

**Friction Item 2: already-met items reach selection.** Two round-robin picks were already met:
- `BLG-GOV-185`: v9.14 deferred it at planning as already met (ST-51), but no banner was added, so it re-entered the pool.
- `BLG-GOV-192`: its proposed cadence predates the item, in `claude/audit.py`.

Both were caught only by reading after selection, and the selection was rerun twice (the second rerun also removed `BLG-OPS-195`, which depended on an item the first rerun dropped). Recommendations:
- A story `deferred_at_planning` as already met should get a ✅ COMPLETE banner at that cycle's closure. Deferred to the PMO Lead (`post_ship_closure.md` backlog step).
- The 10 legacy `Gate criteria: None` governance items (`BLG-GOV-192`–`201`) have a Proposed solution, no AC, and an "S (~0.5-2 days)" estimate. They should be groomed (AC, estimate, or kill) before they are seated again. Three of them (`BLG-GOV-193`–`196`) needed restated ACs this run. Deferred to the PMO Lead (`groom backlog`).

**Friction Item 3: the STEP 4 calibration check reads Scope text only.** `BLG-FE-243`'s AC ("no user-facing 'today' date in `src/` from `toISOString()`") and `BLG-FE-246`'s AC ("every FX input label in `src/`") are sweeps. The Scope-text scan did not flag them. A manual AC read caught both, and the counts were named (15 sites in 10 files; about 8). Recommendation: extend the STEP 4 calibration wording to "Scope or Acceptance Criteria text". Deferred to the Head of Specs Team (`release_planning_prompt.md` STEP 4).

**Friction Item 4: a verification item met by a planning run has no close path.** `BLG-GOV-400` (post-merge AC of v9.14 ST-45) is met by this run's gate-scan reading. Release Planning may not edit any field but a gate, so the item stays open until `groom backlog`. Observation: the next `groom backlog` should banner it, citing this run's `run_manifest.md`. No prompt change is proposed for one instance.

## Prompt Change Classification

No action-now patches. Friction Items 1, 2 and 3 are deferred patches. Friction Item 4 is an observation for the next `groom backlog`.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-11-03__release-v9.15",
  "phase": "Release",
  "filed_utc": "2026-11-03T15:40:00Z",
  "friction_item_count": 4,
  "action_now_count": 0,
  "deferred_count": 3,
  "status": "Active"
}
```
