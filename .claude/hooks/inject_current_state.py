#!/usr/bin/env python3
# SessionStart hook — injects .claude_current_state.json into context automatically,
# so CLAUDE.md §0 ("Before doing anything else: read .claude_current_state.json,
# report active_cycle/status/engine, halt if Blocked") is structural rather than
# dependent on the model remembering to do it on every session start / resume /
# compact / clear. Fires on startup, resume, compact, and clear (see settings.json
# matcher) — the same events §0 names or implies ("session start", "context has
# been compacted").
import sys
import json
import os

PROJECT_ROOT = "/root/swing-trading-model"
STATE_FILE = os.path.join(PROJECT_ROOT, ".claude_current_state.json")


def emit(context=None):
    out = {}
    if context:
        out["hookSpecificOutput"] = {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    print(json.dumps(out))
    sys.exit(0)


try:
    with open(STATE_FILE) as f:
        raw = f.read()
    state = json.loads(raw)
except Exception:
    emit()

context = (
    "CLAUDE.md §0 auto-injected state (.claude_current_state.json) — "
    "read this before doing anything else this session:\n\n"
    f"active_cycle: {state.get('active_cycle', '(unset)')}\n"
    f"status: {state.get('status', '(unset)')}\n"
    f"engine: {state.get('engine', '(unset)')}\n\n"
    "If status is 'Blocked': do not proceed with any governed routine — "
    "surface open escalations and halt.\n\n"
    "Full file contents:\n" + raw
)
emit(context)
