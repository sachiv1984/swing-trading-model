**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Class:** Design Artefact (Class 4)
**Status:** Closed — retroactive (see §1)
**Last Updated:** 2026-08-13
**Cycle:** 2026-08-12__release-v8.7 — ST-12 (EPIC-04, `BLG-BE-30`)

---

# SI-04 Schema Requirements Pre-Design

## 1. Finding: this story's premise is stale — SI-04 already shipped

`BLG-BE-30` (filed 2026-06-03, un-gated 2026-08-11) asks for "SI-04 schema requirements pre-design... to avoid same-sprint data model debt," framed as pre-work "ahead of SI-04 sprint entry." **SI-04 (Strategy Version Performance Comparison) shipped in full over four releases ago** — `2026-07-21__release-v7.7`, EPIC-01, ST-01, `BLG-FEAT-75` (`claude/roadmap/current_roadmap.md` v7.7 entry). The endpoint (`GET /analytics/strategy-version-comparison`) is live in `backend/routers/analytics.py`, backed by `backend/strategy_version_registry.py`.

This document is therefore not forward-looking pre-design — it is a **retroactive confirmation** that the exact schema question `BLG-BE-30` raised was already answered, correctly, at implementation time. Produced now (per this story's own AC: "SI-04 data model requirements documented ahead of SI-04 sprint entry") to formally close the loop `BLG-BE-30` left open, rather than silently skip a story whose premise no longer holds or manufacture a duplicate pre-design exercise for already-shipped work.

## 2. `BLG-BE-30`'s original question, and its answer

`BLG-BE-30`'s Problem statement: *"SI-04 strategy version comparison requires linking trade_plans to historical strategy_rules.md versions. Whether this is a new strategy_versions table, a foreign key, or a snapshot field must be decided before SI-04 sprint to avoid same-sprint data model debt."*

Its Scope asked for three options to be evaluated: (a) new table (`strategy_versions`), (b) FK on `trade_plans` (`strategy_version`), (c) snapshot field (`strategy_snapshot` JSON).

**Answer, as actually implemented (`strategy_version_comparison_contract.md` v0.2.0, Implementation Notes 1–2):** **none of the three.** Trades are attributed to a strategy version by `entry_date` falling within that version's active date window — `[effective_date, next_version_effective_date)` — derived from `claude/strategy/strategy_rules.md`'s own Change Log table, hardcoded into `backend/strategy_version_registry.py`. No `trade_history`/`trade_plans` schema change of any kind. `docs/governance/si04_scope_definition.md` (Product Owner-approved, 2026-05-28 — filed *before* `BLG-BE-30`, but not cross-referenced by it) had already decided this: *"There is no formal strategy versioning schema, no tagged strategy objects, and no version migration required... No new database tables required for Phase 1."* `BLG-BE-30`'s filing (2026-06-03) post-dates that sign-off by six days without picking it up — a cross-referencing gap, not a substantive disagreement; both documents ultimately agree.

## 3. Data model requirements actually exercised by the shipped endpoint (confirmed against source)

For completeness, since this document's nominal purpose is a schema audit — the columns and joins the live endpoint actually reads, confirmed against `backend/routers/analytics.py` and `docs/specs/data_model.md`'s `trade_history`/`positions` tables:

- `trade_history.entry_date`, `exit_date`, `pnl`, `pnl_pct` — used for `trade_count`/`win_rate` per version window. All present, all `NOT NULL` or already-populated columns; no gap.
- `avg_R` (R-multiple) requires the stop price at entry, which `trade_history` does **not** store directly — the same gap `tests/test_tax_year_boundary_completeness.py`'s sibling stories and `get_trade_history_with_stops()` (`database.py`) already work around via `LEFT JOIN positions p ON th.position_id = p.id` reading `p.initial_stop`. The shipped SI-04 endpoint uses this identical, already-established join pattern (`metrics_definitions.md` v1.7.0 canonical R-multiple formula) rather than inventing a new one — no new column needed, existing pattern reused.
- `compliance_rate` sources from the existing Arc 5 compliance composite (`GET /analytics/arc5-compliance`'s underlying metrics), generalised to an arbitrary date range — no new table; reuses existing compliance data paths (`backend/routers/analytics.py::_compute_arc5_composite_for_range`).
- Strategy version *labels/effective-dates* live in `backend/strategy_version_registry.py`, sourced from `strategy_rules.md`'s Change Log — a code-level registry, not a database table, by deliberate design (Implementation Note 2: "Living-reference maintenance obligation: update this file in the same commit as any new Change Log row").

**No indexing gap found for this query shape specifically:** the endpoint filters by `entry_date`/`exit_date` range plus `position_id` join, both already covered by existing indexes (`idx_trade_history_position_id`) or small enough table scans at current single-portfolio trade volumes not to warrant a new composite index. Advisory only, not a finding requiring action: if per-portfolio trade volume grows into the tens of thousands, a composite `(portfolio_id, exit_date)` index would be worth revisiting — no such index exists today, and none of `trade_history`'s current query patterns (this one included) show evidence of needing it yet.

## 4. Recommendation

**No schema change — confirmed, retroactively, as the correct call already made.** `BLG-BE-30` should be marked resolved by the Product Owner / next `groom backlog` pass, referencing this document and `strategy_version_comparison_contract.md` v0.2.0 as the closing evidence. (Out of this story's write scope to edit `BLG-BE-30`'s own backlog entry directly — `execution_prompt.md` §7 permits only new-item addition to `backlog.md`, not editing existing items' status.)

## 5. Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Data Model & Domain Schema Owner role — §5.3) — 2026-08-13. Confirms the shipped implementation's schema decision (no new tables/columns) is correct and complete against `BLG-BE-30`'s original three-option question; no residual schema gap found.
- Signed off by: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3) — 2026-08-13. Confirms the R-multiple join pattern and compliance-rate sourcing reuse existing, already-reviewed code paths rather than introducing new ones.
