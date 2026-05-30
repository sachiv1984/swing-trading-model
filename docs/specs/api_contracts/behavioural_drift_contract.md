**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-30
**Shipped:** v4.6 — ST-04, EPIC-01, cycle 2026-05-30__release-v4.6
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**§13 gate:** PASS — `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md`

---

# SI-02 Behavioural Drift Detection API Contract

## Overview

This document defines the `GET /analytics/behavioural-drift` endpoint, which computes 4 deterministic drift metrics over a 90-day rolling window for the authenticated portfolio.

**§13 compliance:** Output is display-only. No automated recommendations, no ML inference, no automated trade decisions. All formulas are deterministic. Operator may use or discard the output.

**Backend implementation:** `backend/routers/analytics.py` (`get_behavioural_drift`), `backend/services/behavioural_drift_service.py`

**Metric spec:** `docs/specs/metrics/si02_drift_score.md`

---

## Endpoints

- [GET /analytics/behavioural-drift](#get-analyticsbehavioural-drift)

---

## GET /analytics/behavioural-drift

**Purpose**

Returns the SI-02 Behavioural Drift Detection analysis for the authenticated portfolio. Computes 4 metrics (entry timing drift, sizing adherence, post-loss sizing, regime adherence) over the most recent 90 calendar days of closed trades.

**Authentication:** Required (X-API-Key header)

**Parameters:** None

**Minimum data:** 10 closed trades in the analysis window. If below threshold, returns `status: "insufficient_data"` with no metric values.

### Response Shape (200 OK)

```json
{
  "status": "ok",
  "data": {
    "status": "insufficient_data | no_drift | drift_detected | error",
    "analysis_window_days": 90,
    "trade_count_in_window": 12,
    "metrics": [
      {
        "metric_id": "entry_timing_drift",
        "label": "Entry Timing",
        "measured_value": 0.75,
        "unit": "days",
        "status": "ok",
        "threshold_value": 1.0,
        "deviation_pct": -25.0,
        "advisory_note": null
      },
      {
        "metric_id": "sizing_adherence",
        "label": "Sizing Adherence",
        "measured_value": 1.45,
        "unit": "pct_of_portfolio",
        "status": "approaching",
        "threshold_value": 1.5,
        "deviation_pct": -3.33,
        "advisory_note": null
      },
      {
        "metric_id": "consecutive_loss_sizing",
        "label": "Post-Loss Sizing",
        "measured_value": null,
        "unit": "pct_of_portfolio",
        "status": "insufficient_data",
        "threshold_value": 1.5,
        "deviation_pct": null,
        "advisory_note": "Insufficient post-loss-streak trades (1 of 3 required)."
      },
      {
        "metric_id": "regime_context",
        "label": "Regime Adherence",
        "measured_value": 95.5,
        "unit": "pct",
        "status": "ok",
        "threshold_value": 90.0,
        "deviation_pct": 6.11,
        "advisory_note": null
      }
    ],
    "computed_at": "2026-05-30T21:00:00Z"
  }
}
```

### Top-Level Status

| Status | Condition |
|--------|-----------|
| `insufficient_data` | Fewer than 10 closed trades in the 90-day window |
| `no_drift` | All metrics with sufficient data are in `ok` state |
| `drift_detected` | At least one metric is in `approaching` or `breached` state |
| `error` | Service computation failure — response includes error_detail; no metrics returned |

### Metric Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `metric_id` | string | Machine identifier: `entry_timing_drift`, `sizing_adherence`, `consecutive_loss_sizing`, `regime_context` |
| `label` | string | Human-readable label |
| `measured_value` | number or null | Computed metric value; null when insufficient data for this metric only |
| `unit` | string | `days`, `pct_of_portfolio`, or `pct` |
| `status` | string | `ok`, `approaching`, `breached`, or `insufficient_data` |
| `threshold_value` | number | The threshold this metric is compared against |
| `deviation_pct` | number or null | Signed deviation % from threshold: `((measured - threshold) / threshold) × 100` |
| `advisory_note` | string or null | Surfaced when status is `approaching` or `breached`, or when data quality issues exist |

### Metric Thresholds

| Metric | Threshold | Direction | Green | Amber | Red |
|--------|-----------|-----------|-------|-------|-----|
| Entry timing drift | 1.0 day | lte (lower is better) | ≤ 0.80 days | 0.80–1.0 days | > 1.0 days |
| Sizing adherence | `settings.default_risk_percent` | lte | ≤ plan_max × 0.80 | plan_max × 0.80 – plan_max | > plan_max |
| Post-loss sizing | `settings.default_risk_percent` | lte | ≤ plan_max × 0.80 | plan_max × 0.80 – plan_max | > plan_max |
| Regime adherence | 90% | gte (higher is better) | ≥ 108% (≥ 90 × 1.20%) | 90–108% | < 90% |

### Error Response (401)

```json
{"detail": "Unauthorized"}
```

### Error Response (500 / computation failure)

The endpoint returns 200 with `data.status = "error"` and an `error_detail` field rather than a 500 status code, to allow graceful frontend degradation.

---

## Known Deviations

None at v1.0.
