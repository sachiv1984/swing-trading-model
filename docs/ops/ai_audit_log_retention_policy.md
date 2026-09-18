**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-09-16 (ST-07/ST-06, BLG-OPS-154/BLG-OPS-153 — scope extended to `api_call_log`; added storage/row-count projection and silent-purge-failure visibility); prior — 2026-09-10 (ST-13, BLG-OPS-94 — initial policy for gemini_audit_log/claude_audit_log).
**Source:** ST-13 (BLG-OPS-94, EPIC-03, v9.3 sprint execution); ST-07/ST-06 (BLG-OPS-154/BLG-OPS-153, EPIC-02, v9.5 sprint execution)

---

# AI Audit Log Retention Policy

## Purpose

ST-13's acceptance criteria: define a retention window and an archival/deletion procedure for `gemini_audit_log` and `claude_audit_log`, and either execute a first cleanup pass or explicitly defer it with rationale.

**Scope extension (ST-07, BLG-OPS-154, EPIC-02, v9.5):** `api_call_log` — a generic external-API call-count instrumentation table (`backend/database.py`, distinct from the two AI-cost audit tables below: it tracks call *counts*, not tokens/cost) — had no retention window either. It is folded into this same policy document rather than a separate one because it shares the identical enforcement mechanism (`POST /ops/purge-audit-logs`, `.github/workflows/daily-snapshot.yml`'s daily scheduled call) with the two tables below.

## Background

Three tables accumulate call-audit metadata (never AI-generated content itself — see each table's schema below), all growing without bound before this policy:

- **`gemini_audit_log`** — narrower coverage: only the 2 `gemini_service.py` call sites (`POST /trade-plans/generate-plan`, `POST /trade-plans/{plan_id}/generate-thesis`). Already had a documented 90-day retention window (`docs/ops/gemini_cost_tracking.md` v1.2, unchanged by this story) and a purge function (`purge_gemini_audit_log_older_than_90_days()`), but — discovered during this story — **the purge function was never actually called anywhere in the codebase**. The 90-day policy existed only as a comment and a dead function; nothing enforced it.
- **`claude_audit_log`** — broader coverage: every `create_claude_audit_entry()` call site (daily briefing, chat, debrief, plan generation, thesis generation — 5 feature tags, see `docs/specs/api_contracts/ai_endpoints.md#GET /ai/monthly-cost-by-feature`'s taxonomy table). Had **no retention window at all** before this story — `docs/ops/render_log_retention_policy.md` §3.1 (v1.0, 2026-05-31) explicitly assessed this as a feature ("no row-level expiry configured; rows persist indefinitely" — framed as durability, in contrast to Render's 7-day platform log window).
- **`api_call_log`** (ST-07, BLG-OPS-154, EPIC-02, v9.5) — call-count-only instrumentation (no cost/token figures) for external services with no per-call cost, e.g. Alpaca market data and the Research endpoint's upstream sources (`backend/database.py::log_api_call`). Backs `GET /ops/alpaca-call-report` and `GET /ops/research-session-report`. Had no retention window before this story.

## Decision

| Table | Retention window | Rationale |
|-------|-------------------|-----------|
| `gemini_audit_log` | **90 days** (unchanged) | Already an established, documented decision (`gemini_cost_tracking.md` v1.2). No compelling reason found to revise it — this table's narrower coverage (2 call sites) makes it lower-value for long-range compliance review than `claude_audit_log`. |
| `claude_audit_log` | **730 days (24 months), newly defined** | Balances `render_log_retention_policy.md`'s prior compliance-durability framing (Claude API cost monitoring, thesis generation history) against unbounded storage/query-performance growth — the actual reason this story exists (BLG-OPS-94 is an ops/cost debt item). 24 months is the upper end of this story's own AC example range ("12–24 months"), chosen over the lower end specifically to preserve `render_log_retention_policy.md`'s durability intent as much as possible while still bounding growth, rather than silently reversing that prior assessment to a much shorter window. |
| `api_call_log` | **90 days, newly defined (ST-07)** | Matches `gemini_audit_log`'s window rather than `claude_audit_log`'s: this table has no cost/compliance value (call counts only, feeding short-lived rate-limit/quota anomaly checks over a rolling 7-day window per `get_api_session_report()`), so there is no long-range-review reason to retain it 24 months. 90 days gives ~13x the longest lookback window any current consumer (`GET /ops/research-session-report`, 7 days) actually uses. |

**This is a genuine policy change from `render_log_retention_policy.md`'s prior "no row-level expiry configured" assessment** — see that document's own §3.1 update (same commit) acknowledging the change and pointing here.

## Archival/Deletion Procedure

**Method: hard delete, not archive.** No external archival store (S3, cold-storage table, etc.) is configured anywhere in this codebase, and adding one is out of this story's scope (ST-13 is `autonomous` — policy definition + implementation, per `sprint_backlog.md`; provisioning new infrastructure is a larger decision). Rows past their retention window are deleted outright via SQL `DELETE`, matching `gemini_audit_log`'s pre-existing (if previously unenforced) approach.

**Mechanism:**
1. `backend/database.py::purge_gemini_audit_log_older_than_90_days()` (pre-existing), `purge_claude_audit_log_older_than_730_days()` (ST-13), and `purge_api_call_log_older_than_90_days()` (ST-07, v9.5) — all fail-safe (return `0` on any DB error, never raise).
2. `POST /ops/purge-audit-logs` — calls all three functions, returns rows deleted per table plus a `possible_silent_failure` list (ST-06 sub-item 3, v9.5 — see below). Contract: `docs/specs/api_contracts/ops_endpoints.md#POST /ops/purge-audit-logs`.
3. **Enforcement (the actual gap this story closes):** `.github/workflows/daily-snapshot.yml` now calls this endpoint as part of its existing daily scheduled maintenance run — see that workflow's "Purge AI Audit Logs" step. Previously nothing called the gemini purge function; now all three tables are purged daily, safely (idempotent — a day with no stale rows deletes 0).

**Silent-purge-failure visibility (ST-06 sub-item 3, BLG-OPS-153, EPIC-02, v9.5):** because every purge function above fails safe, a `0`-deleted result on its own cannot distinguish "nothing qualified" from "the purge is broken" (e.g. a credentials issue on the scheduled workflow step). `backend/database.py::count_gemini_audit_log_older_than_90_days()` / `count_claude_audit_log_older_than_730_days()` / `count_api_call_log_older_than_90_days()` are read-only counterparts run immediately after each purge attempt: if a table reports `0` deleted but its count is `> 0`, that table is logged as a `WARNING` (`purge_audit_logs: <table> reported 0 rows deleted but stale rows are still present...`) and listed in the endpoint's `possible_silent_failure` response field, giving an operator a concrete signal to check the workflow run logs rather than silently trusting an all-zero response indefinitely.

## First Cleanup Pass

**Deferred, with rationale:** this story's execution environment has no access to a live production or staging database — no `DATABASE_URL` pointing at a real Postgres instance is configured here (the test suite runs against a stubbed `database` module or explicit per-test mocks, never a live connection). Per this story's own `sprint_backlog.md` staging-only-ACs note: *"requires inspecting actual row counts in the live gemini_audit_log/Claude audit log tables; not reproducible from a CI fixture."*

The mechanism is fully implemented and unit-tested (see `tests/test_cost_monitoring.py`) and will execute automatically at its next scheduled `daily-snapshot.yml` run once this PR merges and deploys — no manual first-run action is required beyond that deploy. If either table happens to hold rows already past its window (plausible for `claude_audit_log`, which has accumulated since v4.2 with no prior expiry), those rows will be deleted on that first automatic run, same as every run after it. Nothing in this design requires a distinct manual "first pass" step.

## Storage/Row-Count Projection (ST-06 sub-item 1, BLG-OPS-153, EPIC-02, v9.5)

Rough estimate at current observed call volume — no live production database is accessible from this execution environment (see "First Cleanup Pass" above), so this is derived from each table's known schema (fixed-width columns, no large free-text fields — `ai_output_boundary_samples`, which does store generated text, is a separate table with its own 90-day policy) and the call-site inventory each table's coverage section above documents, not a live `pg_total_relation_size` reading.

| Table | Est. row width | Call sites / cadence | Retention window | Est. steady-state rows | Est. steady-state size |
|-------|----------------|------------------------|-------------------|--------------------------|--------------------------|
| `claude_audit_log` | ~150 bytes/row (UUID, 3 short TEXT columns, 2 INTEGER, 1 NUMERIC, 1 TIMESTAMPTZ, nullable TEXT) | 6 AI-invoking endpoints (per `docs/ops/ai_feature_cost_trend_2026_q3.md` §3), each triggered by discretionary user action — no fixed cadence, but bounded by realistic manual usage (order of 10s of calls/day across all 6 combined at current adoption, not a scheduled job) | 730 days | ~7,300–36,500 rows (10–50/day × 730) | ~1.1–5.5 MB |
| `gemini_audit_log` | ~130 bytes/row (narrower schema — see `gemini_cost_tracking.md`) | 2 call sites (`generate-plan`, `generate-thesis`), same discretionary-usage bound | 90 days | ~450–1,800 rows | <0.5 MB |
| `api_call_log` | ~90 bytes/row (UUID, 2 short TEXT, TEXT session_id, TIMESTAMPTZ, BOOLEAN) | Instrumentation on every Alpaca/Research external call — much higher-frequency than the AI tables above (per-request, not per-user-action; order of 100s–1000s/day plausible under active trading-session usage) | 90 days | ~9,000–90,000 rows (100–1000/day × 90) | ~0.8–8 MB |

**Conclusion:** even at the high end of these ranges, combined steady-state storage across all three tables is low single-digit megabytes — an order of magnitude below anything that would independently justify shortening a retention window on storage-cost grounds alone. This projection exists to make that conclusion explicit and re-checkable (re-derive from real row counts via `SELECT COUNT(*), pg_size_pretty(pg_total_relation_size(...))` once a live database connection is available — flagged as a `[staging-only evidence]`-style follow-up, not blocking this story), not because the current estimate suggests a problem.

## Acceptance

- Defined by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — policy definition + implementation, no observable UI behaviour)
- Date: 2026-09-10; extended 2026-09-16 (ST-07/ST-06, BLG-OPS-154/BLG-OPS-153) — FinOps & Resource Architect sign-off (storage projection, ST-06 sub-item 1); Infrastructure & Operations Owner sign-off (api_call_log retention/purge, ST-07; silent-purge-failure visibility, ST-06 sub-item 3)
