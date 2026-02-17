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
- `strategy/production_strategy.md` — *Canonical production behavior*
- `strategy/strategy_rules.md` — *Detailed rule mechanics*
- `strategy/Strategy_Rules_&_System_Intent_Owner.md` — *Ownership & governance*

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
- `Data_Model_&_Domain_Schema_Owner.md`

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
- `Metrics_Definitions_&_Analytics_Canonical_Owner.md`

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
- `specs/api_contracts/`

**Canonical Documents**
- `api_contracts/README.md` — *Navigation, scope, versioning*
- `api_contracts/conventions.md` — *Global API rules*
- `api_contracts/*_endpoints.md` — *Domain-specific contracts*
- `API_Contracts_&_Documentation_Owner.md` — *Ownership & governance*

**Owner**
- API Contracts & Documentation Owner

---

### 3.5 Frontend & UX Semantics (Planned)

**What it will own**
- User-visible meanings
- Display states and labels
- Allowed user actions and affordances

**Status**
- Planned / to be formalised

**Owner**
- Frontend Spec Owner (TBD)

---

## 4. Conflict Resolution Order

In case of conflict, precedence is resolved in the following order:

1. **Specs Index**
2. Domain Canonical Spec
3. Supporting Specs
4. Code
5. UI behavior
6. Tribal knowledge

No downstream system may override upstream intent.

---

## 5. Change Governance

- Changes to **domain canonical specs** require domain owner approval
- Changes affecting multiple domains require Head of Specs Team review
- Silent divergence between specs and behavior is treated as a **system bug**

---

## 6. Guiding Principle

> Specs explain decisions.  
> This index ensures those decisions form a coherent system.
``
