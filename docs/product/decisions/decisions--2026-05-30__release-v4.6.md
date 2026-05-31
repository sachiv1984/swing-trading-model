**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Release:** v4.6
**Cycle:** 2026-05-30__release-v4.6
**Last Updated:** 2026-05-31
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Decisions Record — v4.6 SI-02 Behavioural Drift Detection & Arc 5 Completion

---

## Release

**Version:** v4.6
**Cycle:** 2026-05-30__release-v4.6
**Plan published:** 2026-05-30

---

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| SI-02 backend (S2-01) promoted to Sprint 1 firm | All pre-planning complete (§13 PASS, metric definitions, data schema); primary Arc 5 feature ready for implementation | Product Owner |
| SI-02 frontend (S2-02) conditional on data density gate | ≥20 closed trades with linked trade_plans required for meaningful drift analysis; ST-16 (BLG-GOV-33) audits count in Sprint 1 | Product Owner |
| Double capacity (24–28 days/sprint) | User directive; enables larger scope than typical governance-only sprints; scope still limited by available actionable backlog items, not capacity | Product Owner |
| BLG-GOV-32 + BLG-GOV-43 combined into ST-15 | Both modify release_planning_prompt.md; grouping reduces version bump overhead to single §6 application | Head of Specs Team |
| BLG-SPEC-32 gate cleared | Third external API integration (Anthropic) confirms ≥2 external APIs gate met; external API spec template now warranted | Head of Specs Team |
| SI-05 Phase 1 (BLG-GOV-67) conditional on 2026-06-21 gate | SI-01 + SI-03 live ≥30 days required; gate clears 2026-06-21; planned as Sprint 2 conditional item | Product Owner |

---

## Sequencing Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| Sprint 1 merge order: EPIC-04 → EPIC-01 | EPIC-04 governance items are fast-deliver and independent; EPIC-01 SI-02 backend is H-effort and the critical path dependency for Sprint 2 EPIC-02 | PMO Lead |
| Sprint 2 merge order: EPIC-03 → EPIC-02 | EPIC-03 Arc 5 enablers have no dependency on EPIC-02; EPIC-02 (SI-02 frontend) depends on EPIC-01 merged from Sprint 1 | PMO Lead |
| Data density audit (ST-16) must complete before EPIC-02 sprint planning seals | If data density gate not met, EPIC-02 deferred; sprint closes with Sprint 1 + EPIC-03 | Product Owner |

---

## Accepted Risks

None. All risks are mitigated inline (RISK-01–05 documented in release_plan.md § Risk Register).

---

## Supersession Note

Superseded by: v4.6 ship — 2026-05-31
Changelog: docs/product/changelog.md#v46
Verification report: claude/cycles/2026-05-30__release-v4.6/verification_report.md
Cycle: 2026-05-30__release-v4.6

Note: arc4_data_density_trajectory_v4.6.md and arc6_ps03_section13_preassessment.md are Operational Records (Class 3) — they are permanent and are NOT superseded by this closure.
