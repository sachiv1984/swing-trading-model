"""
AI endpoint cost & latency drift/anomaly check (ST-54, EPIC-05, v9.2, BLG-OPS-112).

Pure, DB-independent anomaly detector: compares a recent-window aggregate
(cost or latency) against a trailing baseline aggregate for the same
AI-invoking endpoint and flags a spike when the recent value exceeds the
baseline by more than a configurable multiplier.

Scope (ST-54 AC: "Anomaly check scoped and added; confirmed to fire on a
simulated cost/latency spike"): this module provides the detection functions,
verified via a simulated spike in tests/test_ai_endpoint_anomaly_service.py.

Wiring update (ST-09, BLG-OPS-151, EPIC-03, v9.4): `run_scheduled_anomaly_check()`
below wires these into POST /ai/check-endpoint-anomalies, triggered by
.github/workflows/ai-endpoint-anomaly-check.yml on a daily cadence, with a
Telegram alert on any firing anomaly (not log-only).

Latency real-data wiring (ST-13, BLG-OPS-161, EPIC-02, v9.5):
`claude_audit_log` now carries a `latency_ms` column (populated for new
rows going forward by every `create_claude_audit_entry()` call site --
pre-existing rows remain NULL and are excluded from latency windows, not
treated as 0ms), and `database.get_claude_endpoint_latency_windows()`
provides the same recent-vs-baseline-window shape as
`get_claude_endpoint_cost_windows()`. `run_scheduled_anomaly_check()` now
sources latency from there by default -- `simulated_latency_feed` remains
supported (e.g. for tests or a deliberate dry-run) and takes priority when
explicitly passed, but is no longer the only source.

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


def run_scheduled_anomaly_check(
    send_alert: bool = True,
    simulated_latency_feed: Optional[dict] = None,
) -> dict:
    """Wire check_cost_anomaly/check_latency_anomaly into a callable a
    scheduler can invoke (ST-09, BLG-OPS-151, EPIC-03, v9.4).

    Cost: sourced from real `claude_audit_log` data via
    `database.get_claude_endpoint_cost_windows()` (recent 24h vs trailing
    7-day baseline, per endpoint).

    Latency: real data by default, sourced from `claude_audit_log.latency_ms`
    via `database.get_claude_endpoint_latency_windows()` (ST-13, BLG-OPS-161
    — see that function's docstring). Endpoints with no `latency_ms` data
    yet in the current window (either because no calls occurred, or because
    all matching rows predate this column and are still NULL) are simply
    absent from the real-data results, not fabricated as 0ms.

    `simulated_latency_feed` remains supported as `{endpoint:
    {"recent_p95_ms": x, "baseline_p95_ms": y}}` for tests or a deliberate
    dry-run — when passed, it is used *instead of* the real-data source
    (not merged with it), and `latency_data_source` reports which one was
    actually used.

    On any firing anomaly (cost or latency), sends a Telegram alert reusing
    the delivery pattern already used by
    `services.gemini_service.check_and_alert_daily_cost` (SI-05/BLG-OPS-57
    precedent) — not log-only, per this story's AC.
    """
    from database import get_claude_endpoint_cost_windows, get_claude_endpoint_latency_windows

    cost_results = []
    for window in get_claude_endpoint_cost_windows():
        cost_results.append(
            check_cost_anomaly(
                endpoint=window["endpoint"],
                recent_cost_usd=window["recent_avg_cost_usd"],
                baseline_cost_usd=window["baseline_avg_cost_usd"],
            )
        )

    latency_results = []
    if simulated_latency_feed:
        for endpoint, values in simulated_latency_feed.items():
            latency_results.append(
                check_latency_anomaly(
                    endpoint=endpoint,
                    recent_p95_latency_ms=values["recent_p95_ms"],
                    baseline_p95_latency_ms=values["baseline_p95_ms"],
                )
            )
        latency_data_source = "simulated_feed"
    else:
        for window in get_claude_endpoint_latency_windows():
            latency_results.append(
                check_latency_anomaly(
                    endpoint=window["endpoint"],
                    recent_p95_latency_ms=window["recent_p95_latency_ms"],
                    baseline_p95_latency_ms=window["baseline_p95_latency_ms"],
                )
            )
        latency_data_source = "claude_audit_log"

    firing = [r for r in cost_results + latency_results if r.is_anomaly]
    alert_sent = False
    if firing and send_alert:
        alert_sent = _send_anomaly_telegram_alert(firing)

    return {
        "checked_utc": _now_iso(),
        "cost_anomalies": [_result_dict(r) for r in cost_results],
        "latency_anomalies": [_result_dict(r) for r in latency_results],
        "firing_count": len(firing),
        "alert_sent": alert_sent,
        "latency_data_source": latency_data_source,
    }


def _result_dict(r: AnomalyResult) -> dict:
    return {
        "endpoint": r.endpoint,
        "metric": r.metric,
        "is_anomaly": r.is_anomaly,
        "recent_value": r.recent_value,
        "baseline_value": r.baseline_value,
        "multiplier": r.multiplier,
        "reason": r.reason,
    }


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def _send_anomaly_telegram_alert(firing: list) -> bool:
    """Send one Telegram alert summarising all firing anomalies. Mirrors
    `services.gemini_service.check_and_alert_daily_cost`'s delivery
    mechanism (urllib, same bot/chat env vars) rather than a log-only
    notification."""
    from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    import urllib.request
    import urllib.parse

    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        return False

    lines = ["⚠️ AI endpoint cost/latency anomaly detected"]
    for r in firing:
        lines.append(
            f"{r.endpoint} [{r.metric}]: recent={r.recent_value:.4g} "
            f"baseline={r.baseline_value:.4g} ({r.multiplier:.1f}x)"
        )
    msg = "\n".join(lines)
    params = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
    })
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?{params}"
    try:
        urllib.request.urlopen(url, timeout=10)
        return True
    except Exception:
        return False
