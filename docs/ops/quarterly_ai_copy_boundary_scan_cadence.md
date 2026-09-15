**Owner:** AI Compliance & Governance Officer
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-15 (ST-21, EPIC-05, v9.4, BLG-AI-04: initial version)

---

# Quarterly AI-Generated Copy Boundary-Language Re-Scan — Cadence & Checklist

**Added:** ST-21 (EPIC-05, v9.4, BLG-AI-04)

## 1. Problem

Post-ship spot-checks confirm AI-generated copy against §13.2 boundary-language rules (`claude/strategy/strategy_rules.md`) only when a story happens to touch that copy. There is no recurring, calendar-driven re-scan that would catch drift introduced incidentally — e.g. a prompt-template edit made for an unrelated reason, with no story of its own to trigger a review.

This formalises the cadence and checklist; it does not replace the one-time Q3 2026 sample already run under `BLG-GOV-178`/ST-22 (v9.3) — see `docs/ops/ai_output_boundary_sample_audit_20260910.md` — it turns that one-off into a recurring practice, and reuses its tooling and template rather than duplicating them.

## 2. Cadence

**Quarterly, aligned to calendar quarters** (Q1 Jan–Mar, Q2 Apr–Jun, Q3 Jul–Sep, Q4 Oct–Dec) — matches the "Q3 2026" naming already established by the first sample. Target scan date: the **first business day of each quarter**. Owner: **AI Compliance & Governance Officer**.

If a scan is missed (owner unavailable, session gap), run it at the next available session and note the actual-vs-target date gap in that scan's own report — do not skip a quarter silently.

## 3. Scope — In-Scope AI-Surfaced Copy

Every feature where model-generated text reaches the user, per the current AI-endpoint contracts (re-derive this list at each scan — it is a snapshot, not frozen):

| # | Feature | Endpoint | Contract doc |
|---|---------|----------|---------------|
| 1 | Journal summary | `POST /ai/journal-summary` | `docs/specs/api_contracts/ai_endpoints.md` |
| 2 | Daily briefing (summary + per-item actions) | `POST /ai/daily-briefing` | `docs/specs/api_contracts/ai_endpoints.md` |
| 3 | AI chat | `POST /ai/chat` | `docs/specs/api_contracts/ai_endpoints.md` |
| 4 | Post-trade debrief (`summary_text`, `focus_area_text`) | `POST /trades/{id}/debrief` | `docs/specs/api_contracts/trade_endpoints.md` |
| 5 | Trade-plan generation (`setup_thesis`, `entry_rationale`, `early_exit_conditions`) | `POST /trade-plans/generate-plan` | `docs/specs/ai_thesis_generation.md`, `docs/specs/gemini_thesis_generation.md` |

**Out of scope:** static UI copy that merely *describes* AI features (button labels, disclosure badges — e.g. the `AdvisoryBadge` component, `design_system.md`) — that copy is human-authored and reviewed under the normal frontend spec/design-gate process, not this scan. In scope here is only text the model itself generates at request time.

## 4. Reusable Checklist (Run Each Quarter)

1. **Confirm scope is current.** Re-check §3's table against `docs/specs/api_contracts/ai_endpoints.md` and `trade_endpoints.md` for any new AI-invoking endpoint shipped since the last scan; add it to the table if so.
2. **Draw a sample.** Prefer a **genuine** sample of ≥10 real AI outputs via `scripts/run_ai_output_boundary_sample_audit.py`'s consumer path once `BLG-AI-06`/ST-23's generation-time sampling hook is live and credentials are available in-session. If not yet available, disclose this explicitly (per `ESC-EXEC-20260910-01`'s precedent — do not fabricate a live sample) and fall back to the 5-feature illustrative-example sample already used for Q3 2026, clearly labelled as such.
3. **Run the scan.** `python3 scripts/run_ai_output_boundary_sample_audit.py` (or its documented invocation once the ST-23 sampling-hook consumer path exists) against the drawn sample — checks both prescriptive-language and prediction-language pattern classes.
4. **Record the result.** Create `docs/ops/ai_output_boundary_sample_audit_<YYYYMMDD>.md` following the structure of `ai_output_boundary_sample_audit_20260910.md` (Purpose, Method + any disclosed limitation, Sample table with per-item Prescriptive/Prediction result, overall result).
5. **File findings.** Any violation found → file a backlog item (`BLG-AI-*`) via `/backlog-add`, same-day. Zero violations → record "no findings to file," same as Q3 2026.
6. **Escalation status check.** If this scan is the first *genuine* (non-illustrative) sample obtained, close `ESC-EXEC-20260910-01` as `Resolved` (superseding its `Deferred` disposition) per its own `deferred_trigger` and this document's cross-reference — do not leave it `Deferred` once its unblock condition is actually met.
7. **Update this document's §5 log** with the scan date, sample type (genuine/illustrative), and result — one row per quarter.

## 5. Scan Log

| Quarter | Scheduled date | Actual date | Sample type | Result | Report |
|---------|-----------------|--------------|--------------|--------|--------|
| Q3 2026 | (pre-dates this cadence) | 2026-09-10 | Illustrative (5 features × 2 examples ≈ 10; disclosed) | 0 violations | `docs/ops/ai_output_boundary_sample_audit_20260910.md` |
| Q4 2026 | **2026-10-01** | _(pending)_ | _(pending — genuine if ST-23's hook is live by then, else illustrative + disclosure)_ | _(pending)_ | _(pending)_ |

**First scan scheduled under this formal cadence:** Q4 2026, target date **2026-10-01**, owner **AI Compliance & Governance Officer** — satisfies this story's AC directly (the Q3 2026 row above pre-dates this document and is retained for continuity, not counted as "the first scan scheduled under the new cadence").

## 6. Sign-Off

- Signed off by: <fill in — pending §5.3 agent-mediated review>
- Date: <fill in — must be non-blank>
- Comments:

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-15 | ST-21 (EPIC-05, v9.4, BLG-AI-04): Initial version. Quarterly cadence, in-scope feature list, reusable 7-step checklist, and first formally-scheduled scan (Q4 2026, 2026-10-01, AI Compliance & Governance Officer). |
