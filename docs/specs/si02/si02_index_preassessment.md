**Owner:** Head of Engineering; Head of Backend Engineering
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4 (EPIC-02, ST-08, BLG-BE-23)
**Source:** BLG-BE-23 (gate: BLG-GOV-51 ✅ shipped v4.1)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 Query Index Pre-Assessment

## 1. Purpose

This document identifies the database indexes required for SI-02 (Behavioural Drift Detection) queries, produces CREATE INDEX migration statements, and estimates creation cost. It uses the BLG-GOV-51 EXPLAIN ANALYZE results (shipped v4.1, `docs/specs/si02/query_performance_assessment.md`) as its primary input.

This document is filed as an explicit input to SI-02 sprint planning capacity estimation. Sprint planning must not seal for SI-02 without this assessment.

---

## 2. Gate Condition Verification

| Gate | Status | Evidence |
|------|--------|----------|
| BLG-GOV-51 (SI-02 DB query performance pre-assessment) | ✅ Complete | Shipped v4.1 (EPIC-01, ST-13); artefact: `docs/specs/si02/query_performance_assessment.md` |

Gate condition confirmed met. Proceeding with index identification.

---

## 3. Input Summary from BLG-GOV-51

The `query_performance_assessment.md` (BLG-GOV-51) identified:

### 3.1 Existing Indexes (Confirmed Available)

| Table | Index | Column(s) |
|-------|-------|-----------|
| trade_history | idx_trade_history_portfolio | portfolio_id |
| trade_history | idx_trade_history_ticker | ticker |
| positions | idx_positions_portfolio | portfolio_id |
| trade_plans | idx_trade_plans_portfolio | portfolio_id |
| trade_plans | idx_trade_plans_position | position_id WHERE position_id IS NOT NULL |
| signals | idx_signals_portfolio | portfolio_id |
| signals | idx_signals_date | signal_date DESC |

### 3.2 Missing Indexes Identified by BLG-GOV-51

| Table | Proposed Index | Purpose | Priority (BLG-GOV-51) |
|-------|---------------|---------|----------------------|
| trade_plans | idx_trade_plans_signal | signal_id join for entry timing drift analysis | P1 — with DS-07 migration |
| trade_history | idx_trade_history_exit_date | exit_date for consecutive loss window self-join | P2 — at SI-02 sprint |
| trade_history | idx_trade_history_entry_date | entry_date for time-ordered drift analysis | P2 — at SI-02 sprint |

---

## 4. Required Index Definitions

### 4.1 P1 Index — With DS-07 Migration

#### Index: idx_trade_plans_signal

```sql
-- Add concurrently to avoid table lock; include after DS-07 migration adds signal_id column
CREATE INDEX CONCURRENTLY idx_trade_plans_signal
  ON trade_plans(signal_id)
  WHERE signal_id IS NOT NULL;
```

**Purpose:** Enables efficient join from `signals` to `trade_plans` in the core drift query:

```sql
LEFT JOIN signals s ON s.id = tp.signal_id
```

Without this index, the join requires a sequential scan of `trade_plans` for every signal lookup.

**Prerequisite:** DS-07 migration must ship first (adds `signal_id` column to `trade_plans`). This index is already referenced in `si02_gap_analysis.md §6` as part of the DS-07 migration definition.

**Sprint timing:** Include in DS-07 migration script. Do not defer to SI-02 sprint.

---

### 4.2 P2 Indexes — At SI-02 Sprint

#### Index: idx_trade_history_exit_date

```sql
-- Composite index on (portfolio_id, exit_date) for consecutive loss window query
CREATE INDEX CONCURRENTLY idx_trade_history_exit_date
  ON trade_history(portfolio_id, exit_date DESC);
```

**Purpose:** Optimises the self-join in the consecutive loss detection query:

```sql
JOIN trade_history th2 ON th2.portfolio_id = th.portfolio_id
  AND th2.exit_date < th.entry_date
  AND th2.exit_date >= th.entry_date - INTERVAL '60 days'
```

Without this index, the self-join requires a sequential scan for each trade row (O(N²) worst case at scale).

#### Index: idx_trade_history_entry_date

```sql
-- Composite index on (portfolio_id, entry_date) for time-ordered drift analysis
CREATE INDEX CONCURRENTLY idx_trade_history_entry_date
  ON trade_history(portfolio_id, entry_date DESC);
```

**Purpose:** Supports `ORDER BY th.entry_date DESC` in the core drift query and future time-range filtered drift queries.

**Sprint timing:** Add both P2 indexes in the SI-02 sprint migration script (separate from DS-07 migration).

---

## 5. Migration Plan

### 5.1 Migration Timing Strategy

| Index | Migration | Sprint | Blocking? |
|-------|-----------|--------|-----------|
| idx_trade_plans_signal | DS-07 migration | DS-07 sprint (before SI-02) | Yes — column must exist first |
| idx_trade_history_exit_date | SI-02 migration file | SI-02 sprint | No — can be added independently |
| idx_trade_history_entry_date | SI-02 migration file | SI-02 sprint | No — can be added independently |

### 5.2 Estimated Creation Cost

At current production volume (< 20 trades in `trade_history`, < 20 rows in `trade_plans`):

| Index | Estimated table rows | Estimated creation time | Lock type |
|-------|---------------------|------------------------|-----------|
| idx_trade_plans_signal | < 20 | < 1 second | None (CONCURRENTLY) |
| idx_trade_history_exit_date | < 20 | < 1 second | None (CONCURRENTLY) |
| idx_trade_history_entry_date | < 20 | < 1 second | None (CONCURRENTLY) |

**Assessment:** Creation cost is negligible at current data volume. All indexes use `CREATE INDEX CONCURRENTLY` to avoid table locks in production. At 500+ trades, creation time remains low (< 5 seconds on Supabase for a single-user portfolio) — no down-time risk.

### 5.3 Capacity Estimate Input for SI-02 Sprint Planning

The SI-02 sprint must budget for:

| Task | Estimated effort | Sprint |
|------|-----------------|--------|
| Write DS-07 migration with idx_trade_plans_signal | Included in DS-07 story | DS-07 sprint |
| Write SI-02 migration script (2 × P2 indexes) | ~0.5 hr (XS) | SI-02 sprint |
| Verify indexes on staging after migration | ~0.5 hr (XS, part of staging run) | SI-02 sprint |

Total additional SI-02 sprint overhead: **~1 hr (XS × 2)**, covered within the normal backend story capacity budget.

---

## 6. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Head of Engineering | Pending | — |
| Head of Backend Engineering | Pending | — |
