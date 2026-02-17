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
- Lifecycle rules
- Parameter governance

**Canonical Documents**
- `strategy/production_strategy.md` — *Canonical production behavior*
- `strategy/strategy_rules.md` — *Detailed rule mechanics*
- `strategy/strategy_intent_owner.md` — *Ownership & governance*

**Owner**
- Strategy Rules & System Intent Owner

---

### 3.2 Data Model

**What it owns**
- Meaning of fields (price, stop, P&L, value)
- Currency semantics
- State representations

**Canonical Documents**
- `data-model/data_model.md`

**Owner**
- Data Model Owner

---

### 3.3 Metrics & Analytics

**What it owns**
- Definitions of performance metrics
- Calculation methods
- Time alignment rules

**Canonical Documents**
- `metrics/metrics_definitions.md`

**Owner**
- Metrics Owner

---

### 3.4 API Contracts

**What it owns**
- Request/response schemas
- Field guarantees
- Backward compatibility rules

**Canonical Documents**
- `api/api_contracts.md`

**Owner**
- API Spec Owner

---

### 3.5 Frontend & UX Semantics

**What it owns**
- User-visible meanings
- Labels, states, and affordances
- What the user is allowed to do and see

**Canonical Documents**
- `frontend/frontend_specs.md`

**Owner**
- Frontend Spec Owner

---

## 4. Conflict Resolution Order

In case of conflict, precedence is resolved in the following order:

1. **Specs Index**
2. Domain Canonical Spec (e.g. Production Strategy)
3. Supporting Specs
4. Code
5. UI behavior
6. Tribal knowledge

No downstream system may override upstream intent.

---

## 5. Change Governance

- Changes to **domain specs** require owner approval
- Changes affecting multiple domains require Head of Specs Team review
- Silent divergence is treated as a system bug

---

## 6. Guiding Principle

> Specs explain decisions.  
> This index ensures those decisions form a coherent system.
