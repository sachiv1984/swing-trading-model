from typing import Dict, List, Any
from datetime import datetime
from backend.test_data.validation_portfolio import (
    TEST_TRADES,
    TEST_PORTFOLIO_HISTORY,
    EXPECTED_METRICS,
    TOLERANCE_CONFIG,
)


class ValidationService:
    """
    Validates analytics calculations against test data.
    Compares actual calculated values with expected values.
    """

    def __init__(self, analytics_service):
        """
        Args:
            analytics_service: The analytics service that calculates metrics
        """
        self.analytics = analytics_service

    def validate_all(self) -> Dict[str, Any]:
        """
        Run all validation checks on test data.

        Returns:
            dict: Complete validation results
        """
        # Calculate actual metrics from test data
        actual_metrics = self.analytics.calculate_metrics(
            trades=TEST_TRADES, portfolio_history=TEST_PORTFOLIO_HISTORY
        )

        # Run individual validations
        validations = [
            self._validate_sharpe_ratio(actual_metrics),
            self._validate_max_drawdown(actual_metrics),
            self._validate_recovery_factor(actual_metrics),
            self._validate_expectancy(actual_metrics),
            self._validate_profit_factor(actual_metrics),
            self._validate_risk_reward(actual_metrics),
            self._validate_win_rate(actual_metrics),
            self._validate_win_streak(actual_metrics),
            self._validate_loss_streak(actual_metrics),
            self._validate_avg_hold_winners(actual_metrics),
            self._validate_avg_hold_losers(actual_metrics),
            self._validate_time_underwater(actual_metrics),
        ]

        # Calculate summary
        summary = {
            "total": len(validations),
            "passed": sum(1 for v in validations if v["status"] == "pass"),
            "warned": sum(1 for v in validations if v["status"] == "warn"),
            "failed": sum(1 for v in validations if v["status"] == "fail"),
        }

        return {
            "validations": validations,
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    def _validate_sharpe_ratio(self, actual: Dict) -> Dict:
        """Validate Sharpe ratio calculation."""
        expected = EXPECTED_METRICS["sharpe_ratio"]
        actual_value = actual.get("sharpe_ratio", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["sharpe_ratio"]

        return {
            "metric": "sharpe_ratio",
            "expected": expected,
            "actual": round(actual_value, 3),
            "diff": round(diff, 3),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "(Avg Return / Std Dev) × √252",
            "method": actual.get("sharpe_method", "portfolio"),
            "data_points": len(TEST_PORTFOLIO_HISTORY),
        }

    def _validate_max_drawdown(self, actual: Dict) -> Dict:
        """Validate max drawdown calculation."""
        expected = EXPECTED_METRICS["max_drawdown_percent"]
        actual_value = actual.get("max_drawdown", {}).get("percent", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["max_drawdown_percent"]

        return {
            "metric": "max_drawdown",
            "expected": expected,
            "actual": round(actual_value, 2),
            "diff": round(diff, 2),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "((Min Value - Peak) / Peak) × 100",
            "data_points": len(TEST_PORTFOLIO_HISTORY),
        }

    def _validate_expectancy(self, actual: Dict) -> Dict:
        """Validate expectancy calculation."""
        expected = EXPECTED_METRICS["expectancy"]
        actual_value = actual.get("expectancy", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["expectancy"]

        return {
            "metric": "expectancy",
            "expected": expected,
            "actual": round(actual_value, 2),
            "diff": round(diff, 2),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "(Win% × AvgWin) + (Loss% × AvgLoss)",
            "data_points": len(TEST_TRADES),
        }

    def _validate_profit_factor(self, actual: Dict) -> Dict:
        """Validate profit factor calculation."""
        expected = EXPECTED_METRICS["profit_factor"]
        actual_value = actual.get("profit_factor", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["profit_factor"]

        return {
            "metric": "profit_factor",
            "expected": expected,
            "actual": round(actual_value, 3),
            "diff": round(diff, 3),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "Gross Profit / Gross Loss",
        }

    def _validate_risk_reward(self, actual: Dict) -> Dict:
        """Validate risk/reward ratio."""
        expected = EXPECTED_METRICS["risk_reward_ratio"]
        actual_value = actual.get("risk_reward_ratio", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["risk_reward_ratio"]

        return {
            "metric": "risk_reward_ratio",
            "expected": expected,
            "actual": round(actual_value, 3),
            "diff": round(diff, 3),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "Avg Win / Avg Loss",
        }

    def _validate_win_rate(self, actual: Dict) -> Dict:
        """Validate win rate calculation."""
        expected = EXPECTED_METRICS["win_rate"]
        actual_value = actual.get("win_rate", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["win_rate"]

        return {
            "metric": "win_rate",
            "expected": expected,
            "actual": round(actual_value, 2),
            "diff": round(diff, 2),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "(Winners / Total Trades) × 100",
        }

    def _validate_win_streak(self, actual: Dict) -> Dict:
        """Validate max win streak."""
        expected = EXPECTED_METRICS["win_streak"]
        actual_value = actual.get("win_streak", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["win_streak"]  # Must be exact

        return {
            "metric": "win_streak",
            "expected": expected,
            "actual": actual_value,
            "diff": diff,
            "status": "pass" if diff == 0 else "fail",
            "tolerance": tolerance,
            "formula": "Maximum consecutive winning trades",
        }

    def _validate_loss_streak(self, actual: Dict) -> Dict:
        """Validate max loss streak."""
        expected = EXPECTED_METRICS["loss_streak"]
        actual_value = actual.get("loss_streak", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["loss_streak"]  # Must be exact

        return {
            "metric": "loss_streak",
            "expected": expected,
            "actual": actual_value,
            "diff": diff,
            "status": "pass" if diff == 0 else "fail",
            "tolerance": tolerance,
            "formula": "Maximum consecutive losing trades",
        }

    def _validate_avg_hold_winners(self, actual: Dict) -> Dict:
        """Validate average holding period for winners."""
        expected = EXPECTED_METRICS["avg_hold_winners"]
        actual_value = actual.get("avg_hold_winners", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["avg_hold_winners"]

        return {
            "metric": "avg_hold_winners",
            "expected": expected,
            "actual": round(actual_value, 2),
            "diff": round(diff, 2),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "Average days holding winning trades",
        }

    def _validate_avg_hold_losers(self, actual: Dict) -> Dict:
        """Validate average holding period for losers."""
        expected = EXPECTED_METRICS["avg_hold_losers"]
        actual_value = actual.get("avg_hold_losers", 0)
        diff = actual_value - expected
        tolerance = TOLERANCE_CONFIG["avg_hold_losers"]

        return {
            "metric": "avg_hold_losers",
            "expected": expected,
            "actual": round(actual_value, 2),
            "diff": round(diff, 2),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "Average days holding losing trades",
        }

    def _validate_time_underwater(self, actual: Dict) -> Dict:
        """Validate time underwater calculation."""
        expected = EXPECTED_METRICS["time_underwater"]
        actual_value = actual.get("days_underwater", 0)
        diff = actual_value - expected

        return {
            "metric": "time_underwater",
            "expected": expected,
            "actual": actual_value,
            "diff": diff,
            "status": "pass" if diff == 0 else "fail",
            "tolerance": 0,
            "formula": "Days since last equity peak",
        }

    def _validate_recovery_factor(self, actual: Dict) -> Dict:
        """Validate recovery factor calculation."""
        expected = EXPECTED_METRICS["recovery_factor"]
        actual_value = actual.get("recovery_factor", 0)
        diff = actual_value - expected
        tolerance = 0.05  # ±0.05

        return {
            "metric": "recovery_factor",
            "expected": expected,
            "actual": round(actual_value, 3),
            "diff": round(diff, 3),
            "diff_percent": round((diff / expected) * 100, 2) if expected != 0 else 0,
            "status": self._determine_status(abs(diff), tolerance),
            "tolerance": tolerance,
            "formula": "Period Profit / Period Max Drawdown",
        }

    def _determine_status(self, diff: float, tolerance: float) -> str:
        """
        Determine validation status based on difference and tolerance.

        Args:
            diff: Absolute difference between expected and actual
            tolerance: Acceptable tolerance level

        Returns:
            str: "pass", "warn", or "fail"
        """
        if diff <= tolerance:
            return "pass"
        elif diff <= (tolerance * 1.2):  # Within 120% of tolerance
            return "warn"
        else:
            return "fail"
