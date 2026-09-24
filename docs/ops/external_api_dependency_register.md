**Owner:** PMO Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-09-24 (ST-28, EPIC-07, v9.7, BLG-OPS-167 — added yfinance, Anthropic, Supabase, and Render entries, covering all 5 dependencies named in this cycle's failure-mode-matrix story; Alpaca and News API entries unchanged)
**Cycle:** 2026-04-29__release-v3.1 (ST-12)

---

# External API Dependency Register

## Purpose

This register documents all external API dependencies of the Momentum Trading Assistant, their known failure modes, mitigations, and monitoring approach. It is used for incident management, risk review, and onboarding.

---

## Dependencies

### 1. Alpaca Markets API

| Field | Value |
|-------|-------|
| Service | Alpaca Markets |
| Type | Brokerage & market data API |
| Usage | Live price fetching (positions P&L update), bar data (ATR calculation), paper/live order management |
| Endpoint(s) | `https://paper-api.alpaca.markets` (paper) or `https://api.alpaca.markets` (live) |
| Auth | API key + secret (see `external_api_credential_inventory.md`) |
| SLA/uptime | Alpaca publishes a status page; no formal SLA for paper trading tier |

#### Known Failure Modes

| ID | Mode | Description | Introduced |
|----|------|-------------|------------|
| AFM-01 | Null bars crash | When Alpaca returns `null` for a bars response (e.g. non-trading hours, halted ticker, or paper account with no data), the system previously raised an unhandled `AttributeError` or `NoneType` error in the price-fetching layer. | v3.0 incident |
| AFM-02 | Hyphenated ticker handling | Alpaca uses hyphens in some ticker symbols (e.g. `BRK-B`). If the system sends a dot-format or un-normalised ticker to Alpaca, the request fails silently or returns empty data. | v3.0 identified |
| AFM-03 | Rate limiting | Alpaca enforces rate limits on the data API. Bulk operations (e.g. screener enrichment) can exhaust rate limits if not throttled. | Operational observation |

#### Mitigations in Place

| ID | Mode Addressed | Mitigation |
|----|---------------|------------|
| MIT-01 | AFM-01 | `get_current_price` in `utils/pricing.py` wraps Alpaca bar responses with null-guards. If bars is null or empty, returns a fallback price of 0.0 and logs a warning rather than raising. Deployed v3.0 hotfix. |
| MIT-02 | AFM-02 | Ticker normalisation applied at the screener ingestion layer — hyphenated tickers are converted before external API calls. |
| MIT-03 | AFM-03 | Screener batch service uses sequential processing with per-request delays. Bulk enrichment is rate-limited at the service layer. |

#### Monitoring Approach

- `GET /health/detailed` checks Alpaca connectivity and records last successful price fetch
- `GET /health` returns degraded state if Alpaca is unreachable
- Render logs capture all Alpaca API errors with ticker and response body
- Alert: if more than 3 consecutive position price-fetch failures occur, the positions page will display stale-price warnings (controlled by `last_updated` timestamp)

---

### 2. News API

| Field | Value |
|-------|-------|
| Service | News API (newsapi.org or equivalent) |
| Type | Financial news aggregation API |
| Usage | Fetching ticker-specific news for `GET /news/{ticker}` |
| Auth | API key (see `external_api_credential_inventory.md`) |
| SLA/uptime | No formal SLA; free tier enforces 100 requests/day cap |

#### Known Failure Modes

| ID | Mode | Description | Introduced |
|----|------|-------------|------------|
| NFM-01 | Rate limit exhaustion | Free tier cap of 100 requests/day. Under active use, limit can be reached during the trading day. | Operational observation |
| NFM-02 | Ticker with no news | Some tickers return no articles; API returns empty `articles` array rather than an error. | Operational observation |
| NFM-03 | API key expiry / plan downgrade | If the news API key is revoked or the account plan is downgraded, all news requests return 401. | Operational risk |

#### Mitigations in Place

| ID | Mode Addressed | Mitigation |
|----|---------------|------------|
| MIT-04 | NFM-01 | `GET /news/{ticker}` endpoint handles 429 gracefully — returns empty array with a `source_note` field explaining rate limit. Frontend displays "News temporarily unavailable" rather than an error state. |
| MIT-05 | NFM-02 | Empty `articles` array is handled by the frontend — shows "No recent news" state rather than a spinner or error. |
| MIT-06 | NFM-03 | Credential inventory tracks key status. Rotation policy in `external_api_credential_inventory.md` covers provider key renewal. |

#### Monitoring Approach

- News API failures are logged at WARNING level in Render logs
- The `/health/detailed` endpoint does not currently probe the news API (non-critical path)
- Manual monitoring: check Render logs if users report missing news

---

### 3. yfinance (Yahoo Finance)

| Field | Value |
|-------|-------|
| Service | Yahoo Finance (via the `yfinance` Python package) |
| Type | Unofficial market data API (screen-scrape/undocumented endpoint wrapper, not a formal REST API with a published contract) |
| Usage | Primary market-data source for the screener pipeline, historical price/OHLCV data for technical indicators (ATR, moving averages), and price lookups where Alpaca does not cover the market (e.g. UK tickers) |
| Endpoint(s) | No stable published endpoint — `yfinance` calls Yahoo's internal query API, which is not a documented, versioned contract |
| Auth | None (no API key) |
| SLA/uptime | None. No formal support channel; Yahoo can change response shape or block scraping-pattern traffic without notice |

#### Known Failure Modes

| ID | Mode | Description | Introduced |
|----|------|-------------|------------|
| YFM-01 | Silent schema/shape drift | Because `yfinance` has no versioned contract, a Yahoo-side change to response field names or structure can silently return empty/malformed data rather than a clear error, since the package itself has no way to detect an upstream contract change. |
| YFM-02 | Rate limiting / IP-level blocking | High request volume from a single IP (e.g. Render's shared egress IP range) can trigger Yahoo's anti-scraping throttling, returning empty responses or HTTP 429-equivalent behaviour with no formal rate-limit header contract to read. |
| YFM-03 | Timeout on large history pulls | A 1-year daily-bar history pull for a 200-day moving average is a materially larger payload than a single-day quote lookup and is more likely to exceed a short timeout under slow upstream conditions. |

#### Mitigations in Place

| ID | Mode Addressed | Mitigation |
|----|---------------|------------|
| MIT-07 | YFM-03 | `backend/utils/upstream_call.py` configures a distinct, longer timeout (`yfinance_history`, 15s) for history-shaped calls, separate from the standard `yfinance` timeout (10s), plus bounded retry via `retry_with_backoff` (BLG-BE-71, BLG-BE-122). |
| MIT-08 | YFM-01, YFM-02 | `screener_data_service.py` falls back to Stooq and Twelve Data as secondary/tertiary tiers when a yfinance call fails or returns empty data — not a fix for the root cause, but bounds its blast radius on the screener path. |

#### Monitoring Approach

- yfinance call failures are logged at WARNING level; the fallback-tier activation (Stooq/Twelve Data) is itself a signal that yfinance degraded
- No dedicated `/health` probe for yfinance specifically — failures surface indirectly via screener data staleness or fallback-tier usage in logs

---

### 4. Anthropic (Claude API)

| Field | Value |
|-------|-------|
| Service | Anthropic Claude API |
| Type | LLM API — advisory-only AI features (daily briefing, chat, journal summarisation, trade-plan generation) |
| Usage | `POST /ai/daily-briefing`, `POST /ai/chat`, journal summarisation, trade-plan/thesis generation (`gemini_service.py`, despite the filename — historical naming), debrief compliance checks |
| Endpoint(s) | `https://api.anthropic.com` (via the official `anthropic` Python SDK) |
| Auth | API key (`ANTHROPIC_API_KEY`) |
| SLA/uptime | Anthropic publishes a status page (status.anthropic.com); no formal SLA on this account tier |

#### Known Failure Modes

| ID | Mode | Description | Introduced |
|----|------|-------------|------------|
| CFM-01 | Missing API key | If `ANTHROPIC_API_KEY` is not configured, AI features must degrade gracefully rather than 500 — a trading system's core function must not depend on an advisory-only AI feature being available. |
| CFM-02 | Transient 5xx / rate limit / timeout | Anthropic's own infrastructure can return transient errors or rate-limit responses under load, distinct from a genuine client-side error (bad request, auth failure). |
| CFM-03 | Retry backoff inflating recorded latency | Retried calls' recorded `latency_ms` includes backoff sleep time between attempts, not just the final successful attempt's duration (documented as intentional, see `docs/specs/api_contracts/ai_endpoints.md` §Implementation constraints, ST-13/BLG-BE-128, v9.7). |

#### Mitigations in Place

| ID | Mode Addressed | Mitigation |
|----|---------------|------------|
| MIT-09 | CFM-01 | Every AI-invoking endpoint checks for the configured key before calling Anthropic and returns a graceful "AI briefing unavailable — ANTHROPIC_API_KEY not configured" response (or equivalent), never a 500, when absent. |
| MIT-10 | CFM-02 | `backend/utils/upstream_call.py`'s `bounded_upstream_call` decorator (BLG-BE-122) wraps every Anthropic call site with a shared, configured timeout (60s) and bounded retry-with-backoff (`retryable_exceptions` scoped to genuinely transient Anthropic SDK exception types), rather than each call site independently reimplementing retry logic. |
| MIT-11 | — | AI output is advisory-only by design (SRB-v1.7) — never wired into any signal, scoring, or trade-execution pipeline, so an Anthropic outage degrades a convenience feature, not core trading functionality. |

#### Monitoring Approach

- `claude_audit_log` records every call's latency, cost, and outcome — `GET /ai/check-endpoint-anomalies` compares recent 24h p95 cost/latency against a trailing 7-day baseline per endpoint and alerts via Telegram on a >2x anomaly
- `GET /health/detailed` does not currently probe Anthropic directly (advisory-only path, not a hard dependency for core health)

---

### 5. Supabase (PostgreSQL)

| Field | Value |
|-------|-------|
| Service | Supabase-hosted PostgreSQL |
| Type | Primary relational database — the system of record for portfolios, positions, trade history, trade plans, alerts, and all other persisted state |
| Usage | Every read/write path in `backend/database.py`; there is no in-memory or cached fallback for core data |
| Endpoint(s) | A Supabase connection string (`DATABASE_URL`), pgBouncer-fronted |
| Auth | Connection-string credentials (readonly-staging and production credentials are distinct, per `shared_standards.md §16.16`'s sandbox constraint disclosure) |
| SLA/uptime | Supabase publishes a status page; formal SLA depends on the account's paid tier |

#### Known Failure Modes

| ID | Mode | Description | Introduced |
|----|------|-------------|------------|
| SFM-01 | Connection exhaustion | `backend/database.py`'s `get_db()` opens a new `psycopg2.connect()` per call with no connection pooling — a request path calling multiple DB functions in sequence (e.g. the pre-ST-12/BLG-BE-126 Monthly P&L snapshot path) can open several connections in a single HTTP request, and under concurrent load this can approach Supabase's connection limit. |
| SFM-02 | Schema drift from undocumented migrations | A live column can exist, be dropped, or have its nullability changed without a corresponding update to `data_model.md` (3 confirmed live instances found this cycle alone: `positions.exit_note` absent live, 4 orphaned always-NULL columns, `positions.fees_paid` nullability drift — `BLG-SPEC-149`/`150`/`151`). |
| SFM-03 | Query failure on a genuinely offline/unreachable database | A network partition, credential rotation without a corresponding app redeploy, or a Supabase-side outage causes every DB call to fail. |

#### Mitigations in Place

| ID | Mode Addressed | Mitigation |
|----|---------------|------------|
| MIT-12 | SFM-01 | ST-12 (EPIC-03, v9.7, BLG-BE-126) introduced an optional shared-`conn` parameter pattern for the Monthly P&L snapshot path specifically, reducing per-request connection count for that path from one-per-closed-month to at most one additional connection. Not yet applied system-wide — most other multi-call request paths still open one connection per DB function call. |
| MIT-13 | SFM-02 | Recurring live-schema-verification sessions (ST-22/v9.5, this cycle's ST-24/25/26) compare `data_model.md` against a live (readonly staging) schema query and file/fix any drift found — an audit practice, not a structural prevention. |
| MIT-14 | SFM-03 | `GET /health`/`GET /health/database` probe DB connectivity and report degraded status; `create_position`/`update_position` etc. do not currently retry on connection failure — a failed DB call surfaces as an error response to the caller rather than silently degrading, which is the correct behaviour for a system-of-record dependency (unlike the advisory-only AI path, silent degradation here would be worse than a visible failure). |

#### Monitoring Approach

- `GET /health/database` reports DB connectivity and usage; `check_daily_cost`/scheduled jobs can alert via Telegram if DB usage nears a configured threshold
- No connection-pool exhaustion metric currently exists (SFM-01 has no dedicated monitor — flagged, not yet instrumented)

---

### 6. Render (Hosting Platform)

| Field | Value |
|-------|-------|
| Service | Render.com |
| Type | PaaS hosting for the FastAPI backend and its scheduled jobs (cron-equivalent workflows) |
| Usage | Runs the deployed backend process, environment variable/secret injection, and (historically) some scheduled job execution — largely superseded by GitHub Actions cron workflows for scheduling, per this repo's `.github/workflows/*.yml` |
| Endpoint(s) | N/A — this is the hosting platform itself, not an API the application calls at runtime |
| Auth | N/A (deployment-time, not runtime) |
| SLA/uptime | Render publishes a status page; SLA depends on account tier |

#### Known Failure Modes

| ID | Mode | Description | Introduced |
|----|------|-------------|------------|
| RFM-01 | Cold start / spin-down on free-tier-equivalent plans | A Render web service on a lower-cost plan can spin down after inactivity and take tens of seconds to respond to the next request, which can be indistinguishable from an application-level outage to an external caller or a scheduled GitHub Actions job hitting the API. |
| RFM-02 | Deploy-time build/dependency failure | A `requirements.txt` change or platform-level Python version drift can fail the build step, leaving the previous deploy running (not necessarily a visible outage) but blocking the intended release. |
| RFM-03 | Shared egress IP triggering upstream rate limiting | Render's outbound IP range is shared across many customers' services — this is the plausible root cause of intermittent yfinance rate-limiting (YFM-02 above) independent of this application's own request volume. |

#### Mitigations in Place

| ID | Mode Addressed | Mitigation |
|----|---------------|------------|
| MIT-15 | RFM-01 | `docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md`'s synthetic-monitor workflow (`health-check-alert.yml`) periodically probes `GET /health` and alerts via Telegram on failure, surfacing a cold-start-induced slow/failed response the same way it would a genuine outage. |
| MIT-16 | RFM-02 | CI (`ci-tests.yml` and sibling workflows) runs the full test suite against the same `requirements.txt` before merge, catching most dependency-resolution failures before they reach a Render deploy. |
| MIT-17 | RFM-03 | Not directly mitigated at the Render layer — addressed indirectly via yfinance's own fallback tiers (MIT-08 above). |

#### Monitoring Approach

- Scheduled synthetic uptime monitoring (`health-check-alert.yml`) with Telegram alerting on failure
- Render's own deploy logs and dashboard for build/deploy-time failures (external to this repo's own logging)

---

## Register Maintenance

This register must be updated when:
- A new external API dependency is added to the system
- A new failure mode is identified (e.g. during an incident postmortem)
- A mitigation is deployed or removed
- A dependency is decommissioned

Commit updates with: `[GOVERNANCE] Update external API dependency register — <reason>`

---

## Acceptance

- Accepted by: PMO Lead
- Date: 2026-04-30
