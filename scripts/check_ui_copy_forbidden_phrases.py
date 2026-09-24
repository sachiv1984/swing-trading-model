#!/usr/bin/env python3
"""
CI lint of static UI copy for forbidden predictive or advice-crossing phrases
(ST-07, BLG-FE-183, EPIC-02, v9.7).

`claude/strategy/strategy_rules.md` §13.2 says this system is not an automated trading
bot, not a discretionary/adaptive rule system, and not an AI-driven prediction system.
Until now the only control on *static* UI copy (as distinct from AI-generated output,
which `scripts/run_ai_output_boundary_sample_audit.py` samples quarterly) was human
review. This lint scans the string literals and JSX text in `src/` against the same
prescriptive ("you should", "we recommend", "buy now" ...) and prediction ("will rise",
"is expected to", "forecast" ...) phrase lists that audit already maintains -- imported
from it, not copied, so there is one canonical list to update.

What is scanned
  - JS string literals ('...', "...") and the static parts of template literals
  - JSX text nodes (the text between tags)
  Comments are never scanned. Test files (*.test.js, *.spec.js) and `__tests__`
  directories are skipped -- test descriptions are not user-facing copy.
  The scanner is a dependency-free tokeniser, not a full JS parser. Checked against
  @babel/parser over all of src/ (211 files, ~12,000 literals) it extracts every literal
  except ~0.1%, all benign: JSX text that contains an HTML entity (`&amp;`) and JSX text
  split by a quote character, whose fragments are scanned separately (so a forbidden phrase
  that itself straddles a quote inside JSX text would not be seen).
  Known limits: a phrase split across concatenated literals (`'you ' + 'should'`) is not
  joined; only .js/.jsx are scanned (src/ has no .ts/.tsx today); every string literal is
  treated as copy, including import paths and object keys, so a lexical match there needs an
  allow-list entry; code such as `a > forecast && b < 3` can read as JSX text.

Allow-list (scripts/ui_copy_lint_allowlist.json)
  A reviewed, legitimate use of a listed phrase (for example, copy that *negates* the
  phrase, or retrospective wording) is recorded as
      {"file": "src/...", "literal": "<the literal's exact text>", "justification": "<why>"}
  - The entry is keyed on the file AND the literal's exact (whitespace-normalised) text,
    so it suppresses only that literal -- a *new* literal using the same phrase, in the
    same file or anywhere else, still fails.
  - `justification` is required (>= 20 characters). An entry without one is itself a
    violation: an unjustified exception is not an exception.
  - An entry that no longer matches any literal is a violation too ("stale"), so the
    list cannot silently rot -- remove it when the copy it covered is gone.

Usage: python3 scripts/check_ui_copy_forbidden_phrases.py
Exit code 0 = clean, 1 = violations found (each is printed with file:line).
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SRC_DIR = REPO_ROOT / "src"
ALLOWLIST_PATH = Path(__file__).parent / "ui_copy_lint_allowlist.json"

sys.path.insert(0, str(Path(__file__).parent))
from run_ai_output_boundary_sample_audit import (  # noqa: E402
    _PREDICTION_PATTERNS,
    _PRESCRIPTIVE_PATTERNS,
)

_PHRASE_RE = re.compile("|".join(_PRESCRIPTIVE_PATTERNS + _PREDICTION_PATTERNS), re.IGNORECASE)

MIN_JUSTIFICATION_LENGTH = 20
_SCANNED_SUFFIXES = {".js", ".jsx"}
_SKIPPED_NAME_RE = re.compile(r"\.(test|spec)\.jsx?$")

# After one of these (or at the start of the file), a `/` begins a regex literal, not division.
# Deliberately excludes `<`, `>` and `}`: there a `/` is a JSX closing tag (`</div>`) or a
# self-closing tag (`<Foo bar={x} />`), which must not be mistaken for a regex. The one
# `>` case that IS regex context, an arrow `=>`, is handled where this set is used.
_REGEX_PRECEDING_CHARS = set("(,=:[!&|?{;+-*%~^")
_REGEX_PRECEDING_KEYWORDS = ("return", "typeof", "case", "do", "else", "in", "of", "delete", "void", "throw")


def _normalise(text):
    """Fold every run of whitespace (newlines from wrapped JSX text / multi-line templates,
    tabs, double spaces, non-breaking spaces and the literal `&nbsp;` entity) to one space,
    so a phrase cannot evade the single-space patterns by how the source was wrapped."""
    return " ".join(text.replace("&nbsp;", " ").split())


def _unescape(ch):
    """The character an escape `\\<ch>` stands for, as far as phrase matching cares: the
    whitespace escapes become a space (so 'you\\tshould' is seen as 'you should'); any other
    escaped character stands for itself."""
    return " " if ch in "ntr" else ch


def _is_string_opener(source, i):
    """True if the quote at source[i] opens a real JS string literal. A quote that has no
    closing partner on the same line, or an apostrophe directly after a letter/digit (a
    contraction in JSX text: "It's", "Don't"), is text, not a string -- a string opener is
    never glued to the end of an identifier."""
    quote = source[i]
    if quote == "'" and i > 0 and source[i - 1].isalnum():
        return False
    j = i + 1
    n = len(source)
    while j < n and source[j] != "\n":
        if source[j] == "\\":
            j += 2
            continue
        if source[j] == quote:
            return True
        j += 1
    return False


def extract_literals(source):
    """Return [(line_number, text)] for every string literal / template static part / JSX
    text node in `source`. Comments and regex literals are never returned."""
    literals = []
    blanked = []  # the source with strings/comments/regexes replaced by spaces (newlines kept)
    n = len(source)
    i = 0
    line = 1
    last_sig = ""  # last significant (non-space) character emitted as code
    prev_sig = ""  # the significant character before that
    last_word = ""
    prev_word = False

    def emit_code(ch):
        nonlocal last_sig, prev_sig, last_word, prev_word
        blanked.append(ch)
        is_word = ch.isalnum() or ch in "_$"
        if is_word:
            last_word = (last_word + ch) if prev_word else ch
            prev_sig, last_sig = last_sig, ch
        elif not ch.isspace():
            last_word = ""
            prev_sig, last_sig = last_sig, ch
        prev_word = is_word

    def blank(ch):
        blanked.append("\n" if ch == "\n" else " ")

    def mark_literal_end():
        nonlocal last_sig, prev_sig, last_word, prev_word
        prev_sig, last_sig, last_word, prev_word = last_sig, '"', "", False

    template_stack = []  # brace depth at which each open `${` began
    brace_depth = 0

    def scan_template_part():
        """Consume template-literal text from position i up to the closing backtick, or up to
        (and including) the next `${`, in which case the expression is left for the main loop."""
        nonlocal i, line, brace_depth
        start_line = line
        buf = []
        while i < n:
            c = source[i]
            if c == "\\" and i + 1 < n:
                buf.append(_unescape(source[i + 1]))
                if source[i + 1] == "\n":
                    line += 1
                blank(c), blank(source[i + 1])
                i += 2
                continue
            if c == "`":
                blank(c)
                i += 1
                literals.append((start_line, "".join(buf)))
                mark_literal_end()
                return
            if c == "$" and i + 1 < n and source[i + 1] == "{":
                literals.append((start_line, "".join(buf)))
                emit_code("$"), emit_code("{")
                i += 2
                template_stack.append(brace_depth)
                brace_depth += 1
                return
            if c == "\n":
                line += 1
                blanked.append("\n")
            else:
                blank(c)
            buf.append(c)
            i += 1
        literals.append((start_line, "".join(buf)))  # unterminated template: keep what we saw

    while i < n:
        ch = source[i]
        nxt = source[i + 1] if i + 1 < n else ""

        if ch == "\n":
            line += 1
            blanked.append("\n")
            i += 1
            continue

        # comments
        if ch == "/" and nxt == "/" and last_sig != ":":  # `https://` in JSX text is not a comment
            while i < n and source[i] != "\n":
                blank(source[i])
                i += 1
            continue
        if ch == "/" and nxt == "*":
            blank(ch), blank(nxt)
            i += 2
            while i < n and not (source[i] == "*" and i + 1 < n and source[i + 1] == "/"):
                if source[i] == "\n":
                    line += 1
                blank(source[i])
                i += 1
            if i < n:
                blank(source[i]), blank(source[i + 1])
                i += 2
            continue

        # string literals
        if ch in ("'", '"') and not _is_string_opener(source, i):
            emit_code(ch)  # apostrophe / stray quote in JSX text -- stays part of the text
            i += 1
            continue
        if ch in ("'", '"'):
            quote = ch
            start_line = line
            buf = []
            blank(ch)
            i += 1
            while i < n and source[i] != quote and source[i] != "\n":
                if source[i] == "\\" and i + 1 < n:
                    buf.append(_unescape(source[i + 1]))
                    blank(source[i]), blank(source[i + 1])
                    i += 2
                    continue
                buf.append(source[i])
                blank(source[i])
                i += 1
            if i < n and source[i] == quote:
                blank(source[i])
                i += 1
            literals.append((start_line, "".join(buf)))
            mark_literal_end()
            continue

        # template literals: static parts are scanned; each `${ ... }` expression is tokenised as
        # ordinary code (so a string literal inside it is scanned too) via the brace-depth stack.
        if ch == "`":
            blank(ch)
            i += 1
            scan_template_part()
            continue

        # regex literals (so a quote inside /['"]/ cannot derail the string tracking)
        if ch == "/" and (
            last_sig == ""
            or last_sig in _REGEX_PRECEDING_CHARS
            or (last_sig == ">" and prev_sig == "=")
            or last_word in _REGEX_PRECEDING_KEYWORDS
        ):
            blank(ch)
            i += 1
            in_class = False
            while i < n and source[i] != "\n":
                c = source[i]
                if c == "\\" and i + 1 < n:
                    blank(c), blank(source[i + 1])
                    i += 2
                    continue
                if c == "[":
                    in_class = True
                elif c == "]":
                    in_class = False
                elif c == "/" and not in_class:
                    blank(c)
                    i += 1
                    break
                blank(c)
                i += 1
            while i < n and source[i].isalpha():  # flags
                blank(source[i])
                i += 1
            prev_sig, last_sig, last_word, prev_word = last_sig, "/", "", False
            continue

        if ch == "{":
            brace_depth += 1
        elif ch == "}":
            brace_depth -= 1
            if template_stack and template_stack[-1] == brace_depth:
                template_stack.pop()
                blank(ch)  # the `}` closing a template expression is template syntax, not code
                i += 1
                scan_template_part()
                continue
        emit_code(ch)
        i += 1

    # JSX text: text between a closing `>` / `}` and the next `<` / `{`, in the code channel
    # (strings and comments already blanked, so what remains is code + JSX text). An arrow
    # `=>` is not a tag close, so a `>` preceded by `=` is skipped.
    code = "".join(blanked)
    for m in re.finditer(r"(?<![=\-])[>}]([^<>{}]*)[<{]", code):
        text = m.group(1)
        if re.search(r"[A-Za-z]", text):
            start = m.start(1)
            first_text_offset = len(text) - len(text.lstrip())
            literals.append((code.count("\n", 0, start + first_text_offset) + 1, text))
    return literals


def scan_text(source):
    """Return [(line, matched_phrase, literal_text)] for every forbidden phrase found."""
    hits = []
    for line, text in extract_literals(source):
        normalised = _normalise(text)
        m = _PHRASE_RE.search(normalised)
        if m:
            hits.append((line, m.group(0), normalised))
    return hits


def load_allowlist(path):
    """Return (entries, problems). Entries without a usable justification are problems."""
    problems = []
    if not path.exists():
        return [], problems
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [], [f"{path.name}: not valid JSON ({exc})"]
    entries = raw.get("entries", []) if isinstance(raw, dict) else []
    valid = []
    for idx, entry in enumerate(entries):
        where = f"{path.name} entry #{idx + 1}"
        if not isinstance(entry, dict) or not entry.get("file") or not entry.get("literal"):
            problems.append(f'{where}: must have both "file" and "literal"')
            continue
        justification = str(entry.get("justification", "")).strip()
        if len(justification) < MIN_JUSTIFICATION_LENGTH:
            problems.append(
                f'{where} ({entry["file"]}): "justification" is required '
                f"(>= {MIN_JUSTIFICATION_LENGTH} characters) -- an unjustified exception is not an exception"
            )
            continue
        valid.append({"file": entry["file"], "literal": _normalise(entry["literal"])})
    return valid, problems


def iter_source_files(src_dir):
    for path in sorted(src_dir.rglob("*")):
        if path.suffix not in _SCANNED_SUFFIXES or not path.is_file():
            continue
        if _SKIPPED_NAME_RE.search(path.name) or "__tests__" in path.parts:
            continue
        yield path


def check_tree(src_dir, allowlist_path, repo_root=None):
    """Return a list of human-readable violation strings (empty = clean)."""
    repo_root = repo_root or REPO_ROOT  # resolved at call time so tests can point it at a tmp tree
    entries, problems = load_allowlist(allowlist_path)
    violations = list(problems)
    used = set()
    for path in iter_source_files(src_dir):
        rel = path.relative_to(repo_root).as_posix()
        for line, phrase, literal in scan_text(path.read_text(encoding="utf-8", errors="replace")):
            key = (rel, literal)
            if any(e["file"] == rel and e["literal"] == literal for e in entries):
                used.add(key)
                continue
            violations.append(
                f'{rel}:{line}: forbidden phrase "{phrase}" in UI copy: "{literal[:120]}"'
                f" -- reword it, or add an allow-list entry with a justification"
            )
    for e in entries:
        if (e["file"], e["literal"]) not in used:
            violations.append(
                f'{allowlist_path.name}: stale entry for {e["file"]} ("{e["literal"][:80]}") '
                f"matches no forbidden-phrase literal any more -- remove it"
            )
    return violations


def main():
    violations = check_tree(SRC_DIR, ALLOWLIST_PATH)
    if violations:
        print(f"UI copy boundary lint FAILED -- {len(violations)} violation(s):")
        for v in violations:
            print(f"  - {v}")
        print("\nSee strategy_rules.md §13.2 and scripts/check_ui_copy_forbidden_phrases.py's docstring.")
        return 1
    print("UI copy boundary lint: PASSED (no forbidden predictive/advice-crossing phrases in src/ UI copy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
