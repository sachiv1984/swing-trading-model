Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-05
Cycle: 2026-08-05__release-v8.3
Release: v8.3

# Backlog Slice — v8.3

<!-- release-plan-marker: RP:v8.3:2026-08-05__release-v8.3 -->

27 stories across 6 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution).

---

## EPIC-01 — Operational Reliability & Security

**Maps to:** S2-01
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead

### ST-01 — Investigate and fix the SI-05 weekly Telegram digest delivery pipeline
**Source:** BLG-OPS-129
**Effort:** S
**Acceptance Criteria:**
- Root cause identified and documented (or, if genuinely unresolvable, documented as such with next steps)
- SI-05 digest delivery confirmed working again (at least one successful send observed post-fix)
- Infrastructure & Operations Owner sign-off

### ST-02 — Add delivery-failure alerting for the SI-05 weekly digest
**Source:** BLG-OPS-130
**Effort:** S
**Depends on:** ST-01 (alerting design should follow root-cause understanding)
**Acceptance Criteria:**
- Alert fires when the digest is overdue beyond the defined threshold
- Confirmed firing correctly on a deliberately-stale test (consistent with the `BLG-OPS-128` staging-deploy-staleness check pattern)

### ST-03 — Recurring check confirming staging/production API keys remain distinct
**Source:** BLG-OPS-131
**Effort:** S
**Acceptance Criteria:**
- Recurring automated check confirms staging's key is rejected by production and vice versa
- Alert fires if either key is ever found to authenticate against the wrong environment
- Confirmed firing correctly on a deliberately-cross-wired test

### ST-04 — Gemini API key rotation runbook
**Source:** BLG-SEC-17
**Effort:** S
**Acceptance Criteria:**
- Rotation runbook (steps + recommended cadence) added to `docs/security/api_key_security_register.md`

---

## EPIC-02 — Backend Engineering Hardening

**Maps to:** S2-02
**Owner:** Infrastructure & Operations Owner; Head of Engineering; Data Model & Domain Schema Owner; Backend Engineering Patterns Owner

### ST-05 — Database index audit for Arc 4 cross-table queries
**Source:** BLG-BE-37
**Effort:** S
**Acceptance Criteria:**
- Index audit document produced covering Arc 4 query patterns (trade_plans, red_flag_events, arc5_compliance_scores, ai_journal_summaries)
- Any missing indexes produce separate BLG items before sign-off
- Reviewed by Infrastructure & Operations Owner

### ST-06 — Alpaca API rate-limit backoff audit
**Source:** BLG-BE-57
**Effort:** S
**Acceptance Criteria:**
- Audit findings on current retry/backoff logic vs Alpaca's documented rate limits documented
- Any gaps filed as follow-up items

### ST-07 — Canonical enum registry for position_state values shared frontend/backend
**Source:** BLG-BE-67
**Effort:** S
**Acceptance Criteria:**
- Canonical registry exists (shared constants file or OpenAPI enum)
- Backend and frontend confirmed to derive from it, or a documented reconciliation shows they were already consistent

### ST-08 — Conform remaining routers to canonical error envelope + status codes
**Source:** BLG-BE-69
**Effort:** M
**Acceptance Criteria:**
- All listed router error paths (alerts, analytics, digest, ai, paper_trading, plan_vs_reality, portfolio_size, red_flag_journal, saved_filters, screener, strategy_benchmark, ticker_universe, trade_plans, trades_export, validation, watchlist, earnings, news) return the canonical `{status, message}` envelope at the correct HTTP status code
- No change to success-path shapes
- No change to existing frontend error-handling behaviour without a corresponding frontend check
- Applied incrementally across multiple sequenced commits/PRs, not one large diff (per RISK-01)

### ST-09 — Retry/backoff for Yahoo Finance regime-check call sites
**Source:** BLG-BE-79
**Effort:** S
**Acceptance Criteria:**
- Both call sites (`utils/pricing.py::check_market_regime`/`get_ma200`, `services/screener_batch_service.py::_fetch_index_regime`) use `retry_with_backoff`
- Existing fallback behaviour on exhausted retries unchanged
- Regression test confirms retry attempts occur before fallback

### ST-10 — Idempotent retry for Alpaca paper-trading order sync
**Source:** BLG-BE-80
**Effort:** S
**Acceptance Criteria:**
- `client_order_id` derived deterministically from the position id
- `retry_with_backoff` applied to `sync_open_paper_position`
- Test confirms a retried call with the same `client_order_id` does not create a duplicate order (mocked)

---

## EPIC-03 — Frontend & Design-System Debt

**Maps to:** S2-03
**Owner:** Base44 Frontend Prompt Owner; Head of Engineering; Head of UX & Design

**Staging-only ACs:** ST-11 and ST-15 each carry an observable UI acceptance criterion — see RISK-02; Design Gate PASS or Playwright coverage/staging sign-off required before these ACs may be considered met (per CLAUDE.md §2).

### ST-11 — Shared modal shell for compliance/checklist components
**Source:** BLG-FE-103
**Effort:** M
**Acceptance Criteria:**
- Shared modal shell component extracted; `ComplianceRecheckModal.js` and the PT-05 checklist modal both migrated
- No visual/behavioural regression (Playwright coverage confirms)

### ST-12 — Extract a shared modal-confirmation component
**Source:** BLG-FE-121
**Effort:** S
**Acceptance Criteria:**
- Single reusable confirmation-modal component exists (configurable message, optional undo-window countdown)
- Referenced by both `BLG-FE-116`/`BLG-FE-117`'s Base44 prompt templates before their sprint execution begins

### ST-13 — Unified loading-skeleton pattern for async-loading cards
**Source:** BLG-FE-126
**Effort:** M
**Acceptance Criteria:**
- Unified loading-skeleton pattern documented in `design_system.md`
- Not required to retrofit all existing cards in one pass

### ST-14 — Standard Base44 prompt section for dark/light theme compliance
**Source:** BLG-FE-132
**Effort:** S
**Acceptance Criteria:**
- Standard theme-compliance section added to `base44_prompt_template_library.md`
- Base44 Frontend Prompt Owner sign-off

### ST-15 — AI disclaimer component extraction
**Source:** BLG-FE-81
**Effort:** S
**Acceptance Criteria:**
- Single shared `AiDisclaimer` component used by both the AI daily briefing and AI chat widget
- No visual regression (same rendered contrast as post-v6.4 fix)
- Playwright: existing disclaimer visibility assertions still pass

---

## EPIC-04 — QA & Spec Debt

**Maps to:** S2-04
**Owner:** Director of Quality; API Contracts & Documentation Owner; Frontend Specifications & UX Documentation Owner

### ST-16 — Add baseline Playwright coverage for Watchlist.js
**Source:** BLG-QA-86
**Effort:** S
**Acceptance Criteria:**
- New spec file (`tests/e2e/watchlist.spec.js`) passes in CI
- Covers at minimum: entry rendering, news toggle, Add Ticker modal open

### ST-17 — OpenAPI drift gate false-negative sweep
**Source:** BLG-QA-94
**Effort:** S
**Acceptance Criteria:**
- Quarterly 3-way sweep procedure documented (router decorators, contract file headings, openapi.yaml paths)
- First run scheduled
- Zero drift confirmed or gaps filed

### ST-18 — DoQ sign-off staleness pre-merge lint
**Source:** BLG-QA-98
**Effort:** S
**Acceptance Criteria:**
- Pre-merge lint/CI check added to `quality_gate.yml`
- Fails on a synthetic Pending-row test case

### ST-19 — OpenAPI response-example drift spot-check
**Source:** BLG-SPEC-88
**Effort:** S
**Acceptance Criteria:**
- Spot-check of a sample of documented examples against live responses performed and documented
- Any drift found filed as follow-up BLG-SPEC-* items

### ST-20 — API endpoint deprecation-window policy
**Source:** BLG-SPEC-96
**Effort:** S
**Acceptance Criteria:**
- Deprecation-window policy section added to API contract documentation standards
- Head of Specs Team sign-off

### ST-21 — Canonical form validation error-message pattern spec
**Source:** BLG-SPEC-108
**Effort:** S
**Acceptance Criteria:**
- Canonical error-message pattern spec (tone, placement, wording conventions) added to `design_system.md`
- Frontend Specifications & UX Documentation Owner sign-off

---

## EPIC-05 — Governance Process

**Maps to:** S2-05
**Owner:** Head of Specs Team; AI Compliance & Governance Officer; Strategy Rules & System Intent Owner; Director of HR

### ST-22 — SC-02: Remove RESUME PRECHECK mutation detection block from release_planning_prompt.md
**Source:** BLG-GOV-124
**Effort:** S
**Acceptance Criteria:**
- RESUME PRECHECK mutation detection/invalidation map block removed (mutation-detection portion only)
- Terminal State Guard and State File Immutability Rule hard gates extracted and retained in the prompt body
- State.json resume rule retained
- Dry-run validation pass confirming no functional regression
- Version bump + changelog entry
- Head of Specs Team sign-off

### ST-23 — Formal §13 boundary re-attestation cadence
**Source:** BLG-GOV-204
**Effort:** M
**Acceptance Criteria:**
- Semi-annual boundary re-attestation cadence proposed across all shipped AI/automation-adjacent features (IT-06, SI-01, Gemini thesis generation, etc.)
- First review date set
- Strategy Rules & System Intent Owner sign-off

### ST-24 — SI-02 trade-count gate threshold calibration review
**Source:** BLG-GOV-237
**Effort:** S
**Acceptance Criteria:**
- Review performed of whether the 11-trade-plan threshold remains appropriate now that `BLG-FE-109` has shipped (shipped v7.3, 2026-07-16 — condition already met)
- Written conclusion recorded

### ST-25 — prompt_change_log.md mixed prepend/append ordering breaks gap detection
**Source:** BLG-GOV-257
**Effort:** M
**Acceptance Criteria:**
- Chosen fix implemented: either (a) one-time full re-sort of `prompt_change_log.md` into strict newest-first order, or (b) change STEP -1.7-class checks to scan the full file for the latest Date column per filename rather than relying on file position
- The `sprint_planning_prompt.md` false-positive case no longer reproduces
- If (a): file verified newest-first top-to-bottom after the resort
- If (b): new logic documented in `shared_standards.md`

### ST-26 — Cross-role workload balance check
**Source:** BLG-GOV-270
**Effort:** S
**Acceptance Criteria:**
- Lightweight cross-cycle check defined, tallying story ownership per role over a rolling window, surfaced at roadmap rebalance
- Director of HR sign-off

---

## EPIC-06 — Product Retrospective

**Maps to:** S2-06
**Owner:** Financial Reporting & Records Owner

### ST-27 — Monthly P&L report format review — 3-month usage retrospective
**Source:** BLG-FEAT-45
**Effort:** S
**Acceptance Criteria:**
- Format review conducted with 3+ months of usage data available (gate cleared 2026-08-05)
- Any column, section, or display precision improvements identified
- Brief recommendations document produced; if no changes warranted, record "no change" decision
- Product Owner sign-off

---

## Capacity Summary (see `release_plan.md §Capacity Check` for full detail)

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days |
| Total estimated effort (in-scope) | ~25.25 days |
| Utilisation | ~90-105% |
| Over-allocation | No |
