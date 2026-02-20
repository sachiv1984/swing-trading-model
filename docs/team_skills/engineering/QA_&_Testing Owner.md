# QA & Testing Owner

**Role:** QA & Testing Owner
**Reports to:** Engineering Lead
**Governance alignment:** Head of Specs Team (documentation lifecycle, document classes, headers, naming conventions)
**Scope:** Test strategy, acceptance criteria, regression coverage, and testing documentation
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.1 | Section 8 (Lifecycle & Versioning Compliance) updated: test scenario documents formally classified as Class 1 Canonical, with governed location, naming convention, and version increment rule. Version and Last Updated fields added to header to bring charter into full Class 5 compliance. |
| 1.0 | Initial version. |

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
- Ensure appropriate coverage across: core behavior, edge cases, failure modes, and regression risk
- Balance depth of testing with system criticality

### 5.2 Acceptance Criteria Stewardship

- Derive acceptance criteria explicitly from canonical specifications
- Ensure criteria are deterministic, unambiguous, and verifiable
- Keep acceptance criteria aligned as specs change

### 5.3 Regression Coverage Management

- Identify behavior that must not regress
- Ensure regression tests exist for critical paths
- Periodically review coverage against current specifications

### 5.4 Test Scenario Document Authorship

- Author the test scenario document for each feature during Phase 4, after QA review gate and before implementation opens
- Derive every scenario directly from the canonical specs confirmed during the QA review
- Follow the format and coverage rules defined in `docs/team_skills/pmo/processess/testing_guide.md`
- Ensure the test scenario document is available to the QA Lead before Phase 5 begins
- Update the test scenario document version when coverage intent changes

### 5.5 Testing Documentation Maintenance

- Maintain clear, up‑to‑date testing documentation including test scenarios, behavioral matrices, and regression coverage summaries
- Ensure documentation reflects current intended behavior, not historical accidents

### 5.6 Spec Feedback Loop

When a specification is ambiguous, internally inconsistent, or not practically testable, the QA & Testing Owner:
- Documents the issue clearly
- References the affected spec sections
- Raises it to the relevant canonical owner for resolution before writing scenarios against it

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
- QA Lead (hands off test scenario document before Phase 5)
- PMO Lead (coordinates Phase 4 timing and Phase 5 readiness)

---

## 8. Lifecycle & Versioning Compliance

All documentation owned by this role must follow the lifecycle states, header block, and versioning rules defined in `docs/governance/document_lifecycle_guide.md`. The QA & Testing Owner is accountable for compliance of all documents they own.

### Test Scenario Documents — Class 1 Canonical

Test scenario documents are **Class 1 Canonical** documents. They define the authoritative set of scenarios against which a feature is verified. The QA Lead executes them; the QA & Testing Owner owns them.

**Required header fields:**
```
Owner:        QA & Testing Owner
Class:        Canonical (Class 1)
Status:       Canonical
Version:      [x.y]
Last Updated: [date]
Derived from: [list of canonical specs with versions]
```

**Location:** `docs/testing/{roadmap-item-id}-{feature-slug}-test-scenarios.md`

**Naming convention:** `{roadmap-item-id}-{feature-slug}-test-scenarios.md`
Example: `3.2-position-sizing-calculator-test-scenarios.md`

**Version increment rules:**
- Increment required when: coverage intent changes, a scenario is added or removed, a scenario step or expected result is corrected in a way that would change the QA Lead's execution
- No increment required for: typo fixes, formatting changes, clarifications that do not alter how the scenario is executed

**Review trigger:** When a canonical spec linked in the `Derived from` header is updated, the QA & Testing Owner must review the test scenario document and update it if coverage is affected.

### This Charter — Class 5 Role Charter

This document is a Class 5 Role Charter. It must be versioned when role scope or responsibilities change.

---

## 9. Definition of Success

Someone doing this role well enables:

- High confidence that the system behaves as specified
- Early detection of behavioral regressions
- Faster, safer change through clear acceptance criteria
- Fewer disputes about "expected behavior"
- Strong feedback loops between specs, implementation, and validation

Testing becomes a **trust mechanism**, not a bottleneck.

---

## 10. Guiding Principles

- If behavior matters, it must be testable.
- Tests validate intent; specs define it.
- Regressions are failures of alignment, not surprises.
- Quality is enforced through clarity, not heroics.
