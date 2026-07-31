"""
ST-12 (BLG-QA-121, EPIC-03, v8.0) — regression tests for
backend/test_data/generate_synthetic_trade_history.py.

Confirms the generator satisfies its stated acceptance criteria:
  - Produces realistic (non-production) trade-history data satisfying the
    SI-02 (docs/qa/si02_playwright_predesign.md) and Setup Quality Score
    (docs/specs/data_model/trade_plan_schema_audit_v4.6.md §5.2) gate
    thresholds — both require >= 20 closed trades.
  - Every generated record is clearly labelled as synthetic/test-only.
  - Output is deterministic (safe for repeatable test fixtures).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend", "test_data"))

from generate_synthetic_trade_history import (  # noqa: E402
    generate_synthetic_trades,
    SI02_MINIMUM_REQUIRED_TRADES,
    SQS_GATE_MINIMUM_CLOSED_TRADES,
    SYNTHETIC_TAG,
    _looks_like_production,
)


def test_default_count_satisfies_both_gate_thresholds():
    trades = generate_synthetic_trades()
    assert len(trades) >= SI02_MINIMUM_REQUIRED_TRADES
    assert len(trades) >= SQS_GATE_MINIMUM_CLOSED_TRADES


def test_every_trade_is_labelled_synthetic():
    trades = generate_synthetic_trades()
    for trade in trades:
        assert SYNTHETIC_TAG in trade["entry_note"]
        assert SYNTHETIC_TAG in trade["exit_note"]


def test_generation_is_deterministic():
    first = generate_synthetic_trades(count=20, seed=42)
    second = generate_synthetic_trades(count=20, seed=42)
    assert first == second


def test_different_seeds_produce_different_output():
    a = generate_synthetic_trades(count=20, seed=1)
    b = generate_synthetic_trades(count=20, seed=2)
    assert a != b


def test_trade_shape_matches_position_and_exit_api_contract():
    trades = generate_synthetic_trades(count=1)
    trade = trades[0]
    required_fields = {
        "ticker", "market", "entry_date", "shares", "entry_price", "stop_price",
        "entry_note", "exit_date", "exit_price", "exit_reason", "exit_note",
    }
    assert required_fields.issubset(trade.keys())


def test_long_only_stop_below_entry():
    # Backend enforces long-only positions — stop_price must sit below entry_price.
    trades = generate_synthetic_trades(count=25)
    for trade in trades:
        assert trade["stop_price"] < trade["entry_price"]


def test_win_and_loss_outcomes_both_present():
    # A realistic gate-satisfying data set should not be all-winners or all-losers.
    trades = generate_synthetic_trades(count=25)
    wins = sum(1 for t in trades if t["exit_price"] > t["entry_price"])
    losses = sum(1 for t in trades if t["exit_price"] < t["entry_price"])
    assert wins > 0
    assert losses > 0


def test_rejects_count_below_one():
    import pytest
    with pytest.raises(ValueError):
        generate_synthetic_trades(count=0)


def test_production_url_guard():
    # Same heuristic as scripts/reset_staging_db.sh's production guard:
    # trigger substrings are "production" and "/prod".
    assert _looks_like_production("https://trading-assistant-production.onrender.com") is True
    assert _looks_like_production("https://example.com/prod/api") is True
    assert _looks_like_production("https://trading-assistant-staging.onrender.com") is False
    assert _looks_like_production("https://trading-assistant-api-pr-42.onrender.com") is False
