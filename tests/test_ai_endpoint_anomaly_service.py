"""
Unit tests for the AI endpoint cost & latency anomaly check
(ST-54, EPIC-05, v9.2, BLG-OPS-112).

Confirms the check fires on a simulated cost/latency spike (this story's
AC), stays quiet on normal variance, and correctly suppresses noise-floor
cases where the baseline itself is too small for a ratio to be meaningful.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.ai_endpoint_anomaly_service import (  # noqa: E402
    check_cost_anomaly,
    check_latency_anomaly,
    run_scheduled_anomaly_check,
)


def test_cost_anomaly_fires_on_simulated_spike():
    result = check_cost_anomaly(
        endpoint="POST /trade-plans/{plan_id}/generate-thesis",
        recent_cost_usd=0.90,
        baseline_cost_usd=0.10,
    )
    assert result.is_anomaly is True
    assert result.reason == "spike_detected"
    assert result.multiplier == 9.0


def test_cost_anomaly_does_not_fire_on_normal_variance():
    result = check_cost_anomaly(
        endpoint="POST /trade-plans/{plan_id}/generate-thesis",
        recent_cost_usd=0.12,
        baseline_cost_usd=0.10,
    )
    assert result.is_anomaly is False
    assert result.reason == "within_normal_range"


def test_latency_anomaly_fires_on_simulated_spike():
    result = check_latency_anomaly(
        endpoint="POST /ai/chat",
        recent_p95_latency_ms=6000.0,
        baseline_p95_latency_ms=1200.0,
    )
    assert result.is_anomaly is True
    assert result.reason == "spike_detected"
    assert result.multiplier == 5.0


def test_latency_anomaly_does_not_fire_on_normal_variance():
    result = check_latency_anomaly(
        endpoint="POST /ai/chat",
        recent_p95_latency_ms=1400.0,
        baseline_p95_latency_ms=1200.0,
    )
    assert result.is_anomaly is False


def test_cost_anomaly_suppressed_below_noise_floor():
    # $0.001 -> $0.004 is a 4x ratio but both values are below
    # MIN_COST_BASELINE_USD -- must not fire.
    result = check_cost_anomaly(
        endpoint="POST /ai/journal-summary",
        recent_cost_usd=0.004,
        baseline_cost_usd=0.001,
    )
    assert result.is_anomaly is False
    assert result.reason == "baseline_below_noise_floor"


def test_latency_anomaly_suppressed_below_noise_floor():
    result = check_latency_anomaly(
        endpoint="POST /ai/daily-briefing",
        recent_p95_latency_ms=180.0,
        baseline_p95_latency_ms=50.0,
    )
    assert result.is_anomaly is False
    assert result.reason == "baseline_below_noise_floor"


def test_no_baseline_does_not_fire_and_is_labelled():
    result = check_cost_anomaly(
        endpoint="POST /trades/{trade_id}/debrief",
        recent_cost_usd=0.05,
        baseline_cost_usd=0.0,
    )
    assert result.is_anomaly is False
    assert result.reason == "no_baseline"


def test_custom_spike_multiplier_respected():
    result = check_cost_anomaly(
        endpoint="POST /trade-plans/generate-plan",
        recent_cost_usd=0.25,
        baseline_cost_usd=0.10,
        spike_multiplier=2.0,
    )
    assert result.is_anomaly is True
    assert result.multiplier == 2.5


# ---------------------------------------------------------------------------
# run_scheduled_anomaly_check — ST-09 (BLG-OPS-151, EPIC-03, v9.4) scheduled-
# job wiring. Cost is exercised against a mocked claude_audit_log feed
# (no live DATABASE_URL in this environment, disclosed per RISK-03); latency
# is exercised via the simulated_latency_feed parameter for the same reason
# (no latency column exists in claude_audit_log at all — see
# database.get_claude_endpoint_cost_windows docstring, BLG-OPS-161).
# ---------------------------------------------------------------------------

def test_scheduled_check_fires_and_alerts_on_simulated_cost_spike(monkeypatch):
    import database
    import services.ai_endpoint_anomaly_service as svc

    monkeypatch.setattr(
        database,
        "get_claude_endpoint_cost_windows",
        lambda: [
            {"endpoint": "POST /ai/chat", "recent_avg_cost_usd": 0.90,
             "recent_count": 5, "baseline_avg_cost_usd": 0.10, "baseline_count": 40},
        ],
    )
    sent = {}

    def fake_send(firing):
        sent["firing"] = firing
        return True

    monkeypatch.setattr(svc, "_send_anomaly_telegram_alert", fake_send)

    result = run_scheduled_anomaly_check()

    assert result["firing_count"] == 1
    assert result["cost_anomalies"][0]["is_anomaly"] is True
    assert result["alert_sent"] is True
    assert len(sent["firing"]) == 1


def test_scheduled_check_no_alert_on_normal_variance(monkeypatch):
    import database
    import services.ai_endpoint_anomaly_service as svc

    monkeypatch.setattr(
        database,
        "get_claude_endpoint_cost_windows",
        lambda: [
            {"endpoint": "POST /ai/chat", "recent_avg_cost_usd": 0.11,
             "recent_count": 5, "baseline_avg_cost_usd": 0.10, "baseline_count": 40},
        ],
    )
    called = {"count": 0}
    monkeypatch.setattr(
        svc, "_send_anomaly_telegram_alert", lambda firing: called.__setitem__("count", called["count"] + 1) or True
    )

    result = run_scheduled_anomaly_check()

    assert result["firing_count"] == 0
    assert result["alert_sent"] is False
    assert called["count"] == 0


def test_scheduled_check_latency_pending_when_no_feed_supplied():
    result = run_scheduled_anomaly_check(send_alert=False)
    assert result["latency_anomalies"] == []
    assert result["latency_data_source"] == "not_available_pending_BLG-OPS-161"


def test_scheduled_check_latency_fires_on_simulated_feed(monkeypatch):
    import database
    monkeypatch.setattr(database, "get_claude_endpoint_cost_windows", lambda: [])

    result = run_scheduled_anomaly_check(
        send_alert=False,
        simulated_latency_feed={
            "POST /ai/chat": {"recent_p95_ms": 6000.0, "baseline_p95_ms": 1200.0},
        },
    )

    assert result["latency_data_source"] == "simulated_feed"
    assert result["latency_anomalies"][0]["is_anomaly"] is True
    assert result["firing_count"] == 1
