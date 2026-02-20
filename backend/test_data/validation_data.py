"""
Validation Data — BLG-TECH-01 Expanded Dataset
================================================
Updated:              2026-02-20
Updated by:           Engineering (AP-05)
Decisions ref:        docs/product/decisions/blg-tech-01-sharpe-fix-capital-efficiency.md
Canonical Owner:      Sign-off granted 2026-02-20
Workings ref:         docs/product/decisions/blg-tech-01-canonical-owner-verification.md

Changes from previous version (5-trade / population variance dataset):
  - VALIDATION_TRADES expanded from 5 → 12 trades
      Minimum 10 required to exercise trade-based Sharpe fallback (Decision 1 / Decision 2)
  - total_cost (GBP) field added to all trade records (Decision 4)
      FRES.L confirmed at £1,116.70 (£40.98 × 27.25 shares — pounds, not pence; confirmed 2026-02-20)
  - VALIDATION_PORTFOLIO_HISTORY expanded from 13 → 35 snapshots (Decision 1)
      Minimum 30 required to exercise portfolio-based Sharpe
  - EXPECTED_METRICS fully updated:
      sharpe_ratio:         0.00 (insufficient_data)  →  4.14  (portfolio, sample variance n−1)
      sharpe_ratio_trade:   new                        →  0.16  (trade fallback, sample variance n−1)
      capital_efficiency:   0.17 (wrong basis)         →  16.18 (GBP basis, FRES.L corrected)

FX Rate Assumption — synthetic US trades only (Decision 5):
  Rate:    1 USD = 0.80 GBP (illustrative synthetic rate — not a live rate)
  Method:  total_cost (GBP) = entry_price (USD) × shares × 0.80  for US market trades
           total_cost (GBP) = entry_price (GBP) × shares          for UK market trades
  Scope:   this test dataset only — not used anywhere else in the system
"""

# ============================================================
# VALIDATION TRADES — 12 closed trades
#
# Trades 1–5:  original real trades; total_cost field added
# Trades 6–12: synthetic trades added to satisfy 10-trade minimum
#              for trade-based Sharpe fallback validation
# ============================================================

VALIDATION_TRADES = [

    # ── Original real trades ────────────────────────────────────────────────

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
        "holding_days": 19,
        "total_cost": 828.00,       # 3.0 × $345.00 × 0.80 USD→GBP
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
        "holding_days": 12,
        "total_cost": 1113.00,      # 3.5 × $397.50 × 0.80 USD→GBP
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
        "holding_days": 12,
        "total_cost": 604.68,       # 1.5 × $503.90 × 0.80 USD→GBP
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
        "holding_days": 10,
        "total_cost": 1116.70,      # 27.25 × £40.98 — entry_price in pounds (confirmed 2026-02-20)
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
        "holding_days": 10,
        "total_cost": 1069.20,      # 5.5 × $243.00 × 0.80 USD→GBP
    },

    # ── Synthetic trades — BLG-TECH-01 dataset expansion ───────────────────
    # Purpose: satisfy 10-trade minimum for trade-based Sharpe fallback
    # FX:      1 USD = 0.80 GBP (synthetic rate — see module docstring)

    {
        "id": "syn-001",
        "ticker": "AAPL",
        "market": "US",
        "entry_date": "2026-01-05",
        "exit_date": "2026-01-18",
        "shares": 4.0,
        "entry_price": 230.0,
        "exit_price": 245.50,
        "pnl": 49.60,
        "pnl_percent": 6.74,
        "exit_reason": "Trailing Stop",
        "holding_days": 13,
        "total_cost": 736.00,       # 4.0 × $230.00 × 0.80
    },
    {
        "id": "syn-002",
        "ticker": "MSFT",
        "market": "US",
        "entry_date": "2026-01-06",
        "exit_date": "2026-01-20",
        "shares": 2.0,
        "entry_price": 415.0,
        "exit_price": 408.00,
        "pnl": -11.20,
        "pnl_percent": -1.69,
        "exit_reason": "Stop Loss Hit",
        "holding_days": 14,
        "total_cost": 664.00,       # 2.0 × $415.00 × 0.80
    },
    {
        "id": "syn-003",
        "ticker": "NVDA",
        "market": "US",
        "entry_date": "2026-01-07",
        "exit_date": "2026-01-22",
        "shares": 1.0,
        "entry_price": 780.0,
        "exit_price": 835.00,
        "pnl": 44.00,
        "pnl_percent": 7.05,
        "exit_reason": "Trailing Stop",
        "holding_days": 15,
        "total_cost": 624.00,       # 1.0 × $780.00 × 0.80
    },
    {
        "id": "syn-004",
        "ticker": "AMZN",
        "market": "US",
        "entry_date": "2026-01-08",
        "exit_date": "2026-01-19",
        "shares": 3.0,
        "entry_price": 220.0,
        "exit_price": 214.50,
        "pnl": -13.20,
        "pnl_percent": -2.50,
        "exit_reason": "Stop Loss Hit",
        "holding_days": 11,
        "total_cost": 528.00,       # 3.0 × $220.00 × 0.80
    },
    {
        "id": "syn-005",
        "ticker": "TSLA",
        "market": "US",
        "entry_date": "2026-01-09",
        "exit_date": "2026-01-24",
        "shares": 2.0,
        "entry_price": 380.0,
        "exit_price": 395.00,
        "pnl": 24.00,
        "pnl_percent": 3.95,
        "exit_reason": "Target Reached",
        "holding_days": 15,
        "total_cost": 608.00,       # 2.0 × $380.00 × 0.80
    },
    {
        "id": "syn-006",
        "ticker": "GOOGL",
        "market": "US",
        "entry_date": "2026-01-10",
        "exit_date": "2026-01-21",
        "shares": 5.0,
        "entry_price": 185.0,
        "exit_price": 179.50,
        "pnl": -22.00,
        "pnl_percent": -2.97,
        "exit_reason": "Stop Loss Hit",
        "holding_days": 11,
        "total_cost": 740.00,       # 5.0 × $185.00 × 0.80
    },
    {
        "id": "syn-007",
        "ticker": "META",
        "market": "US",
        "entry_date": "2026-01-12",
        "exit_date": "2026-01-27",
        "shares": 2.0,
        "entry_price": 590.0,
        "exit_price": 625.00,
        "pnl": 56.00,
        "pnl_percent": 5.93,
        "exit_reason": "Trailing Stop",
        "holding_days": 15,
        "total_cost": 944.00,       # 2.0 × $590.00 × 0.80
    },
]


# ============================================================
# PORTFOLIO HISTORY — 35 daily snapshots
#
# Date range:   2026-01-20 → 2026-02-23
# Peak:         £5,360.00 on 2026-02-01
# Trough:       £5,075.00 on 2026-02-10  ← max drawdown date
# Max drawdown: £285.00 / -5.32%
# First value:  £5,100.00
# Last value:   £5,330.00
# Period P&L:   £230.00
# Recovery:     230 / 285 = 0.81
# ============================================================

VALIDATION_PORTFOLIO_HISTORY = [
    {"snapshot_date": "2026-01-20", "total_value": 5100.00},
    {"snapshot_date": "2026-01-21", "total_value": 5145.00},
    {"snapshot_date": "2026-01-22", "total_value": 5160.00},
    {"snapshot_date": "2026-01-23", "total_value": 5200.00},
    {"snapshot_date": "2026-01-24", "total_value": 5185.00},
    {"snapshot_date": "2026-01-25", "total_value": 5220.00},
    {"snapshot_date": "2026-01-26", "total_value": 5250.00},
    {"snapshot_date": "2026-01-27", "total_value": 5270.00},
    {"snapshot_date": "2026-01-28", "total_value": 5295.00},
    {"snapshot_date": "2026-01-29", "total_value": 5310.00},
    {"snapshot_date": "2026-01-30", "total_value": 5330.00},
    {"snapshot_date": "2026-01-31", "total_value": 5350.00},
    {"snapshot_date": "2026-02-01", "total_value": 5360.00},  # ← Peak
    {"snapshot_date": "2026-02-02", "total_value": 5340.00},
    {"snapshot_date": "2026-02-03", "total_value": 5300.00},
    {"snapshot_date": "2026-02-04", "total_value": 5260.00},
    {"snapshot_date": "2026-02-05", "total_value": 5220.00},
    {"snapshot_date": "2026-02-06", "total_value": 5180.00},
    {"snapshot_date": "2026-02-07", "total_value": 5140.00},
    {"snapshot_date": "2026-02-08", "total_value": 5110.00},
    {"snapshot_date": "2026-02-09", "total_value": 5090.00},
    {"snapshot_date": "2026-02-10", "total_value": 5075.00},  # ← Trough / max drawdown date
    {"snapshot_date": "2026-02-11", "total_value": 5100.00},
    {"snapshot_date": "2026-02-12", "total_value": 5130.00},
    {"snapshot_date": "2026-02-13", "total_value": 5160.00},
    {"snapshot_date": "2026-02-14", "total_value": 5195.00},
    {"snapshot_date": "2026-02-15", "total_value": 5220.00},
    {"snapshot_date": "2026-02-16", "total_value": 5240.00},
    {"snapshot_date": "2026-02-17", "total_value": 5255.00},
    {"snapshot_date": "2026-02-18", "total_value": 5270.00},
    {"snapshot_date": "2026-02-19", "total_value": 5285.00},
    {"snapshot_date": "2026-02-20", "total_value": 5295.00},
    {"snapshot_date": "2026-02-21", "total_value": 5310.00},
    {"snapshot_date": "2026-02-22", "total_value": 5320.00},
    {"snapshot_date": "2026-02-23", "total_value": 5330.00},
]


# ============================================================
# EXPECTED METRICS
#
# Independently calculated:  2026-02-20
# Canonical formulas from:   metrics_definitions.md v1.5.7
# Verified and signed off:   Canonical Owner, 2026-02-20
# Full workings in:          blg-tech-01-canonical-owner-verification.md
#
# Key changes from previous dataset (5 trades, population variance):
#   sharpe_ratio:         0.00 (insufficient_data)  →  4.14  (portfolio method, n−1)
#   sharpe_ratio_trade:   n/a                        →  0.16  (trade method, n−1) — new key
#   capital_efficiency:   0.17 (wrong GBP basis)    →  16.18 (correct GBP basis)
# ============================================================

EXPECTED_METRICS = {

    # ── Sharpe — portfolio method (primary) ─────────────────────────────────
    # 35 snapshots → portfolio method selected (≥30 required, preferred per spec)
    # n=34 daily returns | mean=0.1310% | sample_std (n−1=33)=0.5024
    # Sharpe = (0.1310 / 0.5024) × √252 = 4.14
    "sharpe_ratio":             4.14,
    "sharpe_method":            "portfolio",

    # ── Sharpe — trade method (second-pass validation in validation.py) ─────
    # Exercised by running calculate_metrics_from_data with portfolio_history=[]
    # n=12 trades | mean ann return=30.870% | sample_std (n−1=11)=188.92
    # Sharpe = 30.870 / 188.92 = 0.16
    "sharpe_ratio_trade":       0.16,

    # ── Max Drawdown ─────────────────────────────────────────────────────────
    # Peak £5,360 on 2026-02-01 → Trough £5,075 on 2026-02-10
    # amount = 5360 − 5075 = £285.00 | percent = 285/5360 × 100 = 5.32%
    "max_drawdown_percent":     -5.32,
    "max_drawdown_amount":      285.00,
    "max_drawdown_date":        "2026-02-10",

    # ── Recovery Factor ──────────────────────────────────────────────────────
    # period_profit = 5330 − 5100 = £230 | 230 / 285 = 0.807 → 0.81
    "recovery_factor":          0.81,

    # ── Trade performance metrics ────────────────────────────────────────────
    # 6 winners / 12 trades
    "win_rate":                 50.0,

    # avg_win=(93.68+104.98+49.60+44.00+24.00+56.00)/6=62.04
    # avg_loss=(-2.33-182.16-12.23-11.20-13.20-22.00)/6=-40.52
    # expectancy=(0.5×62.04)+(0.5×−40.52)=10.76
    "expectancy":               10.76,

    # gross_profit=372.26 | gross_loss=242.12 | 372.26/242.12=1.537→1.53
    "profit_factor":            1.53,

    # avg_win/|avg_loss|=62.04/40.52=1.531→1.53
    "risk_reward_ratio":        1.53,

    # ── Advanced metrics ─────────────────────────────────────────────────────
    "win_streak":               3,      # exact — max consecutive winners by exit_date
    "loss_streak":              3,      # exact — max consecutive losers by exit_date

    # winners: STX(19), SNDK(12), AAPL(13), NVDA(15), TSLA(15), META(15) → mean=14.83→14.8
    "avg_hold_winners":         14.8,

    # losers: MU(12), FRES.L(10), WDC(10), MSFT(14), AMZN(11), GOOGL(11) → mean=11.33→11.3
    "avg_hold_losers":          11.3,

    # 12 trades over 37 days (2026-01-05 to 2026-02-11) → 12/37×7=2.27
    "trade_frequency":          2.27,

    # Capital efficiency — GBP basis (canonical fix):
    # total_pnl=£129.14 | sum(total_cost)=£9,575.58 | mean=£797.965
    # (129.14 / 797.965) × 100 = 16.18%
    # FRES.L total_cost=£1,116.70 confirmed by Canonical Owner 2026-02-20
    "capital_efficiency":       16.18,

    # Trade-sequence method: max days from peak running equity to subsequent trade exit = 8
    "days_underwater":          8,      # exact
}


# ============================================================
# TOLERANCE — unchanged from previous version
# ============================================================

TOLERANCE = {
    "sharpe_ratio":             0.01,
    "max_drawdown_percent":     0.1,
    "recovery_factor":          0.05,
    "expectancy":               0.10,
    "profit_factor":            0.02,
    "risk_reward_ratio":        0.02,
    "win_rate":                 0.5,
    "win_streak":               0,      # exact
    "loss_streak":              0,      # exact
    "avg_hold_winners":         0.5,
    "avg_hold_losers":          0.5,
    "trade_frequency":          0.2,
    "capital_efficiency":       0.05,
    "days_underwater":          0,      # exact
}
