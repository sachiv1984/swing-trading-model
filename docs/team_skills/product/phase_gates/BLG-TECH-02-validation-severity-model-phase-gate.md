# Phase Gate Document — BLG-TECH-02 Validation Severity Model

**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Created:** 2026-02-21
**Filed:** — (immutable on closure)

**Charter authority:** `docs/team_skills/pmo/processess/defect_run.md` v1.1

---

## Defect Summary

| Field | Value |
|-------|-------|
| defect_id | BLG-TECH-02 |
| title | Implement validation severity model |
| source | Roadmap / Backlog (`docs/product/backlog.md`) |
| backlog_priority | P1 — High |
| target_release | v1.6.1 |
| canonical_spec | `analytics_endpoints.md` v1.8.1 (severity model contract — confirmed in roadmap) |
| severity | **High** — confirmed by QA Lead, 2026-02-21 |
| current_state | **LOGGED** |
| state_entered_at | 2026-02-21T00:00:00Z *(recorded at Phase Gate Document creation — UTC)* |
| co_delivery_constraint | Must be delivered alongside BLG-TECH-03. Neither defect may enter Fix In Progress, Fix Validated, or Closed independently without a formal PMO-validated scope decision. See §Co-Delivery Constraint. |

---

## Current Status

```
Current state:    LOGGED
Next gate:        G1 — LOGGED → TRIAGED
Who acts next:    QA Lead (severity), Engineering (BLG-TECH-01 confirmation),
                  Infra & Ops Documentation Owner (validation_system.md action)
Blockers:         B-02 (severity), B-03 (BLG-TECH-03 canonical spec),
                  B-04 (validation_system.md v1.0.2 action unconfirmed)
Escalation timer: STARTED — 2026-02-21T00:00:00Z
                  (timer runs against severity-tier SLA once severity is assigned)
```

---

## Co-Delivery Constraint

BLG-TECH-02 and BLG-TECH-03 are co-delivered per backlog and roadmap:

- BLG-TECH-03 AC states: *"Code touched once alongside BLG-TECH-02"*
- BLG-TECH-03 dependency states: *"Must be delivered alongside BLG-TECH-02"*

**Constraint (GI-5):** Neither defect may independently pass Gate G3 (Fix In Progress), G4 (Fix Validated), or G5 (Closed) unless a formal scope decision — validated by PMO Lead and recorded in both Phase Gate Documents — explicitly decouples them. Both documents are progressed in lock-step.

**Owner acknowledgement required:** Engineering must confirm this constraint in writing before G1 can pass (gate item G1.5). See Action A-05.

---

## Gate Register

### Gate G1 — LOGGED → TRIAGED

**Gate status: 🔴 CANNOT PASS — items outstanding**

---

#### G1.1 — BLG-TECH-01 prerequisite confirmed clear

```
Gate item:  BLG-TECH-01 signed off and v1.6 quality gate satisfied
            (Decision 7, BLG-TECH-01 decisions record: BLG-TECH-02 must
            not begin until BLG-TECH-01 is signed off and v1.6 gate cleared)

Evidence required:
  Written confirmation that BLG-TECH-01 is closed.
  Written confirmation that v1.6 quality gate is satisfied.

Satisfiability note:
  backlog.md records BLG-TECH-01 as "✅ COMPLETE — 2026-02-21"
  roadmap.md records "v1.6 quality gate satisfied"
  — Satisfiable subject to Engineering owner confirmation below.

Evidence:             ⬜ PENDING
Owner confirmation:   ⬜ PENDING — Engineering, date required
PMO validation:       ⬜ PENDING
```

---

#### G1.2 — BLG-TECH-01 outstanding action confirmed (HARD BLOCK on G3)

```
Gate item:  "Apply validation_system.md v1.0.2 — expected value independence
            and coverage completeness rules"
            (BLG-TECH-01 lessons learnt outstanding actions —
            docs/team_skills/pmo/lessons_learnt/BLG-TECH-01.md)
            Trigger: "Before BLG-TECH-02 implementation begins"

This item does NOT block Gate G1 (triage may proceed).
It is a HARD BLOCK on Gate G3 (Fix In Progress).
It is pre-registered here for full auditability.

Evidence required:
  Written confirmation from Infrastructure & Operations Documentation
  Owner and Engineering that validation_system.md v1.0.2 rules have
  been applied. Reference to updated document version required.

Evidence:             🔴 MISSING
Owner confirmation:   🔴 MISSING — Infrastructure & Operations
                      Documentation Owner + Engineering, date required
PMO validation:       FAIL (pending evidence)

⚠️  G3 is hard-blocked until this item passes.
```

---

#### G1.3 — Severity assigned

```
Gate item:  Severity tier formally assigned per defect_lifecycle.md §2

Evidence required:
  Written severity classification: Critical / High / Medium / Low
  Assigned by: QA Lead (sole authority)
  Date of assignment

PMO note:
  Backlog priority P1 ≠ defect severity. The QA Lead makes an
  independent determination. PMO will not infer severity from
  backlog priority. (GI-3)

Evidence:             Severity: High — deviation from analytics_endpoints.md v1.8.1;
                      severity field and by_severity aggregation absent from API
                      responses; canonical acceptance criteria unmet
Owner confirmation:   Yes — QA Lead, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

#### G1.4 — Canonical specification confirmed as implementation authority

```
Gate item:  analytics_endpoints.md v1.8.1 confirmed as the canonical
            implementation spec for the severity model

Evidence required:
  Engineering confirms in writing that analytics_endpoints.md v1.8.1
  is the sole canonical authority for BLG-TECH-02 implementation.

Satisfiability note:
  roadmap.md states: "Contract: analytics_endpoints.md v1.8.1 defines
  the canonical severity model. Engineering may begin pre-alignment."
  — Satisfiable subject to Engineering owner confirmation.

Evidence:             ⬜ PENDING (roadmap reference available)
Owner confirmation:   ⬜ PENDING — Engineering, date required
PMO validation:       ⬜ PENDING
```

---

#### G1.5 — Co-delivery constraint acknowledged

```
Gate item:  Co-delivery constraint between BLG-TECH-02 and BLG-TECH-03
            formally acknowledged by Engineering in writing in this document

Evidence required:
  Written acknowledgement from Engineering owner of this constraint
  (recorded in this document and mirrored in BLG-TECH-03 Phase Gate Document)

Evidence:             🔴 MISSING
Owner confirmation:   🔴 MISSING — Engineering, date required
PMO validation:       ⬜ PENDING
```

---

### Gate G2 — TRIAGED → ROOT CAUSE IDENTIFIED

*Not yet open. Gate items will be defined on entry to TRIAGED state.*

---

### Gate G3 — ROOT CAUSE IDENTIFIED → FIX IN PROGRESS

*Not yet open.*
**Pre-registered hard block:** G1.2 (validation_system.md v1.0.2 action) must pass before this gate opens.

---

### Gate G4 — FIX IN PROGRESS → FIX VALIDATED

*Not yet open.*

---

### Gate G5 — FIX VALIDATED → CLOSED

*Not yet open.*

---

## Action Register

| Action ID | Description | Owner | Deadline | Status | Blocked on |
|-----------|-------------|-------|----------|--------|------------|
| A-01 | Provide written confirmation that BLG-TECH-01 is closed and v1.6 quality gate satisfied (G1.1) | Engineering | By triage session — deadline TBC by PMO Lead | 🔴 OPEN | — |
| A-02 | Assign severity classification for BLG-TECH-02 (written, dated, QA Lead name) (G1.3) | QA Lead | 2026-02-21 | ✅ COMPLETE | — |
| A-03 | Confirm analytics_endpoints.md v1.8.1 as sole canonical authority for BLG-TECH-02 (G1.4) | Engineering | By triage session — deadline TBC by PMO Lead | 🔴 OPEN | — |
| A-04 | Acknowledge co-delivery constraint with BLG-TECH-03 in writing in this document (G1.5) | Engineering | By triage session — deadline TBC by PMO Lead | 🔴 OPEN | — |
| A-05 | Confirm completion of BLG-TECH-01 outstanding action: apply validation_system.md v1.0.2 rules — provide written evidence with document version reference (G1.2 — blocks G3) | Infrastructure & Operations Documentation Owner + Engineering | Before Fix In Progress gate opens | 🔴 OPEN | — |

> ⚠️ GI-2 notice: Deadlines marked "TBC" must be replaced with UTC-dated deadlines by the PMO Lead when the triage session is scheduled. "TBC" is not a compliant deadline.

---

## Open Blockers

| # | Blocker | Affects | Owner | Raised | Status |
|---|---------|---------|-------|--------|--------|
| B-03 | BLG-TECH-03 canonical spec unconfirmed (transitively blocks co-delivery) | G1.5 — state transition to Triaged for BLG-TECH-03 | Head of Specs Team | 2026-02-21 | 🔴 OPEN |
| B-04 | validation_system.md v1.0.2 action unconfirmed | G3 — Fix In Progress gate hard-blocked | Infra & Ops Documentation Owner + Engineering | 2026-02-21 | 🔴 OPEN |

---

## State Transition Log

| # | From | To | Date | Time (UTC) | Declared by | Gate passed |
|---|------|----|------|------------|-------------|-------------|
| 1 | PRE-LOGGED | LOGGED | 2026-02-21 | 00:00:00Z | PMO Lead | — (initial logging) |

---

## Stakeholder Next Steps

**As of 2026-02-21:**

| Role | Action | By when |
|------|--------|---------|
| QA Lead | Assign severity classification for BLG-TECH-02 — written, dated, name confirmed | Triage session (deadline TBC) |
| Engineering | Confirm BLG-TECH-01 closure + v1.6 quality gate satisfied | Triage session (deadline TBC) |
| Engineering | Confirm analytics_endpoints.md v1.8.1 as canonical authority | Triage session (deadline TBC) |
| Engineering | Acknowledge co-delivery constraint in writing | Triage session (deadline TBC) |
| Infra & Ops Documentation Owner + Engineering | Confirm validation_system.md v1.0.2 applied — written evidence with doc version | Before Fix In Progress gate opens |
| PMO Lead | Schedule triage session; replace all TBC deadlines with UTC dates | Immediate |
