**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-02__release-v1.7
**Last Updated:** 2026-03-02

---

# Stage 4 — Backlog Slice: v1.7

This document is the authoritative planning record for the v1.7 release backlog slice. It defines what is committed for execution in v1.7, organized by Epic, with acceptance criteria, owners, and sequencing notes.

The corresponding release slice section is written to `claude/backlog/backlog.md` under marker `RP:v1.7:2026-03-02__release-v1.7`.

---

## Release Metadata

| Field | Value |
|-------|-------|
| Release | v1.7 — Foundation & Governance |
| Cycle ID | 2026-03-02__release-v1.7 |
| Planning Date | 2026-03-02 |
| Total Estimated Effort | ~3.5–4 days |
| Capacity Assessment | PASS (no constraints violated — per workforce_capacity.md) |
| Hard Gates for v1.8 | EPIC-03 must complete before v1.8 pre-alignment |
| Hard Gates for v2.0 | EPIC-04 + EPIC-05 must complete before v2.0 pre-alignment |
| Hard Gates for Gated Features | EPIC-02 must complete before §13-gated features enter pre-alignment |

---

## EPIC-01 — CI/CD Merge Gate Implementation

**Maps to:** S2-01 (BLG-TECH-04)
**Priority:** P2
**Estimated Effort:** ~1 day
**Phase:** Phase 1 engineering (start immediately)
**Execution Owner:** Head of Engineering
**Validation Owner:** QA & Testing Owner + Director of Quality

| Task | Description | Owner |
|------|-------------|-------|
| ST-01 | Author `.github/workflows/validate-analytics.yml` | Head of Engineering |
| ST-02 | Test workflow on real/dry-run PR | Head of Engineering |
| ST-03 | Verify PR comment content | QA & Testing Owner |
| ST-04 | Director of Quality sign-off | Director of Quality |

**Acceptance Criteria:**
- [ ] `.github/workflows/validate-analytics.yml` exists and triggers on PR + push to main/develop
- [ ] Merge blocked on any critical-severity validation failure
- [ ] Non-critical failures produce warning comment only
- [ ] PR comment shows summary with severity breakdown
- [ ] Director of Quality sign-off obtained

---

## EPIC-02 — Strategy Boundaries Governance Review

**Maps to:** S2-02
**Priority:** P1
**Estimated Effort:** ~0.5 day
**Phase:** Phase 1 (start immediately)
**Execution Owners:** Strategy Rules & System Intent Owner (lead) + Product Owner

| Task | Description | Owner |
|------|-------------|-------|
| TASK-01 | Schedule and conduct §13 boundary review session | Strategy Rules owner + Product Owner |
| TASK-02 | Document boundary finding for each of three features | Strategy Rules owner + Product Owner |
| TASK-03 | Update strategy_rules.md if boundaries change (with version increment) | Strategy Rules & System Intent Owner |
| TASK-04 | File decision record at `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md` | Product Owner |
| TASK-05 | Head of Specs Team lifecycle sign-off | Head of Specs Team |

**Features to review:**
1. Signal Parameter Exposure (4.3) — `top_n` and `lookback_days` as user-configurable vs. §13.2 "not a configurable strategy builder"
2. AI Journal Summarisation — non-deterministic AI output vs. §13.1 deterministic system principle
3. New Technical Indicators — which indicators, if any, are canonical without violating strategy builder boundary

**Acceptance Criteria:**
- [ ] Review session completed with both owners present
- [ ] Decision record filed with compliant Class 4 header
- [ ] All three features explicitly addressed in the decision record
- [ ] If strategy_rules.md updated: version incremented, change log added
- [ ] Head of Specs Team lifecycle sign-off obtained
- [ ] §13-gated features may now proceed to pre-alignment per their stated conditions

---

## EPIC-03 — Portfolio Heat Definition in Metrics Spec

**Maps to:** S2-03
**Priority:** P1 (v1.8 hard gate)
**Estimated Effort:** ~0.5 day
**Phase:** Phase 1 (start immediately — v1.8 gate)
**Execution Owner:** Metrics Definitions & Analytics Owner
**Validation Owner:** Head of Specs Team

| Task | Description | Owner |
|------|-------------|-------|
| TASK-06 | Define canonical Position Risk formula (GBP-adjusted; FX handling) | Metrics Definitions & Analytics Owner |
| TASK-07 | Define canonical Portfolio Heat formula | Metrics Definitions & Analytics Owner |
| TASK-08 | Define display thresholds (explicit numeric bands) | Metrics Definitions & Analytics Owner |
| TASK-09 | Update metrics_definitions.md — increment version | Metrics Definitions & Analytics Owner |
| TASK-10 | Head of Specs Team lifecycle compliance sign-off | Head of Specs Team |

**Constraint:** Metrics Definitions owner must NOT be concurrently assigned to v1.9 BLG-FEAT-08. EPIC-03 first.

**Acceptance Criteria:**
- [ ] metrics_definitions.md includes canonical Position Risk formula (FX-adjusted)
- [ ] metrics_definitions.md includes canonical Portfolio Heat formula
- [ ] Display thresholds are explicit numbers (not indicative)
- [ ] Document version incremented per lifecycle guide §5
- [ ] Head of Specs Team sign-off obtained
- [ ] v1.8 pre-alignment gate cleared

---

## EPIC-04 — Structured Logging Standards

**Maps to:** S2-04
**Priority:** P2 (v2.0 pre-requisite)
**Estimated Effort:** ~1 day
**Phase:** Phase 1 engineering (start immediately)
**Execution Owner:** Head of Engineering
**Governance Owner:** Head of Specs Team (for document class assignment)

| Task | Description | Owner |
|------|-------------|-------|
| TASK-11 | Define log levels and usage policy | Head of Engineering |
| TASK-12 | Define structured log format (required and optional fields) | Head of Engineering |
| TASK-13 | Define correlation ID generation and propagation scheme | Head of Engineering |
| TASK-14 | Address async failure observability for v2.0 Alerts | Head of Engineering |
| TASK-15 | Draft standards document | Head of Engineering |
| TASK-16 | Head of Specs Team: assign document class + confirm header | Head of Specs Team |

**Acceptance Criteria:**
- [ ] Log levels (ERROR, WARNING, INFO, DEBUG) defined with usage guidelines
- [ ] Structured log format defined (JSON with required fields: timestamp, level, correlation_id, service, message)
- [ ] Correlation ID scheme defined and documented
- [ ] Async failure observability approach documented
- [ ] Document lifecycle-compliant (class, owner, status, header correct)
- [ ] Head of Specs Team sign-off obtained
- [ ] v2.0 hard gate (structured logging / observability) cleared

---

## EPIC-05 — API Versioning Decision Record

**Maps to:** S2-05
**Priority:** P2 (v2.0 pre-requisite)
**Estimated Effort:** ~0.5 day
**Phase:** Phase 1 (start immediately)
**Execution Owner:** Product Owner (decision lead) + API Contracts & Documentation Owner

| Task | Description | Owner |
|------|-------------|-------|
| TASK-17 | Draft API versioning policy (answer four decision questions) | Product Owner + API Contracts owner |
| TASK-18 | Review draft with API Contracts & Documentation Owner | API Contracts & Documentation Owner |
| TASK-19 | File decision record at `docs/product/decisions/api-versioning-v1.7.md` | Product Owner |
| TASK-20 | Head of Specs Team lifecycle sign-off | Head of Specs Team |

**Four decision questions:**
1. Do we version API endpoints? If yes, what approach (URL versioning, header versioning, other)?
2. Deprecation notice period?
3. How are webhook/async patterns handled?
4. Are existing endpoints grandfather-exempted?

**Acceptance Criteria:**
- [ ] All four decision questions explicitly answered
- [ ] Decision record filed with compliant Class 4 header
- [ ] Head of Specs Team sign-off obtained
- [ ] v2.0 pre-alignment gate (API versioning) cleared

---

## EPIC-06 — Spec Debt Resolution

**Maps to:** S2-06, S2-07, S2-08
**Priority:** P2 (S2-06) / P3 (S2-07, S2-08)
**Estimated Effort:** ~1–2 hours + decision session for S2-07/S2-08
**Phase:** S2-06 in Phase 1; S2-07/S2-08 in Phase 2 (after pre-condition decisions)
**Execution Owner:** API Contracts & Documentation Owner

### S2-06 — BLG-TECH-06

| Task | Description | Owner |
|------|-------------|-------|
| TASK-21 | Add `sharpe_ratio_trade_method` to analytics_endpoints.md validated metrics table | API Contracts & Documentation Owner |
| TASK-22 | Update response example: 14 results; `by_severity.critical.total: 4` | API Contracts & Documentation Owner |
| TASK-23 | Increment analytics_endpoints.md version | API Contracts & Documentation Owner |
| TASK-24 | Sign-off — OBS-01 resolved | API Contracts & Documentation Owner |

**Acceptance Criteria:**
- [ ] analytics_endpoints.md validated metrics table includes `sharpe_ratio_trade_method` (severity, formula, tolerance)
- [ ] Response example shows 14 results and `by_severity.critical.total: 4`
- [ ] Document version incremented
- [ ] OBS-01 formally resolved

### S2-07 — BLG-TECH-08

| Task | Description | Owner |
|------|-------------|-------|
| TASK-25 | Product Owner + API Contracts owner decision: Option (a) spec update vs Option (b) backend fix | Product Owner + API Contracts owner |
| TASK-26 | Implement chosen fix | API Contracts owner / Head of Engineering |
| TASK-27 | Increment relevant document version; sign-off | API Contracts owner |

**Acceptance Criteria:**
- [ ] Decision documented (approach chosen)
- [ ] portfolio_endpoints.md positions summary field list matches live API response
- [ ] No discrepancy between spec and implementation for `/portfolio` positions objects
- [ ] Document version incremented
- [ ] OBS-QWB-R1-01 resolved

### S2-08 — BLG-TECH-09

| Task | Description | Owner |
|------|-------------|-------|
| TASK-28 | Product Owner + API Contracts owner decision: Option (a) backend fix vs Option (b) spec correction | Product Owner + API Contracts owner |
| TASK-29 | Implement chosen fix | API Contracts owner / Head of Engineering |
| TASK-30 | Increment relevant document version; sign-off | API Contracts owner |

**Acceptance Criteria:**
- [ ] Decision documented (approach chosen)
- [ ] GET /trades includes `holding_days` OR trade_endpoints.md corrected and consistent
- [ ] No discrepancy between spec and implementation
- [ ] Document version incremented
- [ ] OBS-QWB-R3-01 resolved

---

## Release Acceptance Summary

v1.7 is released when ALL of the following are confirmed:

| Condition | Confirmed By |
|-----------|-------------|
| EPIC-01 acceptance criteria met | Director of Quality |
| EPIC-02 acceptance criteria met | Strategy Rules owner + Product Owner + Head of Specs Team |
| EPIC-03 acceptance criteria met | Metrics Definitions owner + Head of Specs Team |
| EPIC-04 acceptance criteria met | Head of Engineering + Head of Specs Team |
| EPIC-05 acceptance criteria met | Product Owner + Head of Specs Team |
| EPIC-06 acceptance criteria met | API Contracts owner |
| All new documents lifecycle-compliant | Head of Specs Team (sweep) |
| Release readiness confirmed | Director of Quality |
| Product Owner acceptance | Product Owner |

**Note on S2-07 and S2-08:** If decisions for TASK-25/TASK-28 cannot be reached within the v1.7 execution window, these P3 items may be re-targeted to v1.8 without impacting any v1.7 or v1.8 gates (RISK-02). This decision must be made explicitly by the Product Owner before v1.7 is marked complete.

---

## Stage 4 Outcome

**Result: PASS**

Backlog slice committed. 6 EPICs, 8 scope items, 30 tasks documented. Release acceptance criteria defined. backlog_committed = true (after backlog.md marker written).
