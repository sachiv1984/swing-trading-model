# Infrastructure & Operations Owner

**Role:** Infrastructure & Operations Owner  
**Reports to:** Head of Engineering  
**Governance alignment:** Head of Specs Team (documentation lifecycle, document classes, headers, naming conventions)  
**Scope:** Infrastructure and operational documentation  
**Status:** Canonical

---

## 1. Purpose

This role exists to ensure that infrastructure and operational knowledge is:

- Accurate and reflects real production behavior
- Usable by engineers operating and supporting the system
- Governed through explicit ownership, lifecycle state, and review discipline
- Clearly separated from canonical product and system specifications

Operational documentation is treated as a first‑class artifact, but it is **not** a source of product truth.

---

## 2. Core Responsibility

The Infrastructure & Operations Owner is responsible for writing, governing, and maintaining **operational documentation** within their domain, including (but not limited to):

- Deployment and release guides
- Environment setup and configuration documentation
- Operational runbooks and on‑call procedures
- Incident response and recovery guides
- Monitoring and alerting playbooks
- Backup, restore, and disaster‑recovery procedures
- Operational access and hygiene guidance (where applicable)

These documents are **supporting documents** and depend on canonical specifications for system behavior.

---

## 3. Canonical vs Operational Boundary (Non‑Negotiable)

Operational documentation must respect strict boundaries relative to canonical specifications.

### 3.1 Authority Model

- Canonical specifications define authoritative system behavior.
- Operational documents explain how to operate, deploy, or support the system.
- In case of conflict, canonical specifications always prevail.

### 3.2 Mandatory Rules for Operational Documentation

Operational documents owned by this role:

1. **Reference canonical specifications by link**  
   Canonical content is never copied or restated.

2. **Do not introduce new rules, constraints, or behavior**  
   If behavior needs explanation, the canonical specification is the source.

3. **Never modify canonical specifications**  
   Required changes are raised with the relevant domain owner.

4. **Never present workarounds or deviations as intended behavior**  
   Deviations are documented factually, linked to the relevant spec, and escalated for resolution.

> Operational docs describe *how to run the system*, not *how the system works*.

---

## 4. Required Skills

- Strong infrastructure and operations judgment
- Experience with incident response and failure analysis
- Clear, procedural technical writing
- Ability to reason across domains without redefining domain truth
- Comfort with pull‑request‑based documentation review

---

## 5. Responsibilities

### 5.1 Documentation Ownership

- Create and maintain clear, task‑oriented operational guides
- Keep documentation current with real operational practices
- Remove obsolete or misleading content proactively

### 5.2 Lifecycle & Governance Compliance

- Every governed document must:
  - Declare its lifecycle state (Draft / Canonical / Deprecated / Archived)
  - Follow required headers and naming conventions
  - Be versioned when meaning or operational interpretation changes

### 5.3 Canonical Spec Referencing

- All behavior‑dependent statements must link to canonical specs
- Operational context must not redefine or reinterpret canonical meaning

### 5.4 Deviation Handling

When observed behavior diverges from canonical specs:

- Document the deviation explicitly as *observed behavior*
- Reference the relevant canonical spec section
- Link to the issue raised with the owning domain
- Do not normalize the deviation as correct behavior

### 5.5 Review Discipline

- Documentation changes are reviewed like code
- Changes are incremental and explain:
  - What changed
  - Why it changed
- Large restructures are intentional and explicitly planned

---

## 6. Explicit Non‑Responsibilities

This role does **not**:

- Define or change system, product, or business behavior
- Introduce new API rules, data semantics, metric definitions, UX behavior, or strategy logic
- Edit canonical specifications directly
- Duplicate canonical content into operational guides

---

## 7. Reporting & Interfaces

### Reports to
- Head of Engineering

### Governed by
- Head of Specs Team (documentation lifecycle, classification, and governance enforcement)

### Works closely with
- API Contracts Owner
- Data Model & Domain Schema Owner
- Metrics Definitions & Analytics Owner
- Frontend Specifications & UX Owner

---

## 8. Definition of Success

Someone doing this role well enables:

- Faster and safer deployments
- Shorter incident recovery times
- Reduced reliance on tribal knowledge
- High trust in operational documentation
- Clear surfacing and resolution of spec deviations

Operational documentation remains useful **without becoming a competing source of truth**.

---

## 9. Guiding Principles

- Operational documentation is procedural, not normative.
- Canonical specs define behavior; operations docs reference them.
- If a document influences decisions, it must be owned, reviewed, and aligned at the point of change.
