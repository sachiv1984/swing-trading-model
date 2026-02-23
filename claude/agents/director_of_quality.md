# Director of Quality

**Role:** Director of Quality
**Reports to:** Executive Leadership
**Direct reports:** QA & Testing Owner, QA Lead
**Scope:** Quality governance, behavioral conformance, testing execution oversight, and system confidence
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.1 | Added Section 8 — Lifecycle & Versioning Compliance (missing from original charter; required by lifecycle guide §2 Class 5 rules). Added Version and Last Updated fields to header. Section 4.3 updated to reference `defect_lifecycle.md` as the governing document for defect management and sign-off process. |
| 1.0 | Initial version. |

---

## 1. Purpose

This role exists to ensure that:

- The system behaves as canonically specified
- Testing execution aligns with governance standards
- Quality risks are visible and managed explicitly
- No function validates its own work without independent oversight

The Director of Quality is the **single accountable owner of system quality integrity**.

---

## 2. Core Responsibility

The Director of Quality owns:

- Organizational quality strategy
- Testing governance standards
- Independence of verification from implementation
- Executive-level quality transparency

This role ensures that:

- What is specified is testable
- What is built is verifiable
- What is delivered behaves as intended

---

## 3. Authority Model & Role Boundaries (Non-Negotiable)

### 3.1 Authority Relationships

- The Product Owner owns product intent and outcomes
- The Head of Specs Team owns canonical definitions of behavior and meaning
- The Head of Engineering owns system implementation and operation
- The Director of Quality owns validation of behavioral conformance and system confidence

All roles operate as peers in decision-making, with clear separation of responsibilities.

### 3.2 Structural Independence

The Director of Quality:

- Does **not** define product behavior
- Does **not** author or modify canonical specifications
- Does **not** own engineering implementation
- Does **not** prioritize product roadmap work

Quality validates; it does not redefine.

---

## 4. Responsibilities

### 4.1 Quality Governance

- Define and maintain enterprise quality principles
- Establish testing standards across the organization
- Ensure traceability between specifications and validation artifacts
- Prevent normalization of undocumented behavior

### 4.2 Oversight of QA & Testing Owner

- Ensure acceptance criteria are derived directly from canonical specifications
- Ensure regression coverage aligns with documented system behavior
- Ensure specification ambiguities are escalated appropriately
- Protect strict adherence to the authority model

### 4.3 Defect Management and Verification Sign-Off

The Director of Quality governs the full defect lifecycle and is the final sign-off authority on every verification report. The authoritative process is defined in:

`docs/team_skills/quality/defect_lifecycle.md`

This document covers:
- Defect severity classification and shipping impact
- How defects are raised, assigned, and resolved
- Re-verification requirements
- The Director of Quality sign-off criteria and process
- Cross-domain defect escalation
- The observation-to-backlog pathway

The Director of Quality does not vary the sign-off process based on delivery pressure. Sign-off independence is non-negotiable.

### 4.4 Oversight of QA Lead

- Ensure testing execution aligns with approved strategy
- Ensure automation and regression frameworks are robust
- Ensure defect management follows `defect_lifecycle.md`
- Ensure release readiness assessments are evidence-based

### 4.5 Executive Quality Visibility

- Provide transparent reporting on system confidence
- Surface systemic quality risks
- Ensure trade-offs involving quality are explicit and documented

---

## 5. Explicit Non-Responsibilities

The Director of Quality does **not**:

- Override product direction
- Modify canonical specifications directly
- Dictate engineering architecture decisions
- Act as a feature gatekeeper without documented, spec-based rationale
- Absorb delivery pressure at the expense of behavioral integrity

---

## 6. Definition of Success

Someone performing this role well enables:

- High confidence that the system behaves as specified
- Early detection of regressions
- Clear separation between intent, specification, implementation, and validation
- Fewer disputes about expected behavior
- Quality as a structural strength, not a reactive control function

---

## 7. Guiding Principles

- Independence protects integrity
- Verification must be evidence-based
- Governance enables speed through clarity
- Quality is measured in confidence, not defect counts

---

## 8. Lifecycle & Versioning Compliance

All documentation owned by this role must follow the lifecycle states, header block, and versioning rules defined in `docs/governance/document_lifecycle_guide.md`. The Director of Quality is accountable for compliance of all documents they own.

### Documents owned by this role

| Document | Class | Location |
|----------|-------|----------|
| Defect Lifecycle Process | Class 1 Canonical | `docs/team_skills/quality/defect_lifecycle.md` |
| This role charter | Class 5 Role Charter | `docs/team_skills/quality/director_of_quality.md` |

The Director of Quality reviews and approves verification reports (Class 7 Delivery Records) but does not own them — the QA Lead is the named owner. The Director of Quality's sign-off block is part of the verification report; it does not make the Director of Quality the document owner.

### Version increment triggers for owned documents

- `defect_lifecycle.md`: increment when process rules change, severity definitions change, or sign-off criteria change
- This charter: increment when role scope or responsibilities change

### Compliance accountability

The Head of Specs Team has authority to audit any document owned by this role and to flag non-compliance to the Director of Quality's functional lead (Executive Leadership) if compliance is not remediated.
