# Defect Run

Owner: PMO Lead  
Type: PMO Process Template  
Status: Canonical  
Version: 1.1  
Last Updated: 2026-02-21  

---

## Change Log

| Version | Date | Change |
|--------|------|--------|
| 1.1 | 2026-02-21 | Formalised Phase Gate Document schema, explicit action tracking, system-derived state transitions, and system-enforced escalation timers. |
| 1.0 | — | Initial defect lifecycle definition. |

---

## 1. Purpose

This document defines the **mandatory defect delivery lifecycle**.

It ensures defects are:
- Tracked in exactly one state at all times
- Advanced only through validated gates
- Escalated deterministically
- Fully auditable after closure

---

## 2. Phase Gate Document (System of Record)

A **Phase Gate Document** is mandatory for every defect and is the authoritative execution record.

**Document class:** Class 3 — Operational Record  
**Lifecycle:** Filed (immutable after closure)

---

### 2.1 Required Fields (Normative)

The Phase Gate Document must contain:

- defect_id
- severity
- current_state
- state_entered_at (UTC timestamp)

- actions[]
  - action_id
  - description
  - owner
  - deadline
  - status (open | completed | invalidated)

- gates{}
  - gate_id
    - gate_item_id
      - evidence
      - owner_confirmation (yes/no, name, date)
      - pmo_validation (pass/fail, date)

- state_transition_log[]
  - from_state
  - to_state
  - timestamp
  - reason

All actions are **blocking** until completed or invalidated.

---

## 3. State Transition Rule

A state transition occurs **automatically** when:

- All gate items for the transition are validated, and
- No blocking actions remain

The PMO Lead validates gates.  
The system derives the state.

---

## 4. Defect State Machine

States (unchanged from v1.0):

1. Logged  
2. Triaged  
3. Root Cause Identified  
4. Fix In Progress  
5. Fix Validated  
6. Closed  

A defect may exist in **exactly one state** at any time.

---

## 5. Defect Severity Tiers & Escalation

Severity defines maximum allowed time per state.

- Escalation timers start at `state_entered_at`
- Timers are **system‑enforced**
- Breach triggers automatic escalation to the defined role
- PMO responds to escalations; does not track time manually

Severity thresholds and escalation paths remain unchanged from v1.0.

---

## 6. Actions

- Exactly one active action per owner (GI‑1)
- Every action must have a deadline (GI‑2)
- Actions are recorded in the Phase Gate Document
- Blocking actions prevent gate completion and state transition

---

## 7. Global Invariants (Mandatory)

| Invariant | Rule |
|---------|------|
| GI‑1 | One action per owner |
| GI‑2 | Every action has a deadline |
| GI‑3 | No gate passes without evidence |
| GI‑4 | Phase Gate Document updated within 15 minutes |
| GI‑5 | No ambiguity survives a phase transition |

Violation of any invariant blocks progress.

---

## 8. Closure

A defect may be closed only when:

- All gates are validated
- All actions are completed or invalidated
- The Phase Gate Document is complete and filed

Once filed, the record is immutable.
