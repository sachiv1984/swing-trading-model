#!/usr/bin/env python3
"""
Write-time check: every `**Owner:**` value in a sprint_backlog.md is built from
canonical role names (ST-33, BLG-GOV-375, EPIC-06, v9.11).

shared_standards.md §16.11 requires each `**Owner:**` value (EPIC or ST item)
to be one or more names copied exactly from a `**Role:**` line in
claude/agents/*.md, joined by "; ". roadmap_prompt.md §7.2 tallies the field
verbatim through scripts/compute_role_share_history.py, so a variant spelling
or an inline qualifier ("(disposition)") becomes its own bucket and splits one
role's count. Sprint Planning runs this at STEP 6, before the seal.

Usage: python3 scripts/check_sprint_backlog_owners.py <sprint_backlog.md> [...]
Exit 0 = all Owner values canonical; 1 = violations (one per line); 2 = usage.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "claude" / "agents"
OWNER_RE = re.compile(r"^\*\*Owner:\*\*\s*(.*?)\s*$")
ROLE_RE = re.compile(r"^\*\*Role:\*\*\s*(.*?)\s*$")


def canonical_roles(agents_dir: Path = AGENTS_DIR) -> set:
    roles = set()
    for path in sorted(agents_dir.glob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            m = ROLE_RE.match(line)
            if m and m.group(1):
                roles.add(m.group(1).strip())
                break
    return roles


def check_text(text: str, roles: set, label: str = "sprint_backlog.md") -> list:
    violations = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = OWNER_RE.match(line)
        if not m:
            continue
        value = m.group(1)
        if not value:
            violations.append(f"{label}:{lineno}: empty Owner value")
            continue
        for name in value.split("; "):
            if name.strip() != name or name not in roles:
                violations.append(f"{label}:{lineno}: {name!r} is not a canonical role name (claude/agents/*.md **Role:** line)")
    return violations


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__.strip().splitlines()[-2])
        return 2
    roles = canonical_roles()
    violations = []
    for arg in argv:
        path = Path(arg)
        violations += check_text(path.read_text(encoding="utf-8"), roles, str(path))
    if violations:
        for v in violations:
            print(v)
        print(f"\n{len(violations)} non-canonical Owner value(s).")
        return 1
    print(f"Owner check: PASSED — every Owner value uses canonical role names ({len(roles)} roles).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
