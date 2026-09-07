#!/usr/bin/env python3
"""
Specs_Index.md freshness check (ST-33, EPIC-05, v9.1, BLG-GOV-274).

Compares docs/specs/Specs_Index.md's tracked spec-file references against
the live docs/specs/ tree, reporting:
  - ADDITIONS: .md files that exist under docs/specs/ but are not mentioned
    anywhere in Specs_Index.md (Specs_Index.md may be stale/lapsed).
  - REMOVALS: filenames mentioned in Specs_Index.md that no longer exist
    anywhere under docs/specs/ (a stale reference to a deleted/moved file).

This is a detection tool, not an auto-fixer -- Specs_Index.md updates
require Head of Specs Team review (which files genuinely need indexing vs.
which are intentionally excluded, e.g. drafts/deprecated/archived specs).

Usage: python3 scripts/check_specs_index_freshness.py
Exit code: 0 if clean, 1 if any addition or removal is found (so this can
be wired into a CI/pre-sprint check later if desired -- BLG-GOV-274's own
AC is "check added", not "check enforced as a hard gate").
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = REPO_ROOT / "docs" / "specs"
INDEX_FILE = SPECS_DIR / "Specs_Index.md"

# Files intentionally excluded from the freshness check -- not canonical
# specs themselves, or already tracked by a different, more specific
# mechanism (e.g. the Specs_Index.md file's own self-reference).
EXCLUDE_BASENAMES = {
    "Specs_Index.md",
}
# Directories under docs/specs/ whose contents are excluded (dated/scoped
# working documents, not canonical specs the index tracks by design --
# confirmed by reading Specs_Index.md's own §3/§6/§7/§8 scope, which never
# references files under these subtrees).
EXCLUDE_DIR_PREFIXES = (
    "qa",  # docs/specs/qa/ -- QA scenario/protocol documents, not specs
)


def find_live_spec_files():
    files = set()
    for p in SPECS_DIR.rglob("*.md"):
        rel = p.relative_to(SPECS_DIR)
        if p.name in EXCLUDE_BASENAMES:
            continue
        if rel.parts and rel.parts[0] in EXCLUDE_DIR_PREFIXES:
            continue
        files.add(rel.as_posix())
    return files


def find_indexed_references(index_text):
    """Extract every docs/specs/-relative .md filename/path mentioned in
    Specs_Index.md, both as a full path (docs/specs/foo/bar.md) and as a
    bare filename inside backticks (`bar.md`) under a Canonical Documents
    list -- both conventions are used in the file (see §3.1 vs §3.4)."""
    referenced_basenames = set()
    referenced_paths = set()

    # Full docs/specs/... paths anywhere in the file.
    for m in re.finditer(r"docs/specs/([A-Za-z0-9_./-]+\.md)", index_text):
        referenced_paths.add(m.group(1))

    # Bare `filename.md` or `sub/dir/filename.md` references inside backticks.
    for m in re.finditer(r"`([A-Za-z0-9_./-]+\.md)`", index_text):
        val = m.group(1)
        if "/" in val:
            referenced_paths.add(val)
        else:
            referenced_basenames.add(val)

    return referenced_basenames, referenced_paths


def main():
    if not INDEX_FILE.exists():
        print(f"ERROR: {INDEX_FILE} not found.")
        return 2

    index_text = INDEX_FILE.read_text(encoding="utf-8")
    live_files = find_live_spec_files()
    referenced_basenames, referenced_paths = find_indexed_references(index_text)

    # A live file is "covered" if its full relative path OR its bare
    # basename is mentioned somewhere in the index.
    additions = []
    for rel in sorted(live_files):
        basename = Path(rel).name
        if rel in referenced_paths or basename in referenced_basenames:
            continue
        additions.append(rel)

    # A referenced path/basename is a removal candidate only if no live
    # docs/specs/ file matches it AND no file anywhere else in the repo
    # matches it either -- Specs_Index.md legitimately cross-references many
    # non-docs/specs/ canonical files (e.g. claude/strategy/strategy_rules.md,
    # claude/backlog/backlog.md, qa_evidence_EPIC-xx.md per cycle) by bare
    # filename; those are correctly-scoped cross-references, not stale
    # docs/specs/ removals, and must not be flagged as such.
    live_basenames = {Path(f).name for f in live_files}
    repo_basenames = {p.name for p in REPO_ROOT.rglob("*.md")
                       if ".git" not in p.parts and "node_modules" not in p.parts}
    removals = []
    for path in sorted(referenced_paths):
        if path in live_files:
            continue
        name = Path(path).name
        if name in live_basenames or name in repo_basenames:
            continue
        removals.append(path)
    for basename in sorted(referenced_basenames):
        if basename in live_basenames or basename in repo_basenames:
            continue
        removals.append(basename)

    if not additions and not removals:
        print("Specs_Index.md freshness check: PASSED — no additions or removals detected.")
        return 0

    if additions:
        print(f"ADDITIONS ({len(additions)}) — live docs/specs/ files not referenced in Specs_Index.md:")
        for a in additions:
            print(f"  - docs/specs/{a}")
    if removals:
        print(f"\nREMOVALS ({len(removals)}) — Specs_Index.md references with no matching live file:")
        for r in removals:
            print(f"  - {r}")

    print("\nThis is a detection tool -- review each item with Head of Specs Team before editing Specs_Index.md.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
