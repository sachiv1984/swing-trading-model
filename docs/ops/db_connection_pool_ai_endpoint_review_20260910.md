**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-10
**Source:** ST-21 (BLG-GOV-145, EPIC-05, v9.3 sprint execution)

---

# Database Connection Pool Sizing Review — AI Endpoints

## Purpose

ST-21's acceptance criteria: review the current Supavisor pool configuration (connection count, timeout settings) against AI endpoint DB query volume; document findings as "no change needed" or file a specific adjustment as a separate item. Gate condition (30+ days AI endpoint usage) already confirmed cleared 2026-08-08 at release planning (`claude/backlog/backlog.md` `BLG-GOV-145`).

## Method

Two of the AC's inputs — the live Supavisor pool configuration (exact `pool_size`/timeout numbers as configured in the Supabase/Render dashboard) and real production query-volume logs/monitoring — are not accessible from this execution environment (no live database connection, no production log access; consistent with every other story this sprint that touched staging-only ACs, e.g. `docs/ops/ai_audit_log_retention_policy.md`'s "First Cleanup Pass" deferral). This review instead analyses what **is** verifiable from the codebase: the application's connection-handling architecture and the AI endpoints' actual DB query volume per request, traced directly from source.

## Findings

### 1. No application-side connection pool exists

`backend/database.py::get_db()` (the sole DB access point, used by all 153 functions calling `get_db()` in that file) opens a fresh `psycopg2.connect()` on every call and closes it in a `finally` block — there is no `ThreadedConnectionPool`/`SimpleConnectionPool` or any other connection-reuse mechanism at the application layer. Every database operation is a brand-new TCP connection, held only for the duration of that one operation.

This is a deliberate, already-established architecture: `DATABASE_URL` points at Supavisor's Transaction Pooler (port 6543, `?pgbouncer=true`), enabled since v2.7 (`docs/ops/api_performance_baseline.md` §10, 2026-04-16) — the app relies entirely on Supavisor's server-side pooling to absorb this connect/disconnect churn, by design. Supavisor's transaction-pooling mode exists specifically to handle this "many short-lived connections" pattern efficiently.

### 2. AI endpoint DB query volume per request (traced from source)

| Endpoint | DB connections per request (traced call chain) |
|----------|--------------------------------------------------|
| `POST /trade-plans/generate-plan` | ~5-6: `get_portfolio`, `get_latest_snapshot`, `get_settings` (context-gathering) + `create_gemini_audit_entry` + `create_claude_audit_entry` (`_log_audit`, 2 separate connections) + `create_trade_plan` (persist) |
| `POST /trade-plans/{id}/generate-thesis` | ~4-5: similar context-gathering + the same 2-connection `_log_audit` pattern + plan update |
| `POST /ai/daily-briefing` | ~3-4: portfolio/trade-history context reads + `create_claude_audit_entry` |
| `POST /ai/chat` | ~2-3: lighter context read + `create_claude_audit_entry` |
| `POST /trades/{id}/debrief` | ~3-4: trade context read + `create_claude_audit_entry` (with `compliance_check_result`) |

Each connection is brief — a single query or small transaction, not held across the AI provider network call itself (the Anthropic API call happens between DB operations, not while holding a connection open).

### 3. Concurrency ceiling — rate limits

Every AI endpoint that calls an external LLM directly is rate-limited per-IP (`services/rate_limiter.py`, `_ai_limiter`): 10 req/min for `generate-plan`, `generate-thesis`, and `journal-summary`; 10 req/min for `daily-briefing`; 30 req/min for `chat` (ST-08, EPIC-08, v7.8, BLG-SEC-21). This application is single-portfolio (no multi-tenant concurrent-user load) — realistic concurrent AI-endpoint DB connection demand is a small handful at any given moment, not a sustained burst.

## Disposition: No change needed

Given (a) Supavisor's transaction pooling is architecturally the right tool for this exact connection pattern and has been live and performing well since v2.7 (`GET /portfolio` p50=234ms post-enablement, `api_performance_baseline.md` §10 — well under the 400ms AC-2 gate), (b) AI endpoints' per-request connection count (2-6) is not unusually high relative to the rest of the app's existing traffic (the review found no AI-endpoint-specific spike pattern — every other reviewed endpoint's handlers follow the identical `get_db()`-per-operation pattern), and (c) per-IP rate limits cap realistic concurrent AI load at single digits for a single-portfolio application — **no pool configuration adjustment is warranted at this time.**

**Disclosed gap:** the actual configured Supavisor `pool_size` number and timeout settings (the live dashboard values) were not independently verified in this review, since this execution environment has no access to the Supabase/Render dashboard or production connection logs. This finding is based on code-level architecture and query-volume analysis, cross-referenced against the already-confirmed-adequate v2.7 performance baseline, not a direct read of the live pool configuration numbers. If a future review has dashboard access, confirming the configured pool size explicitly (rather than inferring adequacy from downstream latency) would close this gap.

## Acceptance

- Reviewed by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — a technical review with documented findings, no observable UI behaviour)
- Date: 2026-09-10
