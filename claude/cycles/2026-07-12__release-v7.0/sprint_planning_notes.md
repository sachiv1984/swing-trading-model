**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-13
**Cycle:** 2026-07-12__release-v7.0

# Sprint Planning Notes — 2026-07-12__release-v7.0

## Backlog Slice Source

Original — `claude/cycles/2026-07-12__release-v7.0/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty — no amendment sealed for this cycle).

## Deferred Items

None. All 15 ST items from the authoritative backlog slice (EPIC-01: ST-01..ST-05; EPIC-02: ST-06..ST-12; EPIC-03: ST-13..ST-15) are `include` — within capacity (~9.5 of ~12–14 days), owned, AC-confirmed, design-gate-cleared. See `release_plan.md §Scope → Items explicitly deferred` for backlog items considered and not selected at release planning (`BLG-FEAT-66`, `BLG-FEAT-67`, all SI-02/SI-04/PO-02/Arc-gated items) — out of this routine's scope to revisit.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 (EPIC-01) | None | — | Resolved (lands first) |
| ST-02 (EPIC-01) | ST-01 | Internal (spec-then-implementation) | Resolved |
| ST-03 (EPIC-01) | ST-02 | Internal (same file, RISK-01 sequencing) | Resolved |
| ST-04 (EPIC-01) | ST-02, ST-03 | Internal (coverage requires both badges shipped) | Resolved |
| ST-05 (EPIC-01) | ST-02, ST-03 | Internal (review requires both badges rendered together) | Resolved |
| ST-06 (EPIC-02) | None | — | Resolved (independent) |
| ST-07 (EPIC-02) | None | — | Resolved (independent) |
| ST-08 (EPIC-02) | None | — | Resolved (independent) |
| ST-09 (EPIC-02) | None | — | Resolved (independent) |
| ST-10 (EPIC-02) | None | — | Resolved (independent) |
| ST-11 (EPIC-02) | None | — | Resolved (independent) |
| ST-12 (EPIC-02) | None | — | Resolved (independent) |
| ST-13 (EPIC-03) | None | Internal (soft sequencing before ST-14, same file) | Resolved |
| ST-14 (EPIC-03) | ST-13 | Internal (soft sequencing, `Reports.js` churn avoidance) | Resolved |
| ST-15 (EPIC-03) | None | — | Resolved (independent — position-review UI, not `Reports.js`) |

No circular dependencies. All 7 EPIC-02 items are independent fixes/instrumentation across different files (`reports.md`, `trailing_stop_recommendation_log` table, `DashboardHome.js`/`StrategyBenchmark.js`, `Positions.js`, `GateProgressStrip.js`/`dashboard.md`, `backend/routers/ai.py`, `backend/routers/portfolio_risk.py`) per `release_plan.md §Execution Plan`.

## Execution Sequence

1. EPIC-01 — ST-01 → ST-02 → ST-03 → ST-04 → ST-05 — designated `execution_state.json` owner (first in execution order per `release_plan.md`/`stage4_backlog_slice.md` listing order; also canonical owner of the most heavily shared files, `positions.md` and `PositionCard.js`).
2. EPIC-02 — ST-06..ST-12, no internal sequencing constraint (all independent).
3. EPIC-03 — ST-13 → ST-14 (soft sequencing, same file) → ST-15 may run in any order relative to ST-13/ST-14 (independent file).

All 15 items are `autonomous`-class; no delegated items to sequence ahead/behind.

**Multi-EPIC Execution Notes:** EPIC-01 owns `execution_state.json` (first in execution order). EPIC-02 and EPIC-03 must check for `execution_state.json` existence before creating their own version — if found, read it and append their own EPIC section rather than overwrite.

**Shared file ownership advisory:**
- `docs/specs/frontend/pages/positions.md` — edited by EPIC-01 (ST-01: v2.0→v2.1; ST-05: v2.1→v2.2) **and** independently by EPIC-03 (ST-15: also v2.1→v2.2 per its own design gate artefact). This is a genuine version-number collision risk since both bumps target v2.2 independently. EPIC-01 owns the canonical version (merges first per Merge Order). EPIC-03 must rebase onto `main` after EPIC-01 merges and reconcile/renumber its own edit before finalising ST-15.
- `PositionCard.js` — edited by EPIC-01 (ST-02, ST-03, ST-05) and likely EPIC-03 (ST-15, if review-cadence displays on the Grid View card). EPIC-01 owns the canonical version; EPIC-03 must rebase after EPIC-01 merges.
- `Positions.js` — edited by EPIC-02 (ST-09) and possibly EPIC-03 (ST-15, if displayed in Table View too). EPIC-02 owns the canonical version (merges before EPIC-03 per Merge Order); EPIC-03 must rebase after EPIC-02 merges if it also touches this file.
- `Reports.js` — EPIC-03 only (ST-13, ST-14); no cross-EPIC conflict, internal soft sequencing only.

Full detail: `sprint_backlog.md §Merge Order`.

**Planning-deferred item traceability:** Not applicable this cycle — no ST item from the authoritative backlog slice was excluded from the sealed sprint backlog (all 15 are `include`). No `deferred_at_planning` entries required in `execution_state.json`.

## Delegation Classification Methodology

All 15 items classified `autonomous` per `sprint_planning_prompt.md §3.1` BLG-GOV-72 fast-path and LL-v1.10-P3-3: every item entering this sprint has its design decision fully resolved and locked into an artefact or spec at the design gate (`design_gate.md`, PASSED 2026-07-12 — 10 Design Pre-Approved/Not Applicable, 5 Design Required with all 5 producing a locked `ux_spec.md`/`decision_record.md` before sprint planning). Per BLG-GOV-72: `delegated_frontend` applies "only when the story genuinely cannot be completed by the engine (e.g., new UX design required, external stakeholder input needed, or no locked spec exists)" — none of these conditions hold for any of the 15 items post-design-gate. No override of the default-autonomous classification was applied to any item; no per-item justification for `delegated_*` is therefore required.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — `PositionCard.js`/`positions.md` touched by 3 sequential stories (ST-01, ST-02, ST-03) plus a review (ST-05); mitigated by the execution sequence above (single branch/EPIC, no cross-branch merge risk within EPIC-01 itself). |
| RISK-02 | EPIC-02 (ST-06) | Valid — `reports.md` correction must be precise to avoid repeating the spec/shipped-feature changelog-wording ambiguity that caused the original drift. Mitigation: apply `document_lifecycle_guide.md` conventions carefully, mark corrected sections "Design Only — Implementation Pending". |
| RISK-03 | EPIC-03 (ST-13, ST-14) | Valid — both stories modify `Reports.js`'s P&L views concurrently within the same EPIC/branch. Mitigation: soft-sequence ST-13 before ST-14 (see Dependency Map); no cross-branch conflict since same EPIC. |
| RISK-04 | Release-level (8 of 15 items carry observable UI ACs) | **Resolved** — Design Gate required and now **Passed** (`design_gate.md`, cleared 2026-07-12T23:15:00Z, 15/15 items classified, 0 blocked). No longer a planning-time blocker. Playwright coverage confirmed feasible for every observable AC in this sprint (see per-story `Staging-only ACs: None` fields in `sprint_backlog.md`) — no CLAUDE.md hard-gate deferral to staging sign-off is anticipated. |

## Pre-Sprint Vulnerability Scan

`pip-audit` is not available in this environment (`backend/.venv/bin/python3 -m pip show pip-audit` returned not installed). Per STEP -1 check 6, this is advisory-only and does not block sprint planning. Recommend installing `pip-audit` in `backend/.venv` before Phase 3 execution begins so the scan can run with real results at a later checkpoint (e.g. pre-commit or CI already runs dependency scanning per `claude/system/` CI references — this local pre-sprint check is a defense-in-depth advisory, not the sole gate).

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Confirm 24-hour capture-window default for ST-07's `trailing_stop_recommendation_log` | Product Owner (delegated authority — confirmed at planning) | No |
| Rebase `positions.md`/`PositionCard.js`/`Positions.js` edits in EPIC-03 (ST-15) onto `main` after EPIC-01/EPIC-02 merge | Head of Engineering / Financial Reporting & Records Owner | No — execution-time sequencing note |

No outstanding action is marked `Blocker? Yes`.

## Pre-Sprint Planning Required Decisions (STEP -1 Advisory 5)

`cycle_summary.md ## Pre-sprint Planning Required Decisions` listed one item: `[RISK-04] Design Gate required — 8 of 15 items carry observable UI acceptance criteria — Required: run design-gate --cycle 2026-07-12__release-v7.0 must complete and pass before plan sprint seals — Owner: Head of UX & Design`. **Resolved** — `run design-gate --cycle 2026-07-12__release-v7.0` completed 2026-07-12, `design_gate_status = Passed` confirmed in both `state.json` and `.claude_current_state.json` before this routine began. No unresolved pre-sprint decision remains.

## Hygiene Advisories (non-blocking, STEP -1.7)

Prompt change log gaps detected (current file version exceeds the most recently *dedicated* logged target version — narrative mentions of a filename in another file's change-log row were excluded from this check to avoid false positives):

- ⚠ `roadmap_prompt.md` current v8.7 — last dedicated log entry v8.4→v8.5 (2026-07-09).
- ⚠ `backlog_management_prompt.md` current v1.11 — last dedicated log entry v1.8→v1.9 (2026-06-16).
- ⚠ `release_planning_prompt.md` current v2.42 — last dedicated log entry v2.40→v2.41 (2026-07-06).

Advisory only — does not block sprint planning. Recommend Head of Specs Team backfill the missing `prompt_change_log.md` rows per CLAUDE.md §6.

No `Provisional-Target: Before v7.0 sprint planning` backlog items found in `claude/backlog/backlog.md` — no Pre-Sprint Backlog Advisory section required.

## Carry-Forward Items

Carry-forward items reviewed: 2 items from cycle `2026-07-10__release-v6.9` (`lessons_learnt_closure.md`):

1. `PositionCard.js`'s Grid View still did not render the Trail Stop breach and RISK OFF badges documented in `positions.md` since v6.2 — **directly addressed this cycle**: EPIC-01 (ST-02 RISK OFF badge, ST-03 trailing-stop/breach indicator, ST-04 Playwright parity coverage) closes exactly this gap.
2. v6.9 shipped only its 2 named mandatory items with significant unused capacity headroom — **directly addressed this cycle**: release planning explicitly maximised scope to 15 items (~9.5 of ~12–14 days) per Product Owner scope-maximisation directive (see `cycle_summary.md §Why this release is bigger than v6.9`).

Both prior-cycle carry-forward items are resolved by this sprint's scope; no further action required.
