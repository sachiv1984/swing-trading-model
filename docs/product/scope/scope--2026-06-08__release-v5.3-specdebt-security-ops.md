Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v5.3
Cycle: 2026-06-08__release-v5.3
Last Updated: 2026-06-08

## Release Scope — v5.3 Spec Debt, Security Hardening & Ops Governance

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | BLG-SPEC-53 — Contract gap resolution plan for SPEC-49–52 |
| S2-02 | EPIC-01 | BLG-SPEC-54 — openapi.yaml completeness audit vs all 50 routes |
| S2-03 | EPIC-01 | BLG-QA-51 — QA acceptance criteria for SPEC-49–52 contract stories |
| S2-04 | EPIC-01 | BLG-SPEC-49 — GET /ai/journal-summary/history contract + openapi.yaml |
| S2-05 | EPIC-01 | BLG-SPEC-50 — GET /analytics/compliance-metrics contract + openapi.yaml |
| S2-06 | EPIC-01 | BLG-SPEC-51 — GET /news/{ticker} contract + openapi.yaml |
| S2-07 | EPIC-01 | BLG-SPEC-52 — Watchlist endpoint contracts + openapi.yaml + test.py |
| S2-08 | EPIC-02 | BLG-BE-35 — POST /digest/si05/send API key authentication |
| S2-09 | EPIC-02 | BLG-OPS-57 — SI-05 Telegram delivery failure alerting |
| S2-10 | EPIC-02 | BLG-OPS-58 — CI secret scanning gate |
| S2-11 | EPIC-03 | LL-v5.2-P4-01 — qa_evidence_template.md signer format note (CF-1) |
| S2-12 | EPIC-03 | LL-v5.2-P4-02 — execution_prompt.md STEP 5.3A SSR sub-step (CF-2) |
| S2-13 | EPIC-03 | BLG-GOV-107 — SI-02 frontend activation criteria precision |
| S2-14 | EPIC-03 | BLG-GOV-108 — AI model pin update policy |
| S2-15 | EPIC-03 | BLG-GOV-109 — AI audit log retention policy |
| S2-16 | EPIC-03 | BLG-GOV-110 — Arc 4 trade_plan data completeness audit |
| S2-17 | EPIC-03 | BLG-GOV-104 — strategy_rules.md §11 parameter validation |
| S2-18 | EPIC-04 | BLG-QA-52 — Tax year P&L boundary edge case validation |
| S2-19 | EPIC-04 | BLG-QA-53 — SI-05 digest Playwright E2E coverage |
| S2-20 | EPIC-04 | BLG-QA-54 — Playwright coverage matrix update post-v5.2 |
| S2-21 | EPIC-04 | BLG-FE-66 — Red Flag Journal post-launch UX review document |
| S2-22 | EPIC-04 | BLG-FE-67 — BLG-FE-64 visual design review scope definition |

**Conditional scope (gates must clear before sprint planning seals):**

| S2-ID | Gate | Item |
|-------|------|------|
| S2-C1 | Before 2026-07-01 | BLG-GOV-113 — SI-05 effectiveness review protocol |
| S2-C2 | Before 2026-07-01 | BLG-GOV-114 — si05_digest_log schema validation |
| S2-C3 | 2026-06-21 | BLG-FE-64 — RFJ visual design review pre-brief |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-106 | Pre-sprint planning OA (PT-04 trade count gate check) | Before sprint planning seals |
| BLG-GOV-111 | Resolved inline: design gate pre-assessment complete (NOT REQUIRED) | Done |
| BLG-GOV-105 | Provisional-Target: Unscheduled; Arc 6 not yet on Next horizon | Future |
| BLG-GOV-112 | Gate: 2026-07-04 effectiveness review (post-sprint) | v5.4 |
| BLG-OPS-59 | Gate: ~2026-07-04 (4 weeks production operation) | v5.4 |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-06-08__release-v5.3
