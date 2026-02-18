# QA & Testing Owner

**Role:** QA & Testing Owner  
**Reports to:** Engineering Lead  
**Governance alignment:** Head of Specs Team (documentation lifecycle, document classes, headers, naming conventions)  
**Scope:** Test strategy, acceptance criteria, regression coverage, and testing documentation  
**Status:** Canonical

---

## 1. Purpose

This role exists to ensure that system behavior defined in canonical specifications is:

- Testable
- Verifiable
- Protected against regression
- Continuously validated as specifications evolve

The QA & Testing Owner is the guardian of **behavioral confidence** across the system.

---

## 2. Core Responsibility

The QA & Testing Owner owns:

- Test strategy across unit, integration, system, and regression layers
- Acceptance criteria derived directly from canonical specifications
- Test scenario documentation and maintenance
- Regression coverage aligned to documented system behavior

This role ensures that **what is specified can be tested**, and that **what is tested reflects the specification**.

---

## 3. Relationship to Canonical Specifications (Non‑Negotiable)

Testing artifacts are **supporting documents** and must respect strict boundaries.

### 3.1 Authority Model

- Canonical specifications define intended system behavior.
- Tests verify adherence to canonical specifications.
- Tests do not define or reinterpret behavior.

In the event of conflict, canonical specifications always prevail.

### 3.2 Mandatory Rules for Testing & QA Artifacts

Testing documentation and scenarios owned by this role:

1. **Derive acceptance criteria directly from canonical specifications**  
   Acceptance criteria must reference the relevant canonical spec sections.

2. **Do not introduce new rules, constraints, or behavior**  
   Tests validate behavior; they do not define it.

3. **Do not modify canonical specifications**  
   If a spec is ambiguous, untestable, or inconsistent, the issue is raised to the owning domain.

4. **Do not encode workarounds or bugs as intended behavior**  
   Deviations are documented as observed behavior and escalated for resolution.

> Tests prove correctness against intent; they do not replace intent.

---

## 4. Required Skills

- Strong understanding of testing strategies and quality risk management
- Ability to translate specifications into clear, testable acceptance criteria
- High attention to detail and edge‑case reasoning
- Clear technical writing for test scenarios and documentation
- Comfort working across engineering, product, and specification owners

---

## 5. Responsibilities

### 5.1 Test Strategy Ownership

- Define and maintain the overall testing strategy
- Ensure appropriate coverage across:
  - Core behavior
  - Edge cases
  - Failure modes
  - Regression risk
- Balance depth of testing with system criticality

### 5.2 Acceptance Criteria Stewardship

- Derive acceptance criteria explicitly from canonical specifications
- Ensure criteria are:
  - Deterministic
  - Unambiguous
  - Verifiable
- Keep acceptance criteria aligned as specs change

### 5.3 Regression Coverage Management

- Identify behavior that must not regress
- Ensure regression tests exist for critical paths
- Periodically review coverage against current specifications

### 5.4 Testing Documentation Maintenance

- Maintain clear, up‑to‑date testing documentation, including:
  - Test scenarios
  - Behavioral matrices
  - Regression coverage summaries
- Ensure documentation reflects current intended behavior, not historical accidents

### 5.5 Spec Feedback Loop

When a specification is:
- Ambiguous
- Internally inconsistent
- Not practically testable

The QA & Testing Owner:
- Documents the issue clearly
- References the affected spec sections
- Raises it to the relevant canonical owner for resolution

---

## 6. Explicit Non‑Responsibilities

This role does **not**:

- Define system behavior or business rules
- Change canonical specifications directly
- Decide product intent or UX behavior
- Normalize bugs or deviations through tests
- Act as a gatekeeper without documented, spec‑based rationale

---

## 7. Reporting & Interfaces

### Reports to
- Engineering Lead

### Governed by
- Head of Specs Team (documentation lifecycle and classification enforcement)

### Works closely with
- Strategy Rules & System Intent Owner
- Data Model & Domain Schema Owner
- API Contracts & Documentation Owner
- Metrics Definitions & Analytics Owner
- Frontend Specifications & UX Owner

---

## 8. Lifecycle & Versioning Compliance

All testing documentation owned by this role must:

- Declare lifecycle state (Draft / Canonical / Deprecated / Archived)
- Follow approved headers and naming conventions
- Be versioned when meaning or coverage intent changes
- Be reviewed when linked canonical specifications change

---

## 9. Definition of Success

Someone doing this role well enables:

- High confidence that the system behaves as specified
- Early detection of behavioral regressions
- Faster, safer change through clear acceptance criteria
- Fewer disputes about “expected behavior”
- Strong feedback loops between specs, implementation, and validation

Testing becomes a **trust mechanism**, not a bottleneck.

---

## 10. Guiding Principles

- If behavior matters, it must be testable.
- Tests validate intent; specs define it.
- Regressions are failures of alignment, not surprises.
- Quality is enforced through clarity, not heroics.
