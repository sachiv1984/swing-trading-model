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
  @babel/parser over all of src/ (scripts/ui_copy_lint_babel_differential.py) it extracts
  every literal except ~0.35% (12,846 of 12,891 at 2026-10-05), all benign: symbol-only JSX text
  with no letters (`•`, `%`), which carries no phrase, and JSX text split by a quote character, whose
  fragments are scanned separately (so a forbidden phrase that itself straddles a quote
  inside JSX text would not be seen).

Obfuscation and split handling (ST-18, BLG-QA-194, EPIC-03, v9.9)
  Before matching, each literal is decoded and folded, so a phrase is seen as the user sees it:
  - JS escapes are decoded: \\uXXXX, \\u{...}, \\xXX (an escaped space such as \\u0020 is a space)
  - HTML numeric and named entities are decoded (`&#160;`, `&#x20;`, `&#32;`, `&ensp;`,
    `&nbsp;`, `&amp;` ...), as JSX itself does for text and attribute strings
  - invisible characters are removed (zero-width space/joiners, word joiner, BOM, soft
    hyphen) and the non-breaking hyphen is folded to `-`; every Unicode space folds to ' '
  - a JSX attribute string that spans lines (`title="you<newline> should"`) is extracted
  - adjacent literals are joined when only these separate them, i.e. when the rendered copy
    is the literals run together: `+` (`'you ' + 'should'`), a JSX expression container
    (`You{' '}should`, `{'you '}{'should'}`), a template-literal `${` / `}` around a string
    literal (`` `you ${'should'}` ``), and bare inline formatting tags with no attributes
    (`<b>Buy</b> now`; b, strong, em, i, u, s, mark, small, code, span, abbr, sub, sup).
    A joined hit is reported only when no single part already matches on its own.
  Accepted limits (deliberate, with rationale):
  - copy assembled at runtime is not joined: `['you', 'should'].join(' ')`, a variable or
    function call between literals (`'you ' + verb`, `` `you ${verb}` ``), `.concat()`,
    ternaries. Resolving those needs data-flow analysis, which a lint of static copy cannot
    do soundly; each piece is still scanned on its own, and review covers the composition.
  - an opening inline tag carrying attributes (`Buy <span className="x">now</span>`) and
    block-level tags do not join: attributes are themselves scanned as separate literals, and
    the tag-text boundary is not tracked through them; joining
    across block elements (`<td>Buy</td><td>now</td>`) would invent phrases the user never
    sees as one run of text.
  - only .js/.jsx are scanned (src/ has no .ts/.tsx today); every string literal is treated
    as copy, including import paths and object keys, so a lexical match there needs an
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
import html
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


# Characters that render as nothing (zero-width space/non-joiner/joiner, word joiner,
# BOM/zero-width no-break space, soft hyphen, Mongolian vowel separator) are dropped; the
# non-breaking hyphen renders as a hyphen. Unicode spaces (NBSP, en/em/thin space ...) are
# already whitespace to str.split() below.
_INVISIBLE_FOLD = str.maketrans({
    "\u200b": None, "\u200c": None, "\u200d": None, "\u2060": None, "\ufeff": None,
    "\u00ad": None, "\u180e": None, "\u2011": "-",
})


def _normalise(text):
    """Decode HTML entities (`&#160;`, `&ensp;`, `&nbsp;`, `&amp;` ...), drop invisible
    characters, then fold every run of whitespace (newlines from wrapped JSX text /
    multi-line templates, tabs, double spaces, Unicode spaces) to one space, so a phrase
    cannot evade the single-space patterns by how the source was wrapped or encoded."""
    return " ".join(html.unescape(text).translate(_INVISIBLE_FOLD).split())


def _decode_escape(source, i):
    """Decode the JS escape sequence starting at the backslash at source[i]. Returns
    (text, consumed). Whitespace escapes become a space (so 'you\\tshould' is seen as
    'you should'); \\uXXXX, \\u{...} and \\xXX become their character; a line
    continuation becomes nothing; any other escaped character stands for itself."""
    nxt = source[i + 1]
    if nxt in "ntrvf":
        return " ", 2
    if nxt == "\n":
        return "", 2
    if nxt == "x":
        m = re.match(r"[0-9A-Fa-f]{2}", source[i + 2:i + 4])
        if m:
            return chr(int(m.group(0), 16)), 4
    if nxt == "u":
        m = re.match(r"\{([0-9A-Fa-f]{1,6})\}|([0-9A-Fa-f]{4})", source[i + 2:i + 10])
        if m:
            code_point = int(m.group(1) or m.group(2), 16)
            if code_point <= 0x10FFFF:
                return chr(code_point), 2 + len(m.group(0))
    return nxt, 2


_JSX_ATTR_STRING_MAX_LINES = 10


def _is_string_opener(source, i, jsx_attribute=False):
    """True if the quote at source[i] opens a real JS string literal. A quote that has no
    closing partner on the same line, or an apostrophe directly after a letter/digit (a
    contraction in JSX text: "It's", "Don't"), is text, not a string -- a string opener is
    never glued to the end of an identifier. With `jsx_attribute` (the quote directly
    follows `name=`), the closing partner may sit up to _JSX_ATTR_STRING_MAX_LINES lines
    later: a JSX attribute string, unlike a JS string, may span lines."""
    quote = source[i]
    if quote == "'" and i > 0 and source[i - 1].isalnum():
        return False
    j = i + 1
    n = len(source)
    newlines = 0
    while j < n:
        if source[j] == "\n":
            newlines += 1
            if not jsx_attribute or newlines > _JSX_ATTR_STRING_MAX_LINES:
                return False
        elif source[j] == "\\":
            j += 2
            continue
        elif source[j] == quote:
            return True
        j += 1
    return False


def extract_literals(source):
    """Return [(line_number, text)] for every string literal / template static part / JSX
    text node in `source`. Comments and regex literals are never returned."""
    return [(line, text) for line, text, _, _ in _extract_literal_spans(source)[0]]


def _extract_literal_spans(source):
    """Return (literals, code): literals is [(line, text, start, end)] in source order, where
    [start, end) is the literal's extent in `source`; code is `source` with every string,
    comment and regex blanked to spaces (same length, newlines kept)."""
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
        start = i
        buf = []
        while i < n:
            c = source[i]
            if c == "\\" and i + 1 < n:
                text, consumed = _decode_escape(source, i)
                buf.append(text)
                for k in range(consumed):
                    if source[i + k] == "\n":
                        line += 1
                    blank(source[i + k])
                i += consumed
                continue
            if c == "`":
                literals.append((start_line, "".join(buf), start, i))
                blank(c)
                i += 1
                mark_literal_end()
                return
            if c == "$" and i + 1 < n and source[i + 1] == "{":
                literals.append((start_line, "".join(buf), start, i))
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
        literals.append((start_line, "".join(buf), start, i))  # unterminated template: keep what we saw

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

        # string literals (a JSX attribute string, directly after `name=`, may span lines)
        jsx_attribute = last_sig == "=" and prev_sig not in ("=", "!", "<", ">")
        if ch in ("'", '"') and not _is_string_opener(source, i, jsx_attribute):
            emit_code(ch)  # apostrophe / stray quote in JSX text -- stays part of the text
            i += 1
            continue
        if ch in ("'", '"'):
            quote = ch
            start_line = line
            start = i
            buf = []
            blank(ch)
            i += 1
            while i < n and source[i] != quote and (jsx_attribute or source[i] != "\n"):
                if source[i] == "\\" and i + 1 < n:
                    text, consumed = _decode_escape(source, i)
                    buf.append(text)
                    for k in range(consumed):
                        if source[i + k] == "\n":
                            line += 1
                        blank(source[i + k])
                    i += consumed
                    continue
                if source[i] == "\n":
                    line += 1
                buf.append(source[i])
                blank(source[i])
                i += 1
            if i < n and source[i] == quote:
                blank(source[i])
                i += 1
            literals.append((start_line, "".join(buf), start, i))
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
            literals.append((code.count("\n", 0, start + first_text_offset) + 1, text, start, m.end(1)))
    literals.sort(key=lambda lit: lit[2])
    return literals, code


# What may separate two literals for their rendered text to be one run: whitespace, `+`
# concatenation, JSX expression-container braces, a template-literal `${`, and bare inline
# formatting tags with no attributes. See the module docstring's accepted limits.
_INLINE_TAGS = "b|strong|em|i|u|s|mark|small|code|span|abbr|sub|sup"
_JOINABLE_GAP_RE = re.compile(r"(?:\s|\+|\{|\}|\$\{|</?(?:" + _INLINE_TAGS + r")\s*>)*")


def _joined_runs(literals, code):
    """Yield (line, joined_text, parts) for each maximal run of 2+ adjacent literals that
    only joinable gaps separate."""
    run = []
    for lit in literals + [None]:
        if lit is not None and run and _JOINABLE_GAP_RE.fullmatch(code[run[-1][3]:lit[2]]):
            run.append(lit)
            continue
        if len(run) > 1:
            yield run[0][0], "".join(part[1] for part in run), run
        run = [lit] if lit is not None else []


def scan_text(source):
    """Return [(line, matched_phrase, literal_text)] for every forbidden phrase found, in a
    single literal or in a run of adjacent literals that render as one piece of text (a run
    is reported only if no single part of it already matches on its own)."""
    literals, code = _extract_literal_spans(source)
    hits = []
    matched = set()
    for idx, (line, text, _, _) in enumerate(literals):
        normalised = _normalise(text)
        m = _PHRASE_RE.search(normalised)
        if m:
            hits.append((line, m.group(0), normalised))
            matched.add(idx)
    index_of = {id(lit): idx for idx, lit in enumerate(literals)}
    for line, joined, parts in _joined_runs(literals, code):
        if any(index_of[id(part)] in matched for part in parts):
            continue
        normalised = _normalise(joined)
        m = _PHRASE_RE.search(normalised)
        if m:
            hits.append((line, m.group(0), normalised))
    hits.sort(key=lambda hit: hit[0])
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
