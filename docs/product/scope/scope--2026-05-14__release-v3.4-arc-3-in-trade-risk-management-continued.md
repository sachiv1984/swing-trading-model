Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.4
Cycle: 2026-05-14__release-v3.4
Last Updated: 2026-05-14

**Superseded by:** v3.4 ship — 2026-05-14
**Changelog:** docs/product/changelog.md#v3.4
**Verification report:** claude/cycles/2026-05-14__release-v3.4/verification_report.md
**Cycle:** 2026-05-14__release-v3.4

## Release Scope — v3.4 Arc 3 In-Trade Risk Management (continued)

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Arc 3 Frontend Completion — IT-01/02/03 frontend (position lifecycle badge, grace period alert card, stop trail guided panel). UX specs exist from v3.3 design gate. Playwright E2E scenarios required (TEST-GAP-EPIC-01/02-v33). |
| S2-02 | EPIC-02 | IT-04 Drawdown-Triggered Review Prompt — backend drawdown calculation + configurable threshold; frontend structured review prompt. §13 COMPLIANT. |
| S2-03 | EPIC-02 | IT-05 Position Concentration Limits — backend single-position heat % and sector concentration; frontend warning on threshold breach. |
| S2-04 | EPIC-03 | Frontend Quick Wins — BLG-FE-23 (UK suffix), BLG-FE-24 (negative earnings days), BLG-FE-25 (signals page default), BLG-FE-29 (watchlist research status), BLG-FE-30 (trade plan status badges), BLG-FEAT-21 frontend (abandonment UI). |
| S2-05 | EPIC-04 | Spec, QA & Documentation Debt — BLG-FE-31 (research view component library), BLG-FE-22 (screener morning routine UX spec), BLG-SPEC-28 (trade_plan.md §6.2), BLG-QA-18 (screener accuracy test protocol), BLG-AI-03 (AI journal review cadence). |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| IT-06 Alpaca Paper Trading | §13 review gate not cleared | v3.5+ |
| PT-04 Setup Quality Score | Gate: 20+ closed trades; not yet met | Arc 4 context |
| BLG-FE-26 Research page UX review | Design gate for v3.4 will address; P3 | v3.4 design gate phase |
| BLG-FEAT-20 Net-of-costs tracking | Low TTV; Arc 3/4 data model sequencing | Arc 3/4 context |
| BLG-OPS-13 API performance baseline | Requires live environment + human coordination; P3 | Next operational review |
| BLG-GOV-21 Arc 4 data requirements | Before Arc 4 planning — not yet | Before Arc 4 planning |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-14__release-v3.4
