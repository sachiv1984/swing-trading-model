Owner: Head of Specs Team
Status: Canonical  
Version: 2.3  
Last Updated: 2026-02-23  

---

# Documentation Lifecycle Guide

## 1. Purpose

This guide defines how all governed documentation is:

- Classified
- Created
- Maintained
- Reviewed
- Versioned
- Superseded
- Archived
- Enforced

It applies to **all documents that influence decisions**, regardless of function.

---

## 2. Binding Authority

This guide is **binding** on:

- All roles defined in the Team Charter
- All automated governance routines
- All generated artefacts

No process, tool, or delivery pressure may override it.

---

## 3. Document Classes

Every governed document belongs to **exactly one class**.

(Classes 1–6 unchanged from prior version.)

---

## 4. Universal Header Block

Every governed document must declare:

- Owner
- Status
- Last Updated

Canonical documents additionally require:
- Version

Documents without complete headers are **non‑compliant**.

---

## 5. Lifecycle Enforcement Roles

### 5.1 Head of Specs Team

- Owns lifecycle standards
- Blocks non‑compliant documents
- Resolves classification ambiguity
- Conducts audits

---

### 5.2 Facilitator (Process Role)

- Enforces lifecycle compliance during governed routines
- Verifies document class, headers, and state transitions
- May halt execution if lifecycle rules are violated
- Has **no authority** to waive requirements

---

### 5.3 Challenger (Process Role)

- Surfaces lifecycle risk during decision routines
- Requires explicit justification when documents are relied upon
- May delay advancement when documentation integrity is unclear
- Does **not** assess or approve compliance

---

## 6. Lifecycle Enforcement Triggers

Lifecycle review is mandatory when:

- A document is created
- A document is modified
- A feature ships
- A planning document is superseded
- A new role is created
- A governance routine writes artefacts

Non‑compliance is **blocking**.

---

## 7. Planning Documents & Roadmaps

Roadmaps, backlogs, and decision logs are **Class 4 — Planning Documents**.

They:
- Must never be treated as canonical truth
- Must be superseded by canonical specs when implemented
- Must declare ownership and status explicitly

Automated routines must update these documents **only if lifecycle‑compliant**.

---

## 8. Deviations from Canonical Behaviour

Deviation documentation must include:
- Description
- Canonical requirement
- Priority
- Target release
- Owner
- Backlog reference

Missing fields are **non‑compliant**.

---

## 9. Non‑Negotiable Rule

> If a document influences decisions,  
> it must be owned, lifecycle‑compliant,  
> and enforced at the point of change.
