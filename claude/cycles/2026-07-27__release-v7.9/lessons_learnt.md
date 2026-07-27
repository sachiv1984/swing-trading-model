Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27
Cycle: 2026-07-27__release-v7.9

# Lessons Learnt — Release Planning — v7.9

## What worked well

- The STEP -1.2 Option (b) equivalence rule (added precedent at v7.8, confirmed again here) let this release scope cleanly off a backlog-driven pool without requiring an out-of-band roadmap-section write — the second consecutive cycle this path has worked as designed.
- The fresh `IW-20260727-01` idea-intake batch (21 ungated items, all with clean Problem/Scope/Acceptance Criteria/Owner metadata) supplied almost the entire capacity-fill pool needed to reach the top of the confirmed capacity band with no additional backlog grooming required.

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift (data consistency, not a process-prompt defect)

**Recurrence:** Not checkable (first observed instance of this specific pattern).

**What happened:** The `2026-07-27__scheduled` rebalance's own recorded outcome text (mirrored into both `.claude_current_state.json.last_rebalance_outcome` and `current_roadmap.md` §1's Last Updated history) named `BLG-FE-128` as one of two advisory pull-forward candidates for the next `plan release`. `BLG-FE-128` had already shipped as v7.8 EPIC-01 and was archived by that same day's `groom backlog` run — it could not be a valid candidate for this cycle at all. The error appears to be a stale/incorrect item reference baked into that rebalance's own summary prose, discovered only because this engine independently verified the named candidate's live status before using it as a scope input.

**Where in the routine:** STEP -1 preflight (data-consistency spot-check, not a named sub-check in `release_planning_prompt.md`).

**Root cause:** No existing STEP in `roadmap_prompt.md` cross-checks a pull-forward candidate's own live backlog/archive status against the same session's own `groom backlog` output before naming it in the rebalance's recorded outcome — the two actions (groom backlog archiving `BLG-FE-128`, and naming it as a forward candidate) both occurred in outputs attributed to the same `2026-07-27__scheduled` session record without a cross-check between them.

**Blast radius analysis:**
- What would have propagated: a future `plan release` session trusting the named candidate at face value would have attempted to include an already-shipped, archived item in fresh scope — likely caught at STEP 2/3 (item not found in the active `backlog.md` type sections, only in `backlog_archive.md`), but only after wasted scoping effort.
- When it would have surfaced: at scope-item lookup time in a future Release Planning session.
- Recovery cost if uncaught: low (a single archived-item lookup failure), but avoidable.

**Process patch:**

→ Deferred patch (cannot apply this run — outside this engine's write scope, `roadmap_prompt.md` is not in Release Planning's Write Scope list):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 8 (or wherever pull-forward candidates are named in the rebalance's own outcome text)
  - Change required: before naming a pull-forward candidate in the cycle's recorded outcome, cross-check that the same session's own `groom backlog`/post-ship-closure actions (if run earlier the same day) have not already archived/shipped it.
  - Owner: Head of Specs Team
  - Target: next governance prompt maintenance pass

## Recurrence Escalations

None carried from the prior cycle applicable to this routine (the two carried recurrence escalations from `2026-07-24__release-v7.8` closure — `execution_state.json` cross-EPIC conflict pattern, endpoint-count fallback collision — are both Sprint Execution scoped, not Release Planning; both remain open with a 2026-07-30 SLA per that closure's own escalation table, unaffected by this cycle).

## Process improvements actioned this run

None applied directly (Friction Item 1's fix is out of this engine's write scope — deferred).

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|------------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 8 (pull-forward candidate naming) | Cross-check a named pull-forward candidate's live backlog/archive status against the same session's own `groom backlog` output before naming it | Head of Specs Team | next governance prompt maintenance pass |

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-FEAT-73`/`BLG-FEAT-74` remain parked (perennial-return, Option (b)) with no revised gate-clearing signal since 2026-07-17 — a 3rd consecutive `plan release` cycle (v7.7, v7.8-adjacent rebalance, v7.9) has now passed without a fresh SI-02 live re-check succeeding (credentials absent every session this month). `BLG-OPS-121` (this cycle's own scope) directly targets this gap. | Once `BLG-OPS-121` ships, the next `plan release` should attempt a genuine live SI-02 re-check rather than citing the unchanged 2026-07-17 structured field a further time. | Release Planning |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-27__release-v7.9",
  "phase": "Release",
  "filed_utc": "2026-07-27T16:55:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
