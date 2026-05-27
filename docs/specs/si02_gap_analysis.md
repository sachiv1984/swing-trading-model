**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-26__release-v4.1 (ST-12, BLG-SPEC-39)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 Data Model Gap Analysis

## 1. Purpose

This document analyses the current database schema against SI-02 (Behavioural Drift Detection) requirements and identifies fields that are missing or require augmentation before SI-02 sprint planning can proceed.

SI-02 asks: "Are your actual entries drifting from your stated setup criteria? Are you entering earlier in the signal cycle than your rules permit? Are you sizing up in losing streaks?" (Source: `claude/roadmap/current_roadmap.md`, SI-02 initiative description)

---

## 2. Current Schema Inventory (SI-02 Relevant Tables)

### 2.1 signals

| Field | Available | Notes |
|-------|-----------|-------|
| signal_date | ✅ | Anchor date for timing drift analysis |
| rank | ✅ | Signal quality at time of generation |
| momentum_percent | ✅ | Signal strength |
| ticker | ✅ | Matches to positions/trade_plans |
| status | ✅ | `new`, `entered`, `dismissed`, `expired`, `watchlisted` |
| position_id | ✅ | FK to positions (set when `status = 'entered'`) |

**Limitation:** `signals` links to `positions` (via `position_id`) but NOT to `trade_plans`. The indirect path is: signal → position → trade_plan (via `trade_plans.position_id`). This path is available but creates an N:1 ambiguity when multiple plans exist for the same position.

### 2.2 trade_plans

| Field | Available | Notes |
|-------|-----------|-------|
| position_id | ✅ | FK to positions (null until entry; set at entry) |
| ticker | ✅ | Allows pre-entry plan lookup without position FK |
| created_at | ✅ | Plan creation timestamp; proxy for when analysis was done relative to signal |
| checklist_completed | ✅ | Boolean: was the entry checklist signed off? |
| checklist_items | ✅ | JSONB array: individual checklist item state |
| regime_context_at_entry | ✅ | Regime captured at plan creation time |
| setup_thesis | ✅ | Free-text; not machine-comparable to rules |
| confirmation_criteria | ✅ | Free-text; not machine-comparable to rules |
| entry_rationale | ✅ | Free-text; not machine-comparable to rules |

### 2.3 positions

| Field | Available | Notes |
|-------|-----------|-------|
| entry_date | ✅ | Actual entry date |
| entry_price | ✅ | Actual entry price |
| shares | ✅ | Actual shares entered |
| total_cost | ✅ | Actual total cost in GBP |
| initial_stop | ✅ | Stop at entry (used to derive risk amount) |
| atr | ✅ | ATR at entry (key to verify sizing adherence) |

### 2.4 trade_history

| Field | Available | Notes |
|-------|-----------|-------|
| pnl | ✅ | Realised P&L per closed trade |
| entry_date / exit_date | ✅ | Trade duration history |
| position_id | ✅ | Links back to plan |

### 2.5 settings (portfolio-level)

| Field | Available | Notes |
|-------|-----------|-------|
| default_risk_percent | ✅ | Default risk % at time of query — NOT stored per-entry |
| atr_multiplier_initial | ✅ | Stop sizing rule — NOT stored per-entry |
| min_hold_days | ✅ | Grace period rule |

**Critical limitation:** Settings values are live; they are not snapshotted at entry time. If a user changes `default_risk_percent` from 1% to 1.5% between trades, historical analysis cannot determine what the setting was when each trade was entered. This prevents retrospective sizing adherence analysis.

---

## 3. Gap Analysis

### Gap 1 — Signal-to-Plan Direct Linkage (High Priority)

**Required for:** Entry timing drift analysis (did user enter earlier than the signal warrants?)

**Current state:** `trade_plans` has no `signal_id` field. The link `signal → position → trade_plan` is indirect and unreliable (a position may have been opened without a corresponding signal, or the plan may have been created before the position was linked).

**Proposed addition:**
```sql
ALTER TABLE trade_plans ADD COLUMN signal_id UUID REFERENCES signals(id) ON DELETE SET NULL;
CREATE INDEX idx_trade_plans_signal ON trade_plans(signal_id) WHERE signal_id IS NOT NULL;
```

| Attribute | Value |
|-----------|-------|
| Data type | UUID (nullable FK) |
| Source | Captured at plan creation when user selects a signal as the prompt for the plan |
| Migration complexity | Low — new nullable column; no backfill required for historical plans |
| Data density after addition | New plans only; historical drift analysis unavailable for pre-migration plans |

### Gap 2 — Risk % Used Per Entry (High Priority)

**Required for:** Sizing adherence drift analysis (did user apply consistent risk per trade?)

**Current state:** `default_risk_percent` exists in `settings` but is not captured per-trade. The actual risk % used for sizing any given entry cannot be recovered from stored data (only calculable at entry time from `total_cost`, `initial_stop`, `entry_price`, `shares` — all available, but the inverse calculation is noisy due to rounding and GBP/USD conversion).

**Derivation feasibility:** Risk amount = `(entry_price - initial_stop) × shares` in native currency. Divide by portfolio value at entry to get risk %. Portfolio value at entry is NOT stored directly (it must be reconstructed from `portfolio_history` snapshots if available for that date). This reconstruction is possible but fragile.

**Proposed addition:**
```sql
ALTER TABLE trade_plans ADD COLUMN risk_percent_used NUMERIC(4,2);
ALTER TABLE trade_plans ADD COLUMN portfolio_value_at_entry NUMERIC(12,2);
```

| Attribute | Value |
|-----------|-------|
| Data type | NUMERIC(4,2) for risk_pct; NUMERIC(12,2) for portfolio value |
| Source | Captured from sizing calculator result at plan creation / confirmation |
| Migration complexity | Low — new nullable columns; backfill partially possible from portfolio_history |
| Data density after addition | New plans only; sizing adherence analysis requires >= 10 post-migration trades for meaningful detection |

### Gap 3 — Pre-Entry Validation Snapshot (Medium Priority)

**Required for:** Gate adherence drift analysis (did user enter when pre-entry checks were showing warnings?)

**Current state:** `GET /portfolio/pre-entry-validation` computes checks on demand; no snapshot is captured at entry time. There is no record of what the validation state was when the trade was entered.

**Proposed addition:**
```sql
ALTER TABLE trade_plans ADD COLUMN pre_entry_validation_snapshot JSONB;
```

| Attribute | Value |
|-----------|-------|
| Data type | JSONB (stores the full validation response at plan creation time) |
| Source | Frontend captures and passes to `POST /trade-plans` when user creates/confirms a plan |
| Migration complexity | Low column addition; requires frontend change to capture and pass the snapshot |
| Data density after addition | New plans only; no backfill |

### Gap 4 — Settings Snapshot Per Entry (Medium Priority)

**Required for:** Rule adherence drift analysis using the settings that were active at time of entry

**Current state:** `settings` is a single live row; historical values are not tracked.

**Options:**
- (a) Add an `effective_settings_snapshot JSONB` to `trade_plans` — captures the relevant strategy parameters at plan creation time (low migration complexity)
- (b) Add a `settings_history` table with a `valid_from` timestamp — enables full retrospective settings reconstruction (higher complexity, higher value for future analytics)

**Recommended path:** Option (a) for SI-02 Sprint 1. Option (b) deferred as a P3 backlog item if data density analysis shows it is needed.

| Attribute | Value |
|-----------|-------|
| Data type | JSONB (captures: atr_multiplier_initial, atr_multiplier_trailing, min_hold_days, default_risk_percent) |
| Source | Backend captures at trade_plan creation time from current settings row |
| Migration complexity | Low — new nullable column; no backfill |

### Gap 5 — Consecutive Loss State at Entry (Low Priority for Sprint 1)

**Required for:** Sizing-up-in-losing-streaks detection

**Current state:** Consecutive loss state at time of entry must be derived by querying `trade_history` for the N most recent trades before the entry date. This query is complex but feasible. No stored field needed for Sprint 1 — compute at query time.

**Assessment:** Derivable from `trade_history.pnl` + `positions.entry_date` join. No schema change required for Sprint 1 SI-02 implementation. If performance is an issue at higher trade volumes, a `trade_stats_at_entry` JSONB column can be added to `trade_plans` as a computed snapshot (backlog item).

---

## 4. Availability Summary

| Drift Metric | Data Available? | Gaps to Resolve |
|-------------|----------------|-----------------|
| Entry timing vs signal date | ⚠️ Indirect | Gap 1 (signal_id) |
| Sizing adherence | ⚠️ Derivable but fragile | Gap 2 (risk_percent_used) |
| Pre-entry gate adherence | ❌ Not captured | Gap 3 (validation snapshot) |
| Rule adherence (settings) | ⚠️ Live only | Gap 4 (settings snapshot) |
| Consecutive loss state | ✅ Derivable | None for Sprint 1 |
| Regime context at entry | ✅ Available | None (field exists) |
| Checklist completion | ✅ Available | None (field exists) |

---

## 5. Data Density Gate Assessment

Per the SI-02 gate criteria in `claude/roadmap/current_roadmap.md`: SI-02 requires PO-01 + PO-03 data foundation.

**Current status (2026-05-27):** PT-04 gate not met — fewer than 20 closed trades in `trade_history`. Drift detection requires a minimum baseline of historical entries for pattern detection to be statistically meaningful.

**Recommended minimum:** 20 closed trades with linked `trade_plans` records for meaningful entry timing analysis; 30+ for sizing adherence trend detection.

**Action:** Defer SI-02 sprint planning until the data density gate is confirmed met. This audit confirms the gate is not yet met as of v4.1.

---

## 6. Schema Change Requirements for SI-02 Sprint

The following migration will be required before SI-02 can be implemented:

```sql
-- DS-07: SI-02 schema additions
BEGIN;

ALTER TABLE trade_plans
  ADD COLUMN signal_id UUID REFERENCES signals(id) ON DELETE SET NULL,
  ADD COLUMN risk_percent_used NUMERIC(4,2),
  ADD COLUMN portfolio_value_at_entry NUMERIC(12,2),
  ADD COLUMN pre_entry_validation_snapshot JSONB,
  ADD COLUMN effective_settings_snapshot JSONB;

CREATE INDEX idx_trade_plans_signal ON trade_plans(signal_id) WHERE signal_id IS NOT NULL;

COMMIT;
```

**Notes:**
- All columns nullable; no backfill required
- Frontend changes required to capture `signal_id` and `pre_entry_validation_snapshot` at plan creation
- Backend changes required to capture `portfolio_value_at_entry`, `risk_percent_used`, and `effective_settings_snapshot` at plan creation/activation

---

## 7. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Data Model & Domain Schema Owner | Pending | — |
| Head of Specs Team | Pending | — |
| Head of Backend Engineering | Pending | — |
