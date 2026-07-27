**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-26
**Cycle:** 2026-07-24__release-v7.8 (ST-08 — BLG-SEC-21)

---

# Rate-Limiting Audit — Public-Facing Endpoints

## Purpose

ST-08 (EPIC-08, BLG-SEC-21) extends `BLG-SEC-18`'s general rate-limiting audit, prioritising the specific question: **which endpoints have zero documented rate limit, and for each, is that an accepted risk or a remediation?** This is a bounded, mechanical pass per RISK-04 — not an open-ended full remediation project.

## Scope Note (flagged, not silently resolved)

The story's framing named "82 endpoints across `backend/routers/*.py`" as the audit surface. That count is accurate for `routers/*.py` alone, but **46 additional endpoints are registered directly in `backend/main.py`** (outside any router file) — bringing the true total to **128 live HTTP endpoints** (confirmed by direct count: `grep -c '@app\.\(get\|post\|put\|delete\|patch\)(' backend/main.py` → 46). This audit covers all 128, not just the 82, because the story's intent ("rate-limiting review of public-facing endpoints") is clearly about the whole app surface, not an artefact of how routes happen to be split across files. `GET /health` — the single highest-priority finding below — is one of the 46 `main.py` endpoints, so scoping to 82 would have missed it entirely.

## Method

Full enumeration of all `@router.*`/`@app.*` HTTP method decorators across `backend/routers/*.py` (23 files) and `backend/main.py`, cross-referenced against: (a) app-level rate-limiter usage (`services/rate_limiter.py`), (b) `X-API-Key` middleware coverage (`backend/main.py` `api_key_middleware`), (c) whether each handler makes an outbound call to a metered/paid external API (Alpaca, Yahoo Finance, Anthropic/Claude, Telegram, News API) that would amplify cost or load per request beyond a plain DB read.

## Findings Summary

| Bucket | Count | Description |
|--------|-------|-------------|
| A — Already rate-limited | 2 | `POST /ai/daily-briefing` (10/min/IP), `POST /ai/chat` (30/min/IP) — pre-existing, unchanged this cycle |
| B — Unauthenticated + unlimited (remediated) | 1 | `GET /health` |
| C1 — Authenticated, calls a metered external API, previously unlimited (remediated) | 3 | `POST /ai/journal-summary`, `POST /trade-plans/generate-plan`, `POST /trade-plans/{plan_id}/generate-thesis` |
| C2 — Authenticated, calls a metered external API, accepted as lower-priority risk this cycle | 6 | `GET /earnings/{ticker}`, `GET /news/{ticker}`, `GET /portfolio/paper-positions`, `GET /research/{ticker}`, `POST /screener/run`, `POST /ticker-universe` |
| C3 — Authenticated, no external API call, accepted risk (key-compromise threat model) | 116 | All remaining endpoints across `routers/*.py` and `main.py` |

## Remediation (this cycle)

### 1. `GET /health` — the one true unauthenticated surface

Confirmed via `api_key_middleware` (`backend/main.py`) that `GET /health` is the app's **only** endpoint exempted from `X-API-Key` auth (exact-path match, not a prefix — `/health/detailed`, `/health/database`, `/health/scheduler` all still require the key). It performs 4 DB queries per call and had no rate limit of any kind. **Remediated**: added a new `_public_limiter` instance (`services/rate_limiter.py`) — kept separate from `_ai_limiter` so unauthenticated public traffic can never starve AI-endpoint quota — and gated `GET /health` at **60 requests/minute/IP** (`backend/main.py`).

### 2. Three previously-unlimited endpoints calling Claude directly

`ai.py` already has a working per-endpoint limiter pattern (`_ai_limiter`, used by `/ai/daily-briefing` and `/ai/chat`), but 3 sibling endpoints across the AI/trade-plan surface called Anthropic Claude directly with **no rate limit at all** — a live cost-amplification path for an authenticated-but-compromised key. **Remediated** by applying the identical existing pattern (mechanical reuse, no new mechanism):
- `POST /ai/journal-summary` — 10/min/IP (`routers/ai.py`)
- `POST /trade-plans/generate-plan` — 10/min/IP (`routers/trade_plans.py`)
- `POST /trade-plans/{plan_id}/generate-thesis` — 10/min/IP (`routers/trade_plans.py`)

## Accepted Risk (not remediated this cycle — recorded, not silently skipped, per RISK-04)

### Bucket C2 — other external-API-calling endpoints (6)

| Endpoint | External call | Rationale for accepting risk this cycle |
|----------|---------------|------------------------------------------|
| `GET /earnings/{ticker}` | Live Yahoo Finance | Read-only, no cost per call (Yahoo Finance is unauthenticated/free), bounded by ticker-string input |
| `GET /news/{ticker}` | Live Alpaca News API | Same profile as Alpaca market-data calls already covered by Alpaca's own provider-side rate limiting (`services/alpaca_service.py`'s existing 429 retry/backoff handling) |
| `GET /portfolio/paper-positions` | Live Alpaca account API | Same Alpaca provider-side protection as above |
| `GET /research/{ticker}` | Yahoo Finance on cache miss | Already has a 15-minute per-(ticker,market) TTL cache; residual risk is bounded to distinct-ticker cache-bypass, not unbounded repetition of the same call |
| `POST /screener/run` | Full-universe Yahoo Finance batch (background task) | Already has a single-run-in-progress lock (409 if busy) preventing concurrent/overlapping runs — the remaining gap (rapid serial re-triggers) is a narrower risk than the 3 remediated Claude-calling endpoints |
| `POST /ticker-universe` | Live `yf.Ticker().info` per call | Read-only validation call against a free/unauthenticated Yahoo Finance surface, not a paid/metered API |

**Why accepted rather than remediated:** none of these 6 call a *paid, per-request-metered* API the way the 3 remediated Claude endpoints do (Yahoo Finance is free/unauthenticated; Alpaca's rate limiting is already handled provider-side per `alpaca_service.py`'s existing retry/backoff). Per RISK-04's bounded-scope framing, this cycle remediates the highest-marginal-risk gaps (unauthenticated surface + direct paid-LLM calls) and explicitly defers the remainder rather than expanding scope mid-cycle. Follow-up: file a backlog item if a future audit wants app-level limits on this bucket too (not filed this cycle — none of the 6 is P0/P1; RISK-04 explicitly permits "no implementation required unless a P0/P1 gap is found," and none of these 6 was assessed as P0/P1).

### Bucket C3 — remaining 116 endpoints (no external API call)

Standard authenticated, no-app-level-limit posture. All require a valid `X-API-Key`; abuse requires a leaked/compromised key, which is the threat model already covered by `docs/ops/api_key_rotation_and_audit_schedule.md` (this cycle, EPIC-07) and `docs/ops/api_key_rotation_policy.md`'s emergency rotation triggers. Accepted as low-risk in bulk per RISK-04 — DB-read/write endpoints carry no external cost-amplification surface, only ordinary DB load, which is a capacity/ops concern rather than a security gap.

### Local-dev auth-bypass note (observed during audit, not a new gap)

If the `API_KEY` environment variable is unset entirely, `api_key_middleware` bypasses auth for **every** endpoint (documented local-dev fallback). This is pre-existing behaviour, not introduced by this audit, and is out of scope for ST-08's remediation — noted here only so it isn't silently missed by a future audit re-reading this document.

### Naming note (observed, not a security finding)

`backend/services/gemini_service.py` is misleadingly named — it calls the Anthropic Claude API exclusively (`anthropic.Anthropic(...)`, model `claude-haiku-4-5`/`claude-sonnet-4-6`), not Google Gemini. This is a pre-existing finding already recorded in `backend/database.py`'s `get_monthly_claude_cost()` docstring (`ESC-EXEC-20260720-01`) and cross-referenced in this cycle's `docs/ops/api_key_rotation_and_audit_schedule.md` (EPIC-07). Not a rate-limiting concern; noted here only because the audit surfaced it again independently.

---

## Test Coverage

`tests/test_rate_limit_endpoints.py` — 5 tests: each of the 4 newly-limited endpoints is driven to its configured ceiling and the next request is confirmed to return HTTP 429 with a `Retry-After` header; plus a test confirming `_ai_limiter` and `_public_limiter` are distinct instances (so unauthenticated `/health` traffic cannot exhaust AI-endpoint quota or vice versa). All 5 pass; full regression suite (759 tests) confirms no behavioural change to any other endpoint.

---

## Acceptance

- Accepted by: Cybersecurity & Trust Lead
- Date: 2026-07-26
