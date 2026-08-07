**Owner:** Data Model & Domain Schema Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-08-07
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Schema Versioning — `trade_plan` and `position` Tables

## Purpose

`docs/specs/data_model.md` is the canonical schema of record — its per-table `CREATE TABLE` blocks and numbered `### Migration from vX to vY` / `## DS-NN` sections are the source of truth for every column. This document is a **focused index** over that history, scoped to the two tables with the deepest cumulative migration history in the system (`trade_plans` and `positions`): a single place to see, at a glance, when each field was added, whether it has ever been deprecated, and what the field-level deprecation policy is for these two tables going forward. It does not restate `CREATE TABLE`/`ALTER TABLE` SQL — that lives in `data_model.md`, which this document links to by migration ID/version throughout.

Source of truth for the base schema and every change below: `docs/specs/data_model.md` (Document Version 2.21 as of this doc's writing).

---

## 1. `trade_plans` — Migration History

| Migration | Version | Date | Change |
|-----------|---------|------|--------|
| DS-04 | v2.5 | 2026-04-30 | Table created. `id`, `portfolio_id`, `position_id`, `ticker`, `market`, `created_at`, `updated_at`, `setup_thesis`, `entry_rationale`, `regime_context_at_entry`, `r_target`, `early_exit_conditions`, `confirmation_criteria`, `checklist_completed`, `checklist_items`, `status` (`draft`/`active`/`closed`). |
| DS-06 | v2.7 | 2026-05-10 | Added `abandonment_reason` (VARCHAR, nullable). `status` CHECK extended to include `abandoned`. Enforced non-null at the API layer when `status = 'abandoned'`, not at the DB layer. |
| v2.11→v2.12 | v2.12 | 2026-07-13 | Added `last_reviewed_at`-equivalent review-cadence support (see `data_model.md` for the exact column; shared migration slot with the `positions` v2.11→v2.12 entry below — both tables changed in the same migration). |
| DS-09 | v2.10 | 2026-07-03 | Added `thesis_feedback` (nullable). Persists the Claude thesis-generation feedback control; feeds `metrics_definitions.md#Thesis Adoption Rate`. |
| v2.13→v2.14 | v2.14 | 2026-07-17 | No `trade_plans` column change — entry included here because it renumbers around DS-09/DS-10 in the shared migration sequence; `trade_plans` itself unaffected. |
| DS-10 | v2.11 | 2026-07-03 | **Documentation backfill, no live migration.** `planned_stop_price` had already shipped to production on 2026-05-15 (v3.5) but was undocumented in the canonical file until this entry. |
| DS-11 | v2.20 | 2026-07-30 | Added `strategy_version_at_entry` (VARCHAR(10), nullable). Forward-only — rows created before this migration remain `NULL`; no backfill attempted. Populated at `POST /trade-plans` creation via `get_current_strategy_version()`. |

**Current canonical field count:** 17 (per `data_model.md` DS-04 Field Reference table, plus `abandonment_reason`, `thesis_feedback`, `strategy_version_at_entry` — cross-check `data_model.md` directly before relying on a count here, as this table is a summary, not the source of truth).

## 2. `positions` — Migration History

| Migration | Version | Date | Change |
|-----------|---------|------|--------|
| Base schema | v1.0 | (pre-dates numbered migrations) | Core position fields: `id`, `portfolio_id`, `ticker`, `market`, `entry_date`, `entry_price`, `shares`, `total_cost`, `fees_paid`, `initial_stop`, `current_stop`, `current_price`, `atr`, `holding_days`, `pnl`, `pnl_pct`, `status`, `exit_date`, `exit_price`, `exit_reason`, `entry_note`, `exit_note`, `tags`, `created_at`, `updated_at`. |
| v1.1→v1.2 through v1.6→v1.7 | v1.2–v1.7 | (see `data_model.md`) | Early hardening migrations — `fee_type`, `fill_price`/`fill_currency`, `fees_paid` made `NOT NULL`, `default_risk_percent` added to `settings` (not `positions` itself, listed for completeness of the v1.x sequence). |
| v1.8→v1.9 | v1.9 | — | See `data_model.md` for exact column; not `trade_plans`/`positions`-specific. |
| v1.9→v2.0 | v2.0 | — | Added `user_fill_price` (nullable) — captures actual broker fill at entry for slippage computation. Companion `trade_history.fill_price` added in the same migration. |
| DS-05 | v2.6 | 2026-05-10 | Added `position_state` (VARCHAR(20), nullable), `state_entered_at` (TIMESTAMP, nullable), `state_history` (JSONB, `NOT NULL DEFAULT '[]'`) — Arc 3 lifecycle state machine fields. Computed by `PositionLifecycleService` only; never set by direct DB writes from other services. |
| v2.11→v2.12 | v2.12 | 2026-07-13 | ST-15 (BLG-FEAT-68): added `last_reviewed_at` (ISO timestamp, nullable) — position review cadence nudge, set by `PATCH /positions/{position_id}/mark-reviewed`. |
| v2.16→v2.17 | v2.17 | 2026-07-27 (v7.9) | ST-06 (BLG-BE-73): audit-trail support for manual position overrides (note edit, tag edit, mark-reviewed) — see `data_model.md` for the exact audit-log column/table shape. **Note (ST-13, EPIC-03, v8.4):** this pattern is the one `ST-13` extends to trade-plan mutations post-entry — see `data_model.md`'s live entry for that extension once merged. |
| DS-11 | v2.20 | 2026-07-30 | Added `strategy_version_at_entry` (VARCHAR(10), nullable) — same shape and forward-only semantics as the `trade_plans` addition above. Populated at position creation via `add_position()`. |

**Note on `sector`/`industry`:** DS-03 (v2.4) clarifies these are **virtual fields** returned by `GET /positions` — derived on-request from `yfinance.Ticker.info`, never stored as columns on `positions`. Not part of this table's stored-column migration history for that reason, but included here because `docs/specs/api_contracts/position_endpoints.md` (ST-04, this cycle) documents them as response fields and a reader of this document may otherwise expect a corresponding migration entry.

---

## 3. Field Deprecation Policy — `trade_plans` / `positions`

No column has been formally deprecated on either table as of this document's writing (2026-08-07). If a future migration deprecates a column on `trade_plans` or `positions`:

1. Record it in `data_model.md`'s `## Deprecated Tables` section pattern (see that section's `tickers` → `ticker_universe` precedent) — even though that section is currently scoped to whole-table deprecation, the same disclosure standard (deprecation date, migration/story reference, superseding field or table if any, and "do not add new reads/writes" guidance) applies at column granularity.
2. Add a row to the relevant table above in this document, in the same format as an addition row, with `Change` reading `Deprecated <column> — superseded by <X> / removed with no replacement, reason: <Y>`.
3. Do not physically drop the column in the same migration that deprecates it, unless a dedicated backfill/verification pass has confirmed zero live reads — follow `data_model.md`'s existing down-migration/reversibility convention for the eventual `DROP COLUMN`.

## 4. Maintenance

This document must be updated in the same PR as any future migration touching `trade_plans` or `positions`, alongside the mandatory `data_model.md` update — add one row to the relevant table above (§1 or §2). This is an index, not a substitute for `data_model.md`; if the two ever disagree, `data_model.md` is authoritative and this document should be corrected to match.

**Sign-off:**
- Data Model & Domain Schema Owner: Accepted — 2026-08-07 (agent-mediated; cross-checked against `data_model.md`'s actual migration sections for both tables; no live schema change made by this story)

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-08-07 | ST-09 (BLG-SPEC-97, EPIC-02, v8.4): Initial version. Indexes existing `trade_plans`/`positions` migration history from `data_model.md`; establishes the column-level deprecation policy for both tables going forward. |
