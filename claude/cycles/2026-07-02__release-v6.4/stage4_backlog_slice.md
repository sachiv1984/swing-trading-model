**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.4
**Cycle:** 2026-07-02__release-v6.4
**Last Updated:** 2026-07-02
**Sprint Backlog Source:** This slice is authoritative. Sprint Planning Engine reads this file at Phase 2.

---

# v6.4 Backlog Slice — 2026-07-02__release-v6.4

<!-- release-plan-marker: RP:v6.4:2026-07-02__release-v6.4 -->

---

## EPIC-01 — Backend Correctness & Security Hardening

**Purpose:** Fix the P1 production correctness bug (mandatory per rebalance STEP 8.0 fast-track) where live signal generation reads a deprecated ticker table, and close the two input-validation gaps identified in the ST-04 AI injection risk assessment.

**Sprint assignment:** Sprint 1

**Maps to:** S2-01, S2-02, S2-03

---

### ST-01 — Signal generation reads deprecated `tickers` table instead of `ticker_universe` (BLG-BE-40)

**Type:** Firm
**Effort:** XS (<1h)
**Owner:** Backend Engineering Patterns Owner
**Backlog ref:** BLG-BE-40
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** `signal_service.py`'s `generate_momentum_signals()` imports `get_all_tickers` from `database.py` (legacy `tickers` table) instead of `services.ticker_universe_service.get_all_tickers(active_only=True)`. Live signal generation reads a frozen, unmaintained snapshot instead of the actively-managed ticker list, diverging from both the screener and the backtest.

**Acceptance criteria:**
- AC-01: `signal_service.py` sources its ticker universe from `ticker_universe`, not `tickers`
- AC-02: Live signal generation matches the `ticker_universe` active list — verified by adding/deactivating a ticker in Ticker Universe Management and confirming it appears/disappears in generated signals
- AC-03: No regression to existing signal fields or downstream sizing logic

---

### ST-02 — Sanitise `context_opts.ticker` before system prompt injection (BLG-SEC-01)

**Type:** Firm
**Effort:** XS (<0.25 day)
**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Backlog ref:** BLG-SEC-01
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** `context_opts.ticker` from the request body is interpolated directly into the `ai_chat()` system prompt f-string with no sanitization, elevating an attacker's payload to system-prompt authority level (authenticated attacker only).

**Acceptance criteria:**
- AC-01: `context_opts.ticker` validated before insertion into system prompt — strip/reject values containing `\n`, `\r`, or characters outside `[A-Z0-9.:/-]`, max 20 characters
- AC-02: Strings with newlines or injection characters rejected with HTTP 422
- AC-03: Unit test added for validation logic
- AC-04: Cybersecurity & Trust Lead sign-off

---

### ST-03 — Validate ticker/market strings at signal write time (BLG-SEC-02)

**Type:** Conditional
**Effort:** S (~0.5 day)
**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Backlog ref:** BLG-SEC-02
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** Signal ticker/market strings are interpolated into AI prompts for both daily-briefing and chat endpoints. If the screener's external data source provides crafted values, those propagate to the AI prompt. No validation exists at signal write time.

**Acceptance criteria:**
- AC-01: Signal write path validates ticker and market strings — strip non-alphanumeric characters (allow `.`, `-`, `/`, `:` for international tickers, max 12 chars)
- AC-02: Existing signals reviewed; anomalous values documented or cleaned
- AC-03: Cybersecurity & Trust Lead sign-off

---

## EPIC-02 — Governance & Audit Remediation

**Purpose:** Close all four remediation clusters raised by lifecycle audit AUD-2026-07-01, and resolve the two-cycle-overdue FI-P4-01/FI-P3-02 friction items plus the FI-P3-01 Base44 §6 advisory (folded into ST-06 per Head of Specs Team decision — see `decisions--2026-07-02__release-v6.4.md`).

**Sprint assignment:** Sprint 1

**Maps to:** S2-04, S2-05, S2-06, S2-07

---

### ST-04 — Fix governance version-sync drift (BLG-GOV-150)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-150
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** Three confirmed version/naming desyncs from the lifecycle audit: `OPERATIONAL_GUIDE.md` self-disagreement (header v4.65 vs §14 self-row v4.63 vs §14 Change Log top entry v4.64); §14 "Roadmap Engine Source" row stuck at v7.5 vs actual v7.6; `metrics_definitions_analytics_owner.md` role-name mismatch vs `team_charter.md`.

**Acceptance criteria:**
- AC-01: `OPERATIONAL_GUIDE.md` header, §14 self-row, and §14 Change Log top entry all show the same version number
- AC-02: §14 "Roadmap Engine Source" row matches `roadmap_prompt.md`'s actual `**Version:**` header
- AC-03: `metrics_definitions_analytics_owner.md` role name matches `team_charter.md` §3.3 exactly

---

### ST-05 — Document hygiene cleanup (BLG-GOV-151)

**Type:** Conditional
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-151
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** Five low-severity documentation defects from the lifecycle audit: README §4 routine coverage gap, README §2 broken path, README staleness, Class 6 header format violations in 3 prompts, unbolded header fields in `pmo_lead.md`.

**Acceptance criteria:**
- AC-01: README §4 lists all 13 governed routines with working command + path references
- AC-02: No broken file paths remain in README §2
- AC-03: README `Last Updated` reflects the date of this change
- AC-04: `roadmap_prompt.md`, `release_planning_prompt.md`, `sprint_planning_prompt.md` headers show `Last Updated: [date]` only
- AC-05: `pmo_lead.md` header fields use `**Field:**` bold-label format

---

### ST-06 — Close structural reliability gaps (BLG-GOV-152 + FI-P3-01/FI-P3-02/FI-P4-01 re-target)

**Type:** Firm
**Effort:** M (~1–2 days)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-152
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** Four confirmed reliability/process gaps, two of which are 2-cycle-carried deferred patches at the audit SLA's escalation threshold: append-only guard parity gap (4 of 5 files in `shared_standards.md` §7 lack structural verification); the `spec_references=[]` CI/infrastructure convention (FI-P4-01/DF-10, deferred since v6.2, missed v6.3); the staging-only AC protocol ambiguity for wording-only vs visual-rendering ACs (FI-P3-02, deferred since v6.2, missed v6.3); the `amendment_cycle_prompt.md` §8/§9 `amendment_lessons.md` sunset contradiction. **Additionally folds in FI-P3-01** (Playwright strict-mode advisory to Base44 prompt draft §6, also missed at v6.3) per the Head of Specs Team re-targeting decision recorded in `decisions--2026-07-02__release-v6.4.md`.

**Acceptance criteria:**
- AC-01: All 5 files in `shared_standards.md` §7 have an equivalent structural (not prose-only) append-only guard, or the guard requirement is explicitly documented as N/A with rationale
- AC-02: `execution_prompt.md`'s `spec_references` policy has no remaining path that defaults to `[]` for infrastructural stories with an identifiable primary file (resolves FI-P4-01/DF-10)
- AC-03: CLAUDE.md §2 explicitly distinguishes wording-only ACs from visual/rendering ACs for the staging sign-off substitution rule (resolves FI-P3-02)
- AC-04: `amendment_cycle_prompt.md` §8 and §9 agree on the status of `amendment_lessons.md`
- AC-05: Base44 frontend prompt draft §6 includes a Playwright strict-mode advisory note (resolves FI-P3-01)

---

### ST-07 — Audit & governance process fixes (BLG-GOV-153)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-153
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** Four confirmed process gaps: design gate bypass dual-authority rule missing from `team_charter.md` (Class 1 canonical document, audit check G5 FAIL); `run audit` absent from the `shared_standards.md` §13 dry-run table; ambiguous `FRICTION_LOAD` formula wording in `claude/audit.py`; `scored_initiatives.md` static filename with no per-cycle history.

**Acceptance criteria:**
- AC-01: `team_charter.md` names the design gate bypass dual-authority requirement explicitly (new §5.7)
- AC-02: `shared_standards.md` §13 table includes all CLAUDE.md-listed governed routines, including `run audit`
- AC-03: `claude/audit.py`'s `FRICTION_LOAD` formula wording is unambiguous about its evaluation window ("since PRIOR_AUDIT_ID")
- AC-04: `scored_initiatives.md` naming convention is either consistently cycle-scoped or explicitly documented as current-only, with no orphaned dated files

---

## EPIC-03 — Strategy Benchmark Enhancement & UX/QA Polish

**Purpose:** Deliver the Skill-Silo pull-forward feature (Open Positions panel on Strategy Benchmark page), close two accessibility contrast gaps, register the three missing v6.3 endpoints in the API performance baseline, and close both outstanding v6.3 Playwright test gaps.

**Sprint assignment:** Sprint 1

**Maps to:** S2-08, S2-09, S2-10, S2-11, S2-12, S2-13

**Design Gate:** Required before sprint planning seals — ST-08, ST-09, ST-10 carry observable UI acceptance criteria (see RISK-06).

---

### ST-08 — Add Open Positions panel to Strategy Benchmark page (BLG-FEAT-54)

**Type:** Firm
**Effort:** M (~1–2 days)
**Owner:** Head of UX & Design; Backend Engineering Patterns Owner
**Backlog ref:** BLG-FEAT-54
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-03

**Context:** The Strategy Benchmark page's trade log and Panel 1/2 aggregates only reflect closed trades. When the backtest is fully invested, the page shows no activity past the last entry date, reading as stalled when real capital is actively deployed with real unrealized P&L (~£46k unrealized across 5 open positions observed 2026-06-30).

**Acceptance criteria:**
- AC-01: Panel appears whenever ≥1 unrealized position exists, showing a one-line summary and per-position table
- AC-02: Panel 1/2 realized win-rate/PnL stats are unaffected — unrealized positions never enter those aggregates
- AC-03: New `backtest_open_positions` table is fully replaced (not upserted) on each nightly import, consistent with `backtest_trades`
- AC-04: Any new endpoint ships with `openapi.yaml`, contract doc, and `backend/routers/test.py` registration in the same commit

---

### ST-09 — Improve AI daily briefing disclaimer text contrast (BLG-UX-01)

**Type:** Conditional
**Effort:** XS (<0.25 day)
**Owner:** Head of UX & Design; AI Compliance & Governance Officer
**Backlog ref:** BLG-UX-01
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-03

**Context:** The AI Advisory disclaimer text in `AiDailyBriefing.js` uses `text-slate-500 italic` (≈2.7:1 contrast), below WCAG AA's ≥4.5:1 requirement for text <18px.

**Acceptance criteria:**
- AC-01: Disclaimer text contrast ≥4.5:1 on the dark background (`text-slate-300`)
- AC-02: No visual regression to the "AI Advisory" badge or briefing card layout
- AC-03: Head of UX & Design sign-off

---

### ST-10 — Improve AI chat widget footer disclaimer contrast and add test coverage (BLG-UX-02)

**Type:** Firm
**Effort:** XS (<0.25 day)
**Owner:** Head of UX & Design; AI Compliance & Governance Officer
**Backlog ref:** BLG-UX-02
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-03

**Context:** The AI Chat Widget footer disclaimer uses `text-slate-600 italic text-xs` (≈1.9:1 contrast — critically low, effectively unreadable). No `data-testid` exists, preventing Playwright assertion.

**Acceptance criteria:**
- AC-01: Footer disclaimer text contrast ≥4.5:1 on dark background (`text-slate-400`)
- AC-02: `data-testid="ai-chat-advisory-footer"` present
- AC-03: Playwright test asserts footer text visible and contains "advisory" keyword
- AC-04: Head of UX & Design sign-off

---

### ST-11 — Add v6.3 endpoints to `api_performance_baseline.md` (BLG-OPS-82)

**Type:** Conditional
**Effort:** XS (<1 hour)
**Owner:** Infrastructure & Operations Owner
**Backlog ref:** BLG-OPS-82
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-03

**Context:** Three new GET endpoints shipped in v6.3 (`GET /strategy/benchmark/summary`, `GET /strategy/benchmark/trades`, `GET /health/scheduler`) are not registered in `docs/ops/api_performance_baseline.md`.

**Acceptance criteria:**
- AC-01: All three endpoints registered in `api_performance_baseline.md` with measured p50/p95 (minimum 5 warm requests per endpoint)
- AC-02: Regression threshold documented per §19.2 for each endpoint
- AC-03: Infrastructure & Operations Owner sign-off

---

### ST-12 — Playwright coverage for ST-01 observable UI ACs, AI journal summary error states (TEST-GAP-EPIC-01)

**Type:** Conditional
**Effort:** XS (<0.5 day)
**Owner:** QA & Testing Owner
**Backlog ref:** TEST-GAP-EPIC-01
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-03

**Context:** v6.3 ST-01 introduced observable UI error-state changes on the Trade History tab AI journal summary, cleared by code review only (staging sign-off deferred — reproducibility condition unmet). No Playwright test exists for these error states. See `verification_report.md` §6 (cycle 2026-06-26__release-v6.3), TSG-v63-01.

**Acceptance criteria:**
- AC-01: Playwright test covering "specific error message displayed when AI journal summary unavailable"
- AC-02: Playwright test covering server-error and network-error message rendering
- AC-03: Tests in `tests/e2e/` referencing `data-testid` selectors on the Trade History tab AI summary component

---

### ST-13 — Playwright scenario coverage for Strategy Benchmark page (TEST-GAP-EPIC-03)

**Type:** Firm
**Effort:** S (~1 day)
**Owner:** QA & Testing Owner
**Backlog ref:** TEST-GAP-EPIC-03
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-03

**Context:** v6.3 ST-11 (Strategy Benchmark page) shipped with `test_scenarios: "pending"` in `execution_state.json` (per LL-v2.0-P4-2) — zero Playwright coverage for the page's 3 panels, sticky filters, toggle modes, and exit reason badges. See `verification_report.md` §6 (cycle 2026-06-26__release-v6.3), TSG-v63-02.

**Acceptance criteria:**
- AC-01: Playwright test covering page accessibility from navigation
- AC-02: Playwright test covering year + market filters applying to all panels simultaneously
- AC-03: Playwright test covering Panel 1 "—" placeholder for actual fields when no live trades match
- AC-04: Playwright test covering Panel 3 toggle modes and exit reason badge colours
- AC-05: Tests in `tests/e2e/strategy-benchmark.spec.js` or equivalent

---
