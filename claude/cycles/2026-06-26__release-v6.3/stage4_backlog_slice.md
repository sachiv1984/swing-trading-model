**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.3
**Cycle:** 2026-06-26__release-v6.3
**Last Updated:** 2026-06-26
**Sprint Backlog Source:** This slice is authoritative. Sprint Planning Engine reads this file at Phase 2.

---

# v6.3 Backlog Slice — 2026-06-26__release-v6.3

<!-- release-plan-marker: RP:v6.3:2026-06-26__release-v6.3 -->

---

## EPIC-01 — Production Correctness & AI Security Hardening

**Purpose:** Close the P1 correctness and security gaps created by v6.2 delivery. Two user-reported production bugs (AI journal summary failure, R-multiple display) are mandatory per rebalance STEP 8.0 mandate. AI endpoint rate limiting and injection threat model address the security surface introduced with live Anthropic API integration. Conditional governance items (§13 disclaimer assessment, API contract checklist) extend the AI safety coverage.

**Sprint assignment:** Sprint 1

**Maps to:** S2-01, S2-02, S2-03, S2-04, S2-05, S2-06

---

### ST-01 — Fix AI journal summary on Trade History tab (BLG-BE-39)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Head of Backend Engineering
**Backlog ref:** BLG-BE-39
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** AI journal summary feature on Trade History tab is non-functional. Users expect an AI-generated summary of journal notes for a given trade; the feature fails silently. Root cause unknown — may be a broken endpoint, failed Claude API call, missing API key, or silent error in ai_service.py journal summarisation path.

**Acceptance criteria:**
- AC-01: AI journal summary generates successfully for trades with journal notes on the Trade History tab
- AC-02: Error states are surfaced clearly to the user rather than silently failing
- AC-03: No regression to other ai_service.py functionality (daily briefing, chat endpoints)

---

### ST-02 — Fix R-multiple not displaying on Reflection page (BLG-FE-79)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Base44 Frontend Prompt Owner; Head of Backend Engineering
**Backlog ref:** BLG-FE-79
**Delegation class:** delegated_frontend (observable UI rendering fix)
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** Reflection page shows "—" for R-multiple column across all tickers. R-multiple is a core trade evaluation metric; its absence makes the Reflection page unreliable. Root cause: either backend not computing/returning the field, or frontend not reading it correctly.

**Acceptance criteria:**
- AC-01: R-multiple is displayed as a numeric value for all closed trades with sufficient data on the Reflection page
- AC-02: Trades with insufficient data (no stop loss recorded) show a clearly labelled "N/A" rather than a silent dash
- AC-03: No regression to other Reflection page columns

---

### ST-03 — AI endpoint per-endpoint rate limiting hardening (BLG-OPS-81)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Backlog ref:** BLG-OPS-81
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** POST /ai/daily-briefing and POST /ai/chat have no per-endpoint rate limiting. Both make Anthropic API calls on every request. A single automated abuse vector could exhaust the monthly Anthropic API budget without any circuit-breaker.

**Acceptance criteria:**
- AC-01: POST /ai/daily-briefing rate limit enforced (~10 req/min/IP); 429 returned after limit exceeded
- AC-02: POST /ai/chat rate limit enforced (~30 req/min/IP); 429 returned after limit exceeded
- AC-03: Retry-After header present in all 429 responses
- AC-04: Rate limits documented in openapi.yaml and relevant api_contracts document
- AC-05: Endpoint test suite (backend/routers/test.py) updated to cover 429 response scenario for both endpoints

---

### ST-04 — AI response injection risk assessment (BLG-GOV-146)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Cybersecurity & Trust Lead; AI Compliance & Governance Officer
**Backlog ref:** BLG-GOV-146
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** v6.2 AI chat and daily briefing features consume external data (market data, strategy rules, trade history) as context for Anthropic API calls. A threat model question: can a malicious actor craft market data API responses or strategy_rules.md content that causes the AI to produce misleading trading advice? This threat was not covered by the SRB-v1.7 §13 design gate review.

**Acceptance criteria:**
- AC-01: Threat model document produced covering all external data inputs to the AI prompt construction pipeline (POST /ai/daily-briefing and POST /ai/chat context assembly)
- AC-02: For each input: injection risk classified as accepted / mitigated / open
- AC-03: Open risks (if any) filed as separate backlog items
- AC-04: Document filed as `docs/specs/security/ai_injection_risk_assessment.md`
- AC-05: Cybersecurity & Trust Lead and AI Compliance Officer sign-off

---

### ST-05 — AI feature advisory disclaimer visibility assessment (BLG-GOV-147) [CONDITIONAL]

**Type:** Conditional
**Effort:** S (<0.5 day)
**Owner:** AI Compliance & Governance Officer; Head of UX & Design
**Backlog ref:** BLG-GOV-147
**Delegation class:** autonomous
**Sprint:** Sprint 1 (if capacity after ST-01 through ST-04)
**EPIC:** EPIC-01

**Context:** §13 requires AI advisory disclaimers to be prominently visible on all AI outputs. v6.2 shipped with the assumption that disclaimers were properly implemented. Playwright SC-AI-01 confirms rendering but does not verify prominence (size, contrast, position).

**Acceptance criteria:**
- AC-01: Visual assessment of AI daily briefing and AI chat disclaimer display (font size, colour contrast, position, dismissal behaviour) completed and documented
- AC-02: Confirmation: "disclaimer prominent and compliant" OR remediation items filed as new backlog items targeting v6.3 or v6.4
- AC-03: Assessment documented in `docs/product/decisions/` or `docs/specs/qa/`
- AC-04: AI Compliance Officer and Head of UX & Design sign-off

---

### ST-06 — API contract review checklist for AI advisory endpoints (BLG-GOV-148) [CONDITIONAL]

**Type:** Conditional
**Effort:** S (~0.5 day)
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Backlog ref:** BLG-GOV-148
**Delegation class:** autonomous
**Sprint:** Sprint 1 (if capacity after ST-01 through ST-04)
**EPIC:** EPIC-01

**Context:** API contracts for AI advisory endpoints require §13 boundary confirmation in addition to standard endpoint documentation. No standardised checklist exists for this confirmation step.

**Acceptance criteria:**
- AC-01: §13 boundary confirmation checklist authored covering: advisory-only response structure, no automated action fields, disclaimer presence, rate limiting documented, audit logging documented
- AC-02: Checklist applied retroactively to existing v6.2 AI endpoint contracts (POST /ai/daily-briefing, POST /ai/chat); gaps (if any) filed as remediation items
- AC-03: Checklist document filed in `docs/specs/api_contracts/`
- AC-04: API Contracts Owner and Head of Specs Team sign-off

---

## EPIC-02 — Test Infrastructure & Quality Coverage

**Purpose:** Establish automated test coverage for v6.2 nightly computation services that currently have zero CI coverage. BLG-QA-65/66 (firm) are P1 safety items — a silent regression in trailing stop computation, rebalance exit detection, or inv-vol sizing would affect production without any CI alarm. BLG-QA-67/68 (conditional) extend AI endpoint schema validation and §13 boundary coverage.

**Sprint assignment:** Sprint 1

**Maps to:** S2-07, S2-08, S2-09, S2-10

---

### ST-07 — Nightly stop computation CI simulation tests (BLG-QA-65)

**Type:** Firm
**Effort:** S (~1 day)
**Owner:** QA Lead; Backend Engineering Patterns Owner
**Backlog ref:** BLG-QA-65
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** v6.2 introduced nightly computation of trailing stops, rebalance exits, and inverse-vol position sizing. These computations run on a schedule and have zero automated test coverage. A silent regression would affect production trailing stop levels without any CI alarm.

**Acceptance criteria:**
- AC-01: Trailing stop computation test passes against fixture dataset — fixtures represent known portfolio state (positions with stop history, price data); computed trailing stop output matches expected values
- AC-02: Rebalance exit detection test passes against fixture dataset — fixture represents positions at and near rebalance threshold
- AC-03: Inverse-vol sizing computation test passes against fixture dataset — fixture includes mixed-volatility positions; computed sizing matches expected allocations
- AC-04: All tests registered in CI to run on changes to affected services (trailing_stop_service.py, rebalance_service.py, position_sizing_service.py or equivalent)
- AC-05: Fixture update procedure documented (when and how to update fixtures after strategy_rules.md changes)

---

### ST-08 — Strategy signal regression test specification (BLG-QA-66)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** QA & Testing Owner; Director of Quality
**Backlog ref:** BLG-QA-66
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** BLG-QA-65 (ST-07) requires a formal specification defining scenario coverage requirements, expected outputs, and fixture maintenance procedure. Without a specification, CI simulation tests may cover an incomplete scenario set or drift from production behaviour.

**Acceptance criteria:**
- AC-01: Specification document produced covering scenario coverage requirements for BLG-QA-65: which portfolio states must be represented (trailing stop active, no stop, position at rebalance threshold, inv-vol position, mixed)
- AC-02: Expected output formats and tolerance ranges defined
- AC-03: Fixture maintenance procedure documented (when and how to update fixtures after strategy_rules.md changes)
- AC-04: Document filed as `docs/specs/qa/strategy_signal_regression_spec.md`
- AC-05: Director of Quality and QA Lead sign-off

---

### ST-09 — AI chat response schema validation tests (BLG-QA-67) [CONDITIONAL]

**Type:** Conditional
**Effort:** S (~0.5 day)
**Owner:** QA Lead; API Contracts & Documentation Owner
**Backlog ref:** BLG-QA-67
**Delegation class:** autonomous
**Sprint:** Sprint 1 (if capacity after ST-07 and ST-08)
**EPIC:** EPIC-02

**Context:** POST /ai/chat must return advisory-only structured responses conforming to expected JSON schema. No test currently validates the response schema or confirms that directive language patterns are absent.

**Acceptance criteria:**
- AC-01: Response schema validation test passes in CI — response conforms to expected schema (fields, types, optional fields)
- AC-02: Advisory-only constraint test passes — no directive language patterns present in response body
- AC-03: Tests registered in `backend/routers/test.py` or equivalent CI test entry point

---

### ST-10 — §13 boundary test suite for AI advisory endpoints (BLG-QA-68) [CONDITIONAL]

**Type:** Conditional
**Effort:** S (~0.5 day)
**Owner:** QA & Testing Owner; AI Compliance & Governance Officer
**Backlog ref:** BLG-QA-68
**Delegation class:** autonomous
**Sprint:** Sprint 1 (if capacity after ST-07 and ST-08)
**EPIC:** EPIC-02

**Context:** §13 compliance for AI advisory endpoints depends on consistent enforcement of advisory-only output constraints. No document defines the full set of §13 boundary test scenarios for POST /ai/daily-briefing, POST /ai/chat, and future AI endpoints.

**Acceptance criteria:**
- AC-01: §13 boundary test scenario document produced covering all current AI advisory endpoints — for each endpoint, defines §13 compliance test scenarios: advisory language confirmation, no automated action, disclaimer rendered, no specific instrument recommendations
- AC-02: Document serves as template for future AI endpoint §13 assessment
- AC-03: Document filed as `docs/specs/qa/ai_s13_boundary_test_suite.md`
- AC-04: AI Compliance Officer and QA & Testing Owner sign-off

---

## EPIC-03 — Strategy Benchmark & UX Enhancement

**Purpose:** Flagship feature delivery for v6.3. BLG-FEAT-53 (Strategy Benchmark page) closes the visibility gap between live trading and production_strategy.py backtest performance — the "am I trading this strategy?" question. BLG-FE-80 (morning briefing progressive disclosure) addresses repeat-user UX friction. Conditional ops items (scheduler monitoring, latency baseline, rollback runbook) fill remaining Sprint 2 capacity.

**Sprint assignment:** Sprint 2

**Maps to:** S2-11, S2-12, S2-13, S2-14, S2-15

---

### ST-11 — Strategy Benchmark page: compare live trades against backtest (BLG-FEAT-53)

**Type:** Firm
**Effort:** L (~1 week / 5 days)
**Owner:** Product Owner
**Backlog ref:** BLG-FEAT-53
**Delegation class:** delegated_frontend (major new page with 3 panels, toggle modes, interactive filtering)
**Sprint:** Sprint 2
**EPIC:** EPIC-03

**Context:** No way currently exists to know whether live trading is tracking the production strategy's backtest performance. The backtest (`production_strategy.py`) generates trade-level and annual performance data in CSV files that are not connected to the live system. Design: single scrollable page with sticky year + market filters; Panel 1 (Performance Parity: side-by-side stat cards + PnL bar chart), Panel 2 (Yearly Breakdown table), Panel 3 (Trade Log with toggle modes and exit reason badges).

**Sequencing note:** DB schema migration must precede API implementation, which must precede frontend development. `import_backtest.py` companion script can be developed in parallel.

**Acceptance criteria:**
- AC-01: Strategy Benchmark page accessible from main navigation
- AC-02: Year filter (All / individual year) applies to all three panels simultaneously; market filter works independently
- AC-03: Panel 1 shows backtest stats and actual stats side-by-side; actual stats show "—" when no live trades exist for the selected period (not zero)
- AC-04: Panel 2 yearly breakdown table covers all years present in backtest data (2018–present)
- AC-05: Panel 3 trade log supports three toggle modes (backtest only / actual only / side-by-side); exit reason badges use Stop (red) / Risk-Off (amber) / Rebalance (teal) consistent with existing Positions/Signals badge language
- AC-06: POST /strategy/benchmark/import upserts data correctly; "Last updated" timestamp reflects most recent import date
- AC-07: `import_backtest.py` script reads latest CSVs from `production_results/` and calls the import endpoint; runnable with `python import_backtest.py`
- AC-08: All new API endpoints (POST /strategy/benchmark/import, GET /strategy/benchmark/summary, GET /strategy/benchmark/trades) documented in `docs/reference/openapi.yaml` and `docs/specs/api_contracts/` in the same sprint
- AC-09: New DB tables (backtest_trades, backtest_yearly_performance) and all new routes registered in `backend/routers/test.py` in the same commit as the route implementation

---

### ST-12 — Morning briefing progressive disclosure (BLG-FE-80)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Backlog ref:** BLG-FE-80
**Delegation class:** delegated_frontend (observable UI interaction: expand/collapse state, localStorage persistence)
**Sprint:** Sprint 2
**EPIC:** EPIC-03

**Context:** The AI daily briefing card (AiDailyBriefing.js, shipped v6.2) displays three content-dense sections always fully expanded. A user who has already reviewed market context and signals must scroll past the full briefing to reach AI chat on every page load. Progressive disclosure reduces visual noise for repeat daily usage.

**Acceptance criteria:**
- AC-01: Each section of the AI daily briefing (market context, signals, chat prompt) has a visible expand/collapse toggle
- AC-02: Sections collapse and expand without losing content
- AC-03: Section collapse state persists across page reloads via localStorage (versioned key to handle schema changes)
- AC-04: Default state is all sections expanded (no UX regression for new users)
- AC-05: Playwright: expand all → collapse market context → reload → verify market context still collapsed

---

### ST-13 — Background scheduler health monitoring endpoint (BLG-OPS-79) [CONDITIONAL]

**Type:** Conditional
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Backlog ref:** BLG-OPS-79
**Delegation class:** autonomous
**Sprint:** Sprint 2 (conditional — requires architecture review before implementation)
**EPIC:** EPIC-03

**Context:** v6.2 added a production background scheduler running nightly computations without any health monitoring endpoint. If the scheduler silently fails, there is no alert and no way to detect the failure externally. Gate: architecture review of v6.2 scheduler must confirm available data fields before endpoint design.

**Acceptance criteria:**
- AC-01: Architecture review of v6.2 scheduler documented before implementation begins
- AC-02: `GET /health/scheduler` returns last-run status, timestamps, and any error details for each nightly computation job (trailing stop, rebalance exit, inv-vol sizing)
- AC-03: Endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml`

---

### ST-14 — Measure live latency for POST /ai/daily-briefing and POST /ai/chat (BLG-OPS-78) [CONDITIONAL]

**Type:** Conditional
**Effort:** XS (<1 hour)
**Owner:** Infrastructure & Operations Owner
**Backlog ref:** BLG-OPS-78
**Delegation class:** autonomous
**Sprint:** Sprint 2 (conditional)
**EPIC:** EPIC-03

**Context:** Both AI endpoints were registered in `docs/operations/api_performance_baseline.md §22` during v6.2 with estimated latency characteristics. Actual timing measurements were deferred until post-deployment to production. Without live p50/p95 measurements, the regression threshold from §22.2 cannot be established.

**Acceptance criteria:**
- AC-01: Minimum 5 authenticated warm requests run against production for each endpoint; p50/p95 recorded per §19 methodology
- AC-02: `docs/operations/api_performance_baseline.md §22.3` populated with actual p50/p95 for both endpoints
- AC-03: Regression threshold documented per §22.2 formula (p95 > 2× measured p95)

---

### ST-15 — Render deployment rollback procedure documentation (BLG-OPS-80) [CONDITIONAL]

**Type:** Conditional
**Effort:** XS (<0.5 day)
**Owner:** Infrastructure & Operations Owner
**Backlog ref:** BLG-OPS-80
**Delegation class:** autonomous
**Sprint:** Sprint 2 (conditional)
**EPIC:** EPIC-03

**Context:** No documented runbook exists for rolling back to a prior Render deployment version in case of a production incident. The resolution currently depends on whoever is on call knowing the correct steps.

**Acceptance criteria:**
- AC-01: Rollback procedure document produced and filed in `docs/operations/`
- AC-02: Document covers: rollback steps (navigate Render dashboard, identify prior deploy version, initiate rollback, verify), rollback decision criteria (severity that warrants immediate rollback vs fix-forward), verification steps
- AC-03: Infrastructure & Operations Owner sign-off
