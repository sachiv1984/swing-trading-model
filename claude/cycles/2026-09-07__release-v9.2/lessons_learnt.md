Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-07

# Lessons Learnt — Release Planning 2026-09-07__release-v9.2

## Friction Items

**Friction Item 1 — `BLG-FEAT-92`'s gate condition is not structurally discoverable.** `BLG-FEAT-92` has no formal `**Gate criteria:**` field in `claude/backlog/backlog.md` — its exclusion from scope depends entirely on a Product Owner decision recorded in a *prior* cycle's `docs/product/decisions/decisions--2026-09-03__release-v9.1.md`, which this session had to manually re-locate and re-read to avoid re-litigating (or worse, silently including) it. This is the 4th consecutive cycle (v8.9, v9.0, v9.1, v9.2) this manual reconciliation lookup has been required. The `2026-09-03__release-v9.1` run_manifest itself flagged this as a follow-up for the next `groom backlog` pass ("add a formal `Gate criteria:` field to `BLG-FEAT-92` citing this decision") — that follow-up has still not been applied across two subsequent `groom backlog` runs (2026-09-07 twice). **Recommendation:** `groom backlog`'s own field-completeness scan should be extended to check for exactly this pattern — a backlog item with a `**Depends on:**` field naming another item, where that other item is gated, but the dependent item itself carries no `Gate criteria:` field — and either auto-flag it or (with owner confirmation) write the inherited gate field directly. Filed as `BLG-GOV` follow-up recommendation (not filed as a formal backlog item within this routine's write scope — flagging for the next `groom backlog` session to file).

**Friction Item 2 — day-band effort conversion (XS/S/M/L) has no single canonical source.** This session inferred day-equivalents (XS≈0.15d, S≈0.5d, M≈2.5d, L≈3.5d) from the parenthetical ranges scattered inconsistently across individual backlog items' own `**Effort:**` fields (some state "(~0.5 day)", others just "(~2-3 days)" with no cycle-level midpoint convention documented anywhere centrally). `sprint_capacity.md` templates from prior cycles show the same derived numbers being used but never cite a single source table. **Recommendation:** add a small canonical band-to-days conversion table to `claude/roadmap/workforce_capacity.md` (or `shared_standards.md`) so future Release Planning and Sprint Planning runs don't each re-derive it from scratch.

## Prompt Change Classification

No process patches proposed this cycle — this run consumed existing prompts without finding a defect in `release_planning_prompt.md` itself.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-07__release-v9.2",
  "phase": "Release",
  "filed_utc": "2026-09-07T13:52:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
