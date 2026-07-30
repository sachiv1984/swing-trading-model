Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-30
Cycle: 2026-07-30__release-v8.0

# Lessons Learnt — Release Planning — v8.0

## What worked well

- The prior cycle's Carry-Forward item (`BLG-OPS-111` endpoint-list drift) was correctly identified as out of Release Planning's write scope and routed to Post-Ship Closure without attempted action here — consistent with the engine boundary discipline established at v7.10.
- Grouping 19 stories into 6 thematically-coherent EPICs (by default, in the absence of an explicit user grouping instruction) reproduced the same clean fit pattern seen at v7.10 — no forced groupings were needed.

## Friction Log

### Friction Item 1

**Classification:** Type C — Self-caught verification error (scan-methodology gap, not a prompt defect)

**Recurrence:** No prior instance found in this cycle's checked history.

**What happened:** The initial ungated-pool scan (used to identify scope candidates) checked backlog items only for a `**Gate criteria:**` or `**Gate:**` field to classify an item as gated. `BLG-OPS-48` (ANTHROPIC_API_KEY 6-month scope audit) uses neither field name — it instead carries a `**Gate date:** 2026-11-01` field plus a `Provisional-Target: ~v4.9 (date-gated: no earlier than 2026-11-01)` annotation. The scan's field-name pattern missed both, and the item was initially included in the 20-item scope selection. It was caught before any backlog.md write occurred: the STEP 4 `Provisional-Target` TBD→v8.0 substitution script reported "no TBD found" for this item (because its field already read a date-gated value, not `TBD`), which surfaced the mismatch. Removed from scope before any write; final selection is 19 items.

**Where in the routine:** STEP 2 scope extraction / STEP 4 backlog write preparation (self-verification during the Provisional-Target update, not a named sub-check failure).

**Root cause:** `release_planning_prompt.md` does not define a canonical field-name list for the "ungated pool" scan — it is left to session judgment (same root cause class noted at v7.10's own Friction Item 1, "no canonical, reusable check string for this advisory"). This session's ad hoc scan pattern-matched `**Gate criteria:**`/`**Gate:**` but not the equally valid `**Gate date:**` variant already in use elsewhere in the backlog.

**Blast radius analysis:**
- What would have propagated: `BLG-OPS-48` would have been committed to `stage4_backlog_slice.md` and `backlog.md`'s Release Slice section as firm scope, then surfaced as a blocked/premature story at Sprint Planning or Execution time (its own gate does not clear until 2026-11-01) — a returned-to-backlog outcome, the exact pattern `release_planning_prompt.md` §1.4b was written to prevent for within-sprint gates (this is a beyond-sprint gate, an even clearer miss).
- When it would have surfaced: at Sprint Planning's own gate-condition check, or at Sprint Execution if that check were also missed.
- Recovery cost if uncaught this session: low-medium — a single story would have needed manual removal at Sprint Planning, plus a capacity re-check and re-numbering of subsequent S2/ST IDs, essentially the same rework this session did anyway, just one stage later and after a backlog.md write (harder to unwind cleanly given the idempotency-marker/lock discipline around that file).

**Process patch:** None filed this cycle — single instance, and the underlying root cause (no canonical gate-field list) was already named, not newly discovered, at v7.10's Friction Item 1 without a patch being filed there either. Recorded as a Carry-Forward item below: if a second instance of a gate expressed via a field name other than `**Gate criteria:**`/`**Gate:**` is found at a future release planning session, file a `BLG-GOV-*` item to add an explicit canonical gate-field list (`Gate criteria`, `Gate`, `Gate date`, and any others found) to `release_planning_prompt.md`'s scope-selection guidance.

## Recurrence Escalations

None. This is the first observed instance of this specific scan-methodology gap.

## Process improvements actioned this run

None (the friction item above was assessed as not yet warranting a prompt patch from a single instance, consistent with the `release_planning_prompt.md` v7.10 precedent for single-instance scan-methodology gaps).

## Outstanding deferred patches

None.

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The ungated-pool scope-selection scan used at both v7.10 and v8.0 pattern-matches only `**Gate criteria:**`/`**Gate:**` field names; `BLG-OPS-48` demonstrated a real gate expressed as `**Gate date:**` slipping through undetected at v8.0. | If a second such miss is found at a future release planning session, file a `BLG-GOV-*` item extending `release_planning_prompt.md`'s scope-selection guidance with an explicit canonical gate-field list, rather than leaving the scan pattern to ad hoc session judgment a third time. | Release Planning |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-30__release-v8.0",
  "phase": "Release",
  "filed_utc": "2026-07-30T14:55:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
