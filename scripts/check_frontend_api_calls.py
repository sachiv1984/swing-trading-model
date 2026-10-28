#!/usr/bin/env python3
"""
Frontend API Call Existence Check (ST-23, EPIC-04, v9.13, BLG-QA-228).

Extracts every `doFetch(...)` and `apiFetch(...)` call in `src/`, resolves
its HTTP method and path, and checks that the pair exists in
docs/reference/openapi.yaml. A call to a route that does not exist fails
the check.

Why this exists: `check_openapi_drift.py` compares routers, contract docs
and openapi.yaml with each other, and `check_consumer_contract_drift.js`
covers only the response fields of the central `api` object. Neither looks
at what the frontend actually calls, so `PATCH /positions/{id}` (BLG-FE-226,
removed in v9.13 ST-01) and `POST /signals` (BLG-FE-230) went unnoticed.

How a call is resolved:
- The first argument must be a string or template literal. A leading
  `${...}` interpolation followed by `/` is the API base URL and is dropped.
- The query string is dropped: everything from a literal `?`, and a
  trailing `${...}` interpolation whose expression contains `'?'` or `"?"`
  (the `${qs ? '?' + qs : ''}` idiom).
- Any other `${...}` interpolation matches one path segment, the same way
  an openapi `{param}` does.
- The method comes from a `method:` option in the call's argument list.
  A conditional (`method: id ? 'PUT' : 'POST'`) yields every quoted verb in
  the expression, and each is checked. No `method:` option means GET.
- A first argument that is not a literal (a variable, a function call) is
  reported as unresolved and fails the check. Add the call site to
  UNRESOLVED_ALLOW_LIST with the route it reaches, or rewrite it with a
  literal path.
- A literal starting with http:// or https:// is an external call. It must
  match a prefix in EXTERNAL_ALLOW_LIST.

ALLOW_LIST holds calls that intentionally target a route missing from
openapi.yaml. Each entry names its reason and, for a dead method, the
backlog item that removes it and the date it was added. Remove the entry
when the backlog item lands.

Usage:
    python3 scripts/check_frontend_api_calls.py

Exit code 0: every call resolves to an openapi.yaml route. Exit code 1:
one or more calls do not (printed with file and line).
"""
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
OPENAPI_PATH = REPO_ROOT / "docs" / "reference" / "openapi.yaml"
HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")

CALL_RE = re.compile(r"(?<![\w.$])(doFetch|apiFetch)\s*\(")
DEFINITION_RE = re.compile(r"function\s+$")

# "METHOD /path" -> reason. Paths use the same {param} form as openapi.yaml.
ALLOW_LIST = {
    # Dead Base44 client methods with no caller. BLG-FE-230 deletes them.
    # Added 2026-10-28 (ST-23, v9.13); remove when BLG-FE-230 lands.
    "POST /signals": "dead method Signal.create — BLG-FE-230 (allow-listed 2026-10-28)",
    "GET /apps/public/prod/public-settings/by-id/{param}": (
        "dead method getPublicSettingsById, Base44 platform route — BLG-FE-230 (allow-listed 2026-10-28)"
    ),
    "POST /auth/callback": "dead method exchangeCodeForToken — BLG-FE-230 (allow-listed 2026-10-28)",
}

# "relative/file.js:<first argument source>" -> list of "METHOD /path" the
# call reaches. Each listed route is still checked against openapi.yaml.
UNRESOLVED_ALLOW_LIST: dict[str, list[str]] = {
    # Screener scan polling: `url` is one of two template literals for the
    # same route, with and without run_id (Screener.js startPolling).
    "src/pages/Screener.js:url": ["GET /screener/results"],
}

# URL prefixes of intentional calls to a host other than the app's own API.
# A literal first argument starting with http:// or https:// must match one.
EXTERNAL_ALLOW_LIST: dict[str, str] = {}


def _skip_string(text: str, i: int) -> int:
    """Return the index just past the string literal starting at text[i]."""
    quote = text[i]
    i += 1
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if quote == "`" and text.startswith("${", i):
            i = _skip_balanced(text, i + 1, "{", "}")
            continue
        if c == quote:
            return i + 1
        i += 1
    return i


def _skip_balanced(text: str, i: int, open_c: str, close_c: str) -> int:
    """text[i] is open_c. Return the index just past its matching close_c,
    skipping over string and template literals."""
    depth = 0
    while i < len(text):
        c = text[i]
        if c in "'\"`":
            i = _skip_string(text, i)
            continue
        if c == open_c:
            depth += 1
        elif c == close_c:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return i


def _split_top_level_args(args: str) -> list[str]:
    parts, depth, start, i = [], 0, 0, 0
    while i < len(args):
        c = args[i]
        if c in "'\"`":
            i = _skip_string(args, i)
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(args[start:i])
            start = i + 1
        i += 1
    parts.append(args[start:])
    return [p.strip() for p in parts if p.strip()]


def _template_parts(literal: str) -> list[tuple[str, str]]:
    """Split a template literal body into ("text", s) and ("expr", s) parts."""
    parts, i, buf = [], 0, ""
    while i < len(literal):
        if literal[i] == "\\":
            buf += literal[i:i + 2]
            i += 2
            continue
        if literal.startswith("${", i):
            if buf:
                parts.append(("text", buf))
                buf = ""
            end = _skip_balanced(literal, i + 1, "{", "}")
            parts.append(("expr", literal[i + 2:end - 1]))
            i = end
            continue
        buf += literal[i]
        i += 1
    if buf:
        parts.append(("text", buf))
    return parts


def resolve_path(first_arg: str) -> str | None:
    """Turn the call's first argument into an openapi-style path, or None
    if it is not a string or template literal."""
    if len(first_arg) < 2 or first_arg[0] not in "'\"`" or first_arg[-1] != first_arg[0]:
        return None
    body = first_arg[1:-1]
    parts = _template_parts(body) if first_arg[0] == "`" else [("text", body)]

    # A leading interpolation followed by "/" is the API base URL.
    if len(parts) >= 2 and parts[0][0] == "expr" and parts[1][0] == "text" and parts[1][1].startswith("/"):
        parts = parts[1:]

    path = ""
    for kind, value in parts:
        if kind == "text":
            if "?" in value:
                path += value.split("?", 1)[0]
                break
            path += value
        else:
            if re.search(r"""['"]\?""", value):
                break
            path += "{param}"
    if not path.startswith("/"):
        return None
    return path.rstrip("/") or "/"


def resolve_methods(args: list[str]) -> list[str]:
    for arg in args[1:]:
        m = re.search(r"\bmethod\s*:\s*([^,}\n]+)", arg)
        if m:
            verbs = re.findall(r"""['"`](\w+)['"`]""", m.group(1))
            verbs = [v.upper() for v in verbs if v.upper() in HTTP_METHODS]
            return verbs or ["?"]
    return ["GET"]


def extract_calls(text: str) -> list[dict]:
    """Every doFetch/apiFetch call in a JS source string, with line number,
    raw first argument, resolved path (or None) and methods."""
    calls = []
    for m in CALL_RE.finditer(text):
        if DEFINITION_RE.search(text[max(0, m.start() - 20):m.start()]):
            continue
        open_paren = m.end() - 1
        close = _skip_balanced(text, open_paren, "(", ")")
        args = _split_top_level_args(text[open_paren + 1:close - 1])
        if not args:
            continue
        calls.append({
            "line": text.count("\n", 0, m.start()) + 1,
            "first_arg": args[0],
            "path": resolve_path(args[0]),
            "methods": resolve_methods(args),
        })
    return calls


def load_openapi_routes(openapi_path: Path) -> list[tuple[str, re.Pattern]]:
    spec = yaml.safe_load(openapi_path.read_text())
    routes = []
    for path, ops in (spec.get("paths") or {}).items():
        pattern = re.compile("^" + re.sub(r"\\\{[^}]+\\\}", r"[^/]+", re.escape(path.rstrip("/") or "/")) + "$")
        for method in ops or {}:
            if method.upper() in HTTP_METHODS:
                routes.append((method.upper(), pattern))
    return routes


def _route_exists(method: str, path: str, routes) -> bool:
    # {param} stands for any one segment value, so test it as a placeholder.
    concrete = path.replace("{param}", "x")
    return any(m == method and p.match(concrete) for m, p in routes)


def find_missing_calls(src_dir: Path, openapi_path: Path) -> list[str]:
    routes = load_openapi_routes(openapi_path)
    problems = []
    for js in sorted(src_dir.rglob("*.js")):
        if "node_modules" in js.parts or ".test." in js.name:
            continue
        rel = js.relative_to(src_dir.parent).as_posix()
        for call in extract_calls(js.read_text(encoding="utf-8")):
            where = f"{rel}:{call['line']}"
            external = re.match(r"""['"`](https?://[^'"`$]*)""", call["first_arg"])
            if external:
                if not any(external.group(1).startswith(p) for p in EXTERNAL_ALLOW_LIST):
                    problems.append(f"{where}: external call {external.group(1)!r} is not in EXTERNAL_ALLOW_LIST")
                continue
            if call["path"] is None:
                key = f"{rel}:{call['first_arg']}"
                if key not in UNRESOLVED_ALLOW_LIST:
                    problems.append(f"{where}: unresolved path argument {call['first_arg']!r}")
                    continue
                targets = UNRESOLVED_ALLOW_LIST[key]
            else:
                targets = [f"{m} {call['path']}" for m in call["methods"]]
            for target in targets:
                method, path = target.split(" ", 1)
                if target in ALLOW_LIST:
                    continue
                if method == "?":
                    problems.append(f"{where}: could not read the HTTP method for {path}")
                elif not _route_exists(method, path, routes):
                    problems.append(f"{where}: {target} is not in openapi.yaml")
    return problems


def main() -> int:
    if not OPENAPI_PATH.is_file():
        print(f"ERROR: {OPENAPI_PATH} not found.")
        return 1
    problems = find_missing_calls(SRC_DIR, OPENAPI_PATH)
    if problems:
        print("Frontend API Call Existence Check: FAILED — frontend call(s) to a route "
              "missing from docs/reference/openapi.yaml:")
        for p in problems:
            print(f"  - {p}")
        print("")
        print("Fix the call, document the route in openapi.yaml, or add an entry to "
              "ALLOW_LIST / UNRESOLVED_ALLOW_LIST / EXTERNAL_ALLOW_LIST in scripts/check_frontend_api_calls.py "
              "with its reason.")
        return 1
    print("Frontend API Call Existence Check: PASSED — every doFetch/apiFetch call "
          "resolves to an openapi.yaml route.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
