**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-04
**Cycle:** 2026-09-03__release-v9.1

# Sprint Planning Notes — 2026-09-03__release-v9.1

## Backlog Slice Source

Original — `claude/cycles/2026-09-03__release-v9.1/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in both `.claude_current_state.json` and `state.json` — no amendment sealed for this cycle).

## Carry-Forward Items

Reviewed `claude/cycles/2026-08-21__release-v9.0/lessons_learnt_closure.md` (most recently completed cycle, `post_ship_complete = true`) for a `## Carry-Forward` section: none present. No carry-forward items from prior cycle.

## Deferred Items

None. All 41 items in the authoritative backlog slice enter this sprint — no `defer` classification was needed at STEP 3.1 (all items confirmed ungated, owned, capacity-fitting, and design-gate-cleared prior to this routine).

Items deferred earlier, at release planning (never entered the backlog slice, so not re-recorded here as sprint-level deferrals): `BLG-FEAT-92`, `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-GOV-105`, `BLG-GOV-315` — see `release_plan.md ## Scope` "Items explicitly deferred".

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-25 | ST-24 | Internal (same file, `trade_plan.md`) | Resolved — sequence ST-24 before ST-25 within EPIC-04 to avoid an in-EPIC edit collision on §5.1 vs. the new baseline subsection |
| ST-09..ST-11 | ST-08 | Internal (same EPIC) | Resolved — release plan's explicit sequencing constraint: ST-08 (npm build regression) must land first within EPIC-02 as a currently-reproducible build-breaking bug |

No cross-EPIC dependencies identified. No circular dependencies. No external (delegated third-party) or spec-lock dependencies beyond the design gate (already `Passed` for the full cycle at planning time).

## Delegation Class Assignment

Default `autonomous` applied per `sprint_planning_prompt.md` §3.1 BLG-GOV-72 fast-path (accessible-name/label fixes, refactors with unchanged Playwright coverage, and locked-spec-conformant additions) and LL-v1.10-P3-3 (existing-behaviour refactors). 3 items require `delegated_decision` — all for the same root cause: `execution_prompt.md §7`'s Write Scope Restriction explicitly excludes `claude/strategy/strategy_rules.md` and `claude/roadmap/*` from Sprint Execution's write scope ("Must not modify... `claude/roadmap/*`... `claude/strategy/strategy_rules.md`").

| Item | Delegation Class | Justification |
|------|------------------|----------------|
| ST-21 (BLG-GOV-311) | `delegated_decision` | Edits `claude/strategy/strategy_rules.md` §13.5 roster — outside standard Sprint Execution write scope. Already flagged in `release_plan.md ## Execution Plan` RISK-04; route through delegated/agent-mediated Strategy Rules & System Intent Owner sign-off per `execution_prompt.md` §5.3. |
| ST-26 (BLG-GOV-264) | `delegated_decision` | Creates `claude/roadmap/displacement_debt_register.md` — outside standard Sprint Execution write scope (`claude/roadmap/*`). Flagged directly in `stage4_backlog_slice.md`'s own item note and carried via `ESC-EXEC-20260818-02`; route through delegated/agent-mediated PMO Lead / Head of Specs Team write authority. |
| ST-34 (BLG-SPEC-101) | `delegated_decision` | **Planning-time catch — not named in `release_plan.md`'s risk register.** Adds a worked example to `claude/strategy/strategy_rules.md` — same restricted-file class as ST-21/RISK-04 (`execution_prompt.md §7`). Route through the identical delegated/agent-mediated Strategy Rules & System Intent Owner sign-off pattern as ST-21. |

All other 38 items: `autonomous`. Per LL-v2.2-SP-01, checked all 3 `delegated_decision` items for a HoST design session or equivalent artefact — none of the 3 involve a UX/design decision (all are write-scope authority issues, not design decisions), so the HoST-design-artefact check does not apply; no advisory needed.

## Execution Sequence

Merge order (per `release_plan.md ## Execution Plan` sequencing constraints — EPIC-01 sequenced first as the only EPIC with observable UI ACs):

1. **EPIC-01 — Frontend Accessibility & UI Consolidation** (ST-01 → ST-07; design gate already `Passed` for full cycle, no residual blocker)
2. **EPIC-02 — Backend Reliability & Technical Debt** (ST-08 first within EPIC per release plan constraint, then ST-09 → ST-10 → ST-11)
3. **EPIC-03 — QA & Test Coverage** (ST-12 → ST-18; no design gate required, no sequencing constraint)
4. **EPIC-04 — Governance Process Debt & Overdue Dispositions** (ST-19 → ST-20 → ST-21 → ST-22 → ST-23 → ST-24 → ST-25 → ST-26 → ST-27 → ST-28; ST-24 before ST-25 per Dependency Map)
5. **EPIC-05 — Spec & Knowledge Debt / AI Governance Register** (ST-29 → ST-41; no internal sequencing constraint)

### Multi-EPIC Execution Notes

**`execution_state.json` owner:** EPIC-01 (first in execution order). EPIC-02/03/04/05 branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their own EPIC section rather than overwrite.

**Shared file ownership advisory:**

| Shared file | EPICs touching it | Ownership / rebase note |
|-------------|--------------------|--------------------------|
| `claude/strategy/strategy_rules.md` | EPIC-04 (ST-21) and EPIC-05 (ST-34) | Both edits are additive (§13.5 roster row; worked example section) and target different sections — no line-level collision expected, but EPIC-05 (merging later, per merge order) must rebase onto `main` after EPIC-04 merges before finalising ST-34, per CLAUDE.md §8 step 1. Both route through the same delegated Strategy Rules & System Intent Owner authority — coordinate so the two edits are not made concurrently against a stale base. |
| `trade_plan.md` | EPIC-04 only (ST-24, ST-25) | No cross-EPIC conflict; internal sequencing only (see Dependency Map). |

No other cross-EPIC shared-file collisions identified — EPIC-01's frontend/spec surface (`tests/e2e/accessibility-axe-scan.spec.js`, `PositionSizingWidget.js`/`WhatIfSizingPreview.js`, `positions.md`/`trade_history.md`/`red_flag_journal.md`), EPIC-02's backend surface (`sector_lookup`, `analytics.py`/`digest.py`, `package.json`/lockfile), EPIC-03's QA surface (`Arc5ComplianceSection` tests, DEV-* index), and EPIC-05's remaining spec/register surface (`design_system.md`, AI touchpoint register, `.claude_current_state.json` schema additions via `roadmap_prompt.md`) do not overlap with each other or with EPIC-04 beyond the table above.

## Planning-Deferred Item Traceability

No item in the authoritative backlog slice is excluded from the sealed sprint backlog — all 41 items enter the sprint. No `status: deferred_at_planning` entries are needed in `execution_state.json` at initialisation.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — design gate scoped `design_gate_required: true` and has cleared (`design_gate.md`, `Passed`, 2026-09-03); each fix's AC (KNOWN_VIOLATIONS entry removal) is Playwright-verifiable in CI |
| RISK-02 | EPIC-02 (ST-11, BLG-BE-110) | Valid — structural move only, no query rewrite; full existing test suite for `analytics.py`/`digest.py` must pass unchanged per the item's own AC |
| RISK-03 | EPIC-03 | Valid — no material risk, additive test/audit/documentation scope only |
| RISK-04 | EPIC-04 (ST-21, BLG-GOV-311) | Valid — mitigation (delegated/agent-mediated Strategy Rules & System Intent Owner sign-off) confirmed applicable at planning; **extended informally to ST-34 (EPIC-05) at this planning pass — see Delegation Class Assignment** |
| RISK-05 | EPIC-05 | Valid — no material risk, documentation/register/retrospective scope only |

No risk has materialised since release planning. No multi-vehicle fix-choice risk (no risk register item names alternative fix vehicles this cycle) — the Multi-vehicle fix-choice risk check does not apply.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — no known vulnerabilities across all 58 resolved dependencies.

## Endpoint Test Coverage Audit (STEP -1.8)

`python3 scripts/audit_endpoint_test_coverage.py`: **clean** — 85 route decorators scanned across 25 router files; 8 documented `KNOWN_GAPS` exclusions; no undocumented gaps. Exit 0.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v9.1 sprint planning`: none found. No advisory items.

## Prompt Change Log Gap Hygiene Advisory

Full date-scan method applied (`shared_standards.md §7`) across all Class 6 prompt files with a `**Version:**` header. One genuine gap found:

> ⚠ **Prompt change log gap:** `OPERATIONAL_GUIDE.md` current v4.171 — last standalone `prompt_change_log.md` row v4.170 (2026-08-21). The v4.171 bump (2026-09-03, from `execution_prompt.md` v3.70→v3.71 and `post_ship_closure.md` v2.30→v2.31, post-ship closure `2026-08-21__release-v9.0` outstanding-actions resolution) is recorded in `OPERATIONAL_GUIDE.md`'s own internal Change Log table (line 1500) but was never appended as its own row to `claude/system/prompt_change_log.md`. Add a prepended row per CLAUDE.md §6 step 4.

All other Class 6 files checked (`amendment_cycle_prompt.md`, `backlog_management_prompt.md`, `delivery_verification_prompt.md`, `design_gate_prompt.md`, `execution_prompt.md`, `idea_intake_prompt.md`, `ideas_housekeeping_prompt.md`, `lessons_learnt_prompt.md`, `post_ship_closure.md`, `release_planning_prompt.md`, `roadmap_management_prompt.md`, `roadmap_prompt.md`, `shared_standards.md`, `sprint_planning_prompt.md`) confirm current header version matches the latest-dated `prompt_change_log.md` row for that file. Advisory only — does not block sprint planning; recommend filing as a `groom backlog`/Head of Specs Team follow-up.

## Capacity WARN Acknowledgement

Not applicable — capacity check outcome is `pass`, not `warn` (27.50d within the confirmed 24–28d band). See `sprint_capacity.md §Minimum Capacity Buffer Floor` for the separate (non-WARN) 95%-buffer-floor advisory and its Product Owner acknowledgement.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| File `OPERATIONAL_GUIDE.md` v4.171 prompt-change-log gap row | Head of Specs Team | No — advisory only |
| Coordinate ST-21/ST-34 `strategy_rules.md` edits to avoid concurrent-stale-base risk (rebase after EPIC-04 merges) | PMO Lead / Strategy Rules & System Intent Owner | No — advisory only |
