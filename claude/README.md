Owner: Head of Specs Team
Status: Supporting  
Canonical Source: /charter/team_charter.md  
Last Updated: 2026-07-02  

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
- `/charter/document_lifecycle_guide.md`

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
- `claude/system/roadmap_prompt.md`

---

### 4.2 Other Governed Routines (Summary)

| Routine | Command | Prompt |
|---|---|---|
| Release Planning | `plan release` | `claude/system/release_planning_prompt.md` |
| Sprint Planning | `plan sprint` | `claude/system/sprint_planning_prompt.md` |
| Sprint Execution | `run sprint` | `claude/system/execution_prompt.md` |
| Delivery Verification | `run delivery verification` | `claude/system/delivery_verification_prompt.md` |
| Post-Ship Closure | `run post-ship` | `claude/system/post_ship_closure.md` |
| Amendment Cycle | `amend cycle` | `claude/system/amendment_cycle_prompt.md` |
| Design Gate | `run design-gate` | `claude/system/design_gate_prompt.md` |
| Idea Intake | `run ideas` | `claude/system/idea_intake_prompt.md` |
| Roadmap Management | `manage roadmap` | `claude/system/roadmap_management_prompt.md` |
| Backlog Management | `groom backlog` | `claude/system/backlog_management_prompt.md` |
| Ideas Housekeeping | `run ideas housekeeping` | `claude/system/ideas_housekeeping_prompt.md` |
| Lifecycle Audit | `run audit` | `claude/audit.py` |

Full trigger conditions and phase sequencing: see `claude/system/OPERATIONAL_GUIDE.md` §4.

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
- `/charter/document_lifecycle_guide.md`

Those documents are authoritative.
