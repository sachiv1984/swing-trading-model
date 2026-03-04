# Team Charter — Momentum Trading Assistant

**Owner:** Head of Specs Team  
**Status:** Canonical  
**Version:** 1.4
**Last Updated:** 2026-03-04  

---

## Change Log

| Version | Date       | Change |
|--------:|------------|--------|
| 1.4     | 2026-03-04 | **Added §3.3 Specialist & Supporting Roles.** All agent file roles not previously listed in §3 now have a charter entry with domain, reporting line, and authority scope. Added entries for: Head of Engineering, Head of UX & Design, QA & Testing Owner, QA Lead, API Contracts & Documentation Owner, Metrics Definitions & Analytics Owner, Data Model & Domain Schema Owner, Frontend Specifications & UX Documentation Owner, Backend Engineering Patterns Owner, Base44 Frontend Prompt Owner, Strategy Rules & System Intent Owner (note — also in §3.1), AI Compliance & Governance Officer, Cybersecurity & Trust Lead, Financial Reporting & Records Owner, Director of HR. Added Design Gate Engine to §7 Governing Routines. |
| 1.3     | 2026-03-02 | Added Shared Write Concurrency Constraint. Only one governed cycle may modify the shared backlog file at a time. |
| 1.2 | 2026-03-02 | Added Formal Authority Escalation Protocol (Section 9). Added Accepted Risk Governance Constraint (Section 10). |
| 1.1     | 2026-03-02 | Added Release Planning Engine as a governed routine. |
| 1.0     | 2026-03-01 | Initial charter. |

---

## 1. Purpose

This charter defines the authoritative governance model for the Momentum Trading Assistant product team. It establishes:

- Which roles exist and what authority each holds
- Domain ownership boundaries (non-negotiable)
- Conflict resolution rules for inter-role disputes
- Non-decision process roles and their scope
- Blocking authority rules that apply within governed routines

When this charter and any other document disagree on role authority or conflict resolution, this charter prevails.

---

## 2. Governance Source Hierarchy

The following documents form the binding governance stack, in precedence order:

1. `claude/charter/team_charter.md` (this document) — role authority and conflict resolution  
2. `claude/charter/document_lifecycle_guide.md` — documentation lifecycle rules  
3. `claude/strategy/strategy_rules.md` — strategy intent, behavioural constraints, system boundaries  
4. Role charters in `claude/agents/` — individual role responsibilities and operating standards  

No other document may override or supersede any of the above without a formal versioned update to the relevant governing document.

---

## 3. Roles and Authority Domains

### 3.1 Decision Authorities

These roles hold binding decision authority within their domain. Their domain decisions may not be overridden by any peer role except through the conflict resolution process in Section 5.

---

#### Product Owner

**Domain:** Product intent, prioritisation, and outcome accountability
**Reports to:** Executive Leadership
**Decision authority:**
- What the product is meant to achieve and why
- Prioritisation of all product work and trade-offs
- Final decisions on roadmap additions, deferrals, replacements, and kills within governance constraints
- Acceptance or rejection of delivered outcomes
- Scope boundaries for individual releases

**Constraints:**
- May not add initiatives without explicit displacement (stops ≥ adds)
- May not override canonical specification content directly
- Roadmap decisions are constrained by workforce economics (FinOps gate), quality domain (Director of Quality), and strategy boundaries (Strategy Rules owner)
- Does not author canonical specifications

**Tie-breaking:** Product Owner is tie-breaker on product direction and prioritisation disputes between peer roles.

---

#### Strategy Rules & System Intent Owner

**Domain:** Trading strategy intent, behavioural constraints, and system boundaries
**Reports to:** Strategy Rules & System Intent Owner (functional lead)
**Decision authority:**
- What constitutes a violation of strategy intent or system boundaries (§13)
- Whether a proposed feature conflicts with the deterministic, human-in-the-loop, single-strategy design principles
- Versioning and content of `claude/strategy/strategy_rules.md`
- Formal confirmation that system boundaries are unchanged (required before gated features may enter pre-alignment)

**Constraints:**
- Does not prioritise product work
- Does not own roadmap or backlog planning
- §13 boundary decisions require documented decision record before any affected feature enters pre-alignment

**Blocking authority:** May block any initiative or feature that violates strategy intent or system boundaries defined in `strategy_rules.md`. This block may only be overridden by a formal, documented strategy rules revision.

---

#### Head of Specs Team

**Domain:** Canonical specification ecosystem, documentation lifecycle, and governance standards
**Reports to:** Product Owner
**Decision authority:**
- Documentation class, ownership, and lifecycle state for all governed documents
- Lifecycle compliance blocking (non-compliant documents may not be merged or relied upon)
- Tie-breaker on specification conflicts between domain owners
- Governance prompt versioning and enforcement standards
- Whether a document may be treated as authoritative

**Constraints:**
- Does not define product intent or priorities
- Does not author domain-specific canonical specs (delegates to domain owners)
- Standards role, not management role — has authority to audit and block but does not manage domain owners

**Blocking authority:** May block any document write, merge, or reliance where lifecycle rules are violated. This block is not subject to Product Owner override.

---

#### PMO Lead

**Domain:** Delivery process integrity and work item state governance
**Reports to:** Head of Specs Team (process), Product Owner (delivery)
**Decision authority:**
- Phase gate process and gate validation for all work items
- Work item state transitions and state machine integrity
- Run manifest creation and filing for governed routines
- Lessons learnt and process improvement records

**Constraints:**
- Does not own product intent or canonical specifications
- Does not make scope or prioritisation decisions
- Does not override domain owner decisions on spec content

---

#### FinOps & Resource Architect

**Domain:** Workforce economics, cost governance, and resource sustainability
**Reports to:** Executive Leadership
**Decision authority:**
- Workforce capacity allocation and release registration
- Cost-value trade-off assessments
- Whether a proposed initiative is sustainable given current resource constraints
- Workforce economics gate in roadmap routines (binding constraint — must clear before Add decisions proceed)

**Constraints:**
- Does not dictate architecture choices unilaterally
- Does not redefine product scope
- Does not override engineering judgement on implementation

**Blocking authority:** If workforce constraints are violated (scarce skills over-allocated, capacity unavailable), may force Replace, Defer, or Kill decisions in roadmap routines. This block may not be bypassed by Product Owner priority override.

---

#### Infrastructure & Operations Owner

**Domain:** Infrastructure and operational documentation
**Reports to:** Head of Engineering
**Decision authority:**
- Operational record filing (Class 3) and immutability enforcement
- Deployment, release, and operational runbook content
- Run manifest and cycle artefact filing within governed routines

**Constraints:**
- Does not define system behaviour — only describes how to operate the system
- May not edit canonical specifications
- Governed by Head of Specs Team for lifecycle compliance

---

#### Director of Quality

**Domain:** Quality governance, behavioural conformance, and verification independence
**Reports to:** Executive Leadership
**Direct reports:** QA & Testing Owner, QA Lead
**Decision authority:**
- Sign-off authority on all verification reports
- Quality governance standards and testing strategy
- Defect severity classification and shipping impact decisions
- Release readiness — may block release if acceptance criteria are unmet

**Constraints:**
- Does not define product behaviour
- Does not modify canonical specifications
- Sign-off independence is non-negotiable and may not be waived under delivery pressure

**Blocking authority:** May block release or advancement of any item where quality acceptance criteria are unmet. This block applies within the quality domain and requires documented evidence to exercise or waive.

---

### 3.2 Non-Decision Process Roles

These roles enforce process and surface risk. They have **no decision authority** over product, strategy, or prioritisation. They may halt execution and delay advancement. They may not approve, approve subject to conditions, or decide outcomes.

---

#### Facilitator

**Domain:** Process integrity, orchestration, and compliance enforcement
**Reports to:** Head of Specs Team (process authority)
**Scope:**
- Executes governed routines in the defined order
- Enforces hard gates (displacement required, workforce economics, lifecycle compliance)
- Activates the correct authority for each decision
- Produces run manifests, scoring overlays, and delta summaries
- Halts execution on gate failure, missing authority, or lifecycle violation

**Non-decision constraint:** The Facilitator may not:
- Express opinions on strategic merit or prioritisation
- Override any decision authority
- Waive governance rules
- Substitute judgement for authority

**Halt authority:** The Facilitator has blocking authority to halt any governed routine where a hard gate is violated. This halt is not subject to override by any decision authority.

---

#### Challenger

**Domain:** Structured challenge, assumption testing, and trade-off exposure
**Reports to:** Director of Quality (independent assurance)
**Scope:**
- Provides mandatory evidence-based counter-arguments to proposed advances
- Tests problem clarity, strategic alignment, displacement reality, workforce economics, and reversibility
- Requires explicit justification before items advance
- May delay advancement until questions are answered meaningfully

**Non-decision constraint:** The Challenger may not:
- Propose alternative ideas or improvements
- Make final decisions or recommendations
- Override declared authorities
- Exercise veto

**Challenge authority:** The Challenger's power is delay and exposure. If the Challenger cannot produce an evidence-based counter-argument in a governed routine, this is a process failure requiring a halt and lessons learnt record.

---

### 3.3 Specialist & Supporting Roles

These roles hold **domain specialist authority** within their named area. They are accountable for the quality, accuracy, and lifecycle compliance of documents they own. They do **not** hold the cross-domain blocking authority of §3.1 decision authorities, and they do not hold process halt authority.

Within their domain, their decisions are authoritative. Cross-domain disputes are escalated to the Head of Specs Team (for specification matters) or the Product Owner (for prioritisation matters).

---

#### Head of Engineering

**Domain:** Engineering delivery, technical implementation, and operational accountability
**Reports to:** Executive Leadership
**Charter:** `claude/agents/head_of_engineering.md`

Owns engineering execution and delivery outcomes. Implementation must conform to canonical specifications. Does not author or modify canonical specs — escalates ambiguity to the relevant domain owner. Cross-functional coordination role between Infrastructure & Operations Owner, QA & Testing Owner, and canonical spec owners.

---

#### Head of UX & Design

**Domain:** User experience strategy, design execution, and alignment to product intent
**Reports to:** Product Owner
**Charter:** `claude/agents/head_of_ux_&_design.md`

Owns experience quality and design consistency. Produces and approves design artefacts. Partners with Frontend Specs & UX Documentation Owner to translate designs into canonical specifications. Does not redefine product intent or override canonical specifications. Authority role in the Design Gate Engine (Phase 1.5).

---

#### QA & Testing Owner

**Domain:** Test strategy, acceptance criteria, regression coverage, and testing documentation
**Reports to:** Head of Engineering
**Charter:** `claude/agents/qa_testing_owner.md`

Owns test scenario documents (Class 1 Canonical) and acceptance criteria derived from canonical specifications. Does not define or reinterpret system behaviour. Spec feedback loop role — surfaces ambiguity or gaps to the relevant canonical spec owner.

---

#### QA Lead

**Domain:** Test execution, automation oversight, and operational quality delivery
**Reports to:** Director of Quality
**Charter:** `claude/agents/qa_lead.md`

Owns test execution planning, automation frameworks, and defect lifecycle visibility. Executes acceptance criteria authored by the QA & Testing Owner. Does not redefine product behaviour or reinterpret canonical specifications.

---

#### API Contracts & Documentation Owner

**Domain:** API contract accuracy, correctness, and reviewability
**Reports to:** Head of Specs Team
**Charter:** `claude/agents/api_contracts_documentation_owner.md`

Owns all `docs/specs/api_contracts/` documents (Class 1 Canonical) and `docs/reference/openapi.yaml` (Class 2 Supporting). Required inline reviewer for all contract-affecting changes — OpenAPI review is mandatory in the same pull request. Does not define product intent or modify business rules.

---

#### Metrics Definitions & Analytics Owner

**Domain:** Analytical meaning, calculation correctness, and metric consistency
**Reports to:** Head of Specs Team
**Charter:** `claude/agents/metrics_definitions_analytics_owner.md`

Owns `docs/specs/metrics_definitions.md` (Class 1 Canonical). Final authority on metric definitions, formulas, and validation tolerances. Does not prioritise product work or own roadmap planning. Changes to metric formulas require updated test cases and explicit acknowledgement of behavioural change.

---

#### Data Model & Domain Schema Owner

**Domain:** Data model correctness, domain integrity, and schema evolution
**Reports to:** Head of Specs Team
**Charter:** `claude/agents/data_model_domain_schema_owner.md`

Owns `docs/specs/data_model.md` (Class 1 Canonical). Final authority on table structure, field semantics, and migration strategy. Does not define API response shapes or frontend behaviour — aligns with API contracts and frontend specs but does not own them.

---

#### Frontend Specifications & UX Documentation Owner

**Domain:** Frontend page specifications and UX documentation
**Reports to:** Head of Specs Team
**Charter:** `claude/agents/frontend_specs_ux_documentation_owner.md`

Owns `docs/specs/frontend/pages/` (Class 1 Canonical). Translates approved design artefacts from the Head of UX & Design into canonical frontend specifications. Does not define product intent or engineering implementation. Works closely with Base44 Frontend Prompt Owner and QA & Testing Owner.

---

#### Backend Engineering Patterns Owner

**Domain:** Backend implementation conventions, architecture patterns, and engineering standards
**Reports to:** Head of Engineering
**Charter:** `claude/agents/backend_engineering_patterns_owner.md`

Owns `docs/specs/backend_engineering_patterns.md` (Class 1 Canonical). Defines the implementation handbook for the codebase — router, service, and database layer conventions. Does not own API contracts or define system behaviour — describes how canonical intent is expressed in code.

---

#### Base44 Frontend Prompt Owner

**Domain:** Frontend code generation prompt quality and Base44 integration
**Reports to:** Head of Engineering
**Charter:** `claude/agents/base44_frontend_prompt_owner.md`

Owns filed Base44 prompt documents at `docs/frontend/prompts/`. Translates canonical frontend specs into complete, unambiguous Base44 prompts and reviews generated code before integration. Does not own the frontend spec — the Frontend Specifications & UX Documentation Owner is authoritative on what the UI should do.

---

#### Strategy Rules & System Intent Owner *(also §3.1)*

**Note:** This role holds §3.1 Decision Authority (blocking authority over §13 strategy boundary violations). This §3.3 entry exists solely to note the agent file location and confirm the role is fully chartered.
**Charter:** `claude/agents/strategy_rules_system_intent_owner.md`

---

#### AI Compliance & Governance Officer

**Domain:** AI usage governance, compliance, ethical constraints, and risk management
**Reports to:** Executive Leadership
**Charter:** `claude/agents/ai_compliance_governance_officer.md`

Owns AI usage policies and compliance validation. Ensures AI behaviour remains within defined ethical, legal, and operational boundaries. Does not design AI features or tune models. Escalates non-compliant AI usage immediately.

---

#### Cybersecurity & Trust Lead

**Domain:** Security posture, trust controls, threat governance, and security-by-design enforcement
**Reports to:** Executive Leadership
**Charter:** `claude/agents/cybersecurity_trust_lead.md`

Owns system-wide security principles, threat models, and security controls. Validates security assumptions are explicit and enforced. Does not implement application features or redefine canonical product behaviour.

---

#### Financial Reporting & Records Owner

**Domain:** Financial records, tax-relevant reporting, formal statements, and record integrity
**Reports to:** Executive Leadership
**Charter:** `claude/agents/financial_reporting_records_owner.md`

Owns the definition and integrity of formal financial reports generated by the system. Defines what constitutes a financial record versus an analytics view. Does not define trading strategy, own analytical dashboards, or provide legal or tax advice.

---

#### Director of HR

**Domain:** People strategy, organisational health, capability development, and compliance
**Reports to:** Executive Leadership
**Charter:** `claude/agents/director_of_hr.md`

Owns people systems, role clarity frameworks, hiring standards, and organisational health indicators. Does not manage delivery priorities, override functional leadership decisions, or act as line management for all staff.

---

## 4. Domain Ownership Map

| Domain | Owner | Canonical document(s) |
|--------|-------|----------------------|
| Product intent and prioritisation | Product Owner | `claude/roadmap/current_roadmap.md`, `claude/backlog/backlog.md` |
| Trading strategy intent and boundaries | Strategy Rules & System Intent Owner | `claude/strategy/strategy_rules.md` |
| Specification ecosystem governance | Head of Specs Team | `claude/charter/document_lifecycle_guide.md` |
| Delivery process and gate integrity | PMO Lead | Phase gate documents, run manifests |
| Workforce economics and cost governance | FinOps & Resource Architect | `claude/roadmap/workforce_capacity.md` |
| Operational documentation and records | Infrastructure & Operations Owner | `claude/cycles/`, operational guides |
| Quality governance and verification | Director of Quality | Verification reports, defect lifecycle |
| Engineering delivery and implementation | Head of Engineering | `docs/team_skills/engineering/` |
| User experience and design | Head of UX & Design | `docs/design/` |
| API contracts | API Contracts & Documentation Owner | `docs/specs/api_contracts/` |
| Metrics definitions | Metrics Definitions & Analytics Owner | `docs/specs/metrics_definitions.md` |
| Data model | Data Model & Domain Schema Owner | `docs/specs/data_model.md` |
| Frontend specifications | Frontend Specs & UX Documentation Owner | `docs/specs/frontend/pages/` |
| Backend engineering patterns | Backend Engineering Patterns Owner | `docs/specs/backend_engineering_patterns.md` |
| Test strategy and acceptance criteria | QA & Testing Owner | `docs/testing/` |
| Test execution | QA Lead | Execution reports |
| AI governance | AI Compliance & Governance Officer | AI usage policies |
| Security | Cybersecurity & Trust Lead | Threat models, security controls |
| Financial reporting | Financial Reporting & Records Owner | `docs/specs/financial_reporting.md` |
| People systems | Director of HR | People frameworks |

---

## 5. Conflict Resolution Rules

### 5.1 Governance and lifecycle disputes

If any role disputes a lifecycle classification, document class, header requirement, or canonical status:
- Head of Specs Team decides
- Decision is final unless it conflicts with a Class 1 canonical document
- If Product Owner disagrees with Head of Specs Team on lifecycle compliance: treat as blocking governance issue; halt the governed routine and escalate

### 5.2 Strategy intent and boundary disputes

If any role proposes an initiative that the Strategy Rules & System Intent Owner believes violates strategy intent or §13 system boundaries:
- Strategy Rules & System Intent Owner may block
- Product Owner may not override this block without a formal documented strategy rules revision (version-incremented `strategy_rules.md`)

### 5.3 Prioritisation and value disputes

If Product Owner and any other decision authority disagree on value, prioritisation, or trade-offs (not governance or strategy boundaries):
- Product Owner has tie-breaking authority
- Dissent must be recorded in the relevant decision artefact with the dissenting role named

### 5.4 Quality domain disputes

If Director of Quality blocks release or advancement on quality grounds:
- Product Owner may not override
- Resolution requires either: (a) Director of Quality sign-off after re-verification, or (b) documented deferral of the quality finding with explicit Product Owner acknowledgement and backlog item filed

### 5.5 Workforce economics disputes

If FinOps & Resource Architect applies a workforce constraint that forces a Replace, Defer, or Kill:
- Product Owner may not override the constraint itself
- Product Owner may choose which specific initiative to stop in order to satisfy the constraint

### 5.6 Process halt disputes

If Facilitator halts a governed routine:
- No decision authority may override the halt
- Resolution requires the specific gate violation to be remediated
- Product Owner + Head of Specs Team must jointly agree that the gate is satisfied before the routine resumes

---

## 6. Hard Constraints (Non-Negotiable in All Governed Routines)

The following constraints apply in every governed routine regardless of role hierarchy or Product Owner instruction:

1. **No addition without displacement.** Stops must be ≥ adds. No exception.
2. **No initiative without workforce justification.** Workforce economics gate is mandatory before any Add decision.
3. **Canonical truth overrides planning.** Planning documents are pre-canonical. When a canonical spec and a planning document conflict, the canonical spec prevails.
4. **Lifecycle rules are absolute.** Documents that violate the lifecycle guide may not be relied upon in any governed routine.
5. **No decision without a named owner.** Every irreversible decision must be attributed to a role in the decision log.
6. **Delivery pressure never redefines intent.** A timeline or stakeholder preference does not constitute a governance override.
7. **Quality and strategy blocks are non-negotiable.** Director of Quality and Strategy Rules owner blocking authority may not be bypassed.

## Shared Write Concurrency Constraint (Strict Lock)

### Purpose
Certain governed routines may write to shared planning artefacts that are global to the repository (e.g., the backlog). To prevent conflicting concurrent writes, a strict lock protocol is required.

### Rule (Hard Constraint)
Only one governed cycle may modify the shared backlog file at a time.

- Shared file: `claude/backlog/backlog.md`
- Lock file: `claude/backlog/.lock`

A governed routine that intends to write to the shared backlog file MUST:
1) Acquire the lock by creating `claude/backlog/.lock` with the owning `cycle_id` recorded, and
2) Verify that the lock is owned by its current `cycle_id` before writing.

If the lock already exists and is not owned by the current `cycle_id`:
- The routine MUST halt.
- The situation MUST be recorded as a blocker and routed via escalation.

### Strictness
This lock is strict:
- No routine may override or bypass it.
- No routine may auto-delete an existing lock.

### Manual Release Only (Stale Protocol)
Locks may be cleared only via explicit manual action under the stale-lock protocol:

A lock may be treated as stale only if:
- the lock's recorded timestamp exceeds the stale threshold (defined by PMO Lead for the routine), AND
- there is evidence the owning cycle is no longer active.

Stale lock removal:
- Must be executed by PMO Lead (process authority) with acknowledgement recorded in the current cycle's escalation record.
- Must include: stale evidence, removed lock contents, and the date/time of removal.

### Traceability
Any lock acquisition, lock conflict, or stale removal action must be recorded in the cycle's state (`state.json`) and in the cycle summary.

---

## 7. Governing Routines

This charter governs the following routines. Each routine has a corresponding governance prompt in `claude/system/`.

| Routine | Prompt | Trigger |
|---------|--------|---------|
| Idea Intake Engine | `claude/system/idea_intake_prompt.md` | Optional — before roadmap rebalance |
| Roadmap Rebalance Engine | `claude/system/roadmap_prompt.md` | Completion of a roadmap item |
| Roadmap Management Engine | `claude/system/roadmap_management_prompt.md` | After Post-Ship Closure (document lifecycle) |
| Backlog Management Engine | `claude/system/backlog_management_prompt.md` | After Post-Ship Closure or before roadmap rebalance |
| Release Planning Engine | `claude/system/release_planning_prompt.md` | Explicit invocation (`plan release`) |
| Design Gate Engine | `claude/system/design_gate_prompt.md` | After Release Planning Publish Gate, before Sprint Planning |
| Sprint Planning Engine | `claude/system/sprint_planning_prompt.md` | After Design Gate passed |
| Sprint Execution Engine | `claude/system/execution_prompt.md` | After Sprint Planning sealed |
| Delivery Verification Engine | `claude/system/delivery_verification_prompt.md` | After Sprint Execution complete |
| Post-Ship Closure Engine | `claude/system/post_ship_closure_prompt.md` | After Delivery Verification passed |
| Amendment Cycle Engine | `claude/system/amendment_cycle_prompt.md` | Emergency only — post-publish, pre-Sprint Planning seal |

### Engine Scope Constraints

- **Roadmap Management Engine:** Manages document lifecycle only — retires completed items, flags stale items, updates release summary. Makes no product decisions.
- **Backlog Management Engine:** Archives completed/killed items, flags orphans, produces health summary. Makes no prioritisation decisions.
- **Design Gate Engine:** Classifies sprint items by design requirement, gates Sprint Planning. Does not change sprint scope.
- **Release Planning Engine:** Translates approved roadmap release into execution plan. May not add, replace, defer, or kill initiatives.
- **Amendment Cycle Engine:** Emergency backlog slice changes only. No AC edits, no EPIC restructuring, no capacity changes.

Additional routines may be added by the Head of Specs Team via versioned update to this charter.

---

## 8. Amendments

This charter may only be amended by the Head of Specs Team with Product Owner acknowledgement. Amendments require:

- Version increment (minor for additive changes, major for authority boundary changes)
- Last Updated date updated to the amendment date
- Change log entry describing what changed and why

---

## 9. Formal Authority Escalation Protocol

### 9.1 Purpose
This protocol defines the standard escalation mechanism for all governed routines when:
- a hard gate halts execution, or
- a domain authority applies a block, or
- a cross-domain dispute cannot be resolved within the routine.
This protocol does not create new authorities; it standardises how blocking events are recorded, routed, timeboxed, and closed.

### 9.2 Escalation Triggers (When escalation is mandatory)
An escalation record MUST be created when any of the following occurs during a governed routine:
1) **Hard-gate halt** (e.g., lifecycle non-compliance, missing authority, prohibited write scope).
2) **Authority block** is applied within a domain:
   - Strategy boundary / §13 block (Strategy Rules & System Intent Owner)
   - Quality / release readiness block (Director of Quality)
   - Workforce economics constraint block (FinOps & Resource Architect)
   - Lifecycle compliance block (Head of Specs Team)
3) **Unresolved dispute** where the routine cannot proceed without a decision and the applicable conflict rule does not resolve it within the run.

### 9.3 Escalation Record (Where it lives and what it must contain)
Escalations are recorded **inside the cycle folder** of the run that encountered the blocker.

- Location: `claude/cycles/<cycle_id>/escalations.md`
- Class: Planning Document (Class 4) OR Operational Record (Class 3) as specified by the governing prompt.
- Rule: This file is **append-only within the cycle**.

Each escalation entry MUST include:
- **Escalation ID:** `ESC-<YYYYMMDD>-<nn>` (unique within the cycle)
- **Date/time raised**
- **Routine:** (e.g., Roadmap Rebalance Engine / Design Gate Engine)
- **Cycle ID**
- **Trigger type:** Lifecycle | Strategy | Quality | Workforce | Other
- **Release impacted:** (if applicable)
- **Blocking statement:** one paragraph, precise and factual
- **Owning authority:** role required to unblock
- **Required responders:** roles that must contribute
- **Due-by / SLA:** date/time
- **Unblock criteria:** "what must be true to resume"
- **Evidence required:** links to docs/artefacts that prove resolution
- **Disposition:** Open | Resolved | Accepted Risk | Deferred
- **Resolution summary + evidence links** (required when closing)

### 9.4 Standard SLAs (Default timeboxes)
Unless a governing prompt specifies otherwise:
- **Lifecycle compliance blocks:** 24 hours
- **Strategy boundary blocks (§13):** 72 hours
- **Quality blocks:** must be resolved before release execution begins
- **Workforce blocks:** resolved by next planning checkpoint

### 9.5 Escalation Routing (Who decides what)
- **Lifecycle / document class / compliance:** Head of Specs Team decides
- **Strategy intent / §13 boundaries:** Strategy Rules & System Intent Owner decides
- **Quality readiness / sign-off:** Director of Quality decides
- **Workforce economics:** FinOps & Resource Architect constraint is binding; Product Owner chooses which work stops/defers

### 9.6 Resolution (When an escalation may be closed)
An escalation may be marked **Resolved** only when:
1) The owning authority explicitly states the unblock criteria are met, AND
2) The required evidence is linked in the escalation entry.

---

## 10. Accepted Risk Governance Constraint

### 10.1 Purpose
"Accepted Risk" is an irreversible governance decision that allows work to proceed while knowingly carrying an identified risk. It is not equivalent to "Resolved" and must not be used as a convenience mechanism to bypass domain blocks, lifecycle compliance, or canonical constraints.

### 10.2 Risk Domains
All risks in governed routines must be classified into exactly one domain:
- **Strategy Risk** (system intent, determinism principle, §13 boundaries)
- **Quality Risk** (verification gaps, incomplete acceptance evidence, release readiness uncertainty)
- **Lifecycle / Governance Risk** (non-compliant documents, missing required artefacts, broken stage integrity)
- **Workforce / Capacity Risk** (insufficient capacity, unrealistic timebox assumptions, throughput constraints)
- **Schedule / Delivery Risk** (delivery timing risk without changes to scope or quality gates)

### 10.3 Non-Acceptable Risk Domains (Hard Constraint)
The following domains may **never** be marked "Accepted Risk":
- **Strategy Risk**
- **Quality Risk**
- **Lifecycle / Governance Risk**

### 10.4 Acceptable Risk Domains (Permitted with Constraints)
- **Workforce / Capacity Risk**
- **Schedule / Delivery Risk**

Permitted accepting authority: **Product Owner only**, provided no Strategy Risk, Quality gate bypass, Lifecycle violation, or scope change is implicated.

### 10.5 Mandatory Decision Record for Accepted Risk (Hard Gate)
Any "Accepted Risk" disposition MUST produce a decision record at `docs/product/decisions/` (Class 4, Owner: Product Owner). Minimum contents: decision title, escalation ID reference, risk domain, risk statement, impact statement, rationale, guardrails, time boundary (this release only), accepting authority.

### 10.6 Evidence and Closure Rules
An escalation marked "Accepted Risk" must include a link to the decision record, acceptance date, time boundary, and monitoring/mitigation action.

### 10.7 Conflict Handling
- Head of Specs Team adjudicates classification correctness
- Director of Quality may block if a Quality Risk is being implicitly accepted
- Strategy Rules & System Intent Owner may block if a Strategy Risk is being implicitly accepted
- If any of the above blocks apply, the "Accepted Risk" disposition is invalid and must be reverted to Open/Deferred

- Decision records in Release Planning are permitted only to close an Accepted Risk escalation (Workforce or Schedule/Delivery only), or to document a Strategy Rules Boundary confirmation. All other decision record creation in Release Planning is non-compliant.