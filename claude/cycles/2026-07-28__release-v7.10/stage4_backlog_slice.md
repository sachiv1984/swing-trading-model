Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-28
Cycle: 2026-07-28__release-v7.10
Release: v7.10

# Backlog Slice — v7.10

<!-- release-plan-marker: RP:v7.10:2026-07-28__release-v7.10 -->

23 stories across 6 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution).

---

## EPIC-01 — Backend Reliability & Error-Handling Hardening

**Maps to:** S2-01, S2-02, S2-03, S2-04
**Owner:** Backend Engineering Patterns Owner; Head of Backend Engineering

### ST-01 — Fix errors masked as HTTP 200 in portfolio_risk.py
**Source:** BLG-BE-68
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- All four `portfolio_risk.py` endpoints (`/drawdown-status`, `/concentration-status`, `/sector-weights`, `/gate-metrics`) return HTTP 500 with the canonical `{status, message}` envelope on internal error
- Existing 200-path success shapes unchanged
- Regression test confirms the error path no longer returns HTTP 200

### ST-02 — Extend Alpaca backoff audit (BLG-BE-57) to Yahoo Finance, Gemini, and Claude call sites
**Source:** BLG-BE-75
**Effort:** M
**Acceptance Criteria:**
- All 4 providers' call sites confirmed to use the shared retry/backoff decorator (BLG-BE-71) or have a documented exception
- Backend Engineering Patterns Owner sign-off

### ST-03 — Idempotency key pattern for state-mutating POST endpoints
**Source:** BLG-BE-76
**Effort:** M
**Acceptance Criteria:**
- Idempotency-key pattern documented in `backend_engineering_patterns.md`
- Applied to at least the trade-entry and trade-plan-creation endpoints, additive/opt-in only (client-supplied key) — no change to existing behaviour when the key is absent (see RISK-02)
- Backend Engineering Patterns Owner sign-off

### ST-04 — Deprecated table read-path audit
**Source:** BLG-BE-41
**Effort:** S (~1 day)
**Acceptance Criteria:**
- Audit completed across all `database.py` read functions, cross-checked against `data_model.md` migration history for tables marked deprecated
- Findings documented; any additional deprecated-table reads filed as P0/P1 correctness items per severity
- Head of Backend Engineering sign-off

---

## EPIC-02 — Security Hardening

**Maps to:** S2-05, S2-06, S2-07, S2-08
**Owner:** Cybersecurity & Trust Lead; Head of Engineering

### ST-05 — Secrets-scanning pre-commit/CI gate (gitleaks/trufflehog)
**Source:** BLG-SEC-22
**Effort:** S
**Acceptance Criteria:**
- Local pre-commit hook added (`.githooks/pre-commit`) running a secrets scanner (gitleaks or trufflehog), complementing the existing CI-level gate (BLG-OPS-58)
- Confirmed to catch a deliberately-planted test secret
- Cybersecurity & Trust Lead sign-off

### ST-06 — AI rate-limit bypass test
**Source:** BLG-SEC-09
**Effort:** S (~1 day)
**Acceptance Criteria:**
- Bypass test performed against both rate-limited AI endpoints (daily-briefing, chat) via IP-rotation and X-Forwarded-For header spoofing attempts
- Findings documented; any confirmed bypass filed as a P1/P0 security item
- Cybersecurity & Trust Lead sign-off

### ST-07 — Rate-limit audit on public-facing endpoints ahead of any future auth changes
**Source:** BLG-SEC-18
**Effort:** M
**Acceptance Criteria:**
- Audit of current rate-limiting posture (Render platform-level and application-level) against all public-facing endpoints, documented
- Any gaps filed as follow-up `BLG-SEC-*` items; no implementation required unless a P0/P1 gap is found

### ST-08 — Raw exception text returned in API error responses
**Source:** BLG-SEC-13
**Effort:** M (~1-2 days — touches 44 call sites in backend/main.py)
**Acceptance Criteria:**
- 500-class error responses no longer include raw exception text in the client-facing `detail` field; generic message substituted
- Full exception detail still logged server-side for debugging
- No change to intentional, safe 4xx error messages (see RISK-03 — QA to spot-check a 4xx sample)

---

## EPIC-03 — QA & Test Infrastructure Hardening

**Maps to:** S2-09, S2-10, S2-11, S2-12
**Owner:** QA Lead; QA & Testing Owner; API Contracts & Documentation Owner

### ST-09 — Serve production build for Playwright E2E webServer instead of CRA dev server
**Source:** BLG-QA-127
**Effort:** M (~1-2 days)
**Acceptance Criteria:**
- CI E2E job builds (`npm run build`) and serves a production bundle instead of the CRA dev server, with `REACT_APP_*` vars injected at build time
- A static-serve dependency (`serve` or `http-server`) added and pinned
- `playwright.config.js` `webServer.command` is CI-conditional (production serve in CI, `npm start` for local dev/live-reload)
- Full 677-test suite passes against the production-served build in CI before merging (see RISK-04)

### ST-10 — Red Flag Journal auth regression test
**Source:** BLG-QA-96
**Effort:** S
**Acceptance Criteria:**
- Auth-required regression test (401/403 on missing/invalid `X-API-Key`) added to `backend/routers/test.py` for `GET /portfolio/red-flag-journal`
- Passes in CI; fails if auth check is removed (verified by temporarily removing it locally)

### ST-11 — Endpoint test suite coverage audit against all backend/routers/ files
**Source:** BLG-QA-133
**Effort:** M
**Acceptance Criteria:**
- Audit of `backend/routers/test.py` coverage against every `@router.*` decorator across all router files
- Any coverage gap found is filed or fixed
- QA & Testing Owner sign-off

### ST-12 — Consumer-driven contract check: frontend API calls vs documented contracts
**Source:** BLG-QA-128
**Effort:** M
**Acceptance Criteria:**
- Lightweight consumer-driven contract check implemented (CI or scripted) comparing frontend API call sites against the documented contract fields they consume
- First run's findings triaged
- API Contracts & Documentation Owner sign-off

---

## EPIC-04 — API Contract & Spec Debt Cleanup

**Maps to:** S2-13, S2-14, S2-15, S2-16
**Owner:** API Contracts & Documentation Owner

### ST-13 — `position_endpoints.md` envelope claim doesn't match live `GET /positions` behaviour
**Source:** BLG-SPEC-102
**Effort:** XS
**Acceptance Criteria:**
- `position_endpoints.md` corrected to document the actual (unenveloped) response shape for `GET /positions`
- API Contracts & Documentation Owner sign-off; no functional change

### ST-14 — `GET /positions` undocumented lifecycle fields
**Source:** BLG-SPEC-103
**Effort:** XS
**Acceptance Criteria:**
- All 3 fields (`position_state`, `state_entered_at`, `days_in_state`) added to `position_endpoints.md`'s response schema with type/description
- API Contracts & Documentation Owner sign-off; no functional change

### ST-15 — `trade_endpoints.md` JSON example omits documented fields
**Source:** BLG-SPEC-104
**Effort:** XS
**Acceptance Criteria:**
- JSON example updated to include `commission_gbp`, `spread_cost_gbp`, `net_r_multiple`
- API Contracts & Documentation Owner sign-off; no functional change

### ST-16 — OpenAPI contract linter in CI for heading-level drift
**Source:** BLG-GOV-243
**Effort:** M
**Acceptance Criteria:**
- Existing OpenAPI Drift Detection CI job extended to emit a specific, actionable error message when a `docs/specs/api_contracts/` heading is found at the wrong level (`###`+ instead of `##`), distinct from the generic "endpoint missing from contract" failure
- Confirmed via a test PR with a deliberately mis-leveled heading

---

## EPIC-05 — Frontend Technical Debt & Accessibility

**Maps to:** S2-17, S2-18, S2-19, S2-20
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design; Head of Engineering

**Staging-only ACs:** ST-19 and ST-17 carry observable UI rendering ACs — see RISK-01; Design Gate PASS or Playwright coverage/staging sign-off required before these ACs may be considered met (per CLAUDE.md §2).

### ST-17 — Rewrite calendar.js against the react-day-picker v9+ API
**Source:** BLG-FE-122
**Effort:** S
**Acceptance Criteria:**
- `calendar.js`'s `classNames` map and icon override rewritten against the `react-day-picker` v9+ API (`Chevron` replaces `IconLeft`/`IconRight`; renamed classNames keys)
- Renders correctly, spot-checked (component currently has zero live consumers — pre-staged for EPIC-05/BLG-FE-118; visual output preserved once a consumer exists)
- **Staging-only AC:** visual rendering spot-check — Playwright coverage or recorded staging sign-off required

### ST-18 — `SystemStatus.js` `categorizeEndpoint()` missing branches
**Source:** BLG-FE-123
**Effort:** XS
**Acceptance Criteria:**
- `includes()` branches added for `/price-alerts`, `/saved-filters`, and `/changelog`, grouped under the appropriate existing category consistent with the function's existing pattern
- No change to any other categorisation

### ST-19 — Consolidate StrategyBenchmark.js page header onto shared PageHeader component
**Source:** BLG-FE-106
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `StrategyBenchmark.js` page header renders via the shared `PageHeader` component (`title="Strategy Benchmark"`, `description="Compare live trading vs backtest"`), matching `strategy_benchmark.md` §2
- `BarChart2` icon and "Benchmark data as of DD Mon YYYY" last-updated line preserved via `PageHeader`'s available props or an adjacent element
- No visual regression beyond the intended consolidation
- **Staging-only AC:** visual rendering match — Playwright coverage or recorded staging sign-off required

### ST-20 — Keyboard navigation & focus-order audit
**Source:** BLG-FE-134
**Effort:** M
**Acceptance Criteria:**
- Audit of keyboard navigation and focus order across the app's primary flows (trade entry, trade plan, command palette)
- Findings filed as follow-up items where gaps are found
- Head of UX & Design sign-off

---

## EPIC-06 — Governance Process Hardening

**Maps to:** S2-21, S2-22, S2-23
**Owner:** Head of Specs Team; PMO Lead

### ST-21 — design_gate_prompt.md does not sync .claude_current_state.json root pointer on gate pass
**Source:** BLG-GOV-256
**Effort:** S (~0.5-1 day)
**Acceptance Criteria:**
- `design_gate_prompt.md` STEP 5 also writes `status = Design_Gate_Passed` (and `design_gate_status`/`design_gate_record`/`design_gate_completed_utc`) to `.claude_current_state.json` when the gate passes
- Versioned per `CLAUDE.md` §6 Governance File Edit Checklist (version bump, OPERATIONAL_GUIDE §14 sync, prompt_change_log.md entry, same commit)

### ST-22 — Recent-rebalance recency advisory at roadmap STEP -1
**Source:** BLG-GOV-216
**Effort:** S
**Acceptance Criteria:**
- `roadmap_prompt.md` patched to surface a confirmation advisory at STEP -1 if `last_scheduled_rebalance_utc` is <24h old
- Advisory fires correctly on a same-day re-invocation
- Versioned per `CLAUDE.md` §6

### ST-23 — Same-day scheduled-rebalance cycle_id collision handling
**Source:** BLG-GOV-207
**Effort:** S
**Acceptance Criteria:**
- `roadmap_prompt.md` STEP 0 rule added: detect an existing cycle folder for the computed `cycle_id` and auto-suffix (`-2`, `-3`, …) rather than requiring ad hoc user escalation
- A second same-day scheduled invocation no longer requires manual disambiguation
- Versioned per `CLAUDE.md` §6

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 working-day-equivalent units |
| Total estimated effort (in-scope) | ~26.15 days midpoint |
| Utilisation | ~93-109% |
| Over-allocation | No — intentional full-capacity fill per explicit user instruction |

```yaml
artifacts.stage4_backlog_slice: pass
artifacts.stage4_issue_manifest: pass
attributes.backlog_committed: true
attributes.design_gate_required: true
status: Committed
```
