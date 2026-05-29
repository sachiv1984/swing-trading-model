**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4

# Sprint Capacity — 2026-05-29__release-v4.4

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | ~12–14 working days per sprint (2 sprints planned) |
| Available FTE | Solo developer (evenings + weekends) |
| Per-sprint capacity | ~20–30 hrs |
| Total capacity (2 sprints) | ~40–60 hrs |
| Skill constraints | Backend Engineering delegated_decision (ST-06/07/09); Frontend Specs & UX Documentation Owner delegated_frontend (ST-10/11) |

Source: `claude/roadmap/workforce_capacity.md` (revised 2026-05-27 — baseline raised to ~12–14 days/sprint) + `claude/cycles/2026-05-29__release-v4.4/release_plan.md ## Capacity Check`

## Item Effort Table

### Sprint 1 — EPIC-01 + EPIC-04

| EPIC | ST | Title | Effort | Est. Hours | Delegation Class |
|------|----|-------|--------|------------|-----------------|
| EPIC-01 | ST-01 | BLG-GOV-71: roadmap_prompt.md STEP 8.1 advisory | XS | ~0.5 hr | autonomous |
| EPIC-01 | ST-02 | BLG-GOV-72: sprint_planning_prompt.md frontend classification fast-path | XS | ~0.5 hr | autonomous |
| EPIC-01 | ST-03 | BLG-GOV-73: execution_prompt.md auto-set deviations_filed | XS | ~0.5 hr | autonomous |
| EPIC-01 | ST-04 | BLG-GOV-69/74: qa_evidence_template.md delegated_qa sign-off format | XS | ~0.5 hr | autonomous |
| EPIC-01 | ST-05 | release_planning_prompt.md STEP 7 RESUME PRECHECK patch | XS | ~0.5 hr | autonomous |
| EPIC-04 | ST-13 | Staging URL disambiguation in OPERATIONAL_GUIDE §7 | XS | ~0.5 hr | autonomous |
| **Sprint 1 Total** | | | | **~3 hrs** | |

### Sprint 2 — EPIC-02 + EPIC-03

| EPIC | ST | Title | Effort | Est. Hours | Delegation Class |
|------|----|-------|--------|------------|-----------------|
| EPIC-02 | ST-06 | SI-02 drift detection query pre-design (BLG-BE-17) | M | ~8–12 hrs | delegated_decision |
| EPIC-02 | ST-07 | Arc 5 backend architecture review for SI query patterns (BLG-BE-18) | M | ~8–12 hrs | delegated_decision |
| EPIC-02 | ST-08 | SI-02 query index pre-assessment (BLG-BE-23) | S | ~4–6 hrs | autonomous |
| EPIC-02 | ST-09 | SI-02 background job architecture design (BLG-BE-20) *(Conditional)* | S | ~4–6 hrs | delegated_decision |
| EPIC-03 | ST-10 | SI-02 drift detection result component pre-design (BLG-FE-52) | S | ~4–6 hrs | delegated_frontend |
| EPIC-03 | ST-11 | SI-02 drift detection interaction spec (BLG-FE-53) | S | ~4–6 hrs | delegated_frontend |
| EPIC-03 | ST-12 | SI-02 Playwright scenario pre-design (BLG-QA-31) *(Conditional)* | S | ~4–6 hrs | autonomous |
| **Sprint 2 Total** | | | | **~36–50 hrs** | |

## Total Effort vs Capacity

| Sprint | Est. Effort | Available Capacity | Status |
|--------|-------------|-------------------|--------|
| Sprint 1 | ~3 hrs | ~20–30 hrs | PASS |
| Sprint 2 | ~36–50 hrs | ~20–30 hrs | WARN — high utilisation; within 2-sprint envelope |
| **Total (2 sprints)** | **~39–53 hrs** | **~40–60 hrs** | **WARN — at capacity boundary** |

**Capacity check outcome:** `warn` (inherited from release_plan.md `stage4_5_capacity_check: warn`). Sprint 1 is well within capacity (~3 hrs); Sprint 2 is heavy but within a single part-time sprint at the high end. Product Owner acknowledgement required — see sprint_planning_notes.md.

## Conditional (Deferred)

| EPIC | ST | Title | Effort | Gate Condition |
|------|----|-------|--------|----------------|
| EPIC-02 | ST-09 | SI-02 background job architecture design (BLG-BE-20) | S (~4–6 hrs) | ST-06 (BLG-BE-17) and ST-07 (BLG-BE-18) outputs available; SI-02 sprint scope beginning to crystallise |
| EPIC-03 | ST-12 | SI-02 Playwright scenario pre-design (BLG-QA-31) | S (~4–6 hrs) | ST-09 (BLG-BE-20) architecture output available; ST-10/ST-11 drift surfaces defined |

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-05-29__release-v4.4 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
