Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-09 (Director of Quality — struck stale pre-merge caveat sentence, both PRs now confirmed merged; post-ship closure 2026-09-07__release-v9.2 outstanding-actions resolution)

---

**EPIC:** EPIC-03 — QA & CI Reliability Debt
**Cycle:** 2026-09-07__release-v9.2
**Sprint goal:** Ship the Arc 5 low-volume compliance-score advisory and clear a full-capacity slate of 55 accessibility, QA/CI reliability, governance-process, and spec/tech/ops debt items across all 5 EPICs — exhausting the confirmed ~24–28 day capacity band at 27.55 days, with 0 P1/P2 debt items carried past this sprint on capacity grounds.
**Test scenarios used:** `tests/e2e/accessibility-axe-scan.spec.js`, `tests/e2e/arc5-compliance-section.spec.js`, `tests/test_check_specs_index_freshness.py`, `scripts/test_governance_sync_close_gate_logic.sh`, `scripts/test_governance_sync_diff_logic.sh`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-06 | `.github/workflows/playwright.yml` | Added `package.json`/`package-lock.json` to both `push.paths` and `pull_request.paths` (additive only) | Dependency-bump-only PR triggers the E2E suite; no change to existing frontend-file triggers; Infrastructure & Operations Owner sign-off | Pass | None |
| ST-07 | *(no canonical spec — see notes)* | `accessibility-axe-scan.spec.js`'s `runAxeScan()` replaced its fixed 1000ms sleep with `waitForEntranceAnimations()`, a condition-based poll on inline-style opacity (3000ms timeout guard, proceeds rather than fails) | Fixed sleep removed; all 4 scanned pages continue to pass | Pass | None |
| ST-08 | *(no canonical spec — see notes)* | `SC-ARC5-06`/`SC-ARC5-07` in `arc5-compliance-section.spec.js` scoped to the `Arc5ComplianceSection` container (`heading.locator('..')`), matching the existing `SC-ARC5-08` convention | Both assertions scoped; full spec file (15/15) continues to pass | Pass | None |
| ST-09 | `scripts/test_governance_sync_close_gate_logic.sh` (new) | Regression script directly exercises `is_story_done()`'s unknown/no/yes branches (parameterised copy of the `governance_sync.yml` function) | Regression test specifically covers the `unknown`-status skip behaviour; confirms no auto-close for an untracked story or one later resolved to `blocked_*` | Pass | None |
| ST-10 | *(no canonical spec — underlying fix already shipped v9.1, commit `9eec64b4`)* | Extended `test_governance_sync_diff_logic.sh` with a 3rd regression case using the real BLG-QA-160 incident's own commit pair (`912ea30a`→`1cbd31ee`, EPIC-05 v9.1) | Split work/state-sync commit auto-closes on the 2nd push without a bracketed `[ST-xx]` tag; regression test covers this scenario; existing under/over-closing behaviour unaffected | Pass | None |
| ST-11 | `tests/test_check_specs_index_freshness.py` (new) | 8 pytest tests covering addition detection, removal detection, the `qa/` exclusion rule, and the named false-positive guard (`strategy_rules.md` cross-reference not flagged as removal) | Regression test covers both addition/removal paths and at least one exclusion case; false-positive guard explicitly confirmed | Pass | None |
| ST-12 | `docs/ops/ci_pipeline_baseline.md#8.5` | New §8.5 first trend re-measurement (day 0 → day 1) against the §8.2 budget; one outlier reading investigated and traced to a runner-level "Install Playwright OS dependencies" stall, not a suite regression | Trend report produced; QA & Testing Owner sign-off | Pass | None |
| ST-13 | `docs/governance/deviation_root_cause_pattern_report_2026-09-08.md` (new) | Root-cause grouping pass over the existing 16-record `DEV-*` consolidated register; found a self-confirmed same-cycle currency/FX-conversion recurrence (Class A) and a declining visual/theming-drift class (Class B) | Report produced for the current deviation set; Director of Quality sign-off | Pass | None — Recommendation 1 filed as `BLG-SPEC-137` (out-of-scope finding, not a deviation from this story's own AC) |
| ST-14 | `docs/ops/pip_audit_trend_log.md` (new), `claude/system/sprint_planning_prompt.md` | New trend log backfilled with 6 readings (v8.7–v9.2); `sprint_planning_prompt.md` v3.17→v3.18 applies the convention from the next sprint planning onward | Log convention documented and applied from next sprint planning onward | Pass | None |
| ST-15 | `claude/system/templates/qa_evidence_template.md` | Compared template against CLAUDE.md's FI-P3-02 exception; found zero mentions despite ad hoc use in practice; added an explicit citation-format callout, distinguished from the BLG-GOV-19 Autonomous Class block | Comparison performed; template confirmed current or corrected | Pass | None |
| ST-16 | `docs/governance/fi_p3_02_staging_signoff_tracker.md` (new) | Tracker backfilled via literal-string grep across all `qa_evidence_EPIC-*.md` files — 2 genuine invocations found, 1 rule-origin story correctly excluded | Tracker created and backfilled where findable; QA Lead sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/e2e/accessibility-axe-scan.spec.js` (4/4), `tests/e2e/arc5-compliance-section.spec.js` (15/15) — both re-run green locally post-change (ST-07, ST-08). `tests/test_check_specs_index_freshness.py` (8/8, via `backend/.venv/bin/python3 -m pytest`), `scripts/test_governance_sync_close_gate_logic.sh` (4/4 cases), `scripts/test_governance_sync_diff_logic.sh` (6/6 cases, 3 pre-existing + 3 new) — all new/extended test scripts run directly, all pass.
- Regression areas checked: Accessibility scan timing (all 4 scanned pages), Arc5ComplianceSection full suite, `governance_sync.yml`'s closing logic (both the diff-based detection path and the `is_story_done()` gate), `check_specs_index_freshness.py`'s addition/removal/exclusion logic. No backend service or API contract touched this EPIC — no `tests/` backend pytest re-run required beyond the one new test file.
- Known deviations: None found — all 11 stories' deviation checks completed with nothing to file.

**Frontend testing gate (LL-v3.1-EX-01) — observable AC coverage:**
- None of this EPIC's 11 stories touch `src/pages/` or `src/components/` — zero frontend-visible changes. ST-07/ST-08 modify Playwright *test* files (`tests/e2e/`), not application UI code; their own ACs ("all N scans/scenarios continue to pass") are satisfied by the re-run results above, not by a rendering claim. No AC in this EPIC requires Playwright coverage or a staging run under CLAUDE.md's frontend-visible-change gate — the gate itself does not apply here (no frontend-visible change exists to gate).

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (all 11)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (CI-workflow config, test-file internals, governance/ops documents; all evidenced by direct test-run output above, not by any rendering claim)
- [x] Criterion 3: No frontend-visible change — confirmed via `git diff --stat` on this EPIC's commits (`bdbc3698`, `21405680`): zero files under `src/pages/` or `src/components/` touched — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-09-08
- Comments: Autonomous class sign-off — all four qualifying criteria met (all 11 stories autonomous, all AC verified by direct code review and test-run evidence with no observable UI behaviour anywhere in this EPIC, zero `src/pages/`/`src/components/` changes confirmed via diff, engine signer field populated). 4 of the 11 stories additionally carry their own named-role agent-mediated sign-off per their individual AC (ST-06: Infrastructure & Operations Owner; ST-12: QA & Testing Owner; ST-13: Director of Quality; ST-16: QA Lead) — all Approved, recorded in full in `execution_state.json`'s per-story `sign_off_record` fields. This EPIC-level block is the aggregate autonomous-class acknowledgement per `qa_evidence_template.md`. STEP 4's separate merge-gate condition (a human comment on the PR) has since been satisfied — PR #1598 confirmed merged (per `execution_state.json.merge_gate.all_merged: true`).
