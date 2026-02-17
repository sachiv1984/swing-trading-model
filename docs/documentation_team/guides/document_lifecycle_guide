# Documentation Lifecycle Guide

**Owner:** Head of Specs Team  
**Scope:** Documentation governance and upkeep  
**Applies to:** Canonical specs, supporting specs, reference artifacts  
**Status:** Canonical

---

## 1. Purpose

This guide defines how documentation is:
- Created
- Maintained
- Reviewed
- Versioned
- Deprecated

Its goal is to prevent:
- Silent drift
- Conflicting sources of truth
- Undocumented behavioral change

---

## 2. Document Classes

### Canonical Documents
- Define authoritative product truth
- Are listed in the Specs Index
- Prevail in case of conflict

Examples:
- Strategy rules
- Data model
- Metrics definitions
- API contract Markdown files

### Supporting Documents
- Represent or summarize canonical truth
- Must never contradict canonical documents
- Are reviewed **inline** with their canonical source

Examples:
- OpenAPI specifications
- Diagrams
- Generated or manually maintained references

Supporting documents **do not introduce new rules**.

---

## 3. Lifecycle States

Every governed document must be in exactly one state:

- **Draft** — in progress, not authoritative
- **Canonical** — authoritative source of truth
- **Deprecated** — superseded, retained for context
- **Archived** — historical only, no longer relevant

Lifecycle state must be declared explicitly in the document header where applicable.

---

## 4. Versioning Rules

Versioning is required when:
- Meaning changes
- Behavior changes
- Interpretation by consumers changes

Versioning is **not required** for:
- Typos
- Formatting
- Pure clarification with no semantic change

---

## 5. Mandatory Inline Review for Supporting Artifacts

When a change affects a **canonical document**:

- Any **supporting or reference artifact** that represents that domain **must be reviewed inline in the same pull request**
- Approval must only be granted once alignment is confirmed

This applies explicitly to:
- API contracts ↔ `docs/reference/openapi.yaml`

If a change is explicitly declared **“no contract change”** and affects only internal implementation:
- Supporting artifact review is not required

Disputes about whether a change is contract‑affecting are escalated to the **Head of Specs Team**.

---

## 6. Ownership & Accountability

- Domain owners are responsible for:
  - Accuracy of their canonical specs
  - Ensuring supporting artifacts remain aligned
- The Head of Specs Team is responsible for:
  - Enforcing lifecycle compliance
  - Blocking merges when alignment is skipped
  - Resolving ambiguity and escalation

Automation may assist review, but **does not replace owner accountability**.

---

## 7. Non‑Negotiable Rule

> If a document influences decisions,  
> it must be owned, reviewed, and aligned at the point of change.

This rule applies regardless of tooling, format, or team.
