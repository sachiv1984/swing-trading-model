---
name: record-visual-qa
description: Record human visual staging test results for a story. Use this skill after a tester reports visual QA results (pass/fail/blocked per check). Updates both the visual test script file (stamps each check with its result) and the QA evidence file (DoQ sign-off block). Auto-invokes /dev-file for any unfixed FAILs. Use when someone pastes visual test results like "V-CHART-01a - Pass, V-CHART-02c - Fail", or says "record these QA results", "update the visual test results", or "sign off visual QA".
---

# Record Visual QA Results

Takes freetext visual staging test results, stamps the visual test script
file with each result, updates the QA evidence DoQ sign-off block, and
invokes /dev-file for any unfixed FAILs.

## Step 0 — Load lessons

Read `.claude/skills/lessons_learnt.md`. Look for entries tagged
`[record-visual-qa]` and apply them. If the file doesn't exist, continue.

## Step 0.5 — Which path applies (added ST-34, BLG-GOV-319, v9.5 — reconciles ~5 months' drift from actual practice)

The full check-ID workflow below (Steps 1–7) assumes a dedicated
`docs/testing/staging_visual_test_script_<ST-xx|EPIC-xx>.md` file with
pre-defined `V-xxx` checks exists for the story. That has become the
**minority** case: a sample of recent `qa_evidence_EPIC-*.md` entries
(`2026-09-14__release-v9.4` EPIC-05/EPIC-06, `2026-08-21__release-v9.0`
closure `TSG-v23-01`) shows this repo's whole E2E suite runs against a
local Playwright build, not a distinct deployed staging environment — so
Playwright coverage is now the primary, CI-verifiable evidence path for
almost every observable AC, and a genuine human-run "staging" sign-off
(this skill's actual purpose) is now the **named fallback** CLAUDE.md §2
describes, exercised only for the few ACs Playwright cannot cover (e.g.
timing/animation completion judged by eye, cross-device rendering).

**Check first:** does a `docs/testing/staging_visual_test_script_*.md`
file already exist for this story/EPIC?

- **Yes** → use the full workflow, Steps 1–7 below, unchanged.
- **No** (the common case now) → skip to **Step 4-lite**: record the
  result directly in the story's DoQ sign-off block as a single line,
  matching CLAUDE.md §2's own fallback wording exactly:
  `**Staging sign-off:** {YYYY-MM-DD} — {one-line pass/fail result, e.g. "Pass — all 4 motion-timing components confirmed under 500ms" or "Fail — <what was observed>"}`
  No `V-xxx` check IDs, no separate test script file, no results table.
  If the result is a FAIL: still invoke `/dev-file` (Step 5, unchanged)
  before committing. Then go straight to Step 6 (Commit) — skip Steps
  2, 3, and 4's table/results-table mechanics entirely, since there is
  no check-ID table or test script file to stamp.

## Step 1 — Establish context

Read `.claude_current_state.json` → get `active_cycle`.

Determine from context (or ask if genuinely unclear):
- Which **story** these results are for (e.g. ST-06)
- Which **EPIC** (e.g. EPIC-02)
- Which **visual test script file** (e.g. `docs/testing/staging_visual_test_script_ST-06.md`)
- Which **QA evidence file** (e.g. `claude/cycles/<cycle_id>/qa_evidence_EPIC-02.md`)

Read both files before proceeding.

## Step 2 — Parse the results

Accept results in any freetext form. For each check ID mentioned
(e.g. V-CHART-01a, V-PATH-02b), extract:

| Field | Values |
|-------|--------|
| Check ID | e.g. V-CHART-01a |
| Result | PASS / FAIL / STAGING-BLOCKED / N/A |
| Notes | Any qualifier the tester provided |

For FAILs, also determine:
- Was a **code fix already committed**? → ask for the commit SHA and a
  one-line description of what was fixed
- Or is it **unfixed**? → will invoke /dev-file after Step 4

Checks not mentioned by the tester that exist in the script — note them
as **NOT REPORTED** in the results table; do not assume PASS.

## Step 3 — Stamp the visual test script

For each check in the visual test script file, find its Result line:

```
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___
```

Replace it with the stamped result. Use these formats exactly:

| Outcome | Replacement |
|---------|-------------|
| PASS | `**Result:** ✅ PASS` |
| FAIL (fixed in commit) | `**Result:** ❌ FAIL → FIXED in \`<sha>\` — <one-line description>` |
| FAIL (unfixed) | `**Result:** ❌ FAIL — <tester notes>` |
| STAGING-BLOCKED | `**Result:** ⛔ STAGING-BLOCKED` (leave as-is if already set) |
| N/A | `**Result:** — N/A — <reason>` |
| NOT REPORTED | Leave unchanged — do not modify the original checkboxes |

For checks that already have a stamped result (e.g. STAGING-BLOCKED was
pre-set in the script), confirm the tester's report agrees. If it
disagrees, use the tester's result and add a note.

## Step 4 — Update the QA evidence file

In the story's DoQ Sign-Off section, replace the "Visual AC: Deferred"
placeholder (or any prior partial record) with:

### Results table

```markdown
**Visual AC — Staging results ({YYYY-MM-DD}):**

| Check | Result | Notes |
|-------|--------|-------|
| V-CHART-01a (short description) | ✅ PASS | |
| V-CHART-02c (short description) | ❌ FAIL → FIXED | Root cause. Fix: `<sha>` |
| V-CHART-05a (short description) | ⛔ STAGING-BLOCKED | Reason. Backlog: BLG-xxx |
```

### Sign-off status line

Determine and append one of:

- **All non-blocked checks pass, no re-tests pending:**
  `**Visual sign-off status:** ✅ Granted — all checks pass. Blocked checks noted separately (see BLG-xxx).`

- **FAILs fixed but not yet re-tested:**
  `**Visual sign-off status:** ⏳ Provisional — re-test required for <check IDs> after deploy of \`<sha>\`.`

- **Unfixed FAILs remain:**
  `**Visual sign-off status:** ❌ Deferred — open failures: <check IDs>. See deviation records.`

STAGING-BLOCKED checks are **never** a blocker for sign-off status.
They are noted in the table and referenced to a BLG item only.

## Step 5 — Invoke /dev-file for unfixed FAILs

For each FAIL where no fix commit exists:

1. Use the `/dev-file` skill to file a formal deviation record.
2. Pass the following context:
   - EPIC and story
   - AC reference: the check ID and its scenario ref (from the test script)
   - Expected: what the test script says should be seen
   - Actual: what the tester reported
   - Priority: P2 Medium by default unless the failure blocks a core
     user workflow (P1) or is cosmetic only (P3)
3. After /dev-file completes, update the results table entry with the
   assigned DEV-ID:
   `| V-CHART-xx (description) | ❌ FAIL | DEV-EPIC02-ST06-01 filed |`

## Step 6 — Commit

Stage the visual test script and QA evidence files only.

Commit message format:
```
[EPIC-xx][ST-xx] Record staging visual QA results — N pass, M fail/fixed, K blocked
```

If /dev-file was also invoked and modified qa_evidence, those changes
are already staged — include them in the same commit.

Push immediately after committing.

## Step 7 — Report

Tell the user:
- Total counts: N pass / M fail (X fixed, Y unfixed) / K staging-blocked / J not reported
- Sign-off status (granted / provisional / deferred)
- Any re-test actions needed and what to re-test
- Any deviation IDs filed
- Commit SHA

## Error handling and lessons learnt

If anything goes wrong — wrong check ID parsed, wrong file modified,
sign-off status miscalculated — fix immediately and append to
`.claude/skills/lessons_learnt.md`:

```
| {YYYY-MM-DD} | record-visual-qa | {what went wrong} | {correct approach} |
```

Common mistakes to watch for:
- Treating NOT REPORTED checks as PASS — they are not the same
- Overwriting STAGING-BLOCKED result lines already set in the script
  without verifying the tester agrees
- Committing qa_evidence changes without the visual test script changes
  (both must go in the same commit)
- Forgetting to push after committing (GHA workflow may be waiting on
  the updated evidence)
