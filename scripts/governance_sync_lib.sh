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

# _find_story_context CYCLES_BASE ACTIVE_CYCLE ST_ID
#
# Internal helper. Locates the single .json file containing ST_ID's own
# `.stories` entry (per-EPIC file first, then the legacy single
# execution_state.json), and the JSON path expression to reach the stories
# object within it (".stories" for a per-EPIC file, or the specific
# ".epics.<EPIC-xx>.stories" object for the legacy shape — a legacy file can
# hold multiple EPICs, so the story's own containing epic must be pinned,
# not re-searched across all epics, or a same-named ST_ID in a different
# EPIC could be matched incorrectly).
#
# Prints two lines: the file path, then the jq path expression to the
# stories object (e.g. ".stories" or ".epics[\"EPIC-01\"].stories"). Prints
# nothing (empty output) if ST_ID is not found anywhere.
_find_story_context() {
  local cycles_base="$1" active_cycle="$2" st_id="$3"
  local state_dir="${cycles_base}/${active_cycle}/execution_state"
  if [ -d "$state_dir" ]; then
    for epic_file in "$state_dir"/EPIC-*.json; do
      [ -f "$epic_file" ] || continue
      if jq -e --arg st "$st_id" '.stories[$st] != null' "$epic_file" >/dev/null 2>&1; then
        printf '%s\n.stories\n' "$epic_file"
        return
      fi
    done
  fi
  local legacy_file="${cycles_base}/${active_cycle}/execution_state.json"
  if [ -f "$legacy_file" ]; then
    local epic_key
    epic_key=$(jq -r --arg st "$st_id" '(.epics // {}) | to_entries[] | select(.value.stories[$st] != null) | .key' "$legacy_file" 2>/dev/null | head -1)
    if [ -n "$epic_key" ]; then
      printf '%s\n.epics[%s].stories\n' "$legacy_file" "$(jq -c -n --arg k "$epic_key" '$k')"
      return
    fi
  fi
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
#
# ST-37 (BLG-GOV-349, EPIC-06, v9.8): group-aware for PHASED stories. A
# large story split into sub-phases (e.g. ST-01a/ST-01b/ST-01c, per
# execution_prompt.md's phasing convention — see 2026-09-23__release-v9.7's
# real PO-05/BLG-FEAT-74 precedent) is tracked as separate execution_state
# entries, ALL sharing the SAME `github_issue` number (one issue covers the
# whole phased story, titled with the bare parent ID). Before this fix,
# is_story_done checked only ST_ID's own status -- so ST-01a done alone
# reported "yes", incorrectly implying the whole phased story (and its
# shared issue) was complete while ST-01b/ST-01c were still in progress. Now:
# if ST_ID's own record has a `github_issue`, every OTHER story in the same
# stories object sharing that identical `github_issue` number must also be
# done/merged before this returns "yes" -- a non-phased story (whose issue
# number is unique to it alone) is unaffected, since it has no siblings
# sharing its issue.
is_story_done() {
  local cycles_base="$1" active_cycle="$2" st_id="$3"
  if [ -z "$active_cycle" ]; then
    echo "unknown"; return
  fi
  local context file stories_path status issue_number all_done
  context=$(_find_story_context "$cycles_base" "$active_cycle" "$st_id")
  if [ -z "$context" ]; then
    echo "unknown"; return
  fi
  file=$(echo "$context" | sed -n '1p')
  stories_path=$(echo "$context" | sed -n '2p')
  status=$(jq -r --arg st "$st_id" "${stories_path}[\$st].status // empty" "$file" 2>/dev/null)
  if [ -z "$status" ]; then
    echo "unknown"; return
  fi
  if [ "$status" != "done" ] && [ "$status" != "merged" ]; then
    echo "no"; return
  fi
  issue_number=$(jq -r --arg st "$st_id" "${stories_path}[\$st].github_issue // empty" "$file" 2>/dev/null)
  if [ -z "$issue_number" ] || [ "$issue_number" = "null" ]; then
    echo "yes"; return
  fi
  # Group-aware check: every sibling story sharing this exact github_issue
  # number must also be done/merged.
  all_done=$(jq -r --argjson issue "$issue_number" "
    [${stories_path} | to_entries[] | select(.value.github_issue == \$issue) | .value.status]
    | all(. == \"done\" or . == \"merged\")
  " "$file" 2>/dev/null)
  if [ "$all_done" = "true" ]; then
    echo "yes"
  else
    echo "no"
  fi
}

# get_github_issue_number CYCLES_BASE ACTIVE_CYCLE ST_ID
#
# Prints ST_ID's own recorded `github_issue` number (empty if not found, or
# not recorded). ST-37 (BLG-GOV-349): the close step uses this instead of a
# fuzzy `gh issue list --search "[ST_ID] in:title"` lookup, which fails for
# a phased story -- e.g. ST-01a's issue is titled "[ST-01] ..." (the bare
# parent ID), never "[ST-01a] ...", so a title-prefix search for "[ST-01a]"
# never finds it, regardless of whether is_story_done reports the phased
# group complete. Reading github_issue directly from execution_state (the
# same field STEP 1 of execution_prompt.md already records at issue-creation
# time) sidesteps title-matching entirely -- for phased AND non-phased
# stories alike.
get_github_issue_number() {
  local cycles_base="$1" active_cycle="$2" st_id="$3"
  local context file stories_path
  context=$(_find_story_context "$cycles_base" "$active_cycle" "$st_id")
  [ -z "$context" ] && return
  file=$(echo "$context" | sed -n '1p')
  stories_path=$(echo "$context" | sed -n '2p')
  jq -r --arg st "$st_id" "${stories_path}[\$st].github_issue // empty" "$file" 2>/dev/null
}
