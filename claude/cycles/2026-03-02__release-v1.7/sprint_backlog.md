**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Cycle:** 2026-03-02__release-v1.7
**Last Updated:** 2026-03-02

---

# Sprint Backlog — v1.7 Foundation & Governance

## Product Owner Sign-off

Signed off by: Product Owner
Date: 2026-03-02
Comments: All acceptance criteria reviewed and approved. Sprint scope matches stage4_backlog_slice.md. Proceeding to execution.

---

## Sprint Goal

Establish the foundational governance, quality, and specification artefacts required to unlock v1.8 pre-alignment and v2.0 pre-alignment, and resolve outstanding spec debt items identified in the QWB review.

---

## EPIC-01 — CI/CD Merge Gate Implementation

**Branch:** exec/v1.7-foundation
**Maps to:** S2-01 (BLG-TECH-04)
**Priority:** P2

### ST-01 — Author validate-analytics.yml workflow
**Classification:** delegated_backend
**Assigned to:** Head of Engineering
**Acceptance Criteria:**
- `.github/workflows/validate-analytics.yml` exists and triggers on PR + push to main/develop
- Merge blocked on any critical-severity validation failure (`critical_failed > 0`)
- Calls `POST /validate/calculations` endpoint
- Non-critical failures produce warning comment only

### ST-02 — Test workflow on real/dry-run PR
**Classification:** delegated_backend
**Assigned to:** Head of Engineering
**Acceptance Criteria:**
- Workflow executes successfully on a test PR
- Blocking behaviour confirmed for critical failures
- Warning-only behaviour confirmed for non-critical failures

### ST-03 — Verify PR comment content
**Classification:** delegated_qa
**Assigned to:** QA & Testing Owner
**Acceptance Criteria:**
- PR comment shows summary with severity breakdown
- Comment format matches specification

### ST-04 — Director of Quality sign-off
**Classification:** delegated_qa
**Assigned to:** Director of Quality
**Acceptance Criteria:**
- Director of Quality confirms EPIC-01 acceptance criteria are met
- Sign-off recorded in qa_evidence_EPIC-01.md

---

## EPIC-02 — Strategy Boundaries Governance Review

**Branch:** exec/v1.7-epic02-strategy-boundaries
**Maps to:** S2-02
**Priority:** P1

### TASK-01 — Conduct §13 boundary review session
**Classification:** delegated_decision
**Assigned to:** Strategy Rules & System Intent Owner + Product Owner
**Acceptance Criteria:**
- Review session completed with both owners present
- All three features explicitly reviewed against §13 principles

### TASK-02 — Document boundary findings
**Classification:** delegated_decision
**Assigned to:** Strategy Rules & System Intent Owner + Product Owner
**Acceptance Criteria:**
- Boundary finding documented for Signal Parameter Exposure (4.3)
- Boundary finding documented for AI Journal Summarisation
- Boundary finding documented for New Technical Indicators

### TASK-03 — Update strategy_rules.md if needed
**Classification:** autonomous
**Assigned to:** Strategy Rules & System Intent Owner
**Acceptance Criteria:**
- strategy_rules.md updated with version increment if boundaries changed
- If no change required: documented explicitly in decision record

### TASK-04 — File decision record
**Classification:** autonomous
**Assigned to:** Product Owner
**Acceptance Criteria:**
- Decision record filed at `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md`
- Lifecycle-compliant Class 4 header present
- All three features explicitly addressed

### TASK-05 — Head of Specs Team lifecycle sign-off
**Classification:** delegated_decision
**Assigned to:** Head of Specs Team
**Acceptance Criteria:**
- Head of Specs Team lifecycle sign-off obtained and recorded
- §13-gated features cleared to proceed per stated conditions

---

## EPIC-03 — Portfolio Heat Definition in Metrics Spec

**Branch:** exec/v1.7-epic03-metrics
**Maps to:** S2-03
**Priority:** P1 (v1.8 hard gate)

### TASK-06 — Define canonical Position Risk formula
**Classification:** autonomous
**Assigned to:** Metrics Definitions & Analytics Owner
**Acceptance Criteria:**
- Position Risk formula defined with GBP adjustment and FX handling
- Formula is explicit and canonical (not indicative)

### TASK-07 — Define canonical Portfolio Heat formula
**Classification:** autonomous
**Assigned to:** Metrics Definitions & Analytics Owner
**Acceptance Criteria:**
- Portfolio Heat formula defined canonically
- Relationship to Position Risk clearly stated

### TASK-08 — Define display thresholds
**Classification:** autonomous
**Assigned to:** Metrics Definitions & Analytics Owner
**Acceptance Criteria:**
- Display thresholds are explicit numeric bands (not indicative ranges)
- Thresholds documented with visual guidance

### TASK-09 — Update metrics_definitions.md
**Classification:** autonomous
**Assigned to:** Metrics Definitions & Analytics Owner
**Acceptance Criteria:**
- `docs/specs/metrics_definitions.md` updated with all Portfolio Risk Metrics
- Version incremented per lifecycle guide §5 (minor version bump for new section)

### TASK-10 — Head of Specs Team sign-off
**Classification:** delegated_decision
**Assigned to:** Head of Specs Team
**Acceptance Criteria:**
- Head of Specs Team sign-off obtained
- v1.8 pre-alignment gate cleared

---

## EPIC-04 — Structured Logging Standards

**Branch:** exec/v1.7-epic04-logging
**Maps to:** S2-04
**Priority:** P2 (v2.0 pre-requisite)

### TASK-11 — Define log levels and usage policy
**Classification:** autonomous
**Assigned to:** Head of Engineering
**Acceptance Criteria:**
- ERROR, WARNING, INFO, DEBUG levels defined with usage guidelines
- Policy is unambiguous and actionable

### TASK-12 — Define structured log format
**Classification:** autonomous
**Assigned to:** Head of Engineering
**Acceptance Criteria:**
- JSON format defined with required fields: timestamp, level, correlation_id, service, message
- Optional fields documented
- Format example included

### TASK-13 — Define correlation ID scheme
**Classification:** autonomous
**Assigned to:** Head of Engineering
**Acceptance Criteria:**
- Correlation ID generation scheme defined
- Propagation approach documented (HTTP header, async context)

### TASK-14 — Address async failure observability
**Classification:** autonomous
**Assigned to:** Head of Engineering
**Acceptance Criteria:**
- Async failure observability approach documented for v2.0 Alerts context
- Approach is actionable for implementation

### TASK-15 — Draft standards document
**Classification:** autonomous
**Assigned to:** Head of Engineering
**Acceptance Criteria:**
- `docs/specs/structured_logging_standards.md` created
- Lifecycle header present and compliant

### TASK-16 — Head of Specs Team class assignment and sign-off
**Classification:** delegated_decision
**Assigned to:** Head of Specs Team
**Acceptance Criteria:**
- Document class assigned (Class 1 Canonical Specification)
- Header confirmed compliant
- v2.0 hard gate (structured logging / observability) cleared

---

## EPIC-05 — API Versioning Decision Record

**Branch:** exec/v1.7-epic05-api-versioning
**Maps to:** S2-05
**Priority:** P2 (v2.0 pre-requisite)

### TASK-17 — Draft API versioning policy
**Classification:** autonomous
**Assigned to:** Product Owner + API Contracts & Documentation Owner
**Acceptance Criteria:**
- All four decision questions answered:
  1. Versioning approach (URL versioning, header, other)
  2. Deprecation notice period
  3. Webhook/async versioning approach
  4. Grandfather exemption for existing endpoints

### TASK-18 — Review with API Contracts owner
**Classification:** autonomous
**Assigned to:** API Contracts & Documentation Owner
**Acceptance Criteria:**
- Draft reviewed; no unresolved conflicts with existing spec patterns

### TASK-19 — File decision record
**Classification:** autonomous
**Assigned to:** Product Owner
**Acceptance Criteria:**
- Decision record filed at `docs/product/decisions/api-versioning-v1.7.md`
- Lifecycle-compliant Class 4 header present

### TASK-20 — Head of Specs Team sign-off
**Classification:** delegated_decision
**Assigned to:** Head of Specs Team
**Acceptance Criteria:**
- Sign-off obtained
- v2.0 pre-alignment gate (API versioning) cleared

---

## EPIC-06 — Spec Debt Resolution

**Branch:** exec/v1.7-epic06-spec-debt
**Maps to:** S2-06, S2-07, S2-08
**Priority:** P2 (S2-06) / P3 (S2-07, S2-08)

### TASK-21 — Add sharpe_ratio_trade_method to analytics_endpoints.md
**Classification:** autonomous
**Assigned to:** API Contracts & Documentation Owner
**Acceptance Criteria:**
- `sharpe_ratio_trade_method` added to validated metrics table (severity, formula, tolerance)
- Total metric count: 14

### TASK-22 — Update response example
**Classification:** autonomous
**Assigned to:** API Contracts & Documentation Owner
**Acceptance Criteria:**
- Response example shows 14 results
- `by_severity.critical.total: 4`

### TASK-23 — Increment analytics_endpoints.md version
**Classification:** autonomous
**Assigned to:** API Contracts & Documentation Owner
**Acceptance Criteria:**
- Version incremented (1.8.1 → 1.9.0)
- OBS-01 formally resolved

### TASK-24 — Sign-off OBS-01 resolved
**Classification:** autonomous
**Assigned to:** API Contracts & Documentation Owner
**Acceptance Criteria:**
- OBS-01 marked resolved in spec

### TASK-25 — S2-07 decision: spec update vs backend fix
**Classification:** delegated_decision
**Assigned to:** Product Owner + API Contracts owner
**Acceptance Criteria:**
- Decision documented (Option a: spec update chosen per MEMORY)

### TASK-26 — Implement S2-07 fix
**Classification:** autonomous
**Assigned to:** API Contracts owner
**Acceptance Criteria:**
- `portfolio_endpoints.md` positions summary field list matches live API response
- OBS-QWB-R1-01 resolved

### TASK-27 — Increment portfolio_endpoints.md version
**Classification:** autonomous
**Assigned to:** API Contracts owner
**Acceptance Criteria:**
- Version incremented (1.8.2 → 1.9.0)
- Sign-off recorded

### TASK-28 — S2-08 decision: backend fix vs spec correction
**Classification:** delegated_decision
**Assigned to:** Product Owner + API Contracts owner
**Acceptance Criteria:**
- Decision documented

### TASK-29 — Implement S2-08 fix
**Classification:** autonomous / delegated_backend
**Assigned to:** API Contracts owner / Head of Engineering
**Acceptance Criteria:**
- GET /trades includes `holding_days` field in response
- `trade_service.py` updated to include `holding_days` in `formatted_trades` dict
- `trade_endpoints.md` updated with `holding_days` in changelog

### TASK-30 — Increment trade_endpoints.md version
**Classification:** autonomous
**Assigned to:** API Contracts owner
**Acceptance Criteria:**
- Version incremented (1.8.4 → 1.9.0)
- OBS-QWB-R3-01 resolved

---

## Sprint Scope Summary

| EPIC | Items | Priority | Owner |
|------|-------|----------|-------|
| EPIC-01 | ST-01, ST-02, ST-03, ST-04 | P2 | Head of Engineering / Director of Quality |
| EPIC-02 | TASK-01 to TASK-05 | P1 | Strategy Rules owner + Product Owner |
| EPIC-03 | TASK-06 to TASK-10 | P1 | Metrics Definitions owner |
| EPIC-04 | TASK-11 to TASK-16 | P2 | Head of Engineering |
| EPIC-05 | TASK-17 to TASK-20 | P2 | Product Owner + API Contracts owner |
| EPIC-06 | TASK-21 to TASK-30 | P2/P3 | API Contracts owner |

**Total items:** 30 tasks across 6 EPICs
