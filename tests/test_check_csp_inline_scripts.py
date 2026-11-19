"""BLG-FE-325: scripts/check_csp_inline_scripts.py.

The check must fail on every form it claims to catch (an inline script whose
hash is missing, including the exact minified-vs-source mismatch that hid
BLG-FE-325), pass the allowed forms, and never pass a missing file or CSP.
"""

import base64
import hashlib
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "check_csp_inline_scripts", Path(__file__).parent.parent / "scripts" / "check_csp_inline_scripts.py"
)
csp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(csp)


def h(text):
    return "sha256-" + base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()


def page(script_src, *scripts):
    meta = f'<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src {script_src}; style-src \'self\';" />'
    return "<html><head>" + meta + "".join(scripts) + "</head><body></body></html>"


def write(tmp_path, html, files=("spa-redirect.js", "a.js")):
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "index.html").write_text(html)
    for f in files:
        (tmp_path / f).write_text("//")
    return tmp_path


SOURCE = "\n      (function(l) { if (l.search[1] === '/') { } }(window.location))\n    "
MINIFIED = "!function(l){l.search[1]}(window.location)"


def test_no_inline_scripts_passes(tmp_path):
    assert csp.main([str(write(tmp_path, page("'self'", '<script src="/spa-redirect.js"></script>')))]) == 0


def test_hashed_inline_script_passes(tmp_path):
    html = page(f"'self' '{h(MINIFIED)}'", f"<script>{MINIFIED}</script>")
    assert csp.main([str(write(tmp_path, html))]) == 0


def test_source_hash_with_minified_build_fails(tmp_path, capsys):
    # The BLG-FE-325 case: CSP hash computed from the source text, build ships minified text.
    html = page(f"'self' '{h(SOURCE)}'", f'<script type="text/javascript">{MINIFIED}</script>')
    assert csp.main([str(write(tmp_path, html))]) == 1
    assert "not in script-src" in capsys.readouterr().out


def test_unhashed_inline_script_fails(tmp_path):
    assert csp.main([str(write(tmp_path, page("'self'", "<script>alert(1)</script>")))]) == 1


def test_one_of_two_scripts_unhashed_fails(tmp_path):
    html = page(f"'self' '{h('a()')}'", "<script>a()</script>", "<script>b()</script>")
    assert csp.main([str(write(tmp_path, html))]) == 1


def test_unsafe_inline_allows_inline(tmp_path):
    assert csp.main([str(write(tmp_path, page("'self' 'unsafe-inline'", "<script>x()</script>")))]) == 0


def test_unsafe_inline_is_ignored_when_a_hash_is_present(tmp_path):
    # Browsers ignore 'unsafe-inline' once the directive has a hash or nonce.
    html = page(f"'self' 'unsafe-inline' '{h('a()')}'", "<script>a()</script>", "<script>b()</script>")
    assert csp.main([str(write(tmp_path, html))]) == 1


def test_script_src_elem_takes_precedence(tmp_path):
    meta = lambda pol: f'<meta http-equiv="Content-Security-Policy" content="{pol}" />'  # noqa: E731
    hashed = f"script-src 'self' '{h('a()')}'; script-src-elem 'self'"
    assert csp.main([str(write(tmp_path, meta(hashed) + "<script>a()</script>"))]) == 1
    relaxed = "script-src 'self'; script-src-elem 'self' 'unsafe-inline'"
    assert csp.main([str(write(tmp_path / "b", meta(relaxed) + "<script>a()</script>"))]) == 0


def test_no_script_directive_means_unrestricted(tmp_path):
    html = '<meta http-equiv="Content-Security-Policy" content="style-src \'self\'" /><script>x()</script>'
    assert csp.main([str(write(tmp_path, html))]) == 0


def test_data_src_is_not_src(tmp_path):
    assert csp.main([str(write(tmp_path, page("'self'", '<script data-src="x">x()</script>')))]) == 1


def test_comment_marker_inside_a_script_is_script_text(tmp_path):
    body = "var s = '<!--'; run();"
    html = page(f"'self' '{h(body)}'", f"<script>{body}</script>", "<!-- c -->", "<script>later()</script>")
    # The first script is hashed correctly; the later unhashed one must still be caught.
    _, blocked = csp.check(html)
    assert len(blocked) == 1 and "later()" in blocked[0]


def test_missing_local_script_file_fails(tmp_path):
    html = page("'self'", '<script src="/swing-trading-model/spa-redirect.js"></script>', '<script src="/gone.js"></script>')
    assert csp.main([str(write(tmp_path, html))]) == 1
    # Production subpath maps to the build root; an external origin is not checked.
    html = page("'self'", '<script src="/swing-trading-model/spa-redirect.js"></script>', '<script src="https://cdn.example/x.js"></script>')
    assert csp.main([str(write(tmp_path / "ok", html))]) == 0


def test_json_script_is_not_executed_so_not_checked(tmp_path):
    html = page("'self'", '<script type="application/json">{"a":1}</script>')
    assert csp.main([str(write(tmp_path, html))]) == 0


def test_default_src_fallback_when_no_script_src(tmp_path):
    html = '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'" /><script>x()</script>'
    assert csp.main([str(write(tmp_path, html))]) == 1


def test_missing_index_or_csp_exits_2(tmp_path):
    assert csp.main([str(tmp_path / "nope")]) == 2
    assert csp.main([str(write(tmp_path, "<html><script>x()</script></html>"))]) == 2


def test_script_text_inside_a_comment_is_ignored(tmp_path):
    html = page("'self'", "<!-- no inline <script> in this document -->", '<script src="/a.js"></script>')
    assert csp.main([str(write(tmp_path, html))]) == 0
    # ...but a real inline script after a comment is still checked.
    html = page("'self'", "<!-- note -->", "<script>x()</script>")
    assert csp.main([str(write(tmp_path, html))]) == 1


def test_repo_public_index_has_no_inline_script():
    # The source page itself: after BLG-FE-325 there is nothing inline to hash.
    html = (Path(__file__).parent.parent / "public" / "index.html").read_text()
    sources, blocked = csp.check(html)
    assert sources is not None and blocked == []
