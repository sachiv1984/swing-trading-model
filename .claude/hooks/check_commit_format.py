#!/usr/bin/env python3
# PreToolUse hook logic — warns (never blocks) when a `git commit` message
# doesn't match the CLAUDE.md Section 2 canonical format for the current
# branch. Message parsing from a raw shell command string is heuristic
# (quoting styles vary), so on any parse ambiguity this stays silent
# rather than risk a false warning.
import sys
import json
import re
import subprocess

PROJECT_ROOT = "/root/swing-trading-model"


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

if "git commit" not in command:
    approve()

try:
    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=5
    ).stdout.strip()
except Exception:
    approve()

if not branch:
    approve()

msg = None
m = re.search(r'-m\s+"((?:[^"\\]|\\.)*)"', command, re.DOTALL)
if m:
    msg = m.group(1)
if msg is None:
    m = re.search(r"-m\s+'((?:[^'\\]|\\.)*)'", command, re.DOTALL)
    if m:
        msg = m.group(1)
if msg is None:
    m = re.search(r"<<-?\s*['\"]?EOF['\"]?\s*\n(.*?)\nEOF", command, re.DOTALL)
    if m:
        msg = m.group(1)

if msg is None or not msg.strip():
    approve()

subject = msg.strip().splitlines()[0]

is_exec = branch.startswith("exec/")
is_main = branch == "main"

exec_pattern = re.compile(r'^(\[EPIC-\d+\])(\[ST-\d+\])+ [A-Z]')
gov_pattern = re.compile(r'^\[GOVERNANCE\] [A-Z]')

ok = True
expected = ""
if is_exec:
    expected = "[EPIC-xx][ST-xx] <Description>"
    ok = bool(exec_pattern.match(subject))
elif is_main:
    expected = "[GOVERNANCE] <Description>"
    ok = bool(gov_pattern.match(subject))

if ok or not expected:
    approve()

reason = (
    f"WARNING: commit message may not match CLAUDE.md §2 format for branch '{branch}'.\n\n"
    f"Subject line detected: {subject}\n"
    f"Expected pattern: {expected}\n\n"
    "A missing [ST-xx] tag prevents governance_sync.yml from auto-closing that story's GitHub issue.\n"
    "If this is intentional (e.g. a merge/WIP commit), ignore this warning."
)
approve(reason)
