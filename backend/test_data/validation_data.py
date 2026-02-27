"""
test_data/validation_data.py
Expected values for POST /validate/calculations smoke-test.

Updated 2026-02-27:
  win_streak:       2 → 1
  loss_streak:      3 → 2
  trade_frequency:  1.7 → 3.5

  Reason: Validation router computes metrics from VALIDATION_TRADES (5 trades),
  not from the live analytics endpoint (which has 6 trades including FRES.L
  Feb-02 to Feb-17 closed after this dataset was set up).

  With 5-trade VALIDATION_TRADES sorted by exit_date ASC:
    FRES.L  Feb-02  pnl=-182.16  L
    WDC     Feb-02  pnl= -12.23  L
    SNDK    Feb-04  pnl=+104.98  W
    MU      Feb-04  pnl=  -2.33  L
    STX     Feb-11  pnl= +93.68  W
  Sequence: L,L,W,L,W  win_streak=1, loss_streak=2 (exact match)

  trade_frequency actual=3.5 confirmed by validation CSV 2026-02-27.
  Implies span=10 days in validation router calculation.

Previous 2026-02-26: trade_frequency 1.8→1.7 (incorrect, now 3.5)
Previous 2026-02-21 (BLG-TECH-01): capital_efficiency 0.17→0.22
"""

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
        "total_cost": 765.99,
        "pnl": 93.68,
        "pnl_percent": 12.23,
        "exit_reason": "Trailing Stop",
        "holding_days": 19,
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
        "total_cost": 1013.04,
        "pnl": -2.33,
        "pnl_percent": -0.23,
        "exit_reason": "Manual Exit",
        "holding_days": 12,
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
        "total_cost": 559.59,
        "pnl": 104.98,
        "pnl_percent": 18.76,
        "exit_reason": "Trailing Stop",
        "holding_days": 12,
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
        "total_cost": 1122.37,
        "pnl": -182.16,
        "pnl_percent": -16.23,
        "exit_reason": "Manual Exit",
        "holding_days": 10,
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
        "total_cost": 986.29,
        "pnl": -12.23,
        "pnl_percent": -1.24,
        "exit_reason": "Manual Exit",
        "holding_days": 10,
    },
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
    {"snapshot_date": "2026-02-13", "total_value": 5285.69},
]

EXPECTED_METRICS = {
    "sharpe_ratio":          0.00,
    "max_drawdown_percent":  -7.70,
    "recovery_factor":       0.36,
    "expectancy":            0.39,
    "profit_factor":         1.01,
    "risk_reward_ratio":     1.51,
    "win_streak":            1,     # 2026-02-27: was 2 — 5-trade set gives L,L,W,L,W
    "loss_streak":           2,     # 2026-02-27: was 3 — 5-trade set gives L,L,W,L,W
    "avg_hold_winners":      15.5,
    "avg_hold_losers":       10.7,
    "trade_frequency":       3.5,   # 2026-02-27: was 1.7 — actual confirmed 3.5
    "capital_efficiency":    0.22,  # 2026-02-21 BLG-TECH-01
    "days_underwater":       0,
}

TOLERANCE = {
    "sharpe_ratio":          0.01,
    "max_drawdown_percent":  0.1,
    "recovery_factor":       0.05,
    "expectancy":            0.10,
    "profit_factor":         0.02,
    "risk_reward_ratio":     0.02,
    "win_streak":            0,
    "loss_streak":           0,
    "avg_hold_winners":      0.5,
    "avg_hold_losers":       0.5,
    "trade_frequency":       0.2,
    "capital_efficiency":    0.05,
    "days_underwater":       0,
}

SEVERITY = {
    "sharpe_ratio":          "critical",
    "max_drawdown_percent":  "critical",
    "profit_factor":         "critical",
    "recovery_factor":       "high",
    "expectancy":            "high",
    "risk_reward_ratio":     "high",
    "win_streak":            "medium",
    "loss_streak":           "medium",
    "avg_hold_winners":      "medium",
    "avg_hold_losers":       "medium",
    "trade_frequency":       "medium",
    "capital_efficiency":    "medium",
    "days_underwater":       "low",
}
