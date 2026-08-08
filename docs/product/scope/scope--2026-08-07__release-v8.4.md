Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.4
Cycle: 2026-08-07__release-v8.4
Last Updated: 2026-08-08

Superseded by: v8.4 ship — 2026-08-08
Changelog: docs/product/changelog.md#v8.4
Verification report: claude/cycles/2026-08-07__release-v8.4/verification_report.md
Cycle: 2026-08-07__release-v8.4

## Release Scope — v8.4 User-Facing Reporting & Full-Capacity Debt Clearance

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | User-Facing Reporting Enhancement — Avg P&L/Trade column, CSV export trigger-source column (2 stories) |
| S2-02 | EPIC-02 | API Contract & Spec Debt Closure — openapi.yaml structural defect + 7 documentation-drift items (8 stories) |
| S2-03 | EPIC-03 | Backend Engineering Hardening — indexing, resilience, audit-trail, data-dictionary automation (5 stories) |
| S2-04 | EPIC-04 | Frontend Code Health, Accessibility & Security — Dialog audit, token gaps, ESLint, CSP hardening (4 stories) |
| S2-05 | EPIC-05 | Operational Reliability & Cost Monitoring — SI-05 verification, endpoint coverage, CI cache, cost tracking (6 stories) |
| S2-06 | EPIC-06 | QA & Test Infrastructure Hardening — patch-target fix, regression baseline backfill, recurring checks (4 stories) |
| S2-07 | EPIC-07 | Governance Process Integrity — gate-detection procedure, cross-EPIC merge runbook dry-run (2 stories) |

31 stories total.

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-73` (SI-02 frontend build) | Gate not met — 0 closed trades with linked trade_plans as of last live re-check (2026-07-28); no live re-check performed this session | Re-check at next release planning |
| `BLG-FEAT-74` (PO-05 Lightweight Replay Mode) | Gate not met — §13 determinism pre-clearance not yet run; VH effort exceeds single-cycle sizing | Re-check at next release planning |
| `BLG-OPS-51` (claude_audit_log/Supabase log retention extension) | Gate not met — table 6-month-age threshold not reached until ~2026-11 | Re-check once gate date passes |
| Remaining ~55 ungated P3 backlog items not selected this cycle (mostly `BLG-GOV-*` process/checklist items) | Capacity allocated to this cycle's 30-item scope (~28 days, top of confirmed capacity band); deliberately weighted toward execution/debt scope over governance-process scope this cycle per the Skill-Silo rotation guideline (`release_planning_prompt.md §3`) | Next release planning cycle |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-08-07__release-v8.4
