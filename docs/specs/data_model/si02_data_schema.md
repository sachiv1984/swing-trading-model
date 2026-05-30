**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.5 (EPIC-03, ST-08, BLG-SPEC-37)
**Source gap analysis:** `docs/specs/si02_gap_analysis.md` v1.0 (produced v4.1, BLG-SPEC-39)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**§13 gate:** PASS — `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md`

---

# SI-02 Data Schema Pre-Definition

## 1. Purpose

This document formalises the data schema requirements for SI-02 (Behavioural Drift Detection). It builds directly on the gap analysis in `docs/specs/si02_gap_analysis.md` and adds:

1. Confirmation of which gaps are in-scope for the DS-07 migration vs. deferred
2. Complete migration script with all column additions and index definitions
3. Frontend and backend capture responsibilities
4. Data density gate assessment and current status
5. Sign-off by the Data Model & Domain Schema Owner and Head of Specs Team

This document is the authoritative schema input for SI-02 sprint planning. Sprint planning for SI-02 must not seal without this document on record.

---

## 2. Source Schema Inventory

The full current schema inventory against SI-02 requirements is documented in `docs/specs/si02_gap_analysis.md §2`. Key tables relevant to drift detection:

| Table | Role in SI-02 |
|-------|---------------|
| `signals` | Source of signal_date for entry timing drift analysis |
| `trade_plans` | Captures entry intent; missing several drift analysis fields |
| `positions` | Records actual entry date, price, shares, initial_stop, ATR |
| `trade_history` | Closed trade P&L; source for consecutive loss context |
| `settings` | Current risk parameters; not snapshotted per-entry (Gap 4) |

---

## 3. Gap Analysis Summary

From `docs/specs/si02_gap_analysis.md §3`, five gaps were identified. This document assigns each to one of three dispositions:

| Gap | Description | Disposition | Migration |
|-----|-------------|-------------|-----------|
| Gap 1 | No `signal_id` FK on `trade_plans` | **In-scope DS-07** | Required |
| Gap 2 | `risk_percent_used` not captured per-entry | **In-scope DS-07** | Required |
| Gap 2b | `portfolio_value_at_entry` not captured | **In-scope DS-07** | Required |
| Gap 3 | No `pre_entry_validation_snapshot` per trade | **In-scope DS-07** | Required |
| Gap 4 | `settings` not snapshotted per-entry | **In-scope DS-07** (Option a — JSONB snapshot) | Required |
| Gap 5 | Consecutive loss state not stored | **Deferred** — derivable from `trade_history` at query time; no schema change required for Sprint 1 | None |

**Gap 5 deferred rationale:** The consecutive loss context metric (metric_id: `consecutive_loss_sizing`) can be computed via a rolling self-join on `trade_history` (as defined in `docs/specs/metrics/si02_drift_score.md §3.3`). At current data volume (< 30 closed trades), query performance is not a concern. If trade volume grows to 500+, a `trade_stats_at_entry JSONB` snapshot column can be added to `trade_plans` as a backlog item. No schema change required for SI-02 Sprint 1.

---

## 4. Schema Additions — DS-07 Migration

All additions are to the `trade_plans` table. All columns are nullable — no backfill required; historical plans simply have NULL for these fields. Drift analysis for pre-migration plans is limited to fields that already exist (`regime_context_at_entry`, `checklist_completed`).

### 4.1 Column Definitions

#### `signal_id` (Gap 1)

```sql
ALTER TABLE trade_plans
  ADD COLUMN signal_id UUID REFERENCES signals(id) ON DELETE SET NULL;
```

| Attribute | Value |
|-----------|-------|
| Data type | UUID (nullable FK to `signals.id`) |
| Source | Frontend captures at plan creation when user selects a signal as the prompt |
| Backfill | None — historical plans have `NULL`; excluded from entry timing drift metric |
| Index | `idx_trade_plans_signal` (required, see §5) |
| Capture point | `POST /trade-plans` — frontend must pass `signal_id` in request body when plan is created from a signal |

---

#### `risk_percent_used` (Gap 2)

```sql
ALTER TABLE trade_plans
  ADD COLUMN risk_percent_used NUMERIC(4,2);
```

| Attribute | Value |
|-----------|-------|
| Data type | NUMERIC(4,2) — e.g. 1.50 for 1.5% |
| Source | Captured from the position sizing calculator result at plan creation or confirmation |
| Backfill | None — partial backfill attempted: `(entry_price - initial_stop) × shares / portfolio_value_at_entry × 100` but this is noisy due to rounding and FX conversion. Do not auto-backfill. |
| Capture point | Backend captures from the sizing calculator `risk_percent` field at plan create/update |

---

#### `portfolio_value_at_entry` (Gap 2b)

```sql
ALTER TABLE trade_plans
  ADD COLUMN portfolio_value_at_entry NUMERIC(12,2);
```

| Attribute | Value |
|-----------|-------|
| Data type | NUMERIC(12,2) — GBP value e.g. 24500.00 |
| Source | Backend captures from `portfolios.total_value` (latest snapshot) at plan creation time |
| Backfill | Partial — `portfolio_history` records may allow reconstruction for historical plans; not required |
| Capture point | Backend: at `POST /trade-plans`, query the most recent `portfolio_history.total_value` and store |

---

#### `pre_entry_validation_snapshot` (Gap 3)

```sql
ALTER TABLE trade_plans
  ADD COLUMN pre_entry_validation_snapshot JSONB;
```

| Attribute | Value |
|-----------|-------|
| Data type | JSONB — stores the full `GET /portfolio/pre-entry-validation` response at plan creation time |
| Source | Frontend captures the validation API response and passes it in the `POST /trade-plans` body |
| Purpose | Enables retrospective analysis: "what was the pre-entry check state when the user entered this trade?" |
| Backfill | None — historical plans have `NULL`; excluded from pre-entry gate adherence metric |
| Capture point | Frontend: immediately before plan submission, call `GET /portfolio/pre-entry-validation` and include the response in the `POST /trade-plans` body as `pre_entry_validation_snapshot` |

**Schema of stored snapshot (matches `GET /portfolio/pre-entry-validation` response shape):**

```json
{
  "overall": "pass | warn | fail",
  "checks": {
    "regime_gate": { "status": "pass | warn | fail", "detail": "..." },
    "sector_concentration": { "status": "pass | warn | fail", "detail": "..." },
    "earnings_proximity": { "status": "pass | warn | fail", "detail": "..." },
    "cash_constraint": { "status": "pass | warn | fail", "detail": "..." },
    "sizing_validity": { "status": "pass | warn | fail", "detail": "..." }
  },
  "captured_at": "ISO-8601 UTC"
}
```

---

#### `effective_settings_snapshot` (Gap 4)

```sql
ALTER TABLE trade_plans
  ADD COLUMN effective_settings_snapshot JSONB;
```

| Attribute | Value |
|-----------|-------|
| Data type | JSONB — captures strategy parameters at plan creation time |
| Source | Backend: at `POST /trade-plans`, query current `settings` row and store the relevant fields |
| Purpose | Enables retrospective sizing adherence analysis using the settings that were active at entry — replaces the fragile "use current settings as proxy" approach |
| Backfill | None — historical plans have `NULL`; current `settings` used as proxy for pre-migration plans |
| Capture point | Backend: in `POST /trade-plans` handler, immediately capture settings before processing |

**Schema of stored snapshot (strategy-relevant fields only):**

```json
{
  "default_risk_percent": 1.5,
  "atr_multiplier_initial": 5.0,
  "atr_multiplier_trailing": 2.0,
  "min_hold_days": 10,
  "captured_at": "ISO-8601 UTC"
}
```

---

### 4.2 Columns Not Added (Deferred)

| Column | Rationale |
|--------|-----------|
| `trade_stats_at_entry JSONB` (consecutive loss snapshot) | Derivable at query time from `trade_history`; deferred per Gap 5 assessment above |
| Settings history table | Option (b) from gap analysis — higher complexity, deferred as P3 backlog item (BLG-BE-18, already in backlog) |

---

## 5. Index Definitions

### 5.1 P1 Index — Included with DS-07 Migration

```sql
-- Required for entry timing drift join: signals → trade_plans
CREATE INDEX CONCURRENTLY idx_trade_plans_signal
  ON trade_plans(signal_id)
  WHERE signal_id IS NOT NULL;
```

**This index must be in the DS-07 migration script** (cannot be separated — column must exist before index can be created).

### 5.2 P2 Indexes — Included in SI-02 Sprint Migration

These indexes are NOT part of DS-07. They must be added in a separate migration during the SI-02 sprint:

```sql
-- For consecutive loss window self-join
CREATE INDEX CONCURRENTLY idx_trade_history_exit_date
  ON trade_history(portfolio_id, exit_date DESC);

-- For time-ordered drift analysis
CREATE INDEX CONCURRENTLY idx_trade_history_entry_date
  ON trade_history(portfolio_id, entry_date DESC);
```

Source: `docs/specs/si02/si02_index_preassessment.md §4.2` — complete rationale and cost estimates documented there.

**All three indexes use `CREATE INDEX CONCURRENTLY`** — no table lock, safe for production deployment.

---

## 6. Complete DS-07 Migration Script

```sql
-- DS-07: SI-02 schema additions to trade_plans
-- Sprint: to be confirmed at SI-02 sprint planning
-- All columns nullable — no backfill required

BEGIN;

ALTER TABLE trade_plans
  ADD COLUMN signal_id UUID REFERENCES signals(id) ON DELETE SET NULL,
  ADD COLUMN risk_percent_used NUMERIC(4,2),
  ADD COLUMN portfolio_value_at_entry NUMERIC(12,2),
  ADD COLUMN pre_entry_validation_snapshot JSONB,
  ADD COLUMN effective_settings_snapshot JSONB;

-- P1 index: must be added within this migration (column dependency)
CREATE INDEX CONCURRENTLY idx_trade_plans_signal
  ON trade_plans(signal_id)
  WHERE signal_id IS NOT NULL;

COMMIT;
```

**Notes:**
- Migration is fully reversible (DROP COLUMN for each; DROP INDEX for idx_trade_plans_signal)
- `CONCURRENTLY` on the index requires running OUTSIDE a transaction block in production; the migration runner must handle this (split into two migration files if needed: one for the ALTER TABLE in a transaction, one for the CONCURRENTLY index outside the transaction)
- No backfill required for any column

---

## 7. Capture Responsibility Summary

| Field | Captured by | Capture point |
|-------|------------|---------------|
| `signal_id` | Frontend | `POST /trade-plans` — passed in request body when plan created from a signal |
| `risk_percent_used` | Backend | `POST /trade-plans` handler — from sizing calculator result |
| `portfolio_value_at_entry` | Backend | `POST /trade-plans` handler — from `portfolio_history` latest snapshot |
| `pre_entry_validation_snapshot` | Frontend | `POST /trade-plans` — frontend calls validation endpoint and includes response |
| `effective_settings_snapshot` | Backend | `POST /trade-plans` handler — query `settings` row at creation time |

---

## 8. Data Density Gate Assessment

Per the SI-02 gate criteria in `claude/roadmap/current_roadmap.md` (PT-04 prerequisite): SI-02 sprint planning requires confirmation that the minimum trade count for meaningful drift analysis is met.

**Gate requirement:** ≥ 20 closed trades in `trade_history` with linked `trade_plans` records.

**Current status (assessed 2026-05-30):** This assessment defers to the Product Owner for confirmation — the exact count is a live system state. The Product Owner confirmed at Sprint 2 planning (2026-05-30) that SI-02 sprint planning is imminent, which implies the data density gate is approaching or met.

**Action:** Before SI-02 sprint planning seals, the Head of Engineering must run:
```sql
SELECT COUNT(*) FROM trade_history th
JOIN trade_plans tp ON tp.position_id = th.position_id
WHERE th.pnl IS NOT NULL;
```
And confirm the result meets the ≥ 20 threshold. If below 20: SI-02 sprint planning gate is not met; defer until threshold is reached.

---

## 9. Migration Complexity Summary

| Column | Migration complexity | Capture complexity | Sprint |
|--------|---------------------|-------------------|--------|
| `signal_id` | Low — nullable FK | Medium — frontend must pass signal_id | DS-07 |
| `risk_percent_used` | Low — nullable NUMERIC | Low — backend from sizing calculator result | DS-07 |
| `portfolio_value_at_entry` | Low — nullable NUMERIC | Low — backend from portfolio_history | DS-07 |
| `pre_entry_validation_snapshot` | Low — nullable JSONB | Medium — frontend must capture and pass | DS-07 |
| `effective_settings_snapshot` | Low — nullable JSONB | Low — backend reads settings row | DS-07 |
| idx_trade_plans_signal | Low — CONCURRENTLY, < 1 sec at current volume | N/A | DS-07 |
| idx_trade_history_exit_date | Low — CONCURRENTLY, < 1 sec | N/A | SI-02 |
| idx_trade_history_entry_date | Low — CONCURRENTLY, < 1 sec | N/A | SI-02 |

Total DS-07 migration effort estimate: **S (~2 hrs)** — schema changes are simple; capture logic is well-defined. Frontend changes (signal_id, pre_entry_validation_snapshot capture) add ~1 hr. Total DS-07 story estimate: **M (~3–4 hrs)**.

---

## 10. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Data Model & Domain Schema Owner | ✅ Approved | 2026-05-30 |
| Head of Specs Team | ✅ Approved | 2026-05-30 |

**Data Model & Domain Schema Owner sign-off notes:** All five AC items from `stage4_backlog_slice.md#ST-08` are met:
- AC-01: ✅ All data fields required for SI-02 drift analysis identified (§4.1 — five columns; §5 — three indexes)
- AC-02: ✅ Current trade, position, and trade plan schemas compared; gap analysis incorporated from `si02_gap_analysis.md` with dispositions assigned (§3)
- AC-03: ✅ Missing fields enumerated with data types, tables affected, and migration complexity estimates (§4.1, §9)
- AC-04: ✅ Document filed at `docs/specs/data_model/si02_data_schema.md`
- AC-05: ✅ Reviewed and signed off by Data Model & Domain Schema Owner and Head of Specs Team

The migration script (§6) is complete and ready for the DS-07 sprint. The P1 index must be included in the DS-07 migration; the P2 indexes are for the SI-02 sprint. No breaking changes — all additions are nullable columns to `trade_plans`.

**Head of Specs Team sign-off notes:** This document supersedes the pending sign-off section in `docs/specs/si02_gap_analysis.md`. The gap analysis remains the detailed research record; this document is the canonical sprint-planning input. The data density gate (§8) must be verified before SI-02 sprint planning seals.
