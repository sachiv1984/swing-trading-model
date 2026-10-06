**Owner:** Strategy Rules & System Intent Owner (co-reviewer: AI Compliance & Governance Officer)
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-06 (agent-mediated review corrections: A1 function name and baseline Fail (BLG-AI-09), A4 framing, B3 expected hits, D1 test files); prior — 2026-10-06 (checklist created)
**Source:** ST-15 (`BLG-GOV-140`), EPIC-04, cycle `2026-10-06__release-v9.10`

# AI Chat and Daily Briefing — §13 Quarterly Self-Audit Checklist

## 1. Purpose and Scope

`strategy_rules.md` §13 requires AI output to stay advisory. The system is decision-support, not "an automated trading bot" or "a machine-learning or AI-driven prediction system" (§13.2). The v6.2 AI Advisory Layer cleared §13 review at release (`docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`). This checklist is a **quarterly** self-audit that the boundary still holds as prompts, models and response handling change. Without one, compliance depends on individual vigilance.

**In scope:** `POST /ai/chat` (`AiChatWidget.js`) and `POST /ai/daily-briefing` (`AiDailyBriefing.js`), served by `backend/services/ai_service.py`.

**Relationship to §13.5:** §13.5's semi-annual re-attestation covers *every* §13-cleared feature at roster level. This checklist is a deeper, quarterly check of the two conversational AI surfaces only. A quarterly review in the same month as a §13.5 re-attestation may be cited as that feature's re-attestation evidence.

## 2. Cadence

- **Quarterly.** First review **2026-11-03**, after the `2026-10-06__release-v9.10` sprint closes. Then 2027-02-03, 2027-05-03 and 2027-08-03, and every three months after that.
- Re-run out of cycle when any of these changes: `ai_service.py`'s system prompts, `MODEL_BRIEFING`/`MODEL_VERSION`, `AiDisclaimer.js`, or the AI response rendering components.
- Owner: Strategy Rules & System Intent Owner. Co-reviewer: AI Compliance & Governance Officer.

## 3. Checklist

Record a Pass, Fail or N/A for each item, with evidence (file and line, command output, or screenshot). Any Fail is filed as a backlog item before the review is signed. A Fail on items A1–A3 or B1–B3 is a §13 boundary breach: escalate to the Strategy Rules & System Intent Owner the same day. Exception: A1's baseline Fail on the briefing prompt (`BLG-AI-09`) was reviewed on 2026-10-06 by the Strategy Rules & System Intent Owner (agent-mediated, §5.3) and is not a §13 breach. The user-facing boundary holds through `advisory: true` (`ai_service.py` `generate_daily_briefing` return) and `AiDisclaimer` (`AiDailyBriefing.js`). Any other A1 Fail is a breach.

### A. Advisory language

| # | Check | How to verify |
|---|-------|---------------|
| A1 | Both system prompts state the output is advisory and that the model cannot execute trades | Read `ai_service.py` `generate_daily_briefing` / `ai_chat` `system_prompt` strings. **Baseline 2026-10-06:** the chat prompt states advisory-only; the briefing prompt does not. This is a known Fail tracked as `BLG-AI-09`, and it stays a Fail until that ships. |
| A2 | No forbidden prescriptive or prediction phrasing in shipped UI copy | `python3 scripts/check_ui_copy_forbidden_phrases.py` exits 0 |
| A3 | Sampled live outputs contain no prescriptive or prediction language | `python3 scripts/run_ai_output_boundary_sample_audit.py` against `ai_output_boundary_samples` (needs a production credential; record who ran it). Compare with the previous quarter's result. |
| A4 | Briefing action types are still only `EXIT` / `ENTER` / `MONITOR` / `HOLD`, and the UI presents them as recommendations | Read the briefing system prompt and the `AiDailyBriefing.js` rendering. The prompt itself does not yet use recommendation framing (`BLG-AI-09`). |

### B. No automated action

| # | Check | How to verify |
|---|-------|---------------|
| B1 | Neither endpoint writes to `positions`, `trade_history`, `trade_plans`, `signals` or cash tables | Grep `ai_service.py` and `routers/ai.py` for any `database` write other than `create_claude_audit_entry` and output sampling |
| B2 | No UI path turns an AI action item into a trade, exit or order without a separate, explicit user action | Read `AiChatWidget.js` / `AiDailyBriefing.js` click handlers |
| B3 | No scheduler, cron or background job calls either endpoint | Grep `.github/workflows/` and `backend/` for `/ai/daily-briefing` and `/ai/chat`. Expected hits: `backend/routers/test.py` (the on-demand `GET /test` endpoint suite, not scheduled) and docstring mentions in `ai_endpoint_anomaly_service.py` (not callers). Any other caller is a Fail. |

### C. Disclaimer visibility

| # | Check | How to verify |
|---|-------|---------------|
| C1 | `AiDisclaimer` renders on both the chat widget and the daily briefing | Playwright (existing AI widget specs) or a recorded staging run |
| C2 | The disclaimer passes the axe colour-contrast check in the supported theme | `tests/e2e/accessibility-axe-scan.spec.js` (DashboardHome) passes in CI |
| C3 | Every response payload still carries `advisory: true` | Read the return statements in `ai_service.py` |

### D. Prompt-injection risk

| # | Check | How to verify |
|---|-------|---------------|
| D1 | User-controlled values interpolated into the system prompt are still validated (`_validate_context_ticker`, BLG-SEC-01) | Read `ai_service.py`. Run `tests/test_ai_chat_schema.py` and `tests/test_ticker_market_sanitization_regression.py`. |
| D2 | The chat question goes only in the user turn, never in the system prompt | Read `ai_chat` |
| D3 | No new tool-use, function-calling or retrieval capability has been added that would let model output trigger an action | Read the `_create_message` call kwargs (no `tools=`) |
| D4 | Rate limits on both endpoints are unchanged or tighter | `routers/ai.py` limits; `GET /test` rate-limit check |

### E. Logging (cross-reference)

| # | Check | How to verify |
|---|-------|---------------|
| E1 | `claude_audit_log` rows exist for the quarter's calls, and `create_claude_audit_entry` failures are logged, not swallowed | `docs/ops/ai_output_logging_completeness_audit_2026-10-06.md`; open remediation `BLG-AI-08` |

## 4. Review Log

| Review date | Reviewer | Result | Fails filed | Next review |
|-------------|----------|--------|-------------|-------------|
| 2026-11-03 (scheduled) | Strategy Rules & System Intent Owner; AI Compliance & Governance Officer | — | — | 2027-02-03 |

## 5. Sign-off (checklist adoption)

- Product Owner: _pending_ (always human; `ESC-EXEC-20261006-06`)
- Strategy Rules & System Intent Owner: **Approved** 2026-10-06. Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3). Blocked twice before approval: wrong function name, an untrue A1 premise and a breach-rule contradiction, all corrected. Pending human confirmation.
