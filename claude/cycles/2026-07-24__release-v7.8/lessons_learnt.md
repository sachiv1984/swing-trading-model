Owner: Product Owner
Class: Operational Record (Class 3)
Status: Filed
Report Date: 2026-07-24
Cycle: 2026-07-24__release-v7.8

# Lessons Learnt — Release Planning — v7.8

## What worked well

- The `2026-07-24__scheduled` rebalance's STEP 8.1 Option (b) rationale gave this cycle an explicit, actionable scope-selection path ("scope a release around ungated backlog items") rather than leaving `--version v7.8` unresolvable against an empty roadmap section — the §-1.2 fallback clause (documented Option (b) decision treated as equivalent to a formal planned-release section) worked exactly as designed.
- The STEP 1.4a Perennial-Return Check correctly forced an explicit PO disposition on `BLG-FEAT-73`/`BLG-FEAT-74` at their 2nd consecutive return, rather than letting them silently re-enter scope discussion a 3rd time with no new facts — this closes out a churn pattern flagged as a risk by `2026-07-21__release-v7.7`'s own scope-exclusion note.

## Friction Log

### Friction Item 1

**Classification:** Type A — Process Integrity (prompt/schema conflict, not user error)

**What happened:** `release_planning_prompt.md` v2.42 STEP 7/STEP 9 instruct writing `.claude_current_state.json.status` as `"Validated"`/`"Published"` — neither value exists in the canonical `lifecycle_schema.json` state enum, which instead names the terminal state `Release_Planning_Complete` (the exact string Design Gate's own Lifecycle Guard checks for). Following the prompt literally would have stranded the cycle at Design Gate's next invocation (unrecognised status → self-halt to `Blocked`).

**Where in the routine:** STEP 7 (intermediate global state sync) / STEP 9 (terminal global state sync)

**Resolution applied this cycle:** Per `shared_standards.md` §10.6 conflict-resolution rule (`lifecycle_schema.json` prevails), wrote `status = "Release_Planning_Complete"` instead of the prompt's literal wording. Full detail: `run_manifest.md` §"STEP 7/9 — Global State Sync: Status-Value Conflict Resolution".

**Suggested fix:** `release_planning_prompt.md` STEP 7/STEP 9 status-value language should reference the canonical `lifecycle_schema.json` enum directly rather than this prompt's own cycle-internal `state.json` macro-state vocabulary (§12) — the two are easily conflated since both live in the same document.

**Target:** `action-now` — recommend applying at next governance prompt maintenance pass (Head of Specs Team), per CLAUDE.md §6 Governance File Edit Checklist (version bump + `OPERATIONAL_GUIDE.md` §14 + `prompt_change_log.md` append required in the same commit as the fix).

### Friction Item 2

**Classification:** Type B — Process Friction (no rule violated, pre-existing drift discovered)

**What happened:** `.claude_current_state.json.next_release` was stamped `"v7.4"` at the start of this session — 4 releases stale (v7.4 shipped 2026-07-17; the field was never updated across v7.5, v7.6, or v7.7's own release planning cycles). No engine in the observed chain (`plan release`, post-ship closure, roadmap rebalance) appears to explicitly own updating this field outside of Release Planning's own STEP 9.

**Where in the routine:** STEP 9 (terminal global state sync)

**Resolution applied this cycle:** Corrected to `"v7.8"` as part of this cycle's terminal sync.

**Suggested fix:** Confirm which engine's prompt is meant to own `next_release` maintenance (candidates: Release Planning STEP 9, or `sync gh`'s own read of it per CLAUDE.md §4) and make that ownership explicit in the owning prompt, so the field doesn't silently drift for multiple cycles again.

**Target:** Advisory only — no backlog item filed (the field's only consumer, `sync gh`'s label-creation step, wasn't invoked during the drift window, so no downstream impact occurred).

## Monitoring Carried Forward

- Design Gate required for EPIC-01, 03, 04, 05, 06 (`BLG-FE-128`, `BLG-FE-127`, `BLG-FE-125`, `BLG-FEAT-81`, `BLG-FEAT-82`) — run `run design-gate --cycle 2026-07-24__release-v7.8` before `plan sprint`. EPIC-02, 07–12 have no Design Gate dependency.
- `BLG-FEAT-73`/`BLG-FEAT-74` removed from v7.8 scope and from PO's active consideration set — `manage roadmap` should action the removal of their un-versioned Now-horizon carry-forward entry from `current_roadmap.md` §3 at its next run, since Release Planning's own write scope does not permit that edit.
- EPIC-11 (`BLG-QA-119`) pilot endpoint selection (positions/trades/dashboard candidates) needs Head of Engineering confirmation before implementation — flagged in `release_plan.md` RISK-03, not yet a blocker.

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-24__release-v7.8",
  "phase": "Release",
  "filed_utc": "2026-07-24T11:53:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
