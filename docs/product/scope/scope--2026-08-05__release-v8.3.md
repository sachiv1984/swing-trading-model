Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v8.3
Cycle: 2026-08-05__release-v8.3
Last Updated: 2026-08-05

## Release Scope — v8.3 Operational Reliability & Debt Clearance

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Operational Reliability & Security — SI-05 digest pipeline fix + alerting, staging/production key-distinctness check, Gemini key rotation runbook |
| S2-02 | EPIC-02 | Backend Engineering Hardening — index audit, Alpaca backoff audit, canonical position-state enum, error-envelope conformance, retry/backoff resilience fixes |
| S2-03 | EPIC-03 | Frontend & Design-System Debt — shared modal shell/confirmation components, loading-skeleton pattern, theme-compliance prompt section, AI disclaimer extraction |
| S2-04 | EPIC-04 | QA & Spec Debt — Watchlist Playwright coverage, OpenAPI drift sweeps, DoQ staleness lint, form-validation-message spec, deprecation-window policy |
| S2-05 | EPIC-05 | Governance Process — release-planning prompt simplification, §13 re-attestation cadence, SI-02 gate threshold review, change-log ordering fix, cross-role workload check |
| S2-06 | EPIC-06 | Product Retrospective — Monthly P&L 3-month usage format review |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate unmet / §13 pre-clearance not run; STEP 1.4a.1 mandatory sunset trigger fired this cycle — Product Owner disposition Option (b), parked | Unscheduled, pending gate clearance or a materially new gate-clearance path |
| Arc 5 UX-prep cluster (11 items) | Dependent on the now-parked BLG-FEAT-73 SI-02 UX surface; individual unmet preconditions | Unscheduled |
| BLG-GOV-74 | Gate date 2026-08-29, outside this cycle's execution window | v8.3+ (first cycle on/after 2026-08-29) |
| BLG-BE-24 | Gate: `red_flag_events` table 6+ months old (post 2026-11-22) | Unscheduled |
| Remaining ungated P2/P3 candidates | Capacity — curated selection, not exhaustive fill | v8.4 candidate pool |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-08-05__release-v8.3
