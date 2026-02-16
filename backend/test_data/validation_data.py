"""
Validation data based on YOUR ACTUAL 5 trades.
Expected values from EXPECTED_ANALYTICS_RESULTS.md
"""

# Your actual 5 trades from /trades endpoint
VALIDATION_TRADES = [
    {
        "id": "87ad66e0-c789-4490-9399-055b580b6312",
        "ticker": "STX",
        "market": "US",
        "entry_date": "2026-01-23",
        "exit_date": "2026-02-11",
        "shares": 3.0,
        "entry_price": 345.0,
        "exit_price": 392.14,
        "pnl": 93.68,
        "pnl_percent": 12.23,
        "exit_reason": "Trailing Stop",
        "holding_days": 19,  # ✅ ADD THIS
    },
    {
        "id": "8ff40cd3-09c6-4482-b78c-a1ff864e59e6",
        "ticker": "MU",
        "market": "US",
        "entry_date": "2026-01-23",
        "exit_date": "2026-02-04",
        "shares": 3.5,
        "entry_price": 397.5,
        "exit_price": 402.84,
        "pnl": -2.33,
        "pnl_percent": -0.23,
        "exit_reason": "Manual Exit",
        "holding_days": 12,  # ✅ ADD THIS
    },
    {
        "id": "3e65ca71-305e-462d-bc22-1125014b6438",
        "ticker": "SNDK",
        "market": "US",
        "entry_date": "2026-01-23",
        "exit_date": "2026-02-04",
        "shares": 1.5,
        "entry_price": 503.9,
        "exit_price": 606.29,
        "pnl": 104.98,
        "pnl_percent": 18.76,
        "exit_reason": "Trailing Stop",
        "holding_days": 12,  # ✅ ADD THIS
    },
    {
        "id": "4d498885-4735-413f-9ecc-c2882440a338",
        "ticker": "FRES.L",
        "market": "UK",
        "entry_date": "2026-01-23",
        "exit_date": "2026-02-02",
        "shares": 27.25,
        "entry_price": 40.98,
        "exit_price": 34.5,
        "pnl": -182.16,
        "pnl_percent": -16.23,
        "exit_reason": "Manual Exit",
        "holding_days": 10,  # ✅ ADD THIS
    },
    {
        "id": "65e3e445-960a-4936-b49b-3005918c1f37",
        "ticker": "WDC",
        "market": "US",
        "entry_date": "2026-01-23",
        "exit_date": "2026-02-02",
        "shares": 5.5,
        "entry_price": 243.0,
        "exit_price": 242.67,
        "pnl": -12.23,
        "pnl_percent": -1.24,
        "exit_reason": "Manual Exit",
        "holding_days": 10,  # ✅ ADD THIS
    }
]

VALIDATION_PORTFOLIO_HISTORY = [
    {"snapshot_date": "2026-01-31", "total_value": 5133.52},
    {"snapshot_date": "2026-02-02", "total_value": 5361.88},
    {"snapshot_date": "2026-02-03", "total_value": 5444.29},  # Peak
    {"snapshot_date": "2026-02-04", "total_value": 5179.76},
    {"snapshot_date": "2026-02-05", "total_value": 5146.58},
    {"snapshot_date": "2026-02-06", "total_value": 5241.25},
    {"snapshot_date": "2026-02-07", "total_value": 5258.45},
    {"snapshot_date": "2026-02-09", "total_value": 5241.66},
    {"snapshot_date": "2026-02-10", "total_value": 5025.22},  # Trough
    {"snapshot_date": "2026-02-11", "total_value": 5204.19},
    {"snapshot_date": "2026-02-12", "total_value": 5353.38},
    {"snapshot_date": "2026-02-13", "total_value": 5285.69},  # Current
]

# Expected metrics (from your EXPECTED_ANALYTICS_RESULTS.md)
EXPECTED_METRICS = {
    "sharpe_ratio": 0.00,  # Insufficient data (need 10+ trades)
    "sharpe_method": "insufficient_data",
    "max_drawdown_percent": -7.70,
    "max_drawdown_amount": 419.07,
    "max_drawdown_date": "2026-02-10",
    "recovery_factor": 0.36,
    "expectancy": 0.39,
    "profit_factor": 1.01,
    "risk_reward_ratio": 1.51,
    "win_rate": 40.0,
    "win_streak": 2,
    "loss_streak": 3,
    "avg_hold_winners": 15.5,
    "avg_hold_losers": 10.7,
    "trade_frequency": 1.8,
    "capital_efficiency": 0.17,
    "days_underwater": 0,
}

# Tolerance levels
TOLERANCE = {
    "sharpe_ratio": 0.01,
    "max_drawdown_percent": 0.1,
    "recovery_factor": 0.05,
    "expectancy": 0.10,
    "profit_factor": 0.02,
    "risk_reward_ratio": 0.02,
    "win_rate": 0.5,
    "win_streak": 0,  # Exact
    "loss_streak": 0,  # Exact
    "avg_hold_winners": 0.5,
    "avg_hold_losers": 0.5,
    "trade_frequency": 0.2,
    "capital_efficiency": 0.05,
    "days_underwater": 0,  # Exact
}
