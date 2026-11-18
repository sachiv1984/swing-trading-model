# Sprint Planning Notes — 2026-11-18__release-v9.18

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-18
**Cycle:** 2026-11-18__release-v9.18

## Backlog Slice Source

Original: `claude/cycles/2026-11-18__release-v9.18/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-03, ST-04, ST-07–ST-14, ST-16, ST-17, ST-27, ST-30, ST-33). `amended_backlog_slice_path` is empty; no amendment is active.

## Preflight Record

- **Lifecycle guard:** `status = Design_Gate_Passed`, a valid Sprint Planning entry state (`shared_standards.md` §10.1). Not `Amendment_In_Progress`.
- **Release plan sealed:** `state.json` `status = Published`, `publish_eligible = true`, `open_escalations` empty, `deferred_execution_blockers` empty.
- **Design gate:** `design_gate_required = true`, `design_gate_status = Passed` (`design_gate.md`, 2026-11-18T10:14:32Z). Entered from `Design_Gate_Passed`, so the bypass audit is skipped.
- **Files, roles, write access:** slice has 7 EPICs and 40 ST items; every §5 input is present (schema v2: `release_plan.md ## Execution Plan` and `## Capacity Check` stand in for the pre-v2.11 stage files); all five §4 role files are present; `lessons_learnt_prompt.md` is present; `.write_test` created and removed.
- **Branch:** `main`.
- **Open escalations:** `ESC-EXEC-20260910-01` is Deferred (`blocks_execution: false`); its trigger is `BLG-GOV-399`, which is not in v9.18 scope. No effect on planning.

## Pre-Sprint Required Decisions

`cycle_summary.md ## Pre-sprint Planning Required Decisions` lists one item:

- **RISK-05, ST-27 stock-split rule direction (Strategy Rules & System Intent Owner).** **Resolved at seal, 2026-11-18.** Direction: a new `strategy_rules.md` §9.1 "Stock split on an open position". For a ratio r (2:1 → r = 2): quantity × r; entry, initial stop and trailing stop ÷ r; ATR from split-adjusted history; per-share risk ÷ r, so currency risk and R-multiples are unchanged. Until the user confirms the adjustment, the position gets no stop-breach alert and no exit recommendation. The adjustment is a unit change, not a §7.3 stop movement. The original entry fields stay stored. A ratio that leaves a non-whole quantity is not confirmed automatically: Positions asks the user to enter the post-split share count. The exact text is approved in the story (slice AC 6). Recorded in `sprint_backlog.md`'s sign-off summary.

## Carry-Forward Items

Carry-forward items reviewed: 4 items from cycle `2026-11-11__release-v9.17` (`lessons_learnt_closure.md ## Carry-Forward`).
1. `BLG-GOV-422`, `BLG-QA-262`, `BLG-QA-260` seated with the `BLG-GOV-422` extension: applied by Release Planning (ST-18, ST-19, ST-20).
2. `BLG-FE-294` seated ahead of P3 work: applied (ST-33).
3. Scheduled rebalance before `plan release`: done (`2026-11-18__scheduled`).
4. `BLG-UX-08` re-review: done out of sprint, 2026-11-17.

None needs sprint-planning action.

## Pre-Sprint Vulnerability Scan

pre-sprint pip-audit: clean. `pip-audit -r backend/requirements.txt --format=json`: 53 dependencies, 0 vulnerabilities, no fixes. Trend row appended to `docs/ops/pip_audit_trend_log.md`.

## Pre-Sprint Endpoint Coverage Audit

pre-sprint endpoint coverage audit: clean. `python3 scripts/audit_endpoint_test_coverage.py` exited 0: 94 route decorators across 27 router files; 8 documented `KNOWN_GAPS`; no undocumented gap.

## Hygiene Advisories

- **Prompt change log gaps:** none. The date-scan method found a `prompt_change_log.md` row for every Class 6 prompt's current version.
- **"Before v9.18 sprint planning" backlog items:** none.

## Scope Review (STEP 3.1)

All 40 slice items are `include`. ST-32 is included as **conditional** (§1.4b, within-sprint date gate 2026-11-20). No item is `defer` or `flag`.

- **Stale-feature-target check:** none of the 40 source items is archived or bannered ✅ COMPLETE. ST-07's decision half is met by DL-089 and ST-32's AC 1 by v9.17 ST-15; the slice restates both as remainders. ST-40's precondition `BLG-BE-152` has shipped (archived).
- **Owner normalisation:** ST-40's slice owner "AI Compliance Governance Officer" is written in `sprint_backlog.md` as the canonical `AI Compliance & Governance Officer`. ST-38's "Director of Quality" is a canonical role and is kept.

### Delegation class assignment

| Item | Class | Justification |
|------|-------|---------------|
| ST-01, ST-02 | autonomous | Design Pre-Approved; `design_system.md` v1.27 §Accessibility; Playwright keyboard and axe checks |
| ST-03, ST-04 | autonomous | Fast-path (c): locked `notifications.md` v0.12, `alert-delivery-truth` decision record. ST-04's one real UK row check needs the user's permission for a staging read (staging-only step) |
| ST-05 | delegated_decision | Review and dated decision by the Cybersecurity & Trust Lead and the Product Owner |
| ST-06 | autonomous | CI job, budget doc and `web-vitals` reporting; no UX change |
| ST-07 | delegated_decision | AC is the dated Head of UX & Design approval of `navigation.md` and `design_system.md` |
| ST-08, ST-09, ST-10, ST-11 | autonomous | Fast-path (c): locked `navigation.md` v2.5, `performance.md` v1.3, `strategy_benchmark.md` v0.12, `ticker_universe.md` v1.3, `settings.md` v1.11, `dashboard.md` v4.4. ST-11's decision was taken by the Product Owner at the gate |
| ST-12 | delegated_decision | Mid-task sign-off: the Strategy Rules & System Intent Owner confirms the `trade_plan.md` v1.30 §6 §13-note amendment (dated) before the build (addendum) |
| ST-13 | delegated_decision | Mid-task sign-off: the Metrics Definitions & Analytics Owner writes the rules-followed definition before the build |
| ST-14, ST-15, ST-16 | autonomous | Locked `weekly_digest.md` v0.3 and `navigation.md` v2.5 §Onward Links; decisions taken at the gate |
| ST-17 | delegated_decision | AC 1 needs the Metrics Definitions & Analytics Owner's sign-off of the five step definitions |
| ST-18, ST-21, ST-22, ST-23 | autonomous | Governance prompt and hook edits under the CLAUDE.md §6 checklist, with the Head of Specs Team role agent-mediated |
| ST-19, ST-20, ST-24 | autonomous | CI, test tooling and scripts |
| ST-25, ST-26, ST-28, ST-29 | autonomous | Backend; every AC is pytest |
| ST-27 | delegated_decision | Direction decided at seal (RISK-05); the exact `strategy_rules.md` §9.1 text needs dated Strategy Rules & System Intent Owner approval before the build (AC 6). The production migration at deploy is a Human-Delegation deploy step |
| ST-30 | autonomous | Direction (a) decided by the Product Owner at the gate. AC 1 is verified on staging (staging-only) |
| ST-31 | autonomous | Design Pre-Approved; Playwright request count |
| ST-32 | delegated_backend | AC 2 and AC 3 need a production weekly report from the Infrastructure & Operations Owner (Human-Delegation at sprint start; RISK-03) |
| ST-33, ST-34, ST-36, ST-37, ST-38 | autonomous | Backend and frontend with tests; CI workflows. ST-34's `workflow_dispatch` run is a GitHub Actions run on the EPIC branch, in-sprint |
| ST-35 | delegated_backend | AC 2 needs a staging write, with the user's permission |
| ST-39 | delegated_decision | AC 1: the AI Compliance & Governance Officer's ruling is recorded before the code |
| ST-40 | delegated_decision | Decision by the AI Compliance & Governance Officer and the Product Owner on a sample of real production debriefs (Human-Delegation for the sample) |

No `delegated_frontend` items, so LL-v2.0-P4-2 does not apply.

**LL-v2.2-SP-01 design artefacts for `delegated_decision` items:** ST-07 `navigation-phase4-moves/decision_record.md`; ST-12 `trade-plan-checklist-status/decision_record.md`; ST-13 `rules-followed-filter/decision_record.md`; ST-17 `weekly-review/decision_record.md` §6; ST-27 `position-data-states/decision_record.md` §2; ST-39 `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`; ST-40 `decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`. **No design artefact found for ST-05.** A HoST design session should be scheduled before sprint start. Advisory only: ST-05 is a security review, and its input is `credential_policy.md` §1.1.

### Named-file writes (STEP 3.1)

- Named-file write: `claude/strategy/strategy_rules.md` new §9.1 "Stock split on an open position" (content per the RISK-05 direction above), a one-line cross-reference in §8.1 that a detected, unconfirmed split suppresses the stop-loss trigger, and the file's Change log row (ST-27) — authorised under execution_prompt.md §7 named-file rule (case (c)). Needs a Strategy Rules & System Intent Owner confirmation line in the §6.2 sign-off.
- Named-file write: `BLG-BE-213` `Notes` line, only if `compliance_service.py`'s `fx_rate` does not convert a money value (ST-26 AC 3) — authorised under execution_prompt.md §7 named-file rule.

No `claude/roadmap/*` write is planned. No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned.

**Not authorised by this plan:** if ST-40's decision amends the debrief limits, any change to `strategy_rules.md` §13.5's attestation table is outside the named-file rule. ST-40 records the decision and files the implementation item (its own scope), and does not write `strategy_rules.md`. ST-12's §13-note amendment is in `trade_plan.md` (a spec), not `strategy_rules.md`.

For information, outside the named-file rule: ST-18, ST-21, ST-22 and ST-23 edit `design_gate_prompt.md`, `execution_prompt.md`, `post_ship_closure.md`, `roadmap_prompt.md`, `OPERATIONAL_GUIDE.md` and `prompt_change_log.md` under the CLAUDE.md §6 checklist. ST-05 files any remedy as a new backlog item via `/backlog-add`.

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | None. All 40 slice items are in scope. ST-32 is conditional, not deferred: if its 2026-11-20 gate is not met, it returns to the backlog at sprint close | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal (same `accessibility-axe-scan.spec.js`) | Open |
| ST-04 | ST-03 | Internal (Notification History / `notifications.md`) | Open |
| ST-08 | ST-07 (`navigation.md` half done at gate) | Spec | Resolved (`navigation.md` v2.5) |
| ST-09 | ST-07 | Spec (`design_system.md` §14.5 direction) | Open (not a build blocker: `dashboard.md` v4.4 is locked) |
| ST-10 | ST-09 | Internal (same Dashboard cards and baselines) | Open |
| ST-11 | ST-10 | Internal (`dashboard.md` §1B) | Open |
| ST-13 | Metrics Definitions & Analytics Owner definition | Decision | Open (sprint start) |
| ST-15, ST-16 | ST-14 | Internal (renamed field) | Open |
| ST-17 | ST-15; Metrics owner sign-off | Internal + Decision | Open |
| ST-16 | ST-08's `navigation.md` | Cross-EPIC (EPIC-02 → EPIC-03) | Resolved (gate wrote §Onward Links in v2.5) |
| ST-20 | ST-01, ST-02 (`runAxeScan`) | Cross-EPIC (EPIC-01 → EPIC-04) | Open |
| ST-23 | ST-22 | Internal (governance bumps in sequence) | Open |
| ST-10, ST-27 | ST-19 (`positionUrgency` unit-test convention) | Cross-EPIC (EPIC-04 → EPIC-02, EPIC-05) | Open |
| ST-26 | ST-25 | Internal | Open |
| ST-27 | Strategy Rules & System Intent Owner exact-text approval | Decision | Direction resolved at seal; text open |
| ST-12 | Strategy Rules & System Intent Owner §13-note confirmation | Decision | Open (sprint start) |
| ST-32 | Production weekly report ≥ 2026-11-20 | External (Human-Delegation) | Open (date gate) |
| ST-33 | ST-32 (only if its cause changes which lookups fail) | Cross-EPIC soft | Open |
| ST-36 | ST-34 | Internal (workflows) | Open |
| ST-38 | ST-29 | Cross-EPIC (EPIC-05 → EPIC-06; settings path) | Open |
| ST-39 | AI Compliance & Governance Officer ruling | Decision | Open (sprint start) |
| ST-40 | Production debrief sample | External (Human-Delegation) | Open |
| ST-05 | Cybersecurity & Trust Lead + Product Owner decision | Decision | Open (sprint start) |

No circular dependency.

## Execution Sequence

**Raise at sprint start (Human-Delegations and decisions):** ST-32 production report (due ≥ 2026-11-20); ST-40 production debrief sample; ST-05 decision; ST-39 ruling; ST-27 exact rule text; ST-12 §13-note confirmation; ST-13 and ST-17 metric definitions; ST-07 approval; ST-35 staging write permission.

1. **EPIC-01:** ST-05 (raised), ST-01 → ST-02, ST-03 → ST-04, ST-06.
2. **EPIC-04:** ST-18 and ST-19 first; ST-21, ST-22 → ST-23, ST-24; ST-20 after EPIC-01's axe changes are on `main` (or rebased on them).
3. **EPIC-06 early standalone:** ST-34 (baseline workflow can push) before any EPIC regenerates baselines.
4. **EPIC-07:** ST-39 (after the ruling), ST-40 (when the sample is available).
5. **EPIC-05:** ST-25 → ST-26, ST-28, ST-29, ST-31, ST-30, ST-27 (after the text approval and ST-19's convention).
6. **EPIC-06:** ST-35, ST-36 (after ST-34), ST-37, ST-38 (after ST-29 is on `main`), ST-33, ST-32 (≥ 2026-11-20).
7. **EPIC-02:** ST-07 → ST-08, ST-09 → ST-10 → ST-11, ST-12, ST-13.
8. **EPIC-03:** ST-14 → ST-15 + ST-16 → ST-17.

Autonomous stories go first within each EPIC, while the delegated decisions raised at sprint start come back.

## Multi-EPIC Execution Notes

**`execution_state.json` owner:** EPIC-01 (first in merge order). Every other EPIC branch checks whether the file exists before creating its own; if it exists, the branch reads it and appends its own EPIC section, never overwriting. No story is `deferred_at_planning`. ST-32 is recorded with `status_at_sprint_open: conditional — gate 2026-11-20`.

**EPIC merge sequence:** EPIC-01 → EPIC-04 → EPIC-07 → EPIC-05 → EPIC-06 → EPIC-02 → EPIC-03. ST-34 may merge on its own ahead of the sequence (it touches only its workflow file).

## Shared-File Ownership Advisory

- **`tests/e2e/accessibility-axe-scan.spec.js`, `runAxeScan`** (EPIC-01 ST-01, ST-02; EPIC-04 ST-20): EPIC-01 owns; ST-20 rebases.
- **`src/lib/positionUrgency.js` and its unit tests** (EPIC-04 ST-19; EPIC-05 ST-27 tier 0; EPIC-02 ST-10 `nextEndsText`): EPIC-04 owns the test file and convention; EPIC-05, then EPIC-02, rebase and add cases.
- **`openapi.yaml`, `api_changelog.md`, contracts** (EPIC-01 ST-03 `alerts_endpoints.md`; EPIC-06 ST-33 `earnings_endpoints.md`; EPIC-02 ST-13 `trade_endpoints.md`; EPIC-03 ST-14, ST-16, ST-17 `digest_endpoints.md`): union of paths, highest version (CLAUDE.md §8 step 3). The first merging EPIC sets the next `openapi.yaml` version; later EPICs take the next one.
- **`data_model.md`** (EPIC-05 ST-27 split adjustment migration, ST-28 convention; EPIC-03 ST-17 events table): EPIC-05 owns; EPIC-03 takes the next migration number. Run `check_data_model_drift.py` after each merge.
- **`metrics_definitions.md`** (EPIC-02 ST-13; EPIC-03 ST-14, ST-17): EPIC-02 owns; EPIC-03 rebases.
- **`navigation.md`** (EPIC-02 ST-07/ST-08; EPIC-03 ST-16 §Onward Links): EPIC-02 owns.
- **`src/pages/Positions.js`, `positions.md`** (EPIC-05 ST-27; EPIC-06 ST-33 badge): EPIC-05 owns; EPIC-06 rebases.
- **Settings path** (`backend` settings service; EPIC-05 ST-29; EPIC-06 ST-38): EPIC-05 owns.
- **Governance files** (`design_gate_prompt.md`, `execution_prompt.md`, `post_ship_closure.md`, `roadmap_prompt.md`, `OPERATIONAL_GUIDE.md`, `prompt_change_log.md`, `.githooks/pre-commit`): EPIC-04 internal, committed in sequence. Apply CLAUDE.md §8 step 2a per co-bumped file if any other branch bumps one.
- **`.github/workflows/`** (EPIC-06 ST-34, ST-36; EPIC-01 ST-06 Lighthouse job; EPIC-04 ST-19 unit-test job, ST-23 `prompt-size-budget.yml`): separate jobs or files where possible; a later EPIC that edits the Playwright workflow rebases on ST-36.
- **Visual baselines** (EPIC-02 Dashboard; EPIC-03 Weekly Digest; EPIC-05 Positions/Reports; EPIC-06 badges): ST-34 lands first; each EPIC regenerates the baselines it changes after rebasing; EPIC-03 regenerates last.
- **`backend/routers/test.py`, `SystemStatus.js` fallback, `SC-SS-01b`:** only if ST-17 adds an events endpoint (CLAUDE.md §2).
- **`claude/backlog/backlog.md`:** follow-ups via `/backlog-add` only; run `scripts/check_backlog_item_integrity.py` after each §8 merge (step 2c).

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01–04 | Valid. Merge order and shared-file ownership above; ST-34 early |
| RISK-02 | EPIC-02 | Changed: largely retired. The design gate wrote `navigation.md` v2.5; ST-07 now carries only `design_system.md` §14.5 and the dated approval |
| RISK-03 | EPIC-03, 05, 06, 07 | Valid. Human-Delegations raised at sprint start; post-merge ACs have named trackers (see below) |
| RISK-04 | EPIC-04 | Valid. Sequential commits on one branch, §9.1 Change Log read before each bump, size budget check before each commit |
| RISK-05 | ST-27 | Resolved at seal (direction, Strategy Rules & System Intent Owner, 2026-11-18); exact text approval stays in-story |
| RISK-06 | ST-05 | Valid. Remedy filed as its own item |
| RISK-07 | ST-32 | Valid. Conditional, gate 2026-11-20 |

**Multi-vehicle fix-choice check (LP-14):** ST-30's two directions were decided at the gate (option (a)). ST-37 names two vehicles (root pytest config, or conftest restore); both are XS, so there is no material effort difference. ST-05's remedy options are out of v9.18 scope (RISK-06). The capacity check was `pass`, with no Phasing Recommendation. Nothing to cross-reference.

**Director of Quality readiness (STEP 4.3, agent-mediated):** QA criteria are sufficient for `qa_evidence_EPIC-01`–`07`. Observable UI ACs have Playwright named in the slice. The known in-sprint limits are the staging-only and post-merge ACs listed in `sprint_backlog.md`, each with a tracker or a CLAUDE.md §2 filing obligation. No blocking gap.

## Capacity Buffer Floor

27.95 / 28.00 = 0.998, above the 0.95 advisory floor. Product Owner: proceed, single sprint, 2026-11-18.

## Pre-Seal Backlog Filings

Product Owner authorised, filed 2026-11-18 via `/backlog-add` (design gate observations for filing):
- `BLG-UX-22`: decide and ship the "Weekly review" rename
- `BLG-SPEC-241`: align `dashboard.md` §1A Earnings Alert click target with the shipped card
- `BLG-BE-224`: check that notification re-delivery never sends rows created while a preference was off
- `BLG-QA-274`: record whether the Performance CWV baseline includes the Strategy Benchmark section (relevant to ST-06)

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-05: ST-27 rule direction | Strategy Rules & System Intent Owner | Yes. **Resolved 2026-11-18** |
| Human-Delegations at sprint start: ST-32 production weekly report (≥ 2026-11-20); ST-17 and ST-27 production migrations at deploy; ST-40 production debrief sample | Infrastructure & Operations Owner; AI Compliance & Governance Officer | No |
| In-story sign-offs before build: ST-27 exact text, ST-12 §13-note, ST-13 and ST-17 metric definitions, ST-07 approval, ST-05 decision, ST-39 ruling | Named owners | No |
| Staging permission: ST-35 staging write; ST-04 UK row read; ST-30 staging check | Product Owner (user) | No |
| Schedule a HoST design session for ST-05 (LL-v2.2-SP-01, advisory) | Head of Specs Team | No |
| For any staging-only AC whose sign-off is deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |
