Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v3.3
Cycle: 2026-05-09__release-v3.3
Last Updated: 2026-05-09

## Release Scope — v3.3 Arc 3 In-Trade Risk Management

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Position Lifecycle Manager (IT-01) — data model + backend state machine + frontend state display on positions page |
| S2-02 | EPIC-02 | Grace Period Decision Support (IT-02) + Stop Management Workflow (IT-03) — backend + frontend for both features |
| S2-03 | EPIC-03 | Research view specification & QA closure — BLG-SPEC-24/25/26 (canonical spec + API contract + provenance), BLG-FE-28 (UX spec), BLG-QA-14/15/16/17 (E2E tests + acceptance protocol + test scenarios + integration tests), BLG-OPS-15 (latency baseline), BLG-SEC-06 (sensitivity classification), BLG-GOV-20 (field extension governance) |
| S2-04 | EPIC-04 | Governance patches + mandatory quick wins — OA-01/02/03/05 (CF-01/02/03) governance patches to execution_prompt + sprint_planning_prompt; BLG-GOV-19 PT-05 §13 review; BLG-FEAT-13 feature flag rollout (mandatory); BLG-FEAT-21 + BLG-FE-30 (abandonment status + badges); BLG-FE-23/24/25/29 (frontend quick wins) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| IT-04 Drawdown-Triggered Review Prompt | Sequenced after Arc 3 foundation; no blocking dependency | v3.4 |
| IT-05 Position Concentration Limits | Sequenced with IT-04 | v3.4 |
| IT-06 Alpaca Paper Trading Integration | §13 review required before pre-alignment | v3.4+ |
| PT-04 Setup Quality Score | Gate not met: 20+ closed trades required | v3.4+ (gate) |
| BLG-FE-26 Research page UX review | P3; no blocking workflow | v3.4 |
| BLG-FE-27 Nav bar redesign | P3 design exploration | Arc 3+ |
| BLG-AI-03 AI Journal quarterly review cadence | Process definition before v3.4 | v3.4 |
| BLG-OPS-13 API performance baseline re-run | Live environment required; ops task | Before next perf review |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-09__release-v3.3
