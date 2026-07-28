Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-28
Cycle: 2026-07-28__release-v7.10

# Lessons Learnt — Release Planning — v7.10

## What worked well

- The "ungated pool" scan (backlog items with no `**Gate criteria:**`/`**Gate:**` field) cleanly reproduced the same 181/180-item A-category figure already cited in the `2026-07-28__scheduled` rebalance's own outcome text, cross-validating both the rebalance's structural heuristic and this engine's independent scan.
- Grouping 23 stories into 6 thematically-coherent EPICs (rather than one EPIC per story, the pattern used at every recent release including v7.9) worked cleanly against this backlog-driven pool — no forced groupings were needed; every selected item slotted naturally into exactly one of Backend/Security/QA/Contract/Frontend/Governance themes.

## Friction Log

### Friction Item 1

**Classification:** Type C — Self-caught verification error (not a prompt or backlog defect)

**Recurrence:** No.

**What happened:** An initial `-1.5`/`-1.7` prompt-change-log-integrity spot-check used a grep pattern (`"9.6→9.7"`, `"2.20→2.21"`) that omitted the literal `v` prefix the log actually uses (`v9.6→v9.7`, `v2.20→v2.21`), producing a false-negative "no entry found" result. Both entries were in fact present and correctly filed. Caught before being recorded as an advisory by re-running the check with the exact `vOLD→vNEW` string.

**Where in the routine:** STEP -1.5 / STEP -1.7 advisory checks (self-verification, not a named sub-check failure).

**Root cause:** Ad hoc grep pattern construction rather than a canonical, reusable check string for this advisory (the prompt itself does not specify a literal search pattern for `-1.7`, leaving it to session judgment).

**Blast radius analysis:**
- What would have propagated: a false advisory warning recorded in `run_manifest.md` claiming two prompt versions had no change log entry, when both did.
- When it would have surfaced: immediately, on a human or future-session cross-check against `prompt_change_log.md`.
- Recovery cost if uncaught: low (a single incorrect advisory line), but worth noting since it is exactly the kind of false-positive `shared_standards.md §11`'s enforcement note warns against.

**Process patch:** None filed — this is a single-session verification-method note, not a prompt defect. No change to `release_planning_prompt.md` or `shared_standards.md` is warranted from one instance.

### Friction Item 2

**Classification:** Type A — Data consistency (stale field, not a process-prompt defect)

**Recurrence:** Not checkable (first observed instance).

**What happened:** `BLG-BE-68`'s `Provisional-Target` field read `v7.7` (a specific past release) despite the item never having been included in any release's `stage4_backlog_slice.md` through v7.9 — a stale horizon label left over from whenever it was first estimated, not cleared when v7.7 shipped without it.

**Where in the routine:** STEP 2 scope extraction (item detail read for `S2-01`).

**Root cause:** No existing check flags a backlog item whose `Provisional-Target` names a release that has already shipped without that item. `backlog_management_prompt.md`'s STEP 1 validation (day-range requirement, §16.12) checks the field's *format*, not whether its named release has already passed.

**Blast radius analysis:**
- What would have propagated: nothing incorrect — the field is advisory only (§16.6: "a signal, not a commitment"), and this session updated it to `v7.10` along with all other selected items regardless of its prior value. No functional or scope error resulted.
- When it would have surfaced: at any future Release Planning session that read this field literally without checking whether the named release had already shipped.
- Recovery cost if uncaught: negligible — the field carries no gating authority.

**Process patch:** None filed this cycle — single low-impact instance, field is explicitly advisory per its own spec. If this pattern recurs at a future release (a second stale-shipped-release `Provisional-Target` found), file a `BLG-GOV-*` item for `backlog_management_prompt.md` STEP 1 to flag it as a Type A recurrence.

## Recurrence Escalations

None carried from the prior cycle applicable to this routine. `2026-07-27__release-v7.9`'s own `lessons_learnt.md` carried one deferred patch (`roadmap_prompt.md` STEP 8 pull-forward candidate cross-check, Head of Specs Team) — that patch's target was "next governance prompt maintenance pass," not scoped to this release planning cycle, and is not actionable within this engine's write scope regardless.

## Process improvements actioned this run

None (both friction items above were assessed as not warranting a prompt patch from a single instance).

## Outstanding deferred patches

None.

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-BE-68` carried a stale `Provisional-Target: v7.7` through 3 releases (v7.7/v7.8/v7.9) without correction — the field has no automated staleness check against already-shipped releases. | If a second such stale-shipped-release `Provisional-Target` is found at a future release planning or backlog grooming session, file a `BLG-GOV-*` item extending `backlog_management_prompt.md` STEP 1 to flag (not silently correct) any `Provisional-Target` naming a release already marked `✅ Complete` in `current_roadmap.md`. | Release Planning / Backlog Management |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-28__release-v7.10",
  "phase": "Release",
  "filed_utc": "2026-07-28T23:40:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
