#!/bin/bash
# Regression test for governance_sync.yml's "Update State and Close Issues"
# step — specifically is_story_done()'s three-way return value and how the
# close loop treats each (ST-09, EPIC-03, v9.2, BLG-QA-159).
#
# Prior behaviour (before BLG-GOV-314's ST-19 fix) treated "unknown" (no
# execution_state entry found for a story at all) as equivalent to "close the
# issue" — a false positive: a story not yet tracked is not the same as a
# story confirmed done. The fix changed "unknown" to skip, matching "no"
# (status present but not done/merged). This script exercises both halves of
# that behaviour directly against is_story_done() (not just the close loop's
# branching, which only reads is_story_done()'s output) so a future edit that
# reintroduces "unknown = close" is caught locally rather than only in CI.
#
# is_story_done() below is a parameterised copy of the function embedded in
# .github/workflows/governance_sync.yml's "Update State and Close Issues"
# step (CYCLES_BASE substituted for the hardcoded "claude/cycles" so this
# script can point it at a disposable fixture directory instead of a real
# cycle folder). If that step's logic changes, update this copy to match.
#
# Usage: scripts/test_governance_sync_close_gate_logic.sh
# Exit code 0 = all assertions passed; non-zero = a regression was detected.

set -uo pipefail

FAILED=0
FIXTURE_ROOT="$(mktemp -d)"
CYCLES_BASE="$FIXTURE_ROOT/claude/cycles"
FAKE_CYCLE="test-cycle-close-gate"

cleanup() {
  rm -rf "$FIXTURE_ROOT"
}
trap cleanup EXIT

is_story_done() {
  local active_cycle="$1" st_id="$2"
  if [ -z "$active_cycle" ]; then
    echo "unknown"; return
  fi
  local state_dir="$CYCLES_BASE/${active_cycle}/execution_state"
  local status=""
  if [ -d "$state_dir" ]; then
    for epic_file in "$state_dir"/EPIC-*.json; do
      [ -f "$epic_file" ] || continue
      status=$(jq -r --arg st "$st_id" '.stories[$st].status // empty' "$epic_file" 2>/dev/null)
      [ -n "$status" ] && break
    done
  fi
  if [ -z "$status" ]; then
    local legacy_file="$CYCLES_BASE/${active_cycle}/execution_state.json"
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

# Mirrors the close loop's own branching in governance_sync.yml: only "yes"
# results in an attempted `gh issue close`. Both "no" and "unknown" skip.
would_close() {
  [ "$(is_story_done "$1" "$2")" = "yes" ] && echo "close" || echo "skip"
}

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    echo "  PASS: $label — got '$actual'"
  else
    echo "  FAIL: $label — expected '$expected', got '$actual'"
    FAILED=1
  fi
}

mkdir -p "$CYCLES_BASE/$FAKE_CYCLE"
cat > "$CYCLES_BASE/$FAKE_CYCLE/execution_state.json" <<'EOF'
{
  "epics": {
    "EPIC-01": {
      "stories": {
        "ST-01": { "status": "done" },
        "ST-02": { "status": "blocked_decision" }
      }
    }
  }
}
EOF

echo "=== Case 1: no execution_state entry at all for the story (push time) ==="
echo "Expect is_story_done -> unknown, would_close -> skip (BLG-GOV-314's own fix)"
RESULT_1=$(is_story_done "$FAKE_CYCLE" "ST-99")
assert_eq "unknown status returned" "unknown" "$RESULT_1"
assert_eq "unknown does not close" "skip" "$(would_close "$FAKE_CYCLE" "ST-99")"
echo

echo "=== Case 2: story later resolves to a blocked_* status (still not done) ==="
echo "Expect is_story_done -> no, would_close -> skip — the exact BLG-QA-159"
echo "regression this story guards: an 'unknown'-then-'blocked' story must"
echo "never auto-close, at either point in its lifecycle."
RESULT_2=$(is_story_done "$FAKE_CYCLE" "ST-02")
assert_eq "blocked_* status returned as no" "no" "$RESULT_2"
assert_eq "blocked_* does not close" "skip" "$(would_close "$FAKE_CYCLE" "ST-02")"
echo

echo "=== Case 3: control — a genuinely done story still closes ==="
RESULT_3=$(is_story_done "$FAKE_CYCLE" "ST-01")
assert_eq "done status returned as yes" "yes" "$RESULT_3"
assert_eq "done closes" "close" "$(would_close "$FAKE_CYCLE" "ST-01")"
echo

echo "=== Case 4: no ACTIVE_CYCLE at all (defensive — governance_sync.yml's own first branch) ==="
RESULT_4=$(is_story_done "" "ST-01")
assert_eq "empty ACTIVE_CYCLE returns unknown" "unknown" "$RESULT_4"
assert_eq "empty ACTIVE_CYCLE does not close" "skip" "$(would_close "" "ST-01")"
echo

if [ "$FAILED" -eq 0 ]; then
  echo "All assertions passed."
  exit 0
else
  echo "One or more assertions FAILED — see above."
  exit 1
fi
