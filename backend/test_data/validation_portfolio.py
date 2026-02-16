"""
Test portfolio with known expected metrics for validation.
This is the single source of truth for validation checks.
"""

# Test trades with predictable outcomes
TEST_TRADES = [
    {
        "ticker": "AAPL",
        "market": "US",
        "entry_date": "2026-01-01",
        "exit_date": "2026-01-15",
        "shares": 10,
        "entry_price": 180.00,
        "exit_price": 190.00,
        "pnl": 100.00,
        "pnl_percent": 5.56,
        "exit_reason": "Target Reached",
    },
    {
        "ticker": "MSFT",
        "market": "US",
        "entry_date": "2026-01-05",
        "exit_date": "2026-01-20",
        "shares": 5,
        "entry_price": 380.00,
        "exit_price": 370.00,
        "pnl": -50.00,
        "pnl_percent": -2.63,
        "exit_reason": "Stop Loss Hit",
    },
    {
        "ticker": "GOOGL",
        "market": "US",
        "entry_date": "2026-01-10",
        "exit_date": "2026-01-25",
        "shares": 8,
        "entry_price": 140.00,
        "exit_price": 150.00,
        "pnl": 80.00,
        "pnl_percent": 5.71,
        "exit_reason": "Target Reached",
    },
    {
        "ticker": "TSLA",
        "market": "US",
        "entry_date": "2026-01-12",
        "exit_date": "2026-01-22",
        "shares": 6,
        "entry_price": 210.00,
        "exit_price": 200.00,
        "pnl": -60.00,
        "pnl_percent": -4.76,
        "exit_reason": "Stop Loss Hit",
    },
    {
        "ticker": "NVDA",
        "market": "US",
        "entry_date": "2026-01-15",
        "exit_date": "2026-01-30",
        "shares": 4,
        "entry_price": 500.00,
        "exit_price": 540.00,
        "pnl": 160.00,
        "pnl_percent": 8.00,
        "exit_reason": "Target Reached",
    },
    # Add more trades to reach 15+ for reliable Sharpe
]

# Portfolio snapshots (need 30+ for portfolio-based Sharpe)
TEST_PORTFOLIO_HISTORY = [
    {
        "snapshot_date": "2026-01-01",
        "total_value": 10000.00,
        "cash_balance": 2000.00,
        "positions_value": 8000.00,
        "total_pnl": 0.00,
        "position_count": 5,
    },
    {
        "snapshot_date": "2026-01-02",
        "total_value": 10100.00,
        "cash_balance": 2000.00,
        "positions_value": 8100.00,
        "total_pnl": 100.00,
        "position_count": 5,
    },
    # Add 28+ more snapshots for valid Sharpe calculation
    # Each day from 2026-01-01 to 2026-02-15 (45 days)
]

# Pre-calculated expected metrics (calculate these manually first!)
EXPECTED_METRICS = {
    "sharpe_ratio": 1.23,  # From portfolio history
    "max_drawdown_percent": -8.5,  # Peak to trough
    "max_drawdown_amount": 850.00,
    "recovery_factor": 1.5,
    "expectancy": 45.20,  # Per trade
    "profit_factor": 2.45,
    "risk_reward_ratio": 1.8,
    "win_rate": 60.0,  # 3 winners, 2 losers
    "win_streak": 2,
    "loss_streak": 1,
    "avg_hold_winners": 15.0,  # Days
    "avg_hold_losers": 12.5,  # Days
    "time_underwater": 0,  # Currently at peak
}

# Tolerance levels for each metric
TOLERANCE_CONFIG = {
    "sharpe_ratio": 0.01,  # ±0.01
    "max_drawdown_percent": 0.1,  # ±0.1%
    "expectancy": 0.10,  # ±£0.10
    "profit_factor": 0.02,  # ±0.02
    "risk_reward_ratio": 0.02,  # ±0.02
    "win_rate": 0.5,  # ±0.5%
    "win_streak": 0,  # Exact match
    "loss_streak": 0,  # Exact match
    "avg_hold_winners": 0.5,  # ±0.5 days
    "avg_hold_losers": 0.5,  # ±0.5 days
    "time_underwater": 0,  # Exact match
}
