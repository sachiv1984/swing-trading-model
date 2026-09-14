**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active — partial (see §3)
**Version:** 1.1
**Last Updated:** 2026-09-14 (ST-10, EPIC-03, v9.4, BLG-OPS-152 — confirmed claude_audit_log.endpoint column exists (§3 prerequisite check); real-data AC re-confirmed unmet from this environment, carried-forward estimate left in place, disclosure re-dated); prior — 2026-09-08 (ST-56, EPIC-05, v9.2, BLG-OPS-150 — endpoint inventory complete, real-data AC not fully met, see §3)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Feature Cost-Trend Tracking — Q3 2026

## 1. Purpose

`BLG-OPS-150`'s problem statement: AI feature cost-trend tracking has not kept pace with feature shipping — the last comprehensive tracking document (`docs/ops/anthropic_api_cost_trend_2026.md`, v5.6-era, 2026-06-16) covered 2 AI-invoking endpoints; 4 more have shipped since. This document brings the endpoint inventory current and establishes the Q3 2026 tracking baseline.

## 2. Endpoint Inventory (Confirmed Current, 6 of 6)

Confirmed via direct `backend/routers/`/`backend/services/` inspection (2026-09-08), superseding the 2-endpoint inventory the last comprehensive review covered:

| # | Endpoint | Shipped | Invocation pattern |
|---|----------|---------|---------------------|
| 1 | `POST /trade-plans/{plan_id}/generate-thesis` | v4.0/v4.2 | User-triggered, per trade plan |
| 2 | `POST /ai/check-daily-cost` | v4.1 | Automated, 1×/day (this is the cost-*monitoring* call itself, not a content-generation call — included for completeness; its own cost is negligible, no LLM content generation) |
| 3 | `POST /trade-plans/generate-plan` | — | User-triggered, per trade plan (generates all plan fields from ticker + signal) |
| 4 | `POST /ai/journal-summary` | — | User-triggered |
| 5 | `POST /ai/daily-briefing` | v6.2 | User-triggered (Regenerate button) |
| 6 | `POST /ai/chat` | — | User-triggered |
| 7 | `POST /trades/{trade_id}/debrief` | v8.9 (`BLG-FEAT-90`) | Automated, post-trade-close |

**Note on count:** this table has 7 rows because `/ai/check-daily-cost` is a monitoring call, not a content-generation call, and this story's AC (6 AI-invoking endpoints) refers to the content-generation set. The 6 covered by this story's AC are rows 1, 3, 4, 5, 6, 7.

## 3. Real Query Data — AC Not Fully Met (Disclosed, Not Fabricated)

**This story's AC requires "real query data obtained for at least the current quarter" (Q3 2026: 2026-07-01 to 2026-09-30). This environment has no access to `DATABASE_URL`** (confirmed: `backend/database.py` raises `ValueError` with no env var set; same constraint already documented in `anthropic_api_cost_trend_2026.md` §3) — the production Postgres instance is Render-side only, not reachable from this session. No real query was executed, and none is fabricated here to appear as if it were.

**What this document does instead, consistent with the existing precedent in `anthropic_api_cost_trend_2026.md` §3:**

- Records the exact query needed so a human with production access can run it directly:

```sql
SELECT
  endpoint,
  date_trunc('month', created_at) AS month,
  COUNT(*) AS calls,
  SUM(input_tokens) AS input_tokens,
  SUM(output_tokens) AS output_tokens,
  SUM(cost_usd) AS cost_usd
FROM claude_audit_log
WHERE created_at >= '2026-07-01' AND created_at < '2026-10-01'
GROUP BY 1, 2
ORDER BY 2, 1;
```
**Prerequisite check re-confirmed (ST-10, BLG-OPS-152, v9.4, 2026-09-14):** `claude_audit_log` DOES carry an `endpoint` column (confirmed via direct `backend/database.py` inspection — `ensure_claude_audit_log_table()`'s `CREATE TABLE` and `create_claude_audit_entry()`'s insert both name it; already relied on by `GET /ai/monthly-cost-by-feature` and `database.get_claude_endpoint_cost_windows()`). Per-endpoint attribution for the §3 query above is therefore possible from the schema as-is — no prerequisite gap to file for this sub-criterion.

- Carries forward the last confirmed real reading as the working estimate rather than inventing a new one: ~$0.05–$0.15/month (v5.6 reading, 2 endpoints). With 4 additional endpoints now live, actual Q3 spend is expected to be somewhat higher but still low-volume-gated (per `docs/ops/cra_migration_scoping_2026-09-08.md`-independent reasoning: trade volume, not endpoint count, is the binding constraint on call volume for the trade-plan/debrief-triggered endpoints — see `ai_cost_threshold_review_2026-09-08.md` §3/§4 for the same reasoning applied to the cost threshold).

**Re-confirmed 2026-09-14 (ST-10, EPIC-03, v9.4):** `DATABASE_URL` is still unavailable in this execution environment (re-checked — same `ValueError` path in `backend/database.py`). The actual Q3 2026 production query has still not been run; the carried-forward estimate above is left in place, unchanged, with this disclosure re-dated rather than a new figure being invented. Query remains ready for the first human/session with production access to execute per §4.

## 4. Disposition

**Filed as `BLG-OPS-152`**, following the same pattern already used this story batch (`BLG-SPEC-138`, `BLG-OPS-151`) for AC clauses this environment cannot satisfy directly: FinOps & Resource Architect (or Infrastructure & Operations Owner, whoever next has production DB access) to run the §3 query against real Q3 2026 data and update this document's §3 with actual figures, replacing the carried-forward estimate.

## 5. Sign-Off

**FinOps & Resource Architect (agent-mediated, §5.3):** ST-10 (BLG-OPS-152, EPIC-03, v9.4) re-review, 2026-09-14 — `claude_audit_log.endpoint` column existence confirmed (AC met); real production-DB query still unavailable from this environment, re-disclosed rather than fabricated, carried-forward estimate left in place per RISK-03. `BLG-OPS-152` remains open pending a session/human with production DB access.

**FinOps & Resource Architect:** Partial — endpoint inventory (§2) confirmed current and complete (6 of 6, up from 2). Real-query-data AC clause not met from this environment; disclosed rather than fabricated, query recorded for direct execution, follow-up filed (`BLG-OPS-152`). 2026-09-08.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-14 | 1.1 | ST-10 (EPIC-03, v9.4, BLG-OPS-152): confirmed `claude_audit_log.endpoint` column exists (§3 prerequisite check, AC met); re-confirmed `DATABASE_URL` still unavailable, carried-forward estimate left in place, disclosure re-dated. |
| 2026-09-08 | 1.0 | Endpoint inventory brought current (6 of 6); real-query-data AC clause disclosed as unmet from this environment, follow-up filed (ST-56, EPIC-05, v9.2, BLG-OPS-150). |
