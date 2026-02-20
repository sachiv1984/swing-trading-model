# Process Index

**Owner:** Head of Specs Team
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.0 | Initial version. Created following 3.2 delivery gap assessment — the Specs Index maps canonical product specs but there was no equivalent navigation point for delivery process and governance documents. A new team member could not find "where is the delivery process defined?" through any existing index. |

---

## Purpose

This index maps where authoritative **process and governance documents** live. It is the process equivalent of the Specs Index — if the Specs Index answers "where is this *behaviour* defined?", this index answers "where is this *process* defined?".

It does not restate rules. It points to the canonical source.

---

## How to Use

If you are asking:
- "How does a feature move from roadmap to implementation?"
- "Who writes test scenarios and when?"
- "What happens when I find a defect?"
- "How do I raise a spec question during implementation?"
- "What document class does this belong to?"
- "Who owns this process?"

Start here.

---

## 1. Feature Delivery Process

### Pre-Alignment

| Question | Document | Owner |
|----------|----------|-------|
| Is this feature ready to enter pre-alignment? | `docs/team_skills/pmo/processess/pre_alignment_readiness.md` | PMO Lead |
| How does the pre-alignment process run, phase by phase? | `docs/team_skills/pmo/processess/pre_alignment_run.md` | PMO Lead |
| What does a scope document contain and how is it structured? | `docs/team_skills/pmo/processess/feature_scope_document.md` | PMO Lead |
| Where do I track current phase, next actions, and blockers for a feature? | `docs/team_skills/pmo/processess/templates/phase_gate_template.md` | PMO Lead |

### Testing and Verification

| Question | Document | Owner |
|----------|----------|-------|
| Who writes test scenarios, when, and in what format? | `docs/team_skills/pmo/processess/testing_guide.md` | QA & Testing Owner (executes); PMO Lead (owns template) |
| How are defects raised, assigned, resolved, and closed? | `docs/team_skills/quality/defect_lifecycle.md` | Director of Quality |
| What does the Director of Quality review before signing off? | `docs/team_skills/quality/defect_lifecycle.md §6` | Director of Quality |
| How does an observation become a backlog item? | `docs/team_skills/quality/defect_lifecycle.md §8` | QA Lead (raises); Product Owner (prioritises) |

### Shipping Closure and Lessons Learnt

| Question | Document | Owner |
|----------|----------|-------|
| What does the PMO Lead do at shipping closure? | `docs/team_skills/pmo/processess/pre_alignment_run.md §Phase 5` | PMO Lead |
| How is a lessons learnt review run? | `docs/team_skills/pmo/processess/lessons_learnt.md` | PMO Lead |

---

## 2. Spec Query and Escalation

| Question | Document | Owner |
|----------|----------|-------|
| How do I raise a spec question during implementation? | `docs/team_skills/specs/spec_query_process.md` | Head of Specs Team |
| What happens when a defect spans two canonical domains? | `docs/team_skills/quality/defect_lifecycle.md §7` | Director of Quality (escalation); Head of Specs Team (mediation) |
| How does the Head of Engineering handle an implementation intake? | `docs/team_skills/engineering/implementation_intake.md` | Head of Engineering |

---

## 3. Document Governance

| Question | Document | Owner |
|----------|----------|-------|
| What document class does this document belong to? | `docs/governance/document_lifecycle_guide.md` | Head of Specs Team |
| What header fields are required for this document class? | `docs/governance/document_lifecycle_guide.md §2` | Head of Specs Team |
| What lifecycle states are available? | `docs/governance/document_lifecycle_guide.md §3` | Head of Specs Team |
| When do I need to increment a version? | `docs/governance/document_lifecycle_guide.md §5` | Head of Specs Team |
| Who owns which documents? | `docs/governance/document_lifecycle_guide.md §7` | Head of Specs Team |

---

## 4. Role Responsibilities

| Question | Document | Owner |
|----------|----------|-------|
| What does the PMO Lead do? | `docs/team_skills/pmo/pmo_lead.md` | PMO Lead |
| What does the QA Lead do? | `docs/team_skills/quality/qa_lead.md` | Director of Quality |
| What does the QA & Testing Owner do? | `docs/team_skills/engineering/QA_&_Testing Owner.md` | Engineering Lead |
| What does the Director of Quality do? | `docs/team_skills/quality/director_of_quality.md` | Director of Quality |
| What does the Head of Engineering do? | `docs/team_skills/engineering/Head_of_Engineering.md` | Head of Engineering |
| What does the Head of Specs Team do? | `docs/team_skills/specs/Head_of_Specs_Team.md` | Head of Specs Team |

---

## 5. Relationship to Specs Index

The Specs Index (`docs/specs/Specs_Index.md`) maps **canonical product and system specifications** — strategy rules, data model, API contracts, metrics definitions, frontend specs.

This Process Index maps **delivery process and governance documents** — how features are built, tested, shipped, and governed.

The two indexes are peers. Neither supersedes the other. Use the Specs Index when asking what the system does. Use this index when asking how the team works.
