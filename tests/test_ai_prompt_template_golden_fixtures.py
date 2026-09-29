"""
Golden-fixture CI regression for AI prompt templates (ST-09, BLG-AI-07,
EPIC-03, v9.8).

Problem this closes: boundary-language sampling (BLG-AI-04/BLG-AI-06)
inspects generated *output* text after the fact, so a prompt-template edit
that reintroduces predictive or advice-crossing phrasing is only caught at
the next sample (up to ~90 days). This suite is deterministic and
template-level -- no live API call, no ANTHROPIC_API_KEY required -- and
runs on every CI invocation.

Two checks per covered template:
  1. No disallowed phrase (per strategy_rules.md §13.2, implemented by
     scripts/run_ai_output_boundary_sample_audit.py's scan_prescriptive /
     scan_prediction) appears in the template's static text.
  2. The template's text hash matches the golden fixture's recorded hash
     for the currently-recorded prompt_version -- i.e. if the text changed,
     the source's prompt_version must have changed too. See the fixture
     file's own _metadata for the update procedure.

Covered templates: daily-briefing and chat (backend/services/ai_service.py,
inline `system_prompt` string literals) and the three named system-prompt
constants in gemini_service.py / debrief_service.py.
"""
import ast
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "ai_prompt_template_golden_fixtures.json"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from run_ai_output_boundary_sample_audit import scan_prescriptive, scan_prediction  # noqa: E402


def _load_fixtures():
    return json.loads(FIXTURE_PATH.read_text())["templates"]


def _extract_module_constant_source(file_path: Path, constant_name: str) -> str:
    """Exact source text of a top-level `NAME = "..."` string constant."""
    source = file_path.read_text()
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == constant_name for t in node.targets
        ):
            return ast.get_source_segment(source, node.value)
    raise AssertionError(f"Constant {constant_name!r} not found in {file_path}")


def _extract_function_local_source(file_path: Path, function_name: str, var_name: str) -> str:
    """Exact source text of `var_name = ...` assigned inside function_name."""
    source = file_path.read_text()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            for inner in ast.walk(node):
                if isinstance(inner, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == var_name for t in inner.targets
                ):
                    return ast.get_source_segment(source, inner.value)
            raise AssertionError(f"{var_name!r} not assigned inside {function_name}() in {file_path}")
    raise AssertionError(f"Function {function_name!r} not found in {file_path}")


def _rendered_text_for_scan(entry: dict) -> str:
    """Best-effort literal text for the disallowed-phrase scan: evaluates
    plain string-literal templates; for the chat template (which ends in
    an f-string interpolating live portfolio context) this yields the
    static instructional prefix plus the literal `{portfolio_context}`
    placeholder, since only the fixed template wording is in scope here."""
    file_path = REPO_ROOT / entry["file"]
    if "constant" in entry:
        segment = _extract_module_constant_source(file_path, entry["constant"])
    else:
        segment = _extract_function_local_source(file_path, entry["function"], "system_prompt")
    try:
        # Implicitly-concatenated multi-line string literals (the
        # ai_service.py inline templates) need their enclosing parens back
        # to parse standalone -- ast.get_source_segment only returns the
        # literal's own span, not the `( ... )` wrapper.
        return ast.literal_eval("(" + segment + ")")
    except (ValueError, SyntaxError):
        # Contains an f-string (chat template) -- literal_eval can't evaluate
        # it without live variables. Strip the leading `f` markers and
        # evaluate as a plain string so the static wording can still be
        # scanned; the interpolated portfolio context itself is out of
        # scope for a *template* wording check.
        plain = segment.replace('f"', '"')
        return ast.literal_eval("(" + plain.split("{portfolio_context}")[0] + '")')


def _source_hash(entry: dict) -> str:
    file_path = REPO_ROOT / entry["file"]
    if "constant" in entry:
        segment = _extract_module_constant_source(file_path, entry["constant"])
    else:
        segment = _extract_function_local_source(file_path, entry["function"], "system_prompt")
    return hashlib.sha256(segment.encode()).hexdigest()


def _strip_quoted_examples(text: str) -> str:
    """Drop double-quoted spans before scanning a *prompt* template for
    disallowed phrasing. Prompts legitimately quote the exact phrases they
    forbid the model from producing (e.g. debrief_service.py's
    `_FOCUS_AREA_SYSTEM`: 'Prohibited: "you should", "consider", ...') --
    without this, the instruction-to-avoid-X is indistinguishable from an
    instruction-to-produce-X. This scan is for generation-instruction
    phrasing appearing outside such quoted examples."""
    import re
    return re.sub(r'"[^"]*"', "", text)


class TestNoDisallowedPhraseInTemplates:
    def test_no_covered_template_contains_a_disallowed_phrase(self):
        fixtures = _load_fixtures()
        violations = []
        for key, entry in fixtures.items():
            text = _strip_quoted_examples(_rendered_text_for_scan(entry))
            if scan_prescriptive(text):
                violations.append(f"{key}: prescriptive/directive phrasing found")
            if scan_prediction(text):
                violations.append(f"{key}: predictive/future-certainty phrasing found")
        assert not violations, "Disallowed phrase(s) in AI prompt template(s):\n" + "\n".join(violations)


class TestPromptVersionTracksTemplateText:
    def test_template_text_hash_matches_recorded_prompt_version(self):
        fixtures = _load_fixtures()
        mismatches = []
        for key, entry in fixtures.items():
            live_hash = _source_hash(entry)
            if live_hash != entry["sha256"]:
                mismatches.append(
                    f"{key}: template text changed (hash {entry['sha256'][:12]}... -> {live_hash[:12]}...) "
                    f"but the fixture still records prompt_version {entry['prompt_version']!r}. "
                    f"Bump the version in {entry['file']} and update "
                    f"tests/fixtures/ai_prompt_template_golden_fixtures.json in the same commit."
                )
        assert not mismatches, "\n".join(mismatches)

    def test_fixture_hashes_are_not_placeholders(self):
        fixtures = _load_fixtures()
        for key, entry in fixtures.items():
            assert entry["sha256"] != "PLACEHOLDER", f"{key}: fixture sha256 was never populated"
            assert len(entry["sha256"]) == 64, f"{key}: sha256 does not look like a real digest"
