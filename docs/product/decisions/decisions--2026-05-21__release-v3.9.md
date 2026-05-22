Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.9
Cycle: 2026-05-21__release-v3.9
Last Updated: 2026-05-22

## Planning Decisions — v3.9 Screener Quality & Reliability + Arc 5 Red Flag Journal + Governance Patches

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Screener bug fixes (BLG-TECH-10, BLG-BE-10, BLG-BE-11) in scope as EPIC-01 | P1/P2 priority; screener is live and these bugs silently degrade results for every daily user; BLG-TECH-10 causes majority of US tickers to fail per run | Product Owner | 2026-05-21 |
| SI-03 Red Flag Journal in scope as EPIC-03 | SI-01 shipped v3.8 provides override acknowledgement infrastructure; SI-03 is the natural next step in Arc 5 sequence; M effort; §13 compliant (display-only audit log) | Product Owner; Strategy Rules & System Intent Owner | 2026-05-21 |
| PT-04 Setup Quality Score as conditional scope (EPIC-05) | Gate condition (20+ closed trades) must be confirmed by Product Owner before sprint planning seals; fourth consecutive conditional inclusion — if unmet, recorded as deferred_at_planning | Product Owner | 2026-05-21 |
| Governance patches (EPIC-04) in scope | 2-cycle escalation (DoQ QA enforcement CF-3) must be addressed; CF-4/5 are Head of Specs Team v3.9 targets; BLG-GOV-25 improves planning engine reliability | Head of Specs Team; Director of Quality | 2026-05-21 |
| BLG-OPS-17–24 (cost monitoring suite) excluded | All items gated on 30–60 days operational history; none of these gates are met; deferring to keep sprint scope focused | Product Owner | 2026-05-21 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sprint 1: EPIC-01 (screener fixes) + EPIC-02 (ticker universe) | P1 bug fixes should land first; screener correctness unblocks reliable daily workflow | Product Owner; PMO Lead | 2026-05-21 |
| Sprint 2: EPIC-03 (Red Flag Journal) + EPIC-04 (governance patches) + conditional EPIC-05 | New feature and governance patches have lower urgency than P1 fixes; Sprint 2 allows Red Flag Journal planning to benefit from SI-01 being live in prod | Product Owner | 2026-05-21 |
| Merge order: EPIC-02 → EPIC-01 → EPIC-04 → EPIC-03 | Ticker universe (EPIC-02) has no shared-file risk; screener (EPIC-01) modifies screener batch service; governance (EPIC-04) text-only; Red Flag Journal (EPIC-03) new backend + frontend last | PMO Lead | 2026-05-21 |

### Accepted risks

None — no escalations were raised during this planning cycle.

*(Populate from any Accepted Risk escalations in this cycle. If none: "None")*

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: v3.9 ship — 2026-05-22
Changelog: docs/product/changelog.md#v3.9
Cycle: 2026-05-21__release-v3.9
