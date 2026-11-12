# Sprint Planning Notes — 2026-11-11__release-v9.17

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-12
**Cycle:** 2026-11-11__release-v9.17

## Backlog Slice Source

Original: `claude/cycles/2026-11-11__release-v9.17/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-01, ST-03/ST-04, ST-06, ST-07 and ST-14; no scope change). No amendment (`amended_backlog_slice_path` empty).

## Preflight Record

- Lifecycle guard: `Design_Gate_Passed` → valid entry state. No `Amendment_In_Progress`.
- Release plan `state.json`: `status = Published`, `publish_eligible = true`, `open_escalations` empty, `deferred_execution_blockers` empty.
- Design gate: `design_gate_required = true`, `design_gate_status = Passed` ✅ (2026-11-11T21:25:20Z). Entered from `Design_Gate_Passed`, so the bypass audit is skipped.
- Files and roles: the slice holds 7 EPICs / 20 ST items. This is a schema v2 cycle: the capacity check and execution plan live in `release_plan.md`, so `stage4_5_capacity_check.md`/`stage3_execution_plan.md` are not expected. All five §4 role charters are present; `lessons_learnt_prompt.md` is present; the write test passed and was cleaned up.
- Branch: the session started on `governance/2026-11-11-release-v9.17`. That branch was already fully merged to `main` (PR #2235, no commits ahead of `origin/main`), so the engine switched to `main` and fast-forwarded before STEP 0.
- Open root escalations: `ESC-EXEC-20260910-01` (Deferred, `blocks_execution: false`). Not a blocker for this sprint.

## Pre-Sprint Required Decisions

| Decision | Owner | Outcome |
|----------|-------|---------|
| RISK-05 (1): ST-12 acknowledgement storage: (a) clear on change or (b) snapshot-bound (`trade-plan-found-defects/decision_record.md` §2.2) | Strategy Rules & System Intent Owner | **Resolved 2026-11-12: option (a), clear on change** (the user, in session). ST-12 deletes option (b) from `trade_plan.md` §5e. |
| RISK-05 (2): ST-19 2R Exit Zone threshold: (a) add to `strategy_rules.md` §11 or (b) reword without a number (`positions-decision-first/decision_record.md` §7) | Strategy Rules & System Intent Owner | **Resolved 2026-11-12: option (b), reword without a number** (the user, in session). There is no case (c) write. ST-19 deletes the option (a) tooltip row from `positions.md`. |
| RISK-02: ST-08 sweep boundary | PMO Lead; Product Owner | **Resolved 2026-11-12:** all of `src/pages/`, plus components that fail axe on a routed page in the light theme. The component-only remainder is filed as **BLG-FE-288**. |

## Carry-Forward Items

Carry-forward items reviewed: 4 items from cycle `2026-11-06__release-v9.16` (`lessons_learnt_closure.md ## Carry-Forward`).
1. Five P2 found defects: all seated (ST-11 `BLG-BE-211`, ST-12 `BLG-FE-278`, ST-13 `BLG-FE-281`, ST-14 `BLG-FE-282`, ST-15 `BLG-OPS-217`).
2. Phase 3 P3 items: seated by `release_planning_prompt.md` v2.74 §1.4c step 1b (ST-02–ST-08), with no override.
3. Roadmap inputs (`governance_overhead_audit_2026-11-02.md`, `BLG-GOV-408`): a `run roadmap --reason "scheduled"` action, not a sprint item. Still open; advisory.
4. `BLG-FE-254` Stops moved group: seated with `BLG-BE-205` (EPIC-04, ST-09 → ST-10).

## Pre-Sprint Vulnerability Scan

pre-sprint pip-audit: clean. `pip-audit` 2.10.1 run via the project virtualenv (`backend/.venv/bin/pip-audit -r backend/requirements.txt --format=json`; the system `pip-audit` binary is not installed): 53 dependencies scanned, 0 known vulnerabilities. Trend log row appended to `docs/ops/pip_audit_trend_log.md`.

## Pre-Sprint Endpoint Coverage Audit

pre-sprint endpoint coverage audit: clean. `scripts/audit_endpoint_test_coverage.py` exit 0: 94 route decorators across 27 router files; 8 documented `KNOWN_GAPS`; no undocumented gaps.

## Hygiene Advisories

- **Prompt change log gaps:** none. Every Class 6 prompt's current `**Version:**` has a matching latest-dated row in `prompt_change_log.md` (date-scan method, `shared_standards.md` §11.1).
- **Pre-Sprint Backlog Advisory:** no `Provisional-Target: Before v9.17 sprint planning` items found in `backlog.md`.

## Scope Review (STEP 3.1)

All 20 slice items are `include`. None is `defer` or `flag`.

- **Stale-feature-target check:** none of the 20 source items is archived or bannered ✅ COMPLETE in `backlog.md`/`backlog_archive.md`. `BLG-FE-254` is open, and ST-10 covers its unshipped TL-09/TL-10 remainder only.
- **Owner normalisation:** the slice's "Metrics Definitions & Analytics Canonical Owner" (EPIC-02, ST-06) is written in `sprint_backlog.md` as the canonical `Metrics Definitions & Analytics Owner` (`shared_standards.md` §16.11). Qualifiers such as "(KPI definitions)" and "(consulted)" move to **Notes:**.

### Delegation class assignment

| Item | Class | Justification |
|------|-------|---------------|
| ST-01, ST-02, ST-03, ST-04 | autonomous | BLG-GOV-72 fast-path (c): locked `positions.md` v2.25 (§Decision-First Table, §Warning Strip, §Grace Period View, §Responsive Behavior), `dashboard.md` v4.2 Card 3 and `risk_dashboard.md` v0.1.16 §5, with Playwright feasibility set out in `positions-decision-first/decision_record.md` §10 |
| ST-05 | autonomous | Fast-path (c): locked `journal.md` v1.0 (JA-01..JA-21) |
| ST-06 | delegated_decision | Mid-task sign-off: the build may not start until the Head of UX & Design approves `performance.md` with a date (addendum). AC 2 needs the Metrics Definitions & Analytics Owner's dated KPI confirmation. Design artefact present: `performance-page-brief/decision_record.md` (LL-v2.2-SP-01 satisfied) |
| ST-07 | autonomous | Fast-path (c): locked `trade_plan.md` v1.25 §5g, `strategy_benchmark.md` v0.10 §3a |
| ST-08 | autonomous | Design Pre-Approved: existing tokens, `design_system.md` v1.26. The boundary is set at planning (RISK-02) |
| ST-09 | autonomous | Backend + migration; every AC is pytest or contract. The production migration at deploy is a Human-Delegation deploy step, not an AC |
| ST-10 | autonomous | Locked `dashboard.md` §1B TL-09/TL-10 |
| ST-11 | autonomous | Backend + Playwright. The production backfill run is `post-merge` (tracked by `BLG-BE-211`) |
| ST-12 | autonomous | RISK-05 decided at seal (option (a)); `trade-plan-found-defects/decision_record.md` §2 |
| ST-13 | autonomous | One-line route parameter + Playwright |
| ST-14 | autonomous | `trade_plan.md` v1.25 §5a.3/§5f; addendum fixes the pre-fill source |
| ST-15 | delegated_backend | AC 1 needs a production `api_call_log` read. That read is a Human-Delegation to the Infrastructure & Operations Owner at sprint start (RISK-03) |
| ST-16, ST-17 | autonomous | Workflow + tests; sizing + unit tests |
| ST-18 | autonomous | Governance prompt edit under the CLAUDE.md §6 checklist. The Head of Specs Team confirms the `ESC-CLOSE-20261007-01` scope agent-mediated (§5.3) in the story (RISK-06) |
| ST-19 | autonomous | RISK-05 decided at seal (option (b)); wording-only (FI-P3-02) |
| ST-20 | autonomous | Tooling + unit test |

No `delegated_frontend` items, so LL-v2.0-P4-2 does not apply.

### Named-file writes (STEP 3.1)

None. ST-19's option (b) removes the only candidate case (c) `strategy_rules.md` write. No AC writes a `claude/roadmap/*` file or edits an existing `backlog.md` item. ST-06 (`BLG-FE-237`) and ST-12 (`BLG-FE-269`) record in QA evidence whether the related item's AC is met, for `groom backlog`; ST-10 AC 2 is a Post-Ship Closure banner. Neither is a sprint write.

For information, outside the named-file rule: ST-18 edits `release_planning_prompt.md`, `OPERATIONAL_GUIDE.md` and `prompt_change_log.md` under the CLAUDE.md §6 checklist.

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | None. All 20 slice items are in scope. | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 (urgency order, leading fields) | Internal | Open — sequenced |
| ST-03 | ST-01 (same page) | Internal | Open — sequenced |
| ST-04 | ST-03 (strip's grace entry expands to `GracePeriodView`) | Internal | Open — sequenced |
| ST-06 (build) | Head of UX & Design approval of `performance.md` (sub-step 1) | Spec | Open — in-story gate |
| ST-06 | ST-05 (shared `navigation.md` areas and command palette; merge in sequence) | Internal (merge) | Open — sequenced |
| ST-10 | ST-09 (`stop_last_moved_date`, `previous_stop` on `GET /positions`) | Internal | Open — sequenced |
| ST-12, ST-14 | RISK-05 decision (ST-12) | Decision | Resolved 2026-11-12 |
| ST-12, ST-14, ST-07 | Shared `TradePlan.js`, `trade_plan.md` | Cross-EPIC (file) | Open — merge order |
| ST-16 | ST-15 (post-fix failure counts), soft: ST-16 reads §4 whatever its state | Internal (soft) | Open |
| ST-19 | EPIC-01's `Positions.js` on `main`; RISK-05 decision | Cross-EPIC (file) + Decision | Decision resolved; file sequenced |
| ST-20 | ST-09's `data_model.md` migration (run the detector after both merge) | Cross-EPIC (soft) | Open — merge order |
| ST-08 | Every other UI EPIC merged (baselines for both themes) | Cross-EPIC | Open — merges last |
| ST-15 AC 1 | Production `api_call_log` read | External (Human-Delegation) | Raise at sprint start |
| ST-09, ST-11 | Production migration and backfill at deploy | External (Human-Delegation) | Raise at sprint start |

No circular dependencies.

## Execution Sequence

1. **EPIC-01** (owns `execution_state.json`): ST-01 → ST-02, ST-03 → ST-04.
2. **EPIC-04**: ST-09 → ST-10.
3. **EPIC-07**: ST-18 (start early, independent), ST-20 (after EPIC-04's `data_model.md` is on `main`), ST-19 (on EPIC-01's `Positions.js`).
4. **EPIC-06**: ST-15 (raise the production read delegation at sprint start) → ST-16; ST-17 independent.
5. **EPIC-05**: ST-11, ST-13 independent; ST-12, ST-14 (`TradePlan.js`).
6. **EPIC-02**: ST-05; ST-06 (spec → Head of UX & Design approval → build), merged after ST-05; ST-07 (rebases on EPIC-05's `TradePlan.js`).
7. **EPIC-03**: ST-08, last.

Delegations to raise at sprint start, before autonomous work: ST-15 production read (Infrastructure & Operations Owner); ST-06 spec review slot (Head of UX & Design) and KPI confirmation (Metrics Definitions & Analytics Owner); ST-09/ST-11 production deploy steps (Infrastructure & Operations Owner).

## Multi-EPIC Execution Notes

`execution_state.json` owner: **EPIC-01** (first in execution order). Every other EPIC branch checks whether the file exists before creating its own. If it exists, the branch appends its own EPIC section and never overwrites. No story is `deferred_at_planning`, so no planning-deferred entries are needed.

## Shared-File Ownership Advisory

| File(s) | EPICs / stories | Owner | Rule |
|---------|-----------------|-------|------|
| `src/pages/Positions.js`, `docs/specs/frontend/pages/positions.md` | EPIC-01 ST-01–ST-04; EPIC-07 ST-19; EPIC-03 ST-08 | EPIC-01 | ST-19 rebases on EPIC-01; ST-08 rebases last |
| `src/pages/TradePlan.js`, `docs/specs/frontend/pages/trade_plan.md` | EPIC-05 ST-12, ST-14; EPIC-02 ST-07; EPIC-03 ST-08 | EPIC-05 | ST-07 rebases on EPIC-05 and takes the next `trade_plan.md` version |
| Dashboard components (`DashboardHome`, Today list, Card 3) and `dashboard.md` | EPIC-01 ST-04 (Card 3 link); EPIC-04 ST-10 (Today list) | EPIC-01 | EPIC-04 rebases |
| `docs/specs/data_model.md`, `docs/reference/openapi.yaml`, `docs/specs/api_contracts/position_endpoints.md`, `api_changelog.md` | EPIC-04 ST-09; EPIC-05 ST-11 (if the backfill is recorded); EPIC-06 if any contract changes; EPIC-07 ST-20 reads | EPIC-04 | CLAUDE.md §8 step 3 merge rules |
| `navigation.md`, command palette, `glossary.md` §UI Labels | EPIC-02 ST-05, ST-06 | EPIC-02 (internal) | ST-06 merges after ST-05 (RISK-04) |
| `release_planning_prompt.md`, `OPERATIONAL_GUIDE.md`, `prompt_change_log.md` | EPIC-07 ST-18; frontend spec bumps in EPIC-01/02/05 append `prompt_change_log.md` rows | EPIC-07 | CLAUDE.md §6; §8 step 2a, checked per co-bumped file |
| Visual baselines (both themes) | EPIC-01, EPIC-02, EPIC-05; EPIC-03 regenerates | EPIC-03 | EPIC-03 merges last |
| `claude/backlog/backlog.md` | any follow-up filed via `/backlog-add` | — | Run `scripts/check_backlog_item_integrity.py` after each §8 merge (step 2c) |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01, EPIC-02, EPIC-05, EPIC-07 | Valid. Merge order and shared-file owners fixed above |
| RISK-02 | EPIC-03 ST-08 | Changed: resolved at planning. Boundary set; remainder filed as BLG-FE-288 |
| RISK-03 | EPIC-04, EPIC-05, EPIC-06 | Valid. Human-Delegation at sprint start; post-merge ACs marked with trackers (`BLG-OPS-217`, `BLG-BE-211`) |
| RISK-04 | EPIC-02 ST-05, ST-06 | Valid. In-story spec gate; ST-06 classed `delegated_decision` |
| RISK-05 | EPIC-05 ST-12, EPIC-07 ST-19 | Changed: resolved at planning. ST-12 option (a), ST-19 option (b), 2026-11-12 |
| RISK-06 | EPIC-07 ST-18 | Valid. Head of Specs Team confirms the ruling scope in-story |
| RISK-07 | EPIC-05 ST-12 | Valid. ST-12 records whether `BLG-FE-269` AC 1 is met |

Multi-vehicle fix-choice check: RISK-05's two options had similar effort and both are now decided. RISK-02's boundary is fixed. No other risk names alternative fix vehicles. No Phasing Recommendation exists (capacity `pass`).

## Capacity Buffer Floor

27.95 / 28.00 = 99.8%, above the 95% advisory floor. The Product Owner acknowledged this and chose to proceed with full scope, 2026-11-12.

## Pre-Seal Backlog Filings

Authorised by the Product Owner, 2026-11-12, filed via `/backlog-add`:
- **BLG-SPEC-230**: `positions.md` names two default views (design gate observation).
- **BLG-SPEC-231**: `dashboard.md` Morning Briefing "Positions to Act On" → "Positions to Watch" (design gate observation).
- **BLG-FE-288**: component-only colour-token remainder split from ST-08 (RISK-02).

Post-merge ACs are tracked by their own source items staying open (v9.16 `BLG-OPS-197` precedent), so no separate tracker was filed: `BLG-OPS-217` (ST-15 AC 2, AC 3), `BLG-BE-211` (ST-11 AC 2 production run), `BLG-GOV-419` (ST-18 AC 2).

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Raise Human-Delegations at sprint start: ST-15 production `api_call_log` read; ST-09 production migration and ST-11 production backfill at deploy | Infrastructure & Operations Owner | No |
| Approve `performance.md` (dated) before ST-06's build; confirm each KPI's canonical definition (ST-06 AC 2) | Head of UX & Design; Metrics Definitions & Analytics Owner | No |
| Keep `BLG-OPS-217`, `BLG-BE-211` and `BLG-GOV-419` open as trackers until their post-merge ACs are met | Sprint Execution Engine; Post-Ship Closure Engine | No |
| For any other staging-only AC whose sign-off is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |
| Carry-Forward #3: run `run roadmap --reason "scheduled"` linking the governance overhead audit and `BLG-GOV-408` | PMO Lead | No |
