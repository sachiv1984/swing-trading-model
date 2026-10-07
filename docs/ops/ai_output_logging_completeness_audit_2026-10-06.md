**Owner:** AI Compliance & Governance Officer
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-06 (agent-mediated review corrections: function name, 2 missing early-return paths, BLG-AI-08 hash spec and policy-amendment scope); prior — 2026-10-06 (audit completed)
**Source:** ST-16 (`BLG-GOV-141`), EPIC-04, cycle `2026-10-06__release-v9.10`

# AI Model Output Logging Completeness Audit — October 2026

## 1. Purpose

`BLG-GOV-141` requires every response from the v6.2 AI features to be logged with model ID, prompt hash, response length and timestamp. No standalone policy document states this four-field requirement; the backlog item is its only source. `docs/ops/claude_api_log_hygiene_policy.md` currently describes `claude_audit_log` storing no prompt representation as the correct design, so `BLG-AI-08` must reconcile the two. This audit checks that requirement against the code for both endpoints in scope, `POST /ai/daily-briefing` and `POST /ai/chat`. It also covers the silent-failure path found by the v9.9 AI feature usage review (`docs/ops/ai_feature_usage_review_2026-09-24.md`): `database.create_claude_audit_entry()` swallowed insert errors.

## 2. Method

A code-path audit of `backend/routers/ai.py`, `backend/services/ai_service.py` (`generate_daily_briefing`, `ai_chat`) and `backend/database.py` (`ensure_claude_audit_log_table`, `create_claude_audit_entry`), on `main` at 2026-10-06. Every path from request to response was traced, recording whether it writes a `claude_audit_log` row and which fields that row holds.

No live `claude_audit_log` read was needed. The code path alone shows which fields can and cannot be present, because two of the four required fields have no column. A live read could only confirm row counts, not add the missing fields. So the RISK-04 Human-Delegation for a production read was not raised.

## 3. Paths Audited

| # | Endpoint | Path | Writes a row? |
|---|----------|------|---------------|
| P1 | `POST /ai/daily-briefing` | Success: model call returns | Yes (`ai_service.py`, `endpoint="POST /ai/daily-briefing"`) |
| P2 | `POST /ai/daily-briefing` | `ANTHROPIC_API_KEY` unset: returns before any model call | No. No model output exists, so none is owed. |
| P2a | `POST /ai/daily-briefing` | Portfolio not found: returns before any model call (`ai_service.py` ~line 155) | No. No model output exists, so none is owed. |
| P3 | `POST /ai/daily-briefing` | Model call raises after retries are exhausted | **No.** The outer `except` returns the error payload before the audit write. |
| P4 | `POST /ai/daily-briefing` | Model call succeeds, then `json.loads` of the output fails | Yes. The audit write runs before parsing. |
| P5 | `POST /ai/daily-briefing` | Rate limit exceeded (router 429) | No. No model call. |
| P6 | `POST /ai/chat` | Success | Yes (`endpoint="POST /ai/chat"`) |
| P7 | `POST /ai/chat` | Model call raises | **No**, as P3 |
| P8 | `POST /ai/chat` | Validation or rate-limit rejection before the call | No. No model call. |
| P8a | `POST /ai/chat` | `ANTHROPIC_API_KEY` unset, or portfolio fails to load: returns before any model call | No. No model output exists, so none is owed. |
| P9 | Both | Audit insert itself fails (DB unavailable, schema drift) | Row lost. **Before this story, silently**; now logged (§5). |

## 4. Field Completeness (successful calls, P1/P4/P6)

| Required field | Logged? | Column | Finding |
|----------------|---------|--------|---------|
| model_id | Yes | `model_id` (NOT NULL) | Complete |
| timestamp | Yes | `generated_at` (`DEFAULT NOW()`) | Complete |
| prompt_hash | **No** | none | Gap. `claude_audit_log` has no prompt column of any kind, hash or text. `gemini_audit_log` stores prompt/response hashes; the Claude table never got the equivalent. |
| response_length | **No (proxy only)** | `output_tokens` | Gap. Output token count is recorded and is a reasonable proxy, but no character/byte length of the response is stored. |

Also logged, beyond the policy's four fields: `endpoint`, `prompt_version` (always `"v1.0"`, a hard-coded literal), `input_tokens`, `cost_usd`, `latency_ms`, `compliance_check_result` (not set by these two endpoints).

## 5. Silent-Failure Path — Fixed in This Story

`create_claude_audit_entry()` ended with `except Exception: pass`. It now logs `claude_audit_log insert failed for <endpoint> (model <model_id>): <error>` at WARNING through `database.logger`, and is still non-blocking: an audit write must never fail the user's AI response. Both callers in `ai_service.py` also wrap the call in their own `try/except`, which is unchanged. Covered by `tests/test_claude_audit_entry_failure_logging.py` (failure logged and not raised; a successful insert logs nothing). The same function also serves `debrief_service.py` and `gemini_service.py`, which benefit too.

## 6. Conclusion

**Logging is not complete against the four-field policy.** On every successful call, model ID and timestamp are logged. Prompt hash is never logged. Response length is logged only as a token count. Failed model calls (P3/P7) leave no audit row. These gaps are filed as remediation item `BLG-AI-08`. Adding the columns is a schema change that needs live-DB application, outside this sandbox's access. The silent insert-failure path is fixed (§5).

## 7. Remediation Filed

- `BLG-AI-08`: add `prompt_hash` (SHA-256 of system and user prompt, truncated to 16 hex characters, following `gemini_audit_log` and the hygiene policy's §3.2 precedent; the policy is amended in the same change) and `response_length` (characters) to `claude_audit_log`, populate them on both endpoints, and write a row with an error marker for failed model calls (P3/P7).

## 8. Sign-off

- [x] Every `POST /ai/daily-briefing` and `POST /ai/chat` path checked for model_id, prompt_hash, response_length and timestamp
- [x] Silent-failure path in `create_claude_audit_entry()` fixed and tested
- [x] Gaps filed as a remediation item (`BLG-AI-08`)
- AI Compliance & Governance Officer: **Approved**. Sprint Execution Engine (agent-mediated, AI Compliance & Governance Officer role — §5.3). First pass Blocked: wrong function name, 2 early-return paths missing, BLG-AI-08's hash spec contradicted the hygiene precedent. Re-review Approved after corrections, with each claim checked against `ai_service.py`, `database.py`, `gemini_service.py` and the hygiene policy at line level. Pending human confirmation.
- Date: 2026-10-06
