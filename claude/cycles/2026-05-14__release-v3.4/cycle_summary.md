**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.4
**Cycle:** 2026-05-14__release-v3.4
**Published:** 2026-05-14

---

# Cycle Summary — v3.4 Arc 3 In-Trade Risk Management (continued)

## Release Overview

| Field | Value |
|-------|-------|
| Release | v3.4 |
| Theme | Arc 3 Frontend Completion + IT-04/05 Risk Prompts + Frontend Quick Wins + Spec/QA Debt |
| Cycle ID | 2026-05-14__release-v3.4 |
| Mode | standard |
| Capacity verdict | WARN (11 days estimated vs ~10–13 available) |
| EPICs | 4 |
| Stories | 14 |
| Sprints | 2 |

## Scope Summary

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | 2 | ST-01, ST-02, ST-03 | Arc 3 Frontend Completion (IT-01/02/03) |
| EPIC-02 | 2 | ST-04, ST-05, ST-06 | Arc 3 Risk Prompts: IT-04 Drawdown, IT-05 Concentration Limits |
| EPIC-03 | 1 | ST-07, ST-08, ST-09, ST-10 | Frontend Quick Wins (v3.3 deferred) |
| EPIC-04 | 1 | ST-11, ST-12, ST-13, ST-14 | Spec, QA & Documentation Debt |

## Key Decisions

1. **EPIC-02 sequenced Sprint 2, post design gate** — IT-04/05 are new Arc 3 features without UX specs; design gate (Phase 1.5) must run first.
2. **BLG-FE-31 first item in Sprint 1** — component library for PT-02 research view components; must precede EPIC-01 implementation.
3. **Frontend front-loaded** — carry-forward from LL-v3.3 item 1: EPIC-03 (quick wins) in Sprint 1, EPIC-01 (Arc 3 frontend) in Sprint 2 using component library reference.
4. **Merge order established** — EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02 (carry-forward LL-v3.3 item 2); document in execution_state.json at STEP 3 of sprint execution.

## Carry-Forward Acknowledgements (LL-v3.3)

| # | Item | v3.4 response |
|---|------|--------------|
| 1 | Frontend delegation pattern — front-load frontend | EPIC-03 in Sprint 1; EPIC-01 dedicated to Arc 3 frontend in Sprint 2 |
| 2 | Merge order discipline | Merge order documented in decisions record; must be in execution_state.json at execution STEP 3 |
| 3 | QA evidence branch advisory | Advisory surfaced in sprint execution carry-forward |

## Risks

| RISK-ID | Description | Priority | Sprint |
|---------|-------------|----------|--------|
| RISK-01 | IT-04/IT-05 need design gate UX specs before EPIC-02 sprint planning seals | **High** | EPIC-02, Sprint 2 |
| RISK-02 | EPIC-01 implements pre-existing UX specs — TEST-GAP-EPIC-01/02-v33 scenarios must be authored alongside implementation | Medium | EPIC-01, Sprint 2 |
| RISK-03 | IT-05 depends on DS-03 sector data quality | Low | EPIC-02, Sprint 2 |
| RISK-04 | Frontend-heavy release; capacity at upper bound; further deferral risk | Medium | Release-level |

## Deferred Items

| Item | Reason |
|------|--------|
| IT-06 Alpaca Paper Trading | §13 gate not cleared |
| PT-04 Setup Quality Score | 20+ closed trades gate not met |
| BLG-FE-26 Research page UX review | Design gate phase for v3.4 addresses this |
| BLG-FEAT-20 Net-of-costs tracking | Arc 3/4 sequencing |
| BLG-OPS-13 API performance baseline | Requires live environment + human coordination |
| BLG-GOV-21 Arc 4 data requirements | Before Arc 4 planning |

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] IT-04/05 UX specs — Design gate (Phase 1.5) must produce UX specs for Drawdown Review Prompt and Concentration Limits Warning UI before EPIC-02 stories can be sprint-planned — Owner: Head of UX & Design + Product Owner

## Next Steps

1. Run `run design-gate --cycle 2026-05-14__release-v3.4` (Phase 1.5) — produces UX specs for IT-04/05; also addresses BLG-FE-26 research page UX review
2. Run `plan sprint --cycle 2026-05-14__release-v3.4` (Phase 2) — after design gate passes
