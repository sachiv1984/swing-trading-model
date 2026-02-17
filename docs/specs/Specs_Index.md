# Specs Index (Canonical)

**Owner:** Head of Specs Team  
**Purpose:** Single map of canonical product truth  
**Audience:** Product, Engineering, Analytics, Strategy  
**Status:** Authoritative

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
- “Where is X defined?”
- “Which rules apply?”
- “Who owns this decision?”
- “Can I change this safely?”

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
- Approval is blocked if OpenAPI alignment is skipped for contract‑affecting changes.

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

## 4. Conflict Resolution Order

In case of conflict, precedence is resolved in the following order:

1. **Specs Index**
2. Domain Canonical Spec
3. Supporting Specs
4. Reference Artifacts (e.g. OpenAPI)
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
  - `/docs/documentation_team/guides/DOC_LIFECYCLE_GUIDE.md`

---

## 6. Guiding Principle

> Specs explain decisions.  
> This index ensures those decisions form a coherent system.
