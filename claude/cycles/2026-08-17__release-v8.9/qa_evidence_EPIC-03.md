Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-20 (ST-09 completed post-merge — see DEV-EPIC03-ST09-01); prior — 2026-08-18

# QA Evidence Log — EPIC-03 (Backend Reliability & Performance)

**EPIC:** EPIC-03 — Backend Reliability & Performance
**Cycle:** 2026-08-17__release-v8.9
**Sprint goal:** Ship v8.9: eliminate the two live risk-management stop-price defects on open positions (breakeven-floor ratchet, currency-basis mismatch) and deliver the sector-aware position sizing, pre-commit risk simulator, AI post-trade debrief, and in-app backtesting foundations of the Trade Intelligence Expansion — while clearing this cycle's reliability, QA, ops, and governance debt.
**Test scenarios used:** `tests/test_trade_plans_ticker_index.py` (3 scenarios); `tests/test_ensure_trade_plans_table_memoization.py` (2 scenarios, new); `tests/test_position_state_history.py` (6 scenarios, 2 new); full backend suite regression run

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-08 | `docs/ops/db_index_audit_arc4_2026-08-06.md` | Root cause: 11 per-request call sites of the DDL-heavy `ensure_trade_plans_table()` vs. 0 for the ~4x-faster sibling `GET /positions/tags`. Fix: process-global `_trade_plans_table_ensured` memoization flag so DDL/column-migration calls run once per process, not once per request. New `tests/test_ensure_trade_plans_table_memoization.py` (2 tests); fixed a test-order hazard the new flag introduced in the pre-existing `test_trade_plans_ticker_index.py` (2 rounds of review, 2 independent vacuous-assertion bugs found and fixed, each empirically re-verified via temporary regression injection). | Root cause identified; fix applied or filed as a follow-up with root cause documented; Re-measured p50 within the same order of magnitude as `GET /positions/tags` (staging-only — production/staging latency measurement, not CI-reproducible, per sprint_backlog.md); Backend Engineering Patterns Owner sign-off | Pass with notes | None |
| ST-09 | N/A — staging-only, no canonical spec beyond `docs/ops/api_performance_baseline.md` §36 (target update location) | Completed post-merge, 2026-08-20. EPIC-03 merged (PR #1454); a real post-merge invocation of `POST /digest/si05/send` was triggered (`si05-weekly-digest.yml` `workflow_dispatch`, run 32342881081). Render's captured logs confirmed the request succeeded (200 OK) but the expected `"SI-05 digest sent... in %.2fs"` line was genuinely absent — root-caused to production's `uvicorn` process having no root logging configuration, so no `logger.info()` call anywhere in the app reaches Render's log pipeline (filed as `BLG-BE-107`, a pre-existing, unrelated platform gap this story did not introduce). Product Owner accepted an interim GitHub Actions step-timing proxy in its place (same methodology already used and accepted once before for this endpoint, §36.3/`BLG-OPS-54`) — recorded in `docs/ops/api_performance_baseline.md` §36.5. | A real invocation's Render log confirms the `"SI-05 digest sent... in %.2fs"` line is present with a real elapsed-time value; `docs/ops/api_performance_baseline.md` §36 updated with the real timing | Pass with deviation | `DEV-EPIC03-ST09-01` (P3) |
| ST-10 | `docs/specs/data_model.md#DS-13`; `tests/test_position_state_history.py` | Reordered `refresh_position_lifecycle()` so the primary write (`update_position_lifecycle_state`) runs before the audit write (`create_position_state_history_entry`), preventing a phantom `position_state_history` row if the primary write fails. Reviewed `position_audit_log`'s 3 call sites — already correctly ordered, no fix needed there. Added `data_model.md` DS-13 cross-reference note documenting the ordering decision. 2 new regression tests using live-closure call-order tracking. | A documented, deliberate fix-or-accept decision exists for both audit-write call sites (`position_state_history`, `position_audit_log`); If fixed, a test demonstrates the audit row is not written when the primary write fails; If accepted, the risk and rationale are recorded in `data_model.md`'s relevant DS entries | Pass | None |
| ST-11 | `docs/specs/api_contracts/trade_endpoints.md` | Confirmed `backend/services/trade_csv_service.py::build_trade_history_csv` is dead code (only reference was a bare, non-`__all__` re-export in `services/__init__.py`) — distinct from the live, differently-signed `trade_service.py::build_trade_history_csv(portfolio_id)` still powering `GET /trades/export/csv`. Deleted the file and its import. | Dead-code status confirmed or refuted; if dead, removed; if kept, reason documented in a code comment; Head of Engineering sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_trade_plans_ticker_index.py` (3/3 pass), `tests/test_ensure_trade_plans_table_memoization.py` (2/2 pass, new), `tests/test_position_state_history.py` (6/6 pass, 2 new) — full backend suite `backend/.venv/bin/python3 -m pytest tests/` run repeatedly across this EPIC's changes, most recently 1174 passed / 5 skipped, 0 failed, 0 regressions. `import main` smoke-check confirmed the FastAPI app still boots after the `trade_csv_service.py` removal.
- Regression areas checked: `backend/database.py::ensure_trade_plans_table()` and every one of its 11 call sites (all continue to function correctly under memoization — first call performs DDL, subsequent calls no-op); `position_lifecycle_service.py::refresh_position_lifecycle()` write ordering and exception propagation; `services/__init__.py` import surface after the dead-code removal (confirmed `build_trade_history_csv` was never exported via `__all__`, so no downstream import breaks).
- Known deviations: `DEV-EPIC03-ST09-01` (P3) — see below. ST-08, ST-10, ST-11's deviation checks completed with nothing to file.

### DEV-EPIC03-ST09-01
**Priority:** P3
**Story:** ST-09
**AC:** "A real invocation's Render log confirms the `"SI-05 digest sent... in %.2fs"` line is present with a real elapsed-time value"
**Expected:** A real post-merge production invocation's Render log contains the digest-timing line with a genuine elapsed-time value.
**Actual:** A real post-merge invocation was triggered (run 32342881081, 2026-08-20T07:11:45–51Z) and confirmed successful (200 OK in the Render deploy log), but the digest-timing line never appeared anywhere in the surrounding log window. Root-caused: production's `uvicorn main:app` process has no root logging configuration (`backend/main.py` never calls `logging.basicConfig()`/`dictConfig`, and uvicorn's own default config only wires its own `uvicorn`/`uvicorn.error`/`uvicorn.access` loggers) — every `logger.info()` call in application code, not just this one, is silently filtered out before reaching a handler.
**Impact:** Informational/observability-only — the endpoint's actual functional behaviour (Telegram digest delivery) is unaffected and independently confirmed working. Only the AC's literal Render-log evidence requirement is unmet; a platform-wide logging gap, not a defect introduced by this story or by the prior cycle's `ST-11`/`BLG-BE-87` (whose `logger.info()` call is itself correct — it simply never reaches a handler in production).
**Backlog action:** `BLG-BE-107` filed (P2, Backend Engineering Patterns Owner) — configure root logging so application `logger.info()` calls reach Render's captured logs.
**Notes:** AC-02 (`api_performance_baseline.md` §36 update) satisfied via an interim GitHub Actions step-timing proxy (§36.5), the identical methodology and caveat structure already used and Product-Owner-accepted once before for this same endpoint (§36.3, `BLG-OPS-54`/ST-21, 2026-08-08). Product Owner (human, real-time in-session, 2026-08-20) explicitly chose this resolution over blocking the story further or fixing the logging gap inline before closing ST-09.

**Frontend testing gate (execution_prompt.md §3.2.A):** Not applicable — no story in this EPIC creates or modifies any file under `src/pages/**` or `src/components/**`. Purely backend/data-integrity/governance-doc scope.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no story in this EPIC touches frontend code

> **Mixed-Class EPIC Signer Format (ST-11 / LL-v5.2-P4-01):** EPIC-03 contains both `delegated_backend` stories (ST-08, ST-09) and `autonomous` stories (ST-10, ST-11) — agent-mediated format required.

- Signed off by: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3)
  Sprint Execution Engine (agent-mediated, Data Model & Domain Schema Owner role — §5.3)
  Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3)
  Sprint Execution Engine (agent-mediated, Infrastructure & Operations Owner role — §5.3)
- Date: 2026-08-20 (ST-09 completed post-merge; ST-08/ST-10/ST-11 unchanged since 2026-08-18)
- Comments: Story-level sign-offs provided by Backend Engineering Patterns Owner (ST-08), Data Model & Domain Schema Owner (ST-10), Head of Engineering (ST-11), and Infrastructure & Operations Owner (ST-09), agent-mediated per §5.3 — see below. ST-08 required 2 retries (2 independent vacuous-test-assertion bugs found and fixed) before clearing Approved on the 3rd/final attempt, within the 2-retry cap. ST-10 and ST-11 both Approved on first pass. ST-09 was returned to backlog in-flight on 2026-08-18 (structurally required a post-merge invocation), then completed on 2026-08-20 after EPIC-03 merged — see `DEV-EPIC03-ST09-01` and DEL-20260818-05 for full disposition. All acceptance criteria met; one P3 deviation (`DEV-EPIC03-ST09-01`) — no unresolved P0/P1 gaps.

### Story-level authority sign-off (BLG-GOV-14 — required in addition to, not instead of, the EPIC-level block above)

**Backend Engineering Patterns Owner** (ST-08):
- Signed off by: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3)
- Date: 2026-08-18
- Comments: Approved (final, 3rd/retry-2 attempt). Round 1 found the new `_trade_plans_table_ensured` memoization flag silently made a pre-existing test vacuous when a sibling test in the same file ran first (flag short-circuited the DDL path entirely) — fixed by resetting the flag at the start of both affected tests. Round 2 (retry 1) found a second, independent vacuous-assertion bug in the same test: the search literal `"idx_trade_plans_ticker on trade_plans(ticker)"` contained spaces while being compared against a space-stripped haystack, making the assertion unconditionally true regardless of actual SQL executed — fixed by stripping spaces from the literal too. Round 3 (retry 2, final) independently re-reproduced the empirical regression-injection verification (temporarily reintroducing the plain index, confirming the fixed test now fails, then reverting with no residue) and confirmed no other latent vacuous-assertion pattern in the file or in the new memoization test file. Full suite re-run clean after each round (1174 passed, 5 skipped, 0 failed).
- Known deviations: None found.

**Data Model & Domain Schema Owner** (ST-10):
- Signed off by: Sprint Execution Engine (agent-mediated, Data Model & Domain Schema Owner role — §5.3)
- Date: 2026-08-18
- Comments: Approved. Verified both accept/fix decisions against actual code (not just the document's claims): all 3 `position_audit_log` call sites confirmed primary-then-audit ordered, with no exception handling in the primary-write functions so a failure genuinely propagates before the audit call; the `position_state_history` reorder confirmed correct (same return value, exception propagation preserved) via `git diff`. Both new regression tests confirmed not gameable — order recorded via live `side_effect` closures, not static assertions. Non-blocking polish suggested (DS-13 cross-reference to the ordering note) — applied same-day.
- Known deviations: None found — this is a documented fix-or-accept decision per the AC's own literal wording, not a deviation from a prior spec (no prior spec existed asserting same-transaction atomicity).

**Head of Engineering** (ST-11):
- Signed off by: Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3)
- Date: 2026-08-18
- Comments: Approved. Independently re-verified the dead-code claim via repo-wide search (`backend/`, `tests/`, `scripts/`, `.github/workflows/`, full tree): zero references to `trade_csv_service` or its `build_trade_history_csv(trades: List[Dict])` signature outside this investigation's own documentation. Not exported via `services/__init__.py`'s `__all__` (no broken re-export risk), no dynamic-import path. Confirmed the live, differently-signed `trade_service.py::build_trade_history_csv(portfolio_id)` — implementing `trade_endpoints.md`'s canonical `GET /trades/export/csv` contract — is untouched and still wired via `trades_export.py`. Deleting the whole file (vs. retaining with a deprecation comment) affirmed as the correct AC-offered outcome given no partial/planned use existed. Full suite passed (1174 passed, 5 skipped, 0 failed) and `import main` succeeded post-removal.
- Known deviations: None found.

**Infrastructure & Operations Owner** (ST-09):
- Signed off by: Sprint Execution Engine (agent-mediated, Infrastructure & Operations Owner role — §5.3)
- Date: 2026-08-20
- Comments: Approved with deviation. Confirmed EPIC-03 merged to `main` (PR #1454) before attempting evidence-gathering. A real post-merge invocation was genuinely triggered (`si05-weekly-digest.yml` `workflow_dispatch`, run 32342881081, 2026-08-20T07:11:45–51Z, succeeded) and its Render deploy log genuinely reviewed — the digest-timing line's absence is a verified finding, not an assumption: root-caused to production's `uvicorn` process having no root logging configuration (confirmed via repo-wide grep of `backend/` for `basicConfig`/`addHandler`/`dictConfig` — none found), so `logger.info()` calls throughout the app, not only this one, never reach a handler. This is a genuine, pre-existing platform gap outside this story's own scope, correctly not worked around silently: filed as `BLG-BE-107` rather than left undocumented. Interim resolution (GitHub Actions step-timing proxy, §36.5) follows the identical, already-accepted precedent from §36.3/`BLG-OPS-54` rather than inventing a new methodology. Product Owner (human, real-time in-session, 2026-08-20) explicitly directed this resolution.
- Known deviations: `DEV-EPIC03-ST09-01` (P3) — see above.
