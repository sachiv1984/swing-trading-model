**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.8
**Cycle:** 2026-06-01__release-v4.8
**Last Updated:** 2026-06-01

---

# Decisions Record — v4.8

---

## Scope Decisions

| # | Decision | Authority | Rationale |
|---|----------|-----------|-----------|
| D-01 | v4.8 is a governance/ops sprint with conditional SI-05 Phase 1 | Product Owner | 7 backlog items carry Provisional-Target: v4.8; SI-05 gate clears 2026-06-21 within sprint window |
| D-02 | Standard capacity (not double capacity) | Product Owner | v4.8 scope ~7–10 dev-days; double capacity (v4.6 pattern) unnecessary; v4.7 carry-forward OA-1 resolved |
| D-03 | Design gate NOT required | Head of Specs Team + Product Owner | No new UI surfaces; SI-05 Phase 1 is Telegram-only (no frontend); all items are documentation/governance edits |
| D-04 | BLG-SPEC-43 (SI-04 contract) included conditional on SI-04 confirmation | Product Owner | SI-04 §13 pre-assessment passed v4.7 (6 binding conditions); contract pre-authoring reduces same-sprint spec debt risk |
| D-05 | BLG-GOV-67 (SI-05 Phase 1) included conditional on 2026-06-21 gate | Product Owner | Gate clears within likely sprint window; Phase 1 is Telegram-only — no UI dependencies |

---

## Sequencing Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| S-01 | EPIC-01 and EPIC-02 run in parallel (no dependency) | Independent governance and ops items |
| S-02 | EPIC-03 runs after sprint planning gate check | Gate not cleared at planning time; check at sprint planning seal (2026-06-21) |
| S-03 | Single sprint (no Sprint 2) | All items S–M effort; total ~6–8.5 dev-days within standard capacity |

---

## Accepted Risks

None. RISK-01, RISK-02, RISK-03 are mitigated by design (gate check, backlog filing, scope containment). No formal Accepted Risk escalations raised.

---

## Pre-sprint Planning Required Decisions

No High-priority risks require resolution before sprint planning seals.

Sprint planning gate check required for EPIC-03 (SI-05 Phase 1, gate 2026-06-21). If gate not met at seal: EPIC-03 defers to v4.9.

---

## Supersession Note

*(Completed at Post-Ship Closure — left blank at publish time)*
