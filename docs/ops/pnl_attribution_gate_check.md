**Owner:** Financial Reporting & Records Owner
**Class:** Operations Document (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-27
**Source:** ST-15 (BLG-OPS-32, v4.1 EPIC-04)

---

# P&L Attribution Gate Check

## Purpose

This document is the pre-Arc 5 gate check confirming that the P&L reporting layer correctly handles both plan-linked and non-plan-linked closed trades. It must be reviewed by the Financial Reporting & Records Owner before Arc 5 compliance metrics are integrated into the P&L report (ST-08, BLG-FEAT-40/42).

---

## 1. Attribution Model

The `trade_history` table does not carry a direct `plan_id` FK. Attribution from a closed trade to a trade plan is indirect:

```
trade_history.position_id → positions.id → trade_plans.position_id (nullable)
```

| Linkage type | Condition | Description |
|---|---|---|
| Plan-linked | `trade_history.position_id IS NOT NULL` AND a `trade_plans` row exists with `trade_plans.position_id = trade_history.position_id` | Trade was entered with a structured pre-trade plan |
| Position-linked only | `trade_history.position_id IS NOT NULL` AND no matching `trade_plans` row | Position existed but no trade plan was created |
| Unlinked | `trade_history.position_id IS NULL` | Trade record has no position linkage (legacy import or manual entry) |

**Note:** `trade_plans.position_id` is nullable — a trade plan may exist without being linked to a position (draft plans, abandoned plans). These do not appear in trade_history attribution.

---

## 2. Attribution Count Query

Run the following query against the production database to obtain current attribution counts:

```sql
SELECT
  CASE
    WHEN th.position_id IS NULL THEN 'unlinked'
    WHEN tp.id IS NOT NULL      THEN 'plan_linked'
    ELSE                             'position_linked_no_plan'
  END AS attribution_type,
  COUNT(*)                                   AS trade_count,
  ROUND(SUM(th.pnl)::numeric, 2)             AS total_pnl_gbp,
  ROUND(AVG(th.pnl_pct)::numeric, 2)         AS avg_pnl_pct
FROM trade_history th
LEFT JOIN trade_plans tp ON tp.position_id = th.position_id
WHERE th.portfolio_id = '<portfolio_id>'   -- substitute active portfolio UUID
GROUP BY 1
ORDER BY 1;
```

**Results (production query — 2026-05-27, portfolio `8631cbc2-826d-420d-bfc7-ac27c83a3e2b`):**

| Attribution type | Trade count | Total P&L (GBP) | Avg P&L % |
|---|---|---|---|
| plan_linked | 0 | — | — |
| position_linked_no_plan | 6 | -2.71 | 2.13 |
| unlinked | 0 | — | — |
| **Total** | **6** | **-2.71** | **2.13** |

*All 6 closed trades are position-linked with no associated trade plan. This is expected — trade plans were introduced post v3.x; early trades pre-date the feature.*

---

## 3. P&L Report Behaviour

The P&L report (`GET /reports/tax-year`) aggregates all `trade_history` rows for the portfolio within the requested tax year, regardless of plan linkage. Relevant properties:

| Property | Confirmed | Notes |
|---|---|---|
| Aggregates all `trade_history` rows regardless of `position_id` | ✅ | `database.get_trade_history_by_tax_year` queries `WHERE portfolio_id = %s AND exit_date BETWEEN %s AND %s` — no plan filter |
| Includes unlinked trades in totals | ✅ | No exclusion condition on `position_id IS NULL` |
| `pnl` and `pnl_pct` present for all trade_history rows | ✅ | Both fields nullable but populated at exit time by `close_position` logic |
| Attribution type not currently exposed in report | ℹ️ | The report does not distinguish plan-linked vs. non-plan trades — by design for Arc ≤ 4 |

**Arc 5 integration note:** When ST-08 adds Arc 5 compliance metrics to the P&L report, the compliance section must operate only on plan-linked trades (those with a matching `trade_plans` row). Non-plan-linked trades must not be counted toward Arc 5 compliance metrics, as compliance is defined relative to pre-trade rule adherence. The query in §2 above provides the base counts needed for that filter.

---

## 4. Attribution Anomalies

| Anomaly type | Status | Notes |
|---|---|---|
| Unlinked trades (position_id IS NULL) | ✅ None found | Production query returned 0 unlinked rows |
| Duplicate position linkage (position_id → multiple trade_plans rows) | ✅ None found | Duplicate-plan check query returned 0 rows (2026-05-27) |
| Closed position with no matching trade_history row | Out of scope for this check | Tracked separately via positions reconciliation |

**Duplicate plan linkage mitigation query:**

```sql
SELECT position_id, COUNT(*) AS plan_count
FROM trade_plans
WHERE position_id IS NOT NULL
GROUP BY position_id
HAVING COUNT(*) > 1;
```

Run before Arc 5 integration. If rows returned, use `DISTINCT ON (th.id)` or `LATERAL` join to resolve.

---

## 5. Gate Decision

| Gate | Condition | Status |
|---|---|---|
| Attribution model understood | Plan-linked path documented and SQL provided | ✅ Pass |
| P&L report handles both cases | Confirmed — no attribution filter in current report | ✅ Pass |
| Production attribution counts obtained | Confirmed — 6 trades, all position_linked_no_plan | ✅ Pass |
| No blocking anomalies | No unlinked trades; no duplicate plan linkage | ✅ Pass |
| Arc 5 integration approach defined | Compliance metrics limited to plan-linked trades | ✅ Pass |

**Overall gate status: PASS** — production counts confirmed, no anomalies found, Arc 5 integration approach validated. Safe to proceed with ST-08.

---

## 6. Sign-Off

| Role | Status | Date |
|---|---|---|
| Financial Reporting & Records Owner | Reviewed (BLG-OPS-32, v4.1 ST-15) | 2026-05-27 |
