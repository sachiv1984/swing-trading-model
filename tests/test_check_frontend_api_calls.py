"""
Unit tests for scripts/check_frontend_api_calls.py (ST-23, EPIC-04, v9.13,
BLG-QA-228).

Covers path and method resolution for the call shapes used in src/, the
AC's named failure case (a call to a route that does not exist), the
allow-lists, and a pass against the real src/ tree and openapi.yaml.
"""
import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "check_frontend_api_calls.py"

spec = importlib.util.spec_from_file_location("check_frontend_api_calls", SCRIPT_PATH)
cfac = importlib.util.module_from_spec(spec)
sys.modules["check_frontend_api_calls"] = cfac
spec.loader.exec_module(cfac)

OPENAPI_FIXTURE = """
openapi: 3.0.0
info: {title: t, version: '1'}
paths:
  /positions:
    get: {}
  /positions/{position_id}/exit:
    post: {}
  /watchlist/{entry_id}:
    patch: {}
    delete: {}
"""


def _write_tree(tmp_path, files):
    src = tmp_path / "src"
    for rel, content in files.items():
        f = src / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
    openapi = tmp_path / "openapi.yaml"
    openapi.write_text(OPENAPI_FIXTURE)
    return src, openapi


# ---------------------------------------------------------------------------
# resolve_path / resolve_methods -- pure functions
# ---------------------------------------------------------------------------

def test_resolve_path_plain_string():
    assert cfac.resolve_path("'/positions'") == "/positions"


def test_resolve_path_drops_base_url_and_maps_params():
    assert cfac.resolve_path("`${API_BASE}/positions/${id}/exit`") == "/positions/{param}/exit"


def test_resolve_path_drops_literal_query_string():
    assert cfac.resolve_path("`${API_BASE_URL}/notifications?page=1${filterQuery}`") == "/notifications"


def test_resolve_path_drops_conditional_query_interpolation():
    assert cfac.resolve_path("`/strategy/benchmark/trades${qs ? '?' + qs : ''}`") == "/strategy/benchmark/trades"


def test_resolve_path_returns_none_for_variable():
    assert cfac.resolve_path("url") is None


def test_resolve_methods_defaults_to_get():
    assert cfac.resolve_methods(["'/positions'"]) == ["GET"]


def test_resolve_methods_reads_conditional_method():
    args = ["`/watchlist/${id}`", "{ method: editing ? 'PATCH' : 'DELETE', body }"]
    assert cfac.resolve_methods(args) == ["PATCH", "DELETE"]


def test_extract_calls_handles_multiline_call_and_skips_definition():
    text = (
        "async function doFetch(path, { method = 'GET' } = {}) {}\n"
        "const r = await apiFetch(\n"
        "  `${API_BASE}/positions/${p.id}/exit`,\n"
        "  { method: 'POST', body: JSON.stringify({ a: ')' }) }\n"
        ");\n"
    )
    calls = cfac.extract_calls(text)
    assert len(calls) == 1
    assert calls[0]["line"] == 2
    assert calls[0]["path"] == "/positions/{param}/exit"
    assert calls[0]["methods"] == ["POST"]


# ---------------------------------------------------------------------------
# find_missing_calls end-to-end against a sandboxed tree
# ---------------------------------------------------------------------------

def test_passes_when_every_call_exists(tmp_path):
    src, openapi = _write_tree(tmp_path, {
        "pages/A.js": (
            "doFetch('/positions');\n"
            "apiFetch(`${API_BASE}/positions/${id}/exit`, { method: 'POST' });\n"
            "apiFetch(`${API_BASE}/watchlist/${id}`, { method: 'DELETE' });\n"
        ),
    })
    assert cfac.find_missing_calls(src, openapi) == []


def test_fails_on_call_to_nonexistent_route(tmp_path):
    # The real case this check exists for: PATCH /positions/{id} (BLG-FE-226).
    src, openapi = _write_tree(tmp_path, {
        "pages/A.js": "apiFetch(`${API_BASE}/positions/${id}`, { method: 'PATCH' });\n",
    })
    problems = cfac.find_missing_calls(src, openapi)
    assert problems == ["src/pages/A.js:1: PATCH /positions/{param} is not in openapi.yaml"]


def test_fails_on_wrong_method_for_existing_path(tmp_path):
    src, openapi = _write_tree(tmp_path, {
        "pages/A.js": "doFetch('/positions', { method: 'POST' });\n",
    })
    assert len(cfac.find_missing_calls(src, openapi)) == 1


def test_fails_on_unresolved_path_argument(tmp_path):
    src, openapi = _write_tree(tmp_path, {"pages/A.js": "apiFetch(someUrl);\n"})
    problems = cfac.find_missing_calls(src, openapi)
    assert problems == ["src/pages/A.js:1: unresolved path argument 'someUrl'"]


def test_unresolved_allow_list_route_is_still_checked(tmp_path, monkeypatch):
    src, openapi = _write_tree(tmp_path, {"pages/A.js": "apiFetch(someUrl);\n"})
    monkeypatch.setattr(cfac, "UNRESOLVED_ALLOW_LIST", {"src/pages/A.js:someUrl": ["GET /no-such-route"]})
    problems = cfac.find_missing_calls(src, openapi)
    assert problems == ["src/pages/A.js:1: GET /no-such-route is not in openapi.yaml"]


def test_allow_list_suppresses_dead_method(tmp_path, monkeypatch):
    src, openapi = _write_tree(tmp_path, {"api/c.js": "doFetch('/signals', { method: 'POST' });\n"})
    monkeypatch.setattr(cfac, "ALLOW_LIST", {"POST /signals": "dead — BLG-FE-230"})
    assert cfac.find_missing_calls(src, openapi) == []


def test_external_call_needs_external_allow_list(tmp_path, monkeypatch):
    src, openapi = _write_tree(tmp_path, {"pages/A.js": "apiFetch('https://example.com/x');\n"})
    assert len(cfac.find_missing_calls(src, openapi)) == 1
    monkeypatch.setattr(cfac, "EXTERNAL_ALLOW_LIST", {"https://example.com/": "test"})
    assert cfac.find_missing_calls(src, openapi) == []


def test_every_allow_list_entry_names_its_backlog_item_or_reason():
    for key, reason in cfac.ALLOW_LIST.items():
        assert "BLG-" in reason and "allow-listed 20" in reason, key


# ---------------------------------------------------------------------------
# Real tree
# ---------------------------------------------------------------------------

def test_real_src_tree_passes():
    assert cfac.find_missing_calls(cfac.SRC_DIR, cfac.OPENAPI_PATH) == []
