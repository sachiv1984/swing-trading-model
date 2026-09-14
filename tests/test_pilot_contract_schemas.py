"""
Contract Schema Tests — ST-11 (EPIC-11, v7.8, RISK-03) pilot,
extended ST-06 (BLG-QA-85, EPIC-02, v9.3).

Lightweight schema-contract tests, now covering 5 representative endpoints:
GET /positions, GET /trades, GET /portfolio (original ST-11 pilot, schema
sourced from docs/specs/api_contracts/*.md), plus GET /cash/summary and
GET /signals (ST-06 extension, schema sourced directly from
docs/reference/openapi.yaml's #/components/schemas, per ST-06's specific
"openapi.yaml vs actual route behaviour" acceptance criterion).

Distinct from the existing status-code/envelope smoke tests in
test_api_contracts.py, this file validates that every field documented in
the relevant contract source is actually present on a realistic (non-empty)
response, with the documented type. This catches "field silently
removed/renamed" contract drift that an empty-list smoke test cannot — an
empty list has no fields to check.

Approach documented for extending to further endpoints:
docs/testing/pilot_contract_test_approach.md (ST-06 update: now reflects 5
endpoints covered, 2 of them openapi.yaml-sourced, and records the drift
found/fixed by this extension).

No new dependency added — plain dict/type assertions, consistent with this
repo's existing lint-style tests (e.g. test_lint_api_contract_headings.py),
not a jsonschema library.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from unittest.mock import patch  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Schema helper
# ---------------------------------------------------------------------------

def assert_schema(obj: dict, schema: dict, context: str) -> None:
    """
    Assert every field in `schema` (name -> allowed type or tuple of types)
    is present on `obj` with a value of an allowed type. Does NOT fail on
    extra/undocumented fields on `obj` -- catching removed/renamed fields is
    this pilot's scope, matching the OpenAPI Drift Detection gate's own
    philosophy (docs/specs/api_contracts silent-fail case, CLAUDE.md §2).
    """
    for field, allowed_types in schema.items():
        assert field in obj, f"{context}: missing documented field {field!r}"
        assert isinstance(obj[field], allowed_types), (
            f"{context}: field {field!r} = {obj[field]!r} "
            f"(type {type(obj[field]).__name__}) does not match documented "
            f"type(s) {allowed_types}"
        )


NUM = (int, float)
NUM_OR_NONE = (int, float, type(None))
STR_OR_NONE = (str, type(None))


# ---------------------------------------------------------------------------
# GET /positions  (docs/specs/api_contracts/position_endpoints.md)
# ---------------------------------------------------------------------------

# Schema per position object per position_endpoints.md's `data` schema
# (array) JSON example + Field notes table.
POSITION_SCHEMA = {
    "id": str,
    "ticker": str,
    "market": str,
    "entry_date": str,
    "entry_price": NUM,
    "shares": NUM,
    "current_price": NUM,
    "current_price_native": NUM,
    "stop_price": NUM,
    "stop_price_native": NUM,
    "initial_stop": NUM,
    "pnl": NUM,
    "pnl_percent": NUM,
    "holding_days": int,
    "status": str,
    "grace_period": bool,
    "display_status": str,
    "grace_days_remaining": (int, type(None)),
    "atr_value": NUM,
    "fx_rate": NUM,
    "live_fx_rate": NUM,
    "current_trailing_stop": NUM,
    "risk_off_exit": bool,
    "entry_note": STR_OR_NONE,
    "exit_note": STR_OR_NONE,
    "tags": list,
    "last_reviewed_at": STR_OR_NONE,
}

MOCK_POSITION_FULL = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "ticker": "NVDA",
    "market": "US",
    "entry_date": "2026-02-01",
    "entry_price": 622.00,
    "shares": 10.5,
    "current_price": 623.00,
    "current_price_native": 850.00,
    "stop_price": 607.50,
    "stop_price_native": 829.00,
    "initial_stop": 545.00,
    "pnl": 2394.00,
    "pnl_percent": 3.7,
    "holding_days": 14,
    "status": "open",
    "grace_period": False,
    "display_status": "PROFITABLE",
    "grace_days_remaining": None,
    "atr_value": 15.32,
    "fx_rate": 1.3642,
    "live_fx_rate": 1.3650,
    "current_trailing_stop": 560.50,
    "risk_off_exit": False,
    "entry_note": "Breakout above $800 resistance",
    "exit_note": None,
    "tags": ["momentum", "breakout"],
    "last_reviewed_at": "2026-07-01T09:00:00+00:00",
}

# get_positions_with_prices()'s output is merged, per-position, with
# get_lifecycle_fields_for_position() (backend/main.py get_positions_endpoint,
# backend/services/position_lifecycle_service.py) before being returned.
# These 3 fields are real response fields but are NOT documented in
# position_endpoints.md's GET /positions contract -- observed during this
# pilot, not asserted against here (out of scope for a missing-field check;
# see docs/testing/pilot_contract_test_approach.md for how a future cycle
# could extend this pilot to also catch undocumented-extra-field drift).
MOCK_LIFECYCLE_FIELDS = {
    "position_state": "ESTABLISHED",
    "state_entered_at": "2026-02-01T00:00:00",
    "days_in_state": 14,
}


class TestPositionsContractSchema:

    @patch("main.get_lifecycle_fields_for_position", return_value=MOCK_LIFECYCLE_FIELDS)
    @patch("main.get_positions_with_prices", return_value=[dict(MOCK_POSITION_FULL)])
    def test_get_positions_matches_documented_schema(self, *_):
        r = CLIENT.get("/positions")
        assert r.status_code == 200
        body = r.json()

        # Documented as using "the standard success envelope from
        # conventions.md" (position_endpoints.md GET /positions, Response
        # (200) section) -- but the real handler (backend/main.py
        # get_positions_endpoint) `return`s the list directly, with no
        # {"status": "ok", "data": ...} wrapper. This is a genuine, existing
        # contract/doc mismatch (already implicitly known -- see
        # test_api_contracts.py::TestPositionEndpoints's own comment),
        # re-confirmed here by this pilot. Asserting REALITY, not the
        # doc's envelope claim, since a contract test's job is to catch
        # drift against actual behaviour.
        assert isinstance(body, list), (
            "GET /positions does not return a raw list — either the "
            "implementation changed to add an envelope (update this test) "
            "or this assertion needs revisiting; position_endpoints.md's "
            "'standard success envelope' claim was already known-stale for "
            "this endpoint before this pilot."
        )
        assert len(body) == 1
        assert_schema(body[0], POSITION_SCHEMA, "GET /positions[0]")


# ---------------------------------------------------------------------------
# GET /trades  (docs/specs/api_contracts/trade_endpoints.md)
# ---------------------------------------------------------------------------

TRADE_RECORD_SCHEMA = {
    "id": str,
    "ticker": str,
    "market": str,
    "entry_date": str,
    "exit_date": str,
    "shares": NUM,
    "entry_price": NUM,
    "exit_price": NUM,
    "fill_price": NUM_OR_NONE,
    "slippage_pct": NUM_OR_NONE,
    "fee_drag_pct": NUM_OR_NONE,
    "pnl": NUM,
    "pnl_pct": NUM,
    "pnl_percent": NUM,
    "holding_days": (int, type(None)),
    "exit_reason": STR_OR_NONE,
    "entry_note": STR_OR_NONE,
    "exit_note": STR_OR_NONE,
    "tags": list,
    # Documented in trade_endpoints.md's Field notes table but omitted from
    # its illustrative JSON example (a doc-example-completeness gap, not a
    # code defect -- confirmed present on every record by
    # backend/services/trade_service.py's get_trade_history_with_stats()).
    "commission_gbp": NUM_OR_NONE,
    "spread_cost_gbp": NUM_OR_NONE,
    "net_r_multiple": NUM_OR_NONE,
}

TRADE_TOP_LEVEL_SCHEMA = {
    "total_trades": int,
    "win_rate": NUM,
    "total_pnl": NUM,
    "avg_slippage_pct": NUM_OR_NONE,
    "avg_fee_drag_pct": NUM_OR_NONE,
    "trades": list,
}

MOCK_TRADE_STATS = {
    "total_trades": 1,
    "win_rate": 100.0,
    "total_pnl": 3200.00,
    "avg_slippage_pct": -0.12,
    "avg_fee_drag_pct": 0.38,
    "trades": [
        {
            "id": "750e8400-e29b-41d4-a716-446655440000",
            "ticker": "NVDA",
            "market": "US",
            "entry_date": "2026-01-15",
            "exit_date": "2026-02-17",
            "shares": 10.5,
            "entry_price": 622.00,
            "exit_price": 920.00,
            "fill_price": 621.25,
            "slippage_pct": -0.12,
            "fee_drag_pct": 0.38,
            "pnl": 3200.00,
            "pnl_pct": 35.8,
            "pnl_percent": 35.8,
            "holding_days": 33,
            "exit_reason": "Target Reached",
            "entry_note": "Breakout above $800",
            "exit_note": "Hit target",
            "tags": ["momentum", "winner"],
            "commission_gbp": 4.50,
            "spread_cost_gbp": 1.20,
            "net_r_multiple": 1.842,
        }
    ],
}


class TestTradesContractSchema:

    @patch("main.get_trade_history_with_stats", return_value=MOCK_TRADE_STATS)
    def test_get_trades_matches_documented_schema(self, _):
        r = CLIENT.get("/trades")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"
        data = body["data"]
        assert_schema(data, TRADE_TOP_LEVEL_SCHEMA, "GET /trades data")
        assert len(data["trades"]) == 1
        assert_schema(data["trades"][0], TRADE_RECORD_SCHEMA, "GET /trades data.trades[0]")


# ---------------------------------------------------------------------------
# GET /portfolio  (docs/specs/api_contracts/portfolio_endpoints.md)
# ---------------------------------------------------------------------------

PORTFOLIO_TOP_LEVEL_SCHEMA = {
    "cash": NUM,
    "cash_balance": NUM,
    "total_value": NUM,
    "open_positions_value": NUM,
    "total_pnl": NUM,
    "initial_value": NUM,
    "net_deposits": NUM,
    "live_fx_rate": NUM,
    "last_updated": str,
    "current_drawdown_percent": NUM,
    "peak_portfolio_value": NUM,
    "positions": list,
}

# Portfolio's position objects are a documented SUMMARY shape (fewer fields
# than GET /positions' full object) -- see portfolio_endpoints.md's "Field
# notes (position summary object)" table.
PORTFOLIO_POSITION_SUMMARY_SCHEMA = {
    "id": str,
    "ticker": str,
    "market": str,
    "entry_date": str,
    "entry_price": NUM,
    "shares": NUM,
    "current_price": NUM,
    "current_value": NUM,
    "pnl": NUM,
    "pnl_pct": NUM,
    "current_stop": NUM,
    "holding_days": int,
    "status": str,
    "display_status": str,
    "fx_rate": NUM,
    "grace_period": bool,
    "grace_days_remaining": (int, type(None)),
    "live_fx_rate": NUM,
}

MOCK_PORTFOLIO_SUMMARY_FULL = {
    "cash": 5000.00,
    "cash_balance": 5000.00,
    "total_value": 15000.00,
    "open_positions_value": 10000.00,
    "total_pnl": 1000.00,
    "initial_value": 14000.00,
    "net_deposits": 14000.00,
    "live_fx_rate": 1.3642,
    "last_updated": "2026-02-17T10:30:00Z",
    "current_drawdown_percent": -8.20,
    "peak_portfolio_value": 16340.00,
    "positions": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "ticker": "NVDA",
            "market": "US",
            "entry_date": "2026-02-01",
            "entry_price": 622.00,
            "shares": 10.5,
            "current_price": 570.87,
            "current_value": 5994.14,
            "pnl": 851.57,
            "pnl_pct": 16.56,
            "current_stop": 607.50,
            "holding_days": 14,
            "status": "open",
            "display_status": "PROFITABLE",
            "fx_rate": 1.2650,
            "grace_period": False,
            "grace_days_remaining": None,
            "live_fx_rate": 1.2750,
        }
    ],
}


class TestPortfolioContractSchema:

    @patch("main.get_portfolio_summary", return_value=dict(MOCK_PORTFOLIO_SUMMARY_FULL))
    def test_get_portfolio_matches_documented_schema(self, _):
        r = CLIENT.get("/portfolio")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"
        data = body["data"]
        assert_schema(data, PORTFOLIO_TOP_LEVEL_SCHEMA, "GET /portfolio data")
        assert len(data["positions"]) == 1
        assert_schema(
            data["positions"][0], PORTFOLIO_POSITION_SUMMARY_SCHEMA, "GET /portfolio data.positions[0]"
        )


# ---------------------------------------------------------------------------
# GET /cash/summary  (docs/reference/openapi.yaml #/components/schemas/CashSummary
#                     + docs/specs/api_contracts/cash_endpoints.md)
#
# ST-06 (BLG-QA-85, EPIC-02, v9.3) extension #1 of 2 — first extension of this
# pilot to source its schema from openapi.yaml directly (endpoints 1-3 above
# source from docs/specs/api_contracts/*.md, per the original ST-11 pilot).
# ---------------------------------------------------------------------------

CASH_SUMMARY_SCHEMA = {
    "total_deposits": NUM,
    "total_withdrawals": NUM,
    "net_cash_flow": NUM,
    "current_cash": NUM,
}

MOCK_CASH_SUMMARY_FULL = {
    "total_deposits": 15000.00,
    "total_withdrawals": 1000.00,
    "net_cash_flow": 14000.00,
    "current_cash": 5000.00,
}


class TestCashSummaryContractSchema:

    @patch("main.get_cash_summary", return_value=dict(MOCK_CASH_SUMMARY_FULL))
    def test_get_cash_summary_matches_documented_schema(self, _):
        r = CLIENT.get("/cash/summary")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"
        assert_schema(body["data"], CASH_SUMMARY_SCHEMA, "GET /cash/summary data")


# ---------------------------------------------------------------------------
# GET /signals  (docs/reference/openapi.yaml #/components/schemas/Signal
#                + docs/specs/api_contracts/signal_endpoints.md)
#
# ST-06 (BLG-QA-85, EPIC-02, v9.3) extension #2 of 2.
#
# Drift found and fixed inline in openapi.yaml as part of this story (simple,
# safe additive/rename corrections, unlike the envelope finding below which
# is a bigger behavioural question left as a recorded finding per this
# pilot's own established precedent — see class docstring/module comment):
#   - Signal.momentum_score never matched reality; the real field (per
#     backend/services/signal_service.py and signal_endpoints.md's own JSON
#     example) is momentum_percent. Renamed in openapi.yaml.
#   - CashSummary was missing current_cash, a field already returned by
#     cash_service.py::get_summary() and already documented correctly in
#     cash_endpoints.md. Added in openapi.yaml (see class above).
# ---------------------------------------------------------------------------

SIGNAL_SCHEMA = {
    "id": str,
    "ticker": str,
    "market": str,
    "signal_date": str,
    "status": str,
    "momentum_percent": NUM,
    "current_price": NUM,
    "reason": STR_OR_NONE,
    "relative_strength_pct": NUM_OR_NONE,
    "week52_high_proximity_pct": NUM_OR_NONE,
    "avg_daily_volume_20d": (int, type(None)),
    "price_vs_50d_ma": NUM_OR_NONE,
}

MOCK_SIGNAL_FULL = {
    "id": "950e8400-e29b-41d4-a716-446655440000",
    "ticker": "TSLA",
    "market": "US",
    "signal_date": "2026-02-17",
    "status": "new",
    "momentum_percent": 45.2,
    "current_price": 220.50,
    "reason": None,
    "relative_strength_pct": 12.4,
    "week52_high_proximity_pct": -3.1,
    "avg_daily_volume_20d": 98000000,
    "price_vs_50d_ma": 5.6,
}


class TestSignalsContractSchema:

    @patch("main.get_signals", return_value=[dict(MOCK_SIGNAL_FULL)])
    def test_get_signals_matches_documented_schema(self, _):
        r = CLIENT.get("/signals")
        assert r.status_code == 200
        body = r.json()

        # Finding (recorded, not silently fixed — same treatment as the
        # GET /positions envelope finding above): both openapi.yaml's
        # OkSignalsList response and signal_endpoints.md's "Response uses
        # the standard success envelope" claim say this endpoint returns
        # {"status": "ok", "data": [...]}. The real handler
        # (backend/main.py::get_signals_endpoint) returns the signals list
        # directly, no envelope. Asserting REALITY, matching this pilot's
        # established philosophy that a contract test's job is to catch
        # drift against actual behaviour. Not fixed inline — an envelope
        # change is a bigger behavioural/compatibility question than the two
        # field-level fixes made in openapi.yaml as part of this story.
        assert isinstance(body, list), (
            "GET /signals does not return a raw list — either the "
            "implementation changed to add an envelope (update this test) "
            "or this assertion needs revisiting."
        )
        assert len(body) == 1
        assert_schema(body[0], SIGNAL_SCHEMA, "GET /signals[0]")


# ---------------------------------------------------------------------------
# Negative test (required precedent, per this sprint's lint-test convention
# — e.g. test_lint_api_contract_headings.py's deliberately-miscoded-heading
# test): confirm assert_schema actually catches a missing/wrong-typed field
# rather than trivially passing.
# ---------------------------------------------------------------------------

def test_assert_schema_catches_missing_field():
    try:
        assert_schema({"a": 1}, {"a": int, "b": str}, "test")
        raised = False
    except AssertionError:
        raised = True
    assert raised, "assert_schema failed to catch a missing documented field"


def test_assert_schema_catches_wrong_type():
    try:
        assert_schema({"a": "not-an-int"}, {"a": int}, "test")
        raised = False
    except AssertionError:
        raised = True
    assert raised, "assert_schema failed to catch a wrong-typed field"
