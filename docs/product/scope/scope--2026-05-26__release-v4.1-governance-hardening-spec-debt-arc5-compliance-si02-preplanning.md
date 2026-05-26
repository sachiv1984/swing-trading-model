Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v4.1
Cycle: 2026-05-26__release-v4.1
Last Updated: 2026-05-26

## Release Scope — v4.1 Governance Hardening, Spec Debt, Arc 5 Compliance + SI-02 Pre-Planning

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Governance Prompt Hardening — patch execution_prompt (merge-gate hard gate), sprint_planning_prompt (staging-only AC designation), delivery_verification_prompt (pr_number null guard) |
| S2-02 | EPIC-02 | API Contract Spec Debt Batch 1 — SI-03 Red Flag Journal, SI-01 Pre-Entry Validation, Arc 5 analytics endpoint contracts |
| S2-03 | EPIC-03 | Gemini Thesis API Contract (gate: S2-02 SI-03 closed) |
| S2-04 | EPIC-03 | Arc 5 P&L Compliance Integration — composite score formula + monthly P&L compliance metrics section |
| S2-05 | EPIC-03 | Gemini API daily cost threshold alert via Telegram |
| S2-06 | EPIC-03 | Frontend: Research view signal_type Setup Type column + Arc5ComplianceSection frontend spec |
| S2-07 | EPIC-03 | Staging Verification Bundle — v4.0 deferred staging-only ACs (Arc5ComplianceSection E2E, Gemini staging, ticker validation staging, CI/CD deploy hook) |
| S2-08 | EPIC-04 | SI-02 Pre-Planning — data model gap analysis, §13 evidence criteria, data prerequisite audit, DB query performance assessment |
| S2-09 | EPIC-04 | Security + Governance Patches — Gemini API key scope minimization + STEP 12.1 artefact presence check |
| S2-10 | EPIC-04 | SI-05 Phase 1 roadmap annotation — formal scope annotation for Red Flag + compliance trend delivery |
| S2-11 | EPIC-04 | Operational Reviews — API performance baseline update (v4.0 endpoints), Gemini usage first monthly review, P&L attribution gate check |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| PT-04 (Arc 2 performance analytics) | Gate not met: 20+ closed trades required | v4.x gate-conditional |
| Arc 6 (PS-01 through PS-05) | Gate not met: 50–100+ trades required | Arc 6 horizon |
| BLG-OPS-33 (staging parity audit) | Gate: v4.1 sprint planning complete | v4.2 |
| BLG-GOV-40/42/43/47/48/50/52/53 | Capacity constrained; no blocking dependency | v4.x backlog |
| BLG-FE-45/46/47/49 | Not required for v4.1 objectives | v4.x backlog |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-26__release-v4.1
