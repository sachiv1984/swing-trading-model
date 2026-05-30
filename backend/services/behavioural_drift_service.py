"""
Behavioural Drift Detection Service — SI-02

Computes 4 deterministic drift metrics for a portfolio:
  1. entry_timing_drift    — avg days from signal to entry
  2. sizing_adherence      — avg risk% vs plan max
  3. consecutive_loss_sizing — avg risk% after ≥2 consecutive losses
  4. regime_context        — % of trades entered in valid regime

Spec: docs/specs/metrics/si02_drift_score.md §2–§4
§13 PASS: display-only output; no automated recommendations; no ML inference.
"""

from datetime import datetime, timezone
from typing import Optional


_WINDOW_DAYS = 90
_MIN_TRADES = 10
_MIN_POST_LOSS_TRADES = 3

# Metric direction types
_LTE = "lte"  # measured value should be ≤ threshold (lower is better)
_GTE = "gte"  # measured value should be ≥ threshold (higher is better)


def _classify_status(measured: Optional[float], threshold: float, direction: str) -> str:
    """Classify a metric value as ok / approaching / breached.

    Approaching band: within 20% of the threshold boundary.
    Spec: docs/specs/metrics/si02_drift_score.md §2.2
    """
    if measured is None:
        return "insufficient_data"
    if direction == _LTE:
        if measured <= threshold * 0.80:
            return "ok"
        elif measured <= threshold:
            return "approaching"
        else:
            return "breached"
    else:  # _GTE
        if measured >= threshold * 1.20:
            return "ok"
        elif measured >= threshold:
            return "approaching"
        else:
            return "breached"


def _deviation_pct(measured: Optional[float], threshold: float) -> Optional[float]:
    """Compute signed deviation % from threshold.

    Spec: docs/specs/metrics/si02_drift_score.md §2.3
    Positive = above threshold; negative = below threshold.
    """
    if measured is None or threshold == 0:
        return None
    return round(((measured - threshold) / threshold) * 100, 2)


def _build_metric(
    metric_id: str,
    label: str,
    measured_value: Optional[float],
    unit: str,
    threshold: float,
    direction: str,
    advisory_note: Optional[str] = None,
) -> dict:
    status = _classify_status(measured_value, threshold, direction)
    dev_pct = _deviation_pct(measured_value, threshold) if measured_value is not None else None
    return {
        "metric_id": metric_id,
        "label": label,
        "measured_value": round(measured_value, 4) if measured_value is not None else None,
        "unit": unit,
        "status": status,
        "threshold_value": threshold,
        "deviation_pct": dev_pct,
        "advisory_note": advisory_note,
    }


def _compute_entry_timing_drift(signal_timing: list, total_window_trades: int) -> dict:
    """Metric 1: avg days from signal_date to entry_date.

    Excludes trades without a linked signal_id.
    Spec: docs/specs/metrics/si02_drift_score.md §3.1
    """
    excluded = total_window_trades - len(signal_timing)
    advisory = None

    if not signal_timing:
        metric = _build_metric(
            "entry_timing_drift", "Entry Timing", None, "days", 1.0, _LTE,
            advisory_note=f"{excluded} of {total_window_trades} trades in the window have no linked signal and are excluded from timing analysis.",
        )
        metric["status"] = "insufficient_data"
        return metric

    lags = []
    for row in signal_timing:
        entry = row.get("entry_date")
        signal = row.get("signal_date")
        if entry and signal:
            if hasattr(entry, "date"):
                entry = entry.date()
            if hasattr(signal, "date"):
                signal = signal.date()
            lag = (entry - signal).days
            lags.append(lag)

    if not lags:
        metric = _build_metric("entry_timing_drift", "Entry Timing", None, "days", 1.0, _LTE)
        metric["status"] = "insufficient_data"
        return metric

    avg_lag = sum(lags) / len(lags)
    if excluded > 0:
        advisory = f"{excluded} of {total_window_trades} trades in the window have no linked signal and are excluded from timing analysis."

    return _build_metric("entry_timing_drift", "Entry Timing", avg_lag, "days", 1.0, _LTE, advisory_note=advisory)


def _compute_sizing_adherence(trades: list, plan_max: float) -> dict:
    """Metric 2: avg risk% vs plan max.

    Excludes trades where risk_percent_used is NULL.
    Spec: docs/specs/metrics/si02_drift_score.md §3.2
    """
    sized_trades = [t for t in trades if t.get("risk_percent_used") is not None]
    excluded = len(trades) - len(sized_trades)
    advisory = None

    if not sized_trades:
        metric = _build_metric("sizing_adherence", "Sizing Adherence", None, "pct_of_portfolio", plan_max, _LTE)
        metric["status"] = "insufficient_data"
        return metric

    avg_risk = sum(float(t["risk_percent_used"]) for t in sized_trades) / len(sized_trades)

    if avg_risk < plan_max * 0.50:
        advisory = f"Average sizing ({avg_risk:.2f}%) is below 50% of plan rate ({plan_max:.2f}%). Consider using the position sizing calculator consistently."

    if excluded > 0:
        note = f"{excluded} of {len(trades)} trades excluded (risk_percent_used not recorded)."
        advisory = f"{advisory} {note}" if advisory else note

    return _build_metric("sizing_adherence", "Sizing Adherence", avg_risk, "pct_of_portfolio", plan_max, _LTE, advisory_note=advisory)


def _compute_consecutive_loss_sizing(trades: list, plan_max: float) -> dict:
    """Metric 3: avg risk% for trades entered after ≥2 consecutive losses.

    Requires ≥3 qualifying post-loss-streak trades.
    Spec: docs/specs/metrics/si02_drift_score.md §3.3
    """
    # Identify trades entered after ≥2 consecutive losses (by entry_date order)
    post_loss_risk = []
    n = len(trades)
    for i in range(n):
        # Count consecutive losses immediately preceding trade i
        consecutive = 0
        j = i - 1
        while j >= 0:
            pnl = trades[j].get("pnl")
            if pnl is not None and float(pnl) < 0:
                consecutive += 1
                j -= 1
            else:
                break
        if consecutive >= 2:
            risk = trades[i].get("risk_percent_used")
            if risk is not None:
                post_loss_risk.append(float(risk))

    if len(post_loss_risk) < _MIN_POST_LOSS_TRADES:
        metric = _build_metric(
            "consecutive_loss_sizing", "Post-Loss Sizing", None, "pct_of_portfolio", plan_max, _LTE,
            advisory_note=f"Insufficient post-loss-streak trades ({len(post_loss_risk)} of {_MIN_POST_LOSS_TRADES} required).",
        )
        metric["status"] = "insufficient_data"
        return metric

    avg_post_loss = sum(post_loss_risk) / len(post_loss_risk)
    return _build_metric("consecutive_loss_sizing", "Post-Loss Sizing", avg_post_loss, "pct_of_portfolio", plan_max, _LTE)


def _compute_regime_context(trades: list) -> dict:
    """Metric 4: % of trades entered in valid regime (risk_on or neutral/null).

    Uses custom threshold bands per spec §3.4 (not the generic 20% approaching formula):
    - ok:         pct >= 95%
    - approaching: 90% <= pct < 95%
    - breached:   pct < 90%
    Spec: docs/specs/metrics/si02_drift_score.md §3.4
    """
    if not trades:
        return {
            "metric_id": "regime_context",
            "label": "Regime Adherence",
            "measured_value": None,
            "unit": "pct",
            "status": "insufficient_data",
            "threshold_value": 90.0,
            "deviation_pct": None,
            "advisory_note": None,
        }

    valid_count = sum(
        1 for t in trades
        if t.get("regime_context_at_entry") in ("risk_on", "neutral", None, "")
    )
    pct = (valid_count / len(trades)) * 100
    pct_rounded = round(pct, 4)

    if pct >= 95.0:
        status = "ok"
    elif pct >= 90.0:
        status = "approaching"
    else:
        status = "breached"

    return {
        "metric_id": "regime_context",
        "label": "Regime Adherence",
        "measured_value": pct_rounded,
        "unit": "pct",
        "status": status,
        "threshold_value": 90.0,
        "deviation_pct": _deviation_pct(pct_rounded, 90.0),
        "advisory_note": None,
    }


def _overall_status(metrics: list) -> str:
    """Derive top-level status from metric statuses.

    Spec: docs/specs/metrics/si02_drift_score.md §4
    """
    statuses = [m["status"] for m in metrics if m["status"] != "insufficient_data"]
    if not statuses:
        return "insufficient_data"
    if any(s in ("approaching", "breached") for s in statuses):
        return "drift_detected"
    return "no_drift"


def compute_drift(portfolio_data: dict) -> dict:
    """Compute all 4 SI-02 drift metrics from pre-fetched portfolio_data.

    Args:
        portfolio_data: dict from database.get_behavioural_drift_data()
            Keys: trade_count, trades, settings, signal_timing

    Returns:
        Full drift response dict matching GET /analytics/behavioural-drift schema.
        Spec: docs/specs/metrics/si02_drift_score.md §4
        §13: display-only; no automated recommendations; no ML inference.
    """
    trade_count = portfolio_data.get("trade_count", 0)
    trades = portfolio_data.get("trades", [])
    settings = portfolio_data.get("settings")
    signal_timing = portfolio_data.get("signal_timing", [])

    computed_at = datetime.now(timezone.utc).isoformat()

    if trade_count < _MIN_TRADES:
        return {
            "status": "insufficient_data",
            "analysis_window_days": _WINDOW_DAYS,
            "trade_count_in_window": trade_count,
            "metrics": [],
            "computed_at": computed_at,
        }

    plan_max = 1.5  # default fallback
    if settings and settings.get("default_risk_percent") is not None:
        plan_max = float(settings["default_risk_percent"])

    metrics = [
        _compute_entry_timing_drift(signal_timing, trade_count),
        _compute_sizing_adherence(trades, plan_max),
        _compute_consecutive_loss_sizing(trades, plan_max),
        _compute_regime_context(trades),
    ]

    return {
        "status": _overall_status(metrics),
        "analysis_window_days": _WINDOW_DAYS,
        "trade_count_in_window": trade_count,
        "metrics": metrics,
        "computed_at": computed_at,
    }
