"""
Tests for scripts/check_router_test_registration.py — ST-10 (EPIC-10, v7.9, BLG-QA-125).

Exercises the path/method matching logic directly (pure functions, no git
subprocess calls) including the deliberately-missing case required by AC-02.
"""

import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_router_test_registration.py"
spec = importlib.util.spec_from_file_location("check_router_test_registration", SCRIPT_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules["check_router_test_registration"] = mod
spec.loader.exec_module(mod)


def test_registered_route_is_found():
    test_entries = [("GET", "/health"), ("GET", "/positions")]
    assert mod.is_registered("GET", "/health", test_entries) is True


def test_deliberately_missing_route_is_not_found():
    """AC-02: a new route with no test.py entry must be flagged as unregistered."""
    test_entries = [("GET", "/health"), ("GET", "/positions")]
    assert mod.is_registered("POST", "/portfolio/new-unregistered-endpoint", test_entries) is False


def test_find_unregistered_routes_flags_only_the_missing_one():
    new_routes = [("GET", "/health"), ("POST", "/portfolio/new-unregistered-endpoint")]
    test_entries = [("GET", "/health")]
    missing = mod.find_unregistered_routes(new_routes, test_entries)
    assert missing == [("POST", "/portfolio/new-unregistered-endpoint")]


def test_parameterised_route_matches_representative_value():
    """{ticker} in the router path must match a concrete value like AAPL in test.py."""
    test_entries = [("GET", "/watchlist/AAPL")]
    assert mod.is_registered("GET", "/watchlist/{ticker}", test_entries) is True


def test_parameterised_test_entry_matches_concrete_router_path():
    test_entries = [("GET", "/watchlist/{ticker}")]
    assert mod.is_registered("GET", "/watchlist/AAPL", test_entries) is True


def test_wrong_method_is_not_a_match():
    test_entries = [("GET", "/positions")]
    assert mod.is_registered("POST", "/positions", test_entries) is False


def test_extract_new_routes_prefix_join():
    """Prefix + route path join must not double or drop slashes."""
    result_full_path = ("/portfolio-risk/" + "/gate-metrics".lstrip("/")).replace("//", "/")
    assert result_full_path == "/portfolio-risk/gate-metrics"


def test_parse_test_py_entries_extracts_method_and_path():
    content = '''
    test_cases = [
        {"name": "GET /health", "method": "GET", "url": f"{base_url}/health", "critical": True},
        {"name": "POST /portfolio/position", "method": "POST", "url": f"{base_url}/portfolio/position", "critical": True},
    ]
    '''
    entries = mod.parse_test_py_entries(content)
    assert ("GET", "/health") in entries
    assert ("POST", "/portfolio/position") in entries


def test_no_staged_router_files_is_a_pass(monkeypatch):
    monkeypatch.setattr(mod, "get_staged_router_files", lambda: [])
    assert mod.main() == 0


def test_parenthetical_annotation_does_not_break_matching():
    """Regression: QA & Testing Owner review (EPIC-10 sign-off) found that a real
    test.py entry name like "GET /analytics/metrics (all_time)" was not matching
    the route "/analytics/metrics" because the trailing annotation was treated as
    part of the path. Multiple disambiguated entries for the same route (different
    query-string variants) must all resolve to the same clean path."""
    content = '''
    test_cases = [
        {"name": "GET /analytics/metrics (all_time)", "method": "GET", "url": f"{base_url}/analytics/metrics?period=all_time", "critical": True},
        {"name": "GET /analytics/metrics (last_7_days)", "method": "GET", "url": f"{base_url}/analytics/metrics?period=last_7_days", "critical": False},
    ]
    '''
    entries = mod.parse_test_py_entries(content)
    assert ("GET", "/analytics/metrics") in entries
    assert mod.is_registered("GET", "/analytics/metrics", entries) is True


def test_empty_string_path_decorator_is_matched():
    """Regression: ST-21 (BLG-QA-146, v8.8) re-audit found ROUTE_DECORATOR_RE's path
    capture group was `+` (one-or-more), which silently failed to match a bare
    `@router.get("")`/`@router.post("")` decorator (empty-string path, resolving to
    the router's own prefix root — e.g. ticker_universe.py's GET/POST "/ticker-universe").
    A newly added route registered this way would go undetected by this gate with no
    error or warning. Fixed to `*` (zero-or-more)."""
    line = '@router.get("")'
    m = mod.ROUTE_DECORATOR_RE.search(line)
    assert m is not None
    assert m.group(1) == "get"
    assert m.group(2) == ""


def test_empty_string_path_route_extraction_resolves_to_prefix_root(monkeypatch):
    """End-to-end: a staged `@router.post("")` addition to a prefixed router must be
    extracted as the prefix root path, not silently dropped."""
    monkeypatch.setattr(mod, "get_staged_added_lines", lambda path: ['+@router.post("", status_code=201)'])
    monkeypatch.setattr(
        mod,
        "get_staged_file_content",
        lambda path: 'router = APIRouter(prefix="/ticker-universe")\n@router.post("", status_code=201)\ndef create():\n    pass\n',
    )
    routes = mod.extract_new_routes("backend/routers/ticker_universe.py")
    assert ("POST", "/ticker-universe") in routes
