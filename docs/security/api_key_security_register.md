**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.7
**Last Updated:** 2026-08-10 (ST-02, BLG-OPS-134, v8.5 — entry #6 updated: STAGING_API_KEY secret confirmed added, cross-environment check confirmed genuinely running via live log, false-positive alert bug hardened); prior — 2026-08-05 (ST-04/ST-03, v8.3 — entries #3/#6); prior history retained — see prior entries in version control
**Cycle:** 2026-08-08__release-v8.5 (ST-02 — BLG-OPS-134: entry #6 updated)

---

# External API Key Security Register

## Purpose

This register is the single authoritative source of record for all external API credentials used by the Momentum Trading Assistant. No sensitive values (keys, secrets, passwords) are stored here — only credential metadata.

> **Security alert:** If you find a key or secret value in this file, that is a security incident. Remove it immediately and rotate the credential. Report to the Cybersecurity & Trust Lead.

For rotation procedures, see: `docs/ops/api_key_rotation_policy.md`

---

## Register

### 1. Alpaca API Key

| Field | Value |
|-------|-------|
| Key name | Alpaca API Key ID |
| Env var | `APCA_API_KEY_ID` |
| Purpose | Live and paper trading operations; real-time market data (prices, bars) |
| Scope | Paper Trading or Live Trading (whichever is active) — read positions, place/cancel orders, stream prices |
| Storage location | Render environment variables (staging and production services) |
| Rotation cadence | Annual minimum (12 months) |
| Rotation procedure | `docs/ops/alpaca_key_rotation_policy.md` |
| Last rotation date | Unknown (pre-register baseline) |
| Next rotation due | 12 months from last rotation |
| Notes | Key ID is non-sensitive (public identifier). Secret (`APCA_API_SECRET_KEY`) is separate entry below. Uses Alpaca Paper Trading SDK naming convention. |

---

### 2. Alpaca API Secret

| Field | Value |
|-------|-------|
| Key name | Alpaca API Secret |
| Env var | `APCA_API_SECRET_KEY` |
| Purpose | Required alongside Alpaca API Key ID for all authenticated API calls |
| Scope | Same as Alpaca API Key — full Paper/Live Trading access |
| Storage location | Render environment variables (staging and production services) |
| Rotation cadence | Annual minimum (12 months) — rotate together with `APCA_API_KEY_ID` |
| Rotation procedure | `docs/ops/alpaca_key_rotation_policy.md` |
| Last rotation date | Unknown (pre-register baseline) |
| Next rotation due | 12 months from last rotation |
| Notes | Secret is shown only once at generation in the Alpaca dashboard. If lost, generate a new key pair. |

---

### 3. Anthropic API Key

| Field | Value |
|-------|-------|
| Key name | Anthropic API Key |
| Env var | `ANTHROPIC_API_KEY` |
| Purpose | AI thesis generation for trade plans (`POST /trade-plans/{plan_id}/generate-thesis`); calls `claude-haiku-4-5` via Anthropic SDK |
| Scope | Full Anthropic API access (platform does not support key-level scope restriction — see `docs/security/anthropic_api_key_scope_review.md`) |
| Storage location | Render environment variables (production and staging services) |
| Rotation cadence | Annual minimum (12 months) |
| Rotation procedure | 1. Generate a new key in Anthropic Console → Settings → API Keys. 2. Update `ANTHROPIC_API_KEY` in the Render staging service's Environment tab → save (triggers redeploy). 3. Verify on staging: `POST /trade-plans/{plan_id}/generate-thesis` returns 200 with the new key. 4. Repeat Steps 2–3 for the Render production service. 5. Revoke the old key in Anthropic Console only after production verification succeeds. 6. Update `Last rotation date` below and commit `[GOVERNANCE] Anthropic API key rotated YYYY-MM-DD`. Emergency rotation (suspected compromise): follow the Emergency Rotation Triggers table in `docs/ops/api_key_rotation_policy.md` — revoke first, within 1 hour of detection. General policy and background: `docs/ops/api_key_rotation_policy.md §Anthropic API Key`. (Runbook added ST-04, BLG-SEC-17, EPIC-01, v8.3 — this key is also referred to as the "Gemini API key" in older backlog items; `gemini_service.py`'s filename is legacy-only, see Notes below — there is no separate Gemini credential in this codebase.) |
| Last rotation date | Unknown (first register entry — v4.3, 2026-05-29) |
| Next rotation due | 2026-08-25 (90 days from first inventory entry in external_api_credential_inventory.md) |
| Notes | Configured on both production and staging (added to staging 2026-05-29 for QA verification — ST-06). Frontend feature flag uses `REACT_APP_ANTHROPIC_API_KEY=true` (build-time env var, set in Render frontend service). Legacy service file `backend/services/gemini_service.py` uses this key (filename retained for backward compatibility). Cost audit logging active via `claude_audit_log` table. Monthly threshold alert: $5.00 (`docs/ops/gemini_cost_tracking.md`). |

---

### 4. News API Key

| Field | Value |
|-------|-------|
| Key name | News API Key |
| Env var | `NEWS_API_KEY` |
| Purpose | Fetching financial news articles for ticker-specific news feed (`GET /news/{ticker}`) |
| Scope | Read-only — fetch news articles by query/ticker |
| Storage location | Render environment variables (staging and production services) |
| Rotation cadence | Annual minimum (12 months) |
| Rotation procedure | Follow general procedure in `docs/ops/api_key_rotation_policy.md`; adapt Steps 1–5 for the news API provider's dashboard |
| Last rotation date | Unknown (pre-register baseline) |
| Next rotation due | 12 months from last rotation |
| Notes | Free tier rate limits apply. Provider-specific dashboard for rotation. |

---

### 5. Supabase Database Connection String

| Field | Value |
|-------|-------|
| Key name | Supabase DB Connection String |
| Env var | `DATABASE_URL` |
| Purpose | PostgreSQL database connection for all backend services (positions, trades, signals, alerts, portfolio, AI audit logs) |
| Scope | Full database read/write access to the Supabase project |
| Storage location | Render environment variables (staging and production services — separate Supabase projects) |
| Rotation cadence | Emergency rotation only — no scheduled routine rotation |
| Rotation procedure | Generate new project password in Supabase dashboard → update `DATABASE_URL` in Render → verify `/health/detailed` → test DB-backed endpoints |
| Last rotation date | Not applicable (emergency-only) |
| Next rotation due | Not applicable |
| Notes | Connection string includes the password inline — treat entire string as a secret. Uses Supabase Supavisor Transaction Pooler (port 6543, `?pgbouncer=true&sslmode=require`) for connection pooling. Staging and production use separate Supabase projects; rotate independently. |

---

### 6. Application X-API-Key

| Field | Value |
|-------|-------|
| Key name | Application X-API-Key |
| Env var (backend/Render) | `API_KEY` — **as of 2026-08-04 (ST-06, BLG-SEC-27, EPIC-02, v8.2), staging and production hold two distinct, independently-revocable values.** Prior to this rotation, both services shared one value (a latent risk: a compromise or accidental log-leak of the staging key would also grant production access). Frontend build-time equivalent: `REACT_APP_API_KEY` (baked into the static bundle at build time — GH Pages for production via `.github/workflows/deploy.yml`, Render static site for staging). |
| Local storage variable name | `RENDER_API_KEY` in `~/.api_keys` (production value) — **note the naming mismatch**: despite the local variable being named `RENDER_API_KEY`, its value is the app-level `X-API-Key`, not a Render platform/service API key. Prior sessions incorrectly concluded no application key existed because they searched for a differently-named variable — this entry exists to prevent that recurrence (LP-08, v6.7 closure carry-forward). A separate, genuinely-distinct Render *platform management* API key (used for ST-06/ST-07 rotation and deploy diagnostics) is stored as `RENDER_PLATFORM_API_KEY` in the same file — do not confuse the two. |
| Purpose | Authenticates governed routines (roadmap, release planning, sprint execution) against the production API so gate conditions (e.g. SI-02 trade/trade-plan counts) can be confirmed directly via `GET` endpoints instead of relying on self-report |
| Scope | Full API access, subject to `api_key_middleware` (`backend/main.py`) — required on every request via `X-API-Key` header except `OPTIONS` and `GET /health`. Read-only in practice: governed routines only ever issue `GET` requests with this key. |
| Storage location | Render environment variable `API_KEY` on each service independently (production `srv-d5r98jm3jp1c73figm1g`; staging backend `srv-d6rtdg94tr6s73ce2j6g`; staging frontend `srv-d6rtdg94tr6s73ce2j60` as both `API_KEY` and `REACT_APP_API_KEY`); GitHub Actions repo secrets `API_KEY` and `REACT_APP_API_KEY` carry the production value (consumed by `alert-evaluation.yml`, `daily-snapshot.yml`, `backtest.yml`, `deploy.yml`); local copy of the production value in `~/.api_keys` as `RENDER_API_KEY` for use by governed-routine sessions. `.github/workflows/api-key-cross-environment-check.yml` additionally needs the *staging* value as a GitHub Actions repo secret named `STAGING_API_KEY` — **added 2026-08-08** (`gh secret list` confirms it present); the "human action required" note that previously lived here is resolved. **Live-confirmed running (ST-02, BLG-OPS-134, EPIC-01, v8.5, 2026-08-10):** inspected the 2026-08-09 scheduled run's actual log (not just the YAML source) — the check genuinely executes daily with real secrets, it is not silently skipping. That same run surfaced a different gap: a transient PROD_API_URL read timeout crashed the script with an unhandled exception, which the workflow's alert step could not distinguish from a genuine cross-wired-keys finding, producing a false-positive "keys cross-wired" Telegram alert. Hardened: `probe()` now catches network/timeout errors as a distinct `None`/`ERROR` outcome (never conflated with a real finding), and the missing-secrets skip-guard now fails loud (`::error::` + a distinct alert) instead of silently exiting 0. See `scripts/check_api_key_cross_environment.py` and the workflow file for the fix; `tests/test_api_key_cross_environment.py` covers the new error path. |
| Rotation cadence | Annual minimum (12 months), aligned with other keys in this register |
| Rotation procedure | Generate two new distinct values (staging, production) → update `API_KEY` on each Render service independently (and `REACT_APP_API_KEY` on the staging frontend) → trigger a redeploy on each service (env var changes made via the Render API do not auto-restart the running process) → update the `API_KEY`/`REACT_APP_API_KEY` GitHub Actions secrets to the new production value → trigger `deploy.yml` (`gh workflow run deploy.yml`) to rebuild the production frontend bundle with the new key before the old one is revoked, since the already-deployed GH Pages bundle has the old value baked in and would start failing auth otherwise → update `RENDER_API_KEY` in `~/.api_keys` → verify live: new values succeed, old shared value now returns 401 against production, and each new value fails against the *other* service (confirms genuine distinctness, not just a synchronized rotation) |
| Last rotation date | 2026-08-04 (ST-06, BLG-SEC-27, EPIC-02, v8.2) — first rotation since the key was originally provisioned; also the first time staging and production diverged to distinct values |
| Next rotation due | 2026-08-04 + 12 months |
| Notes | Confirmed working 2026-07-09 (ST-04, BLG-OPS-99, v6.8): `curl -H "X-API-Key: $RENDER_API_KEY" .../signals` → 200, used to directly confirm the SI-02 gate condition (`GET /trades` → `total_trades: 20`; `GET /trade-plans` → 11 plans, 0 with `position_id` set, pre-ST-01-fix baseline) rather than relying on self-report. See `docs/security/signal_anomaly_review_2026-07-09.md` for a second example use (ST-03). **2026-08-04 rotation:** live-verified via 6 direct checks — old shared key fails against production (401) and against staging (401); new production key succeeds against production (200) but fails against staging (401); new staging key succeeds against staging (200) but fails against production (401). Production's GH Pages frontend was rebuilt and redeployed (`gh workflow run deploy.yml`, run `30950208420`) immediately after the secret update to avoid a window where the live frontend's already-baked-in old key would have started failing auth against the rotated backend. |

---

### 7. Telegram Bot Token and Chat ID

| Field | Value |
|-------|-------|
| Key name | Telegram Bot Token / Chat ID |
| Env var | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| Purpose | Outbound-only alert and digest delivery (e.g. `POST /digest/si05/send`) via the Telegram Bot API |
| Scope | Send-message capability to a single fixed chat (`TELEGRAM_CHAT_ID`); no inbound webhook is configured, no read/admin Telegram calls exist in this codebase |
| Storage location | Render environment variables (staging and production services) |
| Rotation cadence | Annual minimum (12 months), aligned with other keys in this register |
| Rotation procedure | Revoke and regenerate token via @BotFather → update `TELEGRAM_BOT_TOKEN` in Render → verify with a manual `POST /digest/si05/send` test send |
| Last rotation date | Unknown (pre-register baseline) |
| Next rotation due | 12 months from last rotation |
| Notes | Identified as a gap during the ST-17 system threat model review (BLG-OPS-71, EPIC-03, v6.8) — this credential was already in production use (`backend/config.py:57-58`) but had never been added to this register. Bot token scope reviewed as minimal-permission (send-only) in `docs/security/security_register.md`; BotFather-side configuration itself was noted there as unverified. |

---

## Rotation Tracking

Update `last_rotated` above after every key rotation and commit with:
`[GOVERNANCE] <key name> rotated YYYY-MM-DD`

Cross-reference with `docs/ops/external_api_credential_inventory.md` — both files should reflect the same rotation date for each credential.

---

## Acceptance

- Accepted by: Cybersecurity & Trust Lead
- Date: 2026-05-29
