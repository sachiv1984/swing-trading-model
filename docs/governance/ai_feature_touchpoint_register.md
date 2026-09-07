**Owner:** AI Compliance & Governance Officer
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-07 (created — v9.1 ST-30, BLG-GOV-266)

---

# AI Feature Touchpoint Register

## Purpose

BLG-GOV-266: build a canonical register of every currently-shipped AI (Claude API) touchpoint with its own §13 (display-only / no automated recommendation) classification, so a reader can confirm §13 compliance across the whole system from one document rather than cross-referencing individual page/API-contract specs.

## Method

Direct code audit of every call site invoking the Claude API, verified via `grep` against `backend/services/*.py` and `backend/routers/ai.py` — not derived from documentation alone (documentation has been found stale relative to code more than once this session; this register is grounded in the actual call graph). Each touchpoint's audit-logging destination was also traced, since 3 distinct tables exist (`claude_audit_log`, `gemini_audit_log`, `ai_audit_log`) and a touchpoint search scoped to only one of them undercounts — this happened in this same cycle's `ai_feature_usage_quarterly_review_2026-09-07.md` (ST-23), which found only 5 of the 6 touchpoints below because it searched only `create_claude_audit_entry` (→ `claude_audit_log`) call sites and missed `POST /journal-summary`, which logs to the separate `ai_audit_log` table via `ai_audit_service.py`. That review has been corrected in the same commit as this register — see its own Changelog entry.

## Register — All 6 Currently-Shipped AI Touchpoints

| # | Endpoint | Service module | Model | Audit table | §13 Classification |
|---|----------|-----------------|-------|--------------|----------------------|
| 1 | `POST /trade-plans/generate-plan` | `gemini_service.py` (`generate_full_plan`) | `claude-haiku-4-5` | `claude_audit_log` + `gemini_audit_log` (dual-write) | **Display-only.** Populates Setup Thesis, Entry Rationale, Confirmation Criteria, Early Exit Conditions, Regime Context, R-Target as editable draft text (`isAiDraft: true`, "AI draft" badge). User must review/edit/submit — no automated position action. Confirmed via `docs/specs/api_contracts/ai_advisory_contract_checklist.md`. |
| 2 | `POST /trade-plans/{plan_id}/generate-thesis` | `gemini_service.py` (`generate_setup_thesis`) | `claude-haiku-4-5` | `claude_audit_log` + `gemini_audit_log` (dual-write) | **Display-only.** Same draft-population pattern as #1, scoped to Setup Thesis alone. |
| 3 | `POST /trades/{trade_id}/debrief` | `debrief_service.py` | `claude-haiku-4-5` | `claude_audit_log` | **Display-only, with an explicit output-side compliance check.** Post-trade debrief narrative; `compliance_check_result` column (added ST-06, EPIC-02, v8.9, §13 review Condition 9) records a prescriptive-language/numeric cross-check outcome specifically so a compliance failure remains auditable — the only touchpoint in this register with a dedicated compliance-check column. |
| 4 | `POST /ai/daily-briefing` | `ai_service.py` | `claude-sonnet-4-6` | `claude_audit_log` | **Display-only, advisory.** `DailyBriefingResponse.advisory: bool` field present in the response model itself — the API contract structurally marks this as non-authoritative. Renders as a dashboard summary card. |
| 5 | `POST /ai/chat` | `ai_service.py` | `claude-sonnet-4-6` | `claude_audit_log` | **Display-only, conversational.** Free-form chat response; no structured action payload in `ChatResponse` — nothing for the frontend to auto-execute even if it wanted to. |
| 6 | `POST /journal-summary` | `ai_service.py` (`summarise_journal_notes`) + `ai_audit_service.py` (`log_ai_summary_run`) | `claude-haiku-4-5-20251001` | `ai_audit_log` (a 3rd, distinct table — not `claude_audit_log`) | **Display-only** (per the endpoint's own docstring: "AI output is display-only — not used in any calculation"). Summarises entry/exit journal notes from closed trades. **Newly found by this register** — missed by `ai_feature_usage_quarterly_review_2026-09-07.md`'s narrower search; corrected there in the same commit. |

## Cross-Check: `check_and_alert_daily_cost` (excluded, correctly)

`POST /ai/check-daily-cost` calls `services.gemini_service.check_and_alert_daily_cost`, which reads existing spend data and sends a Telegram alert if a threshold is exceeded — it does **not** invoke the Claude API itself. Correctly excluded from this register as a monitoring endpoint, not an AI touchpoint. Same reasoning applies to `GET /ai/monthly-cost`, `GET /ai/spend-trend`, and `GET /ai/claude-audit-log` — all read-only reporting over already-logged data.

## §13 Compliance Summary

All 6 touchpoints are classified **display-only** — none takes an automated action, and none is documented as generating a recommendation the system itself acts on. Touchpoint #3 (`/trades/{trade_id}/debrief`) is the only one with a dedicated output-side compliance-check column; the others rely on the display-only classification itself (advisory framing, editable-draft framing, or free-form conversational framing) as their §13 boundary, per each one's own spec/contract cited above. No anomaly found in this classification pass — this register does not itself re-verify each classification's correctness in the running system (out of this story's own scope; each classification cites its own supporting spec/contract document, which is where a fuller re-verification would need to happen).

## Keeping this register current

Whenever a new endpoint is added under `backend/routers/ai.py`, or a new call site is added to `create_claude_audit_entry`/`log_ai_summary_run`/`create_gemini_audit_entry` (or their table's equivalent successor), add a row here in the same commit — matching the existing "every new backend route must be registered" discipline already applied to `backend/routers/test.py` (CLAUDE.md §2). Re-run the search method above (grep every audit-logging call site, not just one table) at each `run ideas housekeeping`/quarterly-review cycle to catch drift.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, AI Compliance & Governance Officer role — §5.3)
- Date: 2026-09-07
- Comments: Register covers all 6 currently-shipped AI touchpoints, verified by code audit against all 3 distinct audit-logging tables (not just one), which caught and corrected a real gap in this same cycle's own earlier quarterly review (ST-23 missed touchpoint #6). Satisfies BLG-GOV-266's acceptance criteria.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-07 | Initial creation — v9.1 ST-30, BLG-GOV-266. |
