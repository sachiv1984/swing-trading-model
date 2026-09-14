#!/usr/bin/env python3
"""
Canonical Spec Cross-Reference Linter — ST-17 (BLG-SPEC-70, EPIC-04, v9.3)

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


def find_orphaned_specs(specs_dir: Path, repo_root: Path, backlog_files: list[Path]) -> list[str]:
    """Return basenames of docs/specs/**/*.md files referenced nowhere else
    (not in any backlog file, and not in any other scannable repo file)."""
    spec_files = find_spec_files(specs_dir)
    spec_basenames = [f.name for f in spec_files]

    # Pre-read backlog text once.
    backlog_text = ""
    for bf in backlog_files:
        if bf.exists():
            backlog_text += bf.read_text(errors="ignore")

    scannable = find_scannable_files(repo_root)

    orphaned = []
    for spec_file, basename in zip(spec_files, spec_basenames):
        if basename in backlog_text:
            continue
        referenced_elsewhere = False
        for other in scannable:
            if other == spec_file:
                continue
            try:
                text = other.read_text(errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue
            if basename in text:
                referenced_elsewhere = True
                break
        if not referenced_elsewhere:
            orphaned.append(str(spec_file.relative_to(repo_root)))
    return sorted(orphaned)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    orphaned = find_orphaned_specs(SPECS_DIR, REPO_ROOT, BACKLOG_FILES)

    if args.json:
        print(json.dumps({"orphaned_specs": orphaned, "count": len(orphaned)}, indent=2))
    else:
        if not orphaned:
            print("No orphaned specs found — every docs/specs/**/*.md file is referenced by at least one backlog item or another repo file.")
        else:
            print(f"ORPHANED SPECS ({len(orphaned)}) — not referenced by any backlog item or codebase comment:")
            for path in orphaned:
                print(f"  - {path}")
            print("\nThis is a detection tool — triage each with Head of Specs Team (keep / merge / archive) per ST-17's AC (RISK-04).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
