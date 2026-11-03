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

Usage: python3 scripts/check_prompt_size_budget.py [--write-baseline]
Exit 0 = budget holds (or baseline written); 1 = violations (one per line).
"""
import glob
import json
import os
import sys

CAP = 68_500
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, "scripts", "prompt_size_baseline.json")
PATTERNS = [
    "claude/system/*_prompt.md",
    "claude/system/post_ship_closure.md",
    "claude/system/shared_standards.md",
]


def prompt_sizes():
    for pat in PATTERNS:
        for path in sorted(glob.glob(os.path.join(ROOT, pat))):
            yield os.path.relpath(path, ROOT), os.path.getsize(path)


def main():
    if "--write-baseline" in sys.argv:
        out = {rel: size for rel, size in prompt_sizes() if size > CAP}
        with open(BASELINE, "w") as f:
            json.dump(out, f, indent=2, sort_keys=True)
            f.write("\n")
        print(f"Wrote {len(out)} baseline(s) to {os.path.relpath(BASELINE, ROOT)}")
        return 0

    baseline = {}
    if os.path.exists(BASELINE):
        with open(BASELINE) as f:
            baseline = json.load(f)

    failures = []
    for rel, size in prompt_sizes():
        limit = baseline.get(rel, CAP)
        if size > limit:
            kind = "baseline" if rel in baseline else "cap"
            failures.append(f"{rel}: {size} bytes > limit {limit} ({kind})")

    if failures:
        print("Engine prompt size budget exceeded (shared_standards.md §11):")
        print("\n".join("  " + f for f in failures))
        print("Move rationale to an appendix, or raise the baseline in "
              "scripts/prompt_size_baseline.json in this PR with a reason in its "
              "prompt_change_log.md row.")
        return 1
    print("OK: engine prompt size budget holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
