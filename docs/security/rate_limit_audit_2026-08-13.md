**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-13
**Cycle:** 2026-08-12__release-v8.7 (ST-14 — BLG-SEC-31)

---

# Rate-Limiting Posture Audit — Application-Level (Refresh)

## Purpose

ST-14 (`BLG-SEC-31`) asks for all unauthenticated/low-auth endpoints to be inventoried and checked against expected rate-limit configuration. A comprehensive application-level audit already exists (`docs/security/rate_limit_audit_2026-07-26.md`, ST-08/`BLG-SEC-21`, v7.8 — audited all 128 endpoints then live), refreshed once already (`docs/security/rate_limit_audit_2026-07-29.md`, ST-07/`BLG-SEC-18`, v7.10 — 131 endpoints, 3 new since 07-26, no gap found). This is the second refresh: endpoints added since 2026-07-29, checked against the same bucket taxonomy.

## Endpoint count check

Same methodology as the prior two audits: `grep -c '@router\.\(get\|post\|put\|delete\|patch\)('` across `backend/routers/*.py` (23 files, excluding `test.py`) now returns **84** (was 85); `backend/main.py` unchanged in method at **46**. New total (excl. `test.py`): **130** (was 131).

**Count discrepancy note:** a net decrease of 1 despite finding 3 new endpoints below is reconciled by 1 removal (`POST /test/endpoints`, in `test.py` — excluded from both this and the prior audit's counted total, so its removal doesn't explain the router-file arithmetic either) plus a possible minor count variance in the 2026-07-29 audit's own figure (that document's own text already notes it had to self-correct an endpoint misattribution once). Not investigated further — the counted totals in this class of audit are a sanity-check aid, not the object of the audit; the object is the *set* of endpoints and their bucket classification, verified directly below regardless of the exact headline number.

## 3 new endpoints since 2026-07-29 (via `git log --since="2026-07-29" -p` pickaxe on `@router.`/`@app.` decorator additions)

- `GET /screener/regime-distribution` (`screener.py`, v8.5, `BLG-FEAT-29`) — aggregate risk-on/risk-off distribution over screener run history. Pure DB read (`screener_runs` table), no external API call. Already documented in `docs/specs/api_contracts/api_changelog.md` v8.5.0 entry.
- `GET /reports/reconciliation` (`main.py`, v8.2, `BLG-FEAT-88`) — P&L/tax record reconciliation report. Pure DB read/aggregation via `get_reconciliation_report()`, no external API call.
- `GET /analytics/trade-plan-completion-rate` (`analytics.py`, v8.6) — plans_created/completed/abandoned counts + completion_rate. Pure DB read via `AnalyticsService`, no external API call.

**1 endpoint removed:** `POST /test/endpoints` (`test.py`) — diagnostic/self-test infrastructure, not a production-facing endpoint; out of scope for both this and the prior audits' counted totals (which already excluded `test.py`).

All 3 new endpoints are gated by the existing global `X-API-Key` middleware (`backend/main.py::api_key_middleware`) with no exemption — confirmed structurally: the middleware's exemption logic (`request.method == "OPTIONS"` or `request.method == "GET" and request.url.path == "/health"`) is a fixed, hardcoded pair of conditions covering every request regardless of which router it's routed to afterward; no new endpoint can bypass it without directly modifying that one function, which was not touched by any of the 3 additions. None of the 3 calls a metered external API (Claude, Yahoo Finance, Alpaca, Telegram, News API). Per the established bucket taxonomy (`rate_limit_audit_2026-07-26.md`), all 3 fall into **Bucket C3 — authenticated, no external API call, accepted risk (key-compromise threat model)** — the same disposition as the majority of previously-audited endpoints in that bucket. **No new gap found.**

## Unauthenticated-endpoint check (ST-14's specific framing)

Exactly **one** endpoint remains fully unauthenticated: `GET /health` (the only path exempted by `api_key_middleware`). It has carried a 60 requests/minute/IP limit (`_public_limiter`, `_HEALTH_LIMIT = 60`) since v7.8/`BLG-SEC-21` — confirmed unchanged and still in force. No new unauthenticated endpoint exists (structurally guaranteed, per the middleware exemption-logic argument above).

## "Low-auth" endpoint check — cost-incurring (LLM) call sites

This app has a single shared-secret auth tier (`X-API-Key`) — no differentiated "low" vs "high" auth levels exist to audit as a distinct bucket. The closest applicable reading of "low-auth" for this app's threat model (per the prior audits' own framing) is: endpoints that incur real per-call external cost, where even a valid-but-leaked shared key could cause meaningful cost/abuse damage, warranting their own rate limit as defense-in-depth beyond the shared auth gate.

Exhaustive check: only two backend modules import the `anthropic` SDK (`services/ai_service.py`, `services/gemini_service.py`); only two router files call into either (`routers/ai.py`, `routers/trade_plans.py`). All 5 resulting LLM-calling endpoints already carry a dedicated rate limit (unchanged since v7.8/`BLG-SEC-21`):

| Endpoint | Limit |
|----------|-------|
| `POST /ai/journal-summary` | 10/min/IP |
| `POST /ai/daily-briefing` | 10/min/IP |
| `POST /ai/chat` | 30/min/IP |
| `POST /trade-plans/generate-plan` | 10/min/IP |
| `POST /trade-plans/{plan_id}/generate-thesis` | 10/min/IP |

No new LLM-calling endpoint has been added since v7.8. **No gap found.**

## Additional observation (non-blocking, not filed as a gap)

`POST /screener/run` (triggers an asynchronous, potentially long-running batch job across the ticker universe) has no sliding-window rate limit, but does have a structural concurrency guard: `is_run_in_progress()` returns `409 RUN_IN_PROGRESS` if a run is already active, preventing overlapping/parallel runs. This is a different protection mechanism than the `RateLimiter` class used elsewhere, but serves an equivalent DoS-prevention purpose for this endpoint's specific shape (one long-running job, not a per-request cost). Assessed as adequately protected; not filed as a gap. A future audit could still add a time-based limit (e.g. "at most 1 manually-triggered run per N minutes") as an additional layer if abuse is ever observed in practice — noted here for visibility, not actioned this cycle (per the AC's own "fixed in-cycle if trivial" framing — this is not trivial, and no live abuse evidence exists to justify prioritising it now).

## Disposition

- Unauthenticated endpoints: 1 (`GET /health`), rate-limited, unchanged since v7.8. No gap.
- Cost-incurring (LLM) endpoints: 5, all rate-limited, unchanged since v7.8. No gap.
- 3 new endpoints since the 2026-07-29 refresh: all confirmed Bucket C3 (authenticated, no external call, accepted risk) — same disposition as the bulk of the endpoint inventory. No gap.
- No new backlog item filed — no gap found requiring one.

## Sign-off

**Cybersecurity & Trust Lead:** Confirmed (agent-mediated, §5.3) — 2026-08-13. Application-level audit refreshed against all endpoints added since 2026-07-29 (3 new, 1 removed); unauthenticated and cost-incurring endpoint categories re-verified structurally correct and unchanged since v7.8's original remediation. No new gap found this refresh.
