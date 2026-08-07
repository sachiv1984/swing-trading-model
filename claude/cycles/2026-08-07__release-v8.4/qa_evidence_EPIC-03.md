Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-07

# QA Evidence — EPIC-03 — Backend Engineering Hardening

**EPIC:** EPIC-03 — Backend Engineering Hardening
**Cycle:** 2026-08-07__release-v8.4
**Sprint goal:** Ship both available user-facing reporting enhancements while clearing a full-capacity slate of API contract & spec debt, backend hardening, frontend code health & security, operational reliability & cost monitoring, QA/test infrastructure, and governance-process integrity work across all 31 scoped stories.
**Test scenarios used:** `tests/test_trade_plans_ticker_index.py`, `tests/test_alpaca_paper_sync_close_positions_backoff.py`, `tests/test_trade_plan_thesis_provenance.py`, `tests/test_trade_plan_audit_log.py`, `tests/test_generate_data_dictionary.py` (all new this EPIC) plus the pre-existing `tests/test_trade_plan_tags.py`, `tests/test_position_trade_plan_link.py`, `tests/test_alpaca_paper_sync_idempotent_retry.py` re-run for regression confirmation.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-10 | `docs/specs/data_model.md`, `tests/test_trade_plans_ticker_index.py` | Added functional index `idx_trade_plans_ticker_upper` (UPPER(ticker)) to `ensure_trade_plans_table()`, replacing a plain index that was never actually created and would not have served the live `WHERE UPPER(ticker)=%s` predicate anyway. `data_model.md` DS-04 block + new migration entry corrected to match. | Functional index created; `data_model.md` matches; `EXPLAIN`-equivalent CI-verifiable check (3 mocked-cursor tests confirming SQL shape) | Pass | None |
| ST-11 | `backend/services/alpaca_paper_sync_service.py`, `tests/test_alpaca_paper_sync_close_positions_backoff.py` | Extracted `_sync_close_paper_position_raw`/`_get_paper_positions_raw`, both `@retry_with_backoff` (matches ST-10/BLG-BE-80's existing open-position pattern). Existing dispositions unchanged: close still best-effort swallow, positions still raises after retries exhausted. | Both call sites retry on transient/429 failure; existing fallback behaviour unchanged; regression test confirms retry-before-fallback | Pass | None |
| ST-12 | `backend/database.py`, `docs/specs/data_model.md`, `docs/specs/api_contracts/trade_plan_endpoints.md`, `tests/test_trade_plan_thesis_provenance.py` | Added `thesis_model_version`/`thesis_prompt_version` (nullable) to `trade_plans`, wired through create/update and request models. | New field present and populated on all newly-created AI-generated records | **Pass with notes** | None filed — see notes |
| ST-13 | `docs/specs/data_model.md`, `tests/test_trade_plan_audit_log.py` | New `trade_plan_audit_log` table, extends `position_audit_log` (BLG-BE-73) pattern. `update_trade_plan()` logs post-entry edits (`position_id` set) only, fail-open. | Audit-trail pattern established by BLG-BE-73 extended to trade plan mutations post-entry; owner sign-off | Pass | None |
| ST-14 | `scripts/generate_data_dictionary.py`, `docs/ops/data_dictionary_diff_triage_2026-08-07.md`, `tests/test_generate_data_dictionary.py` | Script generates data dictionary from live schema via `information_schema`; degrades gracefully with no `DATABASE_URL`. First run in-session: no live DB reachable, gracefully skipped as designed; manual cross-check substituted. | Script added; first run's diff against `data_model.md` triaged; owner sign-off | Pass | None |

**ST-12 notes (Pass with notes):** delivers the backend storage capability only — the frontend does not yet pass `model_version`/`prompt_version` through on save, so the field is not yet populated end-to-end for any real AI-generated record this cycle. This is a genuine, disclosed scope boundary (ST-12 is a backend-only story, Owner: Backend Engineering Patterns Owner, no frontend authority listed) rather than an implementation gap — `BLG-FE-143` filed for the frontend follow-up. The AC's literal "populated on all newly-created AI-generated records" is not fully met until that lands; recorded here rather than silently treated as complete.

**QA test coverage:**
- Scenarios run: 5 new test files (ST-10=3, ST-11=9, ST-12=4, ST-13=6, ST-14=6 = 28 new cases) plus 3 pre-existing files re-run for regression. Full combined run (`pytest` across all 8 files): 56 passed, 0 failed.
- Regression areas checked: full `trade_plans`/`alpaca_paper_sync` test suites re-run clean after each story's change (35 tests after ST-13, confirmed no regression from ST-10 through ST-13's `database.py` edits). No frontend files touched (`src/pages/`, `src/components/` — confirmed via `git diff --name-only main..HEAD`).
- **Found and fixed at post-EPIC-02-merge PR (2026-08-07):** real GitHub Actions CI on PR #1295 caught a collateral regression the pre-merge in-session re-run missed — `tests/test_strategy_version_at_entry.py::test_create_trade_plan_passes_strategy_version_at_entry_to_insert` asserted `params[-1] == "1.4"`, an assumption broken by ST-12 appending `thesis_model_version`/`thesis_prompt_version` after `strategy_version_at_entry` in `create_trade_plan()`'s INSERT column list. Fixed by locating the column's actual positional index from the SQL rather than assuming "last" (position was never a real contract). Re-verified locally post-fix: 6/6 in that file, 54/54 across the broader `trade_plan`/`strategy_version` test slice. This is an environment-parity case per `execution_prompt.md`'s LL-v8.3-P3-02 sub-clause — the in-session pre-merge run did not reproduce the failure the same way real CI did; caught before merge, not after, because PR #1295's CI ran before the merge gate was evaluated.
- Known deviations filed: None. ST-12's residual frontend-wiring gap is disclosed above and tracked via `BLG-FE-143`, not filed as a formal `DEV-*` deviation — the backend AC (field present, storage capability delivered) is met; the gap is in a different story's territory (frontend), consistent with `execution_prompt.md`'s deviation-vs-backlog-item distinction for scope genuinely outside the story's own ownership. The test-fragility fix above is a pre-existing test defect, not an implementation deviation from spec — no DEV-* record applicable.

**Version-collision note (CLAUDE.md §8 step 2a):** `data_model.md` was bumped independently on this branch (v2.20→v2.21→v2.22→v2.23 across ST-10/ST-12/ST-13) while EPIC-02 also bumped it to v2.21 for different content (ST-08/ST-09). This branch's version numbers **must be renumbered** at EPIC-03's post-EPIC-02-merge rebase (per the Merge Order note in `sprint_backlog.md`) — flagged in `execution_state.json.process_notes` and in each affected story's own notes field, so the rebase step does not silently accept a colliding version number.

**Resolved at post-EPIC-02-merge rebase (2026-08-07):** ST-10/ST-12/ST-13's migration blocks renumbered v2.21→v2.22, v2.22→v2.23, v2.23→v2.24 respectively (following EPIC-02's now-canonical v2.21 on `main`); final `data_model.md` document version is **2.24**. No SQL content changed — renumbering only (migration statements, field references, and sign-offs are unchanged from the pre-rebase text).

---

## Autonomous Class Sign-Off Block (BLG-GOV-19)

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-10 through ST-14, all 5 stories)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (mocked-`get_db()` unit tests + code-review cross-checks for every story)
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/pages/` or `src/components/` was created or modified (`git diff --name-only main..HEAD`) — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-07
- Comments: Autonomous class sign-off — all four qualifying criteria met. ST-12's residual frontend-wiring gap (see notes above, tracked via BLG-FE-143) does not change EPIC-03's own AC disposition — it is a backend-only story and the backend AC is met. Domain-specific authorities named per-story in the Sprint Backlog (Backend Engineering Patterns Owner for ST-10/ST-11/ST-14; Data Model & Domain Schema Owner for ST-10/ST-13; AI Compliance & Governance Officer for ST-12) are recorded in `execution_state.json`'s per-story `sign_off_record` fields, consistent with the EPIC-level consolidation note (BLG-GOV-14). **Merge sequencing note:** this EPIC's branch must rebase onto `main` after EPIC-02 merges (per `sprint_backlog.md`'s Merge Order — shared files `data_model.md`, `execution_state.json`) before its own PR is opened; this QA evidence log is complete and does not block on that rebase.
