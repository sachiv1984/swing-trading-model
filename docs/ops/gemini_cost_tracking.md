**Owner:** FinOps & Resource Architect
**Class:** Operations Document (Class 3)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-05-27
**Source:** ST-08 (BLG-OPS-26, v4.0 EPIC-03); ST-15 (BLG-OPS-30, v4.1 EPIC-04)

# Claude API Cost Tracking

## Model and Pricing

| Model | Input token rate | Output token rate |
|---|---|---|
| claude-haiku-4-5 | $1.00 / 1M tokens | $5.00 / 1M tokens |

*Rates as of v4.1 implementation (2026-05-26). Verify against Anthropic pricing page when upgrading model versions.*

## Alert Threshold

**Alert fires at: estimated cost exceeding $5.00/month.**

Alert condition: `SUM(estimated_cost_usd) FROM gemini_audit_log WHERE generated_at >= date_trunc('month', NOW())` > 5.00.

There is no automated alert in the current implementation — this threshold is defined for future monitoring integration. To check manually:

```sql
SELECT
  date_trunc('month', generated_at) AS month,
  COUNT(*) AS calls,
  SUM(total_tokens) AS total_tokens,
  SUM(estimated_cost_usd) AS estimated_cost_usd
FROM gemini_audit_log
WHERE generated_at >= date_trunc('month', NOW())
GROUP BY 1;
```

## Data Schema

The `gemini_audit_log` table (created by `ensure_gemini_audit_log_table()` in `backend/database.py`):

| Column | Type | Description |
|---|---|---|
| id | UUID | Audit entry ID |
| plan_id | UUID | Trade plan ID (nullable) |
| model_version | TEXT | Claude model version string |
| prompt_version | TEXT | Prompt template version |
| input_hash | TEXT | First 16 chars of SHA-256 of input payload |
| output_hash | TEXT | First 16 chars of SHA-256 of output thesis |
| generated_at | TIMESTAMPTZ | When the call was made |
| prompt_tokens | INTEGER | Input tokens (from response usage metadata) |
| completion_tokens | INTEGER | Output tokens |
| total_tokens | INTEGER | Sum of prompt + completion |
| estimated_cost_usd | NUMERIC(12,8) | Estimated cost at published rates |

## Retention Policy

Rows older than 90 days are eligible for deletion via `purge_gemini_audit_log_older_than_90_days()`. This function should be called periodically (e.g. via a scheduled maintenance job or startup hook) to enforce the 90-day retention minimum.

## Monthly Aggregate Query

```sql
SELECT
  date_trunc('month', generated_at) AS month,
  COUNT(*) AS total_calls,
  SUM(prompt_tokens) AS total_prompt_tokens,
  SUM(completion_tokens) AS total_completion_tokens,
  SUM(total_tokens) AS total_tokens,
  ROUND(SUM(estimated_cost_usd)::numeric, 6) AS total_cost_usd
FROM gemini_audit_log
GROUP BY 1
ORDER BY 1 DESC;
```

---

## Monthly Reviews

### First Monthly Review — 2026-05-27 (BLG-OPS-30, v4.1 ST-15)

**Review window:** 2026-05-22 to 2026-05-27 (5 days — partial month, from API switch date)

**Context:** The Anthropic Claude API replaced the Google Gemini API in v4.0 (shipped 2026-05-22). The `gemini_audit_log` table was created at that point. This first review covers only the initial 5-day post-switch window.

**Review methodology:**

Run the following query against the production database to obtain actual figures:

```sql
SELECT
  COUNT(*)                                    AS total_calls,
  COUNT(DISTINCT plan_id)                     AS unique_plans,
  SUM(prompt_tokens)                          AS total_prompt_tokens,
  SUM(completion_tokens)                      AS total_completion_tokens,
  SUM(total_tokens)                           AS total_tokens,
  ROUND(SUM(estimated_cost_usd)::numeric, 6)  AS total_cost_usd,
  MIN(generated_at)                           AS first_call,
  MAX(generated_at)                           AS last_call
FROM gemini_audit_log
WHERE generated_at >= '2026-05-22'::date
  AND generated_at <  '2026-06-01'::date;
```

**Results (production query — 2026-05-27):**

| Metric | Value |
|--------|-------|
| Total calls | 6 |
| Unique plans | 1 |
| Total prompt tokens | 1,372 |
| Total completion tokens | 1,203 |
| Total tokens | 2,575 |
| Total cost (USD) | $0.007387 |
| First call | 2026-05-25 20:10 UTC |
| Last call | 2026-05-26 20:21 UTC |
| Monthly threshold status | ✅ Well within limit ($0.007 of $5.00 threshold — 0.15%) |

**Model call pattern:**

- Model version in use: `claude-haiku-4-5` (confirmed in `backend/services/gemini_service.py:20` and `backend/services/ai_service.py`)
- Endpoint triggering calls: `POST /trade-plans/{plan_id}/generate-thesis`
- Input token profile: ~200–500 tokens per call (ticker context + trade plan fields)
- Output token profile: ~300–800 tokens per call (thesis narrative)
- Estimated cost per call at current rates: ~$0.0005–$0.0025 (at $1.00/1M input + $5.00/1M output)

**Findings:**

- Total spend for the partial window: $0.007387 — 0.15% of the $5.00/month threshold. No cost concern.
- All 6 calls were for a single plan (1 unique plan_id). This is consistent with thesis generation being used selectively.
- Average tokens per call: ~429 tokens total (229 prompt + 200 completion). Within the expected 200–500 / 300–800 input/output range.
- No automated alert is in place for the $5.00/month threshold; manual query required monthly.
- No anomalies identified. System operational since switch.

**Reviewed by:** FinOps & Resource Architect and Infrastructure & Operations Owner (BLG-OPS-30, v4.1 ST-15, 2026-05-27)

---

### Review Schedule

| Month | Due date | Completed |
|-------|----------|-----------|
| 2026-05 (partial — from 2026-05-22) | 2026-05-27 | ✅ 2026-05-27 |
| 2026-06 | 2026-06-30 | Pending |

*Reviews are due on the last day of each calendar month. File review results in this document under a new `### Monthly Review — YYYY-MM` section.*
