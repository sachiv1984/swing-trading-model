**Owner:** Head of Backend Engineering
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4 (EPIC-02, ST-06, BLG-BE-17)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 Drift Detection Query Pre-Design

## 1. Purpose

This document pre-designs the SQL query patterns required for SI-02 (Behavioural Drift Detection). It identifies the data fields each query requires, documents draft SQL patterns for the two primary drift dimensions (win-rate by setup type and win-rate by regime), enumerates missing fields with schema migration scope, and provides a query performance assessment at current trade volume.

Input documents:
- `docs/specs/si02/query_performance_assessment.md` — BLG-GOV-51, shipped v4.1
- `docs/specs/si02/data_prerequisite_audit.md` — data density gate status
- `docs/specs/si02/si02_index_preassessment.md` — index pre-assessment, shipped v4.4 EPIC-02

---

## 2. Fields Required per Trade Record

The following fields are required on each trade record for SI-02 drift analysis. Sources are the table and column that must contain the value at query time.

### 2.1 Fields Available Today

| Field | Source Table | Column | Notes |
|-------|-------------|--------|-------|
| Trade identifier | trade_history | id | Primary key |
| Ticker | trade_history | ticker | |
| Entry date | trade_history | entry_date | |
| Exit date | trade_history | exit_date | |
| P&L | trade_history | pnl | Used for win/loss classification |
| Portfolio ID | trade_history | portfolio_id | Filter scope |
| Position link | trade_history | position_id | Join to positions and trade_plans |
| Risk percent used | trade_plans | risk_percent_used | Sizing adherence metric |
| Checklist completed | trade_plans | checklist_completed | Boolean; process discipline signal |
| Regime context at entry | trade_plans | regime_context_at_entry | Market regime label at time of entry |
| Total cost | trade_history | total_cost | Sizing adherence denominator |

### 2.2 Fields Required but Not Yet Available

| Field | Required For | Gap Reference | Migration Required |
|-------|-------------|---------------|--------------------|
| regime_at_entry | Win-rate by regime query | Gap from data_prerequisite_audit.md | Alias for `regime_context_at_entry`; field exists but label standardisation may be needed — verify at implementation |
| setup_type_at_entry | Win-rate by setup type query | Not present in current schema | DS-07 migration: add `setup_type` column to `trade_plans` |
| entry_condition_score | Signal quality weighting | Not present in current schema | DS-07 migration: add `entry_condition_score` NUMERIC(4,2) to `trade_plans` |
| signal_id | Entry timing drift | Not present in `trade_plans` | DS-07 migration: add `signal_id` UUID FK to `trade_plans` |
| signal_date | Entry timing drift | Derived via signals join | Requires `signal_id` link; no additional migration once signal_id added |
| portfolio_value_at_entry | Sizing adherence % | Available via portfolio_history join | No new column needed; correlated subquery approach |

**Net schema migration scope:** DS-07 migration must add 3 columns to `trade_plans`: `setup_type VARCHAR(64)`, `entry_condition_score NUMERIC(4,2)`, `signal_id UUID REFERENCES signals(id)`. The `regime_context_at_entry` field already exists and does not require a migration, but population coverage must be confirmed as consistently populated across trade_plans rows.

---

## 3. Draft SQL Query Patterns

### 3.1 Win-Rate by Setup Type

**Purpose:** Detects drift in entry behaviour per stated setup type. If a trader's stated edge is "breakout" setups but their recent win-rate on breakout entries is declining, that is behavioural drift.

**Gate dependency:** Requires DS-07 migration (setup_type column must exist in trade_plans).

```sql
-- win_rate_by_setup_type
-- Rolling win-rate per setup type over a configurable lookback window.
-- Win = trade_history.pnl > 0
-- Groups by setup_type captured at trade entry.
SELECT
    tp.setup_type,
    COUNT(th.id)                                            AS total_trades,
    COUNT(CASE WHEN th.pnl > 0 THEN 1 END)                 AS wins,
    ROUND(
        COUNT(CASE WHEN th.pnl > 0 THEN 1 END)::NUMERIC
        / NULLIF(COUNT(th.id), 0),
        4
    )                                                       AS win_rate,
    ROUND(AVG(th.pnl), 2)                                  AS avg_pnl,
    MAX(th.exit_date)                                       AS most_recent_exit
FROM trade_history th
JOIN positions p ON th.position_id = p.id
JOIN trade_plans tp ON tp.position_id = p.id
WHERE th.portfolio_id = $1
  AND tp.setup_type IS NOT NULL
  AND th.exit_date >= CURRENT_DATE - ($2 * INTERVAL '1 day')  -- lookback days param
GROUP BY tp.setup_type
ORDER BY total_trades DESC;
```

**Parameters:** `$1` = portfolio_id, `$2` = lookback window in days (default: 180).

**Drift signal:** If `win_rate` for any `setup_type` drops more than 15 percentage points below the historical baseline for that type, surface as advisory drift indicator.

**Index utilisation:**
- `idx_trade_history_portfolio` (portfolio_id filter) — exists
- `idx_trade_plans_position` (position_id join) — exists
- `idx_trade_history_exit_date` (exit_date filter) — to be added at SI-02 sprint (see `si02_index_preassessment.md §4.2`)

---

### 3.2 Win-Rate by Regime at Entry

**Purpose:** Detects whether the trader's behaviour is appropriately adjusted to regime conditions. If trades are consistently entered in unfavourable regimes (e.g. bear regime) with poor outcomes, drift from stated regime-sensitive strategy is indicated.

**Gate dependency:** Requires `regime_context_at_entry` to be consistently populated in trade_plans. Field exists today; population coverage to be verified at SI-02 sprint start.

```sql
-- win_rate_by_regime_at_entry
-- Win-rate grouped by market regime recorded at trade entry.
SELECT
    tp.regime_context_at_entry                             AS regime,
    COUNT(th.id)                                           AS total_trades,
    COUNT(CASE WHEN th.pnl > 0 THEN 1 END)                AS wins,
    ROUND(
        COUNT(CASE WHEN th.pnl > 0 THEN 1 END)::NUMERIC
        / NULLIF(COUNT(th.id), 0),
        4
    )                                                      AS win_rate,
    ROUND(AVG(th.pnl), 2)                                  AS avg_pnl,
    ROUND(AVG(th.holding_days), 1)                         AS avg_holding_days
FROM trade_history th
JOIN positions p ON th.position_id = p.id
JOIN trade_plans tp ON tp.position_id = p.id
WHERE th.portfolio_id = $1
  AND tp.regime_context_at_entry IS NOT NULL
GROUP BY tp.regime_context_at_entry
ORDER BY total_trades DESC;
```

**Parameters:** `$1` = portfolio_id.

**Drift signal:** If trade count in a risk-off or bear regime exceeds 30% of total trades, surface as advisory drift indicator ("elevated activity in unfavourable regime").

---

### 3.3 Entry Timing Drift

**Purpose:** Detects delay between signal generation and trade entry. Extended lag may indicate hesitation drift or missed signal timing.

**Gate dependency:** Requires DS-07 migration (signal_id and `idx_trade_plans_signal` index).

```sql
-- entry_timing_drift
-- Distribution of days from signal date to trade entry date.
SELECT
    th.ticker,
    th.entry_date,
    s.signal_date,
    (th.entry_date - s.signal_date)                        AS days_signal_to_entry,
    tp.regime_context_at_entry,
    tp.setup_type
FROM trade_history th
JOIN positions p ON th.position_id = p.id
JOIN trade_plans tp ON tp.position_id = p.id
LEFT JOIN signals s ON s.id = tp.signal_id
WHERE th.portfolio_id = $1
  AND tp.signal_id IS NOT NULL
ORDER BY th.entry_date DESC
LIMIT 100;
```

**Aggregation layer (application-side):** Compute median and p90 of `days_signal_to_entry`. If p90 > 5 trading days, surface as advisory drift indicator ("signal-to-entry lag elevated").

---

### 3.4 Sizing Adherence

**Purpose:** Detects whether actual position size (as % of portfolio) deviates from stated risk parameters.

**Gate dependency:** `portfolio_history` must have snapshots available for trade entry dates.

```sql
-- sizing_adherence
-- Actual position size as % of portfolio vs stated risk_percent_used.
SELECT
    th.ticker,
    th.entry_date,
    th.total_cost                                                      AS position_cost,
    tp.risk_percent_used                                               AS planned_risk_pct,
    (
        SELECT ph.total_value
        FROM portfolio_history ph
        WHERE ph.snapshot_date <= th.entry_date
        ORDER BY ph.snapshot_date DESC
        LIMIT 1
    )                                                                  AS portfolio_value_at_entry,
    ROUND(
        th.total_cost::NUMERIC
        / NULLIF(
            (SELECT ph.total_value FROM portfolio_history ph
             WHERE ph.snapshot_date <= th.entry_date
             ORDER BY ph.snapshot_date DESC LIMIT 1),
            0
        ) * 100,
        2
    )                                                                  AS actual_size_pct
FROM trade_history th
JOIN positions p ON th.position_id = p.id
JOIN trade_plans tp ON tp.position_id = p.id
WHERE th.portfolio_id = $1
ORDER BY th.entry_date DESC;
```

**Drift signal (application-side):** If `actual_size_pct > planned_risk_pct * 1.25` for more than 2 trades in the last 10, surface as advisory drift indicator ("position sizing above plan").

---

### 3.5 Consecutive Loss Context

**Purpose:** Detects whether sizing behaviour changes during losing streaks (a common behavioural drift pattern — traders either over-size attempting to recover, or under-size due to confidence erosion).

**Reference:** Pattern retained from `query_performance_assessment.md §2.2`. O(N²) risk noted; see performance section below.

```sql
-- consecutive_loss_context
-- risk_percent_used in context of prior consecutive losses (60-day window).
SELECT
    th.entry_date,
    th.ticker,
    th.pnl,
    tp.risk_percent_used,
    COUNT(CASE WHEN th2.pnl < 0 THEN 1 END)               AS prior_losses_60d
FROM trade_history th
JOIN trade_plans tp ON tp.position_id = th.position_id
JOIN trade_history th2
    ON th2.portfolio_id = th.portfolio_id
   AND th2.exit_date < th.entry_date
   AND th2.exit_date >= th.entry_date - INTERVAL '60 days'
WHERE th.portfolio_id = $1
GROUP BY th.id, th.entry_date, th.ticker, th.pnl, tp.risk_percent_used
ORDER BY th.entry_date;
```

**Note:** Self-join is O(N²). At < 20 trades this is negligible. Mitigated at scale by `idx_trade_history_exit_date` composite index (see `si02_index_preassessment.md §4.2`). At 200+ trades, switch to pre-computed rolling loss count stored in `trade_plans` as a JSONB snapshot field.

---

## 4. Missing Data Fields — Schema Migration Scope

| Field | Table | Type | Migration Complexity | Blocking for SI-02? |
|-------|-------|------|---------------------|---------------------|
| setup_type | trade_plans | VARCHAR(64) NULL | XS — single ALTER TABLE; backfill from existing tags/notes if possible | Yes — required for win_rate_by_setup_type query |
| entry_condition_score | trade_plans | NUMERIC(4,2) NULL | XS — single ALTER TABLE; populated by user at plan creation | No — enhances drift weighting but not required for MVP |
| signal_id | trade_plans | UUID NULL REFERENCES signals(id) | S — ALTER TABLE + FK constraint + `idx_trade_plans_signal` index (see `si02_index_preassessment.md §4.1`) | Yes — required for entry timing drift query |

**DS-07 migration must include all three column additions.** The `regime_context_at_entry` field already exists and does not require a migration, but population coverage must be verified before the SI-02 sprint seals.

**Total migration complexity:** S (small) — three column additions in a single migration file; no data transformation required for MVP. Optional backfill of `setup_type` from trade notes is a separate, post-sprint task.

---

## 5. Query Performance Assessment

### 5.1 Current Trade Volume

Per `data_prerequisite_audit.md §2.1`: trade_history currently contains < 20 closed trades. The data density gate (PT-04 gate: >= 20 trades) is not yet met as of the v4.4 sprint.

### 5.2 Estimated Query Cost at Current Volume

Baseline: Supabase with Supavisor pooling, p50 ~230ms per `query_performance_assessment.md §4`.

| Query | Estimated rows scanned (20 trades) | Estimated p50 | Notes |
|-------|-----------------------------------|---------------|-------|
| win_rate_by_setup_type | ~20 trade_history + ~20 trade_plans join rows | ~250ms | Index-supported; negligible cost |
| win_rate_by_regime_at_entry | ~20 trade_history + ~20 trade_plans join rows | ~250ms | Index-supported; negligible cost |
| entry_timing_drift | ~20 rows + signals join | ~280ms | Requires signal_id; DS-07 gate |
| sizing_adherence | ~20 rows + correlated subquery (portfolio_history) | ~350ms | Correlated subquery adds overhead; acceptable at this volume |
| consecutive_loss_context | ~20 x ~20 = 400 self-join rows | ~350ms | O(N²) self-join; negligible at < 20 trades |

**Overall assessment:** All drift queries run within 500ms p50 at current volume. No performance risk before 200 trades.

### 5.3 Performance Risk at Scale

| Threshold | Query at risk | Mitigation |
|-----------|-------------|------------|
| 100+ trades | sizing_adherence (correlated subquery) | Materialise `portfolio_value_at_entry` into trade_plans at entry time |
| 200+ trades | consecutive_loss_context (self-join) | Pre-compute rolling loss count; store in trade_plans JSONB snapshot field |
| 500+ trades | All aggregation queries | Add `idx_trade_history_exit_date` and `idx_trade_history_entry_date` (per `si02_index_preassessment.md §4.2`); consider query result caching (TTL 8h matching arc5-compliance pattern) |

### 5.4 Row Count Reference

| Table | Estimated rows (current) | Notes |
|-------|--------------------------|-------|
| trade_history | < 20 | PT-04 gate not yet met |
| trade_plans | < 20 | Linked to positions; coverage unverified |
| positions | ~20-40 | Includes open positions |
| signals | Unknown | Populated by signal generation engine |
| portfolio_history | Unknown | Populated by daily snapshot task |

---

## 6. Sign-Off

Reviewed in role as Head of Backend Engineering. Query patterns are appropriate for the current data model and trade volume. DS-07 migration scope is confirmed as small (XS-S). Performance risk is low at current volume and can be mitigated incrementally at scale thresholds documented above.

| Role | Status | Date |
|------|--------|------|
| Head of Backend Engineering | Approved | 2026-05-29 |
