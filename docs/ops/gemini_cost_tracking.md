**Owner:** FinOps & Resource Architect
**Class:** Operations Document (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-24
**Source:** ST-08 (BLG-OPS-26, v4.0 EPIC-03)

# Gemini API Cost Tracking

## Model and Pricing

| Model | Input token rate | Output token rate |
|---|---|---|
| gemini-1.5-flash | $0.075 / 1M tokens | $0.30 / 1M tokens |

*Rates as of v4.0 implementation (2026-05-24). Verify against Google AI pricing page when upgrading model versions.*

## Free-Tier Limits

| Limit | Value |
|---|---|
| Requests per day (RPD) | 1,500 |
| Tokens per month | 1,000,000 |

## Alert Threshold

**Alert fires at: 800,000 tokens/month (80% of 1M free-tier monthly limit).**

Alert condition: `SUM(total_tokens) FROM gemini_audit_log WHERE generated_at >= date_trunc('month', NOW())` > 800,000.

There is no automated alert in the current implementation — this threshold is defined for future monitoring integration. To check manually:

```sql
SELECT
  date_trunc('month', generated_at) AS month,
  COUNT(*) AS calls,
  SUM(total_tokens) AS total_tokens,
  SUM(estimated_cost_usd) AS estimated_cost_usd,
  ROUND(SUM(total_tokens)::numeric / 1000000 * 100, 1) AS pct_of_free_tier
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
| model_version | TEXT | Gemini model version string |
| prompt_version | TEXT | Prompt template version |
| input_hash | TEXT | First 16 chars of SHA-256 of input payload |
| output_hash | TEXT | First 16 chars of SHA-256 of output thesis |
| generated_at | TIMESTAMPTZ | When the call was made |
| prompt_tokens | INTEGER | Input tokens (from response.usage_metadata) |
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
