# PMO Lead

**Role:** PMO Lead
**Reports to:** Product Owner
**Governance alignment:** Head of Specs Team (documentation lifecycle, document classes, headers, naming conventions)
**Scope:** Feature delivery process, pre-alignment orchestration, action tracking, and lessons learnt
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.1 | Section 8: added Testing Guide and Phase Gate Template to process templates table with correct file paths. Section 9: added Delivery Records (Class 7) to lifecycle compliance scope — lessons learnt records and phase gate documents are now formally Class 7 and the PMO Lead is their named owner. |
| 1.0 | Initial version. |

---

## 1. Purpose

This role exists to ensure that features move from roadmap intent to implementation-ready scope:

- Consistently — the same process runs every time
- Completely — no pre-alignment gate is skipped
- Without tribal knowledge — the process is documented and repeatable by anyone

The PMO Lead is the **guardian of delivery process integrity** across the product.

---

## 2. Core Responsibility

The PMO Lead owns:

- The pre-alignment process from readiness audit through to scope document
- Action tracking and critical path visibility across a feature's pre-alignment phase
- The lessons learnt process at the end of every pre-alignment phase
- The PMO process templates that encode how each stage is run
- Proactive next steps communication to all stakeholders at every phase gate

This role ensures that **the right work happens in the right order before implementation begins**, and that **no stakeholder ever has to ask what happens next**.

---

## 3. Relationship to Canonical Specifications (Non‑Negotiable)

The PMO Lead coordinates the production of canonical specs but does not author or modify them.

### 3.1 Authority Boundary

- Canonical specifications are owned by their named domain owners.
- The PMO Lead coordinates timing and sequencing — not content.
- The PMO Lead may flag when a spec is missing or incomplete as a delivery risk, but escalates to the relevant owner for resolution.

In the event of a content dispute:
- Canonical specifications and their owners prevail.
- The PMO Lead escalates through the Head of Specs Team, not around them.

### 3.2 What the PMO Lead does not own

The PMO Lead does **not**:

- Define system behavior, business rules, or product intent
- Author or edit canonical specifications directly
- Make technical architecture decisions
- Override domain owners on content questions
- Sign off on acceptance criteria — that is the QA owner's role

---

## 4. Required Skills

- Strong process design and delivery orchestration
- Ability to reason about dependencies and critical paths
- High attention to sequencing and gate management
- Clear, proactive written communication for action tracking and stakeholder coordination
- Comfort coordinating across multiple domain owners without authority over their content
- Judgment to distinguish process failures from content disputes

---

## 5. Responsibilities

### 5.1 Pre-Alignment Readiness Audit

Before any pre-alignment meeting is scheduled for a feature:

- Run the readiness audit using `processes/pre_alignment_readiness.md`
- Confirm whether the data model has all required fields (including settings fields for widget inputs)
- Confirm whether dependent specs are current
- Confirm whether the roadmap effort estimate reflects actual scope
- Produce a readiness report and a go / no-go recommendation
- If not ready: surface the gaps to the Product Owner before the meeting is scheduled

This step prevents scope discovery from happening during the meeting.

### 5.2 Pre-Alignment Meeting Facilitation

During the pre-alignment meeting:

- Ensure all required roles are present
- Facilitate decision closure — every open question must be resolved before the meeting ends, or explicitly deferred with an owner assigned
- Capture decisions in the decisions record (authored by the Product Owner — the PMO Lead ensures it happens)
- Produce a post-meeting action status summary including critical path, blockers, and what is safe to start in parallel

### 5.3 Pre-Alignment Orchestration

After the meeting, using `processes/pre_alignment_run.md`:

- Track all actions by status (complete / in progress / blocked)
- Maintain and communicate the critical path
- Know what blocks what and when parallel work becomes safe
- Unblock actions by escalating missing inputs to the right owner
- Do not begin the QA review gate until all spec actions are confirmed complete and committed
- Do not begin the scope document until QA sign-off is confirmed

### 5.4 Phase Gate Communication

At every phase gate, and at every significant status change within a phase:

- Update the Phase Gate Document (`processes/templates/phase_gate_template.md`) immediately
- Proactively communicate to all relevant stakeholders: what just closed, who acts next, what they do, and by when
- Do not wait to be asked — if a stakeholder is asking what happens next, the PMO Lead has already failed this standard

### 5.5 Scope Document Coordination

When QA sign-off is confirmed:

- Coordinate the Product Owner to produce the scope document using `processes/feature_scope_document.md`
- Confirm the scope document is committed to `docs/product/scope/` with a compliant Class 4 header
- Confirm the roadmap entry for the feature is updated to reflect locked spec references
- Declare implementation open
- Notify QA Lead that test scenarios should be authored now — reference `processes/testing_guide.md`

### 5.6 Lessons Learnt

At the end of every pre-alignment phase:

- Run the lessons learnt review using `processes/lessons_learnt.md`
- Identify what was discovered late, where friction occurred, and what process improvements are needed
- Identify new skills or templates needed
- File the lessons learnt record as a Class 7 Delivery Record
- Raise any process improvement actions to the Product Owner

### 5.7 PMO Process Template Ownership

- Own and maintain the process templates listed in Section 8
- Update templates when lessons learnt produce process improvements
- Version templates when the process meaning changes (minor increment for additive changes, major for breaking changes)
- Ensure all templates carry correct Class 1 Canonical headers and change logs
- Ensure all templates remain consistent with the lifecycle guide

---

## 6. Explicit Non‑Responsibilities

The PMO Lead does **not**:

- Define product intent or priorities
- Author canonical specifications
- Approve or reject spec content
- Sign off on acceptance criteria
- Make scope decisions — those belong to the Product Owner
- Manage engineers day-to-day

---

## 7. Reporting & Interfaces

### Reports to
- Product Owner

### Governed by
- Head of Specs Team (documentation lifecycle and classification enforcement)

### Works closely with
- Product Owner (scope decisions, decisions record, scope document)
- Head of Specs Team (spec readiness, lifecycle compliance)
- All domain spec owners (action tracking, unblocking)
- QA & Testing Owner (QA gate coordination, test scenario timing)
- QA Lead (verification status, Phase 5 coordination)
- Head of Engineering (implementation handoff, defect resolution coordination)

---

## 8. Process Templates

The PMO Lead owns the following process templates. These are Class 1 Canonical documents — they define authoritative delivery process. Deviating from them without a change log entry is a process compliance failure.

| Template | Location | Purpose |
|----------|----------|---------|
| Pre-Alignment Readiness | `processes/pre_alignment_readiness.md` | Audit run before any pre-alignment meeting is scheduled |
| Pre-Alignment Run | `processes/pre_alignment_run.md` | Orchestration from meeting open to shipping closure |
| Feature Scope Document | `processes/feature_scope_document.md` | Template for producing a compliant scope document |
| Lessons Learnt | `processes/lessons_learnt.md` | Structured review run at the end of every pre-alignment phase |
| Testing Guide | `processes/testing_guide.md` | Who writes test scenarios, when, and in what format |
| Phase Gate Template | `processes/templates/phase_gate_template.md` | Per-feature delivery tracking document updated at every gate |

All templates are stored at `docs/team_skills/pmo/processess/` (process templates) and `docs/team_skills/pmo/processess/templates/` (per-feature fill-in templates).

---

## 9. Lifecycle & Versioning Compliance

All documentation owned by this role must follow the lifecycle states, header block, and versioning rules defined in:

- `docs/governance/document_lifecycle_guide.md`

This applies to:

**Class 1 Canonical — process templates:**
All templates listed in Section 8. Versioned when process meaning changes. Change log entry required for every version increment.

**Class 7 Delivery Records — per-feature artifacts:**
- Lessons learnt records (`docs/product/lessons_learnt/{id}-{slug}-lessons.md`) — filed as Class 7 at end of each delivery
- Phase gate documents (`docs/product/phase_gates/{id}-{slug}-phase-gate.md`) — Active during delivery, Filed at shipping closure

The PMO Lead is the named owner of all Class 7 Delivery Records it produces. Filed status is immutable — no amendments after filing.

**Class 5 Role Charter:**
- This document. Versioned when role scope changes.

---

## 10. Definition of Success

Someone doing this role well enables:

- Features that reach engineering with no open questions
- Spec owners who know exactly what they need to produce and when
- QA reviews that pass first time because specs were complete before review
- Scope documents that engineers can build from without clarification
- Stakeholders who always know the current phase, who acts next, and what they do
- Process improvements that compound across features

Pre-alignment becomes a **reliable, repeatable system** — not a heroic effort.

---

## Guiding Principle

> Features fail in pre-alignment for one of two reasons:
> something was discovered too late, or the wrong work happened in the wrong order.
>
> This role exists to prevent both.
