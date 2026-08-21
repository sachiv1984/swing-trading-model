**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-21
**Cycle:** 2026-08-21__release-v9.0

# Sprint Planning Notes — 2026-08-21__release-v9.0

## Backlog Slice Source

Original — `claude/cycles/2026-08-21__release-v9.0/stage4_backlog_slice.md`. `amended_backlog_slice_path` is empty in `.claude_current_state.json` and `state.json` — no amendment has sealed for this cycle.

## Carry-Forward Items

3 items from prior cycle `2026-08-17__release-v8.9` (`lessons_learnt_closure.md ## Carry-Forward`), reviewed per §16.8:

| # | Observation | Implication | Relevance to this sprint |
|---|-------------|-------------|---------------------------|
| 1 | Two Phase 4-originated deferred patches crossed the `shared_standards.md §6.4` 2-cycle threshold and are now tracked as `ESC-CLOSE-20260821-01`/`-02` (SLA 2026-08-24). | Confirm Head of Specs Team has dispositioned these before treating as routine carry-forward again. | Not a Sprint Planning action item — tracked for Head of Specs Team; SLA date falls within this sprint's likely execution window, flagged for awareness only. |
| 2 | `velocity_metrics.md`'s header fell out of sync with its table content across 2 consecutive post-ship closures before being caught. | Future post-ship closures should verify header-vs-table consistency before chaining a new entry. | Post-Ship Closure engine concern, not Sprint Planning — noted for downstream awareness. |
| 3 | `post_ship_closure.md` STEP 3.1 has no carve-out for split-achievability stories; one was improvised for `BLG-GOV-264`. | Worth formalising before the next cycle produces a similar case. | Post-Ship Closure engine concern, not Sprint Planning — noted for downstream awareness. |

None of the 3 items require a Sprint Planning action this cycle; all are owned by other engines. Recorded per read protocol.

## Pre-Sprint Backlog Advisory

None. No `claude/backlog/backlog.md` item carries `Provisional-Target: Before v9.0 sprint planning`.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — 0 known vulnerabilities across all 57 resolved dependencies.

## Recurring Endpoint Test Coverage Audit

`python3 scripts/audit_endpoint_test_coverage.py`: **clean** — exit 0. 85 route decorators scanned across 25 router files; 8 documented `KNOWN_GAPS` exclusions; no undocumented gaps.

## Pre-Seal Stale-Feature-Target Check (STEP 3.1, AUD-2026-08-21-011)

All 27 source backlog IDs cross-checked against `claude/backlog/backlog_archive.md`. 5 IDs (`BLG-BE-107`, `BLG-OPS-25`, `BLG-OPS-90`, `BLG-QA-26`, `BLG-QA-81`) appear in archive text, but in every case only as **cross-references from other, already-archived items** (duplicate-consolidation notes, incident-history citations, or a related sub-item's gate-condition update) — none is a record of the item itself, or the specific scope named in its `stage4_backlog_slice.md` acceptance criteria, having already shipped. `BLG-QA-81` was individually re-verified directly in `claude/backlog/backlog.md` (still `Provisional-Target: Unscheduled`, gate criteria cleared, no completion marker). No item reclassified — all 27 remain `include`.

## Delegation Classification

Per §3.1 (BLG-GOV-72 fast-path defaults applied; overrides justified below).

| EPIC | Story | Classification | Justification (only where overriding default-autonomous) |
|------|-------|-----------------|-------------------------------------------------------------|
| EPIC-01 | ST-01 | autonomous | Backend calculation-path fix, no UX change |
| EPIC-01 | ST-02 | autonomous | Logging config change; post-deploy verification is executable by the engine (log inspection), no human decision required |
| EPIC-01 | ST-03 | delegated_decision | AC requires an explicit Product Owner decision on the debrief's data source before implementation |
| EPIC-01 | ST-04 | autonomous | Backend prompt/verification-logic fix, no UX change |
| EPIC-01 | ST-05 | autonomous | Internal code consolidation, regression-verified, no UX change |
| EPIC-02 | ST-06 | autonomous | DB audit/correction via existing regression-tested floor-calculation path; no new UI, no open decision — high-risk (RISK-02) but mechanically defined |
| EPIC-02 | ST-07 | delegated_decision | AC requires an explicit Product Owner decision on setup_type treatment |
| EPIC-02 | ST-08 | autonomous | Concurrency lock, backend-only |
| EPIC-02 | ST-09 | autonomous | Test authoring against existing migrations |
| EPIC-02 | ST-10 | delegated_frontend | Outcome not yet chosen at planning time (FX override field reusing the existing `PositionSizingWidget` pattern, vs. a spec-wording-only fix) — genuinely frontend-visible if the field-add path is taken; conservative classification per LL-v1.10-P3-3 |
| EPIC-02 | ST-11 | autonomous | Additive Playwright coverage of existing rendering, no design decision (BLG-GOV-72 (c) fast-path) |
| EPIC-03 | ST-12 | delegated_backend | Restore drill requires deliberate execution against a live non-production infrastructure target — human-reviewable operational action, not a code change |
| EPIC-03 | ST-13 | autonomous | CI/test-suite authoring and wiring |
| EPIC-03 | ST-14 | autonomous | CI/ops scripting |
| EPIC-03 | ST-15 | delegated_decision | Requires confirming a live value in the Render dashboard (external system, no code-level source of truth) |
| EPIC-03 | ST-16 | autonomous | CI config change, locally testable |
| EPIC-04 | ST-17 | delegated_qa | Protocol document + Playwright coverage explicitly requires QA Lead and Product Owner sign-off per its own AC |
| EPIC-04 | ST-18 | delegated_qa | Visual regression baseline capture requires human visual-correctness confirmation (CLAUDE.md frontend visual-evidence rule) |
| EPIC-04 | ST-19 | autonomous | Pure automated test against known fixtures |
| EPIC-04 | ST-20 | delegated_qa | Audit output requires QA Lead sign-off per its own AC |
| EPIC-04 | ST-21 | autonomous | CI config/scan wiring |
| EPIC-04 | ST-22 | autonomous | CI config/reporting wiring |
| EPIC-05 | ST-23 | autonomous | Internal code review, no UX change |
| EPIC-05 | ST-24 | autonomous | Config measurement and adjustment against an explicit threshold; no open decision beyond the item's own AC |
| EPIC-05 | ST-25 | delegated_decision | Requires comparing live Render billing/usage data (external system) against confirmed limits — FinOps judgment call |
| EPIC-05 | ST-26 | autonomous | Dashboard build sourced from existing, already-collected monthly review data |
| EPIC-05 | ST-27 | delegated_decision | Policy document requires stakeholder agreement (Head of Engineering / FinOps) before it can be considered adopted |

No `delegated_frontend` item this cycle introduces a wholly new page or new user-facing controls beyond ST-10's possible FX field (a reuse of an existing established widget pattern, not a new control class) — LL-v2.0-P4-2's `test_scenarios = "pending"` rule is not triggered.

**LL-v2.2-SP-01 check:** 4 `delegated_decision` items this cycle (ST-03, ST-07, ST-15, ST-25) plus ST-27. None require a HoST design-session artefact — all are data-source/policy/config decisions, not UX design decisions; the design gate already confirmed 0 items require a design artefact (`design_gate.md`: "No design artefacts produced this cycle").

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-05 | ST-01 | Internal (same rebalance-date computation surface) | Resolved — both in EPIC-01, sequenced ST-01 before ST-05 |
| ST-06 | None (hard dependency) | Sequencing preference | Resolved — RISK-02 mitigation calls for sequencing ST-06 first within EPIC-02, not a blocking dependency on another story |

No circular dependencies detected. No other explicit `Depends on` fields present in `stage4_backlog_slice.md`.

## Execution Sequence

1. **EPIC-01** — AI Post-Trade Debrief & Backtest Correctness Follow-Through (leads capacity allocation per `release_plan.md ## Execution Plan`; closes out the live production data-correctness bug)
   1. ST-01 (must precede ST-05)
   2. ST-02, ST-03, ST-04 (no ordering constraint between them)
   3. ST-05 (after ST-01)
2. **EPIC-02** — Live Risk-Management & Trade-Plan Data-Integrity Closure
   1. ST-06 first (RISK-02 — live open-position stop backfill, sequence its regression-tested path early within the EPIC)
   2. ST-07, ST-08, ST-09, ST-10, ST-11 (no ordering constraint between them)
3. **EPIC-03** — Operational Resilience & Deploy-Path Safeguards (no cross-item ordering constraint; autonomous items ST-13/ST-14/ST-16 may proceed ahead of delegated ST-12/ST-15 to unblock delegation early)
4. **EPIC-04** — QA Coverage & Process Hardening (no cross-item ordering constraint; autonomous items ST-19/ST-21/ST-22 may proceed ahead of delegated ST-17/ST-18/ST-20)
5. **EPIC-05** — Backend Architecture & Cost/Capacity Hygiene (no cross-item ordering constraint; autonomous items ST-23/ST-24/ST-26 may proceed ahead of delegated ST-25/ST-27)

Rationale for EPIC order: EPIC-01 leads per the release plan's own explicit statement ("Leads capacity allocation"); EPIC-02 follows immediately given RISK-02's live-data sensitivity; EPIC-03/04/05 have no sequencing constraint between them (Execution Plan: EPIC-03 "None" beyond design-gate-not-required note, EPIC-04 same, EPIC-05 "None") and are ordered by their existing EPIC numbering.

## Multi-EPIC Execution Notes (Required — 5 EPICs in scope)

**`execution_state.json` owner: EPIC-01** (first in execution order). All other EPIC branches (EPIC-02 through EPIC-05) must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

**Shared file ownership advisory:** No cross-EPIC shared source files identified this cycle. Each EPIC's scope occupies a distinct domain (EPIC-01: `production_strategy.py`/`backend/services/backtest_rule_service.py`/debrief service; EPIC-02: `positions`/`trade_plans` table logic; EPIC-03: `deploy.yml`/staging CI; EPIC-04: QA docs/Playwright/CI scan config; EPIC-05: DB pool config/Render config/dependency policy). `execution_state.json` itself is the one file all 5 EPICs write to — governed by the owner-EPIC rule above, not a "shared file" in the merge-order sense. `data_model.md` may be touched by EPIC-02 alone if ST-07's decision surfaces a schema change (per `release_plan.md ## Integrity Validation`); no other EPIC is expected to touch it this cycle — if that changes during execution, re-apply CLAUDE.md §8's cross-EPIC conflict resolution procedure.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01, ST-05) | Valid — mitigation (regression test before changing production behaviour; verify consolidation against a fixed historical run) unchanged since release planning, not yet materialised |
| RISK-02 | EPIC-02 (ST-06) | Valid — mitigation (apply only via existing `calculate_trailing_stop()` floor logic, no bespoke script) unchanged since release planning, not yet materialised |
| RISK-03 | EPIC-03 (ST-13, ST-14) | Valid — mitigation (confirm each check fails correctly on a deliberately-broken dry run before enabling as blocking) unchanged since release planning, not yet materialised |
| RISK-04 | EPIC-04 | Valid — no material risk (additive test/audit/documentation scope only) |
| RISK-05 | EPIC-05 (ST-24) | Valid — mitigation (measure before adjusting, configuration-only change) unchanged since release planning, not yet materialised |

No multi-vehicle fix-choice risk (§5.3 LP-14 check) — no risk register item names two or more alternative fix vehicles requiring a pick-one decision at execution kickoff.

## Staging-Only AC Advisory (informs STEP 6.2 seal gate)

The following stories carry at least one AC that CI cannot verify — live external system state, a deliberate staging/infra drill, or a production invocation. Populated into each story's `**Staging-only ACs:**` field in `sprint_backlog.md`:

| Story | Staging-only AC(s) |
|-------|----------------------|
| ST-02 | "A real post-deploy production invocation confirms at least the `si05_digest_service.py` duration line is now captured in Render logs" |
| ST-06 | "Live-DB query confirms the count of open profitable positions with `current_stop < entry_price`, before and after correction" |
| ST-12 | "One full restore drill performed against a non-production target confirming the procedure works" |
| ST-13 | "Confirmed to fail correctly on a deliberately-broken staging deploy (dry run)" |
| ST-15 | "Production `PUBLIC_URL` dashboard value confirmed one way or the other, documented in this item's resolution" |
| ST-24 | "Current concurrent connection usage measured and compared against the configured pool size" |
| ST-25 | "Current Render service tier cost/limits compared against actual measured usage since v6.8" |

None of these are frontend-observable-UI ACs (CLAUDE.md's Playwright-or-staging-signoff rule does not apply to them) — they are backend/infra/ops evidence gaps CI structurally cannot close. Per-story backlog-filing obligations (if any of these are deferred past this sprint's PR) apply at execution time per CLAUDE.md §2.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| None — all acceptance criteria, estimates, and dependencies were fully defined in `stage4_backlog_slice.md`/`release_plan.md`; no `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders arose. | — | No |
