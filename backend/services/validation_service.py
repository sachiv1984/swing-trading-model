"""
ValidationService — Analytics Calculation Validation

BLG-TECH-02: Implements severity field per result and by_severity aggregation
             per analytics_endpoints.md v1.8.1.
BLG-TECH-03: Consolidates all validation business logic from routers/validation.py
             into this service layer per backend_engineering_patterns.md §3.

Canonical spec: analytics_endpoints.md v1.8.1
Architecture:   backend_engineering_patterns.md §3
"""

from datetime import datetime
from services.analytics_service import AnalyticsService
from test_data.validation_data import (
    VALIDATION_TRADES,
    VALIDATION_PORTFOLIO_HISTORY,
    EXPECTED_METRICS,
    TOLERANCE,
)

# Severity assignment per metric — canonical source: analytics_endpoints.md v1.8.1
# Fixed regardless of pass/fail status.
METRIC_SEVERITY = {
    "sharpe_ratio":       "critical",
    "max_drawdown_percent": "critical",
    "profit_factor":      "critical",
    "recovery_factor":    "high",
    "expectancy":         "high",
    "risk_reward_ratio":  "high",
    "win_streak":         "medium",
    "loss_streak":        "medium",
    "avg_hold_winners":   "medium",
    "avg_hold_losers":    "medium",
    "trade_frequency":    "medium",
    "capital_efficiency": "medium",
    "days_underwater":    "low",
}

# Severity tiers for by_severity aggregation — order is canonical
SEVERITY_TIERS = ["critical", "high", "medium", "low"]


class ValidationService:
    """
    Validates analytics calculations against the test portfolio.

    Owns all validation business logic. The router delegates entirely
    to this service — no calculation logic belongs in the router layer.
    """

    def __init__(self, analytics_service: AnalyticsService = None):
        self.analytics = analytics_service or AnalyticsService()

    def validate_all(self) -> dict:
        """
        Run all validation checks against the internal test portfolio.

        Returns the full validated response payload matching the contract
        defined in analytics_endpoints.md v1.8.1.

        Returns:
            dict: {validations: [...], summary: {...}, timestamp: str}

        Raises:
            Exception: Propagated to router for HTTP 500 handling.
        """
        result = self.analytics.calculate_metrics_from_data(
            trades=VALIDATION_TRADES,
            portfolio_history=VALIDATION_PORTFOLIO_HISTORY,
            period="all_time",
            min_trades=2,  # Validation dataset has 5 trades
        )

        exec_metrics = result.get("executive_metrics", {})
        adv_metrics = result.get("advanced_metrics", {})

        validations = self._build_validations(exec_metrics, adv_metrics)
        summary = self._build_summary(validations)

        return {
            "validations": validations,
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # ------------------------------------------------------------------
    # Private — business logic
    # ------------------------------------------------------------------

    def _build_validations(self, exec_metrics: dict, adv_metrics: dict) -> list:
        """Build the validations list with severity per entry."""
        return [
            self._result(
                metric="sharpe_ratio",
                expected=EXPECTED_METRICS["sharpe_ratio"],
                actual=exec_metrics.get("sharpe_ratio", 0.0),
                formula="(Avg Return / Std Dev) × √252",
                extra={"method": exec_metrics.get("sharpe_method", "unknown")},
            ),
            self._result(
                metric="max_drawdown_percent",
                expected=EXPECTED_METRICS["max_drawdown_percent"],
                actual=exec_metrics.get("max_drawdown", {}).get("percent", 0.0),
                formula="((Peak - Trough) / Peak) × 100",
            ),
            self._result(
                metric="profit_factor",
                expected=EXPECTED_METRICS["profit_factor"],
                actual=exec_metrics.get("profit_factor", 0.0),
                formula="Gross Profit / Gross Loss",
            ),
            self._result(
                metric="recovery_factor",
                expected=EXPECTED_METRICS["recovery_factor"],
                actual=exec_metrics.get("recovery_factor", 0.0),
                formula="Net Profit / Max Drawdown",
            ),
            self._result(
                metric="expectancy",
                expected=EXPECTED_METRICS["expectancy"],
                actual=exec_metrics.get("expectancy", 0.0),
                formula="(Win Rate × Avg Win) + (Loss Rate × Avg Loss)",
            ),
            self._result(
                metric="risk_reward_ratio",
                expected=EXPECTED_METRICS["risk_reward_ratio"],
                actual=exec_metrics.get("risk_reward_ratio", 0.0),
                formula="Avg Win / Avg Loss",
            ),
            self._result(
                metric="win_streak",
                expected=EXPECTED_METRICS["win_streak"],
                actual=adv_metrics.get("win_streak", 0),
                formula="Max consecutive winning trades",
            ),
            self._result(
                metric="loss_streak",
                expected=EXPECTED_METRICS["loss_streak"],
                actual=adv_metrics.get("loss_streak", 0),
                formula="Max consecutive losing trades",
            ),
            self._result(
                metric="avg_hold_winners",
                expected=EXPECTED_METRICS["avg_hold_winners"],
                actual=adv_metrics.get("avg_hold_winners", 0.0),
                formula="Avg days held, winning trades",
            ),
            self._result(
                metric="avg_hold_losers",
                expected=EXPECTED_METRICS["avg_hold_losers"],
                actual=adv_metrics.get("avg_hold_losers", 0.0),
                formula="Avg days held, losing trades",
            ),
            self._result(
                metric="trade_frequency",
                expected=EXPECTED_METRICS["trade_frequency"],
                actual=adv_metrics.get("trade_frequency", 0.0),
                formula="Trades per week",
            ),
            self._result(
                metric="capital_efficiency",
                expected=EXPECTED_METRICS["capital_efficiency"],
                actual=adv_metrics.get("capital_efficiency", 0.0),
                formula="(Total PnL / Mean(total_cost)) × 100",
            ),
            self._result(
                metric="days_underwater",
                expected=EXPECTED_METRICS["days_underwater"],
                actual=adv_metrics.get("days_underwater", 0),
                formula="Days since peak equity",
            ),
        ]

    def _result(
        self,
        metric: str,
        expected,
        actual,
        formula: str,
        extra: dict = None,
    ) -> dict:
        """
        Build a single validation result object.

        Includes severity per analytics_endpoints.md v1.8.1.
        Status logic: pass if diff <= tolerance, warn if <= 2×tolerance, else fail.
        """
        tolerance = TOLERANCE[metric]
        diff = abs(actual - expected)

        if diff <= tolerance:
            status = "pass"
        elif diff <= tolerance * 2:
            status = "warn"
        else:
            status = "fail"

        entry = {
            "metric": metric,
            "expected": expected,
            "actual": actual,
            "diff": round(diff, 6),
            "status": status,
            "severity": METRIC_SEVERITY[metric],
            "tolerance": tolerance,
            "formula": formula,
        }

        if extra:
            entry.update(extra)

        return entry

    def _build_summary(self, validations: list) -> dict:
        """
        Build the summary object including by_severity aggregation.

        Per analytics_endpoints.md v1.8.1: by_severity always present
        with all four keys even if a tier has zero metrics.
        """
        total = len(validations)
        passed = sum(1 for v in validations if v["status"] == "pass")
        warned = sum(1 for v in validations if v["status"] == "warn")
        failed = sum(1 for v in validations if v["status"] == "fail")

        # Initialise all four tiers — always present per contract
        by_severity = {
            tier: {"total": 0, "passed": 0, "warned": 0, "failed": 0}
            for tier in SEVERITY_TIERS
        }

        for v in validations:
            tier = v["severity"]
            by_severity[tier]["total"] += 1
            by_severity[tier][v["status"]] += 1

        return {
            "total": total,
            "passed": passed,
            "warned": warned,
            "failed": failed,
            "by_severity": by_severity,
        }