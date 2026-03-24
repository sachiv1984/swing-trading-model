Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-24
Cycle: 2026-03-24__release-v2.3

---

# Sprint Capacity — v2.3 Quality Automation & User Insight

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint count | 3 |
| Sprint duration per sprint | ~6–8 working days (solo developer, evenings + focused sessions) |
| Total confirmed capacity | ~18–24 working days across 3 sprints |
| Available FTE | 1 (solo developer — full-stack) |
| Skill coverage | Backend (FastAPI/Python), Frontend (Base44), QA (Playwright), Infrastructure & Operations, Governance/Spec authoring |

## Skill Constraints

| Skill | Constraint |
|-------|-----------|
| Strategy Rules & System Intent Owner sign-off | Required at delivery verification for ST-01 (BLG-FEAT-11 SPS=4); not a capacity blocker within sprint |
| Playwright E2E | Required for ST-05 (QA-05) and ST-06 (QA-01); within solo-dev skill set |
| Governance prompt authoring | Required for ST-14 (GOV-07) and ST-17 (GOV-08); Head of Specs Team + PMO Lead sign-off required before applying changes |

## Item Effort Mapping

| Item | EPIC | Effort estimate | Notes |
|------|------|----------------|-------|
| ST-01 BLG-FEAT-11 | EPIC-01 | M–L (~3–5 days) | SPS=4 sign-off overhead at DoQ |
| ST-02 BLG-FEAT-09 | EPIC-01 | S–M (~1–2 days) | |
| ST-03 BLG-OPS-08 | EPIC-02 | S (~0.5 day) | Gates ST-04 and ST-05 |
| ST-04 BLG-QA-06 | EPIC-02 | S–M (~1 day) | Gated on ST-03 |
| ST-05 BLG-QA-05 | EPIC-02 | M (~2 days) | Gated on ST-03 + ST-04 |
| ST-06 BLG-QA-01 | EPIC-02 | M (~1–2 days) | Independent of OPS-08 chain |
| ST-07 BLG-SPEC-D14 | EPIC-03 | XS (<1 hour) | Gates ST-09 |
| ST-08 BLG-OPS-09 | EPIC-03 | S (~0.5 day) | |
| ST-09 BLG-OPS-07 | EPIC-03 | S (~0.5 day) | Gated on ST-07 |
| ST-10 BLG-FE-05 | EPIC-04 | S (~0.5 day) | |
| ST-11 BLG-FE-04 | EPIC-04 | XS (<1 hour) | |
| ST-12 BLG-FE-02 | EPIC-04 | M (~1–2 days) | |
| ST-13 BLG-UX-01 | EPIC-04 | M (~1–2 days) | Design decision resolved (design gate) |
| ST-14 BLG-GOV-07 | EPIC-05 | XS (<1 hour) | |
| ST-15 BLG-QA-03 | EPIC-05 | S (~0.5 day) | |
| ST-16 BLG-QA-04 | EPIC-05 | M (~1 day) | |
| ST-17 BLG-GOV-08 | EPIC-05 | L (~2–3 days) | Conditional stretch — depends on Sprint 3 residual capacity |

## EPIC Effort Totals

| EPIC | Stories | Effort estimate |
|------|---------|----------------|
| EPIC-01 | 2 | ~4–7 days |
| EPIC-02 | 4 | ~4–6 days |
| EPIC-03 | 3 | ~1–2 days |
| EPIC-04 | 4 | ~3–5 days |
| EPIC-05 | 4 | ~3–6 days (GOV-08 conditional) |
| **Total** | **17** | **~15–26 days (mid-point ~20 days)** |

## Capacity vs Effort

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~18–24 days (3 sprints) |
| Total estimated effort (all 17 items, GOV-08 included) | ~15–26 days (mid ~20 days) |
| Total estimated effort (GOV-08 excluded as conditional) | ~13–23 days (mid ~18 days) |
| Over-allocation risk | WARN — upper bound with GOV-08 (26 days) exceeds ceiling (24 days) |

**Product Owner capacity WARN acknowledgement (IMP-41):** Acknowledged 2026-03-24. Rationale: BLG-GOV-08 (ST-17) is a conditional stretch item that does not block release if skipped. Without GOV-08, the total mid-point estimate (~18 days) is within the confirmed capacity envelope. GOV-08 will execute in Sprint 3 only if residual capacity permits after ST-13 and ST-16.

## Sprint Phasing

| Sprint | Items | Estimated effort |
|--------|-------|----------------|
| Sprint 1 | ST-14, ST-15, ST-07, ST-08, ST-09, ST-03, ST-06 | ~5–8 days |
| Sprint 2 | ST-04, ST-05, ST-01, ST-02 | ~8–13 days |
| Sprint 3 | ST-10, ST-11, ST-12, ST-13, ST-16, ST-17 (conditional) | ~5–8 days |
