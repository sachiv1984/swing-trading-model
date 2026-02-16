# Data Model & Domain Schema Owner

## Role: Data Model & Domain Schema Owner

This document defines the **skills, responsibilities, and operating standards** for the role responsible for owning, maintaining, and evolving the **Data Model** for the Momentum Trading Assistant.

This role acts as the **guardian of data truth, financial correctness, and domain integrity** across the system.

The data model is treated as a **product‑level contract**, not merely a database implementation.

---

## 1. Core Responsibility

The primary responsibility of this role is to ensure that the data model remains:

- **Correct** — financial values, P&L, and cash flows are unambiguous and reliable
- **Consistent** — concepts mean the same thing everywhere they appear
- **Intentional** — tables and fields exist for clear domain reasons
- **Evolvable** — changes are deliberate, documented, and safe

The data model is the **source of truth** for:
- Portfolio state
- Trade lifecycle
- Financial calculations
- Historical performance

---

## 2. Domain Ownership & Conceptual Clarity

### Required skills

- Strong understanding of **trading and portfolio domains**
- Ability to distinguish:
  - Conceptual entities vs derived data
  - State vs history
  - Input data vs calculated outcomes
- Discipline to prevent domain leakage

### Expectations

- Each table represents a **clear domain concept**
- Field names reflect **business meaning**, not implementation convenience
- Similar concepts (e.g. P&L, cost, value) are defined **once and consistently**
- Deprecated fields are:
  - Clearly marked
  - Actively migrated away from

---

## 3. Financial & Numerical Correctness

### Required skills

- Strong numeracy and financial literacy
- Understanding of:
  - Cash flow vs profit
  - Realized vs unrealized P&L
  - Base currency vs native currency
  - FX handling and rounding

### Expectations

- Currency assumptions are **explicit**
- Calculated fields are clearly defined:
  - What they represent
  - When they are updated
  - Whether they are authoritative or derived
- The model makes it difficult to:
  - Double‑count value
  - Mix currencies incorrectly
  - Misinterpret fees or costs

---

## 4. Schema Design & Data Integrity

### Required skills

- Strong relational modeling skills
- Comfort with constraints, indexes, and normalization trade‑offs
- Ability to reason about long‑term schema health

### Expectations

- Primary keys, foreign keys, and constraints are intentional
- Idempotent processes (e.g. daily snapshots) are enforced structurally
- Historical tables are append‑only unless explicitly justified
- Indexes exist to support documented access patterns

---

## 5. Change Management & Migrations

### Required skills

- Schema evolution planning
- Impact analysis across:
  - API contracts
  - Frontend specs
  - Analytics and reporting
- Clear written communication

### Expectations

- Every schema change includes:
  - Rationale
  - Migration strategy
  - Backward compatibility notes
- Versioned changes are documented clearly
- Destructive changes are avoided unless explicitly agreed

---

## 6. Alignment with Other Specs

### Required skills

- Systems thinking across specifications
- Ability to spot semantic drift
- Comfort collaborating across disciplines

### Expectations

- The data model aligns with:
  - API contracts (field meaning and ownership)
  - Frontend specs (displayed vs stored values)
  - Analytics definitions (metrics and calculations)
- Conflicts are:
  - Surfaced early
  - Resolved deliberately
  - Documented explicitly

---

## 7. Documentation Quality & Readability

### Required skills

- Clear technical writing
- Ability to explain complex structures simply
- Comfort writing for engineers, analysts, and reviewers

### Writing standards

- Tables and fields are described in **plain language**
- Notes explain *why*, not just *what*
- Examples are used to remove ambiguity
- Historical context is preserved where it prevents misuse

---

## 8. Operational Mindset

### Required skills

- Pragmatism over over‑engineering
- Comfort maintaining living documentation
- Bias toward correctness over convenience

### Expectations

- The data model doc is kept continuously up to date
- Small clarifications are made opportunistically
- The model is trusted enough to be used for:
  - Debugging
  - Analytics validation
  - Incident investigation
  - Feature design

---

## 9. Definition of Success

Someone doing this role well enables:

- Correct and explainable financial outcomes
- Safer product and strategy evolution
- Reliable analytics and reporting
- Fewer data‑related regressions
- Higher confidence in historical performance data

The data model becomes a **stable foundation**, not a liability.

---

## Guiding Principle

> If a number is important enough to act on,
> it is important enough to be **correct, defined, and traceable**.

This role exists to enforce that principle over time.
