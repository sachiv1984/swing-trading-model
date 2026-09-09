Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-09

# Lessons Learnt — Release Planning 2026-09-09__release-v9.3

## Friction Items

**Friction Item 1 — no canonical method for selecting a subset when the ungated ready pool exceeds capacity.** This is the first cycle since `v8.5` where the ungated/ready pool (61 items, ~41.0 estimated days) exceeded the sprint capacity band by a wide margin (~13 days over) rather than being fully consumable or falling short of it. `release_planning_prompt.md` §1.4a (Perennial-Return Check) governs *gate-conditional* items returning cycle-over-cycle, but has no equivalent guidance for selecting *which* ungated items to include when there are simply more ready items than capacity allows. This session adopted a round-robin-across-category, oldest-first selection method (documented in `run_manifest.md`) to avoid exhausting one debt category (e.g. Governance, which has by far the largest ready-item count) at the expense of others. This is a reasonable ad hoc choice but is not backed by any documented rule — a future cycle facing the same situation could legitimately choose a different method (e.g. pure age-sort ignoring category, or priority-within-P3 if such sub-tiering existed) and get a materially different scope with no way to tell which approach is "correct" per the prompt. **Recommendation:** add a short subsection to `release_planning_prompt.md` §1.4 (or a new §1.4c) specifying a canonical over-capacity selection method — category-balanced, oldest-first is a reasonable default to codify, given it is what this session and the general debt-clearance pattern established since v8.5 already approximate informally.

**Friction Item 2 — `v9.2`'s own friction items are both confirmed resolved and directly beneficial this cycle.** `2026-09-07__release-v9.2`'s Friction Item 1 (`BLG-FEAT-92` gate-inheritance discoverability) was resolved same-day via the post-ship closure's new Gate-Inheritance Field-Completeness Scan (`backlog_management_prompt.md` v1.16→v1.17); this session's -1.2/scope-construction check required no manual decisions-document lookup as a result — confirmed working as intended. Friction Item 2 (day-band effort conversion table) was resolved via the new `workforce_capacity.md` Canonical Effort Band → Days Conversion Table; this session read directly from that table rather than re-deriving midpoints from scattered parentheticals, the first cycle to do so. Both fixes are functioning exactly as designed — no further action needed, noted here per the Carry-Forward mechanism's own closed-loop verification pattern.

## Prompt Change Classification

No process patches proposed this cycle beyond the deferred recommendation in Friction Item 1 above (deferred — the exact selection-method wording deserves Head of Specs Team review rather than being unilaterally codified by this single session's ad hoc choice).

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-09__release-v9.3",
  "phase": "Release",
  "filed_utc": "2026-09-09T02:15:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
