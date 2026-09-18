**Owner:** Data Model & Domain Schema Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-18
**Story:** ST-24 (BLG-SPEC-57, EPIC-04, v9.5 sprint execution)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Arc 4 Data Model Pre-Definition — PO-02, PO-03, PO-04

> **This document is not a schema commitment. No migration SQL is included by design (per BLG-SPEC-57's own scope) and no table below has been created.** It is a pre-design reference for whoever picks up PO-02, PO-03, or PO-04 sprint planning — mirroring `docs/product/arc4_data_requirements.md`'s role for capture-point requirements (PO-01) and `docs/qa/arc4_e2e_test_strategy_po02_03_04.md`'s role for E2E test approach, but for schema. Table/column names below are proposals for design-time planning; the feature's own sprint planning and API-contract-authoring step may revise them, at which point this document should be updated to match reality or superseded by a real migration entry in `docs/specs/data_model.md`.

---

## 1. Purpose

`BLG-SPEC-57`: define the data model additions Arc 4's remaining post-trade-intelligence features (PO-02 Journal Pattern Recognition, PO-03 Behavioural Error Taxonomy, PO-04 Reflection ↔ Outcome Correlation) will plausibly require, ahead of their eventual sprint planning — while the Arc 3/PO-01 architecture (`plan_vs_reality_service.py`, `trade_reflections`, `trade_plans.regime_context_at_entry`) is still in working memory.

This document has two parts: (§2) closing the still-outstanding capture-point gaps `arc4_data_requirements.md` already identified but did not fully resolve, and (§3) net-new storage for each feature's own AI-derived output.

---

## 2. Outstanding Capture-Point Fields (from `arc4_data_requirements.md` §3.3–3.5)

`arc4_data_requirements.md` (v1.0, 2026-05-15) identified 5 fields as required-but-not-yet-captured for PO-02+. Re-checked against the live codebase this session (`grep` across `backend/` and `docs/specs/data_model.md`): only `deviation_note` has since been implemented (as a key in `trade_history.plan_vs_reality` JSONB, per that document's own §5.4 decision — confirmed live at `docs/specs/api_contracts/trade_endpoints.md` line 309/337). The other 4 remain outstanding:

| Field | Proposed home | Type | Rationale |
|-------|---------------|------|-----------|
| `confidence_at_entry` | `trade_plans` | `SMALLINT` (1–5), nullable | `arc4_data_requirements.md` §5.2 already decided the 1–5 optional scale and "at position-open time" capture point. `trade_plans` already holds the sibling entry-time field `regime_context_at_entry`, so this is the same table, same lifecycle stage — no new table needed for this field alone. |
| `regime_at_open` | `trade_history` | `VARCHAR(20)`, nullable | §3.3's own recommendation: denormalise from `trade_plans.regime_context_at_entry` onto `trade_history` at close time, via the existing PO-01 close-time write path (`plan_vs_reality_service.py`) — not a new service, an added field on an existing write. |
| `thesis_confirmed` | `trade_reflections` | `BOOLEAN`, nullable | Post-trade user annotation (§3.5) — same lifecycle stage and same "did the trader's own account of the trade hold up" register as `trade_reflections`' existing `discipline_assessment`/`key_takeaway` fields. Nullable, no default — absence means "not yet annotated", not "false". |
| `exit_quality` | `trade_reflections` | `VARCHAR(20)`, nullable, `CHECK (exit_quality IN ('too_early','as_planned','stopped_out','target_hit'))` | Same table as `thesis_confirmed` for the same reason; enum values taken directly from §3.5's own proposed label set. |
| `screener_score_at_entry` | *(no schema proposal — see below)* | — | §5.3 explicitly deferred this: "not currently retainable without schema change" because the screener cache is overwritten, so there is no historical value to backfill or denormalise from at write time. Resolving this needs a change to the screener run/cache lifecycle itself (retaining a per-signal historical score), which is out of this pre-definition's scope — it is a screener-service design question, not a data-model placement question. Flagged here so PO-02/03 sprint planning does not re-discover the gap from scratch. |

None of these four are net-new *concepts* — they are narrow, nullable additions to tables that already exist and already hold sibling data at the same lifecycle stage. No new table is proposed for §2.

---

## 3. Net-New Storage for AI-Derived Output

### 3.1 PO-02 — Journal Pattern Recognition

**Proposed table: `journal_pattern_analyses`**

One row per analysis run (portfolio-scoped, not per-trade — PO-02 is a cross-entry pattern search, matching the E2E strategy doc's proposed `GET /journal/pattern-analysis` shape, §4.1 of `arc4_e2e_test_strategy_po02_03_04.md`).

```sql
-- PRE-DEFINITION ONLY -- not a committed migration
CREATE TABLE journal_pattern_analyses (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id        UUID NOT NULL REFERENCES portfolios(id),
    patterns            JSONB NOT NULL,
    journal_entry_count INTEGER NOT NULL,
    model_version       TEXT,
    prompt_version      TEXT,
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_journal_pattern_analyses_portfolio ON journal_pattern_analyses(portfolio_id, generated_at DESC);
```

| Field | Rationale |
|-------|-----------|
| `patterns` JSONB | Array-of-theme shape, matching the E2E mock fixture (`{theme, trade_count, sentiment}[]`) — kept schemaless at the DB layer since the theme taxonomy itself is expected to evolve as the feature is designed; do not lock it into named columns prematurely. |
| `journal_entry_count` | The AI journal entry count the analysis was run over — same field PO-02's own gate condition reads (`get_ai_journal_review_status()`), recorded per-run for auditability of what the pattern set was actually based on. |
| `model_version` / `prompt_version` | Same provenance pattern already established for `trade_plans.thesis_model_version`/`thesis_prompt_version` (DS at `data_model.md` §Migration v2.22→v2.23) — every AI-derived record in this codebase carries its own model/prompt version for audit. |
| No `expires_at`/retention field | Unlike `ai_output_boundary_samples` (a compliance sampling table with an explicit 90-day purge), this is product data the user is expected to keep seeing — no retention policy proposed here; PO-02's own sprint planning should decide if one is needed. |

**Read path:** `ai_journal_entries` is externally-provisioned and read-only to this codebase (`data_model.md` "AI Journal Entries Table" section) — `journal_pattern_analyses` does not join it directly; the analysis-generation service reads from `ai_journal_entries` at run time and writes its *output* here, keeping the external table's read-only boundary intact.

### 3.2 PO-03 — Behavioural Error Taxonomy

**Proposed table: `trade_error_classifications`**

One row per classified trade (not per-run) — matches the E2E strategy doc's proposed per-trade `GET /trades/{id}/error-classification` shape (§4.2).

```sql
-- PRE-DEFINITION ONLY -- not a committed migration
CREATE TABLE trade_error_classifications (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trade_id       UUID NOT NULL REFERENCES trade_history(id) ON DELETE CASCADE,
    error_types    TEXT[] NOT NULL DEFAULT '{}',
    confidence     DECIMAL(3, 2),
    source_inputs  TEXT[] NOT NULL DEFAULT '{}',
    model_version  TEXT,
    prompt_version TEXT,
    classified_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_trade_error_classifications_trade UNIQUE (trade_id)
);

CREATE INDEX idx_trade_error_classifications_trade ON trade_error_classifications(trade_id);
```

| Field | Rationale |
|-------|-----------|
| `error_types` TEXT[] | Array, not a single enum column — the roadmap's own PO-03 description ("entry too early, held too long, sized incorrectly, ignored regime, etc.") implies a trade can plausibly carry more than one classified error simultaneously. |
| `confidence` | Matches the E2E mock's `confidence: 0.8` shape — a per-classification AI confidence score, `DECIMAL(3,2)` to hold 0.00–1.00. |
| `source_inputs` TEXT[] | Records which underlying data the classification was derived from (e.g. `{'plan_vs_reality', 'trade_reflection'}`) — per the E2E doc's own §4.2 flagged open question of whether PO-03 requires both a trade plan *and* a journal entry, or can classify from `plan_vs_reality` alone. Recording the actual inputs used per-row means that open question can be answered empirically once real data exists, rather than needing a schema change later to start tracking it. |
| `UNIQUE (trade_id)` | One classification per trade, upsert model — same 1:1 pattern already used by `trade_reflections` (`UNIQUE (trade_id)`), re-classifiable if the trade's linked plan/reflection data changes. |
| `ON DELETE CASCADE` | Same lifecycle-coupling rationale as `trade_reflections.trade_id`. |

### 3.3 PO-04 — Reflection ↔ Outcome Correlation

**No new table proposed.** Recommend an on-demand aggregate computation (matching the `GET /strategy/benchmark` / `GET /analytics/strategy-version-comparison` pattern already used elsewhere in this codebase for portfolio-wide statistical views), not a persisted-per-trade or persisted-per-run table, for two reasons:

1. The correlation is inherently a portfolio-wide statistic recomputed as new trades close (does a trader's journal depth correlate with trade quality *this month* vs *all-time* is a query-parameter concern, not a stored-row concern) — persisting it invites the same kind of staleness problem `screener_score_at_entry` (§2 above) already illustrates for a different field.
2. Its inputs (`trade_reflections` completeness/depth, `trade_history.pnl`/`r_multiple`, `trade_plans.checklist_items` completion) already exist in full — there is nothing to capture that isn't already stored elsewhere; only the aggregation is new, and that belongs in a service layer, not a table.

If PO-04's actual design later needs to *cache* an expensive correlation computation (analogous to how `screener` results are cached today), that is a caching decision for that feature's own sprint planning, not a data-modelling one — flagged here, not resolved.

**Gate honesty note (carried from `arc4_e2e_test_strategy_po02_03_04.md` §4.3):** whatever service computes this must surface an explicit `insufficient_data` state below the 50-trades-with-plans gate, matching the existing `has_enough_data`/`insufficient_data` convention already used by `GET /analytics/strategy-version-comparison` and `analytics.md`'s own empty-state handling (`Empty & Null Safety` section) — not a misleading low-sample-size figure.

---

## 4. Summary Table

| Feature | New table? | Schema change | Capture-point prerequisites (§2) |
|---------|-----------|----------------|------------------------------------|
| PO-02 Journal Pattern Recognition | Yes — `journal_pattern_analyses` | New table only, no existing table touched | None — reads `ai_journal_entries` (already live) |
| PO-03 Behavioural Error Taxonomy | Yes — `trade_error_classifications` | New table only, no existing table touched | `deviation_note` (already live); benefits from, but per the E2E doc's own flagged open question may not strictly require, PO-02 output |
| PO-04 Reflection ↔ Outcome Correlation | No | None — service-layer aggregation over existing tables | None beyond what already exists |

---

## 5. Cross-Reference

- `BLG-SPEC-56` (Arc 4 API contract pre-authoring, ST-23, this same cycle) should reference this document's proposed table/field shapes when stubbing `docs/specs/api_contracts/` entries for PO-02/03/04, per its own AC.
- `docs/qa/arc4_e2e_test_strategy_po02_03_04.md` (ST-15, BLG-QA-59, v9.5) — this document's proposed field shapes (`patterns`, `error_types`, `confidence`) were chosen to match that document's already-published mock fixture shapes rather than diverge from them.
- `docs/product/arc4_data_requirements.md` (ST-04, v3.5) — §2 above closes its still-outstanding §3.3–3.5 gaps.

---

## 6. Sign-Off

Per `BLG-SPEC-57`'s own AC ("Reviewed by Head of Specs Team and Infrastructure & Operations Owner"):

| Role | Status | Notes |
|------|--------|-------|
| Head of Specs Team | ✅ Accepted | Agent-mediated (§5.3) — see sign-off record for ST-24 in this cycle's `execution_state.json`. |
| Infrastructure & Operations Owner | ✅ Accepted | Agent-mediated (§5.3) — no migration SQL in this document by design (BLG-SPEC-57 scope: "No migration SQL; schema design only"), so no live index/performance review is applicable yet; flagged for that role's real review once an actual migration is authored. |
| Data Model & Domain Schema Owner | (Authoring role) | This document's own owner (per its header) — not a substitute for the two AC-named reviewers above. |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-18 | Initial pre-definition — ST-24 (EPIC-04, v9.5, BLG-SPEC-57). Closes 4 of 5 outstanding `arc4_data_requirements.md` capture-point gaps (schema placement only); proposes 2 new tables (`journal_pattern_analyses`, `trade_error_classifications`) for PO-02/PO-03; recommends no new table for PO-04 (service-layer aggregation over existing data). |
