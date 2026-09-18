#!/usr/bin/env python3
"""
Canonical Spec Cross-Reference Linter — ST-17 (BLG-SPEC-70, EPIC-04, v9.3)
Path-aware duplicate-basename resolution — ST-27 (BLG-SPEC-140, EPIC-04, v9.5)

Scans docs/specs/** for files not referenced by any backlog item or
codebase comment. "Referenced" means the file's basename (e.g.
"research_endpoint.md") appears as a literal substring anywhere in:
  - claude/backlog/backlog.md and claude/backlog/backlog_archive.md
    (a backlog item citing a spec — active or already-resolved)
  - any tracked source/doc file in the repo (*.py, *.js, *.jsx, *.md, *.yml,
    *.yaml) OTHER than the spec file itself — covers both "codebase comment"
    (a code comment naming the spec) and cross-references from sibling spec
    docs or Specs_Index.md

A file referencing only itself (self-mentions, e.g. its own filename in its
own header) does not count — that would trivially make every file "referenced."

**Duplicate-basename resolution (ST-27):** when two or more spec files share
the same basename (e.g. `docs/specs/frontend/README.md` and
`docs/specs/api_contracts/README.md`), a bare-basename match cannot tell
which one a given mention actually refers to — the original (ST-17) detector
cleared *both* files the moment the shared basename appeared anywhere, a
documented blind spot (see `docs/specs/orphaned_spec_scan_20260910.md` §
duplicate basenames, `BLG-SPEC-140`). For a duplicate-basename group, this
detector instead looks for a **path-qualified** reference (the basename
prefixed by one or more real parent-directory segments, e.g.
`frontend/README.md` or `specs/frontend/README.md`) to disambiguate:
  - A file with its own path-qualified reference somewhere is referenced.
  - A file in a group where a *sibling* has a path-qualified reference, but
    it itself has none, is flagged orphaned — a bare-basename mention
    elsewhere cannot be attributed to it once another member already has
    unambiguous proof.
  - A group where *no* member has a path-qualified reference, but the bare
    basename does appear somewhere, is reported as AMBIGUOUS rather than
    silently cleared or silently flagged — the ambiguity-flagging fallback.
  - A group with no reference at all (qualified or bare) is reported as
    orphaned as usual.

This is a read-only detection tool, matching check_specs_index_freshness.py's
own established convention: it reports candidates for Head of Specs Team
triage (keep / merge / archive), it does not decide or act on its own.

Usage: python3 scripts/check_orphaned_specs.py [--json]
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SPECS_DIR = REPO_ROOT / "docs" / "specs"
BACKLOG_FILES = [
    REPO_ROOT / "claude" / "backlog" / "backlog.md",
    REPO_ROOT / "claude" / "backlog" / "backlog_archive.md",
]

# Directories excluded from the repo-wide reference scan (vendored/build/generated).
_SCAN_EXCLUDE_DIRS = {
    ".venv", "venv", "node_modules", "__pycache__", "build", "dist",
    ".git", "playwright-report", "test-results",
}
_SCAN_EXTENSIONS = {".py", ".js", ".jsx", ".md", ".yml", ".yaml"}


def find_spec_files(specs_dir: Path) -> list[Path]:
    """All .md files under docs/specs/, recursively."""
    return sorted(specs_dir.rglob("*.md"))


def find_scannable_files(repo_root: Path) -> list[Path]:
    """All source/doc files repo-wide eligible to carry a reference,
    excluding vendored/build directories."""
    files = []
    for ext in _SCAN_EXTENSIONS:
        for path in repo_root.rglob(f"*{ext}"):
            if any(part in _SCAN_EXCLUDE_DIRS for part in path.parts):
                continue
            files.append(path)
    return files


def _path_qualifiers(spec_file: Path, repo_root: Path) -> list[str]:
    """Path-qualified substrings for a spec file, from least to most specific,
    excluding the bare basename itself (e.g. for docs/specs/frontend/README.md:
    ['frontend/README.md', 'specs/frontend/README.md', 'docs/specs/frontend/README.md'])."""
    rel_parts = spec_file.relative_to(repo_root).parts
    return ["/".join(rel_parts[i:]) for i in range(len(rel_parts) - 2, -1, -1)]


def _read_all(paths: list[Path]) -> dict:
    texts = {}
    for p in paths:
        try:
            texts[p] = p.read_text(errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue
    return texts


def find_orphaned_and_ambiguous_specs(
    specs_dir: Path, repo_root: Path, backlog_files: list[Path]
) -> tuple[list[str], list[dict]]:
    """Return (orphaned, ambiguous) — see module docstring for the
    duplicate-basename disambiguation rules `ambiguous` implements."""
    spec_files = find_spec_files(specs_dir)

    basename_groups: dict[str, list[Path]] = {}
    for f in spec_files:
        basename_groups.setdefault(f.name, []).append(f)

    backlog_text = ""
    for bf in backlog_files:
        if bf.exists():
            backlog_text += bf.read_text(errors="ignore")

    scannable = find_scannable_files(repo_root)
    file_texts = _read_all(scannable)

    orphaned = []
    ambiguous = []

    for basename, files in basename_groups.items():
        if len(files) == 1:
            spec_file = files[0]
            referenced = basename in backlog_text or any(
                basename in text for other, text in file_texts.items() if other != spec_file
            )
            if not referenced:
                orphaned.append(str(spec_file.relative_to(repo_root)))
            continue

        # Duplicate-basename group: resolve via path-qualified references.
        qualified_referenced = {}
        for spec_file in files:
            qualifiers = _path_qualifiers(spec_file, repo_root)
            found = any(q in backlog_text for q in qualifiers)
            if not found:
                for other, text in file_texts.items():
                    if other == spec_file:
                        continue
                    if any(q in text for q in qualifiers):
                        found = True
                        break
            qualified_referenced[spec_file] = found

        any_qualified = any(qualified_referenced.values())
        bare_mentioned = basename in backlog_text or any(
            basename in text for other, text in file_texts.items() if other not in files
        )

        for spec_file in files:
            rel = str(spec_file.relative_to(repo_root))
            if qualified_referenced[spec_file]:
                continue
            if any_qualified:
                # A sibling has unambiguous proof; this one has none — a bare
                # mention elsewhere cannot be attributed to it once another
                # member is already confirmed. Flag as orphaned per ST-27's AC.
                orphaned.append(rel)
            elif bare_mentioned:
                # No member has a path-qualified reference, but the bare
                # basename appears somewhere — can't tell which member(s) it
                # means. Ambiguity-flagging fallback, not silently cleared.
                ambiguous.append(
                    {
                        "path": rel,
                        "basename": basename,
                        "reason": "duplicate basename, no path-qualified reference found for any member of this group",
                        "siblings": sorted(
                            str(f.relative_to(repo_root)) for f in files if f != spec_file
                        ),
                    }
                )
            else:
                orphaned.append(rel)

    return sorted(orphaned), sorted(ambiguous, key=lambda a: a["path"])


def find_orphaned_specs(specs_dir: Path, repo_root: Path, backlog_files: list[Path]) -> list[str]:
    """Return basenames of docs/specs/**/*.md files referenced nowhere else
    (not in any backlog file, and not in any other scannable repo file).
    Thin wrapper over find_orphaned_and_ambiguous_specs for backward
    compatibility with existing callers/tests — see that function for the
    duplicate-basename (ambiguous) category this one omits."""
    orphaned, _ambiguous = find_orphaned_and_ambiguous_specs(specs_dir, repo_root, backlog_files)
    return orphaned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    orphaned, ambiguous = find_orphaned_and_ambiguous_specs(SPECS_DIR, REPO_ROOT, BACKLOG_FILES)

    if args.json:
        print(json.dumps(
            {"orphaned_specs": orphaned, "count": len(orphaned), "ambiguous_specs": ambiguous, "ambiguous_count": len(ambiguous)},
            indent=2,
        ))
    else:
        if not orphaned and not ambiguous:
            print("No orphaned specs found — every docs/specs/**/*.md file is referenced by at least one backlog item or another repo file.")
        if orphaned:
            print(f"ORPHANED SPECS ({len(orphaned)}) — not referenced by any backlog item or codebase comment:")
            for path in orphaned:
                print(f"  - {path}")
            print()
        if ambiguous:
            print(f"AMBIGUOUS SPECS ({len(ambiguous)}) — share a basename with another spec file, and only a bare (non-path-qualified) mention of that basename was found — cannot confirm which sibling it actually refers to:")
            for item in ambiguous:
                print(f"  - {item['path']} (shares basename with: {', '.join(item['siblings'])})")
            print()
        if orphaned or ambiguous:
            print("This is a detection tool — triage each with Head of Specs Team (keep / merge / archive) per ST-17's AC (RISK-04). Ambiguous entries need a path-qualified reference added (or removed) to resolve the ambiguity, not a guess.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
