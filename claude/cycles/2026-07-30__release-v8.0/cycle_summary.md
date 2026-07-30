Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Filed
Report Date: 2026-07-30
Cycle: 2026-07-30__release-v8.0
Release: v8.0
Design Gate Required: true

# Cycle Summary — Release Planning v8.0

## Outcome

Release Plan **Validated**, `publish_eligible = true`. Scope: 19 stories across 6 grouped EPICs, backlog-driven (no formal roadmap release section — STEP -1.2 Option (b) equivalence from `2026-07-28__scheduled`), sized to the top of the confirmed ~24-28 day capacity band (~26.25 days midpoint, ~94-109% utilisation) by default, since no explicit user capacity/grouping instruction was given this session. One item (`BLG-OPS-48`) was self-caught and removed from the initial 20-item selection after its real `Gate date: 2026-11-01` was found during write-up — see Lessons Learnt.

## EPICs

| EPIC-ID | Theme | Stories | Owner |
|---------|-------|---------|-------|
| EPIC-01 | Data Model & Spec Integrity | ST-01–ST-03 | Data Model & Domain Schema Owner; Financial Reporting & Records Owner |
| EPIC-02 | Security Hardening | ST-04–ST-09 | Cybersecurity & Trust Lead; Head of Engineering; Head of UX & Design |
| EPIC-03 | QA & Test Infrastructure Hardening | ST-10–ST-12 | Director of Quality; QA Lead; QA & Testing Owner |
| EPIC-04 | Operations & Reliability | ST-13–ST-17 | Infrastructure & Operations Owner; FinOps & Resource Architect |
| EPIC-05 | Frontend Technical Debt | ST-18 | Base44 Frontend Prompt Owner |
| EPIC-06 | Governance & Engineering Process Hardening | ST-19 | Head of Engineering |

## Gate Outcomes

| Gate | Outcome |
|------|---------|
| STEP -1 Preflight | PASS |
| STEP 1 Readiness | pass |
| STEP 3.5 Local Model Integrity | pass |
| STEP 4.5 Capacity Feasibility | pass (~26.25d / ~24-28d band, ~94-109% utilisation) |
| STEP 5.5 Cross-Stage Integrity | pass |
| STEP 5.7 Decision Record Integrity | not_applicable (no escalations raised) |
| Publish Gate | pass — `status = Validated`, `publish_eligible = true` |

## Design Gate

`design_gate_required = true`. EPIC-02 carries two observable UI acceptance criteria (ST-06 keyboard-operable checklist item, ST-07 modal focus trap/restoration). Run `run design-gate --cycle 2026-07-30__release-v8.0` before `plan sprint`.

## Deferred / Excluded This Cycle

- `BLG-OPS-48` — self-caught scope correction; real `Gate date: 2026-11-01` found during write-up, ~3 months past this cycle's date. Not ready.
- `BLG-FEAT-73`/`BLG-FEAT-74` — SI-02 gate NOT MET / §13 pre-clearance not run; standing PO perennial-return disposition, unchanged.
- Arc 5 pre-entry/compliance-gateway UX cluster (12 items) + `BLG-SPEC-35` — all P1-escalated as a value judgment only on 2026-07-27/28; every item's own gate criteria remain unmet.
- ~145 remaining ungated P2/P3 candidates — capacity reached; carried forward as the `v8.1` candidate pool.

## Escalations

None raised this cycle.

## Artefacts Produced

- `claude/cycles/2026-07-30__release-v8.0/run_manifest.md`
- `claude/cycles/2026-07-30__release-v8.0/state.json`
- `claude/cycles/2026-07-30__release-v8.0/release_plan.md`
- `claude/cycles/2026-07-30__release-v8.0/stage4_backlog_slice.md`
- `claude/cycles/2026-07-30__release-v8.0/stage4_issue_manifest.json`
- `claude/cycles/2026-07-30__release-v8.0/backlog_txn.json`
- `claude/cycles/2026-07-30__release-v8.0/roadmap_txn.json`
- `docs/product/scope/scope--2026-07-30__release-v8.0.md`
- `docs/product/decisions/decisions--2026-07-30__release-v8.0.md`
- `claude/cycles/2026-07-30__release-v8.0/cycle_summary.md` (this file)
- `claude/cycles/2026-07-30__release-v8.0/lessons_learnt.md`

## Next Step

`run design-gate --cycle 2026-07-30__release-v8.0`, then `plan sprint --cycle 2026-07-30__release-v8.0`.
