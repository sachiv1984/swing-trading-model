Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.2
Cycle: 2026-08-04__release-v8.2
Last Updated: 2026-08-05

Superseded by: v8.2 ship — 2026-08-05
Changelog: docs/product/changelog.md#v8.2
Verification report: claude/cycles/2026-08-04__release-v8.2/verification_report.md
Cycle: 2026-08-04__release-v8.2

## Release Scope — v8.2 User-Feature Push (continued) & Full-Capacity Debt Clearance

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | BLG-FEAT-88 — P&L / tax record reconciliation report |
| S2-01 | EPIC-01 | BLG-FE-105 — Compliance Recheck Modal all-pass empty-state design |
| S2-01 | EPIC-01 | BLG-FE-67 — RFJ event type colour palette refinement |
| S2-01 | EPIC-01 | BLG-FE-138 — Trade Plan native form fields weak focus indicator |
| S2-01 | EPIC-01 | BLG-FEAT-86 — Drift-detection metric for the `insufficient_data` streak |
| S2-02 | EPIC-02 | BLG-SEC-27 — Provision a distinct API key for staging |
| S2-02 | EPIC-02 | BLG-OPS-128 — Detect silent staging deploy staleness |
| S2-03 | EPIC-03 | BLG-GOV-160 — File SI-05 Phase 1 30-day effectiveness review record |
| S2-03 | EPIC-03 | BLG-GOV-213 — `velocity_metrics.md` row-count audit |
| S2-03 | EPIC-03 | BLG-GOV-214 — Confirm Arc 5 composite formula accounts for v6.9 recheck events |
| S2-03 | EPIC-03 | BLG-GOV-218 — Rebalance-skip advisory should verify next release is actually scoped |
| S2-03 | EPIC-03 | BLG-GOV-265 — AI vendor Terms-of-Service & data-processing review |
| S2-03 | EPIC-03 | BLG-GOV-269 — Direct-write / governance-bypass pattern tracker |
| S2-03 | EPIC-03 | BLG-GOV-278 — Idea-intake backlog-overlap check effectiveness retrospective |
| S2-03 | EPIC-03 | BLG-GOV-279 — SI-02 production credential provisioning decision |
| S2-03 | EPIC-03 | BLG-GOV-281 — Mandatory §13 boundary pre-check at design gate |
| S2-03 | EPIC-03 | BLG-GOV-283 — Codify a `Last Updated` header-history retention convention |
| S2-03 | EPIC-03 | BLG-GOV-285 — governance_sync.yml auto-close regex fix |
| S2-04 | EPIC-04 | BLG-OPS-116 — Quarterly dependency-upgrade cadence |
| S2-04 | EPIC-04 | BLG-OPS-118 — CI cache tuning to reduce Playwright suite runtime |
| S2-04 | EPIC-04 | BLG-OPS-125 — Automated commit-message format lint |
| S2-05 | EPIC-05 | BLG-QA-126 — Snapshot test for `SystemStatus.js` hardcoded fallback counts |
| S2-05 | EPIC-05 | BLG-SPEC-110 — Reconstruct 13 undocumented `sprint_planning_changelog.md` versions |
| S2-05 | EPIC-05 | BLG-BE-81 — Remove dead-code duplicate `POST /test/endpoints` handler |
| S2-05 | EPIC-05 | BLG-FE-131 — Design-gate checklist addendum for motion/timing-sensitive chart interactions |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate unmet / §13 pre-clearance not run; perennial-return disposition, Option (a), 3rd consecutive cycle | Unscheduled, pending gate clearance or forced disposition at v8.3 |
| Arc 5 UX-prep cluster (BLG-FEAT-44/56, BLG-FE-43/45/54/58/59/62/63/68/69/70/71) | Each item's own Problem statement names a substantive unmet precondition | Unscheduled, pending respective gate clearance |
| BLG-FEAT-45 | Gate clears 2026-08-05, inside the execution window — STEP 1.4b mandates conditional classification for within-sprint date gates | Next cycle, pending gate owner confirmation |
| BLG-BE-24 | Gate: `red_flag_events` table 6+ months old (post 2026-11-22) | Unscheduled, pending gate |
| BLG-OPS-48 | Self-caught during scope write-up: date-gated to 2026-11-01, expressed only inside its `Provisional-Target` field text — missed by the initial scan, caught before commit | ~v4.9, no earlier than 2026-11-01 |
| Remaining ungated P2/P3 candidates not selected this cycle | Capacity — curated highest-value selection made rather than exhaustive fill | v8.3 candidate pool |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-08-04__release-v8.2
