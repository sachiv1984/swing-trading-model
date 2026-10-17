Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-17

# QA Evidence — EPIC-06 — Governance & Spec Tooling

**EPIC:** EPIC-06 — Governance & Spec Tooling
**Cycle:** 2026-10-16__release-v9.13
**Sprint goal:** Make the Daily Position Monitor's exit confirmation record real exits through `POST /positions/{id}/exit` (BLG-FE-226, P1), give exit reasons one allowed list mapped to §8, and make CI fail on any frontend call to a route that does not exist. Also ship v9.13's stop and sizing correctness, AI output safety, operations and governance items.
**Test scenarios used:** `tests/test_scan_backlog_gate_conditions_explicitly_ungated.py`, `tests/test_scan_backlog_gate_conditions_known_non_gate_dates.py`, `tests/test_check_data_model_drift.py`, `tests/test_strategy_version_registry.py` (all pytest). There are no Playwright scenarios: no story changes a frontend file.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-35 | `scripts/scan_backlog_gate_conditions.py` (Case D) | `classify_item()` treats a gate field reading `None`/`N/A`/`-`/`—` (case-insensitive, trimmed, optional trailing period) as ungated. Those items get a separate informational "explicitly ungated" count, in the text report and under a JSON key. Commit `6a4a5fd0`. | AC 1 explicit no-gate values are ungated and counted: Pass (parametrised tests). AC 2 the 17 named items leave the gated list, and the gated count goes 124 → 107 on the 2026-10-16 scan. `BLG-GOV-382` is still gated: Pass (live-backlog test plus a manual scan). AC 3 new tests pass under the venv. The ready-pool view of the 17 is recorded in the EPIC-06 PR body (15 keep a slot; BLG-GOV-185 and BLG-GOV-200 look already done and are flagged for grooming): Pass. | Pass | None |
| ST-36 | `scripts/scan_backlog_gate_conditions.py` (Case D) | `KNOWN_NON_GATE_DATES` allow-list: each entry has an item, an optional date, a reason and a review date. Listed dates are ignored for date-lapse, and the entries are reported in a separate "known non-gate dates" section. BLG-OPS-53 ignores only its ship date, so its real `clears 2026-11-22` still lapses. BLG-FEAT-92 ignores all dates, because its gate is inherited and has no date of its own. Commit `c89dba4e`. | AC 1 allow-list with a reason and review date, reported separately: Pass. AC 2 counting-start and provenance dates are not date-lapsed. Restated AC: tested with a fixture built from the 2026-10-06 gate text. Re-running the scan on the 2026-10-06 backlog (`65a307fe`) takes the lapsed list from 8 to 6, and both items leave it: Pass. | Pass | None |
| ST-37 | `scripts/check_data_model_drift.py`; `docs/specs/data_model.md` (CREATE TABLE blocks) | New "default mismatch" class. `DEFAULT` is parsed from each CREATE TABLE block, and `column_default` is selected from `information_schema.columns`. `normalize_default()` drops casts, unquotes literals, compares numbers numerically and treats `CURRENT_TIMESTAMP` as `now()`. Commit `935ea1fc`. | AC 1 `DEFAULT 0` vs live NULL, and the reverse, is reported: Pass. AC 2 `0` vs `0::numeric` and `'[]'::jsonb` vs `'[]'` raise no false positive: Pass. AC 3 the tool stays read-only: every `cur.execute` is a `SELECT`, asserted by a test. The existing drift/orphan/dashboard tests pass: 44 = 36 existing + 8 new: Pass. Fixtures only; no live DB was queried. | Pass | None |
| ST-38 | `claude/strategy/strategy_rules.md` §13.3, §13.5 (v1.18) | §13.3's third paragraph is replaced, word for word, by the v9.10 addendum's proposed text. The §13.5 Gap Risk Flag row records Binding Condition 6 as met (v9.10). v1.18 Change Log row (documentation only, §16 template), and 1.18 is added to `DOCUMENTATION_ONLY_VERSIONS`. Commit `63314028`. | AC 1 §13.3 paragraph replaced: Pass. AC 2 the §13.5 row records BC 6 as met: Pass. AC 3 version bump, Change Log row (documentation only) and §15 grep recorded (55 files, 0 actionable): Pass. | Pass | None |
| ST-39 | `claude/strategy/strategy_rules.md` §13.5 (v1.18) | The PO-05 roster row no longer says PO-05 reuses IT-06. It uses the BLG-GOV-377 Scope wording. Shares ST-38's commit and bump. Commit `63314028`. | AC 1 the PO-05 row reads as in the Scope: Pass. AC 2 Change Log row and §15 grep recorded: Pass. | Pass | None |
| ST-40 | `claude/roadmap/role_share_history.md` (v9.8–v9.10 rolling line) | Compound count corrected from 19 to 17 of 21, re-derived with `scripts/compute_role_share_history.py`, with an inline correction note. PMO Lead approval `ESC-EXEC-20261017-01` (agent-mediated, §5.3), then reclassified `autonomous`. Commit `3903e9fc`. | AC 1 the compound count matches the script's v9.10 output (17 of 21): Pass. | Pass | None |

**QA test coverage:**
- Scenarios run: the four pytest files above, under `backend/.venv/bin/python3 -m pytest` (gate scan 40 passed; data-model drift/orphan/dashboard 44 passed; strategy version registry 15 passed), plus CI on the branch (see Comments).
- Regression areas checked: Release Planning §1.3a gate-scan output (existing date-disambiguation and gating-item-shipped tests unchanged and passing); the data-model drift detector's existing column/nullable/index/CHECK checks; SI-04 strategy version registry coverage rule.
- Known deviations: None found. All stories' deviation checks completed with nothing to file.

**Story-level authority sign-offs (BLG-GOV-14):** ST-40, PMO Lead (agent-mediated, §5.3), `ESC-EXEC-20261017-01`, cleared 2026-10-17. ST-38/ST-39 were written under RISK-02 option (a): named `strategy_rules.md` writes, authorised by the user with the Strategy Rules & System Intent Owner at sprint planning on 2026-10-16. No further ruling was needed for this documentation-only text.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object. N/A, no frontend change.
- [x] **Strategy values checked:** N/A. No stop/grace/ATR/exit/sizing logic is touched. ST-38/ST-39 change only §13 boundary text; no §5–§11 value or formula changes.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-10-17
- Comments: The user directed this agent-mediated sign-off on 2026-10-17. Decision: Approved on the first pass, with no blocking findings. The reviewer re-ran each check and recorded its own evidence:
  - (1) The 7 named pytest files pass, 99 tests (40 + 44 + 15), with a stub DATABASE_URL. No database was queried.
  - (2) The 2026-10-16 gate scan reports 107 gated items and 17 explicitly ungated. BLG-GOV-382 is still gated.
  - (3) Scanning the 2026-10-06 backlog (`65a307fe`) gives 8 date-lapsed items with the old script and 6 with the new one. Only BLG-OPS-53 and BLG-FEAT-92 drop out.
  - (4) The §13.3 paragraph is verbatim against the v9.10 addendum: the diff is empty and both are 636 bytes. The PO-05 row matches the BLG-GOV-377 Scope.
  - (5) `normalize_default` was probed on the AC pairs and gives no false positives and no false negatives.
  - (6) No `src/` file changed. The only `backend/` change is the 1-line `DOCUMENTATION_ONLY_VERSIONS` entry.
  - (7) All 14 ACs appear in the table, and the grades are correct.

  Non-blocking notes (recorded in the PR, no backlog item needed):
  - N1: the ST-35 ready-pool view goes in the PR body (row reworded).
  - N2: BLG-FEAT-92's whole-item entry disables date-lapse checking for that item. This is mitigated by the `present` flag and the 2027-01-16 review date.
  - N3: `normalize_default` treats text `'0'` and numeric `0` as equal. A later `ALTER … SET DEFAULT` would show as a mismatch. Both are acceptable for a report-only tool.
  - N4: the BLG-GOV-382 assertion in the live-backlog test is conditional on the item existing, so it can retire cleanly when the item is archived.

  Story-level authority: PMO Lead, `ESC-EXEC-20261017-01` (cleared). CI on `c6a4c2e9` and `3903e9fc`: all 7 workflows succeeded on each. The autonomous class (BLG-GOV-19) is not claimed. ST-40 was `delegated_decision` in the sealed plan and was reclassified only after its ruling. Under `execution_prompt.md` §3.2.A the engine does not resolve a borderline Criterion 1 call in its own favour, so this EPIC takes the standard Director of Quality sign-off. This matches the v9.12 EPIC-06 precedent.
