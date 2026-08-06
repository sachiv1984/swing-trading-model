**Owner:** Data Model & Domain Schema Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-06
**Cycle:** 2026-08-05__release-v8.3 (ST-05 — BLG-BE-37)

---

# Database Index Audit — Arc 4 Cross-Table Query Patterns

## Purpose

`BLG-BE-37` requires an index audit covering Arc 4 query patterns across `trade_plans`, `red_flag_events`, `arc5_compliance_scores`, and `ai_journal_summaries`. This audit confirms current index coverage for each table's actual read query shapes and files any gaps as separate backlog items rather than fixing them inline, per the story's acceptance criteria.

## Table Name Reconciliation

Two of the four names in the backlog item's title do not exist verbatim in the schema. Resolved by inspection of `backend/database.py` and `backend/services/reports_service.py::get_arc5_compliance_summary()`:

| Backlog item name | Actual table | Basis |
|---|---|---|
| `trade_plans` | `trade_plans` | Exact match — no reconciliation needed |
| `red_flag_events` | `red_flag_events` | Exact match — no reconciliation needed |
| `arc5_compliance_scores` | `pre_entry_validation_log` | No table named `arc5_compliance_scores` exists anywhere in the codebase (`grep -ri` returns zero hits). `pre_entry_validation_log`'s own docstring names it "for ST-01 arc5-compliance metrics," and `reports_service.py::get_arc5_compliance_summary()` — the function literally named for Arc 5 compliance — reads exclusively from `pre_entry_validation_log` and `red_flag_events`. This is the closest real table to the item's intent. |
| `ai_journal_summaries` | `ai_journal_entries` | No table named `ai_journal_summaries` exists. `ai_journal_entries` is the only AI-journal-related table referenced in `database.py` (`get_ai_journal_review_status()`), gated behind an `information_schema.tables` existence check before every query — see Finding 4 below. |

## Method

1. Enumerated every `CREATE TABLE`/`CREATE INDEX` statement for each resolved table in `backend/database.py` and the canonical schema in `docs/specs/data_model.md`.
2. Enumerated every read query (`SELECT`/`JOIN`/`WHERE`) against each table across `backend/database.py`, `backend/routers/analytics.py`, `backend/routers/red_flag_journal.py`, `backend/services/reports_service.py`, and `backend/services/si05_digest_service.py` (`grep -n` for each table name, then read each call site's `WHERE`/`JOIN`/`GROUP BY` clause).
3. Compared each query's filter/join columns against the indexes actually created by the relevant idempotent `ensure_*` function (not just what `data_model.md` documents — `docs/ops/deprecated_table_read_audit_2026-07-29.md` already found `data_model.md` and the idempotent create-path can drift, e.g. undocumented tables).

## Findings

**1. `trade_plans` — missing functional index on `ticker` (gap, filed as `BLG-BE-82`).**
`ensure_trade_plans_table()` creates `idx_trade_plans_portfolio`, `idx_trade_plans_position`, `idx_trade_plans_status` — no ticker index. `get_trade_plans(ticker=...)` filters `WHERE UPPER(ticker)=%s`. `data_model.md`'s canonical schema separately documents a plain `idx_trade_plans_ticker ON trade_plans(ticker)`, which (a) is not present in the idempotent create path used by the live app, and (b) is a non-functional index that would not be used by an `UPPER(ticker)` predicate regardless. The sibling table `red_flag_events` already gets this right (`idx_rfe_ticker ON red_flag_events (UPPER(ticker))`) — `trade_plans` should match. All other `trade_plans` read paths (`portfolio_id`, `position_id`, `status`, `signal_id` via `idx_trade_plans_signal`) are covered.

**2. `red_flag_events` — fully covered, no gap.**
Read query shapes found: filter by `event_type`, `UPPER(ticker)`, `created_at` range, `severity`. Indexes present: `idx_rfe_event_type`, `idx_rfe_ticker` (functional, `UPPER(ticker)`), `idx_rfe_created_at DESC`. `severity` has no dedicated index but is always combined with an `event_type` or `created_at` predicate in every call site found, and is a 3-value low-cardinality column (`info`/`warning`/`critical`) — a standalone index would not meaningfully improve selectivity. No action needed. `position_id` is write-only in every call site found (populated on insert, never filtered on read) — no read-path index needed for it.

**3. `pre_entry_validation_log` (Arc 5 compliance proxy) — fully covered, no gap.**
Read query shapes found: `GROUP BY rule_type` with `status = 'fail'` filter, and `validated_at` range filter (both used independently and combined) across `reports_service.py`, `routers/analytics.py`, and `si05_digest_service.py`. Indexes present: `idx_pevl_rule_type`, `idx_pevl_validated_at DESC`. No query filters by `ticker` or `market` — both present as columns but unindexed and unneeded. No action needed.

**4. `ai_journal_entries` — out of audit scope, not a codebase-managed table.**
Every read (`database.py::get_ai_journal_review_status()`) is preceded by an `information_schema.tables` existence check before querying — this codebase does not create, migrate, or own this table's schema (no `CREATE TABLE ai_journal_entries` anywhere in `backend/`). It is provisioned externally. Index coverage for an externally-provisioned table cannot be audited or remediated from this repository. This is consistent with `docs/ops/deprecated_table_read_audit_2026-07-29.md`'s prior finding that `ai_journal_entries` is read but undocumented in `data_model.md` (tracked separately as `BLG-SPEC-109`) — no new item filed here for the same underlying gap.

**5. Cross-table join (`trade_history` × `trade_plans` on `position_id`) — fully covered, no gap.**
Found at `routers/analytics.py` (trade_plan_adherence_rate, two call sites) and `database.py::get_trade_plan_tags_pnl()`: `JOIN trade_plans tp ON tp.position_id = th.position_id`. `trade_plans.position_id` has `idx_trade_plans_position`; `trade_history.position_id` has `idx_trade_history_position_id` per `data_model.md`'s canonical schema (this table predates the `ensure_*` idempotent-creation pattern and was provisioned directly — noted as a methodology observation, not a gap, since the index is confirmed present in the schema of record). No action needed.

## Disposition

Audit complete. 1 finding (missing functional ticker index on `trade_plans`), filed as `BLG-BE-82` (P3) rather than fixed inline, per this story's acceptance criteria ("any missing indexes produce separate BLG items before sign-off"). No other index gap found across the four resolved tables' actual read-query shapes. `ai_journal_entries` is out of scope for remediation (externally-provisioned, no CREATE TABLE in this codebase).

## Sign-off

**Reviewed by:** Infrastructure & Operations Owner
**Status:** Approved
**Date:** 2026-08-06
**Notes:** Method and findings verified against the actual `ensure_*` create-paths and call sites cited (not just `data_model.md` prose). Table-name reconciliation (Finding table) is transparent and traceable — same disclosure standard as EPIC-01/ST-04's "Gemini"→Anthropic key resolution. Sole gap (trade_plans ticker index) correctly filed as a separate backlog item rather than fixed inline, per this story's own acceptance criteria. `ai_journal_entries` scoping-out is correctly reasoned (no CREATE TABLE in this codebase) and consistent with the standing `BLG-SPEC-109` finding — no duplicate filing.
