**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.7
**Cycle:** 2026-05-31__release-v4.7
**Published:** 2026-05-31

---

# Stage 4 Backlog Slice — v4.7

---

## EPIC-01 — Arc 5 Completion Pre-work

**Maps to:** S2-01, S2-09
**Owner:** Strategy Rules & System Intent Owner (ST-01); Head of Specs Team / Product Owner (ST-02)
**Sprint:** Sprint 1 (ST-01 firm); Sprint 2 (ST-02 conditional)

SI-04 (Strategy Version Comparison) is the next major Arc 5 feature after SI-02 and SI-03. A §13 pre-assessment must be completed before SI-04 sprint planning seals. SI-05 Phase 1 (Weekly Digest without SI-02) gates on SI-01 + SI-03 live ≥30 days, clearing 2026-06-21.

---

### ST-01 — SI-04 §13 Formal Pre-Assessment (BLG-GOV-62)

**EPIC:** EPIC-01
**Source:** BLG-GOV-62 (P1)
**Effort:** S (~1 day)
**Sprint:** Sprint 1 (firm)
**Delegation:** delegated_decision (Strategy Rules & System Intent Owner)

**Description:**
SI-04 (Strategy Version Comparison) compares trade performance before and after strategy rule changes. Before SI-04 sprint planning seals, a formal §13 review must confirm this feature constitutes display-only historical analysis — not adaptive or predictive output. Last-minute §13 discoveries have blocked prior arcs; pre-assessment eliminates this risk for Arc 5 completion.

**Acceptance Criteria:**
- AC-01: §13 review checklist applied against SI-04 feature description (roadmap §2c Arc 5 and initiative_register.md SI-04 scope)
- AC-02: Determination documented: PASS or CONDITIONAL (with binding conditions) or FAIL
- AC-03: Binding conditions (if any) documented, analogous to IT-06 §13 PASS conditions (4 binding conditions model)
- AC-04: Assessment document produced at `docs/product/decisions/si04_section13_preassessment.md` (Class 3 Operational Record)
- AC-05: Strategy Rules & System Intent Owner sign-off recorded in the assessment document
- AC-06: BLG-GOV-62 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** None — document-only story.

---

### ST-02 — SI-05 Phase 1 Implementation (BLG-GOV-67) [CONDITIONAL]

**EPIC:** EPIC-01
**Source:** BLG-GOV-67 (P2)
**Effort:** M (~2–3 days)
**Sprint:** Sprint 2 (conditional — gate: SI-01 + SI-03 live ≥30 days = 2026-06-21)
**Delegation:** autonomous

**Gate:** Product Owner confirms SI-01 and SI-03 have been live for ≥30 days before Sprint 2 planning seals.

**Description:**
BLG-GOV-54 (shipped v4.1) defined a phased SI-05 delivery. Phase 1 delivers the Weekly Strategy Integrity Digest using SI-01 + SI-03 data only (validation pass rate, override count, red flag frequency trend) — no SI-02 dependency. Extends the existing Telegram weekly digest (shipped v2.4). Gate clears 2026-06-21.

**Acceptance Criteria:**
- AC-01: POST /portfolio/weekly-integrity-digest endpoint (or equivalent Telegram dispatch trigger) implemented
- AC-02: Digest content: validation_pass_rate (7-day period), override_count (7-day), red_flag_events_count (7-day), most_frequent_rule_breach
- AC-03: Data sourced from GET /analytics/arc5-compliance (validation_pass_rate_by_rule) and GET /portfolio/red-flag-journal (red_flag_events_count)
- AC-04: No SI-02 (behavioural drift) data in Phase 1 output — Phase 1 is SI-01 + SI-03 only
- AC-05: Digest dispatched to Telegram via existing alert infrastructure (v2.4 weekly digest pattern)
- AC-06: Unit tests: digest content generation with mock data; Telegram dispatch verified
- AC-07: Playwright scenario: trigger digest endpoint; confirm digest content includes compliance and red-flag data
- AC-08: API contract document produced: `docs/specs/api_contracts/weekly_integrity_digest_contract.md` — in same sprint as endpoint
- AC-09: openapi.yaml updated with new endpoint in same commit as contract
- AC-10: New endpoint registered in backend/routers/test.py in same commit
- AC-11: BLG-GOV-67 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** AC-05 (Telegram dispatch) — verified on staging with real Telegram bot token.

---

## EPIC-02 — User-Facing Analytics Enhancement

**Maps to:** S2-02
**Owner:** Head of Backend Engineering; Financial Reporting & Records Owner
**Sprint:** Sprint 1 (firm)

Arc 5 compliance data (shipped v4.0 analytics endpoint) has not yet been integrated into the monthly P&L report. BLG-FEAT-38 has been deferred from Provisional-Target v4.1 for 3+ cycles. Gate cleared (BLG-FEAT-36/37 complete v4.0).

---

### ST-03 — Arc 5 Compliance Score in Monthly P&L Report (BLG-FEAT-38)

**EPIC:** EPIC-02
**Source:** BLG-FEAT-38 (P2, aged 3+ cycles)
**Effort:** M (~2 days)
**Sprint:** Sprint 1 (firm)
**Delegation:** autonomous

**Description:**
The monthly P&L report (shipped v3.1, GET /reports/monthly-pnl) covers financial performance only. Adding a strategy compliance section produces a holistic monthly review: financial performance + behavioural discipline. Data is sourced from GET /analytics/arc5-compliance (shipped v4.0).

**Acceptance Criteria:**
- AC-01: GET /reports/monthly-pnl response includes a `compliance_summary` section when Arc 5 data is available
- AC-02: `compliance_summary` fields: `validation_pass_rate` (period), `override_count`, `red_flag_events_count`, `most_frequent_rule_breach`
- AC-03: Data sourced from GET /analytics/arc5-compliance — no duplicate data computation
- AC-04: Section absent (or shows "No compliance data" message) when Arc 5 data is unavailable for the period
- AC-05: Existing monthly P&L fields unaffected — additive change only
- AC-06: Unit tests: compliance section present with mock Arc 5 data; absent when data unavailable
- AC-07: Playwright scenario: GET /reports/monthly-pnl response includes compliance_summary with valid data
- AC-08: openapi.yaml updated: monthly-pnl response schema includes compliance_summary (optional field)
- AC-09: BLG-FEAT-38 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** None — testable in CI with mock data.

---

## EPIC-03 — Staging Verifications & Ops Housekeeping

**Maps to:** S2-03, S2-04, S2-05, S2-06
**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner
**Sprint:** Sprint 1 (firm)

Clears v4.6 OA items (BLG-OPS-44, BLG-OPS-45) and aged staging verification (BLG-OPS-28) plus ops hygiene item (BLG-OPS-31).

---

### ST-04 — Staging Deploy Live Verification (BLG-OPS-28)

**EPIC:** EPIC-03
**Source:** BLG-OPS-28 (P2, aged 4+ cycles; Provisional-Target: v4.1)
**Effort:** XS (~0.5 day)
**Sprint:** Sprint 1 (firm)
**Delegation:** delegated_decision (Infrastructure & Operations Owner)

**Description:**
ST-09 (v4.0, BLG-OPS-27) implemented the staging auto-deploy workflow. The AC "staging auto-deploys on main merge" is a staging-only criterion requiring the RENDER_STAGING_DEPLOY_HOOK secret and a live merge to verify. This item completes that verification and closes BLG-OPS-28.

**Acceptance Criteria:**
- AC-01: RENDER_STAGING_DEPLOY_HOOK secret confirmed configured in GitHub repo settings
- AC-02: A code-change commit merged to main triggers a Render staging deploy (confirmed in Render dashboard)
- AC-03: A docs-only commit does not trigger deploy (path filter verified)
- AC-04: Staging sign-off evidence recorded in a verification note at `docs/ops/staging_deploy_verification.md` (date, result, confirming role)
- AC-05: BLG-OPS-28 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** AC-02, AC-03 — require live Render environment.

---

### ST-05 — DS-07 Migration Staging Verification (BLG-OPS-44)

**EPIC:** EPIC-03
**Source:** BLG-OPS-44 (P3, Provisional-Target: v4.7)
**Effort:** XS (~0.5 hr)
**Sprint:** Sprint 1 (firm)
**Delegation:** delegated_decision (Infrastructure & Operations Owner; Data Model & Domain Schema Owner)

**Description:**
ST-01 v4.6 (DS-07 migration) added 5 nullable columns and 3 indexes to trade_plans. AC-05 was pre-designated staging-only and deferred to Phase 4. This item completes the staging verification.

**Acceptance Criteria:**
- AC-01: DS-07 migration applied to staging environment with no errors
- AC-02: `\d trade_plans` confirms all 5 SI-02 columns present: signal_id, risk_percent_used, portfolio_value_at_entry, pre_entry_validation_snapshot, effective_settings_snapshot
- AC-03: 3 indexes confirmed created: idx_trade_plans_signal, idx_trade_history_exit_date, idx_trade_history_entry_date
- AC-04: Staging verification date and results recorded in a verification note
- AC-05: BLG-OPS-44 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** AC-01, AC-02, AC-03 — require live staging database.

---

### ST-06 — Severity Field Staging Verification (BLG-OPS-45)

**EPIC:** EPIC-03
**Source:** BLG-OPS-45 (P3, Provisional-Target: v4.7)
**Effort:** XS (~0.5 hr)
**Sprint:** Sprint 1 (firm)
**Delegation:** delegated_decision (Infrastructure & Operations Owner; Data Model & Domain Schema Owner)

**Description:**
ST-09 v4.6 (BLG-BE-16: severity field) added a severity column to red_flag_events. ACs AC-01/02/03 were pre-designated staging-only. AC-08 (Data Model & Domain Schema Owner sign-off) was pending. This item completes both.

**Acceptance Criteria:**
- AC-01: `\d red_flag_events` confirms severity column present on staging
- AC-02: Default severity assignment verified: pre_entry_override events → warning; others → info
- AC-03: Backfill confirmed: no null severity values in existing events
- AC-04: Data Model & Domain Schema Owner sign-off recorded in verification note
- AC-05: BLG-OPS-45 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** AC-01, AC-02, AC-03 — require live staging database.

---

### ST-07 — Render Log Retention Policy (BLG-OPS-31)

**EPIC:** EPIC-03
**Source:** BLG-OPS-31 (P2)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1 (firm)
**Delegation:** delegated_decision (Infrastructure & Operations Owner)

**Description:**
Review Render's log retention policy and confirm whether database audit tables (gemini_audit_log, red_flag_events) provide sufficient durable audit trail independent of Render's platform logs. Document the policy decision.

**Acceptance Criteria:**
- AC-01: Render log retention policy reviewed (current plan limits documented)
- AC-02: Database audit tables assessed as durable (gemini_audit_log, red_flag_events) — confirmed or flagged
- AC-03: Policy decision documented: "Render logs + database tables sufficient" or "additional archiving required"
- AC-04: Findings filed at `docs/ops/render_log_retention_policy.md` (Class 3 Operational Record)
- AC-05: BLG-OPS-31 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** None — document-only story.

---

## EPIC-04 — Cost & UX Assessments

**Maps to:** S2-07, S2-08
**Owner:** FinOps & Resource Architect (S2-07); Head of UX & Design (S2-08)
**Sprint:** Sprint 1 (firm)

BLG-OPS-37 gate cleared (BLG-OPS-36 monthly review complete v4.2). BLG-FE-49 unscheduled P2 item ready for inclusion.

---

### ST-08 — Anthropic API Tier Cost Assessment (BLG-OPS-37)

**EPIC:** EPIC-04
**Source:** BLG-OPS-37 (P2, gate cleared: BLG-OPS-36 complete v4.2)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1 (firm)
**Delegation:** delegated_decision (FinOps & Resource Architect)

**Description:**
BLG-OPS-36 (Claude API first monthly review) completed in v4.2. With usage data available, this item defines the threshold at which a paid-tier upgrade becomes cost-effective.

**Acceptance Criteria:**
- AC-01: Anthropic API pricing tiers reviewed against actual usage from BLG-OPS-36 monthly review
- AC-02: Usage threshold defined: point at which paid-tier upgrade is cost-effective
- AC-03: Decision framework documented at `docs/ops/anthropic_api_tier_assessment.md`
- AC-04: FinOps & Resource Architect sign-off recorded
- AC-05: BLG-OPS-37 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** None — document-only story.

---

### ST-09 — Pre-Entry Validation Panel UX Assessment (BLG-FE-49)

**EPIC:** EPIC-04
**Source:** BLG-FE-49 (P2)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1 (firm)
**Delegation:** delegated_decision (Head of UX & Design)

**Description:**
PreEntryValidationPanel (shipped v3.8) will need to surface additional Arc 5 context as SI-02, SI-04, SI-05 ship. A UX assessment of current layout, density, and override acknowledgement flow identifies improvement opportunities before Arc 5 completion forces ad-hoc changes.

**Acceptance Criteria:**
- AC-01: PreEntryValidationPanel reviewed: layout clarity, text density, override acknowledgement UX
- AC-02: Improvement candidates identified and ranked by effort/value
- AC-03: Assessment note produced at `docs/product/ux/pre_entry_panel_ux_assessment.md`
- AC-04: Head of UX & Design sign-off recorded
- AC-05: No implementation committed — assessment only; implementation items filed as backlog entries if warranted
- AC-06: BLG-FE-49 marked COMPLETE in backlog with date and cycle reference

**Staging-only ACs:** None — assessment-only story.
