**Owner:** Head of Engineering
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-26__release-v4.1 (ST-13, BLG-GOV-51)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 DB Query Performance Pre-Assessment

## 1. Purpose

This document assesses the database query performance risk for SI-02 (Behavioural Drift Detection) queries before implementation begins. SI-02 requires joining multiple tables (`trade_history`, `trade_plans`, `signals`, `positions`, `portfolio_history`) to compute drift metrics. This assessment identifies expected query cost and recommends an index strategy.

---

## 2. Query Pattern Analysis

### 2.1 Core Drift Query

The primary SI-02 query is expected to be:

```sql
-- Entry timing drift: time from signal date to entry date
SELECT
  th.ticker,
  th.entry_date,
  s.signal_date,
  (th.entry_date - s.signal_date) AS days_from_signal_to_entry,
  tp.risk_percent_used,
  tp.checklist_completed,
  tp.regime_context_at_entry
FROM trade_history th
JOIN positions p ON th.position_id = p.id
JOIN trade_plans tp ON tp.position_id = p.id
LEFT JOIN signals s ON s.id = tp.signal_id  -- requires DS-07 migration
WHERE th.portfolio_id = $1
ORDER BY th.entry_date DESC
LIMIT 100;
```

### 2.2 Consecutive Loss Detection Query

```sql
-- Sizing adherence in context of run of losses
SELECT
  th.entry_date,
  th.pnl,
  tp.risk_percent_used,
  SUM(CASE WHEN th2.pnl < 0 THEN 1 ELSE 0 END) AS prior_consecutive_losses
FROM trade_history th
JOIN trade_plans tp ON tp.position_id = th.position_id
JOIN trade_history th2 ON th2.portfolio_id = th.portfolio_id
  AND th2.exit_date < th.entry_date
  AND th2.exit_date >= th.entry_date - INTERVAL '60 days'
WHERE th.portfolio_id = $1
GROUP BY th.id, th.entry_date, th.pnl, tp.risk_percent_used
ORDER BY th.entry_date;
```

**Risk:** The self-join on `trade_history` (th2) to compute prior consecutive losses is O(N²) in the worst case. With 20–50 trades this is negligible; with 500+ trades it may cause noticeable latency.

---

## 3. Index Analysis

### 3.1 Existing Indexes (Relevant to SI-02)

| Table | Index | Column(s) | Available |
|-------|-------|-----------|-----------|
| trade_history | idx_trade_history_portfolio | portfolio_id | ✅ |
| trade_history | idx_trade_history_ticker | ticker | ✅ |
| positions | idx_positions_portfolio | portfolio_id | ✅ |
| trade_plans | idx_trade_plans_portfolio | portfolio_id | ✅ |
| trade_plans | idx_trade_plans_position | position_id WHERE position_id IS NOT NULL | ✅ |
| signals | idx_signals_portfolio | portfolio_id | ✅ |
| signals | idx_signals_date | signal_date DESC | ✅ |

### 3.2 Missing Indexes for SI-02

| Table | Proposed Index | Purpose | Priority |
|-------|---------------|---------|----------|
| trade_plans | `idx_trade_plans_signal ON trade_plans(signal_id) WHERE signal_id IS NOT NULL` | Join from signals to trade_plans for timing analysis | P1 — add with DS-07 migration |
| trade_history | `idx_trade_history_exit_date ON trade_history(portfolio_id, exit_date DESC)` | Consecutive loss window query (self-join optimisation) | P2 — add at SI-02 sprint |
| trade_history | `idx_trade_history_entry_date ON trade_history(portfolio_id, entry_date DESC)` | Time-ordered drift analysis | P2 — add at SI-02 sprint |

**Note:** `idx_trade_plans_signal` is already included in the DS-07 migration definition in `si02_gap_analysis.md §6`.

---

## 4. Estimated Query Cost

At Supabase with Supavisor pooling (enabled v2.7), DB-backed endpoints have p50 of ~230ms (per `api_performance_baseline.md §10`).

| Query | Estimated rows (20 trades) | Estimated p50 | Estimated p50 (200 trades) | Risk |
|-------|--------------------------|---------------|---------------------------|------|
| Core drift query (single portfolio) | 20 join rows | ~250ms | ~300ms | Low |
| Consecutive loss window query | 20×20 = 400 join rows | ~350ms | ~2,000ms | Medium at scale |
| Full drift aggregation (all metrics) | ~20–50 aggregated rows | ~400ms | ~800ms | Low–Medium |

**Assessment:** At current trade volume (< 20 trades), all drift queries are expected to run within 500ms p50. Performance risk materialises at 200+ trades with the consecutive loss self-join. Threshold: if `trade_history` count exceeds 200 for a portfolio, the consecutive loss query should switch to a pre-computed rolling window (stored in `trade_plans.effective_settings_snapshot` or a dedicated `trade_stats_at_entry` JSONB field).

---

## 5. Recommendations

| Recommendation | Priority | Sprint |
|----------------|---------|--------|
| Add `idx_trade_plans_signal` index with DS-07 migration | P1 | DS-07 sprint |
| Add `idx_trade_history_exit_date` composite index at SI-02 sprint | P2 | SI-02 Sprint |
| Add `idx_trade_history_entry_date` composite index at SI-02 sprint | P2 | SI-02 Sprint |
| Monitor consecutive loss query latency when trade count exceeds 100 | P3 | Post-SI-02 |
| Pre-compute consecutive loss state at entry time (`trade_stats_at_entry` field) when portfolio reaches 200+ trades | P3 | Future |

---

## 6. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Head of Engineering | Pending | — |
| Head of Backend Engineering | Pending | — |
