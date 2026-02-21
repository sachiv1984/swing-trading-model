# Specs Index (Canonical)

**Owner:** Head of Specs Team
**Purpose:** Single map of canonical product truth
**Audience:** Product, Engineering, Analytics, Strategy
**Status:** Authoritative
**Last Updated:** 2026-02-21

---

## 1. Purpose of This Index

This document defines **where authoritative truth lives** across the system.

It answers:
- Which spec owns which decisions
- How specs relate to one another
- Which document prevails in case of conflict

If two specs disagree, **this index determines the escalation path**.

---

## 2. How to Use This Index

When asking:
- "Where is X defined?"
- "Which rules apply?"
- "Who owns this decision?"
- "Can I change this safely?"

Start here.

This index does **not** restate rules.
It points to the **single canonical source**.

---

## 3. Canonical Spec Domains

### 3.1 Strategy

**What it owns**
- Trading intent
- Risk philosophy
- Position lifecycle rules
- Strategy parameter governance

**Canonical Documents**
- `strategy_rules.md`

**Owner**
- Strategy Rules & System Intent Owner

---

### 3.2 Data Model

**What it owns**
- Meaning of fields (price, stop, P&L, value)
- Currency semantics
- Lifecycle and state representations

**Canonical Documents**
- `data_model.md`

**Owner**
- Data Model & Domain Schema Owner

---

### 3.3 Metrics & Analytics

**What it owns**
- Definitions of performance metrics
- Canonical formulas and tolerances
- Data sufficiency and failure behavior

**Canonical Documents**
- `metrics_definitions.md`

**Owner**
- Metrics Definitions & Analytics Canonical Owner

---

### 3.4 API Contracts

**What it owns**
- Request/response schemas
- Field guarantees and defaults
- Idempotency and error semantics
- Backward compatibility rules

**Canonical Location**
- `docs/specs/api_contracts/`

**Canonical Documents**
- `README.md`
- `conventions.md`
- `*_endpoints.md`

**Supporting Reference**
- `docs/reference/openapi.yaml` — *Supporting reference only; must not diverge from canonical contracts*

**Owner**
- API Contracts & Documentation Owner

**Enforcement**
- Any pull request that changes canonical API contracts or backend API behavior **must** be reviewed inline against:
  - Canonical Markdown contracts **and**
  - `docs/reference/openapi.yaml`
- Approval is blocked if OpenAPI alignment is skipped for contract-affecting changes.

---

### 3.5 Frontend & UX Semantics

**What it owns**
- User-visible meanings and mental models
- Page-level user goals, states, and flows
- Reusable UI component behavior
- Cross-cutting UX patterns
- Visual and interaction consistency

**Canonical Location**
- `specs/frontend/`

**Canonical Documents**
- `frontend/README.md`
- `frontend/design_system.md`
- Page, component, and pattern specifications

**Owner**
- Frontend Specifications & UX Documentation Owner

---

### 3.6 Glossary (System-Level Reference)

**What it owns**
- Shared terminology used across specs
- Cross-domain language consistency
- Canonical meanings of commonly referenced terms

**Reference Document**
- `docs/reference/glossary.md`

**Authority**
- Language only — canonical definitions, formulas, and rules live in domain specs

**Owner**
- Head of Specs Team

**Notes**
- The glossary must not introduce new behavior or override domain specifications
- In case of conflict, the relevant domain canonical spec prevails

---

## 4. Conflict Resolution Order

In case of conflict, precedence is resolved in the following order:

1. **Specs Index**
2. Domain Canonical Spec
3. Supporting Specs
4. Reference Artifacts (e.g. OpenAPI, Glossary)
5. Code
6. UI behavior
7. Tribal knowledge

No downstream system may override upstream intent.

---

## 5. Change Governance & Enforcement

- Changes to **domain canonical specs** require domain owner approval
- Changes affecting multiple domains require Head of Specs Team review
- **Supporting reference artifacts must be reviewed inline with their canonical specs**
- Silent divergence between specs and behavior is treated as a **system bug**
- All documentation must comply with the lifecycle rules defined in:
  - `/docs/governance/document_lifecycle_guide.md`

---

## 6. Pending Spec Work — Named Owner Assignments

This section tracks canonical spec gaps that have been identified but not yet filled. Items here block the features or releases noted. No feature may enter pre-alignment until its upstream spec gap is closed.

---

### 6.1 Settings Canonical Specification *(v1.6.1 pre-work gate)*

**Status:** Not yet created — gap identified 2026-02-21
**Blocks:** Any further settings-dependent features entering pre-alignment
**Required by:** v1.6.1 (roadmap pre-work item)
**Assigned owner:** Head of Specs Team

**Gap description:** Settings behaviour (`GET /settings`, `PUT /settings`, all fields and constraints) is currently defined only within `settings_endpoints.md` as part of the API contracts domain. There is no standalone canonical document that owns the settings model itself — its fields, defaults, constraints, and meaning — independently of the API layer. As settings-dependent features grow (v1.6 added `default_risk_percent`; v1.6.1 and beyond will add more), this gap creates drift risk.

**Required output:** A new canonical document (tentatively `docs/specs/settings_model.md` or equivalent) that owns the settings domain: all fields, their types, defaults, constraints, and semantics. The API contract continues to own the request/response shape; the new document owns the model. Owner assignment to be confirmed by Head of Specs Team before v1.6.1 pre-alignment opens.

---

### 6.2 Error Response Standard *(v1.6.1 pre-work gate)*

**Status:** Not yet defined — gap identified 2026-02-21
**Blocks:** Consistent error handling across all endpoints; required before v1.6.1 exits
**Required by:** v1.6.1 (roadmap pre-work item)
**Assigned owner:** API Contracts & Documentation Owner (spec definition) + Head of Engineering (implementation alignment)

**Gap description:** Error response shapes are partially covered by `conventions.md` (standard `{ status: error, message: string }` envelope) but canonical error shapes for specific failure modes — validation errors, business rule violations, not-found, and internal errors — are not fully defined or consistently applied across endpoints. `openapi.yaml` defines reusable error responses but these have not been audited for completeness or consistency against actual backend behaviour.

**Required output:** A section in `conventions.md` (or a dedicated `error_responses.md`) that canonicalises: the full error envelope shape, all error codes, HTTP status mapping, and the rule distinguishing HTTP 400 (malformed input) from HTTP 200 with `valid: false` (business rule failure). `openapi.yaml` must then be reviewed for alignment in the same change.

---

## 7. Open Compliance Issues

This section records known lifecycle or governance compliance gaps that have been identified and are pending resolution. Items here do not block current work but must be resolved by the owner before the document is next updated.

---

### 7.1 `docs/operations/validation_system.md` — Owner field non-compliant

**Identified:** 2026-02-21
**Severity:** Advisory (does not block)
**Current state:** `Owner: Platform Team` — a team name, not a named individual role
**Required state:** A named role per `docs/governance/document_lifecycle_guide.md` §7
**Resolution owner:** Infrastructure & Operations Documentation Owner
**Action:** Update the owner field to the named role responsible for this document. Coordinate with Head of Engineering if the correct owner is unclear.

---

## 8. Guiding Principle

> Specs explain decisions.
> This index ensures those decisions form a coherent system.