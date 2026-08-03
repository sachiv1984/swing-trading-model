#!/usr/bin/env python3
# PreToolUse hook — warns (never blocks) before a `gh pr merge` command runs.
# CLAUDE.md §2: "Never merge a PR autonomously. QA sign-off and Product Owner
# acceptance are always required." Nothing previously intercepted this command
# the way protect-eslint-config.sh intercepts config edits. Kept warn-only
# (not blocking) because §8 Cross-EPIC Merge Conflict Resolution legitimately
# runs `gh pr merge` as its own documented step 6, after sign-off is already
# recorded elsewhere — this just forces that confirmation to surface every time.
import sys
import json
import re

def approve(reason=None):
    out = {"decision": "approve"}
    if reason:
        out["reason"] = reason
    print(json.dumps(out))
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except Exception:
    approve()

command = data.get("tool_input", {}).get("command", "") or ""

if not re.search(r'\bgh\s+pr\s+merge\b', command):
    approve()

m = re.search(r'\bgh\s+pr\s+merge\s+(\d+)', command)
pr_ref = f"PR #{m.group(1)}" if m else "this PR"

reason = (
    f"⚠️  PR MERGE — about to merge {pr_ref}.\n\n"
    "CLAUDE.md §2: \"Never merge a PR autonomously. QA sign-off and Product "
    "Owner acceptance are always required.\"\n\n"
    "Before proceeding, confirm:\n"
    "  1. QA sign-off is recorded (DoQ block with a non-blank Date) for every "
    "story in this PR\n"
    "  2. Product Owner acceptance has been given for this PR specifically\n"
    "  3. If this merge is part of §8 Cross-EPIC Merge Conflict Resolution, "
    "sign-off was already confirmed earlier in that flow\n\n"
    "If either sign-off is missing or unconfirmed, stop and get it before merging."
)
approve(reason)
