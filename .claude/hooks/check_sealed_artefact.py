#!/usr/bin/env python3
# PreToolUse hook — warns (never blocks) when Claude is about to Edit/Write a
# file that the active cycle's own state marks immutable per CLAUDE.md §2
# ("Never modify sealed artefacts. Files marked sealed: true in state.json,
# or in Published state, are immutable"). protect-governance-files.sh already
# covers claude/system|charter|strategy; this covers the cycle-scoped
# artefacts named by path in .claude_current_state.json, gated on the seal
# flags that actually apply to them (sprint_sealed, closure_status, release
# publish status). commit-check Check 6 catches this too, but only if
# invoked before commit — this catches it at edit time instead.
import sys
import json
import os

PROJECT_ROOT = "/root/swing-trading-model"
STATE_FILE = os.path.join(PROJECT_ROOT, ".claude_current_state.json")
OVERRIDE_FILE = "/tmp/claude_governance_override"


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

file_path = data.get("tool_input", {}).get("file_path", "") or ""
if not file_path:
    approve()

abs_path = file_path if os.path.isabs(file_path) else os.path.join(PROJECT_ROOT, file_path)
try:
    abs_path = os.path.realpath(abs_path)
except Exception:
    approve()

if os.path.exists(OVERRIDE_FILE):
    approve()

try:
    with open(STATE_FILE) as f:
        state = json.load(f)
except Exception:
    approve()

sealed_paths = {}  # relative_path -> reason label

if state.get("sprint_sealed") is True:
    for key in ("sprint_goal_path", "sprint_backlog_path", "sprint_capacity_path", "backlog_slice_path"):
        p = state.get(key)
        if p:
            sealed_paths[p] = f"sprint_sealed=true ({key})"

release_plan = state.get("release_plan", {})
if release_plan:
    for key in ("release_plan_path", "scope_doc", "state_json"):
        p = release_plan.get(key)
        if p:
            sealed_paths[p] = f"release_plan.{key} — release published/sealed"

closure_status = state.get("closure_status", "") or ""
if closure_status.startswith("Closed"):
    for key in ("closure_record", "verification_report"):
        p = state.get(key)
        if p:
            sealed_paths[p] = f"closure_status={closure_status} ({key})"

if not sealed_paths:
    approve()

for rel_path, reason_label in sealed_paths.items():
    candidate = os.path.realpath(os.path.join(PROJECT_ROOT, rel_path))
    if candidate == abs_path:
        msg = (
            f"⚠️  SEALED ARTEFACT — {rel_path}\n\n"
            f"Reason: {reason_label} (per .claude_current_state.json)\n\n"
            "CLAUDE.md §2: files marked sealed, or in Published state, are immutable.\n"
            "If this edit is part of an authorised amendment (`amend cycle`) or a new\n"
            "cycle has since superseded this pointer, confirm before proceeding.\n\n"
            "To suppress this warning for this session:\n"
            f"  touch {OVERRIDE_FILE}"
        )
        approve(msg)

approve()
