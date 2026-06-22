#!/bin/bash
# PostToolUse hook — runs ESLint on any JS/JSX file Claude just wrote or edited.
# Feeds lint errors back as Claude context. After 3 consecutive failures
# on the same file, escalates to the user instead of looping.
# Attempt state is stored per-file in /tmp to survive between tool calls.
PROJECT_ROOT="/root/swing-trading-model"

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

# Only lint JS/JSX source files — skip config, node_modules, build artefacts
if [[ ! "$FILE_PATH" =~ \.(js|jsx)$ ]]; then
  echo '{"decision": "approve"}'
  exit 0
fi

if [[ "$FILE_PATH" =~ node_modules|/build/|/dist/|/coverage/ ]]; then
  echo '{"decision": "approve"}'
  exit 0
fi

# Bail gracefully if ESLint binary is not installed
ESLINT_BIN="$PROJECT_ROOT/node_modules/.bin/eslint"
if [ ! -x "$ESLINT_BIN" ]; then
  echo '{"decision": "approve"}'
  exit 0
fi

# Per-file attempt counter (keyed by MD5 of path)
FILE_HASH=$(echo "$FILE_PATH" | md5sum | cut -d' ' -f1)
ATTEMPT_FILE="/tmp/eslint_attempts_${FILE_HASH}"
ATTEMPT=$(cat "$ATTEMPT_FILE" 2>/dev/null || echo 0)
ATTEMPT=$((ATTEMPT + 1))
echo "$ATTEMPT" > "$ATTEMPT_FILE"

cd "$PROJECT_ROOT" || { echo '{"decision": "approve"}'; exit 0; }
LINT_OUTPUT=$("$ESLINT_BIN" "$FILE_PATH" --format stylish 2>&1)
LINT_EXIT_CODE=$?

if [ $LINT_EXIT_CODE -ne 0 ]; then
  TMPFILE=$(mktemp)
  echo "$LINT_OUTPUT" > "$TMPFILE"
  if [ "$ATTEMPT" -ge 3 ]; then
    rm -f "$ATTEMPT_FILE"
    python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    out = f.read()
print(json.dumps({
  'decision': 'approve',
  'reason': 'CRITICAL: ' + out + '\n\nThis file has failed ESLint 3 times in a row. STOP attempting to fix it automatically.\nReport the violations to the user and ask how to proceed.\nDo NOT make further edits to this file without explicit user guidance.'
}))
" "$TMPFILE"
  else
    python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    out = f.read()
attempt = sys.argv[2]
print(json.dumps({
  'decision': 'approve',
  'reason': 'ESLint errors (attempt ' + attempt + '/3) — fix before continuing:\n' + out
}))
" "$TMPFILE" "$ATTEMPT"
  fi
  rm -f "$TMPFILE"
else
  rm -f "$ATTEMPT_FILE"
  echo '{"decision": "approve"}'
fi
