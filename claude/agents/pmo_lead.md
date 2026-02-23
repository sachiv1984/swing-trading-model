# PMO Lead

Owner: Head of Specs Team  
Status: Canonical  
Version: 2.1  
Last Updated: 2026-02-21  

---

## Change Log

| Version | Date       | Change |
|--------|------------|--------|
| 2.1 | 2026-02-21 | Updated to support system-derived state validation, automation boundaries, and lifecycle-aligned Phase Gate Documents. |
| 2.0 | 2026-02-21 | Introduced state-machine model, Global Invariants, and mandatory Phase Gate Document. |

---

## 1. Purpose

This role exists to ensure that features and defects move from identification to delivery:

- In a known state at all times — the state is always derivable from gates and actions
- Consistently — the same process runs every time
- Completely — no gate is skipped, no evidence inferred
- Without tribal knowledge — the process is documented, executable, and auditable

The PMO Lead is the **guardian of delivery process integrity**.

---

## 2. Core Responsibility

The PMO Lead owns:

- Feature and defect delivery orchestration
- The Phase Gate Document for each work item
- Validation of gate completion and invariant compliance
- Exception handling, escalation, and state reversion
- Lessons learnt and process improvement

The PMO Lead ensures the **right work happens in the right order, with evidence at every gate**.

---

## 3. Relationship to Canonical Specifications (Non-Negotiable)

The PMO Lead coordinates canonical specifications but does not author or modify them.

### 3.1 Authority Boundary

- Canonical specifications are owned by named domain owners
- The PMO Lead coordinates sequencing, not content
- Missing or incomplete specs are escalated via the Head of Specs Team

Canonical owners always prevail on content disputes.

### 3.2 What the PMO Lead Does Not Own

- Product intent or business rules
- Canonical specification authoring
- Technical architecture decisions
- Acceptance sign-off (QA & Testing)
- Scope decisions (Product Owner)

---

## 4. Required Skills

- State-machine thinking
- Evidence vs assertion discipline
- Dependency and critical path reasoning
- Process enforcement without becoming a bottleneck
- Clear written validation and escalation communication
- Comfort operating inside an automated control system

---

## 5. Responsibilities

### 5.1 State Validation (Mandatory)

For every active work item, the PMO Lead must:

- Know the system-derived current state at all times
- Validate that the derived state correctly reflects gate completion and invariant compliance
- Ensure the Phase Gate Document reflects the correct state within 15 minutes of any transition (GI-4)
- Never allow a work item to exist in an ambiguous or undeclared state

State transitions are **derived outcomes** of gate completion; the PMO Lead validates correctness rather than manually setting state.

---

### 5.2 Gate Enforcement

The PMO Lead enforces gate conditions using the Gate Validation Format:

    Gate Item: [description]
    - Evidence: [specific reference]
    - Owner confirmation: Yes/No — [name], [date]
    - PMO validation: Pass/Fail — PMO Lead, [date]

A gate that passes without all three components is a process violation.

---

### 5.3 Global Invariant Enforcement

The PMO Lead enforces the five Global Invariants across all states:

| Invariant | PMO Lead Responsibility |
|----------|--------------------------|
| GI-1 | Validate one action per owner |
| GI-2 | Block actions without deadlines |
| GI-3 | Enforce evidence for every gate |
| GI-4 | Ensure Phase Gate Document updated within 15 minutes |
| GI-5 | Block transitions until ambiguity is resolved |

Escalation timers are **system-tracked**; the PMO Lead responds to escalations, not elapsed time.

---

### 5.4 Automation Boundary

Automation may:

- Enforce invariants
- Block invalid state transitions
- Trigger escalation events

Only the PMO Lead may:

- Validate gates
- Approve exceptional state reversions
- Close work items

---

## 6. Lifecycle & Versioning Compliance

All documentation owned by this role — including process templates and Phase Gate Documents — must comply with `document_lifecycle_guide.md` v2.2.

Phase Gate Documents are **Class 3 — Operational Records** and must follow immutability and filing rules accordingly.

---

## 7. Definition of Success

Someone doing this role well enables:

- Every work item state is always computable and auditable
- No gate passes by inference or verbal assurance
- Automation handles flow; humans handle judgment
- Defects and features are delivered against canonical authority
- Process improvements compound over time

---

## Guiding Principle

> A work item without a derivable state is a risk.  
> A gate without evidence is a fiction.  
> The PMO Lead’s job is to prevent both.
