Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-26

# QA Evidence — EPIC-10 (v7.8)

**EPIC:** EPIC-10 — Flaky-test quarantine process for the Playwright suite
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_flaky_quarantine_format.py`

## ST-10 — Define and apply flaky-test quarantine mechanism

**Spec reference:** `docs/testing/flaky_test_quarantine_process.md` (new artefact, Case B)
**Commit:** `3c6fbae7` (implementation `68fba626`)

**What was built:** A documented quarantine tag/process using Playwright's built-in `test.fixme(condition, description)`, with a required `FLAKY-QUARANTINE: <reason> — tracked in BLG-QA-<id>` description format — distinct from the deterministic environment-conditional `test.skip()` pattern already used elsewhere in the suite (`keyboard-shortcuts.spec.js`, `visual-snapshots.spec.js`), which was confirmed (by direct inspection) not to be flakiness and therefore not a migration candidate. Enforcement added via `tests/test_flaky_quarantine_format.py`, which scans `tests/e2e/*.js` for any `test.fixme(` call and fails if it lacks the required prefix or a `BLG-*` backlog reference — preventing an untracked quarantine from silently accumulating.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-10 | `flaky_test_quarantine_process.md` | Quarantine tag/process (test.fixme + required format) | Quarantine tag/process defined (e.g. `test.fixme` with tracked follow-up) and documented | Pass | None |
| ST-10 | (same) | Repo-wide scan performed; no currently-known flaky test found | Process applied to any currently-known flaky test, if one exists at implementation time | Pass — none exists; documented explicitly rather than silently omitted | None |
| ST-10 | (same) | (see Autonomous class section below) | Director of Quality sign-off | Pass — BLG-GOV-19 autonomous class (see below); no additional domain authority named beyond DoQ itself, unlike ST-07/08's Cybersecurity & Trust Lead | None |

**QA test coverage:**
- Scenarios run: `tests/test_flaky_quarantine_format.py` — 5 tests: correctly-formatted quarantine produces no violation, missing-prefix caught, missing-backlog-reference caught, no-fixme-calls produces no violations, and a regression guard confirming the real `tests/e2e/` directory has zero format violations today. All 5 pass.
- Regression areas checked: full backend suite (759 tests on this branch, base `main` count before EPIC-09/12/08's additions merge) — all pass, no behavioural change.
- Known deviations filed: None.

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-10 is the only story, classified `autonomous`.
- Criterion 2 (all AC verifiable by code review/tests alone): ✓.
- Criterion 3 (no frontend-visible change): ✓ — only `docs/testing/` and `tests/` touched.
- Criterion 4 (engine signer field populated): ✓.

**All four criteria met — autonomous class applies**, and directly satisfies this story's own "Director of Quality sign-off" AC — unlike ST-07/ST-08 in this same sprint, no *additional* domain authority beyond Director of Quality itself is named, so there is no separate BLG-GOV-14 layer to record here.

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-26
- Comments: Autonomous class sign-off — all four qualifying criteria met, satisfying this story's own Director of Quality sign-off AC directly.
