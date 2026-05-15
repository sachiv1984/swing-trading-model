Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.5
Cycle: 2026-05-15__release-v3.5
Last Updated: 2026-05-15

## Release Scope — v3.5 Arc 3 Completion + Arc 4 Foundation

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Arc 3 Completion — IT-06 Alpaca Paper Trading: §13 compliance review (prerequisite story) + backend sync service + frontend display. US market only. Scoped conditional on §13 PASS. |
| S2-02 | EPIC-02 | Arc 4 Foundation — BLG-GOV-21 Arc 4 data requirements capture (prerequisite doc) + PO-01 Plan vs Reality Analysis backend (calculation service, data model) + PO-01 frontend (comparison view at trade close). |
| S2-03 | EPIC-03 | Spec & QA Debt — BLG-SPEC-29 (grace-period sessionStorage correction), BLG-SPEC-30 (stop-management PATCH correction), BLG-SPEC-31 (React Query v5 onSuccess scan), BLG-QA-19 (research view regression protocol). |
| S2-04 | EPIC-04 | Governance Patches — BLG-GOV-22 (sprint_planning_prompt.md execution_state.json ownership + Positions.js merge guidance) + execution_prompt.md deviation-filing advisory patches (LL v3.4 items #3–#5) + sprint_close / LL formatting improvements (LL v3.4 items #6–#7). |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| IT-06 implementation (conditional) | If §13 review yields FAIL, implementation scope removed from EPIC-01 | In-sprint decision |
| PT-04 Setup Quality Score | Gate: 20+ closed trades — data volume not yet reached | Arc 4 later cycle |
| BLG-FE-26 Research page UX review | P3; 3 cycles deferred; no blocking workflow | Arc 4/5 design gate |
| BLG-FE-27 Nav bar redesign exploration | Design exploration; not urgent | Arc 4/5 design gate |
| BLG-OPS-13 API performance baseline re-run | Requires live environment + human coordination | Next operational review |
| PO-02 Journal Pattern Recognition | Gate: 6+ months AI-summarised journal entries | Arc 4 later cycle |

### Supersession note

Superseded by: v3.5 ship — 2026-05-15
Changelog: docs/product/changelog.md#v35
Verification report: claude/cycles/2026-05-15__release-v3.5/verification_report.md
Cycle: 2026-05-15__release-v3.5
