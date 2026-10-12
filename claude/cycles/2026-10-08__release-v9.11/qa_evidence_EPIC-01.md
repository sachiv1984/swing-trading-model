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
