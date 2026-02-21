# Defect Run

Owner: PMO Lead
Type: PMO Process Template
Status: Canonical
Version: 1.2
Last Updated: 2026-02-21

---

## Change Log

| Version | Date | Change |
|--------|------|--------|
| 1.2 | 2026-02-21 | G4.1 now requires written deployment confirmation (verbal not sufficient); gate status header closure step added as mandatory PMO procedure; both changes actioned from BLG-TECH-02/03 lessons learnt. |
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
- Timers are **system-enforced**
- Breach triggers automatic escalation to the defined role
- PMO responds to escalations; does not track time manually

Severity thresholds and escalation paths remain unchanged from v1.0.

---

## 6. Actions

- Exactly one active action per owner (GI-1)
- Every action must have a deadline (GI-2)
- Actions are recorded in the Phase Gate Document
- Blocking actions prevent gate completion and state transition

---

## 7. Global Invariants (Mandatory)

| Invariant | Rule |
|---------|------|
| GI-1 | One action per owner |
| GI-2 | Every action has a deadline |
| GI-3 | No gate passes without evidence |
| GI-4 | Phase Gate Document updated within 15 minutes |
| GI-5 | No ambiguity survives a phase transition |

Violation of any invariant blocks progress.

---

## 8. Gate Closure Procedure (v1.2 addition)

When all items within a gate pass, the PMO Lead must, before advancing to the next gate:

1. **Update the gate-level status header** to `✅ ALL {GATE} ITEMS PASS`
2. **Update the current state block** to reflect the new state and next gate
3. **Log the state transition** in the State Transition Log with timestamp and gate reference
4. **Complete all steps within 15 minutes** (GI-4)

A gate whose items all show Pass but whose header still shows an earlier status is **non-compliant with GI-5** and may not be filed as immutable. The Director of Quality will withhold sign-off on a record with this inconsistency.

---

## 9. Gate Definitions

### G4 — FIX IN PROGRESS → FIX VALIDATED

**G4.1 — Fix deployed to verification environment**

Engineering must provide **written** confirmation. Verbal confirmation is not sufficient.

Written confirmation must state all four of the following:

1. The fix is deployed to the verification environment
2. The deployed files match the delivered artefacts — file by file
3. The branch or commit reference of the deployment
4. Engineering name and UTC timestamp

The PMO Lead must not pass G4.1 without written evidence satisfying all four criteria.

**Rationale (v1.2):** BLG-TECH-02/03 experienced two successive production 500 errors because
the files deployed to production did not match the reviewed artefacts. Verbal confirmation
provided no opportunity to catch the mismatch. Written confirmation with an explicit
file-match statement creates a verification moment before the deployment goes live.

**G4.2 — QA Lead re-verification: pass**

QA Lead re-executes the specific acceptance criteria for the defect and confirms pass.
Full re-run is not required unless the fix touched shared components. QA Lead documents
scope decision in writing. Evidence must include: scenario IDs executed, result per scenario,
QA Lead name, UTC timestamp.

---

## 10. Closure

A defect may be closed only when:

- All gates are validated
- All gate-level status headers are updated (per §8)
- All actions are completed or invalidated
- The Phase Gate Document is complete and filed

Once filed, the record is immutable.