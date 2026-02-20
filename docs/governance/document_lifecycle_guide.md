# Documentation Lifecycle Guide

**Owner:** Head of Specs Team
**Scope:** All governed documentation across the entire product
**Status:** Canonical
**Version:** 2.2
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 2.2 | Added Class 7 — Delivery Record. Covers verification reports, lessons learnt records, and phase gate documents — delivery artifacts that are immutable after filing and owned by the QA Lead or PMO Lead respectively. Formalised PMO process templates as Class 1 Canonical sub-type with explicit listing rules. Added test scenario documents as Class 1 Canonical sub-type owned by QA & Testing Owner. Updated lifecycle states table to include Filed as a Class 7 state. Updated enforcement trigger table. Updated PMO process template location reference. |
| 2.1 | Class 4 (Planning Document): added canonical location `docs/product/scope/` for scope documents, naming convention, and scope document as a distinct sub-type with its own supersession rule. Additive only — no existing rules changed. |
| 2.0 | Expanded scope to cover all document classes. Added Operational Record, Planning Document, Role Charter, and Governance Prompt as formal classes. Added universal header block standard. Added enforcement mechanism section. Added trigger rules for governance review. |
| 1.0 | Initial version. Covered Canonical, Supporting, and reference artifacts only. |

---

## 1. Purpose

This guide defines how all product documentation is:
- Classified
- Created
- Maintained
- Reviewed
- Versioned
- Deprecated or archived
- Enforced for compliance

Its goal is to prevent:
- Silent drift between documents and reality
- Conflicting sources of truth
- Undocumented behavioural change
- Documents that influence decisions without a named owner

**This guide applies to every document in the repository** — not only specs. All roles that own documentation are bound by it, regardless of which function they report into.

---

## 2. Document Classes

Every governed document belongs to exactly one class. The class determines which header fields are required, which lifecycle states are valid, and how compliance is checked.

---

### Class 1 — Canonical

**What it is:** The authoritative source of truth for a product domain or process. When this document and any other document disagree, this document prevails.

**Who creates it:** A named domain owner.

**Lifecycle states available:** Draft → Canonical → Deprecated → Archived

**Required header fields:**
```
Owner:        [Role name]
Status:       Canonical
Version:      [x.y]
Last Updated: [date]
```

**Rules:**
- Must be listed in the Specs Index (product domain specs) or the PMO template register in the PMO Lead charter (process templates)
- Must not be contradicted by any Supporting document
- Changes that alter meaning, behaviour, or consumer interpretation require a version increment
- Deprecation requires an explicit successor declaration and effective date

**Sub-types (Class 1):**

*Product and system canonical specs* — define authoritative system behaviour. Owner is the relevant domain spec owner. Listed in the Specs Index.
Examples: `strategy_rules.md`, `data_model.md`, `metrics_definitions.md`, `api_contracts/*_endpoints.md`, `frontend/pages/*.md`

*Process templates* — define authoritative delivery and governance process. Owner is the PMO Lead. Not listed in the Specs Index but listed in the PMO Lead role charter §8. Version incremented when process meaning changes. Deviation from a process template without a change log entry is a process compliance failure.
Examples: `pre_alignment_readiness.md`, `pre_alignment_run.md`, `feature_scope_document.md`, `lessons_learnt.md`, `testing_guide.md`, `templates/phase_gate_template.md`

*Test scenario documents* — define the authoritative set of scenarios the QA Lead executes for a feature. Owner is the QA & Testing Owner. Derived from canonical specs. Versioned when coverage intent changes.
Examples: `docs/testing/{id}-{slug}-test-scenarios.md`

---

### Class 2 — Supporting

**What it is:** A document that represents or summarises canonical truth. It adds no new rules. It must never contradict a Canonical document.

**Who creates it:** The domain owner of the canonical document it supports, or a designated maintainer.

**Lifecycle states available:** Current → Deprecated → Archived (no "Canonical" status — it derives authority from its source)

**Required header fields:**
```
Owner:          [Role name]
Status:         Supporting
Canonical Source: [path to canonical document]
Last Updated:   [date]
```

**Rules:**
- Must be reviewed inline with its canonical source whenever the canonical source changes
- Must declare which canonical document it represents
- A Supporting document becoming inconsistent with its canonical source is a system bug

**Examples:** `docs/reference/openapi.yaml`, diagrams, generated references

---

### Class 3 — Operational Record

**What it is:** A point-in-time record of observed system state. It records facts — it does not define rules or intended behaviour.

**Who creates it:** Infrastructure & Operations Documentation Owner (governs and files); engineering team (generates the underlying data).

**Lifecycle states available:** Filed (permanent — Operational Records are never deprecated or superseded)

**Required header fields:**
```
Owner:              Infrastructure & Operations Documentation Owner
Status:             Operational Record
Deployment Version: [version]
Report Date:        [date]
Environment:        [e.g. Production]
Generated By:       [system or person]
Filed:              [date filed]
```

**Rules:**
- Body content is immutable after filing — it records observed state at a fixed moment
- A newer record does not supersede an older one — both remain permanent artefacts
- Deviations from canonical specs observed in a record must be raised to the relevant domain owner; they are not resolved by annotating the record
- Naming convention: `System_status_report_v{version}_{YYYY-MM-DD}.md`
- Location: `docs/operations/status_reports/`

**Examples:** `System_status_report_v1.4_2026-02-14.md`

---

### Class 4 — Planning Document

**What it is:** A working document capturing product decisions, feature intent, prioritisation, and backlog thinking. It is pre-canonical — when a feature is built, the planning document is superseded by the canonical specs written for that feature.

Planning Documents include two distinct sub-types:

- **Roadmap, backlog, and decisions documents** — ongoing planning artifacts that evolve over time
- **Scope documents** — implementation briefs written at the end of the pre-alignment phase for a specific feature, immediately before engineering begins

**Who creates it:** Product Owner.

**Lifecycle states available:** Draft → Active → Superseded → Archived

**Required header fields:**
```
Owner:        Product Owner
Class:        Planning Document (Class 4)
Status:       [Draft | Active | Superseded]
Last Updated: [date]
```

**Rules:**
- Must carry a standing notice that all implementation detail is indicative and subject to canonical spec review before any code is written
- When a feature moves from planning to implementation, the planning document status is updated to Superseded and must reference the canonical documents that replace it
- Planning documents must never be cited as canonical intent — they record thinking, not decisions
- Implementation detail in planning documents (SQL schemas, endpoint paths, formulas) is illustrative; the canonical spec takes precedence if they conflict

**Scope document additional rules:**
- A scope document must not be written until QA review (acceptance criteria confirmation) is complete
- A scope document is the final gate before implementation is opened — it represents the Product Owner's sign-off that all pre-alignment work is done
- When the feature ships, the scope document status is updated to Superseded and must reference the changelog entry for the delivered version
- Scope documents must include a pre-implementation checklist confirming all canonical specs are locked

**Locations:**
- Roadmap and backlog: `docs/product/roadmap.md`, `docs/product/backlog.md`
- Decisions records: `docs/product/decisions/`
- Scope documents: `docs/product/scope/`

**Naming conventions:**
- Decisions records: `{roadmap-item-id}-{feature-slug}.md` (e.g. `3.2-position-sizing-calculator.md`)
- Scope documents: `scope--{roadmap-item-id}-{feature-slug}.md` (e.g. `scope--3.2-position-sizing-calculator.md`)

**Examples:** `docs/product/roadmap.md`, `docs/product/backlog.md`, `docs/product/decisions/3.2-position-sizing-calculator.md`, `docs/product/scope/scope--3.2-position-sizing-calculator.md`

---

### Class 5 — Role Charter

**What it is:** A document defining the scope, responsibilities, and operating standards of a named role in the documentation or engineering system.

**Who creates it:** Head of Specs Team (for Specs Team roles) or the role's functional lead (for Engineering roles). All charters are stored in `docs/documentation_team/specs/`.

**Lifecycle states available:** Draft → Canonical → Deprecated

**Required header fields:**
```
Owner:        Head of Specs Team [or functional lead]
Status:       Canonical
Version:      [x.y]
Last Updated: [date]
```

**Rules:**
- Every role that owns documents must have a charter
- Every charter must include a "Lifecycle & Versioning Compliance" section explicitly stating that the role owner is accountable for compliance of all documents they own
- Every charter must declare who the role reports to
- Charters are versioned when role scope or reporting line changes
- A role without a charter may not be treated as authoritative — their documents are Draft until a charter exists

**Examples:** `Head_of_Specs_Team.md`, `API_Contracts_&_Documentation_Owner.md`, `Infrastructure_and_Operations_Owner.md`

---

### Class 6 — Governance Prompt

**What it is:** An instruction set used to invoke automated compliance checking against this lifecycle guide. It is part of the governance infrastructure, not a product document.

**Who creates it:** Head of Specs Team.

**Lifecycle states available:** Draft → Active → Deprecated

**Required header fields:**
```
Owner:        Head of Specs Team
Status:       Active
Version:      [x.y]
Last Updated: [date]
```

**Rules:**
- Must reference this lifecycle guide by version
- Must be updated whenever a new document class is added or header requirements change
- Must cover all document classes, not only Canonical documents
- Location: `docs/documentation_team/prompts/`

**Examples:** `governance_reviewer.md`

---

### Class 7 — Delivery Record

**What it is:** A point-in-time record of delivery activity — verification results, process observations, or feature-level gate tracking. Created during or after delivery, immutable after final filing. Does not define rules or canonical intent. Provides permanent traceability for delivery decisions and quality outcomes.

**Who creates it:**
- Verification reports: QA Lead (produced), Director of Quality (signs off)
- Lessons learnt records: PMO Lead
- Phase gate documents: PMO Lead

**Lifecycle states available:** Active (during delivery) → Filed (permanent after final sign-off or shipping closure)

**Required header fields:**
```
Owner:        [QA Lead | PMO Lead]
Class:        Delivery Record (Class 7)
Status:       [Active | Filed]
Feature:      [roadmap item id — feature name]
Version:      [report version, e.g. v1.4]
Date Filed:   [date of final sign-off or shipping closure, or — if Active]
```

**Rules:**
- Body content is immutable after status moves to Filed — no amendments after final sign-off
- A Filed delivery record is a permanent artefact — it is never deleted, deprecated, or superseded
- During Active status (while delivery is in progress), updates are permitted and should include an update history
- Deviations or defects recorded in a delivery record must be resolved through the relevant canonical owner — they are not resolved by annotating the record
- Verification reports must include a Director of Quality sign-off block before status may move to Filed

**Locations:**
- Verification reports: `docs/product/verification/{id}-{slug}-verification.md`
- Lessons learnt records: `docs/product/lessons_learnt/{id}-{slug}-lessons.md`
- Phase gate documents: `docs/product/phase_gates/{id}-{slug}-phase-gate.md`

**Naming conventions:**
- Verification: `{roadmap-item-id}-{feature-slug}-verification.md`
- Lessons learnt: `{roadmap-item-id}-{feature-slug}-lessons.md`
- Phase gate: `{roadmap-item-id}-{feature-slug}-phase-gate.md`

**Examples:** `docs/product/verification/3.2-position-sizing-calculator-verification.md`, `docs/product/lessons_learnt/3.2-position-sizing-calculator-lessons.md`

---

## 3. Lifecycle States

### Universal states (available to all classes unless restricted above)

| State | Meaning | Who sets it | Applies to |
|-------|---------|-------------|------------|
| **Draft** | In progress, not authoritative | Document owner | All classes |
| **Canonical** | Authoritative source of truth | Document owner, confirmed by Head of Specs Team | Class 1, 5 |
| **Active** | In use and current | Document owner | Class 4, 6, 7 (during delivery) |
| **Filed** | Permanently recorded, immutable | QA Lead / PMO Lead (Class 7); Ops Documentation Owner (Class 3) | Class 3, 7 |
| **Superseded** | Replaced by canonical documents | Product Owner | Class 4 |
| **Deprecated** | No longer authoritative; successor declared | Document owner | Class 1, 2, 5, 6 |
| **Archived** | Historical only; no longer referenced | Head of Specs Team | All classes |

**Rules that apply to all classes:**
- Every governed document must be in exactly one state at all times
- State must be declared explicitly in the document header
- No document may move from Deprecated, Filed, or Archived back to an active state — a new document must be created instead
- Deprecation requires: what supersedes it, and from what date

---

## 4. Universal Header Block

Every governed document must carry a header block. The exact fields depend on document class (see Section 2), but the following fields are **required for all classes** except Operational Record and Delivery Record (which have their own fixed sets):

- **Owner** — the named role accountable for this document
- **Status** — one of the lifecycle states defined in Section 3
- **Last Updated** — the date the document was last meaningfully changed

Canonical documents and Role Charters additionally require:
- **Version** — incremented according to the versioning rules in Section 5

A document without a complete header block is non-compliant and must not be treated as authoritative regardless of its content.

---

## 5. Versioning Rules

Versioning applies to Canonical documents (Class 1), Role Charters (Class 5), and Governance Prompts (Class 6).

**A version increment is required when:**
- Meaning changes
- Behaviour or rules change
- A consumer reading the document would act differently as a result

**A version increment is not required for:**
- Typo corrections
- Formatting changes
- Pure clarification that adds no new meaning

**Version format:** `x.y` where `x` (major) increments on breaking or significant behavioural changes, and `y` (minor) increments on additive or clarifying changes.

**Delivery Records (Class 7)** use a report version (e.g. v1.0, v1.1, v1.4) that tracks iterations within a single document during Active status. This is not the same as the document class versioning scheme — it records how many times the document was updated during delivery, not a governance version increment.

---

## 6. Mandatory Inline Review for Supporting Artifacts

When a change affects a Canonical document:

- Any Supporting document that represents that domain must be reviewed inline in the same change
- Approval must only be granted once alignment is confirmed

This applies explicitly to:
- API contracts ↔ `docs/reference/openapi.yaml`

If a change is explicitly declared "no contract change" and affects only internal implementation, Supporting artifact review is not required. Disputes are escalated to the Head of Specs Team.

---

## 7. Ownership & Accountability

**Every document must have a named owner.** A document without an owner is non-compliant.

**Domain owners are responsible for:**
- Accuracy of their documents
- Keeping documents current when the system they describe changes
- Ensuring Supporting documents remain aligned with their Canonical sources
- Initiating deprecation when a document is superseded

**The Head of Specs Team is responsible for:**
- Enforcing lifecycle compliance across all document classes
- Blocking changes when lifecycle rules are violated
- Resolving ambiguity about document class or ownership
- Maintaining and updating this guide
- Conducting or triggering compliance audits

**The Head of Specs Team has authority to audit any document in the repository** regardless of which function its owner reports into. Lifecycle compliance is a cross-functional standard, not a Specs Team internal rule.

---

## 8. Enforcement Mechanism

### When compliance is checked

Governance review must be triggered at the following points:

| Trigger | What is reviewed | Who triggers it |
|---------|-----------------|-----------------|
| New document created | Header completeness, correct class assignment, owner named | Document owner (self-check), Head of Specs Team (on merge) |
| Existing document updated | Version increment if required, header currency | Document owner (self-check), Head of Specs Team (on merge) |
| Feature shipped | Planning documents updated to Superseded; verification report status → Filed; phase gate document status → Filed; canonical specs confirmed filed | Head of Specs Team |
| New role created | Charter exists and is compliant before role is treated as authoritative | Head of Specs Team |
| Periodic audit | All documents checked for compliance | Head of Specs Team (quarterly recommended) |
| Governance guide updated | Governance reviewer prompt updated in same change | Head of Specs Team |
| Delivery record filed | Class 7 header complete, Director of Quality sign-off present (verification reports), status set to Filed | QA Lead / PMO Lead (self-check), Head of Specs Team (on merge) |

### How compliance is checked

The governance reviewer prompt (`docs/documentation_team/prompts/governance_reviewer.md`) is the primary compliance tool. It must be invoked using the prompt as a system instruction with the document(s) under review provided as context.

Automated review assists but does not replace owner accountability.

### What happens when compliance fails

| Severity | Condition | Consequence |
|----------|-----------|-------------|
| **Blocking** | Missing owner, missing status, Canonical document with no version | Document must not be merged or treated as authoritative until remediated |
| **Required** | Incorrect lifecycle state, version not incremented when required, Supporting artifact not reviewed inline, Delivery Record missing Class 7 header | Must be remediated before the change is considered complete |
| **Advisory** | Minor header formatting inconsistency, Last Updated date stale | Should be remediated; does not block |

---

## 9. Roles Outside the Specs Team

This guide applies to **all roles that own documents**, including those outside the Specs Team. Specifically:

- **Product Owner** — Planning Documents must follow Class 4 rules
- **Engineering Lead** — any documentation owned by the engineering function must follow this guide
- **Infrastructure & Operations Documentation Owner** — Operational Records and Operational Guides must follow Class 3 and Class 1 rules respectively
- **QA & Testing Owner** — test scenario documents are Class 1 Canonical; must follow Class 1 rules
- **QA Lead** — verification reports are Class 7 Delivery Records; must follow Class 7 rules
- **PMO Lead** — process templates are Class 1 Canonical; lessons learnt records and phase gate documents are Class 7 Delivery Records

The Head of Specs Team sets these standards. Roles outside the Specs Team follow them. This is a standards relationship, not a management relationship — the Head of Specs Team does not manage those roles but does have authority to flag non-compliance to their functional lead.

---

## 10. Non-Negotiable Rule

> If a document influences decisions,
> it must be owned, reviewed, and aligned at the point of change.
