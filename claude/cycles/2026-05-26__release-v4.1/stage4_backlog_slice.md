Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v4.1
Cycle: 2026-05-26__release-v4.1
Last Updated: 2026-05-26

---

# Stage 4 Backlog Slice — v4.1

<!-- release-plan-marker: RP:v4.1:2026-05-26__release-v4.1 -->

**15 stories / 4 EPICs / 2 sprints**

---

## EPIC-01 — Governance Prompt Hardening

**Maps to:** S2-01
**Sprint:** 1
**Owner:** Head of Specs Team
**Description:** Action three carry-forward OA items from v4.0 post-ship closure. OA-01 and OA-02 are 2nd-recurrence escalations; failure to action in v4.1 triggers CLAUDE.md §2 mandated rule. All three items require governed prompt edits with version bumps, OPERATIONAL_GUIDE.md updates, and prompt_change_log.md entries per CLAUDE.md §6.

---

### ST-01 — execution_prompt.md: Add merge-gate re-invocation as hard gate (OA-01)

**EPIC:** EPIC-01
**Backlog refs:** OA-01 (v4.0 closure_record.md §6)
**Effort:** S (~1 day)
**Owner:** Head of Specs Team

**Problem:** STEP 4 merge-gate re-invocation was a recurrence issue in v4.0 (2nd occurrence). The execution prompt lacks a hard gate requiring merge-gate re-invocation before closing an EPIC.

**Acceptance Criteria:**
- AC-01: execution_prompt.md STEP 4 updated to add merge-gate re-invocation as a hard gate (not advisory)
- AC-02: Version bumped per CLAUDE.md §6; OPERATIONAL_GUIDE.md §14 updated to new version
- AC-03: Entry appended to claude/system/prompt_change_log.md referencing OA-01
- AC-04: OA-03 (sprint_close_reminder.yml investigation) documented as PMO Lead task — investigation outcome recorded in cycle notes or cycle_summary.md

---

### ST-02 — sprint_planning_prompt.md + sprint_backlog.md template: Staging-only AC designation at planning (OA-02)

**EPIC:** EPIC-01
**Backlog refs:** OA-02 (v4.0 closure_record.md §6)
**Effort:** S (~1 day)
**Owner:** Head of Specs Team

**Problem:** Staging-only AC designation was not enforced at sprint planning for v4.0. 2nd recurrence — must be added as a mandatory planning check.

**Acceptance Criteria:**
- AC-01: sprint_planning_prompt.md updated to require explicit staging-only AC designation for any story with staging-only evidence requirements
- AC-02: sprint_backlog.md template updated with staging-only AC marker/notation
- AC-03: Version bumped for both files per CLAUDE.md §6; OPERATIONAL_GUIDE.md §14 updated
- AC-04: Entry appended to claude/system/prompt_change_log.md for each file changed, referencing OA-02

---

### ST-03 — delivery_verification_prompt.md: STEP 5.0A pr_number null guard (OA-04)

**EPIC:** EPIC-01
**Backlog refs:** OA-04 (v4.0 closure_record.md §6)
**Effort:** S (~1 day)
**Owner:** Head of Specs Team

**Problem:** delivery_verification_prompt.md STEP 5.0A can fail when pr_number is null — it should detect this condition and recover via gh pr view before sealing.

**Acceptance Criteria:**
- AC-01: delivery_verification_prompt.md STEP 5.0A updated with pr_number null guard: if pr_number=null, recover via `gh pr view <branch> --json number` before proceeding
- AC-02: Version bumped per CLAUDE.md §6; OPERATIONAL_GUIDE.md §14 updated
- AC-03: Entry appended to claude/system/prompt_change_log.md referencing OA-04

---

## EPIC-02 — API Contract Spec Debt Batch 1

**Maps to:** S2-02
**Sprint:** 1
**Owner:** API Contracts Documentation Owner
**Description:** Three endpoints shipped in prior cycles (v3.8, v3.9, v4.0) without formal API contract documents. This EPIC closes the spec debt for SI-01 Pre-Entry Validation, SI-03 Red Flag Journal, and the Arc 5 analytics endpoint. BLG-SPEC-33 (SI-03) must close before EPIC-03 ST-07 (Gemini thesis contract) can commence — the sprint ordering naturally satisfies this gate.

---

### ST-04 — SI-03 Red Flag Journal API contract document (BLG-SPEC-33)

**EPIC:** EPIC-02
**Backlog refs:** BLG-SPEC-33
**Effort:** S (~1 day)
**Owner:** API Contracts Documentation Owner

**Problem:** `GET /portfolio/red-flag-journal` (shipped v3.9) has no formal API contract. Downstream SI-04/SI-05 work references this endpoint; without a contract, downstream specs lack an authoritative source.

**Acceptance Criteria:**
- AC-01: API contract document created at `docs/specs/api_contracts/` for `GET /portfolio/red-flag-journal`
- AC-02: Endpoint heading at `##` level (OpenAPI drift gate compliant per CLAUDE.md §2)
- AC-03: Contract covers: filter parameters, pagination schema, response structure, error codes
- AC-04: Corresponding openapi.yaml entry verified complete
- AC-05: Reviewed by Head of Specs Team and API Contracts Documentation Owner

---

### ST-05 — SI-01 Pre-Entry Validation API contract document (BLG-SPEC-34)

**EPIC:** EPIC-02
**Backlog refs:** BLG-SPEC-34
**Effort:** S (~1 day)
**Owner:** API Contracts Documentation Owner

**Problem:** `GET /portfolio/pre-entry-validation` (shipped v3.8) has no formal API contract. SI-02 and SI-05 will reference validation rule taxonomy and response schema; contract is prerequisite.

**Acceptance Criteria:**
- AC-01: API contract document created at `docs/specs/api_contracts/` for `GET /portfolio/pre-entry-validation`
- AC-02: Endpoint heading at `##` level (OpenAPI drift gate compliant)
- AC-03: Contract covers: rule enumeration, response structure, override acknowledgement path
- AC-04: Corresponding openapi.yaml entry verified complete
- AC-05: Reviewed by Head of Specs Team and API Contracts Documentation Owner

---

### ST-06 — Arc 5 analytics endpoint API contract (BLG-SPEC-40)

**EPIC:** EPIC-02
**Backlog refs:** BLG-SPEC-40
**Effort:** S (~1 day)
**Owner:** API Contracts Documentation Owner

**Problem:** `GET /analytics/arc5-compliance` (shipped v4.0 ST-01) has no formal API contract document. Frontend spec alignment (BLG-FE-48) and future Arc 6 extension planning require an authoritative contract.

**Acceptance Criteria:**
- AC-01: API contract document created at `docs/specs/api_contracts/` for `GET /analytics/arc5-compliance`
- AC-02: Endpoint heading at `##` level (OpenAPI drift gate compliant)
- AC-03: Contract covers: query parameters, response schema (all fields from ST-01 implementation), error codes
- AC-04: Corresponding openapi.yaml entry verified complete
- AC-05: Reviewed by Head of Specs Team and API Contracts Documentation Owner

---

## EPIC-03 — Feature Integration + Quality

**Maps to:** S2-03, S2-04, S2-05, S2-06, S2-07
**Sprint:** 2
**Owner:** Head of Engineering; QA Lead
**Description:** Sprint 2 feature work: Gemini thesis API contract, Arc 5 compliance metrics in P&L, Gemini cost alerting, frontend improvements, and the v4.0 deferred staging verification bundle. ST-07 gates on EPIC-02 ST-04 (BLG-SPEC-33) completion — naturally satisfied by sprint ordering.

---

### ST-07 — Gemini thesis endpoint API contract (BLG-SPEC-38)

**EPIC:** EPIC-03
**Backlog refs:** BLG-SPEC-38
**Effort:** S (~1 day)
**Owner:** API Contracts Documentation Owner; Head of Specs Team
**Gate:** BLG-SPEC-33 (ST-04) must be closed before commencing — ensures consistent contract format

**Problem:** `POST /trade-plans/{plan_id}/generate-thesis` (shipped v4.0 ST-12) has no formal API contract document. BLG-GOV-55 (CLAUDE.md §2 API contract same-sprint rule) prevents future recurrence; this item addresses the v4.0 retroactive debt.

**Acceptance Criteria:**
- AC-01: Gate condition verified — BLG-SPEC-33 (ST-04) closed before commencing
- AC-02: API contract document created at `docs/specs/api_contracts/` for `POST /trade-plans/{plan_id}/generate-thesis`
- AC-03: Endpoint heading at `##` level (OpenAPI drift gate compliant)
- AC-04: Contract covers: request schema (plan_id path param), response schema ({thesis, model_version, prompt_version}), error cases (missing key, invalid plan_id, Gemini error)
- AC-05: openapi.yaml entry verified complete
- AC-06: Reviewed by API Contracts Documentation Owner and Head of Specs Team

---

### ST-08 — Arc 5 compliance metrics P&L integration (BLG-FEAT-40 + BLG-FEAT-42)

**EPIC:** EPIC-03
**Backlog refs:** BLG-FEAT-40, BLG-FEAT-42
**Effort:** M (~3 days — S for FEAT-40, M for FEAT-42)
**Owner:** Metrics Definitions & Analytics Owner; Financial Reporting & Records Owner

**Problem:** Arc 5 compliance data is available from `GET /analytics/arc5-compliance` (shipped v4.0) but is not surfaced in the monthly P&L report. BLG-FEAT-40 defines the composite compliance score formula; BLG-FEAT-42 integrates both formula and raw metrics into the P&L report.

**Acceptance Criteria:**
- AC-01 (FEAT-40): Composite compliance score formula defined in `docs/specs/metrics_definitions.md` (or equivalent canonical spec)
- AC-02 (FEAT-40): Formula documented with input fields and calculation method; reviewed by Metrics Definitions & Analytics Owner and Product Owner
- AC-03 (FEAT-42): Monthly P&L report includes Arc 5 compliance summary section
- AC-04 (FEAT-42): Data sourced from `GET /analytics/arc5-compliance`; fields: validation_pass_rate_by_rule (top 3), override_rate, events_per_week, top_rule_breach
- AC-05 (FEAT-42): Composite score applied if FEAT-40 formula defined; individual components displayed if not
- AC-06 (FEAT-42): Reviewed by Financial Reporting & Records Owner and Product Owner

---

### ST-09 — Gemini API daily cost threshold alert via Telegram (BLG-OPS-34)

**EPIC:** EPIC-03
**Backlog refs:** BLG-OPS-34
**Effort:** M (~2–3 days)
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner

**Problem:** Gemini thesis generation incurs per-request API costs with no automated daily threshold alert. BLG-OPS-26 provides manual monthly review; BLG-OPS-34 adds automated daily monitoring via existing Telegram infrastructure.

**Acceptance Criteria:**
- AC-01: Daily Gemini spend threshold check implemented (configurable via env var; default $1.00/day)
- AC-02: Daily check queries `gemini_audit_log`: sum `estimated_cost_usd` for current day
- AC-03: Telegram alert fires when daily spend exceeds threshold, including daily total and request count
- AC-04: Unit test coverage for threshold logic
- AC-05: Staging verification: threshold alert fires on staging with test data

---

### ST-10 — Frontend: Research view signal_type + Arc5ComplianceSection spec (BLG-FE-44 + BLG-FE-48)

**EPIC:** EPIC-03
**Backlog refs:** BLG-FE-44, BLG-FE-48
**Effort:** S (~1.5 days — XS for FE-44, S for FE-48)
**Owner:** Head of Engineering; Frontend Specs & UX Documentation Owner

**Problem:** BLG-FE-44: Research view lacks signal_type as Setup Type column — stashed from v4.0 sprint execution. BLG-FE-48: Arc5ComplianceSection component shipped v4.0 without a frontend spec document; BLG-FE-48 fills this gap, enabling BLG-FE-40/41 design work and QA-28 E2E test alignment.

**Acceptance Criteria:**
- AC-01 (FE-44): `signal_type` field surfaced as "Setup Type" column in the Research view table
- AC-02 (FE-44): Column visible in the UI on staging; human staging sign-off or Playwright test coverage
- AC-03 (FE-48): Frontend spec document created for Arc5ComplianceSection component
- AC-04 (FE-48): Spec covers: component props, rendering conditions (loading/error/data), stat card layout, data mapping from GET /analytics/arc5-compliance response
- AC-05 (FE-48): Reviewed by Frontend Specs & UX Documentation Owner and Head of Specs Team

---

### ST-11 — Staging Verification Bundle (BLG-QA-28, BLG-QA-29, BLG-QA-30, BLG-OPS-28)

**EPIC:** EPIC-03
**Backlog refs:** BLG-QA-28, BLG-QA-29, BLG-QA-30, BLG-OPS-28
**Effort:** S (~2 days — XS each)
**Owner:** QA Lead; Infrastructure & Operations Owner

**Problem:** Four staging-only ACs were deferred from v4.0 (CLAUDE.md §2 — deferred observable AC pattern). This story closes all four:
- BLG-QA-28: Playwright E2E coverage for Arc5ComplianceSection
- BLG-QA-29: Gemini thesis generation staging verification
- BLG-QA-30: Ticker validation live Yahoo Finance rejection path staging
- BLG-OPS-28: Staging deploy hook live verification (ST-09 v4.0)

**Acceptance Criteria:**
- AC-01 (QA-28/Playwright): Arc5ComplianceSection Playwright tests pass — heading visible, 4 stat card titles visible, loading skeleton shown, error state shown
- AC-02 (QA-29/Gemini staging): POST /trade-plans/{plan_id}/generate-thesis returns thesis on staging with GEMINI_API_KEY set; "Improve with AI" button visible and functional; sign-off date recorded
- AC-03 (QA-30/ticker staging): Ticker validation live Yahoo Finance rejection path verified on staging; sign-off date recorded
- AC-04 (OPS-28/deploy hook): `RENDER_STAGING_DEPLOY_HOOK` secret configured; code-change merge triggers deploy; docs-only commit does not; results recorded as staging sign-off evidence

---

## EPIC-04 — SI-02 Pre-Planning + Security + Ops

**Maps to:** S2-08, S2-09, S2-10, S2-11
**Sprint:** 2
**Owner:** Strategy Rules & System Intent Owner; Infrastructure & Operations Owner
**Description:** Pre-planning work to prepare for SI-02 sprint planning in a future cycle. All stories produce documents or review outputs — no deployment required. Independent from EPIC-03 within Sprint 2.

---

### ST-12 — SI-02 data model gap analysis (BLG-SPEC-39)

**EPIC:** EPIC-04
**Backlog refs:** BLG-SPEC-39
**Effort:** M (~2 days)
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team

**Problem:** SI-02 (position drift monitoring) requires certain fields in trade/position/trade_plan schemas that may not currently exist. A gap analysis is needed before SI-02 sprint planning to define migration scope.

**Acceptance Criteria:**
- AC-01: Gap analysis document produced (path: `docs/specs/` or SI-02 planning folder)
- AC-02: Missing fields enumerated with: data type, source (captured at entry / derivable / new collection), migration complexity estimate
- AC-03: Reviewed by Data Model & Domain Schema Owner, Head of Specs Team, and Head of Backend Engineering before SI-02 sprint planning

---

### ST-13 — SI-02 pre-planning: §13 criteria + data audit + query performance (BLG-GOV-44 + BLG-GOV-46 + BLG-GOV-51)

**EPIC:** EPIC-04
**Backlog refs:** BLG-GOV-44, BLG-GOV-46, BLG-GOV-51
**Effort:** S (~1.5 days — S each)
**Owner:** Strategy Rules & System Intent Owner; Challenger; Head of Engineering

**Problem:** Three SI-02 pre-planning governance items: (1) GOV-44 — pre-define §13 evidence criteria so SI-02's §13 review has a clear pass/fail framework; (2) GOV-46 — audit SI-02 data prerequisites to confirm data density gate status; (3) GOV-51 — assess DB query performance risk for drift monitoring queries before implementation.

**Acceptance Criteria:**
- AC-01 (GOV-44): §13 evidence criteria document produced: assertions verifiable (determinism, display-only, no adaptive learning, no automated action), expected binding conditions
- AC-02 (GOV-44): Reviewed by Strategy Rules & System Intent Owner
- AC-03 (GOV-46): SI-02 data prerequisite audit complete — confirms whether data density gate is met or how many more trade cycles are needed
- AC-04 (GOV-46): Reviewed by Challenger and Product Owner
- AC-05 (GOV-51): DB query performance pre-assessment produced — estimated query cost, recommended index strategy
- AC-06 (GOV-51): Reviewed by Head of Engineering and Head of Backend Engineering

---

### ST-14 — Security review + governance patches (BLG-GOV-49 + BLG-GOV-54 + BLG-GOV-56)

**EPIC:** EPIC-04
**Backlog refs:** BLG-GOV-49, BLG-GOV-54, BLG-GOV-56
**Effort:** S (~1.5 days — S each)
**Owner:** Cybersecurity & Trust Lead; Product Owner; Head of Specs Team

**Problem:** Three governance items: (1) GOV-49 — Gemini API key scope minimization review (security hardening); (2) GOV-54 — SI-05 Phase 1 scope annotation on roadmap; (3) GOV-56 — STEP 12.1 artefact presence check (delivery_verification_prompt enhancement).

**Acceptance Criteria:**
- AC-01 (GOV-49): Gemini API key scope minimization review complete — confirm minimal required scopes; document findings in `docs/security/`
- AC-02 (GOV-49): External API keys register produced and filed; reviewed by Cybersecurity & Trust Lead
- AC-03 (GOV-54): SI-05 Phase 1 scope annotation added to `claude/roadmap/current_roadmap.md` under the SI-05 initiative entry
- AC-04 (GOV-54): Annotation reviewed by Product Owner and Head of Specs Team
- AC-05 (GOV-56): delivery_verification_prompt.md updated with STEP 12.1 artefact presence check
- AC-06 (GOV-56): Version bumped; OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md entry appended

---

### ST-15 — Operational reviews: API performance baseline + Gemini usage + P&L attribution (BLG-OPS-29 + BLG-OPS-30 + BLG-OPS-32)

**EPIC:** EPIC-04
**Backlog refs:** BLG-OPS-29, BLG-OPS-30, BLG-OPS-32
**Effort:** S (~1.5 days — S each)
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Financial Reporting & Records Owner

**Problem:** Three operational review items: (1) OPS-29 — API performance baseline update to include v4.0 new endpoints (POST /trade-plans/{plan_id}/generate-thesis and GET /analytics/arc5-compliance); (2) OPS-30 — first monthly Gemini API usage review (cost + model call pattern); (3) OPS-32 — P&L attribution gate check (confirms plan-linked vs. non-plan trade attribution before Arc 5 compliance integration).

**Acceptance Criteria:**
- AC-01 (OPS-29): `docs/ops/api_performance_baseline.md` updated to include GET /analytics/arc5-compliance and POST /trade-plans/{plan_id}/generate-thesis baseline metrics
- AC-02 (OPS-29): Reviewed by Infrastructure & Operations Owner
- AC-03 (OPS-30): First monthly Gemini usage review complete — total calls, estimated cost, model call pattern documented
- AC-04 (OPS-30): Review findings filed; reviewed by FinOps & Resource Architect and Infrastructure & Operations Owner
- AC-05 (OPS-32): Plan-linked vs. non-plan trade count confirmed in closed trade history
- AC-06 (OPS-32): P&L report handles both cases correctly; any attribution anomalies flagged
- AC-07 (OPS-32): Reviewed by Financial Reporting & Records Owner
