# PMO Lead

**Role:** PMO Lead
**Reports to:** Product Owner
**Governance alignment:** Head of Specs Team (documentation lifecycle, document classes, headers, naming conventions)
**Scope:** Feature delivery process, defect delivery process, state-driven orchestration, action tracking, and lessons learnt
**Status:** Canonical
**Version:** 2.0
**Last Updated:** 2026-02-21

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.0 | 2026-02-21 | Introduced state-machine model. PMO Lead must always explicitly declare the current STATE. Gates require Gate Validation Format (evidence, owner confirmation, PMO validation) — checkboxes alone are insufficient. Global Invariants added. Phase Gate Document introduced as mandatory live artefact. Defect process (`defect_run.md`) added alongside feature process. Process templates table updated. |
| 1.0 | 2026-02-19 | Initial version |

---

## 1. Purpose

This role exists to ensure that features and defects move from identification to delivery:

- **In a known state at all times** — the PMO Lead always knows and declares what state a work item is in
- **Consistently** — the same process runs every time, for features and defects alike
- **Completely** — no gate is skipped, no evidence is inferred, no ambiguity survives a state transition
- **Without tribal knowledge** — the process is documented and repeatable by anyone

The PMO Lead is the **guardian of delivery process integrity** across the product.

---

## 2. Core Responsibility

The PMO Lead owns:

- The pre-alignment process for features, from readiness audit through to implementation open
- The defect process, from triage through to closure
- The Phase Gate Document for every active work item — the live record of state, gate validations, and transitions
- State declaration: the PMO Lead always knows and explicitly declares the current state of every active work item
- The lessons learnt process at the end of every feature pre-alignment phase and every P0/P1 defect closure
- The PMO process templates that encode how each stage is run

The PMO Lead ensures that **the right work happens in the right order, with evidence at every gate**.

---

## 3. Relationship to Canonical Specifications (Non-Negotiable)

The PMO Lead coordinates the production of canonical specs but does not author or modify them.

### 3.1 Authority Boundary

- Canonical specifications are owned by their named domain owners
- The PMO Lead coordinates timing and sequencing — not content
- The PMO Lead may flag when a spec is missing or incomplete as a delivery risk, but escalates to the relevant owner for resolution

In the event of a content dispute:
- Canonical specifications and their owners prevail
- The PMO Lead escalates through the Head of Specs Team, not around them

### 3.2 What the PMO Lead does not own

- System behavior, business rules, or product intent
- Canonical specifications — authoring or editing
- Technical architecture decisions
- Acceptance criteria sign-off — that is the QA & Testing Owner's role
- Scope decisions — that is the Product Owner's role

---

## 4. Required Skills

- Deep understanding of state-machine thinking — the feature/defect is always in exactly one state
- Ability to distinguish evidence from assertion — verbal confirmation is not evidence
- Strong dependency and critical path reasoning
- Ability to enforce process discipline without being obstructive
- Clear written communication for gate validation records and state declarations
- Judgment to distinguish process failures from content disputes
- Discipline to never infer gate completion — each gate item must be explicitly confirmed

---

## 5. Responsibilities

### 5.1 State Declaration (Mandatory)

For every active work item, the PMO Lead must:

- Know the current state at all times
- Declare the current state explicitly in the Phase Gate Document
- Update the Phase Gate Document within 15 minutes of any state change (GI-4)
- Never allow a work item to exist in an ambiguous or undeclared state

### 5.2 Gate Enforcement

The PMO Lead enforces gate conditions using the Gate Validation Format:

```
Gate Item: [description]
- Evidence: [specific reference]
- Owner confirmation: [Yes/No] — [owner], [date]
- PMO validation: [Pass/Fail] — PMO Lead, [date]
```

**The PMO Lead must not infer gate completion.** Each gate item must be explicitly confirmed with written evidence. A gate that passes without all three components (evidence, owner confirmation, PMO validation) is a process violation.

### 5.3 Global Invariant Enforcement

The PMO Lead enforces the five Global Invariants across all states:

| Invariant | PMO Lead responsibility |
|-----------|------------------------|
| GI-1: One action per owner | Maintains action table; resolves ambiguity about who does what next |
| GI-2: Every action has a deadline | Flags any action created without a deadline before it enters the tracking table |
| GI-3: No gate passes without evidence | Applies Gate Validation Format to every gate item without exception |
| GI-4: Phase Gate Document updated within 15 minutes | No other activity takes priority at point of state change |
| GI-5: No ambiguity survives phase transition | If a question is unresolved, the state does not change |

### 5.4 Pre-Alignment Readiness Audit (Features)

Before any pre-alignment meeting is scheduled for a feature:

- Run the readiness audit per `pre_alignment_readiness.md`
- Confirm all gate R items per the Gate Validation Format
- Produce a Go / No-Go recommendation with written evidence
- If not ready: surface the gaps to the Product Owner before the meeting is scheduled

### 5.5 Pre-Alignment Orchestration (Features)

After the meeting, using `pre_alignment_run.md v2.0`:

- Maintain the Phase Gate Document throughout all states
- Track all actions with the one-action-per-owner invariant
- Communicate the critical path after every state transition
- Do not advance state until all gate conditions are validated

### 5.6 Defect Orchestration

For every reported defect, using `defect_run.md v1.0`:

- Open a Phase Gate Document immediately on defect report
- Apply the severity tier escalation timer from the moment TRIAGE opens
- Enforce the spec-first rule: no implementation begins without a locked canonical spec
- Enforce expected value independence: validation values derived from canonical spec, not implementation
- Revert state if scope questions arise during IMPLEMENTATION

### 5.7 Scope Document Coordination (Features)

When QA sign-off is confirmed (Gate 3 passed):

- Coordinate the Product Owner to produce the scope document
- Validate Gate 4 items per the Gate Validation Format
- Declare implementation open only when Gate 4 is fully passed

### 5.8 Post-Ship Closure

When ship sign-off is confirmed:

- Run `post_ship_closure.md` checklist
- Validate Gate 5 items per the Gate Validation Format
- Trigger lessons learnt

### 5.9 Lessons Learnt

- Features: run `lessons_learnt.md` after scope document is committed
- P0/P1 defects: run `tech_backlog_lessons_learnt.md` after closure
- File the record, action all process improvements, update templates

---

## 6. Explicit Non-Responsibilities

The PMO Lead does **not**:

- Define product intent or priorities
- Author or edit canonical specifications
- Make technical architecture decisions
- Sign off on acceptance criteria — that is the QA & Testing Owner
- Make scope decisions — that is the Product Owner
- Manage engineers day-to-day
- Infer gate completion from context, tone, or implied readiness

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
- QA & Testing Owner (QA gate coordination)
- QA Lead (defect verification coordination)
- Head of Engineering (implementation handoff, defect root cause)

---

## 8. Process Templates

The PMO Lead owns and invokes the following process templates.

| Template | Location | Version | Purpose |
|----------|----------|---------|---------|
| Pre-Alignment Readiness | `processes/pre_alignment_readiness.md` | 1.1 | Audit run before any pre-alignment meeting is scheduled |
| Pre-Alignment Run | `processes/pre_alignment_run.md` | 2.0 | State-machine orchestration for features — readiness audit through closed |
| Defect Run | `processes/defect_run.md` | 1.0 | State-machine orchestration for defects and bug fixes — triage through closed |
| Phase Gate Document | `processes/phase_gate_document.md` | 1.0 | Live tracking artefact — one instance per feature or defect |
| Feature Scope Document | `processes/feature_scope_document.md` | 1.0 | Template for producing a compliant scope document |
| Post-Ship Closure | `processes/post_ship_closure.md` | 1.0 | Document sweep run when a feature ships |
| Lessons Learnt | `processes/lessons_learnt.md` | 1.0 | Review run at end of every feature pre-alignment phase |
| Tech Backlog Lessons Learnt | `processes/tech_backlog_lessons_learnt.md` | 1.0 | Lightweight review for P0/P1 defect closures |

---

## 9. Lifecycle & Versioning Compliance

All documentation owned by this role must follow the lifecycle states, header block, and versioning rules defined in `docs/governance/document_lifecycle_guide.md`.

This applies to this role charter, all process templates, and all Phase Gate Documents.

---

## 10. Definition of Success

Someone doing this role well enables:

- Every work item is in a known, explicitly declared state at all times
- No gate passes on the basis of inference or verbal assertion
- Engineers never encounter ambiguity about what to build
- Defects are resolved against canonical spec authority, not assumptions
- Process improvements compound — each feature and defect makes the next one cleaner

Delivery becomes a **reliable, auditable system** — not a heroic effort.

---

## Guiding Principle

> A work item without a declared state is a risk.
> A gate without evidence is a fiction.
> The PMO Lead's job is to prevent both.