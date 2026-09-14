**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-10
**Source:** ST-13 (BLG-OPS-94, EPIC-03, v9.3 sprint execution)

---

# AI Audit Log Retention Policy

## Purpose

ST-13's acceptance criteria: define a retention window and an archival/deletion procedure for `gemini_audit_log` and `claude_audit_log`, and either execute a first cleanup pass or explicitly defer it with rationale.

## Background

Two tables accumulate AI-call audit metadata (never AI-generated content itself — see each table's schema below), both growing without bound before this policy:

- **`gemini_audit_log`** — narrower coverage: only the 2 `gemini_service.py` call sites (`POST /trade-plans/generate-plan`, `POST /trade-plans/{plan_id}/generate-thesis`). Already had a documented 90-day retention window (`docs/ops/gemini_cost_tracking.md` v1.2, unchanged by this story) and a purge function (`purge_gemini_audit_log_older_than_90_days()`), but — discovered during this story — **the purge function was never actually called anywhere in the codebase**. The 90-day policy existed only as a comment and a dead function; nothing enforced it.
- **`claude_audit_log`** — broader coverage: every `create_claude_audit_entry()` call site (daily briefing, chat, debrief, plan generation, thesis generation — 5 feature tags, see `docs/specs/api_contracts/ai_endpoints.md#GET /ai/monthly-cost-by-feature`'s taxonomy table). Had **no retention window at all** before this story — `docs/ops/render_log_retention_policy.md` §3.1 (v1.0, 2026-05-31) explicitly assessed this as a feature ("no row-level expiry configured; rows persist indefinitely" — framed as durability, in contrast to Render's 7-day platform log window).

## Decision

| Table | Retention window | Rationale |
|-------|-------------------|-----------|
| `gemini_audit_log` | **90 days** (unchanged) | Already an established, documented decision (`gemini_cost_tracking.md` v1.2). No compelling reason found to revise it — this table's narrower coverage (2 call sites) makes it lower-value for long-range compliance review than `claude_audit_log`. |
| `claude_audit_log` | **730 days (24 months), newly defined** | Balances `render_log_retention_policy.md`'s prior compliance-durability framing (Claude API cost monitoring, thesis generation history) against unbounded storage/query-performance growth — the actual reason this story exists (BLG-OPS-94 is an ops/cost debt item). 24 months is the upper end of this story's own AC example range ("12–24 months"), chosen over the lower end specifically to preserve `render_log_retention_policy.md`'s durability intent as much as possible while still bounding growth, rather than silently reversing that prior assessment to a much shorter window. |

**This is a genuine policy change from `render_log_retention_policy.md`'s prior "no row-level expiry configured" assessment** — see that document's own §3.1 update (same commit) acknowledging the change and pointing here.

## Archival/Deletion Procedure

**Method: hard delete, not archive.** No external archival store (S3, cold-storage table, etc.) is configured anywhere in this codebase, and adding one is out of this story's scope (ST-13 is `autonomous` — policy definition + implementation, per `sprint_backlog.md`; provisioning new infrastructure is a larger decision). Rows past their retention window are deleted outright via SQL `DELETE`, matching `gemini_audit_log`'s pre-existing (if previously unenforced) approach.

**Mechanism:**
1. `backend/database.py::purge_gemini_audit_log_older_than_90_days()` (pre-existing) and the new `purge_claude_audit_log_older_than_730_days()` — both fail-safe (return `0` on any DB error, never raise).
2. `POST /ops/purge-audit-logs` (new, this story) — calls both functions, returns rows deleted per table. Contract: `docs/specs/api_contracts/ops_endpoints.md#POST /ops/purge-audit-logs`.
3. **Enforcement (the actual gap this story closes):** `.github/workflows/daily-snapshot.yml` now calls this endpoint as part of its existing daily scheduled maintenance run — see that workflow's "Purge AI Audit Logs" step (same commit). Previously nothing called the gemini purge function; now both tables are purged daily, safely (idempotent — a day with no stale rows deletes 0).

## First Cleanup Pass

**Deferred, with rationale:** this story's execution environment has no access to a live production or staging database — no `DATABASE_URL` pointing at a real Postgres instance is configured here (the test suite runs against a stubbed `database` module or explicit per-test mocks, never a live connection). Per this story's own `sprint_backlog.md` staging-only-ACs note: *"requires inspecting actual row counts in the live gemini_audit_log/Claude audit log tables; not reproducible from a CI fixture."*

The mechanism is fully implemented and unit-tested (see `tests/test_cost_monitoring.py`) and will execute automatically at its next scheduled `daily-snapshot.yml` run once this PR merges and deploys — no manual first-run action is required beyond that deploy. If either table happens to hold rows already past its window (plausible for `claude_audit_log`, which has accumulated since v4.2 with no prior expiry), those rows will be deleted on that first automatic run, same as every run after it. Nothing in this design requires a distinct manual "first pass" step.

## Acceptance

- Defined by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — policy definition + implementation, no observable UI behaviour)
- Date: 2026-09-10
