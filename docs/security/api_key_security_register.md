**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3 (ST-15 — BLG-GOV-50)

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
| Storage location | Render environment variables (production service only — staging excluded; see notes) |
| Rotation cadence | Annual minimum (12 months) |
| Rotation procedure | `docs/ops/api_key_rotation_policy.md §Anthropic API Key` |
| Last rotation date | Unknown (first register entry — v4.3, 2026-05-29) |
| Next rotation due | 2026-08-25 (90 days from first inventory entry in external_api_credential_inventory.md) |
| Notes | Not configured on staging (Anthropic API key absent from staging Render env — `ANTHROPIC_API_KEY` is production-only). Legacy service file `backend/services/gemini_service.py` uses this key (filename retained for backward compatibility). Cost audit logging active via `claude_audit_log` table. Monthly threshold alert: $5.00 (`docs/ops/gemini_cost_tracking.md`). |

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

## Rotation Tracking

Update `last_rotated` above after every key rotation and commit with:
`[GOVERNANCE] <key name> rotated YYYY-MM-DD`

Cross-reference with `docs/ops/external_api_credential_inventory.md` — both files should reflect the same rotation date for each credential.

---

## Acceptance

- Accepted by: Cybersecurity & Trust Lead
- Date: 2026-05-29
