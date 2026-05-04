**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-30
**Cycle:** 2026-04-29__release-v3.1 (ST-12)

---

# External API Credential Inventory

## Purpose

This document is the authoritative inventory of all external API credentials used by the Momentum Trading Assistant. No sensitive values (keys, secrets, tokens) are stored here. This document records credential metadata only — the credential's purpose, storage location, and rotation status.

> **Security note:** If you find a key or secret value in this file, that is a security incident. Remove it immediately and rotate the credential.

---

## Inventory

### 1. Alpaca API Key

| Field | Value |
|-------|-------|
| Service | Alpaca Markets |
| Purpose | Live and paper trading operations; real-time market data (prices, bars) |
| Credential type | API Key + Secret pair |
| Scope | Paper Trading or Live Trading (whichever is active) — read positions, place/cancel orders, stream prices |
| Storage location | Render environment variables: `ALPACA_API_KEY` (key ID) and `ALPACA_API_SECRET` (secret) |
| Rotation policy | `docs/ops/alpaca_key_rotation_policy.md` — every 90 days or on suspected compromise |
| Last rotated | Unknown (pre-inventory baseline) |
| Rotation due | 90 days from last rotation |
| Notes | Secret is shown only once at generation in Alpaca dashboard. If secret is lost, generate a new key pair. |

---

### 2. News API Key

| Field | Value |
|-------|-------|
| Service | News API (newsapi.org or equivalent) |
| Purpose | Fetching financial news articles for ticker-specific news feed (`GET /news/{ticker}`) |
| Credential type | API Key |
| Scope | Read-only — fetch news articles by query/ticker |
| Storage location | Render environment variable: `NEWS_API_KEY` |
| Rotation policy | Rotate every 90 days or on suspected compromise. Follow the same step-by-step structure as `alpaca_key_rotation_policy.md` (Steps 1–5, adapted for the news API provider's dashboard) |
| Last rotated | Unknown (pre-inventory baseline) |
| Rotation due | 90 days from last rotation |
| Notes | Free tier rate limits apply. Key is provider-specific — check provider dashboard for rotation procedure. |

---

## Rotation Tracking

Update the `last_rotated` field in this inventory after every key rotation and commit with message:
`[GOVERNANCE] <service> API key rotated YYYY-MM-DD`

---

## Acceptance

- Accepted by: Cybersecurity & Trust Lead
- Date: 2026-04-30
