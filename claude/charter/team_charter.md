# Team Charter — Momentum Trading Assistant

**Owner:** Head of Specs Team  
**Status:** Canonical  
**Version:** 1.1  
**Last Updated:** 2026-03-02  

---

## Change Log

| Version | Date       | Change |
|--------:|------------|--------|
| 1.1     | 2026-03-02 | Added Release Planning Engine as a governed routine. No changes to role authority, conflict rules, or constraints. |
| 1.0     | 2026-03-01 | Initial charter. Establishes role authority model, domain ownership boundaries, conflict resolution rules, and non-decision role definitions for all governed routines. |

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

---

## 7. Governing Routines

This charter governs the following routines. Each routine has a corresponding governance prompt in `claude/system/`.

| Routine                  | Prompt                                   | Trigger |
|--------------------------|-------------------------------------------|---------|
| Roadmap Rebalance Engine | `claude/system/roadmap_prompt.md`         | Completion of a roadmap item |
| Release Planning Engine  | `claude/system/release_planning_prompt.md`| Explicit user invocation (e.g., `plan release --version "v1.7"`) |

### Release Planning Engine — Scope Clarification

- **Purpose:** Translate an already-approved roadmap release into an execution-ready plan.
- **Constraints:**
  - May not add, replace, defer, or kill initiatives.
  - May not alter strategy intent or §13 boundaries.
  - May not bypass lifecycle, quality, or workforce gates.
- **Outputs:** Planning and operational artefacts only (e.g., release plan, sequencing, acceptance gates, cycle records).

Additional routines may be added by the Head of Specs Team via versioned update to this charter.

---

## 8. Amendments

This charter may only be amended by the Head of Specs Team with Product Owner acknowledgement. Amendments require:

- Version increment (minor for additive changes, major for authority boundary changes)
- Last Updated date updated to the amendment date
- Change log entry describing what changed and why
