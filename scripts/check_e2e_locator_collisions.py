#!/usr/bin/env python3
"""
E2E locator-collision check (ST-21, BLG-QA-268, EPIC-04, v9.18).

execution_prompt.md §3.1.A step 13 asks for a grep of tests/e2e/ for unscoped
locators that match text a story adds, removes, hides or moves. Done by hand it
was missed twice at v9.17: ST-01's new caption "Sorted by what needs attention
first" and new aria-expanded row chevrons broke SC-COMP-03/07, and ST-03 moved
the grace banner copy into a collapsed strip entry that SC-LBG-03 still
asserted. Both failed CI on the story commit. This script does the grep.

What it reads from a diff of src/**/*.js(x):
  1. changed text: string literals and JSX text on added or removed lines;
  2. changed attributes: aria-*, role, title, placeholder, alt, data-testid
     and name attributes on added lines;
  3. moved text: every string inside a component whose JSX usage (<Name ...>)
     is on an added or removed line. A component placed in a collapsed panel,
     another page or a new parent keeps its own lines unchanged, so (1) cannot
     see its text.

What it matches in tests/e2e/**/*.js: locators called directly on `page`
(unscoped): page.getByText, page.getByRole(..., { name }), page.getByLabel,
page.getByPlaceholder, page.getByTitle, and attribute selectors inside
page.locator('...'). A string argument matches as Playwright does by default
(case-insensitive substring, or whole string with exact: true); a regex
argument is run against the text. Template literals are tried with sample
values for each ${...} (the string literals inside it, "", 1 and 2).

Limits (stated, not hidden): text built at run time outside the diffed file
(API data, a constant imported from another module) is not seen; a locator
held in a variable or built with string concatenation is not parsed; scoped
locators (on a locator, not on page) are skipped, since scoping is the fix.
Matches are for review: scope the locator, or confirm it still targets the
right element.

Usage:
  python3 scripts/check_e2e_locator_collisions.py              # staged diff
  python3 scripts/check_e2e_locator_collisions.py --commit SHA  # one commit, tests at SHA
  python3 scripts/check_e2e_locator_collisions.py --diff-file F --src-root DIR --tests-dir DIR
Exit 0 = no match (or no src/ change); 1 = matches listed; 2 = usage error.
"""
import argparse
import itertools
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FILE = re.compile(r"^src/.*\.jsx?$")
# Unit tests and their helpers live under src/ but never render.
NOT_RENDERED = re.compile(r"(?:\.(?:test|spec)\.jsx?$|/__tests__/|^src/test-utils/|^src/setupTests\.js$)")
STRING_LIT = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'|`((?:[^`\\]|\\.)*)`', re.S)
ATTR = re.compile(r"\b(aria-[a-z]+|role|title|placeholder|alt|name)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|\{)")
JSX_TAG = re.compile(r"<([A-Z][A-Za-z0-9_]*)\b")
CLASS_TOKEN = re.compile(r"^[!-]?[a-z0-9]+(?:[:/.\-\[\]%#()][a-z0-9.\[\]%#()/:-]*)*$")
PLACEHOLDER = "\x00"


# ---------------------------------------------------------------- git access

def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], check=True, capture_output=True, text=True).stdout


class Source:
    """Reads post-change file contents and test files from one place."""

    def __init__(self, mode, rev=None, src_root=None, tests_dir=None):
        self.mode, self.rev, self.src_root = mode, rev, src_root
        self.tests_dir = tests_dir

    def read(self, path):
        try:
            if self.mode == "dir":
                with open(os.path.join(self.src_root, path), encoding="utf-8") as f:
                    return f.read()
            if self.mode == "commit":
                return git("show", f"{self.rev}:{path}")
            return git("show", f":{path}")  # the index, for a staged diff
        except (OSError, subprocess.CalledProcessError):
            return None

    def test_files(self):
        if self.tests_dir:
            for base, _dirs, files in os.walk(self.tests_dir):
                for name in sorted(files):
                    if name.endswith(".js"):
                        path = os.path.join(base, name)
                        with open(path, encoding="utf-8") as f:
                            yield os.path.relpath(path, self.tests_dir), f.read()
            return
        if self.mode == "commit":
            names = git("ls-tree", "-r", "--name-only", self.rev, "tests/e2e").split()
            for name in names:
                if name.endswith(".js"):
                    yield name, git("show", f"{self.rev}:{name}")
            return
        e2e = os.path.join(ROOT, "tests", "e2e")
        for base, _dirs, files in os.walk(e2e):
            for name in sorted(files):
                if name.endswith(".js"):
                    path = os.path.join(base, name)
                    with open(path, encoding="utf-8") as f:
                        yield os.path.relpath(path, ROOT), f.read()


# ------------------------------------------------------------- diff parsing

def parse_diff(text):
    """{path: {"added": [line], "removed": [line]}} for src/**/*.js(x)."""
    files, current = {}, None
    for line in text.splitlines():
        if line.startswith("diff --git "):
            current = None
        elif line.startswith("+++ "):
            path = line[4:].strip()
            path = path[2:] if path.startswith("b/") else path
            current = files.setdefault(path, {"added": [], "removed": []}) if SRC_FILE.match(path) and not NOT_RENDERED.search(path) else None
        elif line.startswith("--- "):
            continue
        elif current is not None and line.startswith("+"):
            current["added"].append(line[1:])
        elif current is not None and line.startswith("-"):
            current["removed"].append(line[1:])
    return files


# ------------------------------------------------------- visible strings

def is_comment(line):
    s = line.strip()
    return s.startswith(("//", "/*", "*", "{/*"))


def looks_visible(text):
    """A literal that could be on screen: not a class list, path, key or id."""
    s = text.strip()
    if re.search(r"[{}]", s):
        return False  # a fragment of a template literal split across lines
    if len(re.findall(r"[A-Za-z]", s.replace(PLACEHOLDER, ""))) < 2:
        return False
    if s.startswith(("./", "../", "/", "@", "http", "#/", "data:")) or re.fullmatch(r"#[0-9A-Fa-f]{3,8}", s):
        return False
    tokens = s.replace(PLACEHOLDER, "x").split()
    if all(CLASS_TOKEN.match(t) for t in tokens) and (len(tokens) > 1 or not s[0].isupper()):
        return False  # a class list, test id, key or lowercase identifier
    return True


def is_jsx_text(text):
    """Text that reads as a JSX child, not code: no operators once {expr} is removed."""
    bare = re.sub(r"\{[^{}]*\}", "", text).strip()
    if not bare or not re.match(r"[A-Za-z0-9£$%(]", bare):
        return False
    if re.search(r"[=;<>\"'`{}]|&&|\|\||^[\w.]+\s*:\s|,$|^\w+\(", bare):
        return False
    return True


def template_parts(body):
    """Split a template literal body into literal text and ${...} expressions."""
    parts, i, out = [], 0, ""
    while i < len(body):
        if body.startswith("${", i):
            depth, j = 1, i + 2
            while j < len(body) and depth:
                depth += {"{": 1, "}": -1}.get(body[j], 0)
                j += 1
            parts.append(out)
            parts.append(("expr", body[i + 2:j - 1]))
            out, i = "", j
        else:
            out += body[i]
            i += 1
    parts.append(out)
    return parts


def jsx_text_parts(text):
    """JSX text with {expr} children, as template parts."""
    parts, last = [], 0
    for m in re.finditer(r"\{([^{}]*)\}", text):
        parts.append(text[last:m.start()])
        parts.append(("expr", m.group(1)))
        last = m.end()
    parts.append(text[last:])
    return parts


def strings_in(lines):
    """Visible strings in some source lines, each as template parts."""
    found = []
    for line in lines:
        if is_comment(line) or line.lstrip().startswith(("import ", "export {")):
            continue
        for m in STRING_LIT.finditer(line):
            if m.group(3) is not None:
                parts = template_parts(m.group(3))
            else:
                parts = [m.group(1) if m.group(1) is not None else m.group(2)]
            if looks_visible("".join(p if isinstance(p, str) else PLACEHOLDER for p in parts)):
                found.append(parts)
        # JSX text between tags on one line: >Some text<
        for m in re.finditer(r">([^<>]*[A-Za-z][^<>]*)<", line):
            if not is_jsx_text(m.group(1)):
                continue
            parts = jsx_text_parts(m.group(1))
            if looks_visible("".join(p if isinstance(p, str) else PLACEHOLDER for p in parts)):
                found.append(parts)
        # A JSX text line on its own: no code punctuation once {expr} is removed.
        if " " in line.strip() and is_jsx_text(line):
            parts = jsx_text_parts(line.strip())
            if looks_visible("".join(p if isinstance(p, str) else PLACEHOLDER for p in parts)):
                found.append(parts)
    return found


def instances(parts, cap=64):
    """Sample renderings of template parts, each as (text, literal mask).

    The mask marks characters that come from the source's own literal text, as
    opposed to a sample value standing in for ${...}.
    """
    choices = []
    for p in parts:
        if isinstance(p, str):
            choices.append([(p, True)])
        else:
            lits = [a or b or c for a, b, c in re.findall(r'"([^"]*)"|\'([^\']*)\'|`([^`$]*)`', p[1])]
            choices.append([(v, False) for v in dict.fromkeys(lits + ["", "1", "2"])])
    out = []
    for combo in itertools.product(*choices):
        text = "".join(v for v, _ in combo)
        mask = [lit for v, lit in combo for _ in v]
        out.append((text, mask))
        if len(out) >= cap:
            break
    return out


def display(parts):
    return "".join(p if isinstance(p, str) else "${" + p[1] + "}" for p in parts)


# ------------------------------------------------------ component bodies

def component_body(source_text, name):
    """Lines of a top-level component definition, or None."""
    lines = source_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^(?:export\s+(?:default\s+)?)?(?:function\s+{name}\b|(?:const|let)\s+{name}\s*=)", line):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^(?:export\s+(?:default\s+)?)?(?:async\s+)?(?:function\s|const\s|let\s|class\s)", lines[j]):
            end = j
            break
    return lines[start:end]


def resolve_import(source_text, name, path):
    """The file a component is imported from, as a repo path, or None."""
    m = re.search(rf"import\s+(?:{name}\b|[^;]*\{{[^}}]*\b{name}\b[^}}]*\}})[^;]*from\s+[\"']([^\"']+)[\"']", source_text)
    if not m or not m.group(1).startswith("."):
        return None
    base = os.path.normpath(os.path.join(os.path.dirname(path), m.group(1)))
    return [base + ext for ext in ("", ".js", ".jsx", "/index.js")]


def moved_strings(src, path, lines_changed):
    """Strings inside components whose JSX usage is on a changed line."""
    names = sorted({m.group(1) for line in lines_changed if not is_comment(line) for m in JSX_TAG.finditer(line)})
    text = src.read(path) or ""
    found = []
    for name in names:
        body, where = component_body(text, name), path
        if body is None:
            for candidate in resolve_import(text, name, path) or []:
                other = src.read(candidate)
                if other is not None:
                    body, where = component_body(other, name), candidate
                    break
        if body:
            found.extend((parts, f"{where} <{name}>") for parts in strings_in(body))
    return found


# --------------------------------------------------------------- locators

JS_ARG = r"""(?:'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|`(?:[^`\\$]|\\.)*`|/(?:[^/\\\n]|\\.)+/[a-z]*)"""
TEXT_LOCATOR = re.compile(rf"\bpage\.(getByText|getByLabel|getByPlaceholder|getByTitle)\(\s*({JS_ARG})\s*(,\s*\{{[^}}]*\}})?\s*\)", re.S)
ROLE_LOCATOR = re.compile(rf"\bpage\.getByRole\(\s*({JS_ARG})\s*,\s*\{{([^}}]*)\}}\s*\)", re.S)
CSS_LOCATOR = re.compile(r"""\bpage\.locator\(\s*(['"`])(.+?)\1""", re.S)
NAME_OPT = re.compile(rf"\bname\s*:\s*({JS_ARG})", re.S)
CSS_ATTR = re.compile(r"\[([a-zA-Z-]+)(?:\s*([*^$~|]?=)\s*[\"']?([^\]\"']*)[\"']?)?\]")
SCENARIO = re.compile(r"\btest(?:\.only|\.skip)?\(\s*['\"`]([A-Z][A-Z0-9]*-[A-Z0-9-]*\d[a-z]?)")


def js_arg(arg):
    """(kind, value): ('str', text) or ('re', compiled) or (None, None)."""
    if arg[0] in "'\"`":
        return "str", re.sub(r"\\(.)", r"\1", arg[1:-1])
    m = re.match(r"^/(.*)/([a-z]*)$", arg, re.S)
    flags = (re.I if "i" in m.group(2) else 0) | (re.S if "s" in m.group(2) else 0) | (re.M if "m" in m.group(2) else 0)
    try:
        # JS named groups (?<n>...) are (?P<n>...) in Python; lookbehinds stay.
        return "re", re.compile(re.sub(r"\(\?<(?![=!])", "(?P<", m.group(1)), flags)
    except re.error:
        return None, None


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


MIN_LITERAL_LETTERS = 3


def _literal_letters(text, mask, start, end):
    return sum(1 for i in range(start, end) if mask[i] and text[i].isalpha())


def text_matches(kind, value, exact, candidates):
    """Whether a locator argument matches a rendering of the text.

    A match must cover at least MIN_LITERAL_LETTERS letters of the source's
    own text, so a sample ${...} value ("1") or a two-letter overlap ("BP" in
    "GBP") alone is not a collision.
    """
    for text, mask in candidates:
        if kind == "re":
            m = value.search(text)
            if m and _literal_letters(text, mask, m.start(), m.end()) >= MIN_LITERAL_LETTERS:
                return True
        elif kind == "str":
            v, t = norm(value), norm(text)
            if exact:
                if t == v and sum(c.isalpha() for c in v) >= MIN_LITERAL_LETTERS:
                    return True
                continue
            i = text.lower().find(v.lower()) if v else -1
            if i < 0 and v.lower() in t.lower():
                return sum(c.isalpha() for c in v) >= MIN_LITERAL_LETTERS
            if i >= 0 and _literal_letters(text, mask, i, i + len(v)) >= MIN_LITERAL_LETTERS:
                return True
    return False


def scenario_for(text, offset):
    ids = [m.group(1) for m in SCENARIO.finditer(text, 0, offset)]
    return ids[-1] if ids else "-"


def find_collisions(src, diff_text):
    files = parse_diff(diff_text)
    if not files:
        return [], 0
    pools = []  # (tier, parts, origin)
    attrs = []  # (name, literal value or None, origin)
    for path, ch in files.items():
        for tier, lines in (("added", ch["added"]), ("removed", ch["removed"])):
            pools.extend((tier, parts, path) for parts in strings_in(lines))
        for line in ch["added"]:
            if is_comment(line):
                continue
            for m in ATTR.finditer(line):
                attrs.append((m.group(1), m.group(2) if m.group(2) is not None else m.group(3), path))
        pools.extend(("moved", parts, origin) for parts, origin in moved_strings(src, path, ch["added"] + ch["removed"]))
    rendered = [(tier, parts, origin, instances(parts)) for tier, parts, origin in pools]

    hits = []
    for test_path, text in src.test_files():
        for m in TEXT_LOCATOR.finditer(text):
            kind, value = js_arg(m.group(2))
            exact = bool(m.group(3) and re.search(r"exact\s*:\s*true", m.group(3)))
            if kind:
                hits += _text_hits(test_path, text, m, kind, value, exact, rendered)
        for m in ROLE_LOCATOR.finditer(text):
            name = NAME_OPT.search(m.group(2))
            if name:
                kind, value = js_arg(name.group(1))
                exact = bool(re.search(r"exact\s*:\s*true", m.group(2)))
                if kind:
                    hits += _text_hits(test_path, text, m, kind, value, exact, rendered)
        for m in CSS_LOCATOR.finditer(text):
            for a in CSS_ATTR.finditer(m.group(2)):
                for name, value, origin in attrs:
                    if a.group(1) != name:
                        continue
                    # [attr] matches any added attr; [attr="v"] only a literal "v".
                    # A dynamic value ({...}) is unknown, so it never matches a value selector.
                    if a.group(2) and (value is None or not _css_value_match(a.group(2), a.group(3), value)):
                        continue
                    hits.append(_hit(test_path, text, m, "attribute", f"{name}" + (f'="{value}"' if value is not None else "={…}"), origin))
                    break
    return _dedupe(hits), len(files)


def _css_value_match(op, want, value):
    return {"=": value == want, "*=": want in value, "^=": value.startswith(want),
            "$=": value.endswith(want), "~=": want in value.split(), "|=": value == want or value.startswith(want + "-")}.get(op, False)


def _text_hits(test_path, text, m, kind, value, exact, rendered):
    out = []
    for tier, parts, origin, cands in rendered:
        if text_matches(kind, value, exact, cands):
            out.append(_hit(test_path, text, m, tier, display(parts), origin))
    return out


def _hit(test_path, text, m, tier, what, origin):
    line = text.count("\n", 0, m.start()) + 1
    return {
        "test": f"{test_path}:{line}",
        "scenario": scenario_for(text, m.start()),
        "locator": norm(m.group(0))[:120],
        "tier": tier,
        "text": norm(what)[:100],
        "origin": origin,
    }


def _dedupe(hits):
    seen, out = set(), []
    for h in hits:
        key = (h["test"], h["locator"], h["tier"], h["text"])
        if key not in seen:
            seen.add(key)
            out.append(h)
    return out


TIER_NOTE = {
    "added": "matches text this diff adds",
    "removed": "matches text this diff removes",
    "moved": "matches text in a component this diff moves, hides or re-parents",
    "attribute": "matches an attribute this diff adds",
}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--commit", help="check one commit's src/ diff against tests/e2e at that commit")
    p.add_argument("--diff-file", help="a unified diff to check (with --src-root)")
    p.add_argument("--src-root", help="directory holding the post-change src/ files for --diff-file")
    p.add_argument("--tests-dir", help="directory of e2e test files (default: tests/e2e)")
    args = p.parse_args(argv)

    if args.diff_file:
        if not args.src_root:
            p.error("--diff-file needs --src-root")
        with open(args.diff_file, encoding="utf-8") as f:
            diff_text = f.read()
        src = Source("dir", src_root=args.src_root, tests_dir=args.tests_dir)
    elif args.commit:
        diff_text = git("show", "--format=", args.commit, "--", "src")
        src = Source("commit", rev=args.commit, tests_dir=args.tests_dir)
    else:
        diff_text = git("diff", "--cached", "--", "src")
        src = Source("index", tests_dir=args.tests_dir)

    hits, n_files = find_collisions(src, diff_text)
    if n_files == 0:
        print("OK: no src/**/*.js(x) change in the diff; locator-collision check not needed")
        return 0
    if not hits:
        print(f"OK: {n_files} src file(s) changed; no unscoped tests/e2e locator matches their changed, moved or hidden text")
        return 0
    print(f"LOCATOR COLLISIONS: {len(hits)} unscoped tests/e2e locator use(s) match text or attributes this diff changes.")
    print("Scope each one (to a test ID, region or exact match) or confirm it still finds the intended element.\n")
    groups = {}
    for h in hits:
        groups.setdefault((h["locator"], h["tier"], h["text"], h["origin"]), []).append(f"{h['test']} [{h['scenario']}]")
    for (locator, tier, text, origin), where in groups.items():
        print(f"  {locator}")
        print(f"      {TIER_NOTE[tier]}: \"{text}\" ({origin})")
        for w in where[:6]:
            print(f"      - {w}")
        if len(where) > 6:
            print(f"      - … and {len(where) - 6} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
