# Phase Gate Document — BLG-TECH-03 ValidationService Consolidation

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
| defect_id | BLG-TECH-03 |
| title | Consolidate ValidationService into service layer |
| source | Roadmap / Backlog (`docs/product/backlog.md`) |
| backlog_priority | P1 — High |
| target_release | v1.6.1 |
| canonical_spec | `docs/team_skills/engineering/backend_engineering_patterns.md` (Canonical) — confirmed Head of Specs Team, 2026-02-21 |
| severity | **Medium** — confirmed by QA Lead, 2026-02-21 |
| current_state | **CLOSED** |
| state_entered_at | 2026-02-21T00:00:00Z *(recorded at Phase Gate Document creation — UTC)* |
| co_delivery_constraint | Must be delivered alongside BLG-TECH-02. Neither defect may enter Fix In Progress, Fix Validated, or Closed independently without a formal PMO-validated scope decision. See §Co-Delivery Constraint. |

---

## Current Status

```
Current state:    CLOSED ✅
Filed:            2026-02-21T21:30:00Z (immutable)
Director of Quality sign-off: 2026-02-21
Open conditions:  3 (non-blocking — tracked by PMO Lead)
```

---

## Co-Delivery Constraint

BLG-TECH-02 and BLG-TECH-03 are co-delivered per backlog and roadmap:

- BLG-TECH-03 AC states: *"Code touched once alongside BLG-TECH-02"*
- BLG-TECH-03 dependency states: *"Must be delivered alongside BLG-TECH-02"*

**Constraint (GI-5):** Neither defect may independently pass Gate G3 (Fix In Progress), G4 (Fix Validated), or G5 (Closed) unless a formal scope decision — validated by PMO Lead and recorded in both Phase Gate Documents — explicitly decouples them. Both documents are progressed in lock-step.

**Owner acknowledgement required:** Engineering must confirm this constraint in writing before G1 can pass (gate item G1.5). See Action A-04.

---

## Gate Register

### Gate G1 — LOGGED → TRIAGED

**Gate status: ✅ ALL G1 ITEMS PASS — state transition to TRIAGED pending co-delivery lock-step confirmation with BLG-TECH-02**

---

#### G1.1 — BLG-TECH-01 prerequisite confirmed clear

```
Gate item:  BLG-TECH-01 signed off and v1.6 quality gate satisfied
            (Decision 7, BLG-TECH-01 decisions record: BLG-TECH-03 must
            not begin until BLG-TECH-01 is signed off and v1.6 gate cleared)

Evidence required:
  Written confirmation that BLG-TECH-01 is closed.
  Written confirmation that v1.6 quality gate is satisfied.

Satisfiability note:
  backlog.md records BLG-TECH-01 as "✅ COMPLETE — 2026-02-21"
  roadmap.md records "v1.6 quality gate satisfied"
  — Satisfiable subject to Engineering owner confirmation below.

Evidence:             backlog.md — BLG-TECH-01 status: ✅ COMPLETE 2026-02-21;
                      roadmap.md — "v1.6 quality gate satisfied"
Owner confirmation:   Yes — Head of Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

#### G1.2 — BLG-TECH-01 outstanding action confirmed (HARD BLOCK on G3)

```
Gate item:  "Apply validation_system.md v1.0.2 — expected value independence
            and coverage completeness rules"
            (BLG-TECH-01 lessons learnt outstanding actions —
            docs/team_skills/pmo/lessons_learnt/BLG-TECH-01.md)
            Trigger: "Before BLG-TECH-02 implementation begins"
            — applies transitively to BLG-TECH-03 via co-delivery constraint

This item does NOT block Gate G1 (triage may proceed).
It is a HARD BLOCK on Gate G3 (Fix In Progress).
It is pre-registered here for full auditability.

Evidence required:
  Written confirmation from Infrastructure & Operations Documentation
  Owner and Engineering that validation_system.md v1.0.2 rules have
  been applied. Reference to updated document version required.

Evidence:             docs/operations/validation_system.md v1.0.2
                      Rule 1 added: expected value independence — values must
                      be independently hand-calculated from metrics_definitions.md,
                      never derived by running the implementation.
                      Rule 2 added: coverage completeness — every metric in
                      GET /analytics/metrics must have a EXPECTED_METRICS entry;
                      omission is a governance violation.
Owner confirmation:   Yes — Infrastructure & Operations Documentation Owner
                      + Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
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

Evidence:             Severity: Medium — architectural deviation, validation logic
                      split between router and service stub; no canonical
                      behaviour currently incorrect; risk of future duplication
                      but no present correctness failure
Owner confirmation:   Yes — QA Lead, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

#### G1.4 — Canonical specification confirmed as implementation authority

```
Gate item:  Named canonical specification confirmed as the sole
            implementation authority for BLG-TECH-03 service layer scope

Evidence required:
  Head of Specs Team identifies and confirms in writing the canonical
  spec governing:
    - Service layer structure
    - Validation consolidation (no validation logic in router)
  Named spec document + version required.

Evidence:             docs/team_skills/engineering/backend_engineering_patterns.md
                      (Status: Canonical) — §3 non-negotiable rules:
                      "Routers must be thin. No business logic in a router."
                      "Services contain all business logic."
                      Secondary ref: analytics_endpoints.md v1.8.1 known
                      limitations confirms the deviation is tracked as BLG-TECH-03.
                      Compliance note raised: backend_engineering_patterns.md
                      carries no version number — non-compliant with
                      document_lifecycle_guide.md §2 Class 1; separate
                      governance action raised by Head of Specs Team.
Owner confirmation:   Yes — Head of Specs Team, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

#### G1.5 — Co-delivery constraint acknowledged

```
Gate item:  Co-delivery constraint between BLG-TECH-02 and BLG-TECH-03
            formally acknowledged by Engineering in writing in this document

Evidence required:
  Written acknowledgement from Engineering owner of this constraint
  (recorded in this document and mirrored in BLG-TECH-02 Phase Gate Document)

Evidence:             Written confirmation: BLG-TECH-02 and BLG-TECH-03 to be
                      progressed in lock-step; neither will enter Fix In Progress,
                      Fix Validated, or Closed independently without formal
                      PMO-validated scope decision
Owner confirmation:   Yes — Head of Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

### Gate G2 — TRIAGED → ROOT CAUSE IDENTIFIED

**Gate status: ✅ ALL G2 ITEMS PASS**

---

#### G2.1 — Root cause identified

```
Gate item:  Written root cause statement provided by Engineering

Evidence:   services/validation_service.py is a stub — validate_all()
            contains only TODO comments and returns hardcoded zeroes.
            All 13-metric validation logic lives in routers/validation.py
            validate_calculations() in direct violation of
            backend_engineering_patterns.md §3. Service was scaffolded
            but never implemented; router used as shortcut and never
            migrated.
Owner confirmation:   Yes — Head of Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

#### G2.2 — Files/components confirmed

```
Gate item:  Engineering confirms which files the fix will touch

Evidence:   backend/services/validation_service.py — implement full
            13-metric validation logic.
            backend/routers/validation.py — strip business logic,
            delegate to ValidationService. (Co-delivery: also receives
            severity field additions as part of BLG-TECH-02 in same PR)
Owner confirmation:   Yes — Head of Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

#### G2.3 — No spec change required

```
Gate item:  Engineering confirms no canonical spec change is required
            before fix proceeds

Evidence:   backend_engineering_patterns.md §3 is unambiguous.
            No spec conflict identified. Fix proceeds directly against
            existing canonical spec.
Owner confirmation:   Yes — Head of Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

---

### Gate G3 — ROOT CAUSE IDENTIFIED → FIX IN PROGRESS

**Gate status: ✅ ALL G3 ITEMS PASS**

---

#### G3.1 — Fix confirmed in progress

```
Gate item:  Engineering confirms fix work has begun
Evidence:   Branch: fix/blg-tech-02-03-severity-service-consolidation
Owner confirmation:   Yes — Head of Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

#### G3.2 — Fix scope matches confirmed root cause

```
Gate item:  Engineering confirms fix is scoped to the files identified
            at G2.2 and addresses the root cause identified at G2.1
Evidence:   backend/services/validation_service.py — full implementation;
            all 13-metric validation logic moved here from router;
            severity field and by_severity produced here.
            backend/routers/validation.py — stripped to HTTP in/out only;
            delegates entirely to ValidationService.validate_all().
            No additional files in scope.
Owner confirmation:   Yes — Head of Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

#### G3.3 — Co-delivery constraint observed

```
Gate item:  BLG-TECH-02 and BLG-TECH-03 fixes are in the same PR/branch
Evidence:   Single branch covers both defects:
            fix/blg-tech-02-03-severity-service-consolidation
Owner confirmation:   Yes — Head of Engineering, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

---

### Gate G4 — FIX IN PROGRESS → FIX VALIDATED

**Gate status: ✅ ALL G4 ITEMS PASS**

---

#### G4.1 — Fix deployed to verification environment

```
Gate item:  Engineering confirms fix is deployed and available for QA
Evidence:   Verbal confirmation — Head of Engineering, 2026-02-21T20:55:00Z
            Branch: fix/blg-tech-02-03-severity-service-consolidation
Owner confirmation:   Yes — Head of Engineering, 2026-02-21T20:55:00Z
PMO validation:       Pass — PMO Lead, 2026-02-21T20:55:00Z
```

---

#### G4.2 — QA Lead re-verification: pass

```
Gate item:  QA Lead re-executes acceptance criteria for BLG-TECH-03
            and confirms pass

Scope decision: Full re-run NOT required. AnalyticsService and
validation_data.py untouched. Re-verification scoped to:

  SC-03-01: routers/validation.py source contains no business logic
            PASS — router is 45 lines; HTTP in/out only; delegates
            entirely to ValidationService.validate_all()
  SC-03-02: all 13 original metric actual values identical to
            BLG-TECH-01 baseline (13/13 pass, 2026-02-21T00:24:41Z)
            PASS — all 13 values preserved exactly; no regressions
  SC-03-03: live code path confirmed — stub is dead
            PASS — timestamp 2026-02-21T21:25:19.368999Z (current);
            total 14 not 12; no hardcoded zeroes in actual fields

Production response timestamp: 2026-02-21T21:25:19.368999Z
Owner confirmation:   Yes — QA Lead, 2026-02-21T21:25:00Z
PMO validation:       Pass — PMO Lead, 2026-02-21T21:25:00Z
```

---
**Co-delivery lock:** Cannot open independently of BLG-TECH-02 Gate G4.

---

### Gate G5 — FIX VALIDATED → CLOSED

**Gate status: ✅ ALL G5 ITEMS PASS**

---

#### G5.1 — Director of Quality sign-off

```
Gate item:  Director of Quality independently reviews verification record
            and signs off both defects

Evidence:   Independent review conducted 2026-02-21. Five findings raised:
            Finding 1 (blocking) — G4 header corrected before sign-off.
            Findings 2–5 (non-blocking) — recorded, conditions attached.
            All acceptance criteria confirmed covered by passing scenarios.
            Re-verification pass confirmed — QA Lead, 2026-02-21T21:25:00Z.
            Record internally consistent. QA Lead independence confirmed.

Conditions: (1) Lessons learnt entry required — two failed production deploys
            (2) Product Owner to be notified of OBS-01; backlog item required
                before v1.6.1 ships to canonicalise sharpe_ratio_trade_method
            (3) backend_engineering_patterns.md version governance action
                to be tracked by PMO Lead as separate open item

Owner confirmation:   Yes — Director of Quality, 2026-02-21
PMO validation:       Pass — PMO Lead, 2026-02-21
```

---

## Action Register

| Action ID | Description | Owner | Deadline | Status | Blocked on |
|-----------|-------------|-------|----------|--------|------------|
| A-01 | Provide written confirmation that BLG-TECH-01 is closed and v1.6 quality gate satisfied (G1.1) | Engineering | 2026-02-21 | ✅ COMPLETE | — |
| A-02 | Assign severity classification for BLG-TECH-03 (written, dated, QA Lead name) (G1.3) | QA Lead | 2026-02-21 | ✅ COMPLETE | — |
| A-03 | Identify and confirm in writing the canonical specification governing BLG-TECH-03 service layer scope (G1.4) | Head of Specs Team | 2026-02-21 | ✅ COMPLETE | — |
| A-04 | Acknowledge co-delivery constraint with BLG-TECH-02 in writing in this document (G1.5) | Engineering | 2026-02-21 | ✅ COMPLETE | — |
| A-05 | Confirm completion of BLG-TECH-01 outstanding action: apply validation_system.md v1.0.2 rules — written evidence with document version reference (G1.2 — blocks G3, transitively via co-delivery) | Infrastructure & Operations Documentation Owner + Engineering | 2026-02-21 | ✅ COMPLETE | — |

> ⚠️ GI-2 notice: Deadlines marked "TBC" must be replaced with UTC-dated deadlines by the PMO Lead when the triage session is scheduled. "TBC" is not a compliant deadline.

---

## Open Blockers

| # | Blocker | Affects | Owner | Raised | Status |
|---|---------|---------|-------|--------|--------|
**No open blockers.**

---

## State Transition Log

| # | From | To | Date | Time (UTC) | Declared by | Gate passed |
|---|------|----|------|------------|-------------|-------------|
| 1 | PRE-LOGGED | LOGGED | 2026-02-21 | 00:00:00Z | PMO Lead | — (initial logging) |
| 2 | LOGGED | TRIAGED | 2026-02-21 | 00:00:00Z | PMO Lead | G1 — all items pass |
| 3 | TRIAGED | ROOT CAUSE IDENTIFIED | 2026-02-21 | 00:00:00Z | PMO Lead | G2 — all items pass |
| 4 | ROOT CAUSE IDENTIFIED | FIX IN PROGRESS | 2026-02-21 | 00:00:00Z | PMO Lead | G3 — all items pass |
| 5 | FIX IN PROGRESS | FIX VALIDATED | 2026-02-21 | 21:25:00Z | PMO Lead | G4 — all items pass; QA Lead re-verification pass |
| 6 | FIX VALIDATED | CLOSED | 2026-02-21 | 21:30:00Z | PMO Lead | G5 — Director of Quality sign-off |

---

## Stakeholder Next Steps

**As of 2026-02-21:**

| Role | Action | By when |
|------|--------|---------|
| QA Lead | Assign severity classification for BLG-TECH-03 — written, dated, name confirmed | Triage session (deadline TBC) |
| Engineering | Confirm BLG-TECH-01 closure + v1.6 quality gate satisfied | Triage session (deadline TBC) |
| Engineering | Acknowledge co-delivery constraint in writing | Triage session (deadline TBC) |
| Head of Specs Team | Identify and confirm canonical spec for BLG-TECH-03 service layer scope | Triage session (deadline TBC) |
| Infra & Ops Documentation Owner + Engineering | Confirm validation_system.md v1.0.2 applied — written evidence with doc version | Before Fix In Progress gate opens |
| PMO Lead | Schedule triage session; replace all TBC deadlines with UTC dates | Immediate |