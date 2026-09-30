#!/usr/bin/env python3
"""
Validate .claude_current_state.json against claude/system/state_schema.json
(ST-34, EPIC-06, v9.8, BLG-GOV-342).

Usage: python3 scripts/validate_state_schema.py
Exit code: 0 if valid, 1 if invalid or either file is missing/malformed.

Also checks the state-age advisory this story exists to fix: if
last_updated_utc is present, reports its age in days (the same check
roadmap_prompt.md STEP -1.6 performs) so a human/engine can confirm the
advisory will compute a real age rather than always firing.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = REPO_ROOT / ".claude_current_state.json"
SCHEMA_FILE = REPO_ROOT / "claude" / "system" / "state_schema.json"


def main() -> int:
    try:
        import jsonschema
    except ImportError:
        print("jsonschema package not installed -- run: pip install jsonschema", file=sys.stderr)
        return 1

    if not STATE_FILE.exists():
        print(f"State file not found: {STATE_FILE}", file=sys.stderr)
        return 1
    if not SCHEMA_FILE.exists():
        print(f"Schema file not found: {SCHEMA_FILE}", file=sys.stderr)
        return 1

    state = json.loads(STATE_FILE.read_text())
    schema = json.loads(SCHEMA_FILE.read_text())

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(state), key=lambda e: e.path)

    if errors:
        print(f"INVALID -- {len(errors)} schema violation(s):")
        for err in errors:
            path = "/".join(str(p) for p in err.path) or "(root)"
            print(f"  - {path}: {err.message}")
        return 1

    print("VALID -- .claude_current_state.json conforms to state_schema.json")

    last_updated = state.get("last_updated_utc")
    if not last_updated:
        print("ADVISORY: last_updated_utc is absent -- state-age advisory will fire.")
        return 0

    try:
        ts = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
        age_days = (datetime.now(timezone.utc) - ts).days
        print(f"last_updated_utc: {last_updated} ({age_days} day(s) old)")
        if age_days > 30:
            print("ADVISORY: state file not updated in >30 days -- confirm active_cycle is current.")
    except ValueError:
        print(f"ADVISORY: last_updated_utc is present but not a parseable ISO-8601 timestamp: {last_updated!r}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
