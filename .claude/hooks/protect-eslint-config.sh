#!/bin/bash
# PreToolUse hook — blocks automated modification of eslint.config.mjs.
# If ESLint is preventing a task, report the conflict to the user
# instead of editing the config to bypass it.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")
FILENAME=$(basename "$FILE_PATH")

if [[ "$FILENAME" == "eslint.config.mjs" ]]; then
  if [[ -f "/tmp/claude_config_override" ]]; then
    echo '{"decision": "approve"}'
    exit 0
  fi
  python3 -c "
import json
print(json.dumps({
  'decision': 'block',
  'reason': 'Modifying eslint.config.mjs is forbidden. ESLint rules are a quality gate — not an obstacle to route around.\n\nIf a rule is making your task impossible:\n  1. Stop.\n  2. Report the specific rule and why it blocks you to the user.\n  3. Wait for explicit authorisation before any config change.\n\nDo not attempt to bypass, disable, or inline-suppress a rule without user approval.\n\nIf you have been explicitly asked to edit this file, ask the user to run:\n  touch /tmp/claude_config_override'
}))
"
  exit 0
fi

echo '{"decision": "approve"}'
