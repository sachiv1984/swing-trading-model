**Owner:** Data Model & Domain Schema Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-31
**Cycle:** 2026-05-30__release-v4.6
**Source of truth:** `backend/database.py` — `ensure_trade_plans_table()`, `ensure_si02_trade_plans_columns()`, and associated ensure functions
**Related documents:** `docs/specs/data_model/si02_data_schema.md` v1.0; `docs/specs/data_model.md` DS-04 through DS-07; `claude/roadmap/current_roadmap.md`

---

# Trade Plans Schema Audit — v4.6

## 1. Purpose and Scope

This audit was produced as a post-DS-07 migration record following the v4.6 Sprint 1 delivery (ST-01, EPIC-01). The DS-07 migration added five new columns to the `trade_plans` table in support of SI-02 (Behavioural Drift Detection). This document:

1. Enumerates every field currently present in `trade_plans` as of v4.6
2. Cross-references each field to the roadmap feature that introduced or depends on it
3. Identifies orphaned fields (present in the schema but not surfaced in any current feature)
4. Identifies missing fields needed by roadmap features but not yet present
5. Provides remediation recommendations

The `trade_plans` table is the central domain object for the trading assistant system. It records the user's structured pre-trade reasoning at the time of plan creation, links to the resulting open position (once entered), and supplies the comparison baseline for Arc 4 plan vs reality analysis and Arc 5 SI-02 behavioural drift detection.

---

## 2. Schema Evolution Summary

| Migration | Version | Release | Description |
|-----------|---------|---------|-------------|
| DS-04 | data_model.md v2.5 | v3.1 | Initial `trade_plans` table — PT-01 Trade Plan Object |
| DS-06 | data_model.md v2.7 | v3.3 | `abandonment_reason` VARCHAR(500) — BLG-FEAT-21 |
| PO-01 | ensure_plan_vs_reality_columns | v3.5 | `planned_stop_price` NUMERIC(20,6) — Arc 4 plan vs reality |
| BLG-FEAT-23 | ensure_setup_type_column | v3.8 | `setup_type` backfilled into ensure (existed in CREATE TABLE from DS-04) |
| SI-01 | ensure_override_acknowledged_column | v3.8 | `pre_entry_override_acknowledged` BOOLEAN (existed in CREATE TABLE; backfilled ensure) |
| DS-07 (SI-02) | ensure_si02_trade_plans_columns | v4.6 | Five SI-02 columns: `signal_id`, `risk_percent_used`, `portfolio_value_at_entry`, `pre_entry_validation_snapshot`, `effective_settings_snapshot` |

**Note on DS-07 naming collision:** `docs/specs/data_model.md` records DS-07 as the `signals_status_check watchlisted` migration (v2.8, 2026-05-18). The `si02_data_schema.md` planning document also labels the SI-02 `trade_plans` columns migration as DS-07. The implementation function `ensure_si02_trade_plans_columns()` does not carry a formal DS identifier in code. For clarity this audit refers to the SI-02 trade_plans column set as DS-07(SI-02). The `data_model.md` should be updated to record these columns as DS-08 at the next spec debt clearance.

---

## 3. Complete Field Inventory

All fields listed in creation order. Post-creation migrations noted in the "Added In" column.

### 3.1 Identity and Linkage Fields

| Field | Type | Nullable | Added In | Feature Cross-Reference | Orphaned? | Notes |
|-------|------|----------|----------|------------------------|-----------|-------|
| `id` | UUID | NOT NULL (PK) | DS-04 / v3.1 | PT-01, all features | No | Primary key; auto-generated via `gen_random_uuid()` |
| `portfolio_id` | UUID | NOT NULL | DS-04 / v3.1 | PT-01, all features | No | FK to `portfolios.id`; no explicit FK constraint in DDL (enforced at application layer) |
| `position_id` | UUID | YES | DS-04 / v3.1 | PT-01, Arc 4 PO-01, SI-02 | No | FK to `positions.id`; nullable — plans may exist before entry; used in plan-vs-reality join |
| `signal_id` | UUID | YES | DS-07(SI-02) / v4.6 | SI-02 (entry timing drift metric) | No | FK to `signals.id` ON DELETE SET NULL; P1 index `idx_trade_plans_signal`; enables entry timing drift analysis |

### 3.2 Classification and Metadata Fields

| Field | Type | Nullable | Added In | Feature Cross-Reference | Orphaned? | Notes |
|-------|------|----------|----------|------------------------|-----------|-------|
| `ticker` | VARCHAR(20) | NOT NULL | DS-04 / v3.1 | PT-01, PT-02, PT-03, all features | No | Instrument identifier; used for plan lookup and display |
| `market` | VARCHAR(10) | NOT NULL | DS-04 / v3.1 | PT-01, PT-03 | No | `CHECK (market IN ('US', 'UK'))`; drives currency context |
| `status` | VARCHAR(20) | NOT NULL | DS-04 / v3.1 | PT-01, Arc 4 PO-01, BLG-FEAT-21 | No | `DEFAULT 'draft'`; `CHECK (status IN ('draft', 'active', 'closed'))`; note: `'abandoned'` is a valid status enforced at the API layer (router validation) but **not** included in the DB CHECK constraint — this is a latent schema gap (see §5) |
| `created_at` | TIMESTAMPTZ | NOT NULL | DS-04 / v3.1 | PT-01, SI-02 (drift time-ordering) | No | `DEFAULT NOW()` |
| `updated_at` | TIMESTAMPTZ | NOT NULL | DS-04 / v3.1 | PT-01 | No | `DEFAULT NOW()`; application must update on every write |
| `setup_type` | VARCHAR(50) | YES | DS-04 / v3.1 (ensure v3.8) | PT-01, PT-02 (signal_type display in Research View), SI-02 (setup adherence) | No | 6 canonical values defined in v3.8 frontend (BLG-FEAT-23); feeds Research View signal_type display (v4.1); surface in drift analysis for setup adherence metric |

### 3.3 Pre-Trade Reasoning Fields (Arc 2 — PT-01)

| Field | Type | Nullable | Added In | Feature Cross-Reference | Orphaned? | Notes |
|-------|------|----------|----------|------------------------|-----------|-------|
| `setup_thesis` | TEXT | YES | DS-04 / v3.1 | PT-01, Arc 4 PO-01 | No | User-authored thesis; AI Thesis Generation (POST /trade-plans/{id}/generate-thesis, v4.0) writes to this field |
| `entry_rationale` | TEXT | YES | DS-04 / v3.1 | PT-01, PT-02, Arc 4 PO-01 | No | Pre-populated from SignalContextPanel (v3.7) when plan is created from a watchlisted signal |
| `regime_context_at_entry` | TEXT | YES | DS-04 / v3.1 | PT-01, SI-02 (sizing adherence — regime context at entry) | No | Originally VARCHAR(50), widened to TEXT via `ensure_regime_context_text_column()` to accommodate AI-generated regime summaries; used in SI-02 as drift context field |
| `r_target` | NUMERIC(8,2) | YES | DS-04 / v3.1 | PT-01, Arc 4 PO-01 | No | Planned R multiple; compared against actual outcome in plan-vs-reality analysis |
| `early_exit_conditions` | TEXT | YES | DS-04 / v3.1 | PT-01, Arc 4 PO-01 | No | User-defined exit criteria; compared against actual exit rationale in plan-vs-reality |
| `confirmation_criteria` | TEXT | YES | DS-04 / v3.1 | PT-01, PT-02 | No | Pre-populated from SignalContextPanel (v3.7) when plan is created from a watchlisted signal |

### 3.4 Checklist Fields (Arc 2 — PT-05)

| Field | Type | Nullable | Added In | Feature Cross-Reference | Orphaned? | Notes |
|-------|------|----------|----------|------------------------|-----------|-------|
| `checklist_completed` | BOOLEAN | NOT NULL | DS-04 / v3.1 | PT-05, SI-02 (checklist adherence — historical plans) | No | `DEFAULT FALSE`; set TRUE when all checklist items are checked; pre-migration plans with NULL excluded from checklist drift analysis |
| `checklist_items` | JSONB | NOT NULL | DS-04 / v3.1 | PT-05 | No | `DEFAULT '[]'::JSONB`; stores structured checklist item state; format: array of `{id, label, checked}` objects |

### 3.5 Pre-Entry Validation Fields (Arc 5 — SI-01)

| Field | Type | Nullable | Added In | Feature Cross-Reference | Orphaned? | Notes |
|-------|------|----------|----------|------------------------|-----------|-------|
| `pre_entry_override_acknowledged` | BOOLEAN | YES | DS-04 / v3.1 (ensure v3.8) | SI-01 (Pre-Entry Advisory Panel) | No | Set TRUE when user acknowledges and overrides a pre-entry advisory warning; written to `red_flag_events` when TRUE; feeds SI-02 override rate metric indirectly via `pre_entry_validation_log` |

### 3.6 Arc 4 Plan vs Reality Fields (PO-01)

| Field | Type | Nullable | Added In | Feature Cross-Reference | Orphaned? | Notes |
|-------|------|----------|----------|------------------------|-----------|-------|
| `planned_stop_price` | NUMERIC(20,6) | YES | v3.5 / PO-01 (ensure_plan_vs_reality_columns) | Arc 4 PO-01 (Plan vs Reality), SI-02 (sizing adherence cross-reference) | No | Snapshot of intended stop loss at plan creation; compared against `positions.initial_stop` in plan-vs-reality service; high precision (6dp) to support UK penny stocks |

### 3.7 Abandonment Fields (BLG-FEAT-21)

| Field | Type | Nullable | Added In | Feature Cross-Reference | Orphaned? | Notes |
|-------|------|----------|----------|------------------------|-----------|-------|
| `abandonment_reason` | VARCHAR(500) | YES | DS-06 / v3.3 (BLG-FEAT-21) | Trade plan lifecycle management | Partially | Required at API layer when `status = 'abandoned'`; the abandonment workflow frontend (status badges etc.) was delivered in v3.3; however, no Arc 4 or Arc 5 feature currently reads `abandonment_reason` text for analysis. The column is correct to keep — it supports future PO-03 (Behavioural Error Taxonomy) pattern analysis on abandoned plans. See §4. |

### 3.8 SI-02 Behavioural Drift Detection Capture Fields (DS-07 / v4.6)

| Field | Type | Nullable | Added In | Feature Cross-Reference | Orphaned? | Notes |
|-------|------|----------|----------|------------------------|-----------|-------|
| `signal_id` | UUID | YES | DS-07(SI-02) / v4.6 | SI-02 entry timing drift metric (`days_signal_to_entry`) | No | See §3.1 — listed here for completeness; FK to `signals.id` |
| `risk_percent_used` | NUMERIC(4,2) | YES | DS-07(SI-02) / v4.6 | SI-02 sizing adherence metric (`risk_per_trade_drift`) | No | e.g. 1.50 for 1.5%; captured from sizing calculator at plan create/update; compared against `settings.default_risk_percent` at plan creation time |
| `portfolio_value_at_entry` | NUMERIC(12,2) | YES | DS-07(SI-02) / v4.6 | SI-02 sizing adherence metric (denominator for risk% calculation) | No | GBP value from `portfolio_history.total_value` at plan creation time; enables retrospective sizing calculation where `risk_percent_used` is not populated |
| `pre_entry_validation_snapshot` | JSONB | YES | DS-07(SI-02) / v4.6 | SI-02 pre-entry gate adherence metric (`override_rate`) | No | Full `GET /portfolio/pre-entry-validation` response at plan creation time; schema: `{overall, checks: {regime_gate, sector_concentration, earnings_proximity, cash_constraint, sizing_validity}, captured_at}` |
| `effective_settings_snapshot` | JSONB | YES | DS-07(SI-02) / v4.6 | SI-02 sizing adherence (settings context at entry) | No | Strategy parameters active at plan creation: `{default_risk_percent, atr_multiplier_initial, atr_multiplier_trailing, min_hold_days, captured_at}`; replaces fragile "use current settings as proxy" approach |

---

## 4. Orphaned Fields Assessment

An orphaned field is one present in the schema but not surfaced in any current live feature (API endpoint, frontend component, or analytics calculation).

| Field | Assessment | Recommendation |
|-------|------------|----------------|
| `abandonment_reason` | Partially orphaned — written at abandonment time, displayed in status badge UI, but not consumed by any analytics feature | **Keep.** Retain as foundation for PO-03 (Behavioural Error Taxonomy, v4.0+ roadmap). The text content will feed pattern classification of abandoned-plan behaviour. No removal recommended. |
| `checklist_items` | Active — read by PT-05 checklist component on the Trade Plan form | **Keep.** Not orphaned. |

**Finding:** No fields are recommended for removal. The `abandonment_reason` field is the only one with no current analytics consumer, but its future value in PO-03 is clear and its storage cost is negligible (VARCHAR(500), sparse population).

---

## 5. Missing Fields Assessment

Fields needed by roadmap features that are not yet present in `trade_plans`.

### 5.1 Status Constraint Gap — `abandoned` not in DB CHECK

**Severity:** Low (P3)
**Description:** The `status` column CHECK constraint reads `CHECK (status IN ('draft', 'active', 'closed'))`. The value `'abandoned'` is enforced at the API router layer (`backend/routers/trade_plans.py`) but is not in the DB constraint. A direct SQL INSERT or UPDATE bypassing the router could write an unconstrained status value.
**Recommendation:** Add `'abandoned'` to the CHECK constraint in the next schema migration opportunity. This is a data integrity hardening, not a breaking change.
**Recommended sprint:** Next spec debt clearance cycle (backlog item to be filed).

### 5.2 PT-04 Setup Quality Score — No Schema Field Required Yet

**Description:** PT-04 (Setup Quality Score) computes a deterministic score (0–100) from historical trade data. PT-04 is formally parked (gate not met: < 20 closed trades as of v4.6; 5 consecutive cycle deferrals; PO decision 2026-05-19 to park). When PT-04 ships, it will likely surface the score as a computed/derived field on the API response rather than a stored column (score is recalculated from `trade_history` on demand). No schema addition to `trade_plans` is anticipated for PT-04.
**Recommendation:** Revisit at PT-04 sprint planning. If the score is to be cached on `trade_plans` for performance, add `setup_quality_score NUMERIC(5,2)` at that time.
**Recommended sprint:** PT-04 sprint planning (gate-dependent).

### 5.3 PO-03 Behavioural Error Taxonomy — No Schema Field Required Yet

**Description:** PO-03 (v4.0+ roadmap) will auto-classify plan-vs-reality deviations and journal entries by error type. If classifications are to be stored on `trade_plans`, a `behavioural_error_tags JSONB` column or similar would be needed. This is not yet specced.
**Recommendation:** Defer to PO-03 sprint planning. No action in v4.6.

### 5.4 SI-02 Gap 5 Deferred — Consecutive Loss State

**Description:** SI-02 Gap 5 (consecutive loss state at entry) was explicitly deferred in `docs/specs/data_model/si02_data_schema.md §3` and §4.2. The metric is derivable at query time from `trade_history`. No schema field was added.
**Recommendation:** Monitor query performance. If trade volume exceeds 500 closed trades, add `trade_stats_at_entry JSONB` to `trade_plans` (backlog item BLG-BE-18 already exists).
**Recommended sprint:** Gate-triggered — file sprint story when BLG-BE-18 is triaged.

### 5.5 DS Naming Collision — SI-02 Columns Not Recorded in data_model.md

**Description:** The five SI-02 columns added in v4.6 are documented in `docs/specs/data_model/si02_data_schema.md` but are not yet appended to `docs/specs/data_model.md` as a formal DS-08 migration entry. The existing DS-07 entry in `data_model.md` covers `signals_status_check watchlisted` (v3.7). The SI-02 additions should be formalised as DS-08.
**Recommendation:** Append a DS-08 migration block to `docs/specs/data_model.md` in the next spec debt clearance sprint, recording the five SI-02 columns and `idx_trade_plans_signal` index.
**Recommended sprint:** Next spec debt clearance cycle.

---

## 6. Index Inventory

Indexes active on `trade_plans` as of v4.6:

| Index Name | Columns | Type | Added In | Purpose |
|------------|---------|------|----------|---------|
| `idx_trade_plans_portfolio` | `portfolio_id` | B-tree | DS-04 / v3.1 | Primary lookup path for per-portfolio plan listing |
| `idx_trade_plans_position` | `position_id` WHERE NOT NULL | B-tree (partial) | DS-04 / v3.1 | Plan-to-position join; partial index excludes unlinked plans |
| `idx_trade_plans_status` | `status` | B-tree | DS-04 / v3.1 | Filter by plan status (draft/active/closed) |
| `idx_trade_plans_signal` | `signal_id` WHERE NOT NULL | B-tree (partial) | DS-07(SI-02) / v4.6 | Entry timing drift join: `signals → trade_plans`; partial index excludes plans not created from signals |

---

## 7. Feature Cross-Reference Summary

| Feature | Description | Fields Used | Status |
|---------|-------------|-------------|--------|
| PT-01 (Trade Plan Object) | Core domain object — data model, backend CRUD, frontend | All base fields (§3.1–§3.4) | Shipped v3.1 |
| PT-02 (Pre-Trade Research View) | Unified research surface per ticker | `ticker`, `market`, `setup_type` (signal_type display) | Shipped v3.2 |
| PT-03 (Prospective Heat at Entry) | Prospective heat integrated into research view | `ticker`, `market` (indirect — heat is computed, not stored on plan) | Shipped v3.2 |
| PT-04 (Setup Quality Score) | Deterministic score from own trade history | No `trade_plans` fields needed at current design | Parked (gate not met) |
| PT-05 (Pre-Trade Entry Checklist) | Checklist embedded in trade plan flow | `checklist_completed`, `checklist_items` | Shipped v3.2 |
| Arc 4 PO-01 (Plan vs Reality) | Comparison of planned intent vs actual outcome | `position_id`, `r_target`, `planned_stop_price`, `early_exit_conditions`, `setup_thesis`, `entry_rationale` | Shipped v3.5–v3.6 |
| Arc 5 SI-01 (Pre-Entry Validation) | Advisory panel + override acknowledgement | `pre_entry_override_acknowledged` | Shipped v3.8 |
| Arc 5 SI-02 (Behavioural Drift Detection) | Rolling drift analysis across 4 metrics | `signal_id`, `risk_percent_used`, `portfolio_value_at_entry`, `pre_entry_validation_snapshot`, `effective_settings_snapshot`, `regime_context_at_entry`, `checklist_completed` | DS-07 shipped v4.6; drift service and frontend in progress |
| BLG-FEAT-21 (Plan Abandonment) | Trade plan abandonment workflow | `status` (abandoned value), `abandonment_reason` | Shipped v3.3 |
| PO-03 (Behavioural Error Taxonomy) | Auto-classify deviations by error type | `abandonment_reason` (future consumer), `entry_rationale` | Roadmap — not started |
| SI-05 (Weekly Strategy Integrity Digest) | Weekly review combining SI-02 + SI-03 + score trend | Indirect via SI-02 metrics | Roadmap — depends on SI-02 delivery |

---

## 8. Audit Summary

**Total fields in `trade_plans` as of v4.6:** 25 (including all 5 SI-02 DS-07 additions)

**Orphaned fields requiring removal:** 0

**Fields with partial orphan status:** 1 (`abandonment_reason` — no analytics consumer; keep for PO-03 future use)

**Missing fields blocking current roadmap features:** 0

**Schema gaps identified for future remediation:**
- P3: `status` CHECK constraint missing `'abandoned'` value
- Process: DS-08 formal migration entry needed in `data_model.md` for SI-02 columns
- Deferred (gate-triggered): PT-04 `setup_quality_score` if caching decision is made at sprint planning
- Deferred (volume-triggered): `trade_stats_at_entry` JSONB if BLG-BE-18 is triaged

**Overall assessment:** The `trade_plans` schema is in a healthy state post-DS-07. All 25 fields are accounted for and cross-referenced. The five SI-02 additions are correctly implemented as nullable columns with no backfill requirement. No orphaned fields warrant removal. The two process gaps (status CHECK constraint and DS-08 data_model.md entry) are P3 housekeeping items with no functional impact.

---

## Sign-Off

| Attribute | Value |
|-----------|-------|
| Signed off by | Data Model & Domain Schema Owner |
| Date | 2026-05-31 |
| Comments | All six acceptance criteria are met. AC-01: audit note produced covering post-DS-07 state. AC-02: all 25 `trade_plans` fields enumerated from `backend/database.py` as authoritative source of truth. AC-03: each field cross-referenced to PT-01 through PT-05, Arc 4 PO-01, SI-01, SI-02, BLG-FEAT-21, and Arc 5 roadmap features (§7). AC-04: no fields recommended for removal; `abandonment_reason` flagged as partially orphaned but retained for PO-03 future use (§4). AC-05: four missing-field scenarios identified with sprint recommendations — none block any current in-flight feature (§5). AC-06: this sign-off block constitutes owner approval. The schema is sound for the SI-02 sprint delivery and subsequent Arc 5 analytics work. |
