#!/usr/bin/env bash
# ST-21 (BLG-OPS-125, EPIC-04, v8.2): test suite for scripts/git-hooks/commit-msg.
#
# Run: bash scripts/git-hooks/test_commit_msg.sh
# Exits non-zero if any case fails.

set -uo pipefail

HOOK="$(cd "$(dirname "$0")" && pwd)/commit-msg"
FAILURES=0
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Isolated throwaway git repo so branch-switching here never touches the real repo state.
REPO="$TMPDIR/repo"
mkdir -p "$REPO"
git -C "$REPO" init -q
git -C "$REPO" config user.email "test@example.com"
git -C "$REPO" config user.name "Test"
git -C "$REPO" commit -q --allow-empty -m "[GOVERNANCE] initial commit"

check() {
  local description="$1"
  local branch="$2"
  local message="$3"
  local expected_exit="$4"

  git -C "$REPO" checkout -q -B "$branch" >/dev/null 2>&1
  echo "$message" > "$TMPDIR/msg.txt"
  (cd "$REPO" && bash "$HOOK" "$TMPDIR/msg.txt") >/dev/null 2>&1
  local actual_exit=$?

  if [ "$actual_exit" -eq "$expected_exit" ]; then
    echo "PASS: $description"
  else
    echo "FAIL: $description (expected exit $expected_exit, got $actual_exit)"
    FAILURES=$((FAILURES + 1))
  fi
}

check "exec/** branch, malformed message -> rejected"      "exec/test/EPIC-01"  "no tags at all here"                                   1
check "exec/** branch, valid single-story -> accepted"     "exec/test/EPIC-01"  "[EPIC-01][ST-01] Do the thing"                         0
check "exec/** branch, valid multi-story -> accepted"      "exec/test/EPIC-01"  "[EPIC-01][ST-01][ST-02] Do two things"                 0
check "exec/** branch, valid GOVERNANCE -> accepted"       "exec/test/EPIC-01"  "[GOVERNANCE] Do a governance thing"                    0
check "main branch, malformed message -> unrestricted"     "main"               "no tags at all here"                                   0
check "exec/** branch, empty description -> rejected"      "exec/test/EPIC-01"  "[EPIC-01][ST-01]"                                       1

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "All checks passed."
  exit 0
else
  echo "$FAILURES check(s) failed."
  exit 1
fi
