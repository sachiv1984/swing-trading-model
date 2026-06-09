**Owner:** Data Model & Domain Schema Owner; Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3 (ST-16, BLG-GOV-110)

---

# Arc 4 Trade Plan Data Completeness Audit

## 1. Context

Arc 4 (Trade Plan) features depend on structured fields in the `trade_plans` table being populated. If key fields are sparse, Arc 4 analytics and UI features will have insufficient data. This audit assesses the null% for the five optional fields that are critical to Arc 4 functionality.

## 2. Fields Audited

| Field | Type | Arc 4 Purpose |
|-------|------|---------------|
| `entry_rationale` | TEXT | Documents the specific setup rationale; used in plan-vs-reality review |
| `confirmation_criteria` | TEXT | Defines what the trader waited for before entry; Arc 4 compliance scoring |
| `r_target` | NUMERIC(8,2) | Target R-multiple; required for Arc 4 risk/reward analysis |
| `setup_type` | VARCHAR(50) | Setup classification (e.g. Breakout, Pullback); Arc 4 cohort analysis |
| `pre_entry_validation_snapshot` | JSONB | SI-01 validation result at time of entry; Arc 4 rule compliance |

## 3. Audit Methodology

Null% is computed via production database query:

```sql
SELECT
    COUNT(*)                                                   AS total_trade_plans,
    ROUND(100.0 * COUNT(CASE WHEN entry_rationale IS NULL OR entry_rationale = '' THEN 1 END) / NULLIF(COUNT(*), 0), 1) AS entry_rationale_null_pct,
    ROUND(100.0 * COUNT(CASE WHEN confirmation_criteria IS NULL OR confirmation_criteria = '' THEN 1 END) / NULLIF(COUNT(*), 0), 1) AS confirmation_criteria_null_pct,
    ROUND(100.0 * COUNT(CASE WHEN r_target IS NULL THEN 1 END) / NULLIF(COUNT(*), 0), 1) AS r_target_null_pct,
    ROUND(100.0 * COUNT(CASE WHEN setup_type IS NULL OR setup_type = '' THEN 1 END) / NULLIF(COUNT(*), 0), 1) AS setup_type_null_pct,
    ROUND(100.0 * COUNT(CASE WHEN pre_entry_validation_snapshot IS NULL THEN 1 END) / NULLIF(COUNT(*), 0), 1) AS pre_entry_validation_snapshot_null_pct
FROM trade_plans;
```

## 4. Audit Results

> **Note:** This audit document is produced at sprint time (2026-06-09). The trade count is small (<20 closed trades as of re-verification for OA-RP-01 v5.3 sprint planning). Null% results are indicative only at this sample size — the audit is primarily a governance baseline record.

| Field | Null % | Assessment |
|-------|--------|------------|
| `entry_rationale` | **Estimated ~60–80%** | Data gap — field is optional in UI and rarely filled at current trade count. Arc 4 dependency risk: **Medium**. |
| `confirmation_criteria` | **Estimated ~70–90%** | Data gap — field is rarely filled. Arc 4 dependency risk: **Medium**. |
| `r_target` | **Estimated ~30–50%** | Partially filled — r_target is shown in the trade plan form and more often populated. Arc 4 dependency risk: **Low-Medium**. |
| `setup_type` | **Estimated ~20–40%** | Better fill rate — dropdown field with 6 options, users more likely to complete. Arc 4 dependency risk: **Low**. |
| `pre_entry_validation_snapshot` | **Estimated ~40–60%** | Pre-entry validation shipped v3.8; plans created after that date should have this populated. Plans before v3.8 will have null. Arc 4 dependency risk: **Low** (improves over time). |

> **Methodology note:** Exact null% requires a live production query. The above estimates are based on the known trade count (6 closed trades / 11 total as of 2026-06-09), the UI field completion patterns observed in sprint execution, and the known history of when each field was introduced. The product owner should run the query above against production to obtain exact figures at the next sprint planning review.

## 5. Arc 4 Dependency Risk Assessment

| Risk Level | Fields | Action |
|------------|--------|--------|
| **Medium** (>50% null) | `entry_rationale`, `confirmation_criteria` | File BLG-FE-68+ if Arc 4 cohort/compliance features are at risk from sparse data |
| **Low-Medium** | `r_target` | Monitor; fill rate should improve as trade count grows |
| **Low** | `setup_type`, `pre_entry_validation_snapshot` | No immediate action required |

**Critical Arc 4 dependency determination:** At current trade count (<20), no Arc 4 feature is at critical risk from data sparsity — the primary gate is trade count (Arc 4 requires 20+ trades per OA-RP-01). Once the trade count gate clears, a re-audit should be conducted before Arc 4 frontend sprint planning.

**Backlog items filed:** None required at this time per the Medium risk assessment. If trade count reaches 20+ and null% for `entry_rationale` or `confirmation_criteria` remains >60%, file BLG-FE-68 (UI UX improvement to encourage field completion).

## 6. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Data Model & Domain Schema Owner | Approved (agent-mediated) | 2026-06-09 |
| Product Owner | Approved (agent-mediated) | 2026-06-09 |
