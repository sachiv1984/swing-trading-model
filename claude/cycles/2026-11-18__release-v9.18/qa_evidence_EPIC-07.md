Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-20

# QA Evidence — EPIC-07 — AI Output Boundary

**EPIC:** EPIC-07 — AI Output Boundary
**Cycle:** 2026-11-18__release-v9.18
**Sprint goal:** Ship Site Structure & Usability Phase 4 stages 1–2 (Level A keyboard and label fixes, truthful Telegram alert delivery, a one-line quiet-day Dashboard, the two navigation moves, and a readable, linked Weekly Digest with this week's loop), put the first-time-right checks in place before v9.19's design gate, and make position figures correct across native entry, live FX and stock splits.
**Test scenarios used:** `tests/test_briefing_chat_parameter_change_check.py` (B-DB-06, B-CH-07); regression: `tests/test_ai_stop_time_check.py`, `tests/test_briefing_summary_ticker_check.py`, `tests/test_ai_stop_time_focus_attribution.py`, `tests/test_briefing_actions_and_cash_context.py`, `tests/test_chat_cash_context.py`, `tests/test_chat_answer_rating.py`, `tests/test_ai_prompt_template_golden_fixtures.py`, `tests/test_ai_sampling_failsafe.py`. ST-40 is a decision story: evidence is the production debrief sample and the recorded decision.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-39 | `docs/specs/api_contracts/ai_endpoints.md` v1.42 (`POST /ai/daily-briefing` check 4; `POST /ai/chat` §13.2 parameter-change check); `docs/specs/qa/ai_s13_boundary_test_suite.md` v1.7 (B-DB-06, B-CH-07); `strategy_rules.md` §13.2 | §13.2 output check on the daily briefing and chat, per ruling `ESC-EXEC-20261120-01` (1)(a)/(2)(A): the journal summary's `trading_change` category, per sentence, with a logged negation/declined-suggestion exemption (confirmed 2026-11-20); regenerate once, then code-written replacement per failing field (briefing keeps action `type`/`ticker`; chat returns a withheld message without `answer_id`); the first output takes the fallback if the regeneration fails; one audit row per model call; withheld chat rows cannot be rated. Prompts: briefing v1.4, chat v1.3. Commits `263fb657` (ruling), `5e91c0e8` (code), `652b29ad` (confirmation follow-up). | AC 1: ruling recorded before the code change. AC 2: a briefing or chat output suggesting tightening stops gets the ruled handling, in a test; a deterministic EXIT/HOLD action does not. AC 3: every existing briefing and chat test passes. AC 4: ruling and test cite §13.2 and the §13.5 BLG-FEAT-50/51 row, and answer each. | Pass with notes — AC 1: `263fb657` precedes `5e91c0e8`. AC 2: `TestBriefing`/`TestChat` in `test_briefing_chat_parameter_change_check.py` (tighten-stop advice regenerated, then withheld; EXIT/HOLD rule wording passes on the first call). AC 3: all existing briefing/chat tests pass; the only test edits are prompt-version pins moved for the intended bump. Full backend suite 3749 passed. AC 4: escalation resolution and the test module docstring cite both and answer each. CI: `5e91c0e8` all 7 workflows success (CI Pytest 44710051573); `652b29ad` all 7 success (CI Pytest 44713949353). Notes: detector misses outside the ruled category filed as BLG-AI-34 (P3), with BLG-AI-32. Wording-only response text (withheld messages) is asserted verbatim by backend tests; it renders through the existing briefing card and chat widget with no layout change — verified by code review per CLAUDE.md §2's FI-P3-02 exception. | None |
| ST-40 | `strategy_rules.md` §13.2; `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (§13.5 row, CONDITIONAL) | Decision recorded on `ESC-EXEC-20261120-02`: **keep** the one-sentence focus area, with rationale and a re-review trigger (after BLG-BE-226 and BLG-AI-35). Evidence: 10 production debriefs generated with prompt v1.1 on 2026-11-20 by the user (DEL-20261120-01). Commit `ad42bc87`. | AC 1: a recorded decision (keep or amend), with rationale, from the AI Compliance & Governance Officer and the Product Owner. AC 2: the decision cites §13.2 and the §13.5 row for the ST-06 debrief review, and answers each. | Pass — AC 1: decision by the user as both roles, 2026-11-20, with rationale from the sample (6 of 10 focus sentences omitted by the number check, all 4 went-to-plan trades among them; shown sentences repeat an R figure on a different stop basis from the target). AC 2: both cited and answered in the resolution. AC 1 was met in-sprint, so the seal's post-merge fallback (BLG-GOV-378) was not needed. | None — found defects filed: BLG-BE-226 (P2), BLG-AI-35 (P2), BLG-BE-228 (P2), BLG-BE-227 (P3), BLG-AI-36 (P3) |

**AI evidence (ST-39):**
- Prompt-template version: `BRIEFING_PROMPT_VERSION` v1.3 → v1.4, `CHAT_PROMPT_VERSION` v1.2 → v1.3; golden fixtures updated (`tests/fixtures/ai_prompt_template_golden_fixtures.json`).
- Boundary-language sample (illustrative; no live API key in this environment): "NVDA closed below its trailing stop of £450.00 (last recalculated 2026-10-12 21:05 UTC); the exit rule applies." passes the §13.2 check, and `scan_prescriptive`/`scan_prediction` (`scripts/run_ai_output_boundary_sample_audit.py`) both return False. "Consider tightening your stop on NVDA to lock in gains." fails the §13.2 check; the audit script's `scan_prescriptive` does not catch it, which BLG-AI-34's scope covers. The three code-written withheld texts pass all three scanners.

**AI evidence (ST-40):** prompt template unchanged (`debrief_service.py` `PROMPT_VERSION` v1.1). Boundary-language sample: the 10 production debriefs on `ESC-EXEC-20261120-02`; no shown focus sentence was prescriptive or predictive; STX 2026-07-02 ("allowing the position to decline") is close to suggesting a stop change and is filed as BLG-AI-36.

**P1/P2 found defects for the merge gate (LL-v9.16-P3-05):** BLG-BE-226 (R achieved basis, P2), BLG-AI-35 (debrief number check omits went-to-plan focus sentences, P2) and BLG-BE-228 (duplicate INTC 2026-09-08 `trade_history` row, P2), all found by ST-40's sample review, all pre-existing and not introduced by EPIC-07. Each needs Product Owner and Director of Quality acceptance, with rationale, before merge.

**Story-level authority sign-offs (BLG-GOV-14):** ST-39 — AI Compliance & Governance Officer ruling and confirmation (the user, human, 2026-11-20; `ESC-EXEC-20261120-01`). ST-40 — AI Compliance & Governance Officer and Product Owner decision (the user, human, 2026-11-20; `ESC-EXEC-20261120-02`). Both cleared.

**QA test coverage:**
- Scenarios run: `tests/test_briefing_chat_parameter_change_check.py` (47 cases); full backend suite (3749 passed, 41 skipped, 9 xfailed, stub `DATABASE_URL`).
- Regression areas checked: briefing stop-time and ticker checks, chat focus attribution, chat answer rating and Response Acceptance Rate, prompt golden fixtures, AI output sampling, journal summary language check (shared detector unchanged).
- Known deviations: None found — all stories' deviation checks completed with nothing to file.

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend change
- [x] **Strategy values checked:** N/A — no stop/grace/ATR/exit/sizing logic touched (ST-40 reviewed R figures but changed no code; the R-basis question is filed as BLG-BE-226)
- Signed off by:
- Date:
- Comments:
