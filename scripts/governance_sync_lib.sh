#!/bin/bash
# Shared bash logic for .github/workflows/governance_sync.yml's "Parse Commits
# for Governance" and "Update State and Close Issues" steps (ST-16, BLG-QA-165,
# EPIC-03, v9.5).
#
# Extracted so this logic lives in exactly one place, sourced by both the
# workflow itself and its two regression test scripts
# (scripts/test_governance_sync_diff_logic.sh,
# scripts/test_governance_sync_close_gate_logic.sh) — previously each of the
# 3 consumers held its own hand-maintained copy of these functions, with only
# a comment ("If this logic changes, update this copy to match") enforcing
# consistency. A future edit to one copy with no corresponding edit to the
# others would silently desync the tests from the real behaviour they claim
# to guard.
#
# Usage: `source scripts/governance_sync_lib.sh` from repo root (or any
# directory — this file does not depend on CWD; callers that need git
# commands to resolve correctly must themselves run from within the repo,
# same requirement as before extraction).

# detect_newly_done_st_ids BEFORE_REF AFTER_REF
#
# Diffs every changed execution_state file (per-EPIC and legacy shapes) in
# the given git ref range and prints (one per line, sorted, deduplicated)
# every ST-xx whose status newly became done/merged. ST-19 (BLG-GOV-314):
# exists because a commit-message-only scan misses a story whose completion
# is recorded in a separate follow-up commit tagged only [GOVERNANCE].
detect_newly_done_st_ids() {
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

# is_story_done CYCLES_BASE ACTIVE_CYCLE ST_ID
#
# Prints "yes" (status is done/merged), "no" (status present but not
# done/merged), or "unknown" (no ACTIVE_CYCLE, or no execution_state entry
# found for this ST_ID at all — tries the current per-EPIC mechanism first,
# falls back to the legacy single execution_state.json). CYCLES_BASE lets
# callers point this at either the real "claude/cycles" or a disposable test
# fixture directory. ST-19 (BLG-GOV-314): "unknown" must be treated as SKIP
# by callers, not CLOSE — a story with no tracking entry yet is not the same
# as a story confirmed done (BLG-QA-159's regression).
is_story_done() {
  local cycles_base="$1" active_cycle="$2" st_id="$3"
  if [ -z "$active_cycle" ]; then
    echo "unknown"; return
  fi
  local state_dir="${cycles_base}/${active_cycle}/execution_state"
  local status=""
  if [ -d "$state_dir" ]; then
    for epic_file in "$state_dir"/EPIC-*.json; do
      [ -f "$epic_file" ] || continue
      status=$(jq -r --arg st "$st_id" '.stories[$st].status // empty' "$epic_file" 2>/dev/null)
      [ -n "$status" ] && break
    done
  fi
  if [ -z "$status" ]; then
    local legacy_file="${cycles_base}/${active_cycle}/execution_state.json"
    if [ -f "$legacy_file" ]; then
      status=$(jq -r --arg st "$st_id" '(.epics // {}) | to_entries[] | .value.stories[$st].status? // empty' "$legacy_file" 2>/dev/null | head -1)
    fi
  fi
  if [ -z "$status" ]; then
    echo "unknown"
  elif [ "$status" = "done" ] || [ "$status" = "merged" ]; then
    echo "yes"
  else
    echo "no"
  fi
}
