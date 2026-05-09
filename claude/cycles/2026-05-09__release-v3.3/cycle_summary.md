**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Published
**Release:** v3.3
**Cycle:** 2026-05-09__release-v3.3
**Published:** 2026-05-09

---

# Cycle Summary — v3.3 Arc 3 In-Trade Risk Management

## Theme

**Arc 3 Start** — v3.3 opens the In-Trade Risk Management arc. After two releases building the Arc 2 pre-trade research and planning surface, v3.3 turns to active position management: making position lifecycle state visible and surfacing the right decision prompt at the right moment.

The core Arc 3 milestone for v3.3: every open position has a visible lifecycle state (GRACE/LOSING/PROFITABLE/EXIT ZONE). The grace period alert and stop management workflow deliver the first two structured prompts — human-confirmed, §13-compliant, decision-support only.

## Scope Summary

| EPIC | Stories | Theme |
|------|---------|-------|
| EPIC-01 | ST-01–ST-03 | Arc 3 Foundation — IT-01 Position Lifecycle Manager |
| EPIC-02 | ST-04–ST-07 | Arc 3 Decision Support — IT-02 Grace Period + IT-03 Stop Management |
| EPIC-03 | ST-08–ST-12 | Research View Spec & QA Closure (BLG-SPEC-24/25/26, BLG-FE-28, BLG-QA-14/15/16/17, BLG-OPS-15, BLG-SEC-06, BLG-GOV-20) |
| EPIC-04 | ST-13–ST-17 | Governance Patches + Mandatory (OA-01/02/03/05, CF-01/02/03, BLG-FEAT-13, BLG-FEAT-21, quick wins) |

**Total: 17 stories / 4 EPICs / 2 sprints**

## Key Sequencing Notes

- EPIC-01 must complete in Sprint 1 before EPIC-02 can begin (Arc 3 data foundation).
- EPIC-03 runs in Sprint 1 parallel to EPIC-01 (independent spec/QA work).
- EPIC-04 governance stories (ST-13/14/15) in Sprint 1; BLG-FEAT-13 + quick wins in Sprint 2.

## Deferred

- IT-04 Drawdown Review, IT-05 Concentration Limits → v3.4 (sequenced after Arc 3 foundation).
- IT-06 Alpaca Paper Trading → v3.4+ (§13 review required).
- PT-04 Setup Quality Score → gate not met (20+ closed trades).

## Capacity

⚠ WARN — estimated 17–22 days effort vs ~20 days mid-point capacity. Tight but feasible. Phasing recommendation adopted.

## Risks

- RISK-01 (High): Position state machine data migration — back-fill logic must handle open positions without prior state. Mitigated by explicit UNKNOWN initial state.
- RISK-05 (High): **Design gate required** — EPIC-01 and EPIC-02 have frontend-visible changes. Design gate must produce UX specs for position lifecycle display, grace period prompt, and stop management UI before sprint planning seals.

---

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] Position state machine back-fill strategy — confirm handling of open positions with no prior state (UNKNOWN assignment + graceful display) — Owner: Head of Engineering
- [ ] [RISK-05] Design gate pass — UX specs for IT-01 (position lifecycle state display), IT-02 (grace period prompt), IT-03 (stop management guided UI) must be signed off by Head of UX & Design before sprint planning seals — Owner: Head of UX & Design + Product Owner

---

## Outstanding Actions Inherited (v3.2 → v3.3)

| OA | Description | Status in v3.3 plan |
|----|-------------|---------------------|
| OA-01/CF-01 | execution_prompt sealed-file integrity check | EPIC-04 ST-13 |
| OA-02/CF-02 | Mock payload API shape advisory | EPIC-04 ST-13 |
| OA-03/CF-03 | Backlog 3-cycle deferral policy | EPIC-04 ST-14 + BLG-FEAT-13 in scope |
| OA-04 | PMO Lead OA completion before cycle close | Ongoing monitoring |
| OA-05 | Design gate "before sprint planning" check | EPIC-04 ST-14 |
| OA-06 | Endpoint coverage gap | BLG-OPS-15 (EPIC-03 ST-12) |

## Next Steps

1. **Design gate** — Run `run design-gate --cycle 2026-05-09__release-v3.3` to produce UX specs for EPIC-01/02 frontend surfaces.
2. **Sprint planning** — Run `plan sprint --cycle 2026-05-09__release-v3.3` after design gate passes.
3. **Execution** — Run `run sprint --cycle 2026-05-09__release-v3.3`.
