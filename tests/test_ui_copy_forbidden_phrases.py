"""
UI copy boundary lint — ST-07 (EPIC-02, v9.7, BLG-FE-183).

Unit tests for scripts/check_ui_copy_forbidden_phrases.py: extraction of string literals /
template parts / JSX text, detection of the §13.2 prescriptive and prediction phrases, the
justified-allow-list mechanism, and a regression guard that the real src/ tree is clean.
Mirrors the test_non_registry_dependency_check.py / test_playwright_skip_only_check.py
convention for this class of CI lint.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import check_ui_copy_forbidden_phrases as lint  # noqa: E402
import run_ai_output_boundary_sample_audit as audit  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent


def _phrases(source):
    return [phrase.lower() for _, phrase, _ in lint.scan_text(source)]


def _make_tree(tmp_path, files, allowlist=None):
    src = tmp_path / "src"
    for rel, body in files.items():
        f = src / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(body, encoding="utf-8")
    al = tmp_path / "allowlist.json"
    if allowlist is not None:
        al.write_text(json.dumps(allowlist), encoding="utf-8")
    return src, al


# ── AC-01: CI fails on a disallowed phrase in a new string literal ──────────────────

def test_disallowed_phrase_in_a_new_string_literal_fails(tmp_path):
    """The exact scenario this story exists to catch: a PR adds a new literal with a listed phrase."""
    src, al = _make_tree(tmp_path, {"pages/New.js": 'export const msg = "You should sell now";\n'})
    violations = lint.check_tree(src, al, repo_root=tmp_path)
    assert len(violations) == 1
    assert "src/pages/New.js:1" in violations[0]
    assert "you should" in violations[0].lower()


def test_main_exits_nonzero_on_a_violation_and_zero_when_clean(tmp_path, monkeypatch, capsys):
    """Runs the real main() (the entry point CI invokes) against a tmp tree, not a stub."""
    src, al = _make_tree(tmp_path, {"A.js": 'const x = "we recommend buying";\n'})
    monkeypatch.setattr(lint, "SRC_DIR", src)
    monkeypatch.setattr(lint, "ALLOWLIST_PATH", al)
    monkeypatch.setattr(lint, "REPO_ROOT", tmp_path)

    assert lint.main() == 1
    out = capsys.readouterr().out
    assert "FAILED" in out and "src/A.js:1" in out

    (src / "A.js").write_text('const x = "Realised P&L is net of recorded fees.";\n', encoding="utf-8")
    assert lint.main() == 0
    assert "PASSED" in capsys.readouterr().out


@pytest.mark.parametrize("source, expected", [
    ('const a = "you should reduce your position";', "you should"),
    ("const a = 'We recommend this setup';", "we recommend"),
    ("const a = `Buy now while it lasts`;", "buy now"),
    ('const a = "Price will rise next week";', "will rise"),
    ('const a = "This is expected to climb";', "is expected to"),
    ('const a = "A 3-month forecast";', "forecast"),
    ("const a = <p>You must act today</p>;", "you must"),
    ("const a = <Input placeholder=\"Consider reducing size\" />;", "consider reducing"),
    ("const a = <p>Total {n} — this is likely to rise</p>;", "is likely to"),
])
def test_forbidden_phrase_detected_in_each_kind_of_ui_copy(source, expected):
    assert expected in _phrases(source)


def test_phrase_inside_a_template_literal_expression_is_detected():
    """A string literal nested in a `${ ... }` expression is still user-facing copy."""
    assert "you should" in _phrases('const a = `Status: ${ok ? "fine" : "you should exit"}`;')
    assert "we recommend" in _phrases("const a = `x ${y ? `n ${z ? 'we recommend' : ''}` : ''}`;")


@pytest.mark.parametrize("source", [
    "<p>\n  You\n  should reduce\n</p>",           # Prettier-wrapped JSX text
    "<p>We\n   recommend this</p>",
    "const a = `you\nshould`;",                      # multi-line template literal
    "const a = 'you  should';",                       # double space
    "const a = 'you\\tshould';",                     # tab escape
    "const a = <p>Buy&nbsp;now</p>;",                 # literal &nbsp; entity
    "const a = <p>Buy\u00a0now</p>;",                 # non-breaking space character
])
def test_phrase_is_detected_however_its_whitespace_is_wrapped(source):
    """A compliance gate must not be evadable by line-wrapping or irregular whitespace."""
    assert lint.scan_text(source), source


def test_url_in_jsx_text_is_not_mistaken_for_a_line_comment():
    assert "you should" in _phrases("const a = <p>See https://example.com, then you should sell</p>;")
    # ...but a real line comment right after code is still ignored.
    assert lint.scan_text('const a = "ok"; // you should never be flagged\n') == []


def test_reported_literal_text_is_whitespace_normalised():
    (_, _, literal), = lint.scan_text("const a = `you\n   should sell`;")
    assert literal == "you should sell"


def test_benign_copy_is_not_flagged():
    src = """
    const a = "Realised P&L is net of recorded fees.";
    const b = <p>Includes 2 restated months — see the Monthly tab for details.</p>;
    const c = `${count} closed trades have no fees recorded`;
    """
    assert lint.scan_text(src) == []


def test_comments_are_never_scanned():
    src = """
    // you should never see this flagged
    /* we recommend nothing; will rise; forecast */
    const a = "fine"; // buy now
    const b = <p>{/* you must not flag JSX comments */}ok</p>;
    """
    assert lint.scan_text(src) == []


# ── tokeniser regressions: constructs that could derail string/JSX tracking ─────────

def test_jsx_closing_and_self_closing_tags_do_not_swallow_following_text():
    src = '<div><Foo bar={x} /><p>fine</p><b>You must act</b></div>'
    assert _phrases(src) == ["you must"]


def test_apostrophe_in_jsx_text_does_not_hide_the_rest_of_the_line():
    assert "you should" in _phrases("const a = <p>It's simple. You should sell</p>;")


def test_regex_literal_containing_quotes_does_not_derail_the_scan():
    src = 'const re = /[\'"]you must/g;\nconst a = "we recommend this";\n'
    assert _phrases(src) == ["we recommend"]  # the regex itself is not UI copy; the next literal is


def test_arrow_function_gt_is_not_a_jsx_tag_close():
    assert _phrases("const f = (x) => x > 1 ? <span>buy now</span> : null;") == ["buy now"]


def test_line_numbers_are_reported_correctly_across_multiline_constructs():
    src = 'const a = 1;\n/* c1\n c2 */\nconst t = `line1\nline2`;\nconst b = "you must";\n'
    assert [line for line, _, _ in lint.scan_text(src)] == [6]


def test_test_files_and_tests_directories_are_skipped(tmp_path):
    src, al = _make_tree(tmp_path, {
        "components/Foo.test.js": 'const a = "you should";',
        "components/Foo.spec.js": 'const a = "you should";',
        "components/__tests__/Bar.js": 'const a = "you should";',
        "components/Real.js": 'const a = "ok";',
    })
    assert lint.check_tree(src, al, repo_root=tmp_path) == []


# ── AC-02: allow-list entries require a justification ───────────────────────────────

JUSTIFICATION = "Reflective question posed to the user, not an instruction to trade."


def _entry(**overrides):
    e = {"file": "src/A.js", "literal": "Why enter now?", "justification": JUSTIFICATION}
    e.update(overrides)
    return e


def test_justified_allowlist_entry_suppresses_exactly_that_literal(tmp_path):
    src, al = _make_tree(tmp_path, {"A.js": 'const p = "Why enter now?";\n'}, {"entries": [_entry()]})
    assert lint.check_tree(src, al, repo_root=tmp_path) == []


def test_allowlist_entry_does_not_cover_a_new_literal_with_the_same_phrase(tmp_path):
    """The entry is keyed on the literal's text: a NEW literal using the phrase still fails."""
    src, al = _make_tree(
        tmp_path,
        {"A.js": 'const p = "Why enter now?";\nconst q = "Enter now before it is too late";\n'},
        {"entries": [_entry()]},
    )
    violations = lint.check_tree(src, al, repo_root=tmp_path)
    assert len(violations) == 1
    assert "src/A.js:2" in violations[0]


def test_allowlist_entry_is_scoped_to_its_file(tmp_path):
    src, al = _make_tree(
        tmp_path,
        {"A.js": 'const p = "Why enter now?";\n', "B.js": 'const p = "Why enter now?";\n'},
        {"entries": [_entry()]},
    )
    violations = lint.check_tree(src, al, repo_root=tmp_path)
    assert len(violations) == 1 and "src/B.js" in violations[0]


@pytest.mark.parametrize("bad_entry", [
    {"file": "src/A.js", "literal": "Why enter now?"},                      # no justification at all
    {"file": "src/A.js", "literal": "Why enter now?", "justification": ""},  # empty
    {"file": "src/A.js", "literal": "Why enter now?", "justification": "ok"},  # too short to be a reason
    {"file": "src/A.js", "literal": "Why enter now?", "justification": "   " * 10},  # whitespace only
])
def test_allowlist_entry_without_a_justification_is_itself_a_violation(tmp_path, bad_entry):
    src, al = _make_tree(tmp_path, {"A.js": 'const p = "Why enter now?";\n'}, {"entries": [bad_entry]})
    violations = lint.check_tree(src, al, repo_root=tmp_path)
    assert any("justification" in v for v in violations)
    # ...and an unjustified entry must NOT suppress the underlying flag either.
    assert any("src/A.js:1" in v for v in violations)


def test_allowlist_entry_missing_file_or_literal_is_a_violation(tmp_path):
    src, al = _make_tree(tmp_path, {"A.js": 'const p = "ok";\n'},
                         {"entries": [{"literal": "x", "justification": JUSTIFICATION}]})
    assert any('"file" and "literal"' in v for v in lint.check_tree(src, al, repo_root=tmp_path))


def test_stale_allowlist_entry_is_a_violation(tmp_path):
    src, al = _make_tree(tmp_path, {"A.js": 'const p = "all clean now";\n'}, {"entries": [_entry()]})
    violations = lint.check_tree(src, al, repo_root=tmp_path)
    assert len(violations) == 1 and "stale" in violations[0]


def test_invalid_allowlist_json_is_a_violation(tmp_path):
    src, _ = _make_tree(tmp_path, {"A.js": 'const p = "ok";\n'})
    al = tmp_path / "allowlist.json"
    al.write_text("{not json", encoding="utf-8")
    assert any("not valid JSON" in v for v in lint.check_tree(src, al, repo_root=tmp_path))


def test_missing_allowlist_file_means_no_exceptions(tmp_path):
    src, al = _make_tree(tmp_path, {"A.js": 'const p = "you must";\n'})
    assert not al.exists()
    assert len(lint.check_tree(src, al, repo_root=tmp_path)) == 1


# ── single source of truth + real-tree regression guard ─────────────────────────────

def test_phrase_lists_are_the_ai_output_audits_own_lists_not_a_copy():
    """One canonical §13.2 list to maintain: the lint must import, not duplicate, the audit's."""
    assert lint._PRESCRIPTIVE_PATTERNS is audit._PRESCRIPTIVE_PATTERNS
    assert lint._PREDICTION_PATTERNS is audit._PREDICTION_PATTERNS


def test_real_src_tree_and_allowlist_are_clean_today():
    """Regression guard: the shipped src/ passes with the shipped allow-list (every entry justified,
    none stale). A failure here means new UI copy crossed the §13.2 boundary language — reword it."""
    violations = lint.check_tree(REPO_ROOT / "src", lint.ALLOWLIST_PATH, repo_root=REPO_ROOT)
    assert violations == [], "\n".join(violations)


def test_real_allowlist_entries_all_carry_a_justification():
    raw = json.loads(lint.ALLOWLIST_PATH.read_text(encoding="utf-8"))
    assert raw["entries"], "allow-list unexpectedly empty (the TradePlan placeholder is the baseline entry)"
    for e in raw["entries"]:
        assert len(e["justification"].strip()) >= lint.MIN_JUSTIFICATION_LENGTH, e
