#!/bin/bash
# Regression test for governance_sync.yml's phased-story issue-close logic
# (ST-37, EPIC-06, v9.8, BLG-GOV-349).
#
# Real precedent this guards: 2026-09-23__release-v9.7's PO-05/BLG-FEAT-74
# story was phased into ST-01a/ST-01b/ST-01c, all three sharing GitHub
# issue #1792 (one issue covers the whole phased story, titled with the bare
# parent ID "[ST-01] ..."). Before this fix:
#   - is_story_done("ST-01a") checked only ST-01a's own status -- so it
#     reported "yes" (and the close step attempted to close) as soon as
#     ST-01a alone was done, even while ST-01b/ST-01c were still in
#     progress -- a false "fully done" positive.
#   - Even when genuinely complete, the close step searched for an issue
#     titled "[ST-01a] ..." (the phased ID) which never exists -- the real
#     issue is titled "[ST-01] ..." (the bare parent ID) -- so the issue
#     never actually closed regardless of what is_story_done reported.
#
# This script exercises both fixes directly against governance_sync_lib.sh's
# functions, plus a non-phased control case to confirm no regression of the
# ST-19/BLG-GOV-314 unknown-must-not-close fix this must coexist with.
#
# Usage: scripts/test_governance_sync_phased_story_logic.sh
# Exit code 0 = all assertions passed; non-zero = a regression was detected.

set -uo pipefail
cd "$(dirname "$0")/.."

source scripts/governance_sync_lib.sh

FAILED=0
FIXTURE_ROOT="$(mktemp -d)"
CYCLES_BASE="$FIXTURE_ROOT/claude/cycles"
FAKE_CYCLE="test-cycle-phased"

cleanup() {
  rm -rf "$FIXTURE_ROOT"
}
trap cleanup EXIT

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    echo "  PASS: $label — got '$actual'"
  else
    echo "  FAIL: $label — expected '$expected', got '$actual'"
    FAILED=1
  fi
}

# --- Per-EPIC shape fixture (current mechanism) ---
STATE_DIR="$CYCLES_BASE/$FAKE_CYCLE/execution_state"
mkdir -p "$STATE_DIR"
cat > "$STATE_DIR/EPIC-01.json" <<'EOF'
{
  "stories": {
    "ST-01a": { "status": "done", "github_issue": 1792 },
    "ST-01b": { "status": "blocked_backend", "github_issue": 1792 },
    "ST-01c": { "status": "not_started", "github_issue": 1792 },
    "ST-02": { "status": "done", "github_issue": 1793 }
  }
}
EOF

echo "=== Case 1: partially-done phased story — one phase done, siblings not ==="
echo "Expect is_story_done(ST-01a) -> no (NOT yes, despite ST-01a's own status"
echo "being done) — the exact regression this story exists to fix."
RESULT_1=$(is_story_done "$CYCLES_BASE" "$FAKE_CYCLE" "ST-01a")
assert_eq "partially-done phased story does not report done" "no" "$RESULT_1"
echo

echo "=== Case 2: non-phased control — done story with a unique issue still closes ==="
echo "Guards against a regression where the group-aware check breaks the"
echo "ordinary (non-phased, one-story-per-issue) case."
RESULT_2=$(is_story_done "$CYCLES_BASE" "$FAKE_CYCLE" "ST-02")
assert_eq "non-phased done story still reports yes" "yes" "$RESULT_2"
ISSUE_2=$(get_github_issue_number "$CYCLES_BASE" "$FAKE_CYCLE" "ST-02")
assert_eq "non-phased story's own issue number resolved" "1793" "$ISSUE_2"
echo

echo "=== Case 3: fully-done phased story — all 3 phases done ==="
cat > "$STATE_DIR/EPIC-01.json" <<'EOF'
{
  "stories": {
    "ST-01a": { "status": "done", "github_issue": 1792 },
    "ST-01b": { "status": "done", "github_issue": 1792 },
    "ST-01c": { "status": "merged", "github_issue": 1792 },
    "ST-02": { "status": "done", "github_issue": 1793 }
  }
}
EOF
echo "Expect is_story_done -> yes for EACH phase once all 3 are done/merged"
echo "(merged counts, matching the existing done/merged equivalence)."
for phase in ST-01a ST-01b ST-01c; do
  RESULT=$(is_story_done "$CYCLES_BASE" "$FAKE_CYCLE" "$phase")
  assert_eq "fully-done phased story ($phase) reports yes" "yes" "$RESULT"
done
echo

echo "=== Case 4: issue number resolves to the SHARED parent issue, not a phase-specific one ==="
echo "This is what lets the close step find the real issue (titled with the"
echo "bare parent ID) instead of a fuzzy title search for the phased ID,"
echo "which never matches."
for phase in ST-01a ST-01b ST-01c; do
  ISSUE=$(get_github_issue_number "$CYCLES_BASE" "$FAKE_CYCLE" "$phase")
  assert_eq "$phase resolves to the shared issue 1792" "1792" "$ISSUE"
done
echo

echo "=== Case 5: control — ST-19/BLG-GOV-314 unknown-does-not-close still holds ==="
echo "A phased-aware rewrite must not regress the pre-existing unknown-status"
echo "skip behaviour for a story with no execution_state entry at all."
RESULT_5=$(is_story_done "$CYCLES_BASE" "$FAKE_CYCLE" "ST-99")
assert_eq "no execution_state entry returns unknown" "unknown" "$RESULT_5"
ISSUE_5=$(get_github_issue_number "$CYCLES_BASE" "$FAKE_CYCLE" "ST-99")
assert_eq "no execution_state entry resolves no issue number" "" "$ISSUE_5"
echo

# --- Legacy single-execution_state.json shape ---
LEGACY_CYCLE="test-cycle-phased-legacy"
mkdir -p "$CYCLES_BASE/$LEGACY_CYCLE"
cat > "$CYCLES_BASE/$LEGACY_CYCLE/execution_state.json" <<'EOF'
{
  "epics": {
    "EPIC-02": {
      "stories": {
        "ST-05a": { "status": "done", "github_issue": 2001 },
        "ST-05b": { "status": "not_started", "github_issue": 2001 }
      }
    }
  }
}
EOF

echo "=== Case 6: legacy single-execution_state.json shape — phased grouping also applies ==="
RESULT_6=$(is_story_done "$CYCLES_BASE" "$LEGACY_CYCLE" "ST-05a")
assert_eq "legacy shape: partially-done phased story does not report done" "no" "$RESULT_6"
ISSUE_6=$(get_github_issue_number "$CYCLES_BASE" "$LEGACY_CYCLE" "ST-05a")
assert_eq "legacy shape: issue number still resolves" "2001" "$ISSUE_6"
echo

if [ "$FAILED" -eq 0 ]; then
  echo "All assertions passed."
  exit 0
else
  echo "One or more assertions FAILED — see above."
  exit 1
fi
