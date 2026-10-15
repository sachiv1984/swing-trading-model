#!/usr/bin/env python3
"""Strategy-copy lint (ST-21, BLG-GOV-369, EPIC-03, v9.12).

Lists user-facing text in src/ that restates strategy_rules.md §5–§11 numbers
or formulas and disagrees with them, and strategy-number literals in the pages
that must take those numbers from src/constants/strategy.js.

Two kinds of finding:

  CONTRADICTION  anywhere in src/ (outside src/constants/strategy.js): text
                 that states an ATR multiple other than the §11 initial/losing
                 or profitable multiplier, an ATR period other than the §11
                 period, a grace length other than the §11 grace period, or a
                 stop formula the rules do not use ("High − N×ATR"; the §7.2
                 stop is measured from the current price).
  LITERAL        in the pages named by ST-21 AC 1 (TradeEntry.js, Settings.js,
                 Positions.js, SignalContextPanel.js): a §11 number written as
                 a literal in strategy text instead of read from the constants
                 module.

The expected values are parsed from strategy_rules.md §11 itself, so the lint
follows the rules document, not a copy of it. Comments are ignored: only code
and UI text are checked.

Ownership: the Frontend Specifications & UX Documentation Owner triages every
finding (claude/agents/frontend_specs_ux_documentation_owner.md §7,
Strategy-copy conformance; Director of HR ruling ESC-EXEC-20261013-08).

Usage:
  python3 scripts/check_strategy_copy.py            # report; exit 0 (CI warning)
  python3 scripts/check_strategy_copy.py --strict   # exit 1 on any finding
In GitHub Actions each finding is also emitted as a ::warning annotation.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / "claude" / "strategy" / "strategy_rules.md"
SRC = ROOT / "src"
CONSTANTS = SRC / "constants" / "strategy.js"
LITERAL_PAGES = (
    SRC / "pages" / "TradeEntry.js",
    SRC / "pages" / "Settings.js",
    SRC / "pages" / "Positions.js",
    SRC / "components" / "trades" / "SignalContextPanel.js",
)

TIMES = r"\s*[×x*]\s*"
NUM = r"(\d+(?:\.\d+)?)"


@dataclass(frozen=True)
class Params:
    grace_days: float
    initial_mult: float
    profit_mult: float
    atr_period: float


@dataclass(frozen=True)
class Finding:
    kind: str
    path: Path
    line: int
    text: str
    message: str

    def render(self) -> str:
        rel = self.path.relative_to(ROOT)
        return f"{self.kind} {rel}:{self.line}: {self.message} -- {self.text.strip()[:140]}"


def parse_section_11(rules_text: str) -> Params:
    """Read the four §11 production parameters from strategy_rules.md."""
    match = re.search(r"^## 11\..*?$(.*?)^## 12\.", rules_text, re.M | re.S)
    if not match:
        raise SystemExit("strategy_rules.md: §11 'Current production parameters' not found")
    body = match.group(1)

    def grab(pattern: str, label: str) -> float:
        m = re.search(pattern, body, re.I)
        if not m:
            raise SystemExit(f"strategy_rules.md §11: could not read {label}")
        return float(m.group(1))

    return Params(
        grace_days=grab(r"Grace period:\s*" + NUM, "grace period"),
        initial_mult=grab(r"Initial / losing stop multiplier:\s*" + NUM, "initial multiplier"),
        profit_mult=grab(r"Profitable stop multiplier:\s*" + NUM, "profitable multiplier"),
        atr_period=grab(r"ATR period:\s*" + NUM, "ATR period"),
    )


_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
# A line comment: // not preceded by ':' (URLs) or by a quote/word character.
_LINE_COMMENT = re.compile(r"(?<![:\w'\"`])//.*$", re.M)


def strip_comments(source: str) -> str:
    """Blank out JS comments, keeping line numbers."""
    source = _BLOCK_COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), source)
    return _LINE_COMMENT.sub("", source)


def _same(a: float, b: float) -> bool:
    return abs(a - b) < 1e-9


# Patterns are applied per line of comment-stripped source.
MULT_BEFORE = re.compile(NUM + TIMES + r"ATR\b", re.I)          # "5×ATR", "5 × ATR"
MULT_AFTER = re.compile(r"\bATR" + TIMES + NUM, re.I)            # "ATR × 2.0"
ATR_PERIOD = re.compile(
    NUM + r"[- ]day\s+ATR\b|\bATR\s*\(" + NUM + r"[- ]day|\bATR period:?\s*" + NUM
    + r"|\bATR\s*\(\s*" + NUM + r"\s*d\b|" + NUM + r"d\s+ATR\b",  # "ATR (14d)", "14d ATR"
    re.I,
)
GRACE_LEN = re.compile(
    r"\bgrace[^.\"'`]{0,40}?\(?\b" + NUM + r"\s+(?:calendar\s+|trading\s+)?days?\b"
    r"|\b" + NUM + r"[- ](?:calendar[- ])?day\s+grace\b",
    re.I,
)
# Code: "5 * signal.atr_value", "atrValue * 2".
MULT_CODE = re.compile(r"(?<![\w.])" + NUM + r"\s*\*\s*(?:[\w]+\.)*atr(?:_value|Value)?\b|\b(?:[\w]+\.)*atr(?:_value|Value)?\s*\*\s*" + NUM + r"(?![\w.])", re.I)
# Grace day counters: "Day {n} of 10".
GRACE_DAY_OF = re.compile(r"\bDay\s*\{[^}]*\}\s*of\s+" + NUM + r"\b")
# Any "N-day" phrase in a page that must use the constants module.
N_DAY = re.compile(r"(?<![\w$])" + NUM + r"-day\b(?!\s*MA\b)", re.I)  # the 200-day MA is §8.2, not a §11 parameter
HIGH_FORMULA = re.compile(r"\b(?:highest\s+)?high\s*[−-]\s*\d", re.I)
INTERPOLATED = re.compile(r"\$\{[A-Z_]+\}|\{[A-Z_]+\}")


def _first(m: re.Match) -> float:
    return float(next(g for g in m.groups() if g is not None))


def scan_line(line: str, params: Params) -> list[str]:
    """Return contradiction messages for one line of code/UI text."""
    out = []
    allowed_mults = {params.initial_mult, params.profit_mult}
    for pat in (MULT_BEFORE, MULT_AFTER, MULT_CODE):
        for m in pat.finditer(line):
            value = _first(m)
            if not any(_same(value, a) for a in allowed_mults):
                out.append(
                    f"ATR multiple {value:g} is not a §11 multiplier "
                    f"({params.initial_mult:g} initial/losing, {params.profit_mult:g} profitable)"
                )
    for m in ATR_PERIOD.finditer(line):
        value = _first(m)
        if not _same(value, params.atr_period):
            out.append(f"ATR period {value:g} differs from §11 ({params.atr_period:g} days)")
    for m in list(GRACE_LEN.finditer(line)) + list(GRACE_DAY_OF.finditer(line)):
        value = _first(m)
        if not _same(value, params.grace_days):
            out.append(f"grace length {value:g} days differs from §11 ({params.grace_days:g} days)")
    if HIGH_FORMULA.search(line):
        out.append("stop formula measured from the high; §7.2 measures it from the current price")
    return out


def literal_line(line: str) -> bool:
    """True if a strategy statement on this line writes a §11 number as a literal."""
    for pat in (MULT_BEFORE, MULT_AFTER, MULT_CODE, ATR_PERIOD, GRACE_LEN, GRACE_DAY_OF, N_DAY):
        if pat.search(line):
            return True
    return False


def iter_source_files() -> list[Path]:
    return sorted(
        p for p in SRC.rglob("*")
        if p.suffix in {".js", ".jsx", ".ts", ".tsx"} and p != CONSTANTS and "__tests__" not in p.parts
    )


def run(params: Params) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_source_files():
        code = strip_comments(path.read_text(encoding="utf-8"))
        is_literal_page = path in LITERAL_PAGES
        for i, line in enumerate(code.splitlines(), start=1):
            for message in scan_line(line, params):
                findings.append(Finding("CONTRADICTION", path, i, line, message))
            if is_literal_page and literal_line(INTERPOLATED.sub("", line)):
                findings.append(Finding(
                    "LITERAL", path, i, line,
                    "strategy number written as a literal; import it from src/constants/strategy.js",
                ))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true", help="exit 1 on any finding")
    args = parser.parse_args(argv)

    params = parse_section_11(RULES.read_text(encoding="utf-8"))
    missing = [p for p in LITERAL_PAGES if not p.exists()]
    if missing:
        print("strategy-copy: page(s) named by ST-21 not found: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))
        return 2
    findings = run(params)

    print(
        f"strategy-copy: §11 grace {params.grace_days:g} days, initial/losing {params.initial_mult:g}×ATR, "
        f"profitable {params.profit_mult:g}×ATR, ATR period {params.atr_period:g} days"
    )
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for f in findings:
        print(f.render())
        if in_actions:
            print(f"::warning file={f.path.relative_to(ROOT)},line={f.line},title=strategy-copy {f.kind}::{f.message}")
    contradictions = sum(f.kind == "CONTRADICTION" for f in findings)
    literals = sum(f.kind == "LITERAL" for f in findings)
    print(f"strategy-copy: {contradictions} contradiction(s), {literals} literal(s)")
    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
