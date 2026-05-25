#!/bin/bash
# PreToolUse hook — warns when Claude is about to edit a Class 6 governance file.
# Governance prompts and charter files must only be modified under an active
# governed routine (roadmap, sprint, post-ship, etc.) with the §6 checklist applied.
# Casual edits outside governed routines bypass the version-bump and OPERATIONAL_GUIDE
# update requirements, creating silent drift.
JQ=/usr/bin/jq

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | $JQ -r '.tool_input.file_path // ""')

# Check whether the file is in a governed directory
is_governance_file=false

if [[ "$FILE_PATH" =~ claude/system/.*\.md$ ]] && \
   [[ ! "$FILE_PATH" =~ claude/system/changelogs/ ]] && \
   [[ ! "$FILE_PATH" =~ claude/system/shared/ ]] && \
   [[ ! "$FILE_PATH" =~ claude/system/prompt_change_log\.md$ ]]; then
  is_governance_file=true
fi

if [[ "$FILE_PATH" =~ claude/charter/.*\.md$ ]]; then
  is_governance_file=true
fi

if [[ "$FILE_PATH" =~ claude/strategy/.*\.md$ ]]; then
  is_governance_file=true
fi

if [[ "$is_governance_file" == "false" ]]; then
  echo '{"decision": "approve"}'
  exit 0
fi

# Allow if a governed session override is active
if [[ -f "/tmp/claude_governance_override" ]]; then
  echo '{"decision": "approve"}'
  exit 0
fi

FILENAME=$(basename "$FILE_PATH")

$JQ -n --arg file "$FILENAME" --arg path "$FILE_PATH" '{
  decision: "approve",
  reason: ("⚠️  GOVERNANCE FILE EDIT — \($file)\n\nPath: \($path)\n\nThis is a Class 6 governance file. Before editing, confirm:\n  1. You are operating under an active governed routine (or explicit user instruction)\n  2. You will bump the **Version:** header in this file\n  3. You will update OPERATIONAL_GUIDE.md §14 governance table\n  4. You will update the phase section source prompt header in OPERATIONAL_GUIDE.md\n  5. You will append an entry to claude/system/prompt_change_log.md\n\nAll five steps must land in the same commit (CLAUDE.md §6).\n\nIf you are operating under a governed routine, continue.\nIf this is a casual edit, stop and confirm with the user first.\n\nTo suppress this warning for this session:\n  touch /tmp/claude_governance_override")
}'
