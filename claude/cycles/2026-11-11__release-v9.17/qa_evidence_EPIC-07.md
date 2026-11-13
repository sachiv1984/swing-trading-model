Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-13

# QA Evidence — EPIC-07: Governance, Strategy Copy and Drift Tooling

**EPIC:** EPIC-07 — Governance, Strategy Copy & Drift Tooling
**Cycle:** 2026-11-11__release-v9.17
**Sprint goal:** Ship Site Structure & Usability Phase 3 complete (decision-first Positions page with narrow-screen cards, one warning strip and one grace view; the single Journal area; one Performance page; section indexes on Trade Plan and Strategy Benchmark; the semantic colour token sweep), finish Phase 2's Stops moved group, and fix the four v9.16 Trade Plan found defects.
**Test scenarios used:** `tests/test_check_data_model_drift.py`, `tests/e2e/lifecycle-badge-grace-calendar-days.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-18 | `claude/system/release_planning_prompt.md` §1.3a (v2.75) | §1.3a bound 2: a clearing edit (date-lapsed option (a) or gating-item-shipped clearance) also sets a gate-worded `Provisional-Target` to `TBD`; the dated note keeps the old value; bound 6 lists it in `run_manifest.md`; §7 carve-out names the exception. CLAUDE.md §6 checklist complete (`02587c70`). | AC 1: §1.3a states a clearance may set a gate-worded `Provisional-Target` to `TBD` in the same edit and lists it in `run_manifest.md` — **met** (bound 2 and bound 6). AC 2: next Release Planning gate scan after a clearance does not warn on the item — *post-merge, seal-marked, tracked by BLG-GOV-419*; `TBD` is not matched by `EMBEDDED_GATE_SIGNAL_RE` (checked). | Pass | None |
| ST-19 | `docs/specs/frontend/pages/positions.md` §Position Lifecycle State Badge (v2.27); `positions-decision-first/decision_record.md` §7 | PROFITABLE and EXIT ZONE tooltips take RISK-05 option (b) wording, with no R multiple; option (a) wording removed from the spec (`5a7db63b`; `cad3b87f` moved the v2.27 note out of the tooltip table, where it had cut off the UNKNOWN row, found at DoQ round 1). | The tooltip's threshold is no longer stated as a number; `scripts/check_strategy_copy.py` passes — **met** (0 contradictions, 0 literals). Wording-only AC, also covered by Playwright SC-LBG-06 (CI run 43407147398). | Pass | None |
| ST-20 | `scripts/check_data_model_drift.py`; `docs/ops/data_model_drift_runs/` | Index and CHECK names parsed from forward SQL only (Down Migration sections, `Reversible:` inline SQL, fenced block after a bare `Reversible:` skipped); run-output location documented; first saved run and triage (`f1299c5c`, `6dc668d8`). | AC 1: detector no longer reports `idx_trade_plans_ticker` — **met** (read-only staging run, `2026-11-13_staging.json`). AC 2: a unit test fails if a rollback-only name is reported again — **met** (3 tests; shown to fail with the exclusion bypassed). AC 3: usage says where `--json` output is kept and the next triage cites it — **met** (detector docstring, `data_model_drift_runs/README.md`; `2026-11-13_staging_triage.md` cites the JSON). | Pass | None |

**AC coverage:** ST-18 has two ACs, ST-19 one, ST-20 three (`stage4_backlog_slice.md#ST-18`, `#ST-19`, `#ST-20`); each is named in its row. ST-18 AC 2 is the only staging/post-merge AC, marked `post-merge` at seal with BLG-GOV-419 as its tracker, so ST-18 is graded on its in-sprint AC (execution_prompt.md §3.2.A, LL-v9.13-P3-03).

**Story-level authority sign-offs:**
- ST-18 — Head of Specs Team (agent-mediated, §5.3), 2026-11-13: **Approved**, one round. Recorded as an **extension of `ESC-CLOSE-20261007-01` bound 2**: "Only a clearing edit (date-lapsed option (a) or a gating-item-shipped clearance) may also set a gate-worded `Provisional-Target` to `TBD`, with the old value kept in the dated note and in `run_manifest.md`. Re-gates, plain release targets and every other field stay untouched." The mandatory wording ("also sets") was chosen on purpose over "may", so the same input always gives the same result; it still satisfies AC 1. The scope's "replace gate language … and nothing else in that field" was read as replacing the whole gate-worded value with `TBD`, with the old value kept in the note (reviewer's note 7).
- ST-19 — wording decided by the Strategy Rules & System Intent Owner at RISK-05 (option (b), 2026-11-12, sealed `sprint_backlog.md`); no further sign-off named.

**Implementation notes:**
- ST-20 found and fixed a second detector false positive in the same file: `INDEX_RE` read the prose "`CREATE INDEX IF NOT EXISTS`)" in `data_model.md` DS-36 as an index named `IF`. Disclosed in `6dc668d8` as an opportunistic in-file fix, with a regression test.
- ST-20's staging run (user permission, 2026-11-13, read-only session, no other query) reported one name not in the v9.12 triage: `idx_momentum_signal_runs_portfolio_date` (DS-39, lazily created table). Recorded as unconfirmed in the triage; confirming it needs one catalog query.
- `data_model.md` §Drift Detector Triage still describes `idx_trade_plans_ticker` as reported because "the detector reads rollback SQL: BLG-QA-223". That row is a dated v9.12 record and was not edited (execution write scope); the new triage records the fix.

**QA test coverage:**
- Scenarios run: `tests/test_check_data_model_drift.py` 17/17 locally and in CI Pytest Suite (43408448753 on `6dc668d8`); `tests/e2e/lifecycle-badge-grace-calendar-days.spec.js` with `positions-decision-first` and `positions-decision-cards`, 23/23 locally on an E2E-env production build; Playwright E2E Acceptance Tests run 43407147398 success on `5a7db63b`.
- CI per story SHA: `f1299c5c` all 7 workflows success; `5a7db63b` all 9 success; `02587c70` all 7 success; `6dc668d8` all 7 success.
- Regression areas checked: Positions lifecycle badges and decision-first table/cards; strategy-copy lint; drift detector parsing (index, CHECK, defaults, tables); governance version sync (`governance-drift` Step 1b PASS: header, §14 self-row and Change Log top row all 4.260 / 2026-11-13; all 28 §14 rows match file headers); prompt size budget OK.
- Known deviations: None found — all three stories' deviation checks completed with nothing to file.
- Frontend testing gate: ST-19's only observable AC is wording-only (FI-P3-02) and also has Playwright coverage (SC-LBG-06) observed passing in real CI. ST-18 and ST-20 change no frontend file. No "code review only" AC.
- Same-EPIC testing-gap consistency: no testing-gap backlog item was filed in this EPIC.
- P1/P2 found defects filed during this EPIC: none.
- Autonomous DoQ class: not available (ST-19 changes `src/pages/Positions.js`; BLG-GOV-135).

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, ST-19 changes tooltip text only
- [x] **Strategy values checked:** ST-19 — Exit Zone tooltips now state no number; `strategy_rules.md` defines no R-multiple or Exit Zone rule (whole file searched, including §9 and §11), and `check_strategy_copy.py` passes. ST-18 and ST-20 touch no stop/grace/ATR/exit/sizing logic.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-13
- Comments: User-directed agent-mediated review against `claude/agents/director_of_quality.md` (the user: "agent-mediated review", 2026-11-13). Round 1: **Blocked**, 1 P2 and 2 observations. P2: the ST-19 v2.27 note in `positions.md` was inserted between the EXIT ZONE and UNKNOWN tooltip rows, ending the table early. Fixed in `cad3b87f` (note moved below the table, text unchanged, no version bump). Observations: EPIC-07 `qa_evidence_log` unset (set); signer format (used here). Round 2: **Approved**. The reviewer re-ran and cited: `pytest tests/test_check_data_model_drift.py` 17 passed; with `strip_rollback_sql` made a no-op, 3 tests fail, and with the old `INDEX_RE`, the `IF` test fails; on `data_model.md`, raw-minus-parsed names = {`IF`, `idx_trade_plans_ticker`}, parsed-minus-raw empty, CHECK names unchanged; `check_strategy_copy.py` 0 contradictions/0 literals; prompt size budget OK; scenario IDs OK (1232); execution-state consistency OK; ST-19 tooltip text byte-identical to decision record §7 option (b) and `positions.md` v2.27; job logs of run 43407147398 show both SC-LBG-06 cases passing; ST-18 bounds consistent and all four CLAUDE.md §6 steps present; `EMBEDDED_GATE_SIGNAL_RE` matches `~v4.9 (date-gated)` but not `TBD` or `v9.18`. Post-open CI-fix restatement: ST-19's follow-up `cad3b87f` (Markdown only) — all 7 workflows success, CI Pytest Suite 43414296538. Final CI per story: ST-18 `02587c70` 7/7; ST-19 `5a7db63b` 9/9 (Playwright E2E 43407147398) and `cad3b87f` 7/7; ST-20 `f1299c5c` and `6dc668d8` 7/7 each. Story-level authority: ST-18 Head of Specs Team (agent-mediated) Approved, `ESC-CLOSE-20261007-01` bound 2 extension recorded above — confirmed cleared. The human QA sign-off and Product Owner acceptance at the merge gate remain open (always-human).

## Merge Gate Confirmations

- **Director of Quality QA sign-off:** given by the human repository owner, acting as Director of Quality, in session at 2026-11-13T11:33:07Z ("give DOQ and PO acceptance"), before the merge. It accepts:
  - this evidence: ST-18, ST-19 and ST-20 all Pass, with no deviations;
  - the agent-mediated sign-off block above (round 1 Blocked, P2 fixed in `cad3b87f`; round 2 Approved);
  - the agent-mediated PR #2258 review comment (Director of Quality: Approved with Comments, 4 non-blocking observations).
- **Product Owner acceptance:** given by the human repository owner, acting as Product Owner, in the same instruction at 2026-11-13T11:33:07Z, before the merge. It accepts ST-18, ST-19 and ST-20 against `stage4_backlog_slice.md`. ST-18 AC 2 remains post-merge, tracked by BLG-GOV-419. The acceptance covers the two points the PR review raised for the Product Owner, and the owner made no separate comment on either:
  - the Head of Specs Team's recorded extension of `ESC-CLOSE-20261007-01` bound 2;
  - ST-18's mandatory "sets" wording, in place of the AC's "may".
- **P1/P2 found defects filed during this EPIC:** none. Follow-ups filed: BLG-SPEC-239 (P3), BLG-QA-264 (P4), BLG-QA-265 (P4), BLG-GOV-423 (P3), and a recorded BLG-GOV-422 scope-extension note for v9.18 planning.
- **Merged:** PR #2258, by the human repository owner (`sachiv1984`), at 2026-11-13T12:49:47Z, merge commit `c7153fba`. The merger holds both roles, so under `ESC-CLOSE-20261103-01` this merge also counts as a confirmation: QA sign-off and PO acceptance confirmed by merge, the human repository owner, 2026-11-13T12:49:47Z, merge commit `c7153fba`. This is in addition to the explicit in-session acceptance above.

