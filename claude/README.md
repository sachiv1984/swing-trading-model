Owner: Head of Specs Team
Status: Supporting  
Canonical Source: /charter/team_charter.md  
Last Updated: 2026-03-16  

---

# Claude Organisational Execution Engine

## 1. What This Repository Is

This repository is an **executable governance system**.

It encodes:
- Authority and decision rights
- Documentation lifecycle rules
- Workforce-as-capital allocation
- Deterministic organisational routines

Claude does not advise, brainstorm, or optimise for consensus.  
Claude **enforces the conditions under which decisions are allowed to exist**.

---

## 2. Governing Authorities

All behaviour in this repository is governed by the following **canonical documents**:

- `/charter/team_charter.md`
- `/charter/documentation_lifecycle_guide.md`

If any routine, document, or output conflicts with these authorities,  
**the governance documents prevail**.

---

## 3. Core Invariants (Apply to All Routines)

See `claude/system/invariants.md` for the canonical list.

Any routine that violates these invariants is invalid.

---

## 4. Organisational Routines

This system executes governed organisational routines.

Each routine:
- Has a defined trigger
- Activates a specific set of authorities
- Produces canonical artefacts
- Enforces documentation lifecycle compliance

### 4.1 Roadmap Rebalance (Primary Routine)

**Trigger:** Feature completion  
**Purpose:** Reallocate workforce capacity and update the roadmap  
**Canonical Outputs:**
- Updated roadmap
- Updated initiative register
- Updated workforce capacity
- Decision log entry

This routine performs a full integrity sweep:
- Roadmap validation
- Backlog health review
- Idea evaluation and displacement
- Workforce economics enforcement
- Add / Replace / Defer / Kill decisions

Execution logic is defined in:
- `/system/claude_system_prompt.md`

---

## 5. Repository Structure (Overview)

- `/charter` — Canonical governance authorities  
- `/agents` — Delegated authority roles  
- `/roadmap` — Planning documents (Class 4)  
- `/backlog` — Planning documents (Class 4)  
- `/cycles` — Execution records and audit trail  
- `/system` — Governance and execution prompts  
- `/ideas` — Idea submissions and evaluation artefacts  

All documents in this repository are governed by the **Documentation Lifecycle Guide**.

---

## 6. Adding New Routines

New routines must explicitly define:

1. Trigger condition  
2. Activated decision domains  
3. Required authority roles  
4. Canonical inputs  
5. Canonical outputs  
6. Lifecycle compliance points  

Routines may not:
- Invent or merge authority
- Bypass lifecycle rules
- Modify canonical truth outside declared ownership

---

## 7. What This README Is Not

This README:
- Does not define authority
- Does not override governance documents
- Does not replace lifecycle rules
- Does not describe implementation detail

It is a **Supporting document** that reflects canonical governance.  
It must never be treated as a source of truth for decisions.

---

## 8. Resolving Ambiguity

If ambiguity exists about:
- Authority
- Ownership
- Valid documentation
- Decision rights

Refer to:
- `/charter/team_charter.md`
- `/charter/documentation_lifecycle_guide.md`

Those documents are authoritative.
