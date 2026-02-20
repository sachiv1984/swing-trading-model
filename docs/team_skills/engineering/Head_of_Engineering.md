# Head of Engineering

**Role:** Head of Engineering
**Reports to:** Executive Leadership
**Governance alignment:** Head of Specs Team (canonical truth, documentation lifecycle enforcement)
**Scope:** Engineering delivery, technical execution, and operational accountability
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.1 | Section 8 (Governance & Documentation Expectations) expanded: added implementation intake requirement referencing `implementation_intake.md`, and mid-implementation spec query process referencing `spec_query_process.md`. Version and Last Updated fields added to header to bring charter into full Class 5 compliance. |
| 1.0 | Initial version. |

---

## 1. Purpose

This role exists to ensure that the engineering organization:

- Delivers reliable, high‑quality systems aligned with product and strategy intent
- Executes against canonical specifications accurately and consistently
- Operates systems safely in production
- Scales sustainably in people, process, and technical capability

The Head of Engineering is accountable for **how the system is built, delivered, and operated**, not for defining canonical product truth.

---

## 2. Core Responsibility

The Head of Engineering owns:

- Engineering execution and delivery outcomes
- Technical implementation decisions and architectural direction
- Engineering team structure, capability, and performance
- Operational readiness, reliability, and incident accountability

This role ensures that **canonical intent becomes working, reliable software**.

---

## 3. Relationship to Canonical Specifications (Non‑Negotiable)

### 3.1 Authority Boundary

- Canonical specifications define *what the system does* and *how it is expected to behave*.
- Engineering defines *how that behavior is implemented*.
- Engineering implementation must conform to canonical specifications.

In case of conflict:
- Canonical specifications prevail.
- Engineering escalates ambiguity or infeasibility rather than compensating silently.

### 3.2 Enforcement Responsibility

The Head of Engineering is responsible for ensuring that:

- Engineering teams treat canonical specs as authoritative
- Implementation does not redefine behavior through code, tests, or operations
- Deviations are surfaced, documented, and resolved through the proper owners

---

## 4. Required Skills

- Strong engineering leadership and people management
- Deep understanding of system design, architecture, and trade‑offs
- Delivery planning and execution discipline
- Operational and reliability mindset
- Clear written and verbal communication across technical and non‑technical audiences

---

## 5. Responsibilities

### 5.1 Engineering Delivery & Execution

- Own delivery timelines and execution quality
- Ensure engineering work aligns with agreed scope and intent
- Balance speed, quality, and technical sustainability
- Make pragmatic implementation trade‑offs explicit and reviewable

### 5.2 Technical Architecture & Implementation Direction

- Set and evolve architectural direction
- Ensure consistency across systems and teams
- Prevent ad‑hoc divergence that increases long‑term complexity
- Allow local autonomy within clear architectural guardrails

### 5.3 Operational Accountability

- Own production readiness and system reliability
- Ensure effective incident response and post‑incident learning
- Support Infrastructure & Operations ownership with prioritization and resourcing
- Treat operational issues as engineering responsibilities, not externalities

### 5.4 Team Structure & Capability

- Build and maintain effective engineering team structures
- Hire, develop, and retain strong engineers and engineering leaders
- Ensure ownership is clear and sustainable
- Grow judgment, not just output

### 5.5 Cross‑Role Coordination

- Ensure effective collaboration between Infrastructure & Operations Owner, QA & Testing Owner, and canonical spec owners
- Resolve delivery conflicts and prioritization issues
- Escalate specification conflicts through the proper governance path

---

## 6. Explicit Non‑Responsibilities

The Head of Engineering does **not**:

- Own or define canonical specifications
- Decide product intent, business rules, or analytical meaning
- Modify canonical specs directly
- Allow implementation or tests to become de facto sources of truth

This role enforces alignment; it does not replace specification ownership.

---

## 7. Reporting & Interfaces

### Reports to
- Executive Leadership

### Manages
- Engineering Leads
- Infrastructure & Operations Owner
- QA & Testing Owner
- Engineering contributors and managers

### Works closely with
- Head of Specs Team
- Product and Strategy leadership
- Design and Analytics leadership
- PMO Lead (implementation open, defect assignment, shipping coordination)

---

## 8. Governance & Documentation Expectations

The Head of Engineering ensures that:

- Engineering‑owned documentation follows lifecycle and naming rules
- Supporting documents do not conflict with canonical specifications
- Documentation changes are reviewed with the same discipline as code
- Engineering participates constructively in spec reviews and alignment

### Implementation Intake

When the PMO Lead declares implementation open for a feature, the Head of Engineering runs the implementation intake checklist before any code is written:

`docs/team_skills/engineering/implementation_intake.md`

This confirms: scope document read, spec versions locked, test scenarios reviewed, spec query path understood, feasibility concerns surfaced. If any intake item cannot be checked, the Head of Engineering notifies the PMO Lead before proceeding. Engineering does not start implementation while unresolved intake blockers exist.

### Mid-Implementation Spec Queries

When engineering encounters an ambiguity, gap, or conflict in a canonical specification during implementation:

1. **Do not build a guess.** If a spec point materially affects implementation, raise the question before building against an interpretation.
2. **Use the spec query process** defined at `docs/team_skills/specs/spec_query_process.md`. This sets out the format, the correct recipient (spec owner, not PMO Lead), the turnaround expectation, and the record-keeping requirement.
3. **Notify the PMO Lead immediately** if implementation must pause pending an answer. The Phase Gate Document must be updated and stakeholders notified.
4. **Spec patches come before fixes.** If resolving a defect requires a canonical spec change, the spec owner must patch the spec first. Engineering implements against the updated spec. Do not fix the code and update the spec retrospectively.

The Head of Engineering is responsible for ensuring all engineers on the team understand and follow this process.

---

## 9. Definition of Success

Someone doing this role well enables:

- Predictable, high‑quality delivery
- Systems that behave as specified
- Fewer production surprises
- Clear accountability during incidents
- Engineering teams that scale without chaos

Engineering becomes a **reliable execution engine**, not a source of ambiguity.

---

## 10. Lifecycle & Versioning Compliance

All documentation owned by this role must follow the lifecycle states, header block, and versioning rules defined in `docs/governance/document_lifecycle_guide.md`. The Head of Engineering is accountable for compliance of all documents they own.

### Documents owned by this role

| Document | Class | Location |
|----------|-------|----------|
| Implementation Intake | Class 1 Canonical | `docs/team_skills/engineering/implementation_intake.md` |
| This role charter | Class 5 Role Charter | `docs/team_skills/engineering/Head_of_Engineering.md` |

### Guiding Principles

- Canonical intent is implemented, not interpreted.
- Engineering owns execution and reliability.
- Deviations are surfaced, not normalized.
- Sustainable delivery beats short‑term heroics.
