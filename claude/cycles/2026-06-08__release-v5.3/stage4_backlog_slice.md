Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v5.3
Cycle: 2026-06-08__release-v5.3
Last Updated: 2026-06-08

---

# Backlog Slice — v5.3 Spec Debt, Security Hardening & Ops Governance

## EPIC-01 — API Contract & Spec Debt Resolution

**Maps to:** S2-01, S2-02, S2-03, S2-04, S2-05, S2-06, S2-07
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Sprint:** 1
**Merge order:** Sprint 1, first group (merge after EPIC-02)

Close all 6 API contract gaps identified in the v5.2 endpoint coverage audit (BLG-GOV-100). Produce a resolution plan and QA acceptance criteria first, then author the contracts and openapi.yaml entries. Conduct a completeness audit of all 50 routes against openapi.yaml.

---

### ST-01 — BLG-SPEC-53: API contract gap resolution plan

**S2-ID:** S2-01
**Priority:** P1
**Delegation:** autonomous
**Effort:** M (~1–2 days)
**Spec ref:** BLG-SPEC-53 (backlog.md)

**Acceptance Criteria:**
- Resolution plan document produced (docs/specs/ or claude/cycles/2026-06-08__release-v5.3/) covering all 6 endpoint contract gaps from BLG-SPEC-49–52
- Priority-ranked gap list: by risk (auth exposure, external-facing vs internal, complexity)
- Sprint scope recommendation for v5.3: which gaps ship in which story vs consolidated
- Confirmation of whether additional openapi.yaml gaps exist beyond BLG-SPEC-49–52 (preliminary finding — formal answer from ST-02)
- Head of Specs Team and API Contracts & Documentation Owner sign-off

---

### ST-02 — BLG-SPEC-54: openapi.yaml completeness audit

**S2-ID:** S2-02
**Priority:** P1
**Delegation:** autonomous
**Effort:** S (~0.5–1 day)
**Spec ref:** BLG-SPEC-54 (backlog.md)

**Acceptance Criteria:**
- All 50 routes from backend/routers/ enumerated and compared against docs/reference/openapi.yaml
- Gap report produced: routes present in contract files but absent from openapi.yaml
- openapi.yaml updated for any confirmed gaps found in this audit (beyond BLG-SPEC-49–52)
- Any additional gaps filed as new backlog items (BLG-SPEC-55+) if found
- API Contracts & Documentation Owner sign-off

---

### ST-03 — BLG-QA-51: QA acceptance criteria for SPEC-49–52

**S2-ID:** S2-03
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5 day)
**Spec ref:** BLG-QA-51 (backlog.md)

**Acceptance Criteria:**
- QA readiness document produced defining AC template for endpoint contract stories: what constitutes a "complete" contract (## METHOD /path at ## level, openapi.yaml entry, test.py entry where applicable, SystemStatus fallback count updated where test.py count changes)
- AC template applied to all 6 gaps in BLG-SPEC-49–52
- Template reusable for future endpoint contract gap stories
- Director of Quality sign-off

---

### ST-04 — BLG-SPEC-49: GET /ai/journal-summary/history contract

**S2-ID:** S2-04
**Priority:** P2
**Delegation:** autonomous
**Effort:** XS (~1–2 hours)
**Spec ref:** BLG-SPEC-49 (backlog.md)
**Depends on:** ST-03 (QA AC template) within EPIC-01

**Acceptance Criteria:**
- `## GET /ai/journal-summary/history` heading added to docs/specs/api_contracts/ai_endpoints.md (##-level, not ###)
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---

### ST-05 — BLG-SPEC-50: GET /analytics/compliance-metrics contract

**S2-ID:** S2-05
**Priority:** P2
**Delegation:** autonomous
**Effort:** XS (~1–2 hours)
**Spec ref:** BLG-SPEC-50 (backlog.md)
**Depends on:** ST-03 within EPIC-01

**Acceptance Criteria:**
- `## GET /analytics/compliance-metrics` heading added to docs/specs/api_contracts/analytics_endpoints.md (##-level)
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---

### ST-06 — BLG-SPEC-51: GET /news/{ticker} contract

**S2-ID:** S2-06
**Priority:** P2
**Delegation:** autonomous
**Effort:** XS (~1–2 hours)
**Spec ref:** BLG-SPEC-51 (backlog.md)
**Depends on:** ST-03 within EPIC-01

**Acceptance Criteria:**
- A file in docs/specs/api_contracts/ contains `## GET /news/{ticker}` as a ##-level heading
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---

### ST-07 — BLG-SPEC-52: Watchlist endpoint contracts + test.py

**S2-ID:** S2-07
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5 day)
**Spec ref:** BLG-SPEC-52 (backlog.md)
**Depends on:** ST-03 within EPIC-01

**Acceptance Criteria:**
- A file in docs/specs/api_contracts/ contains `## GET /watchlist`, `## POST /watchlist`, `## DELETE /watchlist/{entry_id}` as ##-level headings
- openapi.yaml updated with all three path entries
- backend/routers/test.py entries added for all three watchlist endpoints
- SystemStatus.js fallback count and SC-SS-01b in tests/e2e/system-status.spec.js updated to reflect new test.py count (per CLAUDE.md §2)
- API Contracts & Documentation Owner and Head of Specs Team sign-off

---

## EPIC-02 — Security & Ops Hardening

**Maps to:** S2-08, S2-09, S2-10
**Owner:** Head of Engineering; Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Sprint:** 1
**Merge order:** Sprint 1, merge first (before EPIC-01)

Add API key authentication to the unauthenticated SI-05 digest endpoint. Add automated failure alerting when SI-05 Telegram delivery fails. Add CI secret scanning to prevent accidental credential commits.

---

### ST-08 — BLG-BE-35: POST /digest/si05/send API key authentication

**S2-ID:** S2-08
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5 day)
**Spec ref:** BLG-BE-35 (backlog.md); security_register.md Review 003

**Acceptance Criteria:**
- POST /digest/si05/send requires API key authentication per the existing pattern (Depends injection, consistent with other protected endpoints)
- 401 returned on unauthenticated request
- Unit test added verifying 401 behaviour on unauthenticated POST /digest/si05/send
- docs/specs/api_contracts/digest_endpoints.md authentication requirements section updated
- Cybersecurity & Trust Lead and Head of Engineering sign-off

---

### ST-09 — BLG-OPS-57: SI-05 Telegram delivery failure alerting

**S2-ID:** S2-09
**Priority:** P1
**Delegation:** autonomous
**Effort:** S (~0.5–1 day)
**Spec ref:** BLG-OPS-57 (backlog.md)

**Acceptance Criteria:**
- Failed digest delivery is logged with status=FAILED in si05_digest_log
- A human-observable alert is triggered: Render log at ERROR level minimum (retry logic per BLG-BE-32 still applies before alert fires)
- Delivery failure alerting documented in docs/operations/deployment_runbook.md
- Infrastructure & Operations Owner sign-off

---

### ST-10 — BLG-OPS-58: CI secret scanning gate

**S2-ID:** S2-10
**Priority:** P1
**Delegation:** autonomous
**Effort:** S (~0.5–1 day)
**Spec ref:** BLG-OPS-58 (backlog.md)

**Acceptance Criteria:**
- Secret scanning step added to GitHub Actions CI pipeline (gitleaks or trufflehog)
- Configured to scan for: Telegram bot token patterns, Anthropic API key patterns, Supabase URL/key patterns, generic high-entropy strings
- CI fails and blocks merge when a real-looking secret is detected
- Confirmed to detect a test dummy token before allowlisting it
- Allowlist documented for any confirmed false positives (.gitleaks.toml or equivalent)
- Cybersecurity & Trust Lead sign-off

---

## EPIC-03 — Governance Patches & Policy

**Maps to:** S2-11, S2-12, S2-13, S2-14, S2-15, S2-16, S2-17
**Owner:** Head of Specs Team; Strategy Rules & System Intent Owner; AI Compliance Governance Officer
**Sprint:** 2
**Merge order:** Sprint 2, merge first (before EPIC-04)

Apply carry-forward lessons learnt governance patches (CF-1/CF-2). Define precise SI-02 frontend gate conditions. Author AI governance policies (model pin update, audit log retention). Conduct Arc 4 trade plan data completeness audit. Perform first annual strategy_rules.md §11 parameter validation.

---

### ST-11 — LL-v5.2-P4-01: qa_evidence_template.md signer format note

**S2-ID:** S2-11
**Priority:** P1 (carry-forward OA)
**Delegation:** autonomous
**Effort:** S (~1–2 hours)
**Spec ref:** lessons_learnt_closure.md CF-1 (2026-06-08__release-v5.2)

**Acceptance Criteria:**
- claude/system/templates/qa_evidence_template.md updated with explicit signer format guidance note for mixed-class EPICs (delegated_backend + autonomous stories in same EPIC)
- Note specifies: signer field must follow `"Sprint Execution Engine (agent-mediated, <Role Name> role — §X.Y)"` format exactly for mixed-class EPICs
- Governance compliance checklist (CLAUDE.md §6): version bumped, OPERATIONAL_GUIDE.md §14 updated, prompt_change_log.md entry appended
- Head of Specs Team sign-off

---

### ST-12 — LL-v5.2-P4-02: execution_prompt.md STEP 5.3A SSR sub-step

**S2-ID:** S2-12
**Priority:** P1 (carry-forward OA)
**Delegation:** autonomous
**Effort:** S (~1–2 hours)
**Spec ref:** lessons_learnt_closure.md CF-2 (2026-06-08__release-v5.2)

**Acceptance Criteria:**
- claude/system/execution_prompt.md STEP 5.3A updated with sub-step: "if System_status_report.md does not yet have a section for the current cycle_id, create it using the System_status_report section template"
- Governance compliance checklist (CLAUDE.md §6): version bumped, OPERATIONAL_GUIDE.md §14 updated, prompt_change_log.md entry appended in same commit
- Head of Specs Team sign-off

---

### ST-13 — BLG-GOV-107: SI-02 frontend activation criteria precision

**S2-ID:** S2-13
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5–1 day)
**Spec ref:** BLG-GOV-107 (backlog.md)

**Acceptance Criteria:**
- 2–3 specific, checkable gate conditions defined for SI-02 frontend sprint planning activation (e.g.: 20+ closed trades with linked trade_plans; GET /analytics/behavioural-drift p99 < 2s confirmed stable; drift scores confirmed meaningful per BLG-GOV-92 Phase 2 criteria)
- current_roadmap.md SI-02 entry updated with precise gate conditions replacing "~Nov 2026"
- PMO Lead and Product Owner sign-off

---

### ST-14 — BLG-GOV-108: AI model pin update policy

**S2-ID:** S2-14
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5–1 day)
**Spec ref:** BLG-GOV-108 (backlog.md)

**Acceptance Criteria:**
- Model pin update policy documented (appended to BLG-GOV-64 policy document or companion doc)
- Policy covers: trigger (new Claude model release or deprecation notice), process (review release notes, run test suite against new model, document cost/quality trade-off), required sign-offs (AI Compliance Governance Officer + Head of Engineering), timeline (updates must complete within 30 days of deprecation notice)
- AI Compliance Governance Officer and Head of Engineering sign-off

---

### ST-15 — BLG-GOV-109: AI audit log retention policy

**S2-ID:** S2-15
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5 day)
**Spec ref:** BLG-GOV-109 (backlog.md)

**Acceptance Criteria:**
- Retention period defined and documented for claude_audit_log entries (recommended: 12 months or aligned with Supabase retention policy from BLG-OPS-53)
- Cleanup mechanism implemented: scheduled cleanup job or Supabase row-level TTL for entries older than retention period
- Policy documented in docs/compliance/ or existing AI audit log spec
- AI Compliance Governance Officer and Infrastructure & Operations Owner sign-off

---

### ST-16 — BLG-GOV-110: Arc 4 trade_plan data completeness audit

**S2-ID:** S2-16
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5–1 day)
**Spec ref:** BLG-GOV-110 (backlog.md)

**Acceptance Criteria:**
- Per-field null% computed for all trade_plans optional fields: entry_rationale, confirmation_criteria, r_target, setup_type, pre_entry_validation_snapshot
- Fields with >50% null rate flagged as "data gaps" with Arc 4 dependency risk noted
- Data completeness report produced
- If gaps are critical to Arc 4 features: backlog items filed for UI/UX improvements
- Data Model & Domain Schema Owner and Product Owner sign-off

---

### ST-17 — BLG-GOV-104: strategy_rules.md §11 parameter validation

**S2-ID:** S2-17
**Priority:** P2
**Delegation:** autonomous
**Effort:** M (~1–2 days)
**Spec ref:** BLG-GOV-104 (backlog.md)

**Acceptance Criteria:**
- All closed trades pulled from production database; per-parameter outcomes computed
- ATR multiplier: initial stop placement vs ATR validated
- Regime gate: entries blocked count; pass rate for allowed entries
- Position sizing: documented formula verified against UI implementation
- Parameter validation document produced; changes recommended or "no change needed" confirmed
- If <20 closed trades: document findings as "insufficient data" with count recorded
- Strategy Rules & System Intent Owner sign-off; Product Owner ratifies any recommended parameter changes

---

## EPIC-04 — QA, Testing & Frontend Review

**Maps to:** S2-18, S2-19, S2-20, S2-21, S2-22
**Owner:** Director of Quality; QA Lead; Base44 Frontend Prompt Owner
**Sprint:** 2
**Merge order:** Sprint 2, merge after EPIC-03
**Cross-sprint dependency:** BLG-QA-54 (ST-20) must run after EPIC-01 contract authoring is merged to main

Validate tax year P&L boundary edge cases. Add Playwright E2E coverage for SI-05 digest. Update coverage matrix post-v5.2 (including EPIC-01 contract additions). Conduct Red Flag Journal UX review. Define BLG-FE-64 scope.

---

### ST-18 — BLG-QA-52: Tax year P&L boundary edge case validation

**S2-ID:** S2-18
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5–1 day)
**Spec ref:** BLG-QA-52 (backlog.md)

**Acceptance Criteria:**
- Tax year boundary logic identified in GET /reports/monthly-pnl or annual equivalent
- Test data scenarios created: trade opened Dec 31 / closed April 7 (straddling UK tax year boundary); trade opened April 4 / closed April 8
- P&L attribution confirmed correct for all boundary cases (or bug filed as BLG-BE-36+ if incorrect)
- Financial Reporting & Records Owner and QA Lead sign-off

---

### ST-19 — BLG-QA-53: SI-05 digest Playwright E2E coverage

**S2-ID:** S2-19
**Priority:** P2
**Delegation:** autonomous
**Effort:** M (~1–2 days)
**Spec ref:** BLG-QA-53 (backlog.md)

**Acceptance Criteria:**
- ≥3 Playwright E2E scenarios for SI-05 digest delivery implemented and passing in CI
- Scenarios cover: (1) happy path delivery, (2) empty red flag scenario (empty state), (3) compliance score present in digest
- Telegram API mocked or stubbed to avoid real API calls in CI
- QA Lead sign-off

---

### ST-20 — BLG-QA-54: Playwright coverage matrix update post-v5.2

**S2-ID:** S2-20
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5 day)
**Spec ref:** BLG-QA-54 (backlog.md)
**Depends on:** EPIC-01 (ST-04–ST-07) merged to main — coverage matrix must capture new contract docs

**Acceptance Criteria:**
- All Playwright E2E test scenarios post-v5.2 counted (tests/e2e/*.spec.js)
- Coverage matrix updated to include all new scenarios added in v5.2 and v5.3 EPIC-01/EPIC-04
- New scenarios mapped to their corresponding feature ACs
- Coverage gaps identified and noted
- Director of Quality sign-off

---

### ST-21 — BLG-FE-66: Red Flag Journal post-launch UX review

**S2-ID:** S2-21
**Priority:** P3
**Delegation:** autonomous
**Effort:** S (~0.5–1 day)
**Spec ref:** BLG-FE-66 (backlog.md)

**Acceptance Criteria:**
- UX review document produced covering: filter UX clarity, pagination interaction, empty state messaging, table readability
- Top-3 friction points documented with proposed improvements
- Any significant friction filed as a separate backlog item (BLG-FE-68+)
- Base44 Frontend Prompt Owner and Head of UX & Design sign-off

---

### ST-22 — BLG-FE-67: BLG-FE-64 visual design review scope definition

**S2-ID:** S2-22
**Priority:** P2
**Delegation:** autonomous
**Effort:** S (~0.5 day)
**Spec ref:** BLG-FE-67 (backlog.md)
**Gate:** BLG-FE-64 gate clears 2026-06-21 — scope definition should complete before or at that date

**Acceptance Criteria:**
- Precise scope of BLG-FE-64 defined: which visual elements (typography, colours, spacing, component consistency — specify which), which pages/components, what acceptance criteria look like
- Clear distinction from BLG-FE-66 documented (visual design vs interaction design)
- One-page scope document produced usable as BLG-FE-64 story AC at sprint planning
- Frontend Specs & UX Documentation Owner and Head of UX & Design sign-off

---

## Conditional Stories

*Add to sprint planning if gates clear before sprint planning seals.*

| ST-ID | EPIC | Gate | Item | Priority |
|-------|------|------|------|----------|
| ST-23 | EPIC-03 | Before 2026-07-01 | BLG-GOV-113 — SI-05 effectiveness review protocol | P1 |
| ST-24 | EPIC-03 | Before 2026-07-01 | BLG-GOV-114 — si05_digest_log schema validation | P1 |
| ST-25 | EPIC-04 | 2026-06-21 | BLG-FE-64 — RFJ visual design review pre-brief | P2 |

**BLG-GOV-113 AC summary:** SI-05 effectiveness review protocol document produced specifying: participants (Product Owner + Director of Quality), evidence sources (si05_digest_log, BLG-GOV-96 criteria, RFJ view counts post-delivery), output format, decision authority. Must complete by 2026-07-01.

**BLG-GOV-114 AC summary:** si05_digest_log schema validated against BLG-GOV-96 effectiveness criteria fields (send_at, status, recipient, content hash). PASS or urgent gap stories filed. Must complete before 2026-07-01.

**BLG-FE-64 AC summary:** RFJ visual design review conducted; findings documented in a pre-brief report; follow-up backlog items filed for any design improvements identified.

---

## Pre-Sprint Planning Required Decisions

The following must be resolved before sprint planning seals:

- [ ] **OA-RP-01** [RISK-03] — PT-04 trade count gate re-verification: query `SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL`. If ≥ 20 trades: PT-04 (M effort) must enter v5.3 scope (EPIC-04 or new EPIC); capacity must be re-assessed. Owner: PMO Lead; Product Owner.
- [ ] **BLG-GOV-106** action — update PT-04 gate status in current_roadmap.md and BLG-FEAT-25 with current count regardless of gate outcome.
- [ ] **Conditional gate check** — confirm whether BLG-GOV-113, BLG-GOV-114, BLG-FE-64 gates have cleared; add as ST-23/24/25 if so.
