#!/usr/bin/env python3
# PostToolUse hook — after any Edit/Write to .claude_current_state.json, warns
# (feedback only, PostToolUse can't block) about top-level fields that have no
# entry in claude/schemas/state_field_owners.json.
#
# Exists because ownerless fields in this file have gone stale silently
# before: `prior_cycle` (self-caught, filed as a follow-up alongside
# BLG-GOV-292, still deliberately left unowned in the manifest) and
# `last_audit_*` (drifted 3 audits stale before AUD-2026-08-08-004 caught it
# — no version of claude/audit.py had ever been told to write those fields).
# A field with no documented owner is a field no engine is accountable for
# keeping current; this surfaces that gap the moment it's introduced instead
# of relying on the next audit to notice.
import sys
import json
import os

PROJECT_ROOT = "/root/swing-trading-model"
STATE_FILE = os.path.join(PROJECT_ROOT, ".claude_current_state.json")
OWNERS_FILE = os.path.join(PROJECT_ROOT, "claude/schemas/state_field_owners.json")


def emit(context=None):
    out = {}
    if context:
        out["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    print(json.dumps(out))
    sys.exit(0)


try:
    data = json.load(sys.stdin)
except Exception:
    emit()

file_path = data.get("tool_input", {}).get("file_path", "") or ""
if not file_path.endswith(".claude_current_state.json"):
    emit()

try:
    with open(STATE_FILE) as f:
        state = json.load(f)
    with open(OWNERS_FILE) as f:
        owners = json.load(f)
except Exception:
    emit()

state_keys = set(state.keys())
owned_keys = set(owners.get("fields", {}).keys())
known_unowned = set(owners.get("_meta", {}).get("known_gaps", []))
# known_gaps entries are free-text ("prior_cycle — see its own entry..."); only
# match on the leading field-name token before any separator.
known_unowned_keys = {g.split(" ")[0] for g in known_unowned}

unowned = sorted(k for k in (state_keys - owned_keys) if k not in known_unowned_keys)
stale_manifest = sorted(owned_keys - state_keys)

if not unowned and not stale_manifest:
    emit()

parts = []
if unowned:
    parts.append(
        "New field(s) in .claude_current_state.json with no entry in "
        "claude/schemas/state_field_owners.json: " + ", ".join(unowned) +
        ". Add an owner entry (the engine/prompt file responsible for writing "
        "it) in the same commit — see that file's _meta.maintenance note."
    )
if stale_manifest:
    parts.append(
        "claude/schemas/state_field_owners.json documents field(s) no longer "
        "present in .claude_current_state.json: " + ", ".join(stale_manifest) +
        ". Prune the stale entries, or confirm the field was intentionally "
        "removed rather than accidentally dropped."
    )

emit("\n\n".join(parts))
