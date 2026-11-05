Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-05

# QA Evidence — EPIC-04: AI Output Checks & §13 Boundary

**EPIC:** EPIC-04 — AI Output Checks & §13 Boundary
**Cycle:** 2026-11-03__release-v9.15
**Branch:** `exec/2026-11-03__release-v9.15/EPIC-04`
**Sprint goal (cycle):** Make every route into Trade Entry show the §4.2 pre-entry checks and pre-fill the live FX rate (BLG-FE-244, BLG-FE-245, P1). Deliver Site Structure & Usability Phase 1: navigation v2/glossary, Dashboard "Today" and Journal area specs approved, one name per page, legacy Dashboard route removed, per-page tab titles. Ship v9.15's metric-correctness, AI-check, operations, data-model and governance items alongside.
**Test scenarios used:** `tests/test_briefing_summary_ticker_check.py`, `tests/test_ai_stop_time_focus_attribution.py`, `tests/test_journal_summary_language_check.py`, `tests/test_strategy_version_registry.py`

## Rulings and Delegations

| Record | Authority | Outcome |
|--------|-----------|---------|
| `ESC-EXEC-20261105-01` (ST-25, ST-27) | AI Compliance & Governance Officer (the user, in session) | Resolved 2026-11-05T08:50:24Z: (A″) approved as proposed. Recorded in `02becfc8` before the code commit `e6ba8e52`. |
| `ESC-EXEC-20261105-02` (ST-28) | Strategy Rules & System Intent Owner (the user, in session) | Resolved 2026-11-05T08:50:24Z: outcome (1), clarify. Applied in `122619e9` (case (c)). |
| `DEL-20261105-01` (ST-24) | AI Compliance & Governance Officer (the user, in session) | Carried post-merge 2026-11-05T08:50:24Z; tracked by `BLG-AI-27`. |
| ST-26 ruling-scope confirmation | AI Compliance & Governance Officer | Agent-mediated per §5.3; see "ST-26 Ruling-Scope Confirmation" below. |

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-24 | `ai_endpoints.md#POST /ai/daily-briefing` (check 3); `tests/test_briefing_summary_ticker_check.py` | Delegation `DEL-20261105-01` for the production caveat-token log read. It was not available in-sprint, so it was carried post-merge as `BLG-AI-27` (`aad0d041`), filed before the PR opens. | AC 1 (the token list with counts is recorded): **not met** in-sprint. AC 2 (each non-ticker found is added and covered by `test_non_ticker_words_ignored`, or none found is recorded): **not met** in-sprint. | Pass_with_deviation | `BLG-AI-27` (both ACs carried; AI Compliance & Governance Officer decision, 2026-11-05) |
| ST-25 | `ai_endpoints.md#POST /ai/journal-summary`; `ai_s13_boundary_test_suite.md` B-JS-04; `tests/test_journal_summary_language_check.py` | Ruling (A″) applied to `journal_summary_language_failures()`: "can" dropped from form (3); past-tense reported speech passes (`_in_reported_speech`); five new forms (1b), (6)–(9), plus "think about" in (1). B-JS-04 updated (suite 1.6), `ai_endpoints.md` 1.39 (`e6ba8e52`). DoQ review fix `ec0ada79`: the reported-speech exemption stops at its own sentence or clause, and form (6) accepts bullets. | AC 1 (ruling recorded before the code change): met, `02becfc8` precedes `e6ba8e52`. AC 2 (each BLG-AI-24 sentence has its ruled result in a test): met, `test_missed_advisory_forms_caught` (6 caught), `test_a_double_prime_descriptive_wording_passes` ("can" and reported-speech sentences pass). AC 3 (every ST-15 and v9.13 ST-18 case keeps its result): met, the existing parametrised cases are unchanged and pass. | Pass | None. Known false-positive class and exemption gaps tracked by `BLG-AI-30` (not ruled sentences, so no AC is affected) |
| ST-26 | `ai_endpoints.md#POST /ai/chat`; `tests/test_ai_stop_time_focus_attribution.py` | `_NON_TICKER_WORDS` adds AM, PM, EOD, EOW, EOM, IMO, IMHO, FYI, NOTE, TBD, ASAP, Q1–Q4, FY, YOY, VIX, GMT and BST; `ai_endpoints.md` 1.38 (`b937a396`). | AC 1 (each BLG-AI-25 sentence with focus `MU` held gets the MU note): met, `test_time_and_chat_words_do_not_block_focus` (5 cases). AC 2 ("TSLA's stop was hit last week." still gets no MU note; all ST-16 and ST-17 tests pass): met, `test_sentence_naming_a_ticker_not_held_not_given_to_focus` and the full file pass. | Pass | None |
| ST-27 | `ai_endpoints.md#POST /ai/journal-summary`; B-JS-04; `tests/test_journal_summary_language_check.py` | Form (4)'s "help" excludes a following explain / account for / show (A″ (iii)), same commit as ST-25 (`e6ba8e52`). | AC 1 (both BLG-AI-26 sentences return `[]`): met, `test_a_double_prime_descriptive_wording_passes`. AC 2 ("Tighter stops could help." and the other six BLG-AI-20 sentences still caught): met, `test_advisory_phrasings_caught` (7 cases). | Pass | None |
| ST-28 | `docs/product/decisions/decisions--2026-11-03__release-v9.15--ST-28-journal-summary-section13-reread.md`; `strategy_rules.md` §13.2, §13.5; `tests/test_strategy_version_registry.py` | Dated §13 re-read decision record. `strategy_rules.md` 1.24 → 1.25 (documentation only): a §13.2 sentence and a §13.5 roster row for the journal summary, a §16 Change Log row, and `DOCUMENTATION_ONLY_VERSIONS` "1.25" (`122619e9`). DoQ review fix `3ce6e3bd`: §13.2 is cut back to the single ruled sentence, and the briefing/chat check gap is stated. | AC 1 (dated re-read recorded in `docs/product/decisions/`): met. AC 2 (answers each clause cited; states whether the summary belongs on §13.5): met, §2 table and §4 of the record. AC 3 (outcome confirmed or clarified text under case (c), with Change Log row and registry entry): met, clarified; registry test passes; §15 re-run 0 actionable (27 files, independently re-counted by the DoQ review). | Pass | None. The daily briefing and chat have no output check enforcing the new §13.2 sentence: `BLG-AI-29` |

**AI evidence (AI-Touching Story Evidence Addendum):**
- ST-25/ST-27. Prompt-template version: unchanged (`JOURNAL_SUMMARY_PROMPT_VERSION` v1.1); only the output check changed. Boundary-language sample (illustrative, no live API access): "Moving stops to breakeven after a 2R gain could help explain the lower drawdown." now returns `[]`, and "Perhaps revisit stop placement." returns `["trading_change"]`. `scan_prescriptive` is part of `journal_summary_language_failures()` and runs on every case in the test file.
- ST-26. Prompt-template version: unchanged (`CHAT_PROMPT_VERSION` v1.2, `BRIEFING_PROMPT_VERSION` v1.3). Boundary-language sample (illustrative): "Your stop was hit at 3 PM." with focus `MU` held → "Your stop was hit at 3 PM. (MU stop last recalculated 2026-10-20 21:05 UTC)". The code appends a note and never edits model text.
- ST-24. No code change.

## ST-26 Ruling-Scope Confirmation

`sprint_backlog.md` ST-26 Notes asks for the AI Compliance & Governance Officer's agent-mediated confirmation that the additions stay within ruling `ESC-EXEC-20261027-02` (B), whose condition 2 is a minimum list.

- Status: **Approved.** Sprint Execution Engine (agent-mediated, AI Compliance & Governance Officer role — §5.3), 2026-11-05. The review was read-only.
- Within the ruling: condition 2 says "at least UK, US, … UTC", so the list is a minimum. `b937a396` only adds words to the frozenset, with no regex, caveat-wording, result-value or prompt change. Ruling `ESC-EXEC-20261030-03` defines a ticker-like token by reference to the list, so its mechanism is unchanged. Count: 20 words (11 + Q1–Q4 + 5), matching the commit and the contract.
- Residual risk (non-blocking): some listed words are also real tickers. MA and ON were already on the list; ST-26 adds PM, the only new word in `backend/tickers_full_list.csv` (checked word by word with `grep -cE`). A held PM is still cited. A PM that is not held is no longer caveated in the briefing, and in chat "PM's stop was hit last week." with focus MU held (PM not held) gets the MU note. This was confirmed by an in-process probe. It is unlikely and fails soft: a note is added and model text is never edited. Tracked by `BLG-AI-28`, which also covers MA and ON.
- Tests: the two test files pass (103 passed). `test_non_ticker_words_ignored` is parametrised over the whole list, so all 20 words are covered.

## Agent-Mediated Director of Quality Review

- Pass 1 (2026-11-05): **Blocked**, with 2 blocking findings:
  1. Form (6) let the reported-speech exemption reach into the next sentence and across ";". Fixed in `ec0ada79` with next-sentence, ";" and bullet tests.
  2. §13.2 carried a second, unruled sentence claiming briefing and chat output checks that do not exist. Fixed in `3ce6e3bd`; the gap is tracked by `BLG-AI-29`.
- Non-blocking findings:
  - Contract wording for form (6) and form (8): fixed in `ec0ada79`.
  - Form (6) false positives and exemption speaker/spillover gaps: `BLG-AI-30`.
  - ST-24 `acceptance_verified`: a note was added in `execution_state.json`.
  - Uncommitted artefacts: committed.
  - Merge `origin/main` before the PR (CLAUDE.md §8).

## QA Test Coverage

- Scenarios run: `DATABASE_URL=<stub> backend/.venv/bin/python3 -m pytest tests/ -k "journal or ai_ or briefing or chat or debrief"` → 450 passed, 10 skipped. `tests/ -k strategy` → 149 passed. CI per commit: see Comments.
- Regression areas checked: briefing ticker caveat (check 3, which shares `_NON_TICKER_WORDS`), chat and briefing stop-time attribution, journal-summary regenerate/fallback and audit rows, the monthly P&L narrative and debrief scans (unchanged), and the strategy version registry.
- Known deviations: none found in the deviation checks for ST-25 to ST-28. ST-24 is graded Pass_with_deviation and tracked by `BLG-AI-27`. Follow-ups from the reviews: `BLG-AI-28` (non-ticker words that are real tickers), `BLG-AI-29` (no briefing/chat check for §13.2), `BLG-AI-30` (form (6) false positives, exemption gaps).
- Frontend testing gate: N/A. No story changes `src/**`; all ACs are backend or documentation.

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object. N/A, no frontend change.
- [x] **Strategy values checked:** N/A. No stop/grace/ATR/exit/sizing logic touched. ST-26 changes only which sentences are attributed to the stop-time note, not any stop value; ST-28 is a §13 text change.
- Signed off by:
- Date:
- Comments:
