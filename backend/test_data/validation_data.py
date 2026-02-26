"""
test_data/validation_data.py
Expected values for POST /validate/calculations smoke-test.

Updated 2026-02-26:
  trade_frequency: 1.8 → 1.7
    Reason: Data now has 6 trades over 25-day span (Jan 23 – Feb 17).
    Formula: (6 / 25) × 7 = 1.68 → rounds to 1.7.
    Previous expected value of 1.8 was stale (used older trade set).
    Tolerance ±0.2 so this was technically still passing, but corrected
    for accuracy.

  win_streak: 2, loss_streak: 3 — unchanged (still correct).
    Sequence by exit_date ASC: L,L,L,W,W,L → max_win=2, max_loss=3.
    Note: BLG-TECH-08 fix (ORDER BY ASC) was required to compute these
    correctly from analytics_service.py. Prior to that fix the query
    returned trades DESC, causing off-by-one streak results.

Previous update 2026-02-21 (BLG-TECH-01):
  capital_efficiency: 0.17 → 0.22
    Reason: Cost basis corrected to Mean(total_cost) GBP from trade_history.
"""

# ---------------------------------------------------------------------------
# Expected values — compared against GET /analytics/metrics response
# ---------------------------------------------------------------------------

EXPECTED_METRICS = {
    "sharpe_ratio":          0.00,
    "max_drawdown_percent":  -7.70,
    "recovery_factor":       0.36,
    "expectancy":            0.39,
    "profit_factor":         1.01,
    "risk_reward_ratio":     1.51,
    "win_streak":            2,
    "loss_streak":           3,
    "avg_hold_winners":      15.5,
    "avg_hold_losers":       10.7,
    "trade_frequency":       1.7,   # Updated 2026-02-26: was 1.8
    "capital_efficiency":    0.22,  # Updated 2026-02-21 (BLG-TECH-01)
    "days_underwater":       0,
}

# ---------------------------------------------------------------------------
# Tolerances — per analytics_endpoints.md v1.8.1
# ---------------------------------------------------------------------------

TOLERANCE = {
    "sharpe_ratio":          0.01,
    "max_drawdown_percent":  0.1,
    "recovery_factor":       0.05,
    "expectancy":            0.10,
    "profit_factor":         0.02,
    "risk_reward_ratio":     0.02,
    "win_streak":            0,     # exact match
    "loss_streak":           0,     # exact match
    "avg_hold_winners":      0.5,
    "avg_hold_losers":       0.5,
    "trade_frequency":       0.2,
    "capital_efficiency":    0.05,
    "days_underwater":       0,     # exact match
}

# ---------------------------------------------------------------------------
# Severity tiers — per analytics_endpoints.md v1.8.1 §POST /validate/calculations
# ---------------------------------------------------------------------------

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
