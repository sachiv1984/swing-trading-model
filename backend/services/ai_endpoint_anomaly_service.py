"""
AI endpoint cost & latency drift/anomaly check (ST-54, EPIC-05, v9.2, BLG-OPS-112).

Pure, DB-independent anomaly detector: compares a recent-window aggregate
(cost or latency) against a trailing baseline aggregate for the same
AI-invoking endpoint and flags a spike when the recent value exceeds the
baseline by more than a configurable multiplier.

Scope (ST-54 AC: "Anomaly check scoped and added; confirmed to fire on a
simulated cost/latency spike"): this module provides the detection function
and is verified via a simulated spike in tests/test_ai_endpoint_anomaly_service.py
-- it is not wired to a live scheduled job or alert-delivery channel this
cycle (no production DB access from this environment to source real
recent-window data; see docs/ops/ai_feature_cost_trend_2026_q3.md §3 for the
same constraint documented against ST-56). Wiring this into an actual
scheduled check (e.g. alongside POST /ai/check-daily-cost) is follow-up
scope, filed as BLG-OPS-151.

Covers all 6 current AI-invoking endpoints (per the same inventory used in
docs/ops/ai_feature_cost_trend_2026_q3.md):
  - POST /ai/journal-summary
  - POST /ai/daily-briefing
  - POST /ai/chat
  - POST /trade-plans/generate-plan
  - POST /trade-plans/{plan_id}/generate-thesis
  - POST /trades/{trade_id}/debrief
This module is endpoint-agnostic (it operates on cost/latency numbers, not
endpoint-specific logic), so no per-endpoint branching is required to cover
all 6 -- the caller supplies which endpoint's numbers it's checking.
"""
from dataclasses import dataclass
from typing import Optional

DEFAULT_COST_SPIKE_MULTIPLIER = 3.0
DEFAULT_LATENCY_SPIKE_MULTIPLIER = 3.0

# Below this baseline, small absolute variance produces a huge (and
# meaningless) percentage swing -- e.g. $0.001 -> $0.004 is a "4x spike"
# but an operationally irrelevant $0.003 delta. Suppress cost-anomaly
# firing below this floor regardless of multiplier.
MIN_COST_BASELINE_USD = 0.01
# Same rationale for latency: a 50ms -> 200ms swing on a near-instant
# endpoint is noise, not a real drift signal, below this floor.
MIN_LATENCY_BASELINE_MS = 200.0


@dataclass
class AnomalyResult:
    endpoint: str
    metric: str  # "cost" or "latency"
    is_anomaly: bool
    recent_value: float
    baseline_value: float
    multiplier: Optional[float]  # recent / baseline, None if baseline is 0
    reason: str


def _check_metric(
    endpoint: str,
    metric: str,
    recent_value: float,
    baseline_value: float,
    spike_multiplier: float,
    min_baseline: float,
) -> AnomalyResult:
    if baseline_value is None or baseline_value <= 0:
        # No baseline yet (e.g. a brand-new endpoint) -- cannot compute a
        # meaningful ratio. Not flagged as an anomaly (nothing to compare
        # against), but the caller should not treat this as "confirmed normal".
        return AnomalyResult(
            endpoint=endpoint,
            metric=metric,
            is_anomaly=False,
            recent_value=recent_value,
            baseline_value=baseline_value or 0.0,
            multiplier=None,
            reason="no_baseline",
        )

    if baseline_value < min_baseline:
        return AnomalyResult(
            endpoint=endpoint,
            metric=metric,
            is_anomaly=False,
            recent_value=recent_value,
            baseline_value=baseline_value,
            multiplier=recent_value / baseline_value,
            reason="baseline_below_noise_floor",
        )

    ratio = recent_value / baseline_value
    is_anomaly = ratio >= spike_multiplier
    return AnomalyResult(
        endpoint=endpoint,
        metric=metric,
        is_anomaly=is_anomaly,
        recent_value=recent_value,
        baseline_value=baseline_value,
        multiplier=ratio,
        reason="spike_detected" if is_anomaly else "within_normal_range",
    )


def check_cost_anomaly(
    endpoint: str,
    recent_cost_usd: float,
    baseline_cost_usd: float,
    spike_multiplier: float = DEFAULT_COST_SPIKE_MULTIPLIER,
) -> AnomalyResult:
    """Flag a cost spike when recent_cost_usd >= spike_multiplier * baseline_cost_usd,
    with baseline_cost_usd below MIN_COST_BASELINE_USD suppressed as noise."""
    return _check_metric(
        endpoint, "cost", recent_cost_usd, baseline_cost_usd, spike_multiplier, MIN_COST_BASELINE_USD
    )


def check_latency_anomaly(
    endpoint: str,
    recent_p95_latency_ms: float,
    baseline_p95_latency_ms: float,
    spike_multiplier: float = DEFAULT_LATENCY_SPIKE_MULTIPLIER,
) -> AnomalyResult:
    """Flag a latency spike when recent_p95_latency_ms >= spike_multiplier *
    baseline_p95_latency_ms, with baseline below MIN_LATENCY_BASELINE_MS
    suppressed as noise."""
    return _check_metric(
        endpoint,
        "latency",
        recent_p95_latency_ms,
        baseline_p95_latency_ms,
        spike_multiplier,
        MIN_LATENCY_BASELINE_MS,
    )
