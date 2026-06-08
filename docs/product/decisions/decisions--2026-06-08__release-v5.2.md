Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v5.2
Cycle: 2026-06-08__release-v5.2
Last Updated: 2026-06-08

## Planning Decisions — v5.2 Governance Debt, SI-05 Ops & Spec Compliance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include OA-01 (release_planning_prompt.md §-1.2 patch) as firm EPIC-01 story | OA due before v5.2 sprint planning seals per v5.1 lessons_learnt carry-forward D-1 (LL-RP-v5.1-01); Head of Specs Team accountable | Product Owner | 2026-06-08 |
| Include OA-02 (execution_prompt.md §3.1.A patch) as firm EPIC-01 story | OA due before v5.2 sprint planning seals per v5.1 lessons_learnt carry-forward D-2; Head of Specs Team accountable | Product Owner | 2026-06-08 |
| Include BLG-SPEC-47 (pass_rate alignment) despite P3 severity | Must resolve before next SI-05 feature increment; DEV-v51-EPIC01-01 outstanding; HoST to make canonical determination | Head of Specs Team | 2026-06-08 |
| Include BLG-SPEC-48 (digest endpoint contract) as P1 firm story | CLAUDE.md §2 same-sprint contract rule; v5.1 shipped POST /digest/si05/send without confirmed contract document | Head of Specs Team | 2026-06-08 |
| Include all SI-05 ops/reliability items (BLG-BE-32/33, BLG-OPS-55/56) | SI-05 Phase 1 shipped in v5.1 with no delivery log, retry handling, or documented operational procedures; these are prerequisite for staged verification sprint | Product Owner | 2026-06-08 |
| Include BLG-GOV-97 (model deprecation check) as firm P1 | BLG-GOV-90 deprecation monitoring procedure defined; first check is overdue; AI API calls break in production if model is deprecated without notice | AI Compliance & Governance Officer | 2026-06-08 |
| Include all three security reviews (BLG-GOV-98/99/100) | SI-05 introduced a Telegram bot token and new unauthenticated endpoint; security review is standard governance for new external-facing capabilities | Cybersecurity & Trust Lead | 2026-06-08 |
| Include BLG-QA-47 + BLG-GOV-94 (acceptance test protocol + delivery verification protocol) | Staged verification sprint for v5.1 deferred ACs cannot begin without formal protocols; these are prerequisite documents | Director of Quality | 2026-06-08 |
| Include BLG-GOV-96 (SI-05 effectiveness criteria) | Phase 2 activation decision (BLG-GOV-92) depends on Phase 1 effectiveness evidence; criteria must be defined before the 30-day review date (2026-07-04) | Product Owner | 2026-06-08 |
| Include BLG-FE-64 as conditional (gate 2026-06-21) | Gate clears 13 days from release planning; high likelihood of inclusion at sprint planning; include now to avoid delaying to v5.3 | Product Owner | 2026-06-08 |
| Defer BLG-GOV-93 (OA check procedure) | Scope absorbed: OA-01 and OA-02 are explicitly included as firm EPIC-01 stories; procedural tracking is handled in run_manifest.md | PMO Lead | 2026-06-08 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Merge order: EPIC-03 → EPIC-02 → EPIC-04 → EPIC-01 | Security reviews (EPIC-03) unblock parallel work; backend reliability (EPIC-02) prerequisite for health check in OPS-56; QA/verification docs (EPIC-04) unblock staged sprint; prompt patches (EPIC-01) last to avoid affecting engine mid-sprint | PMO Lead | 2026-06-08 |
| Design gate: not required | All 17+ stories are backend, governance document, or spec/assessment work — no new UI or UX components introduced; confirmed by design dependency scan (0 items flagged) | Head of UX & Design + Product Owner | 2026-06-08 |
| Single sprint (no Sprint 2) | Total effort ~10–11 days mid-point; feasible in 2-week window with parallel document production; no hard gates blocking sprint completion | PMO Lead | 2026-06-08 |

### Accepted risks

None — no escalations raised in this cycle; RISK-03 (auth gap discovery) is managed as a conditional follow-on item if gap is found, not an accepted risk.

### Supersession note

Superseded by: v5.2 ship — 2026-06-08
Changelog: docs/product/changelog.md#v52
Verification report: claude/cycles/2026-06-08__release-v5.2/verification_report.md
Cycle: 2026-06-08__release-v5.2
