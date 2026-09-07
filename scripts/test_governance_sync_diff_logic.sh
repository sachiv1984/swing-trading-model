#!/bin/bash
# Regression test for governance_sync.yml's diff-based ST-ID detection
# (ST-19, EPIC-04, v9.1, BLG-GOV-314).
#
# Confirms the fix for the under-closing failure mode: a story whose completion
# is set in a *separate* follow-up commit tagged only [GOVERNANCE] (no [ST-xx]
# in that commit's own message) is still detected as newly-done, because
# detection is based on diffing execution_state's actual story-status content
# between the push's before/after refs — not on scanning commit messages alone.
#
# This mirrors the exact logic embedded in .github/workflows/governance_sync.yml's
# "Parse Commits for Governance" step. If that step's logic changes, update this
# script to match (or better: extract both into one shared script sourced by both).
#
# Usage: scripts/test_governance_sync_diff_logic.sh
# Exit code 0 = all assertions passed; non-zero = a regression was detected.

set -uo pipefail
cd "$(dirname "$0")/.."

FAILED=0

detect_newly_done() {
  local before="$1" after="$2"
  local diff_st_ids=""
  local changed_state_files
  changed_state_files=$(git diff --name-only "$before" "$after" -- 'claude/cycles/*/execution_state/EPIC-*.json' 'claude/cycles/*/execution_state.json' 2>/dev/null || true)
  for f in $changed_state_files; do
    local after_json before_json after_map before_map newly_done
    after_json=$(git show "$after:$f" 2>/dev/null || echo '{}')
    before_json=$(git show "$before:$f" 2>/dev/null || echo '{}')
    after_map=$(echo "$after_json" | jq -c '
      if has("stories") then .stories
      elif has("epics") then ([.epics[].stories] | add // {})
      else {} end
      | with_entries(.value = .value.status)
    ' 2>/dev/null || echo '{}')
    before_map=$(echo "$before_json" | jq -c '
      if has("stories") then .stories
      elif has("epics") then ([.epics[].stories] | add // {})
      else {} end
      | with_entries(.value = .value.status)
    ' 2>/dev/null || echo '{}')
    newly_done=$(jq -n --argjson after "$after_map" --argjson before "$before_map" '
      $after
      | to_entries[]
      | select(.value == "done" or .value == "merged")
      | select(($before[.key] // "") != "done" and ($before[.key] // "") != "merged")
      | .key
    ' 2>/dev/null | tr -d '"')
    diff_st_ids="$diff_st_ids $newly_done"
  done
  echo "$diff_st_ids" | tr ' ' '\n' | sed '/^$/d' | sort -u
}

assert_contains() {
  local label="$1" haystack="$2" needle="$3"
  if echo "$haystack" | grep -qx "$needle"; then
    echo "  PASS: $label — found '$needle'"
  else
    echo "  FAIL: $label — expected '$needle', got: [$haystack]"
    FAILED=1
  fi
}

assert_empty() {
  local label="$1" actual="$2"
  if [ -z "$(echo "$actual" | tr -d '[:space:]')" ]; then
    echo "  PASS: $label — correctly empty"
  else
    echo "  FAIL: $label — expected empty, got: [$actual]"
    FAILED=1
  fi
}

echo "=== Regression case 1: split work-commit + governance-commit (the real v9.1 EPIC-03 case) ==="
echo "Range: cffda202 (work commit, [EPIC-03][ST-12][ST-13][ST-14], ST-12-14 NOT yet done)"
echo "    -> 8350caba ([GOVERNANCE] tracking commit, no [ST-xx] tag, sets ST-12-18 done)"
RESULT_1=$(detect_newly_done "cffda202" "8350caba")
assert_contains "under-closing fix" "$RESULT_1" "ST-12"
assert_contains "under-closing fix" "$RESULT_1" "ST-13"
assert_contains "under-closing fix" "$RESULT_1" "ST-14"
echo

echo "=== Regression case 2: work commit with no execution_state change in range ==="
echo "Range: b897b28 (ST-22 work commit) -> 04d47ab (ST-20 work commit) — neither touches execution_state.json"
RESULT_2=$(detect_newly_done "b897b28" "04d47ab")
assert_empty "no false positive when execution_state untouched" "$RESULT_2"
echo

if [ "$FAILED" -eq 0 ]; then
  echo "All assertions passed."
  exit 0
else
  echo "One or more assertions FAILED — see above."
  exit 1
fi
