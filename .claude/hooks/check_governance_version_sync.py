#!/usr/bin/env python3
# PreToolUse hook — warns (never blocks) when a `git commit` stages a governance
# prompt file (claude/system/*.md) whose **Version:** header changed, without
# also staging the companion files CLAUDE.md §6 requires in the same commit:
#   - claude/system/OPERATIONAL_GUIDE.md   (§14 governance table + phase section header)
#   - claude/system/prompt_change_log.md   (one appended row per file changed)
#
# This is the same "N files must move together in one commit" shape as
# check_commit_gates.py's backend-route four-way sync and OpenAPI drift checks
# — those already have an automated gate; the §6 governance-file checklist did
# not, despite CLAUDE.md §8 2a documenting a real incident from this exact gap
# (sprint_planning_prompt.md v3.13/v3.14 both independently cut — see
# prompt_change_log.md's 2026-08-03__release-v8.1 entries).
#
# Warn-only, mirroring check_commit_gates.py's posture: this is a heuristic
# diff-text check (it only confirms the companion *files* are staged, not that
# their content actually reflects this specific version bump — CLAUDE.md §6's
# own version-match nuance stays a judgment call for the /governance-drift
# skill), so on any ambiguity this stays silent rather than risk a false block.
import sys
import json
import re
import subprocess

PROJECT_ROOT = "/root/swing-trading-model"

# Files that receive the §6 checklist's updates — never trigger on themselves.
COMPANION_FILES = [
    "claude/system/OPERATIONAL_GUIDE.md",
    "claude/system/prompt_change_log.md",
]

VERSION_ADD_RE = re.compile(r'^\+\*\*Version:\*\*\s*(\S+)')
VERSION_DEL_RE = re.compile(r'^-\*\*Version:\*\*\s*(\S+)')


def approve(reason=None):
    out = {"decision": "approve"}
    if reason:
        out["reason"] = reason
    print(json.dumps(out))
    sys.exit(0)


def run(args):
    try:
        return subprocess.run(
            args, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        ).stdout
    except Exception:
        return ""


try:
    data = json.load(sys.stdin)
except Exception:
    approve()

command = data.get("tool_input", {}).get("command", "") or ""

if "git commit" not in command:
    approve()

staged_files = [f for f in run(["git", "diff", "--cached", "--name-only"]).splitlines() if f]
if not staged_files:
    approve()

prompt_files = [
    f for f in staged_files
    if f.startswith("claude/system/") and f.endswith(".md") and f not in COMPANION_FILES
]

bumped = []
for f in prompt_files:
    diff = run(["git", "diff", "--cached", "--", f])
    added_version = None
    removed_version = None
    for line in diff.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        m = VERSION_ADD_RE.match(line)
        if m:
            added_version = m.group(1)
        m = VERSION_DEL_RE.match(line)
        if m:
            removed_version = m.group(1)
    if added_version and added_version != removed_version:
        bumped.append((f, removed_version, added_version))

if not bumped:
    approve()

missing = [c for c in COMPANION_FILES if c not in staged_files]

if not missing:
    approve()

lines = "\n".join(
    f"  {f}: {old or '(new)'} -> {new}" for f, old, new in bumped
)
approve(
    "Governance version-drift check (CLAUDE.md §6) — version-bumped governance "
    "prompt file(s) staged without all required companion files:\n" + lines +
    "\n\nMissing from staged set: " + ", ".join(missing) +
    "\n\nCLAUDE.md §6 requires, in the SAME commit: (1) bump the file's own "
    "Version header [done here], (2) update OPERATIONAL_GUIDE.md §14 "
    "governance table, (3) update the corresponding §5-§10/§6B/§6B.8/§6M phase "
    "section source-prompt header in OPERATIONAL_GUIDE.md, (4) append a row to "
    "prompt_change_log.md. Run the /governance-drift skill to check the "
    "content is actually in sync, not just staged — this hook only checks "
    "file presence."
)
