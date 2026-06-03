**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-03
**Cycle:** 2026-06-03__scheduled

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled run
Run: 2026-06-03__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-03
Prior cycle checked: 2026-06-02__scheduled (claude/cycles/2026-06-02__scheduled/lessons_learnt.md — found)

---

## What worked well

- **Overdue patch resolved cleanly.** The backlog_management_prompt.md STEP 6.2 post-write verification patch (OVERDUE at STEP -1.5) was applied promptly within the same session before the run proceeded. The OVERDUE detection mechanism worked as designed — escalation to Head of Specs Team and resolution in the same session is the ideal outcome.
- **Terminal park decisions executed efficiently.** All 26 Parked-cycle-2 ideas reached terminal classification in a single STEP 4 pass. The three-cycle hard cap prevented re-parking and forced genuine decisions. 18 items were successfully converted to gate-conditional backlog items with specific gate criteria — a productive cycle despite no roadmap changes.
- **Gate-cleared promotions handled correctly.** 7 ideas had gates cleared by v5.0 deliverables (BLG-GOV-86/87/88 shipped). STEP 4.0 gate-condition re-check identified all 7 correctly. Each received a meaningful gate-cleared classification rather than a stale re-park.
- **STEP 8.1 soft gate fired and resolved cleanly.** Both conditions true (empty Now horizon + no next-release section). PO chose Option (b) — defer — with a specific rationale naming the next command. This is the second consecutive firing of this gate since the v4.9 patch; the pattern is working.
- **CPS stability confirmed.** Fifth consecutive cycle at CPS 1.15, Δ = 0.00. Governance-heavy maintenance period v4.7–v5.0 complete. No Strategy Drift Alert; no Challenger engagement required at STEP 2.

---

## Friction Log

| # | Type | Description | Blast radius | Patch |
|---|------|-------------|-------------|-------|
| F-01 | Type A (process friction) | OVERDUE deferred patch at STEP -1.5 halted the run before any artefact was created. The backlog_management_prompt.md patch was filed 2026-06-01__scheduled, carried 2026-06-02__scheduled, and missed at the 2026-06-03 `groom backlog` run (which was the stated target). | Single-cycle halt; resolved in same session; no downstream impact. | Applied this cycle (v1.7→v1.8; commit 9da50369). No further action needed for this specific patch. |

---

## Deferred Patches

| # | File | Section | Change | Owner | Target |
|---|------|---------|--------|-------|--------|
| 1 | No deferred patches this cycle. | — | — | — | — |

*All prior deferred patches resolved (backlog_management_prompt.md v1.8 applied this session). No new deferred patches filed.*

---

## Outstanding Actions

None. No escalations.

---

## Process Observations (Not Friction)

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-01 | 18 ideas converted to gate-conditional backlog items in a single rebalance is the highest single-cycle backlog addition from ideas to date. This is a one-time clearance of the accumulated Parked-cycle-2 queue. The new BLG-SPEC-44/45/46 and BLG-BE-27–31 group represents a meaningful SI-02/SI-04/Arc 4 pre-planning preparation layer. PMO Lead to monitor at next groom backlog to ensure items are correctly placed and not orphaned. | PMO Lead | Monitor at next `groom backlog` (post-v5.1 post-ship). |
| LL-02 | The `groom backlog` run at v5.0 post-ship (2026-06-03) did not archive BLG-GOV-69/70/72/78, BLG-SPEC-43 despite these items being COMPLETE. The new backlog_management_prompt.md v1.8 post-write verification would have flagged this. These 5 items should be cleaned at the next groom. | PMO Lead | Flag at next `groom backlog`: BLG-GOV-69/70/72/78, BLG-SPEC-43 COMPLETE but not archived. |
| LL-03 | BLG-GOV-73 (scheduled rebalance cadence review) is gate-eligible (meta-review cycles_since_meta_review ≥ 3 condition was met at 2026-06-02__scheduled). Consider advancing at v5.1 sprint planning if capacity allows. | PMO Lead | Flag at v5.1 sprint planning. |
| LL-04 | v5.0 carry-forward item 2 (delivery_verification_prompt.md §-1.3 Tier 2 mixed-class EPIC signer format) is still open. Target: v5.1. Head of Specs Team should apply this as an action-now patch at v5.1 release planning or sprint close. | Head of Specs Team | Apply at v5.1 release planning or sprint close. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-06-03__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-06-03T20:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
