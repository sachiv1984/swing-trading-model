#!/usr/bin/env python3
"""
Read-only live-schema vs docs/specs/data_model.md drift detector
(ST-28, EPIC-05, v9.9, BLG-SPEC-157).

v9.5 found 5 live-vs-spec divergences by hand (BLG-SPEC-148/149/150/151/154:
missing index, documented-but-missing column, undocumented live columns,
a nullable mismatch, an undocumented CHECK constraint). This script
mechanises that comparison so it can be re-run instead of re-derived by hand:

- Parses each "## N. <Table Name> Table" section's CREATE TABLE block (for
  the table name) and its "### Fields" markdown table (for the documented
  column set + nullability).
- Parses every `CREATE [UNIQUE] INDEX [IF NOT EXISTS] <name>` statement in
  the whole document for documented index names.
- Parses every `ADD CONSTRAINT <name> CHECK (...)` statement for documented
  named CHECK constraints.
- Against a read-only DATABASE_URL, queries information_schema.columns,
  pg_indexes, and pg_constraint for the live state, and reports:
    - undocumented live columns (live, not in the Fields table)
    - missing columns (documented, not live)
    - nullable mismatches (documented vs live disagree)
    - missing indexes (documented CREATE INDEX name not found live)
    - missing CHECK constraints (documented ADD CONSTRAINT name not found live)
    - default mismatches (ST-37, EPIC-06, v9.13, BLG-SPEC-184): a column's
      `DEFAULT` in its section's CREATE TABLE block disagrees with the live
      `column_default`, including a documented default with none live
      (`fees_paid DEFAULT 0`, found by hand in v9.9) and the reverse.
      Postgres casts and quoting are normalised first, so `0` vs
      `0::numeric` and `'[]'::jsonb` vs `'[]'` match. Only columns listed
      in the CREATE TABLE block are compared; a column added later by
      ALTER TABLE has no documented default to compare.

Runs read-only wherever DATABASE_URL is available; refuses to run any
write statement itself regardless of the connected role's privileges.

Usage:
    python3 scripts/check_data_model_drift.py docs/specs/data_model.md
    python3 scripts/check_data_model_drift.py docs/specs/data_model.md --json
"""
import argparse
import decimal
import json
import os
import re
import sys
from pathlib import Path

TABLE_SECTION_RE = re.compile(r"^##\s+\d+\.\s+(.+?)\s+Table\s*$", re.M)
CREATE_TABLE_NAME_RE = re.compile(r"CREATE TABLE\s+(\w+)\s*\(", re.I)
FIELDS_TABLE_ROW_RE = re.compile(
    r"^\|\s*([A-Za-z_][\w]*)\s*\|\s*([^|]+?)\s*\|\s*(YES|NO)\s*\|", re.M
)
INDEX_RE = re.compile(r"CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF NOT EXISTS\s+)?(\w+)", re.I)
CHECK_CONSTRAINT_RE = re.compile(r"ADD CONSTRAINT\s+(\w+)\s+CHECK", re.I)

# ST-37 (BLG-SPEC-184): column defaults.
TABLE_CONSTRAINT_WORDS = {"PRIMARY", "UNIQUE", "CONSTRAINT", "FOREIGN", "CHECK", "EXCLUDE"}
SERIAL_TYPES = {"SERIAL", "BIGSERIAL", "SMALLSERIAL"}
COLUMN_DEFAULT_RE = re.compile(
    r"\bDEFAULT\s+(.+?)(?:\s+(?:NOT\s+NULL|NULL|PRIMARY\s+KEY|REFERENCES|UNIQUE|CHECK|CONSTRAINT|GENERATED|COLLATE)\b.*)?$",
    re.I | re.S,
)
QUOTED_RE = re.compile(r"'(?:[^']|'')*'")
CAST_RE = re.compile(
    r"::\s*\"?[A-Za-z_]\w*\"?"
    r"(?:\s+(?:varying|precision|with(?:out)?\s+time\s+zone))*"
    r"(?:\s*\(\s*\d+(?:\s*,\s*\d+)?\s*\))?(?:\[\])?",
    re.I,
)


def parse_table_sections(text: str):
    """Return {table_name: {field: nullable_bool}} for each '## N. X Table' section."""
    headers = list(re.finditer(r"^##\s+\d+\.\s+.+?\s+Table\s*$", text, re.M))
    tables = {}
    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]
        name_m = CREATE_TABLE_NAME_RE.search(block)
        if not name_m:
            continue
        table_name = name_m.group(1)
        fields_idx = block.find("### Fields")
        fields_block = block[fields_idx:] if fields_idx != -1 else block
        next_heading = re.search(r"\n#{2,3}\s", fields_block[1:])
        if next_heading:
            fields_block = fields_block[: next_heading.start() + 1]
        fields = {}
        for row in FIELDS_TABLE_ROW_RE.finditer(fields_block):
            field, _type, nullable = row.groups()
            if field.lower() in ("field", "---", "-------"):
                continue
            fields[field] = (nullable == "YES")
        if fields:
            tables[table_name] = fields
    return tables


def _create_table_columns(block: str, open_paren: int):
    """Split the CREATE TABLE column list starting at block[open_paren] into
    top-level definitions (commas inside parentheses or quotes do not split)."""
    body = "\n".join(line.split("--", 1)[0] for line in block[open_paren + 1:].split("\n"))
    parts, depth, current, quoted = [], 0, [], False
    for ch in body:
        if ch == "'":
            quoted = not quoted
        elif not quoted and ch == "(":
            depth += 1
        elif not quoted and ch == ")":
            if depth == 0:
                break
            depth -= 1
        elif not quoted and ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    parts.append("".join(current).strip())
    return [p for p in parts if p]


def parse_documented_defaults(text: str):
    """Return {table_name: {column: default_expr_or_None}} from each
    '## N. X Table' section's CREATE TABLE block. SERIAL types are recorded
    as a nextval() default, which is what Postgres creates for them."""
    headers = list(re.finditer(r"^##\s+\d+\.\s+.+?\s+Table\s*$", text, re.M))
    tables = {}
    for i, m in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[m.end():end]
        name_m = CREATE_TABLE_NAME_RE.search(block)
        if not name_m:
            continue
        columns = {}
        for definition in _create_table_columns(block, name_m.end() - 1):
            words = definition.split()
            if len(words) < 2 or words[0].upper() in TABLE_CONSTRAINT_WORDS:
                continue
            if words[1].upper() in SERIAL_TYPES:
                columns[words[0]] = "nextval()"
                continue
            d = COLUMN_DEFAULT_RE.search(definition)
            columns[words[0]] = d.group(1).strip() if d else None
        if columns:
            tables[name_m.group(1)] = columns
    return tables


def _strip_parens(s: str) -> str:
    while s.startswith("(") and s.endswith(")"):
        inner, depth = s[1:-1], 0
        for ch in inner:
            depth += {"(": 1, ")": -1}.get(ch, 0)
            if depth < 0:
                return s
        s = inner.strip()
    return s


def normalize_default(expr):
    """Canonical form of a column default for comparison, or None for no
    default. Drops ::type casts outside quotes, unquotes a bare literal,
    compares numbers numerically, lower-cases unquoted SQL, treats
    CURRENT_TIMESTAMP as now() and any nextval(...) as one sequence default."""
    if expr is None:
        return None
    s = _strip_parens(expr.strip())
    pieces, last = [], 0
    for q in QUOTED_RE.finditer(s):
        pieces.append(CAST_RE.sub("", s[last:q.start()]).lower())
        pieces.append(q.group(0))
        last = q.end()
    pieces.append(CAST_RE.sub("", s[last:]).lower())
    s = _strip_parens("".join(pieces).strip())
    if s in ("", "null"):
        return None
    if s.startswith("nextval("):
        return ("expr", "nextval()")
    if s == "current_timestamp":
        s = "now()"
    if QUOTED_RE.fullmatch(s):
        s = s[1:-1].replace("''", "'")
        kind = "str"
    else:
        kind = "expr"
    try:
        return ("num", decimal.Decimal(s))
    except decimal.InvalidOperation:
        return (kind, s)


def default_mismatches(documented: dict, live: dict):
    """Columns present in both whose normalised defaults differ.
    documented/live map column -> raw default expression (or None)."""
    return [
        {"column": c, "documented_default": documented[c], "live_default": live[c]}
        for c in sorted(set(documented) & set(live))
        if normalize_default(documented[c]) != normalize_default(live[c])
    ]


def parse_index_names(text: str):
    return sorted(set(INDEX_RE.findall(text)))


def parse_check_constraint_names(text: str):
    return sorted(set(CHECK_CONSTRAINT_RE.findall(text)))


def run_live_checks(tables, index_names, check_names, documented_defaults=None):
    import psycopg2  # local import: only needed when DATABASE_URL is set

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        cur = conn.cursor()
        report = {"tables": {}, "missing_indexes": [], "missing_check_constraints": []}

        for table_name, documented in tables.items():
            cur.execute(
                "SELECT column_name, is_nullable, column_default FROM information_schema.columns "
                "WHERE table_schema = 'public' AND table_name = %s",
                (table_name,),
            )
            rows = cur.fetchall()
            live = {row[0]: (row[1] == "YES") for row in rows}
            live_defaults = {row[0]: row[2] for row in rows}
            if not live:
                continue  # table not found live (not this script's concern here)

            undocumented = sorted(set(live) - set(documented))
            missing = sorted(set(documented) - set(live))
            nullable_mismatches = [
                {"column": c, "documented_nullable": documented[c], "live_nullable": live[c]}
                for c in sorted(set(documented) & set(live))
                if documented[c] != live[c]
            ]
            defaults = default_mismatches((documented_defaults or {}).get(table_name, {}), live_defaults)
            if undocumented or missing or nullable_mismatches or defaults:
                report["tables"][table_name] = {
                    "undocumented_live_columns": undocumented,
                    "missing_columns": missing,
                    "nullable_mismatches": nullable_mismatches,
                    "default_mismatches": defaults,
                }

        if index_names:
            cur.execute(
                "SELECT indexname FROM pg_indexes WHERE schemaname = 'public' AND indexname = ANY(%s)",
                (index_names,),
            )
            found = {row[0] for row in cur.fetchall()}
            report["missing_indexes"] = sorted(set(index_names) - found)

        if check_names:
            cur.execute(
                "SELECT conname FROM pg_constraint WHERE contype = 'c' AND conname = ANY(%s)",
                (check_names,),
            )
            found = {row[0] for row in cur.fetchall()}
            report["missing_check_constraints"] = sorted(set(check_names) - found)

        return report
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("data_model", type=Path, help="Path to docs/specs/data_model.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.data_model.exists():
        print(f"Not found: {args.data_model}", file=sys.stderr)
        return 1

    text = args.data_model.read_text()
    tables = parse_table_sections(text)
    index_names = parse_index_names(text)
    check_names = parse_check_constraint_names(text)
    documented_defaults = parse_documented_defaults(text)

    if "DATABASE_URL" not in os.environ:
        print("DATABASE_URL not set -- nothing to compare against (read-only check skipped).", file=sys.stderr)
        return 1

    report = run_live_checks(tables, index_names, check_names, documented_defaults)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    any_findings = False
    for table_name, findings in report["tables"].items():
        any_findings = True
        print(f"=== {table_name} ===")
        if findings["undocumented_live_columns"]:
            print(f"  Undocumented live columns: {', '.join(findings['undocumented_live_columns'])}")
        if findings["missing_columns"]:
            print(f"  Documented but missing live: {', '.join(findings['missing_columns'])}")
        for mm in findings["nullable_mismatches"]:
            print(f"  Nullable mismatch: {mm['column']} (documented={mm['documented_nullable']}, live={mm['live_nullable']})")
        for dm in findings["default_mismatches"]:
            print(f"  Default mismatch: {dm['column']} (documented={dm['documented_default']!r}, live={dm['live_default']!r})")
    if report["missing_indexes"]:
        any_findings = True
        print(f"Documented but missing live indexes: {', '.join(report['missing_indexes'])}")
    if report["missing_check_constraints"]:
        any_findings = True
        print(f"Documented but missing live CHECK constraints: {', '.join(report['missing_check_constraints'])}")
    if not any_findings:
        print("No divergence found: live schema matches data_model.md for all parsed tables, column defaults, indexes, and CHECK constraints.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
