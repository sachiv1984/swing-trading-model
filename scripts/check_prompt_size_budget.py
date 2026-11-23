#!/usr/bin/env python3
"""
Engine prompt size ratchet (AUD-2026-11-03-003; shared_standards.md §11).

The §11 size budget asked each bump of an over-cap prompt to cite a split
item. 16 of 21 bumps between AUD-2026-10-08 and AUD-2026-11-03 did not, and
execution_prompt.md and release_planning_prompt.md kept growing. This script
makes the budget a CI check instead:

  - a prompt under the 68,500-byte single-read cap fails if it crosses it
  - a prompt already over the cap fails if it grows past its entry in
    scripts/prompt_size_baseline.json

To accept growth, raise the file's baseline in the same PR and say why in the
bump's prompt_change_log.md row. .github/workflows/prompt-size-budget.yml runs
this on every PR touching claude/system/.

--staged (ST-23, BLG-GOV-421, v9.18) measures the prompts and the baseline as
they are in the git index, for .githooks/pre-commit: a commit is judged on
what it will contain, not on unstaged edits. The workflow also runs on pushes
to main, so a commit that skipped the hook (--no-verify) shows a red run.

Usage: python3 scripts/check_prompt_size_budget.py [--staged | --write-baseline]
Exit 0 = budget holds (or baseline written); 1 = violations (one per line).
"""
import fnmatch
import glob
import json
import os
import subprocess
import sys

CAP = 68_500
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, "scripts", "prompt_size_baseline.json")
PATTERNS = [
    "claude/system/*_prompt.md",
    "claude/system/post_ship_closure.md",
    "claude/system/shared_standards.md",
]


def _git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], check=True, capture_output=True, text=True).stdout


def _matches(rel):
    """The same files glob() finds: top-level claude/system/ only."""
    return os.path.dirname(rel) == "claude/system" and any(
        fnmatch.fnmatchcase(os.path.basename(rel), os.path.basename(pat)) for pat in PATTERNS)


def prompt_sizes(staged=False):
    if staged:
        # -s -z: stage numbers and NUL-separated, unquoted paths. A path with a
        # non-zero stage is an unresolved merge conflict, not a size to check.
        unmerged = set()
        for entry in sorted(_git("ls-files", "-s", "-z", "--", "claude/system").split("\0")):
            if not entry:
                continue
            meta, rel = entry.split("\t", 1)
            if not _matches(rel):
                continue
            if meta.split()[2] != "0":
                unmerged.add(rel)
                continue
            yield rel, int(_git("cat-file", "-s", f":{rel}"))
        for rel in sorted(unmerged):
            print(f"Skipped {rel}: unresolved merge conflict in the index; resolve it and re-run.")
        return
    for pat in PATTERNS:
        for path in sorted(glob.glob(os.path.join(ROOT, pat))):
            yield os.path.relpath(path, ROOT), os.path.getsize(path)


def load_baseline(staged=False):
    if staged:
        try:
            return json.loads(_git("show", ":scripts/prompt_size_baseline.json"))
        except subprocess.CalledProcessError:
            return {}
    if os.path.exists(BASELINE):
        with open(BASELINE) as f:
            return json.load(f)
    return {}


def main():
    if "--write-baseline" in sys.argv:
        out = {rel: size for rel, size in prompt_sizes() if size > CAP}
        with open(BASELINE, "w") as f:
            json.dump(out, f, indent=2, sort_keys=True)
            f.write("\n")
        print(f"Wrote {len(out)} baseline(s) to {os.path.relpath(BASELINE, ROOT)}")
        return 0

    staged = "--staged" in sys.argv
    baseline = load_baseline(staged)

    failures = []
    for rel, size in prompt_sizes(staged):
        limit = baseline.get(rel, CAP)
        if size > limit:
            kind = "baseline" if rel in baseline else "cap"
            failures.append(f"{rel}: {size} bytes > limit {limit} ({kind})")

    if failures:
        where = " (staged)" if staged else ""
        print(f"Engine prompt size budget exceeded{where} (shared_standards.md §11):")
        print("\n".join("  " + f for f in failures))
        print("Move an equal amount of rationale or history to the file's changelog or "
              "appendix (headroom rule), or raise the baseline in "
              "scripts/prompt_size_baseline.json in the same commit with a Head of "
              "Specs Team reason in its prompt_change_log.md row.")
        return 1
    print("OK: engine prompt size budget holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
