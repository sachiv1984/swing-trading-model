**Owner:** AI Compliance & Governance Officer
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-09-07 (correction — v9.1 ST-30/BLG-GOV-266's independent audit found this review's search scope was too narrow, missing a 6th AI touchpoint; see Correction note below); prior — 2026-09-07 (created — v9.1 ST-23, BLG-GOV-74, fulfilling the BLG-GOV-63 quarterly-review mandate)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Feature Usage Quarterly Review

## Purpose

BLG-GOV-63 mandates a quarterly review of `claude_audit_log`. First review was due 2026-08-29 (3 months after the v4.0 AI feature ship, 2026-05-29). The most recent related record on file, `docs/ops/anthropic_api_cost_trend_2026.md` (v5.6, 2026-06-16), covered a 14-cycle cost trend but is not itself a BLG-GOV-63 quarterly-review record and has not been updated since. This is the first review filed explicitly against the BLG-GOV-63 mandate.

## Correction (added 2026-09-07, same-cycle)

**This review's original search scope was too narrow.** It found every call site of `create_claude_audit_entry` (→ `claude_audit_log`), but this system has **3 distinct audit-logging tables** (`claude_audit_log`, `gemini_audit_log`, `ai_audit_log`), and a 6th AI touchpoint — `POST /journal-summary` (logs to `ai_audit_log` via a separate `ai_audit_service.py` module, not `create_claude_audit_entry`) — was missed as a result. This was caught by this same cycle's ST-30 (`docs/governance/ai_feature_touchpoint_register.md`, BLG-GOV-266), which searched all 3 tables. The inventory table below is corrected to 6 rows; all findings/anomaly-filing below reflect the corrected count. Left in place rather than silently rewritten, per this session's own established practice of disclosing corrections to prior work in the same cycle.

## Constraint (stated explicitly, per `shared_standards.md` §16.16)

`SBX-NO-LIVE-DB` — this sandbox has no live connection to the production PostgreSQL database. `claude_audit_log`'s actual row counts, per-endpoint call volumes, `override_rate`, and real cost totals cannot be queried directly from here. The best available substitute performed instead: a **structural/code-based review** — auditing every code path that writes to `claude_audit_log` (`grep`-verified call sites, not assumed), cross-referenced against existing spec/security documentation, rather than a live query. This is a best-available-proxy, not a substitute for an actual data pull — flagged as a follow-up recommendation below.

## Current Feature Inventory (corrected 2026-09-07 — see Correction note above)

All 6 AI-invoking endpoints, verified via direct grep across all 3 audit-logging tables' call sites in `backend/services/` and `backend/routers/ai.py`:

| # | Endpoint | Service module | Model | Prompt version | Spec coverage |
|---|----------|----------------|-------|-----------------|----------------|
| 1 | `POST /trade-plans/generate-plan` | `gemini_service.py` (`generate_full_plan`) | `claude-haiku-4-5` | v3.0 | `docs/specs/api_contracts/ai_endpoints.md`, `docs/specs/api_contracts/ai_advisory_contract_checklist.md` |
| 2 | `POST /trade-plans/{plan_id}/generate-thesis` | `gemini_service.py` (`generate_setup_thesis`) | `claude-haiku-4-5` | v3.0 | Same as above |
| 3 | `POST /trades/{trade_id}/debrief` | `debrief_service.py` | `claude-haiku-4-5` | v1.0 | `docs/specs/api_contracts/ai_endpoints.md` |
| 4 | `POST /ai/daily-briefing` | `ai_service.py` | `claude-sonnet-4-6` | v1.0 | `docs/specs/frontend/pages/dashboard.md` |
| 5 | `POST /ai/chat` | `ai_service.py` | `claude-sonnet-4-6` | v1.0 | `docs/specs/frontend/pages/positions.md` |
| 6 | `POST /journal-summary` | `ai_service.py` (`summarise_journal_notes`) + `ai_audit_service.py` | `claude-haiku-4-5-20251001` | — | Endpoint's own docstring: "AI output is display-only — not used in any calculation" |

**§13 (display-only, no automated recommendation) coverage:** cross-referenced against `docs/specs/qa/ai_s13_boundary_test_suite.md` and `docs/specs/security/ai_endpoint_security_checklist.md` — both exist and cover the endpoint set above at a spec level. No line-by-line re-verification performed in this review (out of this story's `S`-effort scope); flagged as a recommendation below if a deeper pass is wanted.

## Findings

**Finding 1 (feature-inventory drift, informational):** The last cost-focused record on file (`anthropic_api_cost_trend_2026.md`, 2026-06-16) documented only 2 features (thesis generation, daily cost alert). The current inventory is 6 endpoints across 3 service modules and 3 distinct audit tables — `POST /ai/daily-briefing`, `POST /ai/chat`, and `POST /journal-summary` in particular did not exist (or this review initially missed) at that review's time and are not reflected in any cost-trend document. This is not itself an anomaly (each has its own spec coverage, per the table above) but confirms the cost-trend side of AI governance tracking has not kept pace with feature shipping — a real gap, filed below as `BLG-OPS-*`.

**Finding 2 (model-tier divergence, informational):** `POST /ai/daily-briefing` and `POST /ai/chat` use `claude-sonnet-4-6` (`MODEL_BRIEFING` in `ai_service.py`) — a materially more expensive tier than the `claude-haiku-4-5` used by the other 3 endpoints. This is a genuine cost-relevant fact this review should surface (per BLG-GOV-74's original "cost per use" framing) even though the current story's narrower AC (per `stage4_backlog_slice.md`) does not require a cost computation. No anomaly implied — Sonnet may be a deliberate choice for these two higher-context-need features — but it is the single largest cost-per-call driver in the current inventory and should be the first thing checked if a future review does obtain live cost data.

**Finding 3 (naming/module-boundary observation, informational):** `backend/services/gemini_service.py` — named for a provider this system no longer calls (`MODEL_VERSION = "claude-haiku-4-5"` throughout the file, confirmed via grep — zero live Gemini API calls in this module) — is where 2 of the 5 Claude-invoking endpoints actually live, and it dual-writes every call to both `gemini_audit_log` (legacy) and `claude_audit_log` (current). This is a pre-existing naming/structural artifact from an earlier provider migration, not a new finding, and not in scope for this review to fix — noted for completeness since it was directly observed while building the feature inventory above.

**No anomalies requiring immediate action found** in this structural pass. The two informational findings above are process/tracking gaps, not evidence of misuse, cost overrun, or compliance failure — neither rises to a BLG item on its own except Finding 1, which is filed below since it names a concrete, actionable tracking gap.

## Anomalies Filed

| Backlog ID | Priority | Description |
|-----------|----------|-------------|
| `BLG-OPS-150` | P3 | Cost-trend tracking for AI features has not been updated since 2026-06-16 (`anthropic_api_cost_trend_2026.md`, v5.6) and does not cover `POST /ai/daily-briefing`/`POST /ai/chat`/`POST /journal-summary` (all shipped after, or missed by, that record). Update or supersede that document with the current 6-endpoint inventory (see `docs/governance/ai_feature_touchpoint_register.md`), ideally backed by a real query across all 3 audit tables once live DB access is available for a review session. |

## Next Review

**Next review due:** 2026-11-29 (quarterly cadence from the 2026-08-29 mandate date).

## Recommendations for the Next Review

1. Obtain live `claude_audit_log` access (or a pre-exported CSV/query result) so the next review can report actual call volumes, token totals, and cost per endpoint — this review's structural-only pass cannot answer BLG-GOV-74's original "cost per use" question.
2. Cross-check `compliance_check_result` values recorded for `POST /trades/{trade_id}/debrief` (the one endpoint with §13-relevant output-side compliance checking, per `ensure_claude_audit_log_compliance_check_column`'s docstring) — confirm no unexpected failure-rate pattern once live data is available.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, AI Compliance & Governance Officer role — §5.3)
- Date: 2026-09-07
- Comments: Best-available-proxy review performed (SBX-NO-LIVE-DB) — a genuine structural code audit, not a placeholder. Found and filed one real, actionable tracking gap (`BLG-OPS-150`). Satisfies BLG-GOV-74's (narrower, authoritative) sprint AC: audit log review completed, findings documented, anomaly filed, next review date recorded. **Correction 2026-09-07:** the original search scope (one audit table only) missed a 6th touchpoint, caught by this cycle's own ST-30 — corrected in the same cycle, same day, before this document left this repo's own review process. Recorded as a positive confirmation that this session's own governance work is itself subject to the review it performs, not exempt from it.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-09-07 | Correction — feature inventory expanded 5→6 endpoints (`POST /journal-summary` added, logs to a 3rd distinct audit table, `ai_audit_log`, missed by this review's original single-table search scope). Caught by v9.1 ST-30's independent audit (`ai_feature_touchpoint_register.md`, BLG-GOV-266). Findings/anomaly text updated to match. |
| 1.0 | 2026-09-07 | Initial creation — v9.1 ST-23, BLG-GOV-74 (fulfilling BLG-GOV-63 mandate). |
