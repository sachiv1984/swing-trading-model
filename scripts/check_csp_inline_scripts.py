#!/usr/bin/env python3
"""Fail when the BUILT index.html runs an inline script its own CSP would block.

BLG-FE-325 (2026-11-19). public/index.html's Content-Security-Policy once allowed
an inline <script> by a sha256 hash computed from the source file. The production
build minifies index.html, so the built script's hash differed and the browser
blocked it in every build, unnoticed: Playwright runs with bypassCSP (the mocks
need it), so no test could see the violation. This check reads the build output,
which is what the browser receives.

For every inline <script> (no src attribute) in <build>/index.html, the sha256 of
its exact text, base64-encoded, must appear as 'sha256-...' in the CSP that governs
<script> elements: script-src-elem, else script-src, else default-src (the browser's
order). 'unsafe-inline' allows inline scripts only when that directive has no hash
or nonce (browsers ignore it otherwise). Every <script src> on this site's own path
must also exist in the build (a missing file is a script that silently never runs).
Exit 1 lists each problem; exit 2 when index.html or the CSP meta tag is missing,
so a broken path never passes.

Limits: reads the meta-tag CSP only (GitHub Pages sends no CSP header); does not
see event-handler attributes (onclick=...) or javascript: URLs; type="application/json"
and other non-JS script types are skipped, as browsers do not execute them; HTML
comments are skipped, as browsers do.

Usage: python3 scripts/check_csp_inline_scripts.py [build_dir]
"""

import base64
import hashlib
import re
import sys
from pathlib import Path

NON_JS_TYPES = {"application/json", "application/ld+json", "text/template", "text/x-template"}


def _policy(html: str):
    # content="..." holds single-quoted keywords ('self'), so match up to the same quote.
    m = re.search(
        r'<meta[^>]+http-equiv=["\']Content-Security-Policy["\'][^>]*content=(["\'])(.*?)\1',
        html, re.I | re.S,
    )
    if not m:
        return None
    directives = {}
    for d in m.group(2).split(";"):
        parts = d.strip().split()
        if parts:
            directives.setdefault(parts[0].lower(), parts[1:])
    return directives


def csp_script_src(html: str):
    """Sources that govern <script> elements, or None when there is no CSP meta tag.

    Returns "unrestricted" when no directive covers scripts (the browser allows them).
    """
    directives = _policy(html)
    if directives is None:
        return None
    for name in ("script-src-elem", "script-src", "default-src"):
        if name in directives:
            return directives[name]
    return "unrestricted"


# One pass in document order: a comment is skipped whole (so "<script>" inside a
# comment is not a script), and a script body is read whole (so "<!--" inside a
# script does not start a comment).
_TOKENS = re.compile(r"<!--.*?-->|<script\b([^>]*)>(.*?)</script\s*>", re.S | re.I)


def scripts(html: str):
    """Yield (attrs, body) for every <script> element outside comments."""
    for m in _TOKENS.finditer(html):
        if m.group(0).startswith("<!--"):
            continue
        yield m.group(1), m.group(2)


def _attr(attrs: str, name: str):
    m = re.search(r'(?:^|\s)' + name + r'\s*=\s*(["\'])(.*?)\1', attrs, re.I | re.S)
    return m.group(2) if m else None


def inline_scripts(html: str):
    for attrs, body in scripts(html):
        if _attr(attrs, "src") is not None:
            continue
        t = _attr(attrs, "type")
        if t and t.strip().lower() in NON_JS_TYPES:
            continue
        yield body


def sha256_source(text: str) -> str:
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode() + "'"


def allows_unsafe_inline(sources) -> bool:
    has_hash_or_nonce = any(x.startswith(("'sha256-", "'sha384-", "'sha512-", "'nonce-")) for x in sources)
    return "'unsafe-inline'" in sources and not has_hash_or_nonce


def check(html: str):
    """Return (sources, list of blocked-script messages); sources None = no CSP meta."""
    sources = csp_script_src(html)
    if sources is None:
        return None, []
    if sources == "unrestricted" or allows_unsafe_inline(sources):
        return sources, []
    blocked = []
    for body in inline_scripts(html):
        h = sha256_source(body)
        if h not in sources:
            snippet = " ".join(body.split())[:80]
            blocked.append(f"inline script {h} not in script-src: {snippet!r}")
    return sources, blocked


def missing_script_files(html: str, build: Path):
    """<script src> files on this site's path that are not in the build.

    A src like /swing-trading-model/spa-redirect.js (production PUBLIC_URL) or
    /spa-redirect.js (root build) maps to build/spa-redirect.js; other origins are skipped.
    """
    missing = []
    for attrs, _ in scripts(html):
        src = _attr(attrs, "src")
        if not src or re.match(r"^(?:[a-z]+:)?//", src, re.I):
            continue
        rel = src.split("?")[0].split("#")[0].lstrip("/")
        candidates = [rel] + ([rel.split("/", 1)[1]] if "/" in rel else [])
        if not any((build / c).is_file() for c in candidates):
            missing.append(f"<script src=\"{src}\"> not found in {build}")
    return missing


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    build = Path(argv[0] if argv else "build")
    index = build / "index.html"
    if not index.is_file():
        print(f"ERROR: {index} not found — build missing or path wrong", file=sys.stderr)
        return 2
    sources, blocked = check(index.read_text(encoding="utf-8"))
    if sources is None:
        print(f"ERROR: no Content-Security-Policy meta tag in {index}", file=sys.stderr)
        return 2
    missing = missing_script_files(index.read_text(encoding="utf-8"), build)
    for msg in blocked:
        print(f"::error title=CSP blocks a built inline script::{msg}")
    for msg in missing:
        print(f"::error title=Script file missing from the build::{msg}")
    if blocked or missing:
        print(f"FAIL: {len(blocked)} inline script(s) blocked by the page's own CSP, {len(missing)} script file(s) missing, in {index}")
        return 1
    print(f"OK: every inline script in {index} is allowed by its CSP, and every local script file exists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
