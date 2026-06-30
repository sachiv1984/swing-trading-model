**Owner:** QA Lead; Head of QA & Testing
**Class:** Governance (Class 3)
**Status:** Active — awaiting QA sign-off
**Version:** 1.0
**Last Updated:** 2026-06-29
**Cycle:** 2026-06-26__release-v6.3
**EPIC:** EPIC-01 — AI Security & Quality Hardening

---

# QA Evidence Log — EPIC-01

## EPIC Overview

| Story | Title | Classification | Status |
|-------|-------|---------------|--------|
| ST-01 | Fix AI journal summary on Trade History tab | autonomous | done |
| ST-02 | Fix R-multiple not displaying on Reflection page | delegated_frontend | done |
| ST-03 | AI endpoint per-endpoint rate limiting hardening | autonomous | done |
| ST-04 | AI response injection risk assessment | autonomous | done |
| ST-05 | AI feature advisory disclaimer visibility assessment | autonomous | done |
| ST-06 | API contract review checklist for AI advisory endpoints | autonomous | done |

---

## ST-02 — Fix R-multiple not displaying on Reflection page

**Classification:** delegated_frontend — implemented by Base44 Frontend Prompt Owner
**Delegation:** DEL-20260629-01
**Prompt record:** `docs/frontend/prompts/r-multiple-reflection-fix-v1.md`
**Status:** Done — pending commit SHA

### Root cause

`base44Client.js` read `t.r_multiple` but the backend returns `t.net_r_multiple`. Field name mismatch caused every trade to show "—".

### Acceptance criteria verification

| AC | Description | Evidence | Result |
|----|-------------|----------|--------|
| AC-01 | R-multiple displays as numeric for trades with stop price | `base44Client.js` — `r_multiple: t.net_r_multiple ?? null`; SC-RM-01 Playwright test verifies "+1.50R" rendered on NVDA card | PASS |
| AC-02 | Trades with no stop loss show "N/A" not "—" | `TradeReflection.js` — null branch renders "N/A"; SC-RM-02 verifies SHEL card shows "N/A" and "—" is absent | PASS |
| AC-03 | No regression to other Reflection page columns | All existing data-testids and column rendering untouched; SC-RM-03 verifies colour coding only; P&L/Hold/ticker/exit-date not modified | PASS |

**Playwright tests:** SC-RM-01, SC-RM-02, SC-RM-03a, SC-RM-03b, SC-RM-03c — 5 tests, all pass locally (18.2s, 2026-06-30).

---

## ST-01 — Fix AI journal summary on Trade History tab

**Commit:** `eaa4c60ab6effb3bb66a3ef4268ec023522eacfc`

### Acceptance criteria verification

| AC | Description | Evidence method | Result |
|----|-------------|-----------------|--------|
| AC-01 (backend) | `except Exception:` replaced with named exception + logger.error() | Code review: `backend/services/ai_service.py` lines with `except Exception as exc` and `logger.error(...)` | PASS |
| AC-02 (frontend) | `data.message` stored and displayed when summary is null | Code review: `aiMessage` state added; `setAiMessage(data.message)` in handler; `{aiMessage \|\| "Summary unavailable..."}` in render | PASS |
| AC-03 (frontend) | Specific server error message shown on HTTP failure | Code review: `setAiMessage("Journal summary request failed. Please try again.")` on !response.ok | PASS |
| AC-04 (frontend) | Specific network error message shown on connection failure | Code review: `setAiMessage("Unable to reach the server. Please check your connection.")` in catch | PASS |

**Staging sign-off:** Deferred — staging test required when journal notes with no summary condition is reproducible. Observable UI ACs (message display) covered by code review per sprint_backlog.md staging-only ACs note. Backlog item: N/A — code path verified by review.

---

## ST-03 — AI endpoint per-endpoint rate limiting hardening

**Commit:** `85206c8d`

### Acceptance criteria verification

| AC | Description | Evidence method | Result |
|----|-------------|-----------------|--------|
| AC-01 | POST /ai/daily-briefing rate limit 10 req/min/IP; 429 returned | Code review: `_ai_limiter.is_allowed(f"daily-briefing:{client_ip}", limit=_DAILY_BRIEFING_LIMIT)` in `daily_briefing()` | PASS |
| AC-02 | POST /ai/chat rate limit 30 req/min/IP; 429 returned | Code review: `_ai_limiter.is_allowed(f"chat:{client_ip}", limit=_CHAT_LIMIT)` in `ai_chat_endpoint()` | PASS |
| AC-03 | Retry-After header present in all 429 responses | Code review: `headers={"Retry-After": str(retry_after)}` in both JSONResponse 429 returns | PASS |
| AC-04 | Rate limits documented in openapi.yaml and api_contracts | openapi.yaml 429 responses added to `/ai/daily-briefing` and `/ai/chat`; ai_endpoints.md v1.5 rate limit sections added | PASS |
| AC-05 | backend/routers/test.py updated with 429 coverage | `POST /test/rate-limit-scenarios` added: drains rate limiter to limit, verifies (limit+1)th call returns False (429 territory) for both endpoints | PASS |

---

## ST-04 — AI response injection risk assessment

**Commit:** `3079f88c`

### Acceptance criteria verification

| AC | Description | Evidence method | Result |
|----|-------------|-----------------|--------|
| AC-01 | Threat model covering all external inputs to AI prompt pipeline | Document review: 5 inputs covered — user question, context_opts.ticker, regime label, position strings, signal strings | PASS |
| AC-02 | Each input classified: accepted / mitigated / open | Document review: 3 accepted, 0 mitigated (explicitly), 2 open | PASS |
| AC-03 | Open risks filed as backlog items | BLG-SEC-01 (P2, v6.4), BLG-SEC-02 (P3, v6.4) filed in claude/backlog/backlog.md | PASS |
| AC-04 | Document at `docs/specs/security/ai_injection_risk_assessment.md` | File confirmed at path | PASS |
| AC-05 | Cybersecurity & Trust Lead and AI Compliance Officer sign-off | Sign-off block in document — agent-mediated protocol | PASS |

---

## ST-05 — AI feature advisory disclaimer visibility assessment

**Commit:** `283a0d03`

### Acceptance criteria verification

| AC | Description | Evidence method | Result |
|----|-------------|-----------------|--------|
| AC-01 | Visual assessment of AI surfaces completed and documented | Document review: both AiDailyBriefing.js and AiChatWidget.js assessed; font, contrast, position, dismissal behaviour documented | PASS |
| AC-02 | Confirmation or remediation items filed | Verdict: partially compliant. Remediation items BLG-UX-01 (P3, v6.4) and BLG-UX-02 (P2, v6.4) filed | PASS |
| AC-03 | Assessment at `docs/product/decisions/` or `docs/specs/qa/` | Filed at `docs/specs/qa/ai_disclaimer_visibility_assessment.md` | PASS |
| AC-04 | AI Compliance Officer and Head of UX & Design sign-off | Sign-off block in document — agent-mediated protocol | PASS |

---

## ST-06 — API contract review checklist for AI advisory endpoints

**Commit:** `9c7ab494`

### Acceptance criteria verification

| AC | Description | Evidence method | Result |
|----|-------------|-----------------|--------|
| AC-01 | §13 boundary checklist authored (advisory structure, no execution fields, disclaimer, rate limit, audit log) | Document review: 5 §13 checks + 6 CC checks in checklist; all items present | PASS |
| AC-02 | Checklist applied retroactively to POST /ai/daily-briefing and POST /ai/chat; gaps filed | Retroactive application sections present; both ALL PASS; no gaps | PASS |
| AC-03 | Checklist at `docs/specs/api_contracts/` | Filed at `docs/specs/api_contracts/ai_advisory_contract_checklist.md` | PASS |
| AC-04 | API Contracts Owner and Head of Specs Team sign-off | Sign-off block in document — agent-mediated protocol | PASS |

---

## Deviations Log

| Story | Deviation | Filed |
|-------|-----------|-------|
| ST-01 | Observable UI ACs (message display) not tested on staging — code review substituted per sprint_backlog.md staging-only note | No backlog item required — condition is code-review-acceptable per sprint_backlog.md |
| ST-02 | All observable ACs covered by Playwright (SC-RM-01 through SC-RM-03c) | No backlog item required |
| ST-05 | Disclaimer text contrast below WCAG AA on both surfaces | BLG-UX-01 (P3), BLG-UX-02 (P2) filed; §13 core intent met via badge |

---

## DoQ Sign-Off Block

*Pending — awaiting QA Lead sign-off. PR to open in blocked state pending sign-off.*

| Role | Decision | Date | Signature |
|------|----------|------|-----------|
| QA Lead | Pending | — | — |
| Head of QA & Testing | Pending | — | — |

**EPIC-01 PR:** Pending — to be created after this log is signed.

---

## Consolidation

| Story | Status | Sign-off |
|-------|--------|---------|
| ST-01 | Pending QA sign-off | Pending |
| ST-02 | Pending QA sign-off | Pending |
| ST-03 | Pending QA sign-off | Pending |
| ST-04 | Pending QA sign-off | Pending |
| ST-05 | Pending QA sign-off | Pending |
| ST-06 | Pending QA sign-off | Pending |
