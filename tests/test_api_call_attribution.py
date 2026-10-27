"""
ST-31 (BLG-OPS-19, EPIC-05, v9.13) — attribute each external API call to the
feature that triggered it.

- AC 1: every outbound market-data call is tagged with its triggering
  endpoint or feature. Covered at each layer: host classification, the
  transport wrappers (requests, and curl_cffi for yfinance), the request
  middleware (route template, background tasks), worker threads in a
  screener run, and the batch write to api_call_log.
- AC 2: an attribution report (cost by feature) is computable and names the
  top 3 contributors: build_attribution_report and GET /ops/api-call-attribution.

CI-safe: no network and no database. HTTP is stopped at
requests.adapters.HTTPAdapter.send; database writes are patched.
"""
import contextvars
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import load_real_database, real_database_imports  # noqa: E402

with real_database_imports():
    from fastapi.testclient import TestClient  # noqa: E402

    import main  # noqa: E402
    from services import screener_batch_service  # noqa: E402
    from utils import api_attribution  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
ALPACA_BARS = "https://data.alpaca.markets/v2/stocks/AAPL/bars"
ALPACA_NEWS = "https://data.alpaca.markets/v1beta1/news"


def _response(status=200, body=None):
    resp = requests.Response()
    resp.status_code = status
    resp._content = json.dumps(body or {}).encode()
    resp.url = YAHOO
    return resp


@pytest.fixture(autouse=True)
def empty_buffer():
    with patch("database.log_api_calls"):
        api_attribution.flush()
    yield
    with patch("database.log_api_calls"):
        api_attribution.flush()


def _buffered():
    with api_attribution._buffer_lock:
        return list(api_attribution._buffer)


class TestClassify:
    @pytest.mark.parametrize("url,service", [
        (YAHOO, "yahoo"),
        ("https://query2.finance.yahoo.com/v1/test/getcrumb", "yahoo"),
        ("https://finance.yahoo.com/", "yahoo"),
        (ALPACA_BARS, "alpaca_data"),
        (ALPACA_NEWS, "alpaca_news"),
        ("https://paper-api.alpaca.markets/v2/positions", "alpaca_paper"),
        ("https://api.twelvedata.com/time_series", "twelve_data"),
        ("https://stooq.com/q/d/l/", "stooq"),
    ])
    def test_provider_hosts(self, url, service):
        assert api_attribution.classify(url)[0] == service

    @pytest.mark.parametrize("url", [
        "https://api.anthropic.com/v1/messages",
        "https://api.telegram.org/bot1/sendMessage",
        "https://api.render.com/v1/services",
        "not a url",
    ])
    def test_other_hosts_are_not_recorded(self, url):
        assert api_attribution.classify(url) is None
        api_attribution.record_call(url, True)
        assert _buffered() == []

    def test_path_is_kept_without_query(self):
        assert api_attribution.classify(YAHOO + "?range=1y") == ("yahoo", "/v8/finance/chart/AAPL")

    def test_every_service_has_a_unit_cost(self):
        services = set(api_attribution.PROVIDER_HOSTS.values()) | {api_attribution.ALPACA_NEWS_SERVICE}
        assert services == set(api_attribution.PROVIDER_SERVICES)


class TestFeature:
    def test_default_is_unattributed(self):
        api_attribution.record_call(YAHOO, True)
        assert _buffered()[0][2] == "unattributed"

    def test_feature_scope_tags_and_restores(self):
        with api_attribution.feature_scope("POST /screener/run"):
            api_attribution.record_call(YAHOO, True)
        api_attribution.record_call(YAHOO, False)
        rows = _buffered()
        assert [(r[0], r[1], r[2], r[3]) for r in rows] == [
            ("yahoo", "/v8/finance/chart/AAPL", "POST /screener/run", True),
            ("yahoo", "/v8/finance/chart/AAPL", "unattributed", False),
        ]


class TestTransport:
    def test_requests_calls_are_recorded_with_status(self):
        assert hasattr(requests.Session.request, "_api_attribution_original")
        with patch("requests.adapters.HTTPAdapter.send", side_effect=[_response(200), _response(429)]):
            with api_attribution.feature_scope("GET /market/regime"):
                requests.get(YAHOO, timeout=1)
                requests.get(ALPACA_BARS, timeout=1)
        rows = _buffered()
        assert [(r[0], r[2], r[3]) for r in rows] == [
            ("yahoo", "GET /market/regime", True),
            ("alpaca_data", "GET /market/regime", False),
        ]

    def test_exception_is_recorded_as_failure_and_reraised(self):
        with patch("requests.adapters.HTTPAdapter.send", side_effect=requests.ConnectionError("down")):
            with pytest.raises(requests.ConnectionError):
                requests.get(YAHOO, timeout=1)
        assert _buffered()[0][3] is False

    def test_yfinance_transport_is_wrapped(self):
        curl_requests = pytest.importorskip("curl_cffi.requests")
        assert hasattr(curl_requests.Session.request, "_api_attribution_original")

    def test_install_is_idempotent(self):
        wrapped = requests.Session.request
        api_attribution.install()
        assert requests.Session.request is wrapped


class TestFlush:
    def test_flush_writes_one_batch_and_empties_the_buffer(self):
        api_attribution.record_call(YAHOO, True)
        api_attribution.record_call(ALPACA_NEWS, True)
        with patch("database.log_api_calls") as log:
            assert api_attribution.flush() == 2
        (rows,), _ = log.call_args
        assert [r[0] for r in rows] == ["yahoo", "alpaca_news"]
        assert _buffered() == []

    def test_buffer_flushes_itself_at_the_threshold(self):
        with patch("database.log_api_calls") as log:
            for _ in range(api_attribution.FLUSH_THRESHOLD):
                api_attribution.record_call(YAHOO, True)
        assert log.call_count == 1
        assert len(log.call_args[0][0]) == api_attribution.FLUSH_THRESHOLD
        assert _buffered() == []

    def test_write_failure_drops_the_batch_without_raising(self, caplog):
        api_attribution.record_call(YAHOO, True)
        with patch("database.log_api_calls", side_effect=RuntimeError("db down")):
            assert api_attribution.flush() == 0
        assert _buffered() == []
        assert any("attribution flush failed" in r.getMessage() for r in caplog.records)

    def test_empty_flush_does_not_touch_the_database(self):
        with patch("database.log_api_calls") as log:
            assert api_attribution.flush() == 0
        log.assert_not_called()


class TestMiddleware:
    def test_request_calls_are_tagged_with_the_route_template(self):
        news = {"news": [{"headline": "h", "created_at": "2026-10-27T10:00:00Z"}]}
        with patch("services.news_service._credentials_configured", return_value=True), \
             patch("requests.adapters.HTTPAdapter.send", return_value=_response(200, news)), \
             patch("database.log_api_calls") as log:
            resp = CLIENT.get("/news/AAPL")
        assert resp.status_code == 200
        rows = [r for call in log.call_args_list for r in call[0][0]]
        assert [(r[0], r[1], r[2]) for r in rows] == [("alpaca_news", "/v1beta1/news", "GET /news/{ticker}")]

    def test_request_without_provider_calls_writes_nothing(self):
        with patch("database.get_api_call_attribution", return_value=[]), \
             patch("database.log_api_calls") as log:
            CLIENT.get("/ops/api-call-attribution")
        log.assert_not_called()

    def test_unmatched_path(self):
        request = MagicMock(method="GET", scope={"type": "http", "path": "/no/such/route"})
        assert main._route_feature(request) == "GET unmatched"

    def test_feature_resolver_is_read_at_call_time(self):
        scope = {}
        token = api_attribution.set_feature(lambda: scope.get("route", "pending"))
        try:
            scope["route"] = "GET /later"
            api_attribution.record_call(YAHOO, True)
        finally:
            api_attribution.reset_feature(token)
        assert _buffered()[0][2] == "GET /later"


class TestScreenerRun:
    def _run(self, universe):
        def fake_fetch(ticker, market, days=30):
            api_attribution.record_call(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}", True)
            return None

        persisted = {}
        with patch.object(screener_batch_service, "_fetch_index_regime", return_value=None), \
             patch.object(screener_batch_service, "fetch_ohlcv", side_effect=fake_fetch), \
             patch.object(screener_batch_service, "_persist_run",
                          side_effect=lambda *a, **k: persisted.update(k)), \
             patch.object(screener_batch_service, "_persist_results"), \
             patch.object(screener_batch_service.time, "sleep"), \
             patch("database.log_api_calls") as log:
            with api_attribution.feature_scope("POST /screener/run"):
                result = screener_batch_service.run_screener(universe)
        rows = [r for call in log.call_args_list for r in call[0][0]]
        return result, persisted, rows

    def test_worker_thread_calls_keep_the_run_feature_and_are_flushed(self):
        result, _, rows = self._run(["AAPL", "MSFT", "NVDA", "BARC.L"])
        assert sorted(r[1] for r in rows) == sorted(
            f"/v8/finance/chart/{t}" for t in ["AAPL", "MSFT", "NVDA", "BARC.L"])
        assert {r[2] for r in rows} == {"POST /screener/run"}
        assert _buffered() == []

    def test_run_records_its_duration(self):
        result, persisted, _ = self._run(["AAPL"])
        assert isinstance(persisted["duration_seconds"], float) and persisted["duration_seconds"] >= 0
        assert result["duration_seconds"] == persisted["duration_seconds"]

    def test_copied_context_reaches_executor_threads(self):
        from concurrent.futures import ThreadPoolExecutor
        with api_attribution.feature_scope("job"):
            with ThreadPoolExecutor(max_workers=2) as ex:
                bare = ex.submit(api_attribution.get_feature).result()
                copied = ex.submit(contextvars.copy_context().run, api_attribution.get_feature).result()
        assert (bare, copied) == ("unattributed", "job")


ROWS = [
    {"feature": "POST /screener/run", "service": "yahoo", "total_calls": 400, "failure_count": 5},
    {"feature": "POST /screener/run", "service": "alpaca_data", "total_calls": 300, "failure_count": 0},
    {"feature": "GET /news/{ticker}", "service": "alpaca_news", "total_calls": 50, "failure_count": 1},
    {"feature": "POST /positions/nightly-stop-update", "service": "yahoo", "total_calls": 80, "failure_count": 0},
    {"feature": "unattributed", "service": "yahoo", "total_calls": 10, "failure_count": 0},
]


class TestReport:
    def test_ranks_by_calls_while_every_provider_is_free(self):
        report = api_attribution.build_attribution_report(ROWS, "weekly")
        assert report["total_calls"] == 840
        assert report["estimated_cost_usd"] == 0.0
        assert report["top_contributors"] == [
            "POST /screener/run", "POST /positions/nightly-stop-update", "GET /news/{ticker}"]
        screener = report["by_feature"][0]
        assert screener["by_service"] == {"yahoo": 400, "alpaca_data": 300}
        assert screener["failure_count"] == 5
        assert [s["service"] for s in report["by_service"]] == ["yahoo", "alpaca_data", "alpaca_news"]

    def test_cost_outranks_volume_once_a_provider_charges(self):
        with patch.dict(api_attribution.UNIT_COST_USD, {"alpaca_news": 0.01}):
            report = api_attribution.build_attribution_report(ROWS, "weekly")
        assert report["top_contributors"][0] == "GET /news/{ticker}"
        assert report["by_feature"][0]["estimated_cost_usd"] == 0.5
        assert report["estimated_cost_usd"] == 0.5

    def test_empty(self):
        report = api_attribution.build_attribution_report([], "daily")
        assert (report["total_calls"], report["by_feature"], report["top_contributors"]) == (0, [], [])


class TestEndpoint:
    def test_200_report(self):
        with patch("database.get_api_call_attribution", return_value=ROWS) as q:
            resp = CLIENT.get("/ops/api-call-attribution")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok" and body["data"]["window"] == "weekly"
        assert body["data"]["top_contributors"][0] == "POST /screener/run"
        services, window = q.call_args[0]
        assert set(services) == set(api_attribution.PROVIDER_SERVICES) and window == "weekly"

    def test_daily_window(self):
        with patch("database.get_api_call_attribution", return_value=[]) as q:
            assert CLIENT.get("/ops/api-call-attribution?window=daily").status_code == 200
        assert q.call_args[0][1] == "daily"

    def test_bad_window_422(self):
        assert CLIENT.get("/ops/api-call-attribution?window=monthly").status_code == 422

    def test_query_failure_503_not_zero(self):
        with patch("database.get_api_call_attribution", side_effect=RuntimeError("db down")):
            resp = CLIENT.get("/ops/api-call-attribution")
        assert resp.status_code == 503
        assert resp.json()["error"] == "attribution_query_failed"


def _db_with_cursor():
    cur = MagicMock()
    cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
    conn = MagicMock(__exit__=MagicMock(return_value=False))
    conn.__enter__ = MagicMock(return_value=conn)
    conn.cursor.return_value = cur_ctx
    return conn, cur


class TestDatabaseLayer:
    def setup_method(self):
        self.db = load_real_database("database_real_for_test_api_call_attribution")

    def test_log_api_calls_inserts_one_batch(self):
        conn, cur = _db_with_cursor()
        rows = [("yahoo", "/v8/finance/chart/AAPL", "GET /x", True, "2026-10-27T00:00:00Z")]
        with patch.object(self.db, "get_db", return_value=conn), \
             patch.object(self.db, "ensure_api_call_log_table"), \
             patch("psycopg2.extras.execute_values") as ev:
            self.db.log_api_calls(rows)
        sql, sent = ev.call_args[0][1], ev.call_args[0][2]
        assert "INSERT INTO api_call_log (service, endpoint, feature, success, called_at)" in sql
        assert sent == rows
        conn.commit.assert_called_once()

    def test_log_api_calls_empty_is_a_no_op(self):
        with patch.object(self.db, "get_db") as get_db:
            self.db.log_api_calls([])
        get_db.assert_not_called()

    def test_attribution_query_groups_by_feature_and_service(self):
        conn, cur = _db_with_cursor()
        cur.fetchall.return_value = [{"feature": "unattributed", "service": "yahoo",
                                      "total_calls": 3, "failure_count": 0}]
        with patch.object(self.db, "get_db", return_value=conn), \
             patch.object(self.db, "ensure_api_call_log_table"):
            rows = self.db.get_api_call_attribution(("yahoo", "alpaca_data"), "weekly")
        sql, params = cur.execute.call_args[0]
        assert "COALESCE(feature, 'unattributed')" in sql and "GROUP BY 1, 2" in sql
        assert "INTERVAL '7 days'" in sql and params == (["yahoo", "alpaca_data"],)
        assert rows[0]["total_calls"] == 3

    def test_attribution_query_failure_raises(self):
        with patch.object(self.db, "get_db", side_effect=RuntimeError("db down")), \
             patch.object(self.db, "ensure_api_call_log_table"):
            with pytest.raises(RuntimeError):
                self.db.get_api_call_attribution(("yahoo",), "daily")

    def test_ensure_adds_feature_column_once_per_process(self):
        conn, cur = _db_with_cursor()
        self.db._api_call_log_ready = False
        with patch.object(self.db, "get_db", return_value=conn):
            self.db.ensure_api_call_log_table()
            self.db.ensure_api_call_log_table()
        sql = [c[0][0] for c in cur.execute.call_args_list]
        assert "ALTER TABLE api_call_log ADD COLUMN IF NOT EXISTS feature TEXT" in sql
        assert any("idx_acl_called_at_feature" in s for s in sql)
        assert conn.commit.call_count == 1
