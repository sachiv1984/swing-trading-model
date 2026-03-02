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

*(No changes in v1.1 — see v1.0 for full definitions.)*

---

## 4. Domain Ownership Map

*(No changes in v1.1 — see v1.0 for full definitions.)*

---

## 5. Conflict Resolution Rules

*(No changes in v1.1 — see v1.0 for full definitions.)*

---

## 6. Hard Constraints (Non-Negotiable in All Governed Routines)

*(No changes in v1.1 — see v1.0 for full definitions.)*

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
