#!/bin/bash
# PostToolUse hook — runs ESLint on any JS/JSX file Claude just wrote or edited.
JQ=/usr/bin/jq
# Feeds lint errors back as Claude context. After 3 consecutive failures
# on the same file, escalates to the user instead of looping.
#
# Attempt state is stored per-file in /tmp to survive between tool calls.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | $JQ -r '.tool_input.file_path // ""')

# Only lint JS/JSX source files — skip config, node_modules, build artefacts
if [[ ! "$FILE_PATH" =~ \.(js|jsx)$ ]]; then
  echo '{"decision": "approve"}'
  exit 0
fi

if [[ "$FILE_PATH" =~ node_modules|/build/|/dist/|/coverage/ ]]; then
  echo '{"decision": "approve"}'
  exit 0
fi

# Per-file attempt counter (keyed by MD5 of path)
FILE_HASH=$(echo "$FILE_PATH" | md5sum | cut -d' ' -f1)
ATTEMPT_FILE="/tmp/eslint_attempts_${FILE_HASH}"
ATTEMPT=$(cat "$ATTEMPT_FILE" 2>/dev/null || echo 0)
ATTEMPT=$((ATTEMPT + 1))
echo "$ATTEMPT" > "$ATTEMPT_FILE"

# Run ESLint using the project's installed v9 binary
cd /home/ubuntu/swing-trading-model || exit 0
LINT_OUTPUT=$(./node_modules/.bin/eslint "$FILE_PATH" --format stylish 2>&1)
LINT_EXIT_CODE=$?

if [ $LINT_EXIT_CODE -ne 0 ]; then
  if [ "$ATTEMPT" -ge 3 ]; then
    # Three strikes — stop looping and escalate
    rm -f "$ATTEMPT_FILE"
    $JQ -n --arg out "$LINT_OUTPUT" '{
      decision: "approve",
      reason: ("CRITICAL: \($out)\n\nThis file has failed ESLint 3 times in a row. STOP attempting to fix it automatically.\nReport the violations to the user and ask how to proceed.\nDo NOT make further edits to this file without explicit user guidance.")
    }'
  else
    # Return errors as feedback for Claude to fix
    $JQ -n --arg out "$LINT_OUTPUT" --argjson attempt "$ATTEMPT" '{
      decision: "approve",
      reason: ("ESLint errors (attempt \($attempt)/3) — fix before continuing:\n\($out)")
    }'
  fi
else
  # Lint passed — reset attempt counter
  rm -f "$ATTEMPT_FILE"
  echo '{"decision": "approve"}'
fi
