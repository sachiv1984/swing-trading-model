**Owner:** AI Compliance & Governance Officer
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-10
**Source:** ST-22 (BLG-GOV-178, EPIC-05, v9.3 sprint execution)

---

# Quarterly AI Output Sampling Audit — Q3 2026

## Purpose

ST-22's acceptance criteria: sample 10 random AI outputs and check them against §13.2 boundary language (`claude/strategy/strategy_rules.md` — no autonomous-sounding directives, advisory framing preserved) and for determinism/no-prediction drift; conduct the first quarterly sample; file any findings as backlog items.

## Method and a Disclosed Limitation

`scripts/run_ai_output_boundary_sample_audit.py` scans text against two pattern classes: **prescriptive language** (directive/command phrasing — extends the pattern already in production use for post-trade debriefs, `backend/services/debrief_service.py::scan_prescriptive`, generalised here for cross-feature reuse) and **prediction language** (future-certainty forecasting claims, testing the "no-prediction drift" half of the AC). 7 unit tests (`tests/test_run_ai_output_boundary_sample_audit.py`) prove both scanners catch real violations on deliberately-violating fixtures, not just that they pass on clean text.

**This execution environment has no live production database connection and no configured `ANTHROPIC_API_KEY`** — the same constraint disclosed in `docs/ops/ai_audit_log_retention_policy.md` (ST-13) and `docs/ops/db_connection_pool_ai_endpoint_review_20260910.md` (ST-21) this same sprint. Neither `claude_audit_log`/`gemini_audit_log` (real historical AI outputs) nor a live Anthropic API call (to generate fresh real output) was available for this run.

**This quarter's sample is therefore drawn from the 10 distinct, illustrative example outputs already documented in the canonical AI-endpoint contract docs** (`docs/specs/api_contracts/ai_endpoints.md`, `trade_endpoints.md`, `ai_thesis_generation.md`, `gemini_thesis_generation.md`) — one from each of the 5 AI-invoking features' documented response shapes. These are spec-author-written illustrative text, not live model output, and this distinction matters: hand-authored examples are far more likely to already be boundary-compliant than a genuine model sample would be, since a spec author writing an illustrative example naturally writes compliant-sounding text. **A clean result against this sample is evidence the scanning mechanism itself works correctly (validated further by the unit tests' deliberately-violating fixtures) — it is not equivalent evidence that live production model output is drift-free.** See "Escalation" below for the genuine first sample this story's AC actually calls for.

## Sample (10 items) and Result

| # | Source | Text | Prescriptive | Prediction |
|---|--------|------|:---:|:---:|
| 1 | `POST /ai/journal-summary` | "Across the selected trades, recurring themes include..." | clean | clean |
| 2 | `POST /ai/daily-briefing` (summary) | "Your portfolio has 3 open positions. NVDA is near its trailing stop — monitor closely today. Markets are risk-on with two strong new signals." | clean | clean |
| 3 | `POST /ai/daily-briefing` (action) | "Within 3% of trailing stop — watch closely." | clean | clean |
| 4 | `POST /ai/daily-briefing` (action) | "Rank #1 momentum signal today." | clean | clean |
| 5 | `POST /ai/chat` | "NVDA is currently closest to its trailing stop, sitting 2.8% above the stop level of £450.00." | clean | clean |
| 6 | `POST /trades/{id}/debrief` (summary_text) | "Entered at 100.0, exited at 108.5. P&L: +8.50 (+8.50%). Exit reason: Target Reached. Held 12 day(s)..." | clean | clean |
| 7 | `POST /trades/{id}/debrief` (focus_area_text) | "Your exit was 3 days earlier than the 15-day median holding period across your last 5 closed trades in this setup type." | clean | clean |
| 8 | `POST /trade-plans/generate-plan` (setup_thesis) | "Strong momentum breakout above the 52-week high with confirmed volume surge, supported by Risk On regime." | clean | clean |
| 9 | `POST /trade-plans/generate-plan` (entry_rationale) | "Price holding above the 200 SMA with ATR expanding at 1.8x baseline; momentum at +4.2% with regime firmly Risk On." | clean | clean |
| 10 | `POST /trade-plans/generate-plan` (early_exit_conditions) | "Close below 200 SMA; regime flips to Risk Off; price retraces more than 1 ATR from entry." | clean | clean |

**Result: 0 violations across all 10 samples, both check classes.** No findings to file as backlog items from this sample.

## Escalation — Genuine First Live Sample Still Required

Per this sprint's `delegated_decision` classification of ST-22 (§13.2 boundary-language compliance judgment requires AI Compliance & Governance Officer authority, not mechanical resolution), and given the data-access limitation above means this sample could not draw from real production output: **the genuine first quarterly sample against live `claude_audit_log`/`gemini_audit_log` records is escalated to the AI Compliance & Governance Officer**, using the now-available `scripts/run_ai_output_boundary_sample_audit.py` tooling (which accepts any `(source, text)` list, not just this quarter's doc-derived one).

**Unblock criteria:** AI Compliance & Governance Officer (or anyone with production DB read access) pulls 10 random rows from `claude_audit_log`'s content-adjacent context (the actual generated text is not stored in the audit table itself, per its schema — only cost/token metadata; the real text would need to come from the corresponding `trade_plans`/`trade_debriefs` rows or application logs at generation time) and runs them through the scanner, or requests a live sample be captured going forward (e.g., a lightweight opt-in sampling hook at generation time) if no historical text is retrievable. Full disposition — pass, or findings filed as backlog items — should be recorded as a dated addendum to this document or a new dated report following this one's template.

**SLA:** 72 hours (strategy/compliance-adjacent decision), per `claude/system/execution_prompt.md` §3.1.D default.

## Acceptance

- Scanned by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — a detection script run + result documentation, no observable UI behaviour). Escalation above requires human AI Compliance & Governance Officer action for the genuine live-data sample.
- Date: 2026-09-10
