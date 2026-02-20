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

    BLG-TECH-01 2026-02-20:
      - Primary pass uses full dataset (35 snapshots + 12 trades) → portfolio Sharpe method
      - Second pass uses trade-only data (no snapshots) → trade Sharpe fallback method
        (Addendum 1 — both methods must be independently exercised per Decision 2)

    No request body required.
    """
    try:
        service = AnalyticsService()

        # ── Primary pass — full dataset ──────────────────────────────────────
        # 35 snapshots → portfolio method selected for Sharpe
        result = service.calculate_metrics_from_data(
            trades=VALIDATION_TRADES,
            portfolio_history=VALIDATION_PORTFOLIO_HISTORY,
            period="all_time",
            min_trades=2
        )

        exec_metrics = result.get("executive_metrics", {})
        adv_metrics = result.get("advanced_metrics", {})

        validations = []

        # Sharpe Ratio — portfolio method
        actual_sharpe = exec_metrics.get("sharpe_ratio", 0.0)
        validations.append({
            "metric": "sharpe_ratio",
            "expected": EXPECTED_METRICS["sharpe_ratio"],
            "actual": actual_sharpe,
            "diff": abs(actual_sharpe - EXPECTED_METRICS["sharpe_ratio"]),
            "status": "pass" if abs(actual_sharpe - EXPECTED_METRICS["sharpe_ratio"]) <= TOLERANCE["sharpe_ratio"] else "fail",
            "tolerance": TOLERANCE["sharpe_ratio"],
            "formula": "(Mean(daily_returns) / StdDev_SAMPLE(daily_returns)) × √252",
            "method": exec_metrics.get("sharpe_method", "unknown")
        })

        # Max Drawdown Percent
        actual_mdd = exec_metrics.get("max_drawdown", {}).get("percent", 0.0)
        validations.append({
            "metric": "max_drawdown_percent",
            "expected": EXPECTED_METRICS["max_drawdown_percent"],
            "actual": actual_mdd,
            "diff": abs(actual_mdd - EXPECTED_METRICS["max_drawdown_percent"]),
            "status": "pass" if abs(actual_mdd - EXPECTED_METRICS["max_drawdown_percent"]) <= TOLERANCE["max_drawdown_percent"] else "fail",
            "tolerance": TOLERANCE["max_drawdown_percent"],
            "formula": "((Peak - Trough) / Peak) × 100"
        })

        # Recovery Factor
        actual_rf = exec_metrics.get("recovery_factor", 0.0)
        validations.append({
            "metric": "recovery_factor",
            "expected": EXPECTED_METRICS["recovery_factor"],
            "actual": actual_rf,
            "diff": abs(actual_rf - EXPECTED_METRICS["recovery_factor"]),
            "status": "pass" if abs(actual_rf - EXPECTED_METRICS["recovery_factor"]) <= TOLERANCE["recovery_factor"] else "fail",
            "tolerance": TOLERANCE["recovery_factor"],
            "formula": "Net Profit / Max Drawdown Amount"
        })

        # Expectancy
        actual_exp = exec_metrics.get("expectancy", 0.0)
        validations.append({
            "metric": "expectancy",
            "expected": EXPECTED_METRICS["expectancy"],
            "actual": actual_exp,
            "diff": abs(actual_exp - EXPECTED_METRICS["expectancy"]),
            "status": "pass" if abs(actual_exp - EXPECTED_METRICS["expectancy"]) <= TOLERANCE["expectancy"] else "fail",
            "tolerance": TOLERANCE["expectancy"],
            "formula": "(Win Rate × Avg Win) + (Loss Rate × Avg Loss)"
        })

        # Profit Factor
        actual_pf = exec_metrics.get("profit_factor", 0.0)
        validations.append({
            "metric": "profit_factor",
            "expected": EXPECTED_METRICS["profit_factor"],
            "actual": actual_pf,
            "diff": abs(actual_pf - EXPECTED_METRICS["profit_factor"]),
            "status": "pass" if abs(actual_pf - EXPECTED_METRICS["profit_factor"]) <= TOLERANCE["profit_factor"] else "fail",
            "tolerance": TOLERANCE["profit_factor"],
            "formula": "Gross Profit / Gross Loss"
        })

        # Risk/Reward Ratio
        actual_rr = exec_metrics.get("risk_reward_ratio", 0.0)
        validations.append({
            "metric": "risk_reward_ratio",
            "expected": EXPECTED_METRICS["risk_reward_ratio"],
            "actual": actual_rr,
            "diff": abs(actual_rr - EXPECTED_METRICS["risk_reward_ratio"]),
            "status": "pass" if abs(actual_rr - EXPECTED_METRICS["risk_reward_ratio"]) <= TOLERANCE["risk_reward_ratio"] else "fail",
            "tolerance": TOLERANCE["risk_reward_ratio"],
            "formula": "Avg Win / Avg Loss"
        })

        # Win Rate
        actual_wr = result.get("summary", {}).get("win_rate", 0.0)
        validations.append({
            "metric": "win_rate",
            "expected": EXPECTED_METRICS["win_rate"],
            "actual": actual_wr,
            "diff": abs(actual_wr - EXPECTED_METRICS["win_rate"]),
            "status": "pass" if abs(actual_wr - EXPECTED_METRICS["win_rate"]) <= TOLERANCE["win_rate"] else "fail",
            "tolerance": TOLERANCE["win_rate"],
            "formula": "(Winners / Total Trades) × 100"
        })

        # Win Streak
        actual_ws = adv_metrics.get("win_streak", 0)
        validations.append({
            "metric": "win_streak",
            "expected": EXPECTED_METRICS["win_streak"],
            "actual": actual_ws,
            "diff": abs(actual_ws - EXPECTED_METRICS["win_streak"]),
            "status": "pass" if actual_ws == EXPECTED_METRICS["win_streak"] else "fail",
            "tolerance": TOLERANCE["win_streak"],
            "formula": "Max consecutive winning trades"
        })

        # Loss Streak
        actual_ls = adv_metrics.get("loss_streak", 0)
        validations.append({
            "metric": "loss_streak",
            "expected": EXPECTED_METRICS["loss_streak"],
            "actual": actual_ls,
            "diff": abs(actual_ls - EXPECTED_METRICS["loss_streak"]),
            "status": "pass" if actual_ls == EXPECTED_METRICS["loss_streak"] else "fail",
            "tolerance": TOLERANCE["loss_streak"],
            "formula": "Max consecutive losing trades"
        })

        # Avg Hold Winners
        actual_ahw = adv_metrics.get("avg_hold_winners", 0.0)
        validations.append({
            "metric": "avg_hold_winners",
            "expected": EXPECTED_METRICS["avg_hold_winners"],
            "actual": actual_ahw,
            "diff": abs(actual_ahw - EXPECTED_METRICS["avg_hold_winners"]),
            "status": "pass" if abs(actual_ahw - EXPECTED_METRICS["avg_hold_winners"]) <= TOLERANCE["avg_hold_winners"] else "fail",
            "tolerance": TOLERANCE["avg_hold_winners"],
            "formula": "Avg days held for winning trades"
        })

        # Avg Hold Losers
        actual_ahl = adv_metrics.get("avg_hold_losers", 0.0)
        validations.append({
            "metric": "avg_hold_losers",
            "expected": EXPECTED_METRICS["avg_hold_losers"],
            "actual": actual_ahl,
            "diff": abs(actual_ahl - EXPECTED_METRICS["avg_hold_losers"]),
            "status": "pass" if abs(actual_ahl - EXPECTED_METRICS["avg_hold_losers"]) <= TOLERANCE["avg_hold_losers"] else "fail",
            "tolerance": TOLERANCE["avg_hold_losers"],
            "formula": "Avg days held for losing trades"
        })

        # Trade Frequency
        actual_tf = adv_metrics.get("trade_frequency", 0.0)
        validations.append({
            "metric": "trade_frequency",
            "expected": EXPECTED_METRICS["trade_frequency"],
            "actual": actual_tf,
            "diff": abs(actual_tf - EXPECTED_METRICS["trade_frequency"]),
            "status": "pass" if abs(actual_tf - EXPECTED_METRICS["trade_frequency"]) <= TOLERANCE["trade_frequency"] else "fail",
            "tolerance": TOLERANCE["trade_frequency"],
            "formula": "Trades per week"
        })

        # Capital Efficiency — GBP basis (BLG-TECH-01 AP-07)
        actual_ce = adv_metrics.get("capital_efficiency", 0.0)
        validations.append({
            "metric": "capital_efficiency",
            "expected": EXPECTED_METRICS["capital_efficiency"],
            "actual": actual_ce,
            "diff": abs(actual_ce - EXPECTED_METRICS["capital_efficiency"]),
            "status": "pass" if abs(actual_ce - EXPECTED_METRICS["capital_efficiency"]) <= TOLERANCE["capital_efficiency"] else "fail",
            "tolerance": TOLERANCE["capital_efficiency"],
            "formula": "(Total PnL / Mean(total_cost GBP)) × 100"
        })

        # Days Underwater
        actual_du = adv_metrics.get("days_underwater", 0)
        validations.append({
            "metric": "days_underwater",
            "expected": EXPECTED_METRICS["days_underwater"],
            "actual": actual_du,
            "diff": abs(actual_du - EXPECTED_METRICS["days_underwater"]),
            "status": "pass" if actual_du == EXPECTED_METRICS["days_underwater"] else "fail",
            "tolerance": TOLERANCE["days_underwater"],
            "formula": "Max days since peak running equity (trade-sequence)"
        })

        # ── Second pass — trade-only dataset ─────────────────────────────────
        # portfolio_history=[] forces trade-based Sharpe fallback
        # Exercises the fallback code path independently (Decision 2 / Addendum 1)
        result_trade_only = service.calculate_metrics_from_data(
            trades=VALIDATION_TRADES,
            portfolio_history=[],
            period="all_time",
            min_trades=2
        )

        exec_trade_only = result_trade_only.get("executive_metrics", {})
        actual_sharpe_trade = exec_trade_only.get("sharpe_ratio", 0.0)
        actual_sharpe_trade_method = exec_trade_only.get("sharpe_method", "unknown")

        validations.append({
            "metric": "sharpe_ratio_trade_method",
            "expected": EXPECTED_METRICS["sharpe_ratio_trade"],
            "actual": actual_sharpe_trade,
            "diff": abs(actual_sharpe_trade - EXPECTED_METRICS["sharpe_ratio_trade"]),
            "status": "pass" if abs(actual_sharpe_trade - EXPECTED_METRICS["sharpe_ratio_trade"]) <= TOLERANCE["sharpe_ratio"] else "fail",
            "tolerance": TOLERANCE["sharpe_ratio"],
            "formula": "Mean(Ann Returns) / StdDev_SAMPLE(Ann Returns)",
            "method": actual_sharpe_trade_method,
            "note": "Second pass — trade fallback path; portfolio_history=[] to force trade method"
        })

        # ── Summary ───────────────────────────────────────────────────────────
        passed = sum(1 for v in validations if v["status"] == "pass")
        warned = sum(1 for v in validations if v["status"] == "warn")
        failed = sum(1 for v in validations if v["status"] == "fail")

        from datetime import datetime as dt
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
                "timestamp": dt.utcnow().isoformat() + "Z"
            }
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )
