**Owner:** PMO Lead
**Class:** Supporting Document (Class 2) — Living Reference
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-06
**Source:** BLG-GOV-18 (v3.2 ST-16)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# External API Dependency Risk Register

**Purpose:** Lightweight risk register for all production external API dependencies. Covers endpoints used, reliability record, known failure modes, fallback behaviour, and tier/plan details.

**Maintenance Obligation:** This document is a mandatory living reference. Updating it is a required step whenever a new external API dependency is introduced or an existing dependency changes (tier, endpoints, failure modes). This update obligation is referenced in the OPERATIONAL_GUIDE rebalance checklist (see OPERATIONAL_GUIDE §12 or equivalent section).

---

## 1. Alpaca Markets API

| Field | Detail |
|-------|--------|
| **Service** | Alpaca Markets |
| **Purpose** | Market data (price quotes, historical bars, news headlines), paper trading execution |
| **API Tier** | Unlimited (free tier — delayed data) / Live trading requires funded account |
| **Base URL** | `https://data.alpaca.markets` (data); `https://paper-api.alpaca.markets` (paper trading) |
| **Authentication** | `APCA-API-KEY-ID` + `APCA-API-SECRET-KEY` headers |
| **Credentials** | See `docs/operations/credential_policy.md` |
| **Endpoints in use** | Latest bar quotes (pricing), historical bars, news headlines |
| **Rate limits** | Free tier: 200 calls/min (data); subject to change by Alpaca |
| **Current reliability** | Generally stable; occasional 429 rate-limit errors during batch scans |
| **Known failure modes** | (1) 429 Too Many Requests during screener runs — handled via `PRICE_FETCH_DELAY_SECONDS = 0.3` delay; (2) null bars returned for low-liquidity/UK tickers — handled in `utils/pricing.py` with explicit null check; (3) API key expiry — no automatic renewal |
| **Fallback behaviour** | On fetch failure: screener skips the affected ticker; pricing falls back to last cached value if available; UK FX rate falls back to `DEFAULT_FX_RATE = 1.27` |
| **Risk level** | Medium — core data provider; no secondary real-time price source |
| **Renewal / monitoring** | Alpaca dashboard. Check monthly for tier changes or TOS updates. |

---

## 2. Yahoo Finance (yfinance)

| Field | Detail |
|-------|--------|
| **Service** | Yahoo Finance via `yfinance` Python library |
| **Purpose** | Historical price data for analytics, market regime signals (SPY, FTSE proxies), supplementary ticker data |
| **API Tier** | Unofficial / public API (no formal agreement) — accessed via `yfinance` library |
| **Authentication** | None (public) |
| **Credentials** | None required |
| **Endpoints in use** | `yfinance.Ticker.history()` for historical OHLCV; `yfinance.download()` for batch |
| **Rate limits** | Unofficial — approximately 2,000 requests/hour before throttling; no formal SLA |
| **Current reliability** | Unreliable: Yahoo Finance periodically changes its API endpoints (breaking `yfinance`), especially after Yahoo product updates. The `yfinance` library typically releases a patch within days |
| **Known failure modes** | (1) `yfinance` library breaks after Yahoo API changes — fix: upgrade `yfinance` version; (2) Rate limiting (429) for large batch downloads — fix: add delays; (3) Missing/incorrect data for UK tickers in pence (GBp) — handled via `PENCE_TO_POUNDS_THRESHOLD` conversion |
| **Fallback behaviour** | On `yfinance` failure: screener returns empty results; analytics show stale data until data is re-fetched |
| **Risk level** | High — no formal SLA, unofficial API, historically breaks 2–3 times per year |
| **Mitigation** | Pin `yfinance` version in `requirements.txt`; monitor for library updates when data fetch errors spike |
| **Renewal / monitoring** | Monitor GitHub releases for `yfinance`. No formal renewal — purely library-based |

---

## 3. Anthropic Claude API

| Field | Detail |
|-------|--------|
| **Service** | Anthropic Claude API |
| **Purpose** | AI-generated weekly digest commentary, live trading assistant responses |
| **API Tier** | Pay-per-token (API key billing) |
| **Base URL** | `https://api.anthropic.com` |
| **Authentication** | `x-api-key` header — `ANTHROPIC_API_KEY` env var |
| **Credentials** | See `docs/operations/credential_policy.md` |
| **Model in use** | `claude-haiku-4-5-20251001` (digest); model may vary for live assistant |
| **Endpoints in use** | `POST /v1/messages` |
| **Rate limits** | Tier-dependent; typical developer tier: 5 RPM, 10K TPM (see Anthropic dashboard) |
| **Current reliability** | High — Anthropic maintains strong uptime SLA for API; occasional brief outages |
| **Known failure modes** | (1) Rate limit exceeded during batch runs — mitigated by single digest call design; (2) API key expiry or billing limit reached — app falls back gracefully (digest shows placeholder text) |
| **Fallback behaviour** | On failure: weekly digest AI section skipped with informational message; live assistant returns error to user |
| **Risk level** | Low — supplemental feature; no core trading logic depends on it |
| **Renewal / monitoring** | Anthropic console — monitor billing. Rotate key annually per credential_policy.md |

---

## 4. Telegram Bot API

| Field | Detail |
|-------|--------|
| **Service** | Telegram Bot API |
| **Purpose** | Alert delivery (price threshold alerts, system notifications) |
| **API Tier** | Free (Telegram Bot API has no tiers) |
| **Base URL** | `https://api.telegram.org/bot{token}/sendMessage` |
| **Authentication** | Bot token in URL — `TELEGRAM_BOT_TOKEN` env var |
| **Credentials** | See `docs/operations/credential_policy.md` |
| **Endpoints in use** | `sendMessage` |
| **Rate limits** | 30 messages/second to different chats; 1 message/second to same chat |
| **Current reliability** | High — Telegram API is stable |
| **Known failure modes** | (1) Bot blocked by user — message silently fails; (2) Chat ID invalid — returns 400; (3) Network timeout — alert dropped silently |
| **Fallback behaviour** | Alert delivery failure is logged but not retried; alerts are best-effort |
| **Risk level** | Low — alert delivery only; no core function depends on it |
| **Renewal / monitoring** | No expiry. Monitor via `@BotFather` on Telegram |

---

## Risk Summary

| API | Risk Level | Primary Concern |
|-----|-----------|----------------|
| Alpaca Markets | Medium | No secondary price source; key expiry not auto-renewed |
| Yahoo Finance | High | Unofficial API; breaks on Yahoo changes 2–3× per year |
| Anthropic Claude | Low | Supplemental; billing cap is main risk |
| Telegram Bot | Low | Best-effort delivery; no retry |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-06 | Initial risk register. v3.2 ST-16 (BLG-GOV-18). Covers all 4 production external API dependencies at v3.2. |
