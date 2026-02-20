from fastapi import APIRouter, HTTPException
from services.analytics_service import AnalyticsService
from test_data.validation_data import (
    VALIDATION_TRADES,
    VALIDATION_PORTFOLIO_HISTORY,
    EXPECTED_METRICS,
    TOLERANCE
)

router = APIRouter(prefix="/validate", tags=["Validation"])


@router.post("/calculations")
async def validate_calculations():
    """
    Validate all analytics calculations against test portfolio.

    No request body required - validates against internal test data.

    Returns:
        dict: Validation results with pass/fail for each metric
    """
    try:
        service = AnalyticsService()

        result = service.calculate_metrics_from_data(
            trades=VALIDATION_TRADES,
            portfolio_history=VALIDATION_PORTFOLIO_HISTORY,
            period="all_time",
            min_trades=2  # Validation dataset has 5 trades
        )

        exec_metrics = result.get("executive_metrics", {})
        adv_metrics = result.get("advanced_metrics", {})

        validations = []

        # Sharpe Ratio
        validations.append({
            "metric": "sharpe_ratio",
            "expected": EXPECTED_METRICS["sharpe_ratio"],
            "actual": exec_metrics.get("sharpe_ratio", 0.0),
            "diff": abs(exec_metrics.get("sharpe_ratio", 0.0) - EXPECTED_METRICS["sharpe_ratio"]),
            "status": "pass" if abs(exec_metrics.get("sharpe_ratio", 0.0) - EXPECTED_METRICS["sharpe_ratio"]) <= TOLERANCE["sharpe_ratio"] else "fail",
            "tolerance": TOLERANCE["sharpe_ratio"],
            "formula": "(Avg Return / Std Dev) × √252",
            "method": exec_metrics.get("sharpe_method", "unknown")
        })

        # Max Drawdown Percent
        validations.append({
            "metric": "max_drawdown_percent",
            "expected": EXPECTED_METRICS["max_drawdown_percent"],
            "actual": exec_metrics.get("max_drawdown", {}).get("percent", 0.0),
            "diff": abs(exec_metrics.get("max_drawdown", {}).get("percent", 0.0) - EXPECTED_METRICS["max_drawdown_percent"]),
            "status": "pass" if abs(exec_metrics.get("max_drawdown", {}).get("percent", 0.0) - EXPECTED_METRICS["max_drawdown_percent"]) <= TOLERANCE["max_drawdown_percent"] else "fail",
            "tolerance": TOLERANCE["max_drawdown_percent"],
            "formula": "((Peak - Trough) / Peak) × 100"
        })

        # Recovery Factor
        validations.append({
            "metric": "recovery_factor",
            "expected": EXPECTED_METRICS["recovery_factor"],
            "actual": exec_metrics.get("recovery_factor", 0.0),
            "diff": abs(exec_metrics.get("recovery_factor", 0.0) - EXPECTED_METRICS["recovery_factor"]),
            "status": "pass" if abs(exec_metrics.get("recovery_factor", 0.0) - EXPECTED_METRICS["recovery_factor"]) <= TOLERANCE["recovery_factor"] else "fail",
            "tolerance": TOLERANCE["recovery_factor"],
            "formula": "Net Profit / Max Drawdown"
        })

        # Expectancy
        validations.append({
            "metric": "expectancy",
            "expected": EXPECTED_METRICS["expectancy"],
            "actual": exec_metrics.get("expectancy", 0.0),
            "diff": abs(exec_metrics.get("expectancy", 0.0) - EXPECTED_METRICS["expectancy"]),
            "status": "pass" if abs(exec_metrics.get("expectancy", 0.0) - EXPECTED_METRICS["expectancy"]) <= TOLERANCE["expectancy"] else "fail",
            "tolerance": TOLERANCE["expectancy"],
            "formula": "(Win Rate × Avg Win) + (Loss Rate × Avg Loss)"
        })

        # Profit Factor
        validations.append({
            "metric": "profit_factor",
            "expected": EXPECTED_METRICS["profit_factor"],
            "actual": exec_metrics.get("profit_factor", 0.0),
            "diff": abs(exec_metrics.get("profit_factor", 0.0) - EXPECTED_METRICS["profit_factor"]),
            "status": "pass" if abs(exec_metrics.get("profit_factor", 0.0) - EXPECTED_METRICS["profit_factor"]) <= TOLERANCE["profit_factor"] else "fail",
            "tolerance": TOLERANCE["profit_factor"],
            "formula": "Gross Profit / Gross Loss"
        })

        # Risk Reward Ratio
        validations.append({
            "metric": "risk_reward_ratio",
            "expected": EXPECTED_METRICS["risk_reward_ratio"],
            "actual": exec_metrics.get("risk_reward_ratio", 0.0),
            "diff": abs(exec_metrics.get("risk_reward_ratio", 0.0) - EXPECTED_METRICS["risk_reward_ratio"]),
            "status": "pass" if abs(exec_metrics.get("risk_reward_ratio", 0.0) - EXPECTED_METRICS["risk_reward_ratio"]) <= TOLERANCE["risk_reward_ratio"] else "fail",
            "tolerance": TOLERANCE["risk_reward_ratio"],
            "formula": "Avg Win / Avg Loss"
        })

        # Win Streak
        validations.append({
            "metric": "win_streak",
            "expected": EXPECTED_METRICS["win_streak"],
            "actual": adv_metrics.get("win_streak", 0),
            "diff": abs(adv_metrics.get("win_streak", 0) - EXPECTED_METRICS["win_streak"]),
            "status": "pass" if adv_metrics.get("win_streak", 0) == EXPECTED_METRICS["win_streak"] else "fail",
            "tolerance": TOLERANCE["win_streak"],
            "formula": "Max consecutive winning trades"
        })

        # Loss Streak
        validations.append({
            "metric": "loss_streak",
            "expected": EXPECTED_METRICS["loss_streak"],
            "actual": adv_metrics.get("loss_streak", 0),
            "diff": abs(adv_metrics.get("loss_streak", 0) - EXPECTED_METRICS["loss_streak"]),
            "status": "pass" if adv_metrics.get("loss_streak", 0) == EXPECTED_METRICS["loss_streak"] else "fail",
            "tolerance": TOLERANCE["loss_streak"],
            "formula": "Max consecutive losing trades"
        })

        # Avg Hold Winners
        validations.append({
            "metric": "avg_hold_winners",
            "expected": EXPECTED_METRICS["avg_hold_winners"],
            "actual": adv_metrics.get("avg_hold_winners", 0.0),
            "diff": abs(adv_metrics.get("avg_hold_winners", 0.0) - EXPECTED_METRICS["avg_hold_winners"]),
            "status": "pass" if abs(adv_metrics.get("avg_hold_winners", 0.0) - EXPECTED_METRICS["avg_hold_winners"]) <= TOLERANCE["avg_hold_winners"] else "fail",
            "tolerance": TOLERANCE["avg_hold_winners"],
            "formula": "Avg days held for winning trades"
        })

        # Avg Hold Losers
        validations.append({
            "metric": "avg_hold_losers",
            "expected": EXPECTED_METRICS["avg_hold_losers"],
            "actual": adv_metrics.get("avg_hold_losers", 0.0),
            "diff": abs(adv_metrics.get("avg_hold_losers", 0.0) - EXPECTED_METRICS["avg_hold_losers"]),
            "status": "pass" if abs(adv_metrics.get("avg_hold_losers", 0.0) - EXPECTED_METRICS["avg_hold_losers"]) <= TOLERANCE["avg_hold_losers"] else "fail",
            "tolerance": TOLERANCE["avg_hold_losers"],
            "formula": "Avg days held for losing trades"
        })

        # Trade Frequency
        validations.append({
            "metric": "trade_frequency",
            "expected": EXPECTED_METRICS["trade_frequency"],
            "actual": adv_metrics.get("trade_frequency", 0.0),
            "diff": abs(adv_metrics.get("trade_frequency", 0.0) - EXPECTED_METRICS["trade_frequency"]),
            "status": "pass" if abs(adv_metrics.get("trade_frequency", 0.0) - EXPECTED_METRICS["trade_frequency"]) <= TOLERANCE["trade_frequency"] else "fail",
            "tolerance": TOLERANCE["trade_frequency"],
            "formula": "Trades per week"
        })

        # Capital Efficiency
        # BLG-TECH-01: block added 2026-02-20 — was previously missing from this router,
        # causing capital_efficiency to be absent from all validation output.
        # Expected value updated to 0.22 (from 0.17) to reflect corrected GBP total_cost basis.
        validations.append({
            "metric": "capital_efficiency",
            "expected": EXPECTED_METRICS["capital_efficiency"],
            "actual": adv_metrics.get("capital_efficiency", 0.0),
            "diff": abs(adv_metrics.get("capital_efficiency", 0.0) - EXPECTED_METRICS["capital_efficiency"]),
            "status": "pass" if abs(adv_metrics.get("capital_efficiency", 0.0) - EXPECTED_METRICS["capital_efficiency"]) <= TOLERANCE["capital_efficiency"] else "fail",
            "tolerance": TOLERANCE["capital_efficiency"],
            "formula": "(Total PnL / Mean(total_cost)) × 100"
        })

        # Days Underwater
        validations.append({
            "metric": "days_underwater",
            "expected": EXPECTED_METRICS["days_underwater"],
            "actual": adv_metrics.get("days_underwater", 0),
            "diff": abs(adv_metrics.get("days_underwater", 0) - EXPECTED_METRICS["days_underwater"]),
            "status": "pass" if adv_metrics.get("days_underwater", 0) == EXPECTED_METRICS["days_underwater"] else "fail",
            "tolerance": TOLERANCE["days_underwater"],
            "formula": "Days since peak equity"
        })

        passed = sum(1 for v in validations if v["status"] == "pass")
        warned = sum(1 for v in validations if v["status"] == "warn")
        failed = sum(1 for v in validations if v["status"] == "fail")

        from datetime import datetime

        return {
            "status": "ok",
            "data": {
                "validations": validations,
                "summary": {
                    "total": len(validations),
                    "passed": passed,
                    "warned": warned,
                    "failed": failed
                },
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )
