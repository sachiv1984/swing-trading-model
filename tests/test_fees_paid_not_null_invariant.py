"""
ST-47 (BLG-QA-213, EPIC-06, v9.12) — regression guard for the
positions.fees_paid NOT NULL invariant (data_model.md DS-23: NOT NULL with no
default, justified by every write path supplying a numeric value).

  - Entry flow: add_position() for a UK and a US position passes a present,
    non-None, numeric, >= 0 `fees_paid` to create_position().
  - Partial exit: exit_position() passes a numeric, non-None `fees_paid` to
    update_position().
  - Seeds: every `INSERT INTO positions` in a *.sql file under backend/ or
    scripts/ names fees_paid and supplies as many values as columns.

The database layer is mocked throughout (stub DATABASE_URL convention, no
live DB access). The real calculations module is loaded from its file, for
the same suite-order reason as tests/test_atr_provenance.py.
"""
import importlib.util
import re
import sys
from datetime import date
from numbers import Real
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

_spec = importlib.util.spec_from_file_location("_real_calculations_st47", BACKEND / "utils" / "calculations.py")
real_calcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(real_calcs)

import services.position_service as position_service  # noqa: E402

SETTINGS = [{
    "uk_commission": 9.95, "us_commission": 0, "stamp_duty_rate": 0.005,
    "fx_fee_rate": 0.0015, "atr_multiplier_initial": 5, "atr_multiplier_trailing": 2,
}]


def _assert_numeric_fee(data, where):
    assert "fees_paid" in data, f"{where}: fees_paid missing"
    fee = data["fees_paid"]
    assert fee is not None, f"{where}: fees_paid is None"
    assert isinstance(fee, Real) and not isinstance(fee, bool), f"{where}: fees_paid {fee!r} not numeric"
    assert fee >= 0, f"{where}: fees_paid {fee!r} negative"


class _Patcher:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()


class TestEntryFlowSuppliesFeesPaid(_Patcher):

    def _add(self, market):
        for name in ("calculate_initial_stop", "calculate_uk_entry_fees", "calculate_us_entry_fees"):
            self._patch(name, new=getattr(real_calcs, name))
        self._patch("get_portfolio", return_value={"id": "portfolio-1", "cash": 100000.0})
        self._patch("get_settings", return_value=SETTINGS)
        mock_create = self._patch("create_position", return_value={"id": "new-position-id"})
        self._patch("update_portfolio_cash")
        self._patch("get_unlinked_trade_plan_for_entry", return_value=None)
        self._patch("get_current_strategy_version", return_value="1.4")
        position_service.add_position(
            ticker="VOD" if market == "UK" else "NVDA", market=market, entry_date=str(date.today()),
            shares=10, entry_price=100.0, atr_value=3.0, fx_rate=1.25 if market == "US" else None,
        )
        assert mock_create.call_count == 1
        return mock_create.call_args.args[1]

    @pytest.mark.parametrize("market", ["UK", "US"])
    def test_create_position_receives_numeric_fees_paid(self, market):
        _assert_numeric_fee(self._add(market), f"{market} entry")

    def test_uk_fee_is_commission_plus_stamp_duty(self):
        assert self._add("UK")["fees_paid"] == pytest.approx(9.95 + 1000 * 0.005)

    def test_us_fee_is_fx_fee_in_gbp(self):
        assert self._add("US")["fees_paid"] == pytest.approx(1000 * 0.0015 / 1.25)


class TestPartialExitSuppliesFeesPaid(_Patcher):

    @pytest.mark.parametrize("market", ["UK", "US"])
    def test_update_position_receives_numeric_fees_paid(self, market):
        position = {
            "id": "pos-1", "ticker": "VOD.L" if market == "UK" else "NVDA", "market": market,
            "shares": 10, "total_cost": 1014.95, "fees_paid": 14.95, "entry_price": 100.0,
            "fill_price": 100.0, "entry_date": "2026-01-01", "status": "open", "fx_rate": 1.0,
            "user_fill_price": None, "entry_note": None, "tags": None,
        }
        self._patch("get_portfolio", return_value={"id": "portfolio-1", "cash": 100000.0})
        self._patch("get_positions", return_value=[position])
        self._patch("get_settings", return_value=SETTINGS)
        self._patch("update_portfolio_cash")
        self._patch("create_trade_history")
        self._patch("get_trade_plans_by_position", return_value=[])
        self._patch("ensure_planned_entry_price_column", return_value=None)
        mock_update = self._patch("update_position")
        kwargs = {"position_id": "pos-1", "exit_price": 110.0, "shares": 4, "exit_date": "2026-02-01"}
        if market == "US":
            kwargs["exit_fx_rate"] = 1.25
        position_service.exit_position(**kwargs)
        updates = [c.args[1] for c in mock_update.call_args_list if "shares" in c.args[1]]
        assert updates, "partial exit did not update the position's shares"
        _assert_numeric_fee(updates[0], f"{market} partial exit")
        assert updates[0]["fees_paid"] == pytest.approx(14.95 * 6 / 10, abs=0.01)


# ── Seeds: every INSERT INTO positions names fees_paid ─────────────────────

INSERT_RE = re.compile(r"INSERT\s+INTO\s+positions\s*\(", re.IGNORECASE)


def _strip_comments(sql):
    return re.sub(r"--[^\n]*", "", sql)


def _balanced(text, start):
    """Return (inner, end) for the parenthesised group opening at text[start]."""
    depth, i, quote = 0, start, False
    while i < len(text):
        ch = text[i]
        if ch == "'":
            quote = not quote
        elif not quote and ch == "(":
            depth += 1
        elif not quote and ch == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    raise ValueError("unbalanced parentheses")


def _split_top_level(text):
    parts, depth, quote, cur = [], 0, False, ""
    for ch in text:
        if ch == "'":
            quote = not quote
        if not quote and ch == "(":
            depth += 1
        if not quote and ch == ")":
            depth -= 1
        if ch == "," and depth == 0 and not quote:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def positions_insert_problems(sql, label):
    """Return a list of problems with every INSERT INTO positions in `sql`."""
    sql = _strip_comments(sql)
    problems = []
    for m in INSERT_RE.finditer(sql):
        cols_text, end = _balanced(sql, m.end() - 1)
        cols = [c.strip().lower() for c in _split_top_level(cols_text)]
        where = f"{label}: INSERT INTO positions at offset {m.start()}"
        if "fees_paid" not in cols:
            problems.append(f"{where}: column list omits fees_paid")
        rest = sql[end:].lstrip()
        if rest[:6].upper() == "VALUES":
            pos = end + (len(sql[end:]) - len(rest)) + 6
            while True:
                nxt = sql[pos:].lstrip()
                if not nxt.startswith("("):
                    break
                pos += len(sql[pos:]) - len(nxt)
                values_text, pos = _balanced(sql, pos)
                n = len(_split_top_level(values_text))
                if n != len(cols):
                    problems.append(f"{where}: {n} values for {len(cols)} columns")
                after = sql[pos:].lstrip()
                if not after.startswith(","):
                    break
                pos += len(sql[pos:]) - len(after) + 1
        elif rest[:6].upper() == "SELECT":
            from_m = re.search(r"\bFROM\b", rest, re.IGNORECASE)
            n = len(_split_top_level(rest[6:from_m.start()]))
            if n != len(cols):
                problems.append(f"{where}: SELECT lists {n} expressions for {len(cols)} columns")
        else:
            problems.append(f"{where}: unrecognised insert source (expected VALUES or SELECT)")
    return problems


def _seed_files():
    return sorted(p for base in ("backend", "scripts") for p in (ROOT / base).rglob("*.sql")
                  if ".venv" not in p.parts and "node_modules" not in p.parts)


def test_repo_seeds_supply_fees_paid():
    files = [p for p in _seed_files() if INSERT_RE.search(_strip_comments(p.read_text()))]
    assert files, "expected at least one SQL file inserting into positions"
    problems = [x for p in files for x in positions_insert_problems(p.read_text(), str(p.relative_to(ROOT)))]
    assert problems == []


def test_seed_insert_omitting_fees_paid_fails(tmp_path):
    seed = ROOT / "backend" / "test_data" / "seed_chart_test_data.sql"
    broken = seed.read_text().replace("total_cost, fees_paid, pnl", "total_cost, pnl", 1).replace(
        "1150.00, 0.00, 100.00", "1150.00, 100.00", 1)
    copy = tmp_path / "seed_copy.sql"
    copy.write_text(broken)
    problems = positions_insert_problems(copy.read_text(), "seed_copy.sql")
    assert any("omits fees_paid" in p for p in problems)


def test_value_count_mismatch_fails():
    sql = "INSERT INTO positions (ticker, fees_paid, shares) VALUES ('A', 0.0, 1), ('B', 0.0);"
    assert positions_insert_problems(sql, "x") == ["x: INSERT INTO positions at offset 0: 2 values for 3 columns"]


def test_select_form_counts_expressions():
    good = "INSERT INTO positions (ticker, fees_paid) SELECT pos.ticker, pos.fees_paid FROM t;"
    bad = "INSERT INTO positions (ticker, fees_paid) SELECT pos.ticker FROM t;"
    assert positions_insert_problems(good, "x") == []
    assert "SELECT lists 1 expressions for 2 columns" in positions_insert_problems(bad, "x")[0]
