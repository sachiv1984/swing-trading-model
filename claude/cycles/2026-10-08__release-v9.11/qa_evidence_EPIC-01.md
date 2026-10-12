Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-12

# QA Evidence — EPIC-01

**EPIC:** EPIC-01
**Cycle:** 2026-10-08__release-v9.11
**Sprint goal:** see `sprint_goal.md`.

Per-story entries are added as stories close; the EPIC-level consolidation block and DoQ sign-off block are added at EPIC completion (`execution_prompt.md` §3.2.A).

---

## ST-01 — Give the post-trade debrief R achieved, the stop at exit and entry slippage

- **Spec references:** `docs/specs/api_contracts/trade_endpoints.md#POST /trades/{trade_id}/debrief`; `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`; `tests/test_debrief_service.py`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-01`), commit `8ef4c07b`:
  - AC1: for the three 2026-10-07 production examples, the summary states R achieved vs target and the stop at exit, and describes a profitable stop-out as a trailing stop — **Met** by fixture tests in `tests/test_debrief_service.py` (the summary is built deterministically in code, so the fixtures cover its wording exactly).
  - AC2: a focus area citing R achieved (e.g. "2.24R") passes the numeric check; a number not derived from source data still fails — **Met**, fixture tests (including a fabricated 2.5R that still fails).
  - AC3: a profitable "Stop Loss Hit" trade's prompt includes the trailing stop at exit — **Met**, fixture test.
  - AC4: AI Compliance & Governance Officer sign-off on the Condition 2 interpretation recorded; `PROMPT_VERSION` bumped — **Met**. [Agent-mediated review — on behalf of AI Compliance & Governance Officer, user-directed], cleared 2026-10-08T11:03:10Z, with 8 binding conditions recorded in `execution_state.json` (`sign_off_record`). Debrief `PROMPT_VERSION` v1.0 → v1.1.
- **Not yet live:** staging at `82633f5` (ST-02 run, 2026-10-09) does not carry ST-01, so its debrief showed no R figures, as expected. Live wording is checked after merge and deploy.
- **Deviations:** none (contract updated in the same commit).
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## ST-02 — Verify all six AI features after the PR #1921 import fix, and file the escaped-defect note

- **Spec references:** `stage4_backlog_slice.md#ST-02`; `docs/specs/api_contracts/ai_endpoints.md`; `docs/specs/api_contracts/ai_thesis_generation.md`; `docs/testing/escaped_defect_note_ai_sampling_import_2026-10-08.md`
- **Delegated action (DEL-20261008-01):** performed by the user (human, acting for the Infrastructure & Operations Owner) on staging. Staging backend deployed at `82633f5`, which contains the PR #1921 fix `d27df233` and has the same `backend/` and `src/` as `main` at the time of the run. A working Anthropic key was set.
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-02`):
  - AC1: dated staging run of all six AI features — **Met, with one defect filed** (run 2026-10-09):

    | # | Feature | How exercised | Result |
    |---|---------|---------------|--------|
    | 1 | Post-trade debrief | Trade History → closed trade → Regenerate | Generated. Focus area text present (only returned when the Claude call succeeds and passes the compliance and numeric checks). R achieved / stop at exit / slippage absent as expected — ST-01 is not on staging yet |
    | 2 | Journal summary | Trade History → AI journal summary | **Failed** — HTTP 422 `int_parsing` on every `trade_ids` element: the request model types `trade_ids` as `list[int]`, trade IDs are UUIDs. Pre-existing, unrelated to PR #1921. Filed **BLG-BE-162** (P1, v9.12), commit `d67f8a9e` |
    | 3 | Daily briefing | Dashboard daily briefing | Generated (summary + HOLD/HOLD/ENTER action list). Quality notes below |
    | 4 | Chat | One question about BARC | Generated; figures matched the briefing (price £2.18, stop £1.90) |
    | 5 | Generate plan | Trade Plan → "Improve with AI" (`POST /trade-plans/generate-plan`) | Generated; all plan fields filled |
    | 6 | Generate thesis | Direct API call, `POST /trade-plans/{plan_id}/generate-thesis` on a saved AAPL plan | Generated: `available: true`, `model_version` `claude-haiku-4-5`, `prompt_version` `v3.0`. No UI calls this endpoint (the "Generate thesis" button is a client-side template, `trade_plan.md` §5b; "Improve with AI" moved to `generate-plan` in `f91a718a`). Retirement filed as **BLG-BE-163** (P3, v9.12), commit `f7cd9c00` |

  - AC2: a sampled output recorded after opting in — **Met** (2026-10-12). Opt-in is by environment variable, not a Settings toggle: `AI_OUTPUT_SAMPLING_ENABLED=true` and `AI_OUTPUT_SAMPLING_RATE=1.0` set on `trading-assistant-api-staging`, then one chat question. Staging query on `ai_output_boundary_samples` returned `feature` = `chat (POST /ai/chat)`, `sampled_at` = `2026-10-12 07:56:01.417819+00`, preview "Based on your portfolio snapshot, your two open positions (BARC and LGEN) are bo…". The user was asked to remove the two variables afterwards (sampling is default-off).
  - AC3: escaped-defect note filed — **Met**, commit `d730ac69` (`docs/testing/escaped_defect_note_ai_sampling_import_2026-10-08.md`, citing ST-03, ST-04 and `BLG-QA-218`).
- **Daily briefing quality notes (not AC failures, not filed):** (a) the prompt renders cash as "cash £X of £{initial_cash}"; staging's `initial_cash` is 0, so the model reported "£15,006 against a £0 target cash level"; (b) with only held tickers among the top signals, the model emitted an ENTER action for the placeholder ticker `NEW_SIGNAL` — the prompt does not forbid invented tickers.
- **Deviations:** DEL-20261008-01's instruction to opt in "in Settings" was wrong — sampling is enabled by `AI_OUTPUT_SAMPLING_ENABLED` on the backend (`ai_output_sampling_service.py`); corrected in `delegation_log.md`. No code deviation.
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## ST-03 — Keep the AI-output sampling hook from breaking or hiding errors in AI responses

- **Spec references:** `docs/specs/api_contracts/ai_endpoints.md#AI Output Boundary-Language Sampling Hook (ST-23, BLG-AI-06, v9.4)`; `backend/utils/ai_sampling.py`; `tests/test_ai_sampling_failsafe.py`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-03`), commit `6151c0c0`:
  - AC1: a failure inside the sampling hook, including at import, leaves each AI endpoint's response unchanged — **Met**, `tests/test_ai_sampling_failsafe.py` covers all 6 endpoints for both failure points; 8 of its 10 tests fail on the pre-change code.
  - AC2: daily briefing and chat log the exception (with `exc_info`) when they return their fallback message — **Met**, asserted in the same file.
- **Deviations:** none.
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## ST-04 — Test that every backend module imports with only backend/ on the path

- **Spec references:** `tests/test_backend_import_path_isolation.py`; `.github/workflows/ci-tests.yml`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-04`), commit `7e4ebd11`:
  - AC1: reintroducing the `ai_output_sampling_service` bare import makes the new test fail — **Met**, shown locally.
  - AC2: the test passes on `main` and runs in CI Phase A — **Met on the branch**: added to `ci-tests.yml` Phase A and passing there (CI Pytest Suite run 38221200370 on `18a7e1ad`, success). It reaches `main` with this EPIC's merge.
- **Deviations:** none.
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## ST-05 — Make the debrief Regenerate button recognisable, and show failures and the generated time

- **Spec references:** `docs/specs/frontend/pages/trade_history.md#Post-Trade Debrief`; `docs/design/2026-10-08__release-v9.11/debrief-regenerate-feedback/decision_record.md`; `tests/e2e/trade-debrief.spec.js`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-05`), commit `ac85987b` (`src/components/trades/TradeDebrief.js`):
  - AC1: Regenerate has a visible border/background in both themes, and the axe scan of the debrief section reports no colour-contrast violations — **Met**, Playwright SC-DBF-06a (dark and light).
  - AC2: a mocked 500 on POST shows an error message and keeps the existing debrief — **Met**, Playwright SC-DBF-07a.
  - AC3: after a successful regenerate, the generated timestamp updates — **Met**, Playwright SC-DBF-08a.
- **CI:** the `ci_pending` note is cleared — Playwright E2E Acceptance Tests run 37780192461 on `ac85987b`: success.
- **Deviations:** none. The debrief-section axe check lives in `trade-debrief.spec.js`, not the shared `accessibility-axe-scan.spec.js`; no conflict with EPIC-06's ST-37.
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## ST-06 — claude_audit_log: add prompt_hash and response_length, and log failed model calls

- **Spec references:** `stage4_backlog_slice.md#ST-06`; `docs/specs/data_model.md#DS-27`; `docs/ops/claude_api_log_hygiene_policy.md`; `tests/test_claude_audit_log_prompt_hash.py`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-06`):
  - AC1: successful briefing and chat calls write `prompt_hash` and `response_length`, with unit tests for both endpoints — **Met**, code commit `5c753cbc`; `tests/test_claude_audit_log_prompt_hash.py` 8 passed (re-run 2026-10-12).
  - AC2: a failed model call writes an audit row marked as failed (`model_call_failed`) — **Met**, same commit and test file.
  - AC3: migration recorded in `data_model.md` and applied live, with verification output; hygiene policy amended — **Met**. DS-27 recorded in `data_model.md` (v2.53) and `claude_api_log_hygiene_policy.md` amended in `5c753cbc`. Applied live on 2026-10-12 by the user (human, with live write access, acting for the Data Model & Domain Schema Owner, DEL-20261008-03): staging, then production. Verification output, identical in both environments: `prompt_hash` `character varying` 16 `YES`; `response_length` `integer` `NULL` `YES`. Recorded in `data_model.md` DS-27 Live Confirmation.
- **Deviations:** none.
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## ST-07 — State in the daily-briefing system prompt that output is advisory and cannot execute trades

- **Spec references:** `docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing`; `docs/ops/ai_chat_section13_quarterly_self_audit_checklist.md`; `tests/test_ai_prompt_advisory_statements.py`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-07`), commit `8f3f836d`:
  - AC1: the briefing prompt states advisory-only and no execution, frames actions as recommendations, and the golden-fixture tests pass with a recorded `prompt_version` bump — **Met**; `BRIEFING_PROMPT_VERSION` v1.0 → v1.1; golden fixtures pass (Golden Output Regression Gate run 38221200416, success).
  - AC2: self-audit checklist A1 passes for both the chat and briefing prompts — **Met**, `tests/test_ai_prompt_advisory_statements.py`; checklist updated.
- **Deviations:** none.
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## ST-08 — AI briefing and chat state when a quoted stop was last recalculated

- **Spec references:** `docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing`; `tests/test_ai_stop_recalculation_time.py`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-08`), commit `a3cbdc74`:
  - AC1: briefing and chat responses that mention a stop include its recalculation time (`stop_calculated_at`), shown by a fixture test — **Met as a prompt-side control, narrowed.** Fixture tests show each position line in the briefing and chat context carries `stop_calculated_at` (or "stop not recalculated since entry"), and both prompts instruct the model to state it whenever it mentions a stop. `BRIEFING_PROMPT_VERSION` v1.1 → v1.2, `CHAT_PROMPT_VERSION` v1.0 → v1.1. Nothing checks the model's *response*: a reply that cites a stop without the time is not rejected (disclosed in `ai_endpoints.md`). The remaining gap is tracked in **BLG-AI-10**.
- **Deviations:** AC narrowed to the prompt side — BLG-AI-10.
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## ST-09 — Pin every Claude model ID in one backend module

- **Spec references:** `backend/ai_models.py`; `tests/test_ai_model_ids_pinned.py`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-09`), commit `e4ed97eb`:
  - AC1: no `claude-` model literal outside the new module and no unpinned alias in production code; a test fails if one is reintroduced — **Met**, `tests/test_ai_model_ids_pinned.py` (`test_reintroduced_literal_is_detected`). Staging generate-thesis returned `model_version` `claude-haiku-4-5` (ST-02 run, pre-merge code).
- **Deviations:** none.
- **QA findings / disposition:** _(Director of Quality — at EPIC-01 DoQ consolidation)_

---

## EPIC-01 Consolidation

**EPIC:** EPIC-01 — Post-Trade Debrief & AI Reliability
**Cycle:** 2026-10-08__release-v9.11
**Sprint goal:** Make the post-trade debrief state R achieved and the stop at exit so it stops misreading correct trades, confirm every AI feature works after the v9.4–v9.10 import defect, and make the Risk Dashboard and Positions page show real prices, GBP entry values, true stop distance and calendar-day grace (see `sprint_goal.md`).
**Test scenarios used:** `tests/test_debrief_service.py`, `tests/test_ai_prompt_template_golden_fixtures.py`, `tests/test_ai_sampling_failsafe.py`, `tests/test_backend_import_path_isolation.py`, `tests/test_ai_prompt_advisory_statements.py`, `tests/test_ai_stop_recalculation_time.py`, `tests/test_ai_model_ids_pinned.py`, `tests/test_claude_audit_log_prompt_hash.py`, `tests/e2e/trade-debrief.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `trade_endpoints.md#POST /trades/{trade_id}/debrief` | Debrief summary states R achieved vs target, stop at exit and slippage; numeric check accepts derived R. AI evidence: debrief `PROMPT_VERSION` v1.1 | Covers AC1–AC4 (fixture tests; AI Compliance & Governance Officer Condition 2 sign-off, agent-mediated) | Pass | None |
| ST-02 | `stage4_backlog_slice.md#ST-02`; `ai_endpoints.md` | Staging run of six AI features at `82633f5` (2026-10-09); sampled chat row (2026-10-12); escaped-defect note | Covers AC1–AC3. AC1 partly met: journal summary failed (HTTP 422, UUID `trade_ids` typed int) | Pass_with_deviation | BLG-BE-162 (journal summary defect); BLG-BE-163 filed incidentally (unused generate-thesis endpoint) |
| ST-03 | `ai_endpoints.md#AI Output Boundary-Language Sampling Hook` | Sampling hook fail-safe at import and call; briefing/chat log fallback with `exc_info`. AI evidence: prompts unchanged | Covers AC1–AC2 | Pass | None |
| ST-04 | `tests/test_backend_import_path_isolation.py` | Import-isolation test in CI Phase A | Covers AC1–AC2 (passes on branch; reaches `main` at merge) | Pass | None |
| ST-05 | `trade_history.md#Post-Trade Debrief` | Recognisable Regenerate button, error on failure, updated timestamp | Covers AC1–AC3, Playwright SC-DBF-06a/07a/08a (CI run 37780192461) | Pass | None |
| ST-06 | `data_model.md#DS-27` | `claude_audit_log.prompt_hash`/`response_length`; failed calls logged; DS-27 applied live 2026-10-12 | Covers AC1–AC3 | Pass | None |
| ST-07 | `ai_endpoints.md#POST /ai/daily-briefing` | Briefing prompt states advisory-only, no execution. AI evidence: `BRIEFING_PROMPT_VERSION` v1.1 | Covers AC1–AC2 | Pass | None |
| ST-08 | `ai_endpoints.md#POST /ai/daily-briefing` | `stop_calculated_at` in briefing/chat context; prompts instruct the model to state it. AI evidence: briefing v1.2, chat v1.1 | AC1 narrowed to a prompt-side control; responses are not checked | Pass_with_deviation | BLG-AI-10 |
| ST-09 | `backend/ai_models.py` | All Claude model IDs pinned in one module, with a guard test. AI evidence: prompts unchanged | Covers AC1 | Pass | None |

**AI evidence — boundary-language sample:** the live samples available are from the ST-02 staging run at `82633f5`, which predates this EPIC's prompt changes (debrief v1.1, briefing v1.1/v1.2, chat v1.1), so they are a pre-change baseline, not post-change output. `scan_prescriptive` and `scan_prediction` from `scripts/run_ai_output_boundary_sample_audit.py` were run on the debrief focus area, the briefing summary and the chat answer (2026-10-12): no match in any. Post-change output is first sampled on staging after merge.

**Story-level authority sign-offs (BLG-GOV-14):**
- ST-01 — AI Compliance & Governance Officer, Condition 2 interpretation: agent-mediated (§5.3, user-directed), cleared 2026-10-08T11:03:10Z.
- ST-02 — Infrastructure & Operations Owner (DEL-20261008-01): human in session (the user), cleared 2026-10-12.
- ST-06 — Data Model & Domain Schema Owner (DEL-20261008-03): human in session (the user), cleared 2026-10-12.

**QA test coverage:**
- Scenarios run: the 9 files above. CI on branch head `18a7e1ad`: CI Pytest Suite 38221200370, Golden Output Regression Gate 38221200416, Critical-Path Smoke Tests (Playwright) 38221200380, Portfolio Integration Tests 38221200377, Service Layer Coverage Gate 38221200341, Endpoint Coverage Report 38221200400 — all success. Playwright E2E Acceptance Tests 37780192461 on `ac85987b` (last `src/`/`tests/e2e` change) — success. `tests/test_claude_audit_log_prompt_hash.py` re-run locally 2026-10-12: 8 passed.
- Regression areas checked: AI endpoints (debrief, briefing, chat, journal summary, generate-plan, generate-thesis), AI audit logging, AI output sampling, backend import paths, Trade History debrief UI.
- Frontend testing gate (CLAUDE.md §2): the only frontend change is ST-05, and each of its observable ACs has Playwright coverage passing in CI. No AC is "code review only".
- Known deviations: ST-02 (BLG-BE-162), ST-08 (BLG-AI-10). Every other story's deviation check completed with nothing to file.

**Sign-off:**

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- [ ] **Strategy values checked:** ST-01 — §5 initial stop (R = (exit − entry) / (entry − initial stop)), §7 trailing stop at exit, §8.1 stop-loss trigger; ST-08 — §7 stop recalculation (`stop_calculated_at`). Other stories: no stop/grace/ATR/exit/sizing logic touched.
- Signed off by:
- Date:
- Comments:
