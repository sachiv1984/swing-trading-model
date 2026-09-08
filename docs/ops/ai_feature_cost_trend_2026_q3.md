**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active — partial (see §3)
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-56, EPIC-05, v9.2, BLG-OPS-150 — endpoint inventory complete, real-data AC not fully met, see §3)
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
(Assumes `claude_audit_log` carries an `endpoint` column identifying which of the 6 call sites produced each row — **verify this column exists before running**; if it doesn't, per-endpoint attribution isn't currently possible from the schema and would itself be a prerequisite gap worth its own backlog item.)

- Carries forward the last confirmed real reading as the working estimate rather than inventing a new one: ~$0.05–$0.15/month (v5.6 reading, 2 endpoints). With 4 additional endpoints now live, actual Q3 spend is expected to be somewhat higher but still low-volume-gated (per `docs/ops/cra_migration_scoping_2026-09-08.md`-independent reasoning: trade volume, not endpoint count, is the binding constraint on call volume for the trade-plan/debrief-triggered endpoints — see `ai_cost_threshold_review_2026-09-08.md` §3/§4 for the same reasoning applied to the cost threshold).

## 4. Disposition

**Filed as `BLG-OPS-152`**, following the same pattern already used this story batch (`BLG-SPEC-138`, `BLG-OPS-151`) for AC clauses this environment cannot satisfy directly: FinOps & Resource Architect (or Infrastructure & Operations Owner, whoever next has production DB access) to run the §3 query against real Q3 2026 data and update this document's §3 with actual figures, replacing the carried-forward estimate.

## 5. Sign-Off

**FinOps & Resource Architect:** Partial — endpoint inventory (§2) confirmed current and complete (6 of 6, up from 2). Real-query-data AC clause not met from this environment; disclosed rather than fabricated, query recorded for direct execution, follow-up filed (`BLG-OPS-152`). 2026-09-08.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-08 | 1.0 | Endpoint inventory brought current (6 of 6); real-query-data AC clause disclosed as unmet from this environment, follow-up filed (ST-56, EPIC-05, v9.2, BLG-OPS-150). |
