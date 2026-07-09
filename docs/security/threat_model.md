**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Class:** Class 2 (Reference Document / Security Policy)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-09
**Story:** ST-17 (BLG-OPS-71, EPIC-03, v6.8)

---

# System Threat Model — Momentum Trading Assistant

## Purpose

This document identifies the system's attack surfaces, classifies its data by sensitivity, names the realistic threat actors, records the mitigations already in place, and lists the gaps found during this review with their tracking references. It satisfies BLG-OPS-71 AC-01–AC-03.

**Scope note:** This is a single-user, personal trading decision-support tool, not a multi-tenant SaaS product. The threat model is calibrated accordingly — the realistic threat actor set and acceptable-risk bar differ materially from a public-facing consumer product.

---

## 1. System Overview

FastAPI backend (Render) + React SPA frontend (Render static site) + Supabase-hosted Postgres (via Supavisor pooler). No user accounts or session system — single static API key gates all write/read access. External integrations: Alpaca (paper/live trading data and order placement), Anthropic Claude (AI briefing/chat/thesis — advisory-only, never auto-executing, per the system's §13 boundary in `claude/strategy/strategy_rules.md`), Yahoo Finance (market data, unauthenticated public API), a news API, and Telegram (outbound alert delivery only).

---

## 2. Attack Surfaces

| Surface | Description | Auth coverage |
|---|---|---|
| Public REST API (`backend/main.py` + routers) | ~85 endpoints across positions, trades, signals, portfolio, analytics, AI, digest | Global `api_key_middleware` requires `X-API-Key` on every route except `OPTIONS` and `GET /health`. `POST /digest/si05/send` additionally carries an explicit `Depends(_verify_api_key)` (`backend/routers/digest.py:240`) — confirmed fixed (BLG-BE-35, shipped v5.3 ST-08); no open auth gap on this endpoint. |
| React SPA (static assets) | Public, served from Render static hosting | No auth at the CDN/static level (expected — the SPA itself calls the authenticated API); CSP configured in `public/index.html` restricts script/style/connect sources, but permits `'unsafe-inline'` for `script-src`/`style-src` — see §5, BLG-SEC-12 (new). |
| Supabase Postgres | All application state | Reached only via `DATABASE_URL` (Supavisor pooler, `sslmode=require`); not directly internet-exposed outside the backend's connection. |
| Alpaca API | Trading data + order placement (paper and, per credential scope, potentially live) | `APCA_API_KEY_ID`/`APCA_API_SECRET_KEY`, Render env vars. |
| Anthropic Claude API | AI briefing/chat/thesis generation | `ANTHROPIC_API_KEY`, Render env var; cannot be scope-restricted at the Anthropic platform level (confirmed in `docs/security/anthropic_api_key_scope_review.md`) — app-level cost audit logging (`claude_audit_log`) is the primary compensating control. |
| Yahoo Finance (yfinance) | Historical OHLCV / price data | No credential — public data source; risk is availability/data-integrity, not confidentiality. |
| News API | Ticker news headlines | `NEWS_API_KEY`, read-only scope. |
| Telegram Bot API | Outbound-only alert/digest delivery | `TELEGRAM_BOT_TOKEN` + fixed `TELEGRAM_CHAT_ID`; no inbound webhook configured — confirmed no read/admin Telegram calls exist in `si05_digest_service.py`. |
| CI/CD (GitHub Actions) | Deploys to Render, runs secret-scanning, dependency audits | GitHub-native auth; secrets stored as GitHub Actions secrets, not in the repo. |
| Render environment variables | Holds all 7 inventoried credentials (see `docs/security/api_key_security_register.md`, updated to add the Telegram entry as part of this review) | Render account access is the single point of credential exposure if compromised. |

---

## 3. Data Classification

| Data | Sensitivity | Notes |
|---|---|---|
| API keys / secrets (`API_KEY`, `APCA_*`, `ANTHROPIC_API_KEY`, `DATABASE_URL`, `NEWS_API_KEY`, `TELEGRAM_BOT_TOKEN`) | **CRITICAL** | Direct financial/billing exposure if leaked (Alpaca = real trading capability if a live key is ever used; Anthropic/News = billing exposure). Inventoried in `api_key_security_register.md`. |
| Position data, stop levels, P&L, cash balances | **HIGH** | Financial data; no PII attached (confirmed no name/email/IP columns exist anywhere in the schema per `red_flag_journal_security_review.md` §2), but reveals real trading capital and strategy performance. |
| Trade plan private fields (`setup_thesis`, `entry_rationale`, `stop_level`, `r_target`, `early_exit_conditions`) | **HIGH** | Classified as proprietary strategy IP in `docs/specs/security/trade_plan_data_sensitivity.md`, which is the canonical tiering document for this data (Public/Internal/Private) — this threat model defers to it rather than duplicating its tiers. |
| Signals, screener results, market regime data | **MEDIUM** | Derived from public market data; sensitive mainly as a signal of what the system is watching, not independently exploitable. |
| Settings / user preferences | **MEDIUM** | Configuration only, no credentials embedded. |
| AI audit logs (`claude_audit_log`, `gemini_audit_log`) | **MEDIUM** | Token counts, cost, model IDs, prompt version — no raw prompt/response text stored (confirmed: `claude_audit_log` schema is metadata-only, no summary/response text column). |

---

## 4. Threat Actors

| Actor | Motivation | Realistic capability against this system |
|---|---|---|
| External web attacker | Opportunistic scanning, credential theft, or targeted attack if the app's existence becomes known | Must obtain the API key to do anything beyond hitting `GET /health` or the unauthenticated digest endpoint (§5). No brute-forceable login form exists to attack. Primary vector would be credential leakage (e.g., accidental commit, log exposure) rather than direct exploitation of the API itself. |
| Compromised dependency (supply chain) | Malicious or compromised npm/PyPI package exfiltrating secrets or injecting code | Mitigated by CI dependency audits (`pip-audit`, `npm audit`) tracked in `security_register.md`; residual risk exists between audit cycles — see the standing gate-conditional dependency-review backlog item (quarterly cadence or CVE-triggered). |
| Accidental exposure (self) | Operator/engine error — committing a secret, verbose error responses leaking internals, misconfigured CSP | The most realistic actor for a single-user system. Addressed partially (CI secret-scanning gate exists per `security_register.md`); §5 identifies two residual gaps in this category (verbose error detail, CSP `unsafe-inline`). |
| AI prompt injection (via ticker/market/user-supplied text reaching the LLM context) | Manipulate AI output or exfiltrate context via crafted input | Formally threat-modelled in `docs/specs/security/ai_injection_risk_assessment.md`. Both risks identified there (`context_opts.ticker` injection, signal ticker/market injection) are closed — fixed via BLG-SEC-01 and BLG-SEC-02 respectively. §13 architectural boundary (advisory-only, no auto-execution) caps the blast radius of any successful injection to misleading text output, not unauthorized trades. |

---

## 5. Current Mitigations

- **Authentication:** Global `X-API-Key` middleware (`backend/main.py`) on all routes except `OPTIONS`/`GET /health`.
- **Input sanitization:** `_sanitize_signal_string()` (`database.py:584`) restricts ticker/market strings to `[A-Za-z0-9.\-/:]`, applied at all signal write paths.
- **SQL column allowlisting:** `SIGNAL_UPDATABLE_COLUMNS` frozenset (`database.py:664`) — `update_signal()` raises on any key outside the allowlist; `PATCH /signals/{id}` (`main.py`) pre-validates the same allowlist before building the query. **Fixed this same sprint** (EPIC-01 ST-02, BLG-SEC-08, v6.8) — closes what was previously an open structural SQL-construction risk.
- **Rate limiting:** Per-IP sliding-window limiter on AI endpoints (`POST /ai/daily-briefing` 10/min, `POST /ai/chat` 30/min) — the two endpoints with real per-call cost exposure.
- **CSP:** Configured in `public/index.html` (`default-src 'self'`, `connect-src 'self' https:`, etc.).
- **AI injection controls:** `context_opts.ticker` sanitization (BLG-SEC-01) and signal ticker/market validation (BLG-SEC-02), both fixed.
- **§13 architectural boundary:** AI-generated content is advisory-only and cannot trigger trade execution, capping the impact of any AI-side compromise.
- **CI secret-scanning gate + dependency audits:** pip-audit and npm audit run in CI; results tracked in `security_register.md`.
- **Data minimization:** No PII stored anywhere in the schema; AI audit logs are metadata-only (no raw prompt/response text retained).

---

## 6. Gaps Identified

| Gap | Severity | Status |
|---|---|---|
| `update_signal`/`PATCH /signals/{id}` unvalidated SQL column keys | — | **Resolved this sprint** — EPIC-01 ST-02, BLG-SEC-08 |
| AI rate-limit bypass not yet load-tested | P3 | **Already tracked** — BLG-SEC-09 (open) |
| API key rotation runbook never exercised end-to-end | P3 | **Already tracked** — BLG-SEC-11 (open) |
| CSP permits `'unsafe-inline'` for `script-src` and `style-src`, weakening XSS mitigation on the SPA | P3 | **New — filed as BLG-SEC-12** |
| 44 call sites in `backend/main.py` return raw Python exception text (`detail=str(e)`) directly in API error responses, risking incidental disclosure of internal paths, schema hints, or library details to any caller holding the API key | P3 | **New — filed as BLG-SEC-13** |
| `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` was in live production use (`backend/config.py:57-58`) but absent from `api_key_security_register.md`'s credential inventory | — | **Fixed during this review** — register entry #7 added, version 1.3→1.4 |

No CRITICAL or HIGH-severity gaps were found unresolved at the close of this review — the one CRITICAL-adjacent item found open at review start (BLG-SEC-08) was resolved earlier in this same sprint.

---

## 7. Sign-Off

```
ST-17 (BLG-OPS-71, EPIC-03, v6.8) — System Threat Model Sign-Off

Reviewed: docs/security/threat_model.md v1.0

Cybersecurity & Trust Lead: Approved (agent-mediated, retry 1 — corrected a stale
  claim that POST /digest/si05/send lacked API-key auth; confirmed fixed v5.3 ST-08) — 2026-07-09
Infrastructure & Operations Owner: Approved (agent-mediated, retry 1 — required
  adding TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID to api_key_security_register.md,
  which was missing a live production credential) — 2026-07-09
```
