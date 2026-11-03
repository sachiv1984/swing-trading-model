#!/usr/bin/env python3
# SessionStart hook — injects .claude_current_state.json into context automatically,
# so CLAUDE.md §0 ("Before doing anything else: read .claude_current_state.json,
# report active_cycle/status/engine, halt if Blocked") is structural rather than
# dependent on the model remembering to do it on every session start / resume /
# compact / clear. Fires on startup, resume, compact, and clear (see settings.json
# matcher) — the same events §0 names or implies ("session start", "context has
# been compacted"). Injects the §0 header fields and unresolved escalations only:
# the full file outgrew the hook output cap (AUD-2026-11-03-001).
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
        state = json.load(f)
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
    "Header fields:\n"
    + json.dumps({k: state.get(k) for k in (
        "active_cycle", "cycle_name", "status", "prior_status", "engine",
        "last_updated_utc", "next_release", "sprint_sealed",
        "design_gate_status", "verification_status", "closure_status",
        "post_ship_complete", "completed_cycle_count", "last_audit_id",
        "last_audit_cycle_count", "active_amendment", "amendment_status",
        "blocked_sla_breached", "execution_state_path", "backlog_slice_path",
    ) if k in state}, indent=2, ensure_ascii=False)
    + "\n\nUnresolved escalations (disposition != Resolved, open + deferred):\n"
    + json.dumps({k: v for m in ("open_escalations", "deferred_escalations")
                  for k, v in (state.get(m) or {}).items()
                  if isinstance(v, dict) and v.get("disposition") != "Resolved"},
                 indent=2, ensure_ascii=False)
    + "\n\nResolved escalation records are omitted (AUD-2026-11-03-001). Read any "
    "other field from .claude_current_state.json field-level, per "
    "shared_standards.md §14."
)
emit(context)
