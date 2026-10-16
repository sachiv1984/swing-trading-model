"""
ST-02 (BLG-SPEC-186, EPIC-01, v9.13): the allowed exit_reason values and the
strategy_rules.md §8 condition each maps to (data_model.md §3 Exit Reason
Values, DS-34).

- Every allowed value maps to exactly one of §8's three conditions.
- Every legacy alias DS-34 backfills resolves to an allowed value.
- POST /positions/{id}/exit rejects an unlisted value with a 400 (the contract's
  "Invalid exit_reason"), before anything is written, and accepts each allowed
  value and an omitted / null reason.
- data_model.md's table and DS-34's CHECK lists match backend/exit_reasons.py.
"""
import re
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from exit_reasons import (  # noqa: E402
    EXIT_REASONS,
    LEGACY_ALIASES,
    SECTION_8_MANUAL,
    SECTION_8_RISK_OFF,
    SECTION_8_STOP_LOSS,
)

SECTION_8 = {SECTION_8_STOP_LOSS, SECTION_8_RISK_OFF, SECTION_8_MANUAL}


def test_six_allowed_values_each_map_to_one_section_8_condition():
    assert set(EXIT_REASONS) == {
        "Stop Loss Hit", "Trailing Stop", "Risk-Off Signal",
        "Manual Exit", "Target Reached", "Partial Profit Taking",
    }
    for value, category in EXIT_REASONS.items():
        assert category in SECTION_8, value
    assert set(EXIT_REASONS.values()) == SECTION_8


def test_every_legacy_alias_resolves_to_an_allowed_value():
    for alias, value in LEGACY_ALIASES.items():
        assert value in EXIT_REASONS, alias
        assert alias not in EXIT_REASONS


def _data_model():
    return (ROOT / "docs" / "specs" / "data_model.md").read_text(encoding="utf-8")


def test_data_model_table_matches_the_module():
    text = _data_model()
    section = text.split("### Exit Reason Values", 1)[1].split("\n---", 1)[0]
    rows = re.findall(r'^\| `"([^"]+)"` \| ([^|]+) \|', section, re.M)
    assert {v: c.strip() for v, c in rows} == EXIT_REASONS


def test_ds34_check_constraints_list_exactly_the_allowed_values():
    ds34 = _data_model().split("## DS-34", 1)[1].split("\n## DS-", 1)[0]
    up = ds34.split("### Up Migration", 1)[1].split("### Down Migration", 1)[0]
    lists = re.findall(r"exit_reason IN \(([^)]*)\)", up)
    assert len(lists) == 2  # positions and trade_history
    for found in lists:
        assert set(re.findall(r"'([^']+)'", found)) == set(EXIT_REASONS)
    for alias, value in LEGACY_ALIASES.items():
        assert f"'{alias}'" in up, alias


class TestExitEndpointValidation:
    @staticmethod
    def _client():
        from tests._real_database import real_database_imports
        with real_database_imports():
            from fastapi.testclient import TestClient
            import main
        return TestClient(main.app, raise_server_exceptions=False), main

    _BODY = {"shares": 10, "exit_price": 120.0, "exit_date": "2026-10-16"}

    @pytest.mark.parametrize("reason", ["market_regime", "stop_hit", "Rebalance", "stop loss hit", ""])
    def test_unlisted_value_is_rejected_with_400_before_any_write(self, reason):
        client, main = self._client()
        with patch.object(main, "exit_position") as mock_exit:
            response = client.post("/positions/pos-1/exit", json={**self._BODY, "exit_reason": reason})
        assert response.status_code == 400
        assert "exit_reason must be one of: Stop Loss Hit, Trailing Stop" in response.text
        mock_exit.assert_not_called()

    @pytest.mark.parametrize("reason", sorted(EXIT_REASONS))
    def test_each_allowed_value_is_accepted(self, reason):
        client, main = self._client()
        with patch.object(main, "exit_position", return_value={"market": "UK"}) as mock_exit:
            response = client.post("/positions/pos-1/exit", json={**self._BODY, "exit_reason": reason})
        assert response.status_code == 200
        assert mock_exit.call_args.kwargs["exit_reason"] == reason

    @pytest.mark.parametrize("body", [{}, {"exit_reason": None}])
    def test_omitted_or_null_reason_is_accepted(self, body):
        client, main = self._client()
        with patch.object(main, "exit_position", return_value={"market": "UK"}):
            response = client.post("/positions/pos-1/exit", json={**self._BODY, **body})
        assert response.status_code == 200
