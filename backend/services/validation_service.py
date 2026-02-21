"""
HOTFIX — BLG-TECH-02/03 production KeyError: 'pass'

Error:
    by_severity[tier][v["status"]] += 1
    KeyError: 'pass'

Root cause:
    _build_summary initialises tier dicts with keys "passed"/"warned"/"failed"
    but indexes directly with v["status"] which is "pass"/"warn"/"fail".
    Keys don't match values. First result causes KeyError.

Fix:
    Add STATUS_MAP to translate status values to dict keys before indexing.
    Applied to _build_summary only. No other changes.

Branch: fix/blg-tech-02-03-severity-service-consolidation (hotfix commit)
Author: Head of Engineering
Date:   2026-02-21T20:55:00Z
"""

from datetime import datetime
from test_data.validation_data import (
    VALIDATION_TRADES,
    VALIDATION_PORTFOLIO_HISTORY,
    EXPECTED_METRICS,
    TOLERANCE,
)
from services.analytics_service import AnalyticsService


# ---------------------------------------------------------------------------
# Severity mapping — canonical source: analytics_endpoints.md v1.8.1
# Do not modify without an API Contracts Owner spec update first.
# ---------------------------------------------------------------------------
METRIC_SEVERITY = {
    "sharpe_ratio":              "critical",
    "sharpe_ratio_trade_method": "critical",
    "max_drawdown_percent":      "critical",
    "profit_factor":             "critical",
    "recovery_factor":           "high",
    "expectancy":                "high",
    "risk_reward_ratio":         "high",
    "win_streak":                "medium",
    "loss_streak":               "medium",
    "avg_hold_winners":          "medium",
    "avg_hold_losers":           "medium",
    "trade_frequency":           "medium",
    "capital_efficiency":        "medium",
    "days_underwater":           "low",
}

# Maps v["status"] values → by_severity dict keys
# v["status"] is "pass"/"warn"/"fail"
# by_severity keys are "passed"/"warned"/"failed"
STATUS_MAP = {
    "pass": "passed",
    "warn": "warned",
    "fail": "failed",
}


def _check(metric: str, actual, expected, tolerance) -> dict:
    diff = abs(actual - expected)
    if tolerance == 0:
        status = "pass" if actual == expected else "fail"
    else:
        status = "pass" if diff <= tolerance else "fail"

    return {
        "metric":    metric,
        "expected":  expected,
        "actual":    actual,
        "diff":      diff,
        "status":    status,
        "severity":  METRIC_SEVERITY.get(metric, "low"),
        "tolerance": tolerance,
    }


def _by_severity(validations: list) -> dict:
    """
    Aggregate validation results by severity tier.

    Returns all four tiers always, even if a tier has zero metrics.
    Canonical shape defined in analytics_endpoints.md v1.8.1.

    Uses STATUS_MAP to translate "pass"/"warn"/"fail" → "passed"/"warned"/"failed"
    to match the initialised tier dict keys. Direct indexing without this map
    was the cause of the production KeyError.
    """
    tiers = {
        "critical": {"total": 0, "passed": 0, "warned": 0, "failed": 0},
        "high":     {"total": 0, "passed": 0, "warned": 0, "failed": 0},
        "medium":   {"total": 0, "passed": 0, "warned": 0, "failed": 0},
        "low":      {"total": 0, "passed": 0, "warned": 0, "failed": 0},
    }
    for v in validations:
        tier = tiers.get(v["severity"])
        if tier is None:
            continue
        tier["total"] += 1
        key = STATUS_MAP.get(v["status"])
        if key:
            tier[key] += 1
        else:
            tier["failed"] += 1
    return tiers


class ValidationService:
    """
    Validates analytics calculations against the canonical test portfolio.

    All validation business logic lives here.
    The router delegates entirely to validate_all().
    """

    def __init__(self, analytics_service: AnalyticsService = None):
        self.analytics = analytics_service if analytics_service is not None else AnalyticsService()

    def validate_all(self) -> dict:
        """
        Two calculation passes:
          Pass 1 — portfolio + trade data  → exercises portfolio Sharpe path
          Pass 2 — trade data only         → exercises trade Sharpe fallback
                                             (BLG-TECH-01 Addendum 1)
        """
        # ------------------------------------------------------------------
        # Pass 1 — full dataset
        # ------------------------------------------------------------------
        result = self.analytics.calculate_metrics_from_data(
            trades=VALIDATION_TRADES,
            portfolio_history=VALIDATION_PORTFOLIO_HISTORY,
            period="all_time",
            min_trades=2,
        )

        exec_m = result.get("executive_metrics", {})
        adv_m  = result.get("advanced_metrics", {})

        validations = []

        # --- critical tier -------------------------------------------------

        sharpe = _check(
            "sharpe_ratio",
            actual=exec_m.get("sharpe_ratio", 0.0),
            expected=EXPECTED_METRICS["sharpe_ratio"],
            tolerance=TOLERANCE["sharpe_ratio"],
        )
        sharpe["formula"] = "(Avg Return / Std Dev) × √252"
        sharpe["method"]  = exec_m.get("sharpe_method", "unknown")
        validations.append(sharpe)

        max_dd = _check(
            "max_drawdown_percent",
            actual=exec_m.get("max_drawdown", {}).get("percent", 0.0),
            expected=EXPECTED_METRICS["max_drawdown_percent"],
            tolerance=TOLERANCE["max_drawdown_percent"],
        )
        max_dd["formula"] = "((Peak − Trough) / Peak) × 100"
        validations.append(max_dd)

        pf = _check(
            "profit_factor",
            actual=exec_m.get("profit_factor", 0.0),
            expected=EXPECTED_METRICS["profit_factor"],
            tolerance=TOLERANCE["profit_factor"],
        )
        pf["formula"] = "Gross Profit / Gross Loss"
        validations.append(pf)

        # --- high tier -----------------------------------------------------

        rf = _check(
            "recovery_factor",
            actual=exec_m.get("recovery_factor", 0.0),
            expected=EXPECTED_METRICS["recovery_factor"],
            tolerance=TOLERANCE["recovery_factor"],
        )
        rf["formula"] = "Net Profit / Max Drawdown"
        validations.append(rf)

        exp = _check(
            "expectancy",
            actual=exec_m.get("expectancy", 0.0),
            expected=EXPECTED_METRICS["expectancy"],
            tolerance=TOLERANCE["expectancy"],
        )
        exp["formula"] = "(Win Rate × Avg Win) + (Loss Rate × Avg Loss)"
        validations.append(exp)

        rr = _check(
            "risk_reward_ratio",
            actual=exec_m.get("risk_reward_ratio", 0.0),
            expected=EXPECTED_METRICS["risk_reward_ratio"],
            tolerance=TOLERANCE["risk_reward_ratio"],
        )
        rr["formula"] = "Avg Win / Avg Loss"
        validations.append(rr)

        # --- medium tier ---------------------------------------------------

        ws = _check(
            "win_streak",
            actual=adv_m.get("win_streak", 0),
            expected=EXPECTED_METRICS["win_streak"],
            tolerance=TOLERANCE["win_streak"],
        )
        ws["formula"] = "Max consecutive winning trades"
        validations.append(ws)

        ls = _check(
            "loss_streak",
            actual=adv_m.get("loss_streak", 0),
            expected=EXPECTED_METRICS["loss_streak"],
            tolerance=TOLERANCE["loss_streak"],
        )
        ls["formula"] = "Max consecutive losing trades"
        validations.append(ls)

        ahw = _check(
            "avg_hold_winners",
            actual=adv_m.get("avg_hold_winners", 0.0),
            expected=EXPECTED_METRICS["avg_hold_winners"],
            tolerance=TOLERANCE["avg_hold_winners"],
        )
        ahw["formula"] = "Avg days held, winning trades"
        validations.append(ahw)

        ahl = _check(
            "avg_hold_losers",
            actual=adv_m.get("avg_hold_losers", 0.0),
            expected=EXPECTED_METRICS["avg_hold_losers"],
            tolerance=TOLERANCE["avg_hold_losers"],
        )
        ahl["formula"] = "Avg days held, losing trades"
        validations.append(ahl)

        tf = _check(
            "trade_frequency",
            actual=adv_m.get("trade_frequency", 0.0),
            expected=EXPECTED_METRICS["trade_frequency"],
            tolerance=TOLERANCE["trade_frequency"],
        )
        tf["formula"] = "Trades per week"
        validations.append(tf)

        # BLG-TECH-01: expected 0.17 → 0.22 (total_cost GBP basis)
        ce = _check(
            "capital_efficiency",
            actual=adv_m.get("capital_efficiency", 0.0),
            expected=EXPECTED_METRICS["capital_efficiency"],
            tolerance=TOLERANCE["capital_efficiency"],
        )
        ce["formula"] = "(Total PnL / Mean(total_cost)) × 100"
        validations.append(ce)

        # --- low tier ------------------------------------------------------

        du = _check(
            "days_underwater",
            actual=adv_m.get("days_underwater", 0),
            expected=EXPECTED_METRICS["days_underwater"],
            tolerance=TOLERANCE["days_underwater"],
        )
        du["formula"] = "Days since peak equity"
        validations.append(du)

        # ------------------------------------------------------------------
        # Pass 2 — trade data only (forces trade Sharpe fallback)
        # BLG-TECH-01 Addendum 1 — PMO-confirmed scope
        # ------------------------------------------------------------------
        result_trade = self.analytics.calculate_metrics_from_data(
            trades=VALIDATION_TRADES,
            portfolio_history=[],
            period="all_time",
            min_trades=2,
        )
        exec_trade = result_trade.get("executive_metrics", {})

        trade_sharpe = _check(
            "sharpe_ratio_trade_method",
            actual=exec_trade.get("sharpe_ratio", 0.0),
            expected=EXPECTED_METRICS.get("sharpe_ratio_trade", 0.0),
            tolerance=TOLERANCE["sharpe_ratio"],
        )
        trade_sharpe["formula"] = "(Avg Ann Return / Sample StdDev) — trade method"
        trade_sharpe["method"]  = "trade"
        validations.append(trade_sharpe)

        # ------------------------------------------------------------------
        # Summary
        # ------------------------------------------------------------------
        passed = sum(1 for v in validations if v["status"] == "pass")
        warned = sum(1 for v in validations if v["status"] == "warn")
        failed = sum(1 for v in validations if v["status"] == "fail")

        return {
            "validations": validations,
            "summary": {
                "total":       len(validations),
                "passed":      passed,
                "warned":      warned,
                "failed":      failed,
                "by_severity": _by_severity(validations),
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }