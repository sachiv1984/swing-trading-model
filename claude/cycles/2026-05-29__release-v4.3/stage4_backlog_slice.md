**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-05-29__release-v4.3
**Release:** v4.3
**Published:** 2026-05-29
**Sealed:** true

---

# Backlog Slice — v4.3 Governance Consolidation, QA Debt Clearance & Ops Hardening

18 stories | 4 EPICs | 2 sprints

---

## EPIC-01: Governance Patch Resolution

**Description:** Resolve 3 outstanding actions from v4.2 post-ship closure (execution_prompt.md and qa_evidence_template.md patches) and deliver two governance hardening items (staging-only AC reference table, AI feature inventory). All OA-1/2/3 items are sprint-seal prerequisites — Sprint Planning must confirm all are present before sealing.

**Maps to:** S2-01, S2-02

---

### ST-01 — execution_prompt.md STEP 3.2.A: qa_signed_off advisory patch

**Backlog source:** OA-1 (v4.2 closure_record.md §6)
**Owner:** Head of Specs Team
**Effort:** XS (~0.5 day)
**Staging-only ACs:** None

**Problem:** After DoQ sign-off is completed and qa_evidence_EPIC-xx.md is committed, execution_state.json `qa_signed_off: true` is not updated in the same commit. This creates stale state detectable at delivery verification.

**Acceptance Criteria:**
- AC-01: execution_prompt.md STEP 3.2.A includes advisory: "After completing DoQ sign-off and committing qa_evidence_EPIC-xx.md, update execution_state.json `qa_signed_off: true` in the same commit"
- AC-02: Prompt version bumped per CLAUDE.md §6 governance file edit checklist
- AC-03: OPERATIONAL_GUIDE.md §14 execution engine source version updated
- AC-04: prompt_change_log.md entry appended (date, filename, vOLD→vNEW, summary, authority)
- AC-05: Head of Specs Team sign-off recorded

---

### ST-02 — execution_prompt.md STEP 5.3/STEP 8: sprint close branch safety advisory

**Backlog source:** OA-2 (v4.2 closure_record.md §6)
**Owner:** Head of Specs Team
**Effort:** XS (~0.5 day)
**Staging-only ACs:** None

**Problem:** Sprint close artefacts (sprint_close.md, lessons_learnt_cycle.md) may land on an exec branch rather than main when the execution engine runs STEP 8 from an exec branch context. No branch safety check exists at STEP 5.3 or STEP 8.

**Acceptance Criteria:**
- AC-01: Head of Specs Team decision: gate (halt if not on main) or advisory (warn if not on main) — decision recorded in this story
- AC-02: execution_prompt.md STEP 5.3 or STEP 8 includes the chosen check per the decision
- AC-03: Prompt version bumped per CLAUDE.md §6 checklist
- AC-04: OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md entry appended
- AC-05: Head of Specs Team sign-off recorded

---

### ST-03 — qa_evidence_template.md: AC mapping 1:1 advisory

**Backlog source:** OA-3 (v4.2 closure_record.md §6)
**Owner:** Head of Specs Team
**Effort:** XS (~0.5 day)
**Staging-only ACs:** None

**Problem:** QA evidence files consolidate multiple ACs into fewer evidence rows, creating traceability friction at delivery verification. Evidence rows should map 1:1 to backlog slice ACs; where consolidation occurs, the covered ACs must be noted explicitly.

**Acceptance Criteria:**
- AC-01: qa_evidence_template.md includes advisory: "Evidence table rows should map 1:1 to backlog slice ACs. When consolidating multiple ACs into one row, note which AC IDs are covered in the Evidence column."
- AC-02: Template version bumped if governed; governance checklist applied if Class 6
- AC-03: Head of Specs Team sign-off recorded

---

### ST-04 — Staging-only AC pre-designation reference table

**Backlog source:** BLG-GOV-42
**Owner:** Head of Specs Team; Director of Quality
**Effort:** S (~1 day)
**Staging-only ACs:** None

**Problem:** OA-01/02 escalation resolved in v4.1. Sprint planners still lack a consolidated reference table of known staging-only AC patterns, leading to ad-hoc designation and occasional misses.

**Acceptance Criteria:**
- AC-01: Reference table produced listing staging-only AC categories (e.g. "any AC requiring live external API call", "any AC referencing Render staging env", "Playwright E2E requiring non-mocked network")
- AC-02: At least 4 pattern examples drawn from v3.7–v4.2 deliveries (BLG-QA-24/28/29/30)
- AC-03: Reference table integrated into sprint planning reference materials (sprint_planning_prompt.md advisory or OPERATIONAL_GUIDE.md) — Head of Specs Team decides location
- AC-04: Head of Specs Team and Director of Quality sign-off recorded

---

### ST-05 — AI feature inventory document

**Backlog source:** BLG-GOV-47
**Owner:** AI Compliance & Governance Officer
**Effort:** S (~0.5 day)
**Staging-only ACs:** None

**Problem:** v4.1 replaced Gemini with Claude API. As AI features accumulate, no formal AI feature inventory exists for compliance, audit, and §13 review traceability.

**Acceptance Criteria:**
- AC-01: AI feature inventory document produced and filed in `docs/ai/ai_feature_inventory.md` (or equivalent governance location)
- AC-02: Inventory covers all current AI-touching features: Claude thesis generation (POST /trade-plans/{plan_id}/generate-thesis), AI Journal Summarisation (POST /ai/journal-summary), Claude cost threshold alert (POST /ai/check-daily-cost)
- AC-03: Each entry includes: feature name, endpoint, model used, purpose, §13 compliance status, data inputs/outputs
- AC-04: Reviewed by AI Compliance & Governance Officer and Strategy Rules & System Intent Owner

---

## EPIC-02: QA Debt & Test Coverage

**Description:** Clear 8 overdue QA backlog items: 3 staging verifications (v4.0/v4.1 deferred), Playwright E2E for Arc5ComplianceSection, Arc 5 E2E integration test specification, CI pipeline execution time baseline, Playwright scenario coverage matrix, and Arc 5 Playwright coverage audit. Staging verifications are human-delegate tasks (staging-only evidence).

**Maps to:** S2-03

---

### ST-06 — Staging verification: Claude thesis generation

**Backlog source:** BLG-QA-29
**Owner:** QA Lead
**Effort:** XS (~0.5 day)
**Staging-only ACs:** AC-01, AC-02, AC-03, AC-04 (all staging — requires live ANTHROPIC_API_KEY)

**Problem:** ST-12 EPIC-03 v4.0 (POST /trade-plans/{plan_id}/generate-thesis, "Improve with AI" button) has a staging-only AC that was deferred. Note: implementation uses Claude API (not Gemini) as of v4.1.

**Acceptance Criteria:**
- AC-01: On staging: `POST /trade-plans/{plan_id}/generate-thesis` returns thesis text when ANTHROPIC_API_KEY is set [staging-only]
- AC-02: "Improve with AI" button visible on TradePlan edit page when AI key configured [staging-only]
- AC-03: Button click generates thesis and populates setup_thesis textarea [staging-only]
- AC-04: Sign-off date recorded in qa_evidence file (EPIC-03 v4.3 or standalone note)

---

### ST-07 — Staging verification: ticker validation live Yahoo Finance rejection path

**Backlog source:** BLG-QA-30
**Owner:** Director of Quality; Head of Engineering
**Effort:** XS (~0.5 day)
**Staging-only ACs:** AC-01, AC-02 (requires live internet + staging env)

**Problem:** ST-05 v4.0 (BLG-BE-15) adds Yahoo Finance symbol validation. The AC "invalid ticker returns HTTP 422" requires live internet-connected staging with SKIP_TICKER_VALIDATION unset.

**Acceptance Criteria:**
- AC-01: POST an invalid ticker to staging `POST /ticker-universe` → HTTP 422, detail message present, ticker not saved [staging-only]
- AC-02: POST a valid ticker (e.g. AAPL) → HTTP 201, ticker present in subsequent GET [staging-only]
- AC-03: Sign-off date recorded

---

### ST-08 — Staging verification: Claude API daily cost threshold alert

**Backlog source:** BLG-QA-35
**Owner:** QA Lead; Infrastructure & Operations Owner
**Effort:** XS (~0.5 day)
**Staging-only ACs:** AC-01, AC-02 (requires live Telegram + staging DB rows)

**Problem:** ST-09 EPIC-03 v4.1 (POST /ai/check-daily-cost) has a staging-only AC requiring live TELEGRAM_BOT_TOKEN and gemini_audit_log rows (now claude_audit_log).

**Acceptance Criteria:**
- AC-01: On staging: `POST /ai/check-daily-cost` returns 200 with threshold/cost fields [staging-only]
- AC-02: With AI_DAILY_COST_THRESHOLD set below current daily spend: Telegram alert fires and is received [staging-only]
- AC-03: Sign-off date recorded

---

### ST-09 — Playwright E2E coverage for Arc5ComplianceSection

**Backlog source:** BLG-QA-28
**Owner:** QA Lead
**Effort:** S (~0.5 day)
**Staging-only ACs:** None

**Problem:** ST-02/04 v4.0 introduced Arc5ComplianceSection with 4 stat cards (Red Flag Events/Week, Override Rate, Top Rule Breach, Trade Plan Adherence). No Playwright test covers the rendering.

**Acceptance Criteria:**
- AC-01: Playwright test in `tests/e2e/` for PerformanceAnalytics page — "Arc 5 Signal Compliance" heading visible
- AC-02: All 4 stat card titles visible in test
- AC-03: Loading skeleton shown when API pending (use `page.route()` to mock)
- AC-04: Error state shown when API returns 500
- AC-05: Test passes in CI

---

### ST-10 — Arc 5 end-to-end integration test specification

**Backlog source:** BLG-QA-36
**Owner:** Director of Quality; QA Lead
**Effort:** M (~2 days)
**Staging-only ACs:** None

**Problem:** No formal integration test spec covers the complete Arc 5 compliance pipeline: SI-01 pre-entry validation → override acknowledgement → SI-03 red flag event written → Arc5ComplianceSection metrics update.

**Acceptance Criteria:**
- AC-01: Integration test spec document produced covering SI-01 → SI-03 data flow, Arc5ComplianceSection metric source, override chain
- AC-02: Observable assertions defined for each integration point
- AC-03: Playwright automation candidates vs manual verification steps identified
- AC-04: Reviewed by Director of Quality and QA Lead
- AC-05: Document filed in `docs/qa/` or `tests/e2e/`

---

### ST-11 — CI pipeline execution time baseline measurement

**Backlog source:** BLG-QA-38
**Owner:** QA Lead
**Effort:** XS (~0.25 day)
**Staging-only ACs:** None

**Problem:** No baseline for total CI pipeline execution time exists. BLG-QA-27 gates on CI > 5 minutes sustained across 3+ cycles; this item performs the measurement.

**Acceptance Criteria:**
- AC-01: Total CI pipeline execution time measured (3 sample runs, p50 noted)
- AC-02: Gate status determination for BLG-QA-27 documented (< 5 min → defer; ≥ 5 min → flag gate cleared)
- AC-03: Measurement recorded in QA notes or `docs/ops/`
- AC-04: Reviewed by QA Lead

---

### ST-12 — Playwright scenario coverage matrix and Arc 5 coverage audit

**Backlog source:** BLG-QA-32, BLG-QA-33
**Owner:** Director of Quality; QA Lead
**Effort:** M (~2 days)
**Staging-only ACs:** None

**Problem:** No consolidated view maps features to Playwright coverage (BLG-QA-32). Arc 5 specifically (SI-01/03 + Arc5ComplianceSection integration) needs a targeted coverage audit (BLG-QA-33).

**Acceptance Criteria (BLG-QA-32):**
- AC-01: Coverage matrix produced: feature/story → Playwright spec file(s) → scenario count → staging-only ACs flagged
- AC-02: Covers v3.7–v4.2 delivered features
- AC-03: Features with zero automated coverage identified

**Acceptance Criteria (BLG-QA-33):**
- AC-04: Arc 5 coverage assessment document produced (all SI features: SC-PEV-*, SC-RFJ-*, SC-AC5-*)
- AC-05: Gaps identified with specific scenario recommendations
- AC-06: Both documents filed in `docs/qa/`; reviewed by Director of Quality

---

## EPIC-03: Operations & Security Hardening

**Description:** Confirm staging environment parity, add the claude-audit-log endpoint to the performance baseline, and produce two security policy documents (API key rotation policy and external API key security register).

**Maps to:** S2-04

---

### ST-13 — Staging environment parity audit

**Backlog source:** BLG-OPS-33
**Owner:** Infrastructure & Operations Owner
**Effort:** M (~2 days)
**Staging-only ACs:** AC-01/02/03 (requires staging access)
**Note:** This story should execute before ST-06/07/08 staging verifications in Sprint 2.

**Problem:** A systematic parity audit of staging vs production (env vars, database schema, endpoints) was gated on v4.1 sprint planning complete — gate cleared 2026-05-27.

**Acceptance Criteria:**
- AC-01: Staging env vars verified against production (ANTHROPIC_API_KEY, Alpaca keys, DB connection, Telegram keys) [staging-only]
- AC-02: Database schema parity confirmed (claude_audit_log / gemini_audit_log, red_flag_events tables present in staging) [staging-only]
- AC-03: Sampled health check: v4.0/v4.1/v4.2 new endpoints respond on staging [staging-only]
- AC-04: Parity report produced and filed in `docs/ops/`
- AC-05: Infrastructure & Operations Owner sign-off recorded

---

### ST-14 — claude-audit-log performance baseline

**Backlog source:** BLG-OPS-42
**Owner:** Infrastructure & Operations Owner
**Effort:** XS (~0.25 day)
**Staging-only ACs:** AC-01 (requires live environment timing run)

**Problem:** GET /ai/claude-audit-log (added v4.2 ST-07) is in openapi.yaml but absent from docs/ops/api_performance_baseline.md.

**Acceptance Criteria:**
- AC-01: GET /ai/claude-audit-log added to api_performance_baseline.md with at least estimated p50 latency (staging or prod run) [staging-only]
- AC-02: Reviewed by Infrastructure & Operations Owner

---

### ST-15 — API key rotation policy and external API key security register

**Backlog source:** BLG-GOV-36, BLG-GOV-50
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Effort:** S (~1 day)
**Staging-only ACs:** None

**Problem:** No API key rotation cadence policy exists (BLG-GOV-36, overdue from v4.0). No consolidated external API key security register exists covering all credentials (BLG-GOV-50).

**Acceptance Criteria (BLG-GOV-36):**
- AC-01: Policy document `docs/ops/api_key_rotation_policy.md` produced
- AC-02: Covers Alpaca keys (annual rotation minimum) and ANTHROPIC_API_KEY (annual rotation minimum)
- AC-03: Rotation procedure documented (how to rotate without service disruption; env var update, staging + prod)
- AC-04: Responsibility assigned: Infrastructure & Operations Owner as executor; Cybersecurity & Trust Lead as policy owner

**Acceptance Criteria (BLG-GOV-50):**
- AC-05: External API key security register produced in `docs/security/api_key_security_register.md`
- AC-06: All external API keys listed: Alpaca key+secret, ANTHROPIC_API_KEY, Supabase/DB connection string
- AC-07: Each entry includes: key name, purpose, scope, rotation cadence, storage location, last rotation date
- AC-08: Reviewed by Cybersecurity & Trust Lead

---

## EPIC-04: Frontend Polish & Arc 5 Feature

**Description:** Fix the pre-entry check entry price bug, audit Claude thesis UI copy for Gemini references, and implement Arc 5 compliance score in the monthly P&L report.

**Maps to:** S2-05

---

### ST-16 — Pre-entry check entry price bug fix

**Backlog source:** BLG-FE-50
**Owner:** Frontend Engineer
**Effort:** XS (~0.25 day)
**Staging-only ACs:** None

**Problem:** The sizing validity check in the pre-entry validation panel requires entry_price and stop_price query params. The entry_price value appears to be written/formatted incorrectly, causing the check to fail.

**Acceptance Criteria:**
- AC-01: Root cause identified and documented (comment in code or PR description)
- AC-02: Sizing validity check passes when a valid numeric entry_price and stop_price are provided to the panel
- AC-03: No regression to other pre-entry checks (regime, signal, position sizing, earnings proximity, sector concentration)
- AC-04: Unit test or Playwright test covers the fixed path

---

### ST-17 — Claude thesis generation UI copy audit

**Backlog source:** BLG-FE-51
**Owner:** Base44 Frontend; Head of UX & Design
**Effort:** S (~0.5 day)
**Staging-only ACs:** None

**Problem:** v4.1 replaced Gemini with Claude API for thesis generation. UI copy, loading messages, error states, and tooltips may still reference "Gemini" or be provider-specific.

**Acceptance Criteria:**
- AC-01: All UI copy related to AI thesis generation audited (loading state, success message, error text, tooltips, button labels)
- AC-02: No "Gemini" references remain in production UI copy
- AC-03: Loading, success, and error states are provider-agnostic (e.g. "AI-generated thesis" not "Gemini-generated thesis")
- AC-04: Changes reviewed by Head of UX & Design
- AC-05: Playwright or unit test confirms no "Gemini" text in AI thesis generation flow UI

---

### ST-18 — Arc 5 compliance score in monthly P&L report

**Backlog source:** BLG-FE-38
**Owner:** Financial Reporting & Records Owner; Base44 Frontend
**Effort:** M (~2 days)
**Staging-only ACs:** AC-04 (observable rendering — Playwright required or staging sign-off)

**Problem:** Monthly P&L report (v3.1) covers financial performance only. Arc 5 compliance data is now available (SI-01/03, Arc5ComplianceSection). Adding a compliance section enables holistic monthly review: financial performance + behavioural discipline in one document.

**Acceptance Criteria:**
- AC-01: New "Strategy Compliance" section present in monthly P&L report output (GET /reports/monthly-pnl)
- AC-02: Section includes: validation_pass_rate (period), override_count, red_flag_events_count, most_frequent_rule_breach — sourced from GET /analytics/arc5-compliance data
- AC-03: Section renders correctly in the frontend Monthly P&L view
- AC-04: Playwright test covers: "Strategy Compliance" heading visible, at least 2 metric fields present [staging-only if Playwright mocking not feasible — designate at sprint planning]
- AC-05: No regression to existing P&L report financial sections
