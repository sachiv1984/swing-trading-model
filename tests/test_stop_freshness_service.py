"""
ST-10 (EPIC-02, v9.13, BLG-SPEC-188): stop freshness -- median and maximum age of
positions.stop_calculated_at across open positions (metrics_definitions.md
§Stop Freshness), and GET /positions/stop-freshness.

Service-level: database functions mocked by name; the arithmetic is exercised
directly against a fixed `now`. Endpoint-level: TestClient with the service
patched, for the 200 envelope and the 500 path.
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.stop_freshness_service as svc  # noqa: E402
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    from fastapi.testclient import TestClient  # noqa: E402

    import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)

NOW = datetime(2026, 10, 17, 9, 0, 0, tzinfo=timezone.utc)


def _pos(ticker, hours_ago):
    stamp = None if hours_ago is None else NOW - timedelta(hours=hours_ago)
    return {"ticker": ticker, "stop_calculated_at": stamp}


def _run(positions, portfolio={"id": "portfolio-1"}):
    with patch.object(svc, "get_portfolio", return_value=portfolio), \
         patch.object(svc, "get_positions", return_value=positions) as get_positions:
        result = svc.get_stop_freshness(now=NOW)
    return result, get_positions


class TestStopFreshnessService:

    def test_median_max_and_counts_exclude_null_stamps(self):
        result, get_positions = _run([
            _pos("VOD.L", 10), _pos("AAPL", 78.2), _pos("MSFT", 20), _pos("BP.L", 30), _pos("NEW.L", None),
        ])
        get_positions.assert_called_once_with("portfolio-1", status="open")
        assert result["open_positions"] == 5
        assert result["recalculated_positions"] == 4
        assert result["never_recalculated"] == 1
        assert result["median_age_hours"] == 25.0  # mean of the two middle ages, 20 and 30
        assert result["max_age_hours"] == 78.2
        assert result["oldest_ticker"] == "AAPL"
        assert result["oldest_stop_calculated_at"] == (NOW - timedelta(hours=78.2)).isoformat()
        assert result["as_of"] == NOW.isoformat()

    def test_odd_count_median_is_the_middle_age(self):
        result, _ = _run([_pos("A", 1), _pos("B", 18.4), _pos("C", 50)])
        assert result["median_age_hours"] == 18.4

    def test_naive_timestamp_is_read_as_utc(self):
        naive = (NOW - timedelta(hours=6)).replace(tzinfo=None)
        result, _ = _run([{"ticker": "A", "stop_calculated_at": naive}])
        assert result["max_age_hours"] == 6.0

    def test_no_stamps_gives_null_ages_and_counts(self):
        result, _ = _run([_pos("A", None), _pos("B", None)])
        assert result["recalculated_positions"] == 0
        assert result["never_recalculated"] == 2
        assert result["median_age_hours"] is None
        assert result["max_age_hours"] is None
        assert result["oldest_ticker"] is None

    def test_no_open_positions(self):
        result, _ = _run([])
        assert (result["open_positions"], result["recalculated_positions"], result["never_recalculated"]) == (0, 0, 0)
        assert result["median_age_hours"] is None

    def test_no_portfolio_reads_no_positions(self):
        result, get_positions = _run([], portfolio=None)
        get_positions.assert_not_called()
        assert result["open_positions"] == 0


class TestStopFreshnessEndpoint:

    def test_200_wraps_service_result(self):
        payload = {"open_positions": 0}
        with patch("services.stop_freshness_service.get_stop_freshness", return_value=payload):
            response = CLIENT.get("/positions/stop-freshness")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "data": payload}

    def test_failure_returns_500_without_detail(self):
        with patch("services.stop_freshness_service.get_stop_freshness", side_effect=RuntimeError("db down")):
            response = CLIENT.get("/positions/stop-freshness")
        assert response.status_code == 500
        assert "db down" not in response.text

    def test_route_is_not_shadowed_by_the_position_id_route(self):
        get_paths = [r.path for r in main.app.routes if "GET" in (getattr(r, "methods", None) or set())]
        assert get_paths.index("/positions/stop-freshness") < get_paths.index("/positions/{position_id}")
