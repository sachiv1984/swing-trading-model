# strategy_version_comparison_contract.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical — Implemented v7.7 EPIC-01 ST-01
**Version:** 0.2.0
**Last Updated:** 2026-07-23
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Cycle:** 2026-06-01__release-v4.8 (ST-07 — BLG-SPEC-43); implemented 2026-07-21__release-v7.7 (ST-01, EPIC-01, BLG-FEAT-75)
**SI Initiative:** SI-04 — Strategy Version Performance Comparison
**§13 Binding Conditions:** 6 conditions cleared v4.7 (Strategy Rules & System Intent Owner sign-off)

---

## Overview

This document defines the `GET /analytics/strategy-version-comparison` endpoint for SI-04.

**Purpose:** Allow the system to compare performance metrics across different versions of the trading strategy configuration, surfacing which version produced better trade outcomes (win rate, R-multiple, trade count).

**Motivation:** As the strategy evolves across cycles, there is no current mechanism to quantify the performance impact of strategy changes. This endpoint provides a data-driven view of strategy version history and their associated trade performance.

**Dependency (resolved v7.7 ST-01 — see Implementation Notes 1 below):** rather than adding a `strategy_version` column to `trade_history` (confirmed absent from the schema at implementation time, contradicting a stale backlog claim that version-tagged trade history "already exists"), trades are attributed to a version by `entry_date` falling within that version's active date window. Each version's window is derived from `claude/strategy/strategy_rules.md`'s own Change Log table (`backend/strategy_version_registry.py`) — no schema migration was required.

**Contract status:** Implemented v7.7 (ST-01, EPIC-01, BLG-FEAT-75). Originally pre-authored to lock the interface design before the sprint in which SI-04 is executed, following the pattern established by SI-03 (arc5_compliance_analytics.md) and SI-01 (behavioural_drift_contract.md).

---

## Endpoints

- [GET /analytics/strategy-version-comparison](#get-analyticsstrategy-version-comparison)

---

## GET /analytics/strategy-version-comparison

**Purpose:** Return a side-by-side performance comparison of two strategy versions.

**Version:** 0.1.0 (pre-sprint draft)

### Request

```
GET /analytics/strategy-version-comparison
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `version_from` | string | Yes | The baseline strategy version label (e.g., `"v1.0"`, `"2026-01-01"`). Must match an existing version tag in the strategy version registry. |
| `version_to` | string | Yes | The comparison strategy version label. Must be chronologically after `version_from`. |
| `date_range` | string | No | ISO 8601 date range filter applied to trade history in the format `YYYY-MM-DD/YYYY-MM-DD`. If omitted, all trades tagged to each version are included. |

### Response Schema

```json
{
  "version_from": "string",
  "version_to": "string",
  "date_range": "YYYY-MM-DD/YYYY-MM-DD | null",
  "version_from_metrics": {
    "trade_count": "integer",
    "win_rate": "number (0.0–1.0)",
    "avg_R": "number",
    "performance_delta": null,
    "compliance_rate": "number (0.0–1.0) | null"
  },
  "version_to_metrics": {
    "trade_count": "integer",
    "win_rate": "number (0.0–1.0)",
    "avg_R": "number",
    "performance_delta": "number",
    "compliance_rate": "number (0.0–1.0) | null"
  },
  "comparison_summary": {
    "win_rate_delta": "number (version_to.win_rate - version_from.win_rate)",
    "avg_R_delta": "number (version_to.avg_R - version_from.avg_R)",
    "trade_count_delta": "integer",
    "assessment": "string (Improved | Degraded | Insufficient data)"
  }
}
```

**Field definitions:**

| Field | Description |
|-------|-------------|
| `trade_count` | Number of closed trades tagged to this strategy version |
| `win_rate` | Proportion of trades that closed positive (R > 0) |
| `avg_R` | Average R-multiple across all closed trades for this version |
| `performance_delta` | Change in avg_R vs the `version_from` baseline; null for version_from itself |
| `compliance_rate` | Arc 5 compliance composite score (`metrics_definitions.md` "Arc 5 Compliance Composite Score"), computed over the version's date window rather than the endpoint's usual rolling 7/30-day window. Sourcing decision: Strategy Rules & System Intent Owner, 2026-07-23 (v7.7 ST-01) — see Implementation Notes 4. Null only if the underlying compliance tables are unavailable (schema not yet migrated). |
| `comparison_summary.assessment` | "Insufficient data" when either version has < 10 trades; else "Improved" when `avg_R_delta >= 0`, else "Degraded" |

### Error Cases

| HTTP Status | Code | Description |
|-------------|------|-------------|
| 404 | `version_not_found` | One or both `version_from`/`version_to` labels not found in strategy version registry |
| 422 | `insufficient_data` | A version has fewer than the minimum required trades (< 10) to compute meaningful metrics; response includes `min_trades_required: 10` |
| 422 | `invalid_date_range` | `date_range` format invalid or `version_to` date is before `version_from` date |
| 400 | `version_order_error` | `version_to` is chronologically earlier than or equal to `version_from` |

**404 response shape:**
```json
{
  "status": "error",
  "code": "version_not_found",
  "message": "Strategy version 'v1.0' not found in version registry",
  "missing_version": "string"
}
```

**422 (insufficient_data) response shape:**
```json
{
  "status": "error",
  "code": "insufficient_data",
  "message": "Version 'v1.0' has only 4 trades — minimum 10 required for reliable comparison",
  "version": "string",
  "trade_count": "integer",
  "min_trades_required": 10
}
```

---

## Implementation Notes

1. **Strategy version attribution (resolved v7.7 ST-01 — no `strategy_version` column added):** trades are attributed to a version by `entry_date` falling within that version's active date window, not a per-trade column. Each version's window is `[effective_date, next_version_effective_date)` per `claude/strategy/strategy_rules.md`'s own Change Log table. Two versions sharing an effective date (1.1 and 1.2, both 2026-02-18) correctly yield a zero-width window for the earlier one.

2. **Version registry:** implemented as `backend/strategy_version_registry.py` — a hardcoded list mirroring `strategy_rules.md`'s Change Log (version label + effective date), not a database table or new schema. Living-reference maintenance obligation: update this file in the same commit as any new Change Log row in `strategy_rules.md`.

3. **Comparison direction:** `performance_delta` on `version_to_metrics` represents `version_to.avg_R - version_from.avg_R`. Positive = improvement. `avg_R` uses the canonical per-trade R-multiple formula (`metrics_definitions.md` v1.7.0) via `positions.initial_stop`; trades without a determinable stop are excluded from `avg_R` but still counted in `trade_count`/`win_rate`.

4. **`compliance_rate` sourcing (Strategy Rules & System Intent Owner decision, 2026-07-23, v7.7 ST-01):** sources from the Arc 5 compliance composite score (`GET /analytics/arc5-compliance`'s four underlying metrics — `override_rate`, `events_per_week`, `trade_plan_adherence_rate`, `top_rule_breach` severity — combined via the existing composite formula), generalised from its native rolling 7/30-day window to an arbitrary `[start_date, end_date)` range matching the version's attribution window. `journal_completion_rate` (`GET /analytics/compliance-metrics`) was considered and rejected: it measures whether a trade has a journal note, not rule-following discipline, and reusing the name `compliance_rate` for a different concept than the Arc 5 composite already carries elsewhere in the product would be intent drift (role charter §6, "same field must mean the same thing everywhere"). Implemented in `backend/routers/analytics.py::_compute_arc5_composite_for_range`.

5. **Minimum trade count:** 10 trades per version is the minimum for statistically meaningful comparison. Below this threshold: return 422 `insufficient_data` rather than unreliable metrics.

---

## §13 Binding Conditions (SI-04)

Six binding conditions cleared v4.7 by Strategy Rules & System Intent Owner sign-off. Implementation proceeds only after all conditions are confirmed met at sprint planning gate:

1. Strategy version tagging infrastructure must be implemented before this endpoint ships
2. Version comparison must be read-only (no strategy modification capability)
3. Comparison scope limited to closed trades only
4. No real-time position modification based on comparison output
5. Performance metrics are advisory — not fed back into strategy execution logic
6. Version registry access is read-only from this endpoint

---

## Known Deviations

None. Implementation matches this contract (v0.2.0) at v7.7 ST-01.

---

## Contract Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.2.0 | 2026-07-23 | Sprint Execution Engine | Implemented (v7.7, ST-01, EPIC-01, BLG-FEAT-75). Added `compliance_rate` field to `version_from_metrics`/`version_to_metrics` (Strategy Rules & System Intent Owner sourcing decision — Arc 5 composite score, generalised to an arbitrary date range). Resolved the strategy-version-attribution dependency via date-range windows sourced from `strategy_rules.md`'s Change Log (`backend/strategy_version_registry.py`), not a new `strategy_version` column. `comparison_summary.assessment` rule made explicit (Improved when `avg_R_delta >= 0`, else Degraded). Status: Draft — Pre-Sprint → Canonical. |
| 0.1.0 | 2026-06-01 | Sprint Execution Engine | Initial pre-sprint contract draft. Response schema, query parameters, error cases, §13 binding conditions. SI-04 strategy version comparison endpoint. |
