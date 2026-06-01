# strategy_version_comparison_contract.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Draft — Pre-Sprint (SI-04 Phase 1 gate cleared v4.7; implementation in future sprint)
**Version:** 0.1.0
**Last Updated:** 2026-06-01
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Cycle:** 2026-06-01__release-v4.8 (ST-07 — BLG-SPEC-43)
**SI Initiative:** SI-04 — Strategy Version Performance Comparison
**§13 Binding Conditions:** 6 conditions cleared v4.7 (Strategy Rules & System Intent Owner sign-off)

---

## Overview

This document defines the `GET /analytics/strategy-version-comparison` endpoint for SI-04.

**Purpose:** Allow the system to compare performance metrics across different versions of the trading strategy configuration, surfacing which version produced better trade outcomes (win rate, R-multiple, trade count).

**Motivation:** As the strategy evolves across cycles, there is no current mechanism to quantify the performance impact of strategy changes. This endpoint provides a data-driven view of strategy version history and their associated trade performance.

**Dependency:** This endpoint requires strategy version tracking infrastructure (version tagging on trades as they enter `trade_history`). Implementation is conditional on strategy version tracking being in place (see SI-04 §13 binding conditions).

**Contract status:** Pre-authored — no backend implementation yet. This document locks the interface design before the sprint in which SI-04 is executed, following the pattern established by SI-03 (arc5_compliance_analytics.md) and SI-01 (behavioural_drift_contract.md).

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
    "performance_delta": null
  },
  "version_to_metrics": {
    "trade_count": "integer",
    "win_rate": "number (0.0–1.0)",
    "avg_R": "number",
    "performance_delta": "number"
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
| `comparison_summary.assessment` | "Insufficient data" when either version has < 10 trades |

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

1. **Strategy version tagging:** Trades must be tagged with the active strategy version at entry time. This requires a `strategy_version` column in `trade_history` — the prerequisite infrastructure item for SI-04.

2. **Version registry:** A strategy version registry (table or config file) must exist to validate `version_from` and `version_to` labels. Format TBD at implementation time.

3. **Comparison direction:** `performance_delta` on `version_to_metrics` represents `version_to.avg_R - version_from.avg_R`. Positive = improvement.

4. **Minimum trade count:** 10 trades per version is the minimum for statistically meaningful comparison. Below this threshold: return 422 `insufficient_data` rather than unreliable metrics.

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

None. (Pre-sprint draft — no implementation against which to record deviations.)

---

## Contract Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-06-01 | Sprint Execution Engine | Initial pre-sprint contract draft. Response schema, query parameters, error cases, §13 binding conditions. SI-04 strategy version comparison endpoint. |
