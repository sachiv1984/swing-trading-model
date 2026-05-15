**Owner:** Head of UX & Design + Product Owner
**Class:** Planning Document (Class 4)
**Status:** Draft — Awaiting Product Owner + Head of UX & Design Sign-off
**Version:** 0.1
**Last Updated:** 2026-05-15
**Story:** ST-04 (EPIC-02, v3.5) — BLG-GOV-21
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Arc 4 Data Requirements Capture

> **This document is not a feature specification or implementation commitment. It is a reference input for Arc 4 sprint planning.**

---

## 1. Purpose

This document captures data points that Arc 4 features (PO-01 through PO-05) will require but that are not currently stored in the system. Each entry specifies why the data cannot be derived from existing records.

Arc 4 focus: AI integration, Plan vs Reality analysis, and trade quality measurement.

---

## 2. Existing Relevant Data (Reference)

The following Arc 4-relevant data is ALREADY stored and does NOT need to be added:

| Data | Location |
|------|----------|
| Trade entry price, stop, size | `positions.entry_price`, `stop_price`, `position_size` |
| Exit price, date, reason | `trade_history.exit_price`, `exit_date`, `exit_reason` |
| Calculated R-multiple | `trade_history.r_multiple` |
| Trade plan: thesis, rationale, regime, checklist | `trade_plans` table (linked via `position_id`) |
| Post-trade reflection: what worked, discipline | `trade_reflections` table (linked via `trade_id`) |
| Signal ATR, entry/stop suggestion | `signals` table (linked via `position_id`) |
| Market regime label at plan creation | `trade_plans.regime_context_at_entry` |

---

## 3. Missing Data Requirements

### 3.1 Plan vs Reality — Structured Comparison (PO-01)

**Purpose:** PO-01 produces a structured comparison of the trade plan's predictions against actual trade outcomes. The comparison needs numeric planned values, not just free-text fields.

| Field | Type | Source | Why not derivable |
|-------|------|--------|------------------|
| `planned_stop_price` | DECIMAL | User input (numeric, at plan creation) | `trade_plans.early_exit_conditions` is free text; no numeric planned stop is stored |
| `planned_entry_price` | DECIMAL | Signal `entry_price` or user input | Signal entry price is stored in `signals` but not copied/snapshotted to `trade_plans`; linkage may break if signal is updated |
| `plan_vs_reality` | JSONB | Calculated by PO-01 service at trade close | New field on `trade_history`; structured comparison record — see §3.2 |

**Note on `planned_stop_price`:** This is the single most critical missing field. The current trade plan stores early exit conditions as free text (e.g. "Close below 50-day MA"). For Plan vs Reality comparison, a numeric planned stop at entry time is required. This field should be added to `trade_plans` alongside `early_exit_conditions`.

---

### 3.2 Plan vs Reality — Calculated Output Structure (PO-01)

**Purpose:** The PO-01 calculation service produces a structured comparison record attached to each closed trade that had a trade plan.

| Calculated field | Type | Derivation | Requires new data? |
|-----------------|------|-----------|-------------------|
| `entry_delta_pct` | DECIMAL | `(actual_entry - planned_entry) / planned_entry` | Requires `planned_entry_price` (§3.1) |
| `stop_discipline` | STRING | Comparison of actual initial stop vs planned stop | Requires `planned_stop_price` (§3.1) |
| `r_target_vs_actual` | DECIMAL | `actual_r_multiple - planned_r_target` | Both exist; derivable from existing data |
| `plan_linked` | BOOLEAN | Whether trade had a linked trade plan | Derivable |
| `plan_adherence_flag` | STRING | System-flagged: "on_plan" / "entry_deviation" / "stop_deviation" / "early_exit" | Derivable once §3.1 fields exist |

---

### 3.3 Pre-Entry State Snapshot (PO-02/PO-03)

**Purpose:** PO-02 and later arcs may use pre-entry market state for AI context. Currently, state at entry is partially derivable from signals and trade_plans, but a unified snapshot is not stored.

| Field | Type | Source | Why not derivable reliably |
|-------|------|--------|---------------------------|
| `atr_at_entry` | DECIMAL | From linked signal | Signal ATR is stored but only for positions with a linked signal; paper positions or manual entries have no signal ATR |
| `screener_score_at_entry` | INTEGER | From linked signal/screener | Screener cache is overwritten; historical score is not retained |
| `regime_at_open` | STRING | From `trade_plans.regime_context_at_entry` | Already stored on trade plan but NOT on `positions` or `trade_history`; requires join through trade_plans |

**Recommendation:** For PO-02 context, `regime_at_open` should be denormalised from `trade_plans` onto `trade_history` at close time via the PO-01 service. `screener_score_at_entry` is not currently retainable without schema change; defer to Arc 4 decision.

---

### 3.4 AI Context Inputs (PO-03 / AI Journal)

**Purpose:** AI journal entry generation will benefit from structured context, not just free-text reflections.

| Field | Type | Source | Why not derivable |
|-------|------|--------|------------------|
| `confidence_at_entry` | INTEGER (1–5) | User input at position open | Not currently captured; entirely new capture point |
| `setup_quality_score` | INTEGER | Calculated: count of pre-entry checklist items checked / total | Derivable from `trade_plans.checklist_items` JSONB — no new storage needed |
| `deviation_note` | TEXT | User input: why did execution deviate from plan? | `trade_reflections.trade_rationale` covers some of this but is general; a specific deviation capture point is missing |

---

### 3.5 Qualitative Annotations (PO-04/PO-05)

**Purpose:** Future arc features (trade quality scoring, pattern detection) will benefit from explicit labels.

| Field | Type | Source | Why not derivable |
|-------|------|--------|------------------|
| `thesis_confirmed` | BOOLEAN | User annotation post-trade | Cannot be inferred from price action alone; requires human judgement |
| `exit_quality` | STRING | User annotation: "too early" / "as planned" / "stopped out" / "target hit" | `exit_reason` captures reason but not quality assessment |

---

## 4. Priority Order for Arc 4 Planning

| Priority | Field(s) | Arc feature |
|----------|----------|-------------|
| P1 — Required for PO-01 | `planned_stop_price` on `trade_plans`; `plan_vs_reality` JSONB on `trade_history` | PO-01 Plan vs Reality service |
| P2 — Useful for PO-02/AI Journal | `confidence_at_entry`; `deviation_note`; `regime_at_open` denorm | AI context / journal quality |
| P3 — Future arcs | `screener_score_at_entry`; `thesis_confirmed`; `exit_quality` | PO-04/PO-05 pattern detection |

---

## 5. Decisions Deferred to Product Owner

The following require a product decision before implementation:

1. **`planned_stop_price` capture point:** Should this be a new numeric field on `trade_plans` (added at plan creation), or captured at position-open time (added to the position-open workflow)?
2. **`confidence_at_entry` range:** 1–5 scale or free text? Mandatory or optional?
3. **`screener_score_at_entry` retention:** Requires schema change and historical fill. Worthwhile for v3.5 or defer to Arc 4?
4. **`deviation_note` placement:** New field on `trade_reflections`, or as part of the PO-01 Plan vs Reality record?

---

## 6. Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| Product Owner | — | — | Pending |
| Head of UX & Design | — | — | Pending |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-05-15 | Initial draft — ST-04 (EPIC-02, v3.5). BLG-GOV-21 requirement. Engine-authored for Product Owner + Head of UX & Design review. |
