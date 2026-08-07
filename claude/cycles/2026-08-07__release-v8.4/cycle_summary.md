Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Filed
Report Date: 2026-08-07
Cycle: 2026-08-07__release-v8.4
Release: v8.4
Design Gate Required: true

# Cycle Summary — Release Planning v8.4

## Outcome

Release Plan **Validated**, `publish_eligible = true`. Scope: 31 stories across 7 grouped EPICs, backlog-driven (no formal roadmap release section — STEP -1.2 Option (b) equivalence from `2026-07-28__scheduled`, same decision already relied on by every release since `v8.0`), sized to ~27.75 days midpoint (~99-115% utilisation, top of band) against the confirmed ~24-28 day capacity band. Explicit user instruction this session: **"Use full capacity and prioritise user features."** Capacity sized to the top of the band accordingly; scope led by the 2 genuinely user-facing items available in the ungated backlog pool (`BLG-FE-141`, and `BLG-FEAT-78` found via a self-caught gate correction), with the remaining 29 stories weighted toward execution/debt scope over governance-process scope.

## EPICs

| EPIC-ID | Theme | Stories | Owner |
|---------|-------|---------|-------|
| EPIC-01 | User-Facing Reporting Enhancement | ST-01, ST-31 | Financial Reporting & Records Owner |
| EPIC-02 | API Contract & Spec Debt Closure | ST-02–ST-09 | API Contracts & Documentation Owner; Data Model & Domain Schema Owner |
| EPIC-03 | Backend Engineering Hardening | ST-10–ST-14 | Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; AI Compliance & Governance Officer |
| EPIC-04 | Frontend Code Health, Accessibility & Security | ST-15–ST-18 | Head of Engineering; Frontend Specifications & UX Documentation Owner; Cybersecurity & Trust Lead |
| EPIC-05 | Operational Reliability & Cost Monitoring | ST-19–ST-24 | Infrastructure & Operations Owner; FinOps & Resource Architect |
| EPIC-06 | QA & Test Infrastructure Hardening | ST-25–ST-28 | QA & Testing Owner; Director of Quality; Financial Reporting & Records Owner; Metrics Definitions & Analytics Owner |
| EPIC-07 | Governance Process Integrity | ST-29, ST-30 | Head of Specs Team; Head of Engineering |

*(ST-31 numbered out of sequence — a late-breaking addition found via a self-caught gate correction after the initial STEP 2 numbering pass; see `run_manifest.md`.)*

## Gate Outcomes

| Gate | Outcome |
|------|---------|
| STEP -1 Preflight | PASS |
| STEP 1 Readiness | pass |
| STEP 3.5 Local Model Integrity | pass |
| STEP 4.5 Capacity Feasibility | pass (~27.75d / ~24-28d band, ~99-115% utilisation, top of band) |
| STEP 5.5 Cross-Stage Integrity | pass |
| STEP 5.7 Decision Record Integrity | not_applicable (no escalations raised) |
| Publish Gate | pass — `status = Validated`, `publish_eligible = true` |

## Design Gate

`design_gate_required = true`. `ST-01` (`BLG-FE-141`, new visible table column) and `ST-16` (`BLG-FE-140`, visible colour-token fix) both carry observable UI acceptance criteria. Run `run design-gate --cycle 2026-08-07__release-v8.4` before `plan sprint`.

## Deferred / Excluded This Cycle

- `BLG-FEAT-73`/`BLG-FEAT-74` — remain gate-blocked (parked at `v8.3`); no live gate re-check performed this session, last confirmed unmet 2026-07-28. Neither in `returned_to_backlog` status from `v8.3`, so no fresh Perennial-Return Check disposition required.
- `BLG-OPS-51` — checked and confirmed still gated (`claude_audit_log` 6-month-age threshold, clears ~2026-11-22).
- Remaining ~55 ungated P3 backlog items not selected this cycle (mostly `BLG-GOV-*` process/checklist items) — capacity reached at ~28 days; deliberately weighted away from governance-process scope this cycle per the Skill-Silo rotation guideline.

## Promoted This Cycle

- `BLG-FEAT-78` (Trade-tag/trigger-source column, tax-year P&L CSV export) — **self-caught gate correction**: gate condition (`BLG-FE-116` ships) confirmed met (`BLG-FE-116` shipped v7.5, retired 2026-07-20); the item's `Gate criteria` field was never updated after shipping. Corrected in `backlog.md` and promoted into scope (EPIC-01/ST-31) — a 2nd genuine user-facing item this cycle.

## Escalations

None raised this cycle.

## Advisory Findings (surfaced, not blocking)

- **Thin user-feature pool persists:** even after the `BLG-FEAT-78` gate correction, only 2 of 31 stories are genuine build-and-ship user features. All larger roadmap-flagship features (`BLG-FEAT-73`/`74`/`76` and the dependent Arc 5/Arc 4 cluster) remain gate-blocked. This is the same pattern documented at every release since `v8.0` — see `run_manifest.md §STEP 2` for full detail.
- **Scan-window artifact self-corrected:** this session's own ad hoc gate-verification script mis-attributed a neighbouring item's `Gate criteria` line to `BLG-QA-110` (which has no gate at all) due to a fixed-line-count read window. `BLG-GOV-286` (in this cycle's scope, ST-29) has had its acceptance criteria extended to explicitly cover this failure mode alongside the 3 previously-known ones.
- **Skill-Silo rotation applied:** most recent rebalance (`2026-07-28__scheduled`) reported a 2nd consecutive worsening Skill-Silo reading (65.8%). This cycle's scope is accordingly weighted toward execution/debt (only 2 of 31 stories are governance-process-shaped: `BLG-GOV-286`, `BLG-GOV-212`).

## Artefacts Produced

- `claude/cycles/2026-08-07__release-v8.4/run_manifest.md`
- `claude/cycles/2026-08-07__release-v8.4/state.json`
- `claude/cycles/2026-08-07__release-v8.4/release_plan.md`
- `claude/cycles/2026-08-07__release-v8.4/stage4_backlog_slice.md`
- `claude/cycles/2026-08-07__release-v8.4/stage4_issue_manifest.json`
- `claude/cycles/2026-08-07__release-v8.4/backlog_txn.json`
- `claude/cycles/2026-08-07__release-v8.4/roadmap_txn.json`
- `docs/product/scope/scope--2026-08-07__release-v8.4.md`
- `docs/product/decisions/decisions--2026-08-07__release-v8.4.md`
- `claude/cycles/2026-08-07__release-v8.4/cycle_summary.md` (this file)
- `claude/cycles/2026-08-07__release-v8.4/lessons_learnt.md`

## Next Step

`run design-gate --cycle 2026-08-07__release-v8.4`, then `plan sprint --cycle 2026-08-07__release-v8.4`.
