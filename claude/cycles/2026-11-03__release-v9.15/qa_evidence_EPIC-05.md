Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-06

# QA Evidence — EPIC-05: Operations, Security & Market-Data Monitoring

**EPIC:** EPIC-05 — Operations, Security & Market-Data Monitoring
**Cycle:** 2026-11-03__release-v9.15
**Branch:** `exec/2026-11-03__release-v9.15/EPIC-05`
**Sprint goal (cycle):** Make every route into Trade Entry show the §4.2 pre-entry checks and pre-fill the live FX rate (BLG-FE-244, BLG-FE-245, P1). Deliver Site Structure & Usability Phase 1: navigation v2/glossary, Dashboard "Today" and Journal area specs approved, one name per page, legacy Dashboard route removed, per-page tab titles. Ship v9.15's metric-correctness, AI-check, operations, data-model and governance items alongside.
**Test scenarios used:** `tests/test_nightly_computations.py`, `tests/test_momentum_signal_run_marker.py`, `tests/test_rebalance_exit_signal_numpy_regression.py`, `tests/test_ci_code_changes.py`

## Decisions and Escalations

- `ESC-EXEC-20261105-05` (ST-31, Scope): resolved in session on 2026-11-05 by the Product Owner (the user). On a governance-only or docs-only change, CI Pytest Phase A runs the docs-coupled tests; the other four suites skip. No backlog remainder.
- ST-33: returned to backlog in flight on 2026-11-05, authorised by the Product Owner (the user, in session). Conditional story (`release_planning_prompt.md` §1.4b, gate 2026-11-09) whose gate cannot clear before EPIC-05 merges; the expected path per `sprint_backlog.md` ST-33 Notes, not a deviation. `BLG-OPS-197` stays open. No delegation record was raised.
- `DEL-20261105-04` (ST-29, Anthropic console read): Unblocked in session on 2026-11-06. The Cybersecurity & Trust Lead (the user) supplied the key list, names and dates only.
- **ST-29 pre-existing problems accepted for post-merge (Product Owner and Director of Quality, the user, in session, 2026-11-06T10:06:48Z):** the overdue Anthropic key rotation (`BLG-OPS-214`, P1) and the second copy of the key in the `REACT_APP_ANTHROPIC_API_KEY` GitHub secret (`BLG-OPS-213`, P2) are carried past the EPIC-05 merge. The user chose this over rotating before merge. Both items stay open and tracked.
- No live system access by the engine. Local pytest used a stub `DATABASE_URL` (CLAUDE.md §9). The ST-29 published-bundle check read the public `gh-pages` branch by match count only.

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-29 | `docs/security/anthropic_api_key_scope_audit_2026-11-06.md`; `docs/ops/api_key_rotation_policy.md` | Six-month audit record: a code audit of every `ANTHROPIC_API_KEY` reference and Anthropic client, a count-only search of the published GitHub Pages bundle, and the console key list (one key, created 2026-05-25, last used 2026-10-14). `external_api_credential_inventory.md` v1.2 records the rotation status. Commit `5e83a975`. | AC 1 scope minimal, endpoints named: **not met as worded**. The key is used by six live AI endpoints, each named, all shipped features, but the register omits the v9.11 narrative endpoint (`BLG-SPEC-223`); the GitHub Pages build gets a second copy of the key as `REACT_APP_ANTHROPIC_API_KEY`, absent from the published bundle (`BLG-OPS-213`), so the key is not used *only* by register endpoints. AC 2 rotation per schedule: **not met**; the first rotation was due 2026-08-25 and has not happened. AC 3 findings documented: **met**. | Pass_with_deviation | AC 1 carried by `BLG-SPEC-223` and `BLG-OPS-213` (P2); AC 2 by `BLG-OPS-214` (P1) |
| ST-30 | `docs/specs/api_contracts/signal_endpoints.md#POST /signals/rebalance-exit` (v1.11); `docs/specs/data_model.md#DS-39` | Each completed momentum signal run writes a `momentum_signal_runs` marker (DS-39, v2.68) after saving its signals. `POST /signals/rebalance-exit` ranks from today's latest marker. No marker (run missing, or failed part way) → no signals, 503, `rebalance_exit` error. A failed marker write is logged and later reads as a missing run. Commit `e0329f64` (with ST-32). | AC: with no completed screener run today, rebalance-exit creates no signals and raises an alert (test). RX-08 (no marker, even with today's signal rows → `screener_run_missing`, no signals); RX-09 (endpoint → 503, job recorded as error, `curl -f` in `rebalance-exit.yml` fails); `test_failed_run_records_no_marker`. "Screener run" read as the momentum signal run, as `strategy_rules.md` §8.4 states ("that day's completed momentum signal run"). | Pass | None. Out-of-scope follow-up `BLG-OPS-212` (DS-39 Live Confirmation, post-deploy) |
| ST-31 | `.github/actions/detect-code-changes/action.yml`; `.github/workflows/ci-tests.yml`; `tests/docs_coupled.py` | `changes` job in the five workflows; suite jobs skip only when detection reports `false`, and a skipped job reports success. Phase A always runs and, on a governance-only change, runs `pytest tests/ --docs-coupled-only` (static selection, re-derived each run). Fails safe to running everything. Commit `898003a9`. | AC 1 governance-only PR reports all required checks without running the suites: shown on the branch at `cef1df61` (a `claude/`-only push). The four suites and Phase B were skipped and reported success; Phase A ran the docs-coupled subset and passed. The PR-on-`main` confirmation is seal-marked `post-merge`, tracked by `BLG-OPS-211`. AC 2 code PR still runs them: on `898003a9` all five suites ran and passed (CI Pytest 42083447473, Smoke 42083447471, Service Coverage 42083447599, Golden 42083447457, Integration 42083447464); the pull-request event path of the detector has not run yet; the PR-event run IDs are added here when the PR opens. 42 structural and classifier tests in `tests/test_ci_code_changes.py`. | Pass_with_deviation | AC 1 narrowed by Product Owner ruling `ESC-EXEC-20261105-05` (Phase A runs the docs-coupled subset instead of skipping; no remainder). AC 1 on `main` post-merge, `BLG-OPS-211` |
| ST-32 | `docs/specs/api_contracts/signal_endpoints.md#POST /signals/rebalance-exit` (v1.11); `docs/specs/data_model.md#DS-39` | Same change as ST-30: a completed run with zero qualifying tickers writes an empty marker, which is an empty ranking, not a missing run. Commit `e0329f64`. | AC: zero-qualifier completed run → signals for non-risk-off, post-§8.1 positions and no 503 (RX-11: the plain position and the in-grace position below its stop get signals; the risk-off and post-grace at-stop positions do not; RX-12: endpoint returns 200); missing run → 503 as now (RX-08, RX-09). Marker writes: `test_zero_qualifier_run_records_an_empty_marker`, `test_qualifying_run_records_the_ranked_tickers_after_saving_them`. | Pass | None |
| ST-33 | `docs/specs/data_model.md#DS-36`; `docs/ops/data_pipeline_cost_baseline.md` | Not executed. | AC 1 and AC 2 (production data, seal-marked `post-merge`). | Returned to backlog (conditional, gate 2026-11-09 not cleared) | None; expected path. `BLG-OPS-197` stays open |

## QA Test Coverage

- Scenarios run: full backend suite with `backend/.venv/bin/python3 -m pytest` and a stub `DATABASE_URL` (CLAUDE.md §9), after ST-30/ST-31/ST-32: 3402 passed / 38 skipped. Docs-coupled subset alone (`--docs-coupled-only`): 1086 passed / 5 skipped, 45s.
- CI: on `898003a9` (ST-31 head, covers `e0329f64`) every workflow `success`, including all five code suites. On `cef1df61` (`claude/`-only), the four suites and Phase B were skipped and Phase A ran the docs-coupled step. `5e83a975` (ST-29) is docs-only, so the suites skip by design.
- Regression areas checked: month-end rebalance (§8.4 ranking, §8.1/§8.2 precedence, grace), momentum signal generation, `POST /signals/rebalance-exit` responses, CI workflow triggers and required checks, test collection (conftest hook added; full suite unchanged).
- Spec and gate scripts: OpenAPI three-way drift none (pre-commit); API performance baseline drift passed (no new endpoint); contract heading lint passed; contract example freshness no drift; backlog item integrity OK; `check_specs_index_freshness.py` output identical to the pre-change baseline.
- Known deviations: ST-29 (`Pass_with_deviation`: AC 1 `BLG-SPEC-223`/`BLG-OPS-213`, AC 2 `BLG-OPS-214`); ST-31 (`Pass_with_deviation`, ruling `ESC-EXEC-20261105-05`, no remainder). All other deviation checks completed with nothing to file in a canonical spec. Out-of-scope findings filed: `BLG-OPS-212`, `BLG-SPEC-223`, `BLG-OPS-213`.
- Frontend testing gate: N/A. No story changes `src/**`.
- Governance self-consistency: N/A. No story edits a governance prompt or `OPERATIONAL_GUIDE.md`.

## Agent-Mediated Director of Quality Review

- Pass 1 (2026-11-06): **Blocked**, 3 blocking findings, all applied:
  1. ST-31 graded `Pass` although the ruling narrows AC 1 → regraded `Pass_with_deviation`, naming `ESC-EXEC-20261105-05`.
  2. ST-31 AC 2 claimed a PR re-confirmation that did not exist yet → reworded to the push runs on `898003a9`; PR-event run IDs to be added at PR open.
  3. ST-29 AC 1 graded "met" although the register omits an endpoint and a second copy of the key exists → "not met as worded" (`BLG-SPEC-223`, `BLG-OPS-213`). The pre-existing P1/P2 problems ST-29 found (`BLG-OPS-214`, `BLG-OPS-213`) need documented Product Owner and Director of Quality acceptance before the "No unresolved P0 or P1 deviations" line can be ticked (`delivery_verification_prompt.md` no-remainder rule). **Resolved 2026-11-06: the user, as Product Owner and Director of Quality, accepted carrying both post-merge (see Decisions and Escalations).**
- Non-blocking, applied: test for a run that fails while saving signals (`test_run_that_fails_while_saving_signals_records_no_marker`).
- Non-blocking, recorded: (a) a deploy that lands on a month-end after the 16:00 UTC momentum run gives one false 503 that day (no marker yet; DS-39 Deploy order states it); (b) the docs-coupled selector is a static text match: `changelog_service.py`, `changelog_digest_service.py` and `ai_spend_trend_service.py` read `docs/product/changelog.md` at runtime, so a future test reaching them only through `TestClient` would not be selected (none does today: 72 of 261 files selected, no reader missed); (c) ST-30/ST-32 correctness, ST-31 fail-safe paths and required checks, no secrets recorded, and spec bookkeeping all checked with nothing found.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations. The P1 (`BLG-OPS-214`) and P2 (`BLG-OPS-213`) problems ST-29 found are carried post-merge with documented Product Owner and Director of Quality acceptance (Decisions and Escalations); to be repeated in `verification_report.md` §4 at Phase 4.
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object. N/A, no frontend change.
- [x] **Strategy values checked:** ST-30/ST-32 — `strategy_rules.md` §8.4 (ranking from that day's completed momentum signal run; no completed run → no recommendation and an alert; §8.1 after grace and §8.2 take precedence; applies during grace per §6.3). No story touches stop, ATR or sizing values.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-06
- Comments:
  - Pass 1: Blocked (3 blocking: ST-31 grade, ST-31 AC 2 evidence claim, ST-29 AC 1 grade and P1/P2 acceptance). All applied. Pass 2: Approved.
  - Story grades: ST-29 Pass_with_deviation (AC 1 `BLG-SPEC-223`/`BLG-OPS-213`, AC 2 `BLG-OPS-214`); ST-30 Pass; ST-31 Pass_with_deviation (ruling `ESC-EXEC-20261105-05`, no remainder; AC 1 on `main` post-merge `BLG-OPS-211`); ST-32 Pass; ST-33 returned to backlog (conditional, expected path).
  - Story-level authorities: ST-31 Product Owner (`ESC-EXEC-20261105-05`); ST-29 Cybersecurity & Trust Lead console evidence (`DEL-20261105-04`); ST-29 carry-forward acceptance by the Product Owner and Director of Quality; ST-33 return by the Product Owner. All given in session by the user and cleared.
  - CI: every workflow `success` on `898003a9` (all five code suites ran). Pending before merge: the PR-event runs (the detector's pull-request path, ST-31 AC 2 on the PR) and CI on the PR head, added to this log when the PR opens.
  - This agent-mediated sign-off does not satisfy the always-human merge-gate rows (QA sign-off and PO acceptance).

## Merge Gate Confirmations

*(Written when the merge is recorded.)*
