**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-02__release-v1.7
**Last Updated:** 2026-03-02

---

# Stage 3 — Execution Plan

## v1.7 Epic Registry

| Epic ID | Title | Maps to | Owner | Effort |
|---------|-------|---------|-------|--------|
| EPIC-01 | CI/CD Merge Gate Implementation | S2-01 | Head of Engineering + QA & Testing Owner | ~1 day |
| EPIC-02 | Strategy Boundaries Governance Review | S2-02 | Strategy Rules & System Intent Owner + Product Owner | ~0.5 day |
| EPIC-03 | Portfolio Heat Definition in Metrics Spec | S2-03 | Metrics Definitions & Analytics Owner | ~0.5 day |
| EPIC-04 | Structured Logging Standards | S2-04 | Head of Engineering | ~1 day |
| EPIC-05 | API Versioning Decision Record | S2-05 | Product Owner + API Contracts & Documentation Owner | ~0.5 day |
| EPIC-06 | Spec Debt Resolution | S2-06, S2-07, S2-08 | API Contracts & Documentation Owner | ~1–2 hours + decisions |

---

## Epic Definitions

---

### EPIC-01 — CI/CD Merge Gate Implementation
**Maps to:** S2-01
**Owner:** Head of Engineering (implementation); QA & Testing Owner (validation)
**Effort:** ~1 day
**Dependencies:** BLG-TECH-02 ✅ COMPLETE

**Scope:**
Add `.github/workflows/validate-analytics.yml` that calls `POST /validate/calculations` on all PRs and pushes to `main`/`develop`. The workflow reads the validation response, fails the job if any result with `severity: critical` has `passed: false`, and posts a structured PR comment showing validation summary and severity breakdown.

**Tasks:**
- ST-01: Author `.github/workflows/validate-analytics.yml` — define trigger events, service startup, API call, result parsing, merge gate condition, PR comment action
- ST-02: Test workflow on a real or dry-run PR — verify trigger, blocking behaviour on critical failure, non-blocking behaviour on non-critical failure
- ST-03: Verify PR comment content is accurate and well-formatted
- ST-04: QA sign-off (Director of Quality)

**Acceptance Gate:**
- Workflow triggers on PR and push to `main` and `develop` ✅
- Merge blocked on critical-severity failures only ✅
- Non-critical failures generate warning comment, do not block ✅
- PR comment shows summary with severity breakdown ✅
- Director of Quality sign-off ✅

---

### EPIC-02 — Strategy Boundaries Governance Review
**Maps to:** S2-02
**Owner:** Strategy Rules & System Intent Owner (lead); Product Owner (co-owner)
**Effort:** ~0.5 day (one workshop session + document)
**Dependencies:** None

**Scope:**
Conduct a structured review of §13 (System Boundaries) in strategy_rules.md. The review must explicitly address three features currently awaiting gate clearance:

1. **Signal Parameter Exposure (4.3):** Is exposing `top_n` and `lookback_days` as user-configurable parameters consistent with §13.2 ("not a configurable strategy builder")? The roadmap notes scope is strictly limited to these two existing parameters.
2. **AI Journal Summarisation:** Does non-deterministic AI output conflict with the deterministic system principle (§13.1)?
3. **New Technical Indicators:** Which indicators, if any, are canonical to this strategy without constituting a configurable strategy builder?

**Expected Output:** Decision record (SRB type) documenting:
- Explicit finding for each of the three features
- Whether boundaries are unchanged or require a strategy_rules.md revision

**Tasks:**
- TASK-01: Schedule and conduct §13 boundary review session with Strategy Rules & System Intent Owner + Product Owner
- TASK-02: For each of the three features, document the boundary finding (compliant / non-compliant / conditional)
- TASK-03: If any boundary changes are required — update strategy_rules.md with version increment and change log entry
- TASK-04: File decision record at `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md` with lifecycle-compliant header
- TASK-05: Head of Specs Team lifecycle sign-off on decision record

**Acceptance Gate:**
- Session completed with both owners ✅
- Decision record filed and lifecycle-compliant ✅
- All three features addressed explicitly ✅
- If strategy_rules.md changed: version incremented, change log updated ✅
- Head of Specs Team sign-off ✅
- Gate cleared: §13-gated features may now proceed to pre-alignment per their stated conditions ✅

---

### EPIC-03 — Portfolio Heat Definition in Metrics Spec
**Maps to:** S2-03
**Owner:** Metrics Definitions & Analytics Owner
**Effort:** ~0.5 day
**Dependencies:** None

**Scope:**
Update `docs/specs/metrics_definitions.md` with canonical, implementation-ready definitions for:
- **Position Risk** (contribution of a single position to overall portfolio heat)
- **Portfolio Heat** (aggregate risk exposure as a percentage of portfolio value)
- **Display thresholds** (e.g., green/amber/red bands for the heat gauge in v1.8)

The indicative formula in the roadmap (`Position Risk = (Entry Price − Stop Price) × Shares`; `Portfolio Heat = Sum of Position Risks / Portfolio Value`) must be confirmed, refined, or replaced with the canonical definition. Indicative formulas in planning documents do not constitute canonical intent.

**Constraints:**
- This is the v1.8 hard gate — v1.8 pre-alignment may not open until this item is complete and signed off
- Metrics Definitions owner must NOT begin v1.9 BLG-FEAT-08 concurrently (RISK-03)

**Tasks:**
- TASK-06: Define canonical Position Risk formula (GBP-adjusted; FX handling required for non-GBP instruments)
- TASK-07: Define canonical Portfolio Heat formula (Sum of Position Risks / Portfolio Value × 100)
- TASK-08: Define display thresholds (explicit numeric bands for heat gauge UI in v1.8)
- TASK-09: Update `metrics_definitions.md` with new section — increment version
- TASK-10: Head of Specs Team lifecycle compliance sign-off

**Acceptance Gate:**
- metrics_definitions.md includes canonical Portfolio Heat section with formula and thresholds ✅
- Position Risk formula handles FX-adjusted instruments ✅
- Display thresholds are explicit numbers, not indicative ✅
- Document version incremented per lifecycle guide §5 ✅
- Head of Specs Team sign-off ✅
- v1.8 pre-alignment gate cleared ✅

---

### EPIC-04 — Structured Logging Standards
**Maps to:** S2-04
**Owner:** Head of Engineering
**Effort:** ~1 day
**Dependencies:** None

**Scope:**
Define lightweight structured logging standards to ensure that async failures in v2.0 Alerts are observable and debuggable. This is not a full Prometheus implementation (BLG-TECH-05 remains deferred). The output is a standards document adopted by the engineering team.

**Topics to cover:**
- Log levels (ERROR, WARNING, INFO, DEBUG) with usage guidelines per level
- Structured log format — JSON with required fields: `timestamp` (ISO-8601 UTC), `level`, `correlation_id`, `service`, `message`, plus optional domain fields
- Correlation ID scheme — how correlation IDs are generated, propagated, and surfaced in API responses (for async tracing in v2.0)
- Async failure observability — how background/async job failures will be logged and monitored under this standard
- What NOT to log (sensitive data, PII, full request bodies)

**Tasks:**
- TASK-11: Define log levels and usage policy
- TASK-12: Define structured log format (required and optional fields)
- TASK-13: Define correlation ID generation and propagation scheme
- TASK-14: Address async failure observability (v2.0 Alerts relevance)
- TASK-15: Draft standards document
- TASK-16: Head of Specs Team lifecycle compliance check — assign document class and confirm header

**Note on document class:** The structured logging standards document does not map to an existing document class in the lifecycle guide without further analysis. The Head of Specs Team must assign the appropriate class and confirm the header block before this document may be treated as authoritative. This is captured as RISK-04.

**Acceptance Gate:**
- Log levels, format, and correlation ID scheme documented ✅
- Async failure observability addressed for v2.0 ✅
- Document is lifecycle-compliant — class assigned, owner named, status set ✅
- Head of Specs Team sign-off ✅
- v2.0 Alerts hard gate (structured logging) cleared ✅

---

### EPIC-05 — API Versioning Decision Record
**Maps to:** S2-05
**Owner:** Product Owner (decision lead); API Contracts & Documentation Owner (contributor)
**Effort:** ~0.5 day
**Dependencies:** None

**Scope:**
Produce a decision record that defines the API versioning and deprecation policy. This must be decided before v2.0 pre-alignment opens, as Alerts will likely introduce webhook or async callback patterns that may require versioning.

**Questions to resolve:**
1. Do we version API endpoints? (e.g., `/api/v1/portfolio` vs `/portfolio`) If yes: approach (URL versioning, header versioning, other)?
2. If versioned: what is the deprecation notice period before an old version is removed?
3. How are webhook/async patterns handled under this policy?
4. Are existing endpoints grandfather-exempted or subject to the new policy?

**Tasks:**
- TASK-17: Draft API versioning policy — answer the four questions above
- TASK-18: Review with API Contracts & Documentation Owner
- TASK-19: File decision record at `docs/product/decisions/api-versioning-v1.7.md` with lifecycle-compliant Class 4 header
- TASK-20: Head of Specs Team lifecycle sign-off

**Acceptance Gate:**
- All four questions answered explicitly ✅
- Decision record filed with compliant header ✅
- Head of Specs Team sign-off ✅
- v2.0 pre-alignment gate (API versioning) cleared ✅

---

### EPIC-06 — Spec Debt Resolution
**Maps to:** S2-06, S2-07, S2-08
**Owner:** API Contracts & Documentation Owner
**Effort:** ~1–2 hours total (+ pre-condition decision time for S2-07 and S2-08)
**Dependencies:** Pre-condition decisions for S2-07 and S2-08 (can be combined into one joint session)

**S2-06 Sub-tasks (BLG-TECH-06 — no pre-condition required):**
- TASK-21: Update `analytics_endpoints.md` — add `sharpe_ratio_trade_method` to validated metrics table with severity (`critical`), formula reference, and tolerance
- TASK-22: Update response example to show 14 results and `by_severity.critical.total: 4`
- TASK-23: Increment `analytics_endpoints.md` version
- TASK-24: API Contracts owner sign-off (OBS-01 formally resolved)

**S2-07 Sub-tasks (BLG-TECH-08 — requires pre-condition decision):**
- TASK-25: [Pre-work] Product Owner + API Contracts owner joint decision session — choose Option (a) spec update or Option (b) backend fix
- TASK-26: Implement chosen fix
- TASK-27: Increment relevant document version; sign-off

**S2-08 Sub-tasks (BLG-TECH-09 — requires pre-condition decision):**
- TASK-28: [Pre-work] Product Owner + API Contracts owner joint decision session — choose Option (a) backend fix or Option (b) spec correction (can be combined with TASK-25)
- TASK-29: Implement chosen fix
- TASK-30: Increment relevant document version; sign-off

**Acceptance Gate:**
- S2-06: analytics_endpoints.md shows 14 validated metrics; OBS-01 resolved ✅
- S2-07: No discrepancy between portfolio_endpoints.md and live `/portfolio` positions objects ✅
- S2-08: GET /trades includes holding_days OR trade_endpoints.md corrected and consistent ✅
- All changed documents version-incremented and lifecycle-compliant ✅

---

## Risk Register

### RISK-01 — §13 Boundary Review Contested Result
**Relates to:** EPIC-02
**Probability:** Low
**Impact:** Medium
**Description:** The §13 boundary review (S2-02) may surface contested or unresolved boundary questions. If the Strategy Rules & System Intent Owner and Product Owner do not reach agreement on any of the three features, the escalation protocol applies (team_charter.md §5.2, 72-hour SLA). v1.7 cannot be fully closed until EPIC-02 produces its decision record.
**Mitigation:** The review covers three features with well-documented gate conditions already stated in the roadmap. Scope is bounded. No binding technical implementation decision is required — only a documented boundary finding.
**Fallback:** If contested and unresolved within 72 hours, escalation is created and EPIC-02 remains open. v1.7 may ship other items; EPIC-02 is the only gate item for §13-dependent gated features, not a gate for v1.8.

### RISK-02 — BLG-TECH-08 / BLG-TECH-09 Pre-Execution Decision Delays
**Relates to:** EPIC-06
**Probability:** Low
**Impact:** Low
**Description:** S2-07 (BLG-TECH-08) and S2-08 (BLG-TECH-09) require Product Owner + API Contracts owner approach decisions before implementation. If the joint decision session is delayed, those P3 items may not complete within the v1.7 execution window.
**Mitigation:** The decision is a lightweight approach choice, not a design decision. Schedule the joint session in Phase 1 alongside other governance tasks. S2-06 (BLG-TECH-06) has no dependencies and delivers independently.
**Fallback:** Re-target S2-07 and S2-08 to v1.8 if decisions cannot be reached within v1.7 window. No v1.7 gates depend on these items.

### RISK-03 — Metrics Definitions Owner Concurrency Constraint
**Release-level**
**Probability:** Medium (if v1.9 planning begins before EPIC-03 is complete)
**Impact:** Medium
**Description:** The Metrics Definitions & Analytics Owner is required for EPIC-03 (S2-03, v1.7) and for BLG-FEAT-08 Compliance Metrics (v1.9). Per workforce_capacity.md, these must NOT run concurrently. v1.9 must not start until EPIC-03 is signed off.
**Mitigation:** EPIC-03 is Phase 1 of v1.7. v1.9 does not begin until v1.8 closes. Sequencing already confirmed in workforce_capacity.md. No immediate scheduling conflict.
**Monitoring:** FinOps & Resource Architect to confirm no concurrent allocation before v1.9 pre-alignment opens.

### RISK-04 — Structured Logging Document Lifecycle Classification
**Relates to:** EPIC-04
**Probability:** Medium
**Impact:** Low
**Description:** The structured logging standards document does not have a pre-assigned class in the lifecycle guide. Head of Specs Team must classify it before it may be treated as authoritative. If Head of Specs Team requires significant structural changes, effort may exceed the ~1 day estimate.
**Mitigation:** Include Head of Specs Team lifecycle compliance sign-off as an explicit acceptance gate task (TASK-16). Head of Specs Team should be engaged early in EPIC-04 drafting — not only at review time.

---

## Execution Phasing

### Phase 1 — Governance, Spec & Decision Work (start immediately)

All Phase 1 items can run in parallel:

| Item | Owner | Notes |
|------|-------|-------|
| EPIC-02 — §13 Boundary Review | Strategy Rules + Product Owner | Schedule review session |
| EPIC-03 — Portfolio Heat Formula | Metrics Definitions owner | P1; v1.8 gate; start immediately |
| EPIC-05 — API Versioning Decision | Product Owner + API Contracts owner | Schedule decision session |
| EPIC-06 S2-06 — BLG-TECH-06 | API Contracts owner | No dependencies; start immediately |
| EPIC-06 S2-07/S2-08 pre-work | Product Owner + API Contracts owner | Decision session; can combine with EPIC-05 session |

### Phase 1 Engineering (start immediately, parallel with Phase 1 governance)

| Item | Owner | Notes |
|------|-------|-------|
| EPIC-01 — CI/CD Workflow | Head of Engineering | BLG-TECH-02 complete; start now |
| EPIC-04 — Structured Logging | Head of Engineering | Engage Head of Specs Team early for class assignment |

### Phase 2 — Implementation Follow-Through (after Phase 1 pre-work decisions)

| Item | Owner | Notes |
|------|-------|-------|
| EPIC-06 S2-07 — BLG-TECH-08 | API Contracts owner | After decision from TASK-25 |
| EPIC-06 S2-08 — BLG-TECH-09 | API Contracts owner | After decision from TASK-28 |

---

## Dependency Map

```
BLG-TECH-02 (complete) ──► EPIC-01
(no deps)               ──► EPIC-02
(no deps)               ──► EPIC-03
(no deps)               ──► EPIC-04
(no deps)               ──► EPIC-05
(no deps)               ──► EPIC-06 (S2-06 only)
TASK-25 decision        ──► EPIC-06 (S2-07)
TASK-28 decision        ──► EPIC-06 (S2-08)

EPIC-02 complete        ──► §13-gated features may enter pre-alignment
EPIC-03 complete        ──► v1.8 pre-alignment gate cleared
EPIC-04 + EPIC-05 complete ──► v2.0 pre-alignment gates cleared (2 of 3; QA planning session = 3rd)
```

---

## Verification Approach

| Epic | Verification Method | Acceptance Authority |
|------|--------------------|--------------------|
| EPIC-01 | Live workflow test on PR + QA sign-off | Director of Quality |
| EPIC-02 | Decision record review against §13 criteria | Strategy Rules & System Intent Owner + Product Owner + Head of Specs Team |
| EPIC-03 | metrics_definitions.md review against formula completeness and threshold specificity | Metrics Definitions & Analytics Owner + Head of Specs Team |
| EPIC-04 | Document review against logging standards checklist | Head of Engineering + Head of Specs Team |
| EPIC-05 | Decision record review against versioning policy completeness | Product Owner + Head of Specs Team |
| EPIC-06 | Spec review against live API responses (no code change for S2-06; as-implemented for S2-07/S2-08) | API Contracts & Documentation Owner |

**Release-level acceptance:** Director of Quality release readiness confirmation (overall) + Head of Specs Team lifecycle compliance sweep across all new documents.

---

## Stage 3 Outcome

**Result: PASS**

6 EPICs defined. All S2 IDs mapped. 4 risks registered with EPIC or Release-level references. EPIC and RISK IDs are stable. Execution phasing reflects dependencies. plan_structured = true.
