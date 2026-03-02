**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-02__release-v1.7
**Last Updated:** 2026-03-02

---

# Stage 2 — Scope Extraction

> Scope items are extracted without modification from canonical planning inputs:
> - claude/roadmap/current_roadmap.md (§v1.7 — Foundation & Governance)
> - claude/backlog/backlog.md (items with Target release: v1.7)
>
> No scope changes are permitted in this stage.

---

## Scope Source Summary

| Source | Items Extracted |
|--------|----------------|
| current_roadmap.md §v1.7 | S2-01, S2-02, S2-03, S2-04, S2-05 |
| backlog.md (target release: v1.7) | S2-06 (BLG-TECH-06), S2-07 (BLG-TECH-08), S2-08 (BLG-TECH-09) |

---

## Scope Items

---

### S2-01 — CI/CD GitHub Actions Validation Workflow

**Backlog ID:** BLG-TECH-04
**Source:** current_roadmap.md §v1.7
**Type:** Engineering / Delivery Automation
**Priority:** P2
**Estimated Effort:** ~1 day
**Status in Backlog:** Open (planned, v1.7)

**Description:**
Add `.github/workflows/validate-analytics.yml`. Run `POST /validate/calculations` on pull requests and pushes to `main` and `develop`. Block merge on critical-severity failures only. Post validation summary as PR comment.

**Dependencies:**
- BLG-TECH-02 (Validation Severity Model) — ✅ COMPLETE (severity model required for merge gate logic)

**Acceptance Criteria:**
- Workflow exists at `.github/workflows/validate-analytics.yml`
- Workflow triggers on PR and push to `main` and `develop`
- Merge is blocked if any critical-severity validation fails
- Non-critical failures generate a warning comment but do not block merge
- PR comment shows validation summary with severity breakdown

**Owner:** Head of Engineering (implementation) + QA & Testing Owner (validation)

---

### S2-02 — Strategy Rules §13 Boundary Review

**Source:** current_roadmap.md §v1.7
**Type:** Governance / Spec Review
**Priority:** P1 (gates all §13-dependent gated features)
**Estimated Effort:** ~0.5 day (one workshop session)

**Description:**
Formal review of system boundaries in §13 of strategy_rules.md in light of features under consideration: signal parameter exposure, AI journal summarisation, and new technical indicators. Each of these touches §13. This review must produce a documented decision before any of those features enters pre-alignment.

**Dependencies:** None

**Output:** Decision record confirming either:
- (a) Boundaries unchanged — formal confirmation record (SRB type)
- (b) strategy_rules.md updated with version increment (if boundaries change)

**Acceptance Criteria:**
- Workshop held with Strategy Rules & System Intent Owner + Product Owner
- Decision record produced and lifecycle-compliant
- All three gated features addressed explicitly in the record
- If strategy_rules.md changes: version incremented; change log updated
- Head of Specs Team lifecycle sign-off

**Owners:** Strategy Rules & System Intent Owner (lead) + Product Owner (co-owner)

---

### S2-03 — Metrics Definitions — Portfolio Heat Formula & Thresholds

**Source:** current_roadmap.md §v1.7
**Type:** Spec / Metrics Definition
**Priority:** P1 (v1.8 hard pre-requisite)
**Estimated Effort:** ~0.5 day

**Description:**
Must be complete before v1.8 enters pre-alignment. Define canonical Portfolio Heat formula and display thresholds in metrics_definitions.md. Indicative formula: `Position Risk = (Entry Price − Stop Price) × Shares`; `Portfolio Heat = Sum of Position Risks / Portfolio Value`. Thresholds are indicative — the canonical definition prevails.

**Dependencies:** None (definitional task; no engineering prerequisites)

**Output:** metrics_definitions.md updated with:
- Canonical Portfolio Heat formula
- Canonical display thresholds
- Version incremented

**Acceptance Criteria:**
- metrics_definitions.md includes canonical heat formula (Position Risk and Portfolio Heat)
- Display thresholds are explicitly defined (not indicative)
- Document version incremented per document_lifecycle_guide.md §5
- Head of Specs Team lifecycle sign-off confirming canonical status

**Owner:** Metrics Definitions & Analytics Owner

---

### S2-04 — Structured Logging / Observability Standards

**Source:** current_roadmap.md §v1.7
**Type:** Engineering / Standards
**Priority:** P2 (v2.0 pre-requisite — ensures async failures in Alerts are observable)
**Estimated Effort:** ~1 day

**Description:**
Lightweight observability baseline before Alerts (v2.0) introduces async processing. Not full Prometheus (BLG-TECH-05 remains deferred). Define agreed structured logging standards, log levels, and correlation IDs. Ensures async failures in v2.0 are observable and debuggable.

**Dependencies:** None

**Output:** Structured logging standards document (class to be determined by Head of Specs Team)

**Acceptance Criteria:**
- Log level definitions and usage policy documented (ERROR, WARNING, INFO, DEBUG minimum)
- Structured log format defined (JSON with required fields including timestamp, level, correlation_id, service, message)
- Correlation ID scheme defined
- Async failure observability approach documented (relevant to v2.0 Alerts)
- Document is lifecycle-compliant (class, owner, status, header per document_lifecycle_guide.md)
- Head of Specs Team lifecycle sign-off

**Owner:** Head of Engineering

---

### S2-05 — API Versioning Strategy Decision Record

**Source:** current_roadmap.md §v1.7
**Type:** Governance / Decision
**Priority:** P2 (v2.0 pre-requisite — must be decided before Alerts and webhook/async patterns enter pre-alignment)
**Estimated Effort:** ~0.5 day

**Description:**
Define the API versioning and deprecation policy before Alerts (v2.0) introduces webhook or async patterns. Questions to resolve: do we version endpoints? What is the deprecation notice period? This decision must be made before v2.0 pre-alignment opens.

**Dependencies:** None

**Output:** Decision record in `docs/product/decisions/` covering:
- Versioning policy (versioned vs. non-versioned endpoints; approach if versioned)
- Deprecation notice period
- Handling of webhook/async patterns under the policy

**Acceptance Criteria:**
- Decision record filed with lifecycle-compliant header (Class 4, owner named, status Active)
- Versioning policy explicitly stated (yes or no; if yes, approach defined)
- Deprecation period explicitly stated
- Webhook/async pattern treatment addressed
- Head of Specs Team lifecycle sign-off

**Owners:** Product Owner (decision lead) + API Contracts & Documentation Owner

---

### S2-06 — Canonicalise sharpe_ratio_trade_method as 14th Validation Metric

**Backlog ID:** BLG-TECH-06
**Source:** backlog.md (target release: v1.7 — updated from v1.6.1 per DL-001 cycle 2026-03-01__item-3.2)
**Type:** Spec Accuracy / Governance
**Priority:** P2
**Estimated Effort:** ~30 min – 1 hour (spec update only; no code change required)
**Source Observation:** OBS-01, QA Lead, 2026-02-21T21:25:00Z

**Description:**
`POST /validate/calculations` returns 14 validation results. `analytics_endpoints.md` v1.8.1 describes 13 metrics and does not document `sharpe_ratio_trade_method`. The 14th metric was introduced under BLG-TECH-01 Addendum 1. Implementation is correct and passes. The spec is incomplete.

**Dependencies:** None (no code change)

**Acceptance Criteria:**
- `analytics_endpoints.md` validated metrics table includes `sharpe_ratio_trade_method` with severity, formula, and tolerance
- Response example reflects 14 results
- `by_severity.critical.total` shown as 4 in example (not 3)
- No deviation between spec and live `POST /validate/calculations` response
- Document version incremented

**Owner:** API Contracts & Documentation Owner

---

### S2-07 — Align portfolio_endpoints.md Positions Summary Field List

**Backlog ID:** BLG-TECH-08
**Source:** backlog.md (target release: v1.7 — OBS-QWB-R1-01)
**Type:** Spec Accuracy
**Priority:** P3
**Estimated Effort:** ~30 min (spec-only fix) or ~2–4 hours (backend fix)
**Source Observation:** OBS-QWB-R1-01, QA Lead, QWB verification, 2026-03-01

**Description:**
`GET /portfolio` positions summary objects omit `current_price_native`, `stop_price`, `stop_price_native`, and `pnl_percent` — fields listed in portfolio_endpoints.md. Pre-existing behaviour, not introduced by QWB.

**Pre-Condition (Required before implementation):**
Product Owner + API Contracts & Documentation Owner decision on fix approach:
- Option (a): Update `portfolio_endpoints.md` to accurately document the lightweight summary shape, distinguishing it from the full position object on `GET /positions`
- Option (b): Add the missing fields to the backend `GET /portfolio` response

**Dependencies:** Decision session (Product Owner + API Contracts owner) — can be combined with S2-08 pre-condition decision

**Acceptance Criteria:**
- portfolio_endpoints.md positions summary field list matches live API response, OR
- Backend `GET /portfolio` response includes the missing fields and spec is aligned
- No discrepancy between spec and implementation for `/portfolio` positions objects
- Document version incremented if spec changes

**Owner:** API Contracts & Documentation Owner (post-decision)

---

### S2-08 — Add holding_days to GET /trades Response

**Backlog ID:** BLG-TECH-09
**Source:** backlog.md (target release: v1.7 — OBS-QWB-R3-01)
**Type:** Spec Accuracy
**Priority:** P3
**Estimated Effort:** ~30 min (spec-only fix) or ~1 hour (backend fix)
**Source Observation:** OBS-QWB-R3-01, QA Lead, QWB verification, 2026-03-01

**Description:**
`holding_days` is absent from trade objects in the `GET /trades` response. `trade_endpoints.md` v1.8.4 lists it as a required field. Pre-existing behaviour, not introduced by QWB.

**Pre-Condition (Required before implementation):**
Product Owner + API Contracts & Documentation Owner decision on fix approach:
- Option (a): Add `holding_days` to the backend `GET /trades` response (spec-compliant fix)
- Option (b): Remove `holding_days` from `trade_endpoints.md` documented schema, with a note explaining its absence and where the value can be sourced (e.g., `trades_for_charts`)

**Dependencies:** Decision session (Product Owner + API Contracts owner) — can be combined with S2-07 pre-condition decision

**Acceptance Criteria:**
- `GET /trades` trade objects include `holding_days` (integer), OR
- `trade_endpoints.md` schema corrected to remove the field, with explanation
- No discrepancy between spec and implementation
- Document version incremented if spec changes

**Owner:** API Contracts & Documentation Owner (post-decision)

---

## Scope Summary Table

| ID | Item | Source | Type | Priority | Effort |
|----|------|--------|------|----------|--------|
| S2-01 | BLG-TECH-04 — CI/CD Validation Workflow | Roadmap v1.7 | Engineering | P2 | ~1 day |
| S2-02 | §13 Boundary Review | Roadmap v1.7 | Governance | P1 | ~0.5 day |
| S2-03 | Metrics Defs — Portfolio Heat Formula | Roadmap v1.7 | Spec/Metrics | P1 | ~0.5 day |
| S2-04 | Structured Logging Standards | Roadmap v1.7 | Engineering | P2 | ~1 day |
| S2-05 | API Versioning Decision Record | Roadmap v1.7 | Governance | P2 | ~0.5 day |
| S2-06 | BLG-TECH-06 — sharpe_ratio_trade_method | Backlog (v1.7) | Spec Accuracy | P2 | ~30 min–1 hr |
| S2-07 | BLG-TECH-08 — portfolio positions summary | Backlog (v1.7) | Spec Accuracy | P3 | ~30 min + |
| S2-08 | BLG-TECH-09 — holding_days in GET /trades | Backlog (v1.7) | Spec Accuracy | P3 | ~30 min + |

**Total estimated effort:** ~3.5–4 days (consistent with workforce_capacity.md assessment of ~3.5 days for v1.7)

---

## Stage 2 Outcome

**Result: PASS**

8 scope items extracted. All have S2-IDs assigned. No scope changes introduced. Items derived entirely from roadmap §v1.7 and backlog items with explicit v1.7 target release assignments. Scope is consistent with the v1.7 "Foundation & Governance" theme.
