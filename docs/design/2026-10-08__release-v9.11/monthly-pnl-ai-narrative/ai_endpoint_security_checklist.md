**Owner:** Cybersecurity & Trust Lead
**Class:** Design Decision Record (supporting)
**Status:** Approved
**Cycle:** 2026-10-08__release-v9.11
**Story:** ST-25 (EPIC-04, BLG-FEAT-59) — `stage4_backlog_slice_addendum.md` §ST-25 step 2

# AI Endpoint Security Checklist — Monthly P&L Narrative

Completed against `docs/specs/security/ai_endpoint_security_checklist.md` v1.0 before the design record (`decision_record.md`, same folder) is approved, as `design_gate_prompt.md` §2.2 requires for a new AI-calling endpoint.

## Endpoint Under Review

| Endpoint | Calls a model? | Purpose |
|----------|---------------|---------|
| `POST /reports/monthly-pnl/narrative` | Yes | Return the stored narrative for one tax year's range, or generate it (or regenerate it on request) |
| `GET /reports/monthly-pnl/narrative?year=YYYY` | No | Return the stored narrative for that range, if one exists for the current input hash |

Only the `POST` calls a model, so the checks below apply to it. Exact request and response shapes are fixed in the API contract at implementation (CLAUDE.md §2 registration chain).

**Constraints from upstream records:**
- §13 determination: `docs/product/decisions/decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md` (CONDITIONAL, 12 binding conditions).
- Cost estimate: `docs/ops/ai_monthly_pnl_narrative_cost_estimate_2026-10-08.md` (ST-23): Haiku 4.5, about $0.00365 per model call and $0.0073 for a worst-case generation (one regeneration).

**Sequencing gate:** ST-25 must not ship before EPIC-01's ST-06 (commit `5c753cbc`, adding `claude_audit_log.prompt_hash`/`response_length`) is on `main`. §13 Condition 8 needs those columns. The sprint's merge order (EPIC-01 first, EPIC-04 fifth) already meets this. EPIC-04's merge gate must confirm it.

## 1. Rate Limiting — PASS

- **`POST` limit:** 10 requests per minute per IP. It uses the shared `_ai_limiter` (`services/rate_limiter.py`) under its own key prefix (`monthly-pnl-narrative:{ip}`), the same figure as `POST /ai/daily-briefing` and `POST /ai/journal-summary`.
- **429:** `{"status": "error", "message": "Rate limit exceeded. Try again later."}` with a `Retry-After` header, matching `ai_advisory_contract_checklist.md` CC-01. The contract entry must state both.
- **`GET`:** gated by the X-API-Key only, with no rate limit, like every other non-AI read (only `/health` uses `_public_limiter`). It reads one stored row and makes no model call.

## 2. Cost Gating — PASS (option (a): enforced daily call cap)

**Real-time control: a daily call cap.**
- The `POST` checks its own branches in this order:
  1. If a narrative is stored for the current input hash and `regenerate` is not true, return it with 200. No model call is made and the cap is not consulted.
  2. Otherwise, count today's (UTC) `claude_audit_log` rows for endpoint `POST /reports/monthly-pnl/narrative`.
  3. At **40** or more, make no model call. Return 429 with `{"status": "error", "message": "Daily limit for AI summaries reached. Try again tomorrow."}`, no narrative in the body, and `Retry-After` set to the seconds until 00:00 UTC.
- **Fails closed:** if the count query errors, make no model call and return 503 (`"AI summary is unavailable right now."`). A pytest covers this path.
- **What the cap bounds:** each row is one model call, so 40 rows cost about 40 × $0.00365 ≈ **$0.15 a day**. The stated bound, **$0.30 a day** (40 × $0.0073), allows for overshoot: concurrent requests can each read a count of 39, and each can make up to 2 calls before its rows land.
- **Against expected use:** ST-23's heavy-use scenario is 4 generations a day, which is up to 8 calls, so the cap is 5–10× heavy use.

**Logging.** Every model call, including a regeneration after a failed output check, writes a `claude_audit_log` row via `create_claude_audit_entry`. The endpoint tag follows the method-plus-path convention: `"POST /reports/monthly-pnl/narrative"`. Each row carries:
- cost, tokens and `prompt_version`;
- the compliance-check result (§13 Condition 8);
- `prompt_hash` and `response_length` (sequencing gate above).

`check-endpoint-anomalies` (per-endpoint cost and latency against a 7-day baseline, read from `claude_audit_log`) and `GET /ai/monthly-cost-by-feature` therefore cover this endpoint with no new monitoring.

**The daily cost alert does not cover this endpoint.** `POST /ai/check-daily-cost` sums `gemini_audit_log` only (`database.get_daily_ai_cost()`), so it never sees Claude spend from this or any other Claude feature. This predates ST-25 and is filed as `BLG-OPS-183`. Until it is fixed, the cap is the only real-time spend control. Without the cap, the rate limit alone would allow 600 generations an hour: about $4.38 an hour, or about $105 a day.

**Per-request cost is bounded by construction:**
- The input is a fixed set of numeric fields for at most 13 calendar-month rows (a tax year can span April twice), plus a fixed server-side system prompt. No caller-supplied text reaches the prompt, so the input cannot be inflated. The planning figure is about 1,650 input tokens.
- Output is capped by `max_tokens` (400).
- At most 2 model calls per request, then the deterministic fallback.

**Repeat views cost nothing.** The narrative is stored against `(tax year, input-figure hash)`.

**Accepted residual risks** (single-user product):
- The cap is global, so anyone holding the API key can use the day's 40 calls and deny the feature until 00:00 UTC.
- `create_claude_audit_entry` deliberately never fails a request. A dropped audit row lets the cap under-count by that row.

**Revisit trigger:** any one of these:
- ST-23's re-estimation trigger fires: narrative spend over $0.50 in a calendar month, a prompt over 2,500 input tokens, or a switch to Sonnet;
- the cap is hit in normal use;
- `BLG-OPS-183` lands, after which the daily alert becomes a second control.

## 3. Prompt-Injection Awareness — PASS

**Input inventory:**

| Input | Source | Insertion point |
|-------|--------|-----------------|
| `year`, `month` | `reports_service.get_monthly_pnl_report()` (integers) | User-role message, as a JSON data block |
| `realised_pnl_gbp`, `restated_diff_gbp` | Same (floats or null) | User-role message, JSON |
| `trade_count`, `null_fee_trade_count` | Same (integers) | User-role message, JSON |
| `restated` | Same (boolean) | User-role message, JSON |
| Range figures: total, total trades, best and worst month, profitable and losing month counts, month count, tax-year label tokens | Computed server-side from the rows above | User-role message, JSON |
| Basis caption (net or gross of fees) | Fixed server string chosen by code | User-role message, JSON |
| Request `year` parameter | Caller | Not interpolated. Only selects rows, after validation as an integer tax-year start (a future tax year is rejected). |

- No user-authored text (tickers, journal notes, trade notes, chat input) and no external API response reaches the prompt. The system prompt is a static string with no interpolation. This avoids the higher-risk pattern found in `ai_injection_risk_assessment.md` Input 2.
- **SRB-v1.7 display-only constraint confirmed:** the response is shown in the Monthly P&L view only and carries `advisory: true` (§13 Condition 6). It feeds no signal, score, compliance check, trade action, figure, export, snapshot or reconciliation (§13 Conditions 5 and 7).
- **Second line of defence:** the §13 output-side checks. These are the value check and the direction check (Condition 3), and the prescriptive, forward-looking and tax-language scan with its deterministic fallback (Condition 4). Even if the model were manipulated, text that states an unsourced number, gets a figure's direction wrong or gives advice is never shown.

## Disposition

**AI Endpoint Security Checklist (docs/specs/security/ai_endpoint_security_checklist.md v1.0):**
- Rate limiting: PASS — 10/min/IP on the generating `POST` via `_ai_limiter`; 429 with `Retry-After` per CC-01; the `GET` makes no model call.
- Cost gating: PASS — every call audit-logged under `POST /reports/monthly-pnl/narrative`. A fail-closed cap of 40 calls a day bounds spend at about $0.15 a day ($0.30 with race overshoot). The daily cost alert does not see Claude spend (`BLG-OPS-183`), so the cap is the real-time control. Per-request cost is bounded, and repeat views are served from storage.
- Prompt-injection awareness: PASS — inputs are system-computed numbers and a fixed caption, sent as user-role JSON, with a static system prompt. Display-only (`advisory: true`). Output-side checks with a deterministic fallback.
- Signed off by: Sprint Execution Engine (agent-mediated, Cybersecurity & Trust Lead role — §5.3), user-directed
- Date: 2026-10-09
- Comments: First pass Blocked (the daily cost alert never sees Claude spend; cap behaviour on audit failure unspecified). Second pass Approved. Bounds recomputed from ST-23's Haiku prices: one call is 1,650 × $1/M + 400 × $5/M = $0.00365, so 40 calls is $0.146 a day; the $0.30 bound allows about 82 calls of race overshoot. Runaway without the cap: 600/h × $0.0073 = $4.38/h, $105.12/day. Confirmed `get_daily_ai_cost()` reads only `gemini_audit_log` (`BLG-OPS-183`). Every prompt input matches `get_monthly_pnl_report()` and the §13 §1 list.
