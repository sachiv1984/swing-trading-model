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
| ST-19 | `docs/specs/frontend/pages/positions.md` §Position Lifecycle State Badge (v2.27); `positions-decision-first/decision_record.md` §7 | PROFITABLE and EXIT ZONE tooltips take RISK-05 option (b) wording, with no R multiple; option (a) wording removed from the spec (`5a7db63b`). | The tooltip's threshold is no longer stated as a number; `scripts/check_strategy_copy.py` passes — **met** (0 contradictions, 0 literals). Wording-only AC, also covered by Playwright SC-LBG-06 (CI run 43407147398). | Pass | None |
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

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, ST-19 changes tooltip text only
- [ ] **Strategy values checked:** ST-19 — Exit Zone tooltips now state no number; `strategy_rules.md` defines no R-multiple or Exit Zone rule (whole file searched, including §9 and §11), and `check_strategy_copy.py` passes. ST-18 and ST-20 touch no stop/grace/ATR/exit/sizing logic.
- Signed off by:
- Date:
- Comments:
