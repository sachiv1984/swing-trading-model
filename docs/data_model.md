**Owner:** Head of Engineering
**Class:** Living Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-15
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Data Model Reference

This document records the canonical data model for the swing trading system database. Each section describes a table, its key fields, and any schema migrations applied.

---

## Schema Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-15 | Initial document — ST-05 (EPIC-02, v3.5). Records plan_vs_reality JSONB on trade_history and planned_stop_price on trade_plans. |

---

## Tables

---

### `trade_history`

Stores closed trade records. One row per closed position.

**Key fields:**

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| portfolio_id | UUID | FK to portfolios |
| position_id | UUID | FK to positions (the closed position) |
| ticker | TEXT | Ticker symbol |
| market | TEXT | Market code (US, UK) |
| entry_date | DATE | Trade entry date |
| exit_date | DATE | Trade exit date |
| shares | NUMERIC | Share quantity |
| entry_price | NUMERIC | Entry price in native currency |
| exit_price | NUMERIC | Exit price in native currency |
| pnl | NUMERIC | Realised P&L |
| pnl_pct | NUMERIC | P&L as percentage |
| holding_days | INTEGER | Days held |
| exit_reason | TEXT | Reason for exit |
| tags | TEXT[] | User-assigned tags |
| entry_note | TEXT | Notes recorded at entry |
| exit_note | TEXT | Notes recorded at exit |
| fill_price | NUMERIC | Actual fill price (may differ from entry_price) |
| **plan_vs_reality** | **JSONB** | **Plan vs Reality comparison record (PO-01). Populated by plan_vs_reality_service on trade close. NULL if no trade plan was linked. Schema: see §plan_vs_reality JSONB structure below.** |

**Migration v1.0 — 2026-05-15:**
```sql
ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS plan_vs_reality JSONB;
```
Applied via `ensure_plan_vs_reality_columns()` at startup. ST-05 (EPIC-02, v3.5).

---

#### `plan_vs_reality` JSONB Structure

| Key | Type | Description |
|-----|------|-------------|
| plan_linked | boolean | Whether a trade plan was linked |
| trade_plan_id | uuid | ID of the linked trade plan |
| r_achieved | float \| null | Actual R-multiple achieved: (exit - entry) / (entry - initial_stop) |
| r_target | float \| null | Planned R target from trade plan |
| r_delta | float \| null | r_achieved - r_target |
| entry_delta_pct | float \| null | Entry timing accuracy: (actual - planned) / planned * 100. null until planned_entry_price snapshot is implemented. |
| stop_discipline | string | "on_plan" / "minor_deviation" / "deviation" / "not_captured" |
| exit_reason_actual | string \| null | Actual exit reason |
| exit_reason_planned | string \| null | Planned early exit conditions (free text) |
| lifecycle_state_at_exit | string \| null | Position lifecycle state at time of exit |
| plan_adherence_flag | string | "on_plan" / "entry_deviation" / "stop_deviation" / "early_exit" |
| deviation_note | string \| null | User-authored deviation note (populated via ST-06 frontend view) |

---

### `trade_plans`

Stores pre-trade reasoning documents. Linked to positions via `position_id`.

**Key fields (additions only):**

| Field | Type | Description |
|-------|------|-------------|
| r_target | NUMERIC | Planned R multiple target |
| early_exit_conditions | TEXT | Free-text description of conditions that would trigger early exit |
| **planned_stop_price** | **NUMERIC(20,6)** | **Planned stop price at plan creation (numeric, optional). Added v3.5 for PO-01 plan vs reality stop_discipline comparison. NULL for plans created before v3.5.** |

**Migration v1.0 — 2026-05-15:**
```sql
ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS planned_stop_price NUMERIC(20, 6);
```
Applied via `ensure_plan_vs_reality_columns()` at startup. ST-05 (EPIC-02, v3.5).

**Note on `planned_stop_price`:** Per `docs/product/arc4_data_requirements.md` §3.1 Decision 1: this is an optional numeric field added to the TradePlan form alongside `early_exit_conditions`. Existing plans without this field have `planned_stop_price = null`; PO-01 comparison reports `stop_discipline = "not_captured"` for such trades.

---
