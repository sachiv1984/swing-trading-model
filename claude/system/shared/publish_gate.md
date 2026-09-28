**Owner:** Director of Quality
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-09-28 (release_planning_prompt.md v2.57 fix — Pre-Seal Revalidation's step 1 corrected: it referenced the RESUME PRECHECK mutation-detection/invalidation-map machinery, which release_planning_prompt.md v2.47 (2026-08-06) removed as dead code; replaced with a reference to the calling engine's own Publish Gate condition re-check, matching the lightweight resume model that replaced it); prior — 2026-05-14 (initial extraction from release_planning_prompt.md v2.28 token-efficiency refactor)

---

# Publish Gate, Pre-Seal Revalidation, and Sealing

## Publish Gate (Hard Constraint)

The run may be marked Validated/Published only if ALL engine-specific gate conditions (declared by the calling engine) are true. If `deferred_execution_blockers` is non-empty:
- status MUST be `Blocked` (or remain non-Published)
- publish_eligible = false
- HALT (do not mark Published)

If Publish Gate passes:
- status = `Validated`
- publish_eligible = true

Else:
- publish_eligible = false

---

## Pre-Seal Revalidation (Hard Gate)

Before executing Publish Sealing:

1. Re-run the calling engine's own Publish Gate condition checks (§ above) against the current state — the former RESUME PRECHECK mutation-detection/invalidation-map machinery was removed (release_planning_prompt.md v2.47, 2026-08-06) in favour of this lightweight re-check.
2. If any tracked artifact or assumption changed since Publish Gate evaluation:
   - Invalidate Publish Gate.
   - Set `publish_eligible = false`.
   - Resume from the earliest invalidated step.
   - **HALT** (sealing may not proceed).
3. Sealing may only proceed if **no invalidations** occur during this check.

### Final Publish Preconditions (Hard Gate)

Before Publish Sealing:

- locks.backlog_lock.status must be "released"
- locks.roadmap_lock.status must be "released" OR "not_checked"
- locks.*.owned must be false
- locks.*.txn_state must be "committed" OR "none"

If any lock remains acquired, prepared, or blocked:
- HALT.

---

## Publish Sealing Checklist (execute in order)

1. **Verify artefacts** — `release_plan.md` and `stage4_backlog_slice.md` must exist. If either missing: HALT; status remains Validated.
2. **Seal assumptions** — Write `assumptions.timebox` + `assumptions.capacity` into `state.sealed.sealed_assumptions`. These become immutable.
3. **Record snapshot hash** — Write current git commit SHA into `state.sealed.state_snapshot_hash`.
4. **Finalize seal** — Set `sealed_utc = now (UTC)`, `drift_detected = false`, `drift_notes = []`.
5. **Final transition** — Set `status = Published`, `last_transition_utc = now`, `publish_eligible = true`. Forbidden to mark Published before step 4 completes. If sealing fails → HALT; remain Validated.

---

## State Integrity Rule

If:
- status == Published
- Sealed fields missing OR
- state_snapshot_hash mismatch

Treat as drift.

Do NOT repair.

Require amendment cycle.

---

## Completion Condition (Shared)

Run is complete only if ALL of the following are true:
- Cycle folder exists
- state.json valid and status = Published
- publish_eligible = true
- cycle_summary.md exists
- lessons_learnt.md exists
- No open escalations (open_escalations is empty)
- deferred_execution_blockers is empty

Engine-specific additional conditions are declared by the calling engine.
