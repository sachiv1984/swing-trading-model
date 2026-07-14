**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-14
**Cycle:** 2026-07-14__release-v7.1
**Release:** v7.1
**Design Gate Required:** true

---

# Cycle Summary — Release Planning 2026-07-14__release-v7.1

**Release:** v7.1 — Nightly Backtest Data Integrity
**Roadmap source:** `claude/roadmap/current_roadmap.md` §3, Now horizon (opened rebalance 2026-07-13__scheduled, STEP 8.0 Production Correctness Fast-Track)
**Mode:** standard | **Issues:** none | **Auto-escalate:** true

## Scope

3 EPICs, 7 stories (S2-01–S2-07):
- **EPIC-01 — Nightly Backtest Data Integrity** (ST-01 `BLG-BE-59`, ST-02 `BLG-BE-60`) — mandatory roadmap anchors, both P1.
- **EPIC-02 — Table View Badge Spec Compliance** (ST-03 `BLG-FE-107`) — mandatory anchor, blocked on Design Gate.
- **EPIC-03 — v7.0 Post-Ship Hardening** (ST-04 `BLG-BE-61`, ST-05 `BLG-QA-106`, ST-06 `BLG-SPEC-83`, ST-07 `BLG-SPEC-84`) — capacity-filling, all `Provisional-Target: v7.1`.

## Capacity

Estimated effort 14.0 days (midpoint) against ~12–14 day capacity — **WARN** (tight fit, zero buffer; pessimistic case ~15.5 days). Phasing recommendation on file in `release_plan.md §Capacity Check` — Sprint 1: EPIC-01 + EPIC-02 (~6.0d); Sprint 2 (or defer): EPIC-03 (~8.0d).

## Design Gate

`design_gate_required = true` — 2 items carry observable UI acceptance criteria requiring design-gate classification: ST-03 (`BLG-FE-107`, badge colour/label) and ST-05 (`BLG-QA-106`, UX consistency review sub-item). Run `run design-gate --cycle 2026-07-14__release-v7.1` before `plan sprint`.

## Pre-sprint Planning Required Decisions

The following High-priority decision must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-03] `BLG-FE-107` Table View RISK OFF badge treatment undecided — Design Gate must resolve option (a) spec-compliance fix vs. option (b) formal amber acceptance before EPIC-02 can be sequenced or estimated with confidence — Owner: Head of UX & Design / Head of Specs Team

## Escalations

None raised this cycle. `open_escalations` empty; `deferred_execution_blockers` empty.

## Publish Gate

PASS — `status = Validated`, `publish_eligible = true`. All hard gate conditions met (stage1_readiness, stage3_5_model_integrity, stage5_5_cross_stage_integrity = pass; stage4_5_capacity_check = warn, allowed in standard mode; stage5_7_decision_record_integrity = not_applicable; plan_structured/plan_executable/backlog_committed = true).

## Artefacts Produced

- `claude/cycles/2026-07-14__release-v7.1/run_manifest.md`
- `claude/cycles/2026-07-14__release-v7.1/release_plan.md`
- `claude/cycles/2026-07-14__release-v7.1/stage4_backlog_slice.md`
- `claude/cycles/2026-07-14__release-v7.1/stage4_issue_manifest.json`
- `docs/product/scope/scope--2026-07-14__release-v7.1-nightly-backtest-data-integrity.md`
- `docs/product/decisions/decisions--2026-07-14__release-v7.1.md`
- `claude/backlog/backlog.md` (Release Slice v7.1 section added)
- `claude/roadmap/current_roadmap.md` (execution notes annotation added under §3 v7.1)

## Next Steps

1. `run design-gate --cycle "2026-07-14__release-v7.1"` — resolve RISK-03 (ST-03 badge treatment) and ST-05's UX consistency sub-item.
2. `plan sprint --cycle "2026-07-14__release-v7.1"` — consume the Pre-sprint Required Decisions checklist and the WARN capacity phasing recommendation.
