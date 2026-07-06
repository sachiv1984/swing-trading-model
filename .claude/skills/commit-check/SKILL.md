---
name: commit-check
description: Run a pre-commit checklist to catch process violations before they become documented deviations. Use this skill before every git commit on an exec branch, whenever the user says "check before committing", "is this ready to commit?", "pre-commit check", or "commit check". Also use proactively whenever you are about to commit changes that touch API contracts, governance files, or involve a new endpoint — those are the highest-risk areas for silent process violations.
---

# Commit Check

Runs the project's mandatory pre-commit checklist and either clears the commit or surfaces what needs fixing first.

## Step 0 — Load lessons

Read `.claude/skills/lessons_learnt.md`. Look for entries tagged `[commit-check]` and apply them. If the file doesn't exist, continue.

## Step 1 — Get current context

Run these commands in parallel:

```bash
git branch --show-current                          # current branch name
git diff --cached --name-only                      # staged files
git diff --cached --stat                           # staged summary
git log --oneline -1                               # last commit (for context)
```

## Step 2 — Determine commit type

From the branch name, determine whether this is:

| Branch pattern | Commit type |
|----------------|-------------|
| `exec/<cycle>/<epic>` | **Sprint execution** — format: `[EPIC-xx][ST-xx] <description>` |
| `main` | **Direct-to-main** — only permitted for governance commits: `[GOVERNANCE] <description>` |
| Anything else | Flag as unexpected — confirm with user before proceeding |

## Step 3 — Run the checklist

Run every check. Do not skip any. Mark each PASS ✅, FAIL ❌, or N/A —.

---

### Check 1 — Branch matches EPIC

The commit must land on the branch corresponding to its EPIC.

- Get the EPIC of the story being committed (from staged file paths or ask the user)
- Confirm the branch name ends in the correct EPIC: `exec/<cycle>/EPIC-xx`
- **FAIL if:** EPIC-03 work is being committed on the EPIC-02 branch, or any cross-EPIC commit is about to happen

---

### Check 2 — Commit message format

The commit message must follow the canonical format exactly.

For sprint execution commits:
```
[EPIC-xx][ST-xx] <imperative description starting with a capital letter>
```

For governance commits (on main or governance branches):
```
[GOVERNANCE] <imperative description>
```

**FAIL if:** Missing brackets, wrong prefix, lowercase start, missing story ID, or any other format deviation.

If no commit message has been composed yet, draft the correct one for the user.

---

### Check 3 — OpenAPI drift detection

If any of the staged files match `docs/specs/api_contracts/**`:

1. Check whether the staged file contains a new or modified `## METHOD /path` heading (at exactly `##` level — not `###`)
2. If yes: confirm that `docs/reference/openapi.yaml` is also staged
3. **FAIL if:** A `## METHOD /path` heading was added or changed but openapi.yaml is not staged

Also check: if `docs/reference/openapi.yaml` is staged, confirm the version number was bumped.

Note: This is a hard gate — PRs will be blocked by `OpenAPI Drift Detection` CI if this is missed.

---

### Check 4 — Governance file §6 checklist

If any of the staged files are in `claude/system/`, `claude/charter/`, or `claude/strategy/`:

Confirm all four §6 steps are complete in this commit:
- [ ] Version bumped in the file's own header (`**Version:**`)
- [ ] `docs/ops/OPERATIONAL_GUIDE.md` §14 governance table updated to the new version
- [ ] Corresponding phase section in OPERATIONAL_GUIDE.md (§5–§10) source prompt header updated
- [ ] Entry appended to `claude/system/prompt_change_log.md`

**FAIL if:** Any of the four steps are missing. The §6 checklist is non-negotiable.

---

### Check 5 — No direct commits to main for sprint work

**FAIL if:** The current branch is `main` and the staged files include implementation code (backend Python files, frontend JS/JSX, SQL migrations). Direct-to-main is only for governance, documentation, and CLAUDE.md-class changes.

---

### Check 6 — No sealed artefacts modified

Check `.claude_current_state.json` for `sealed: true` flags and check `claude/cycles/{cycle_id}/state.json` for sealed artefact paths.

**FAIL if:** Any staged file is in the sealed artefacts list.

---

### Check 8 — QA sign-off Date completeness

This check fires when any `qa_evidence_EPIC-xx.md` file is staged for commit, or when the commit is about to open a PR (i.e., if the staged changes include a PR-related action for an EPIC).

1. For each staged `qa_evidence_EPIC-xx.md`, read the sign-off block.
2. Locate the line: `- Date:` in the sign-off block.
3. **FAIL if:** The Date field is blank or contains only a placeholder (e.g., `- Date:` with nothing after it, `- Date: <fill in>`, or `- Date: pending`).
4. **PASS if:** The Date field contains a non-blank, non-placeholder value (e.g., `- Date: 2026-04-14`).

Per execution_prompt.md §3.2.B (BLG-GOV-18): a PR must not be opened until the DoQ sign-off Date is non-blank.

---

### Check 7 — E2E coverage declaration for frontend stories

This check fires when **any** of the staged files are frontend implementation files (e.g. `src/**/*.js`, `src/**/*.jsx`, `src/**/*.ts`, `src/**/*.tsx`).

1. Identify the ST story ID from the commit message or staged context.
2. Look for a corresponding E2E coverage declaration. This can be in any of:
   - The QA evidence file for the active EPIC (`claude/cycles/{cycle_id}/qa_evidence_EPIC-xx.md`) — look for a row or note under the story's DoQ sign-off block
   - A comment block in the staged spec file (`tests/e2e/*.spec.js`) referencing the story ID
   - An explicit note in the commit message body (e.g. `E2E: SC-XX-01–05 in tests/e2e/foo.spec.js`)
3. **PASS if** any of the following are true:
   - One or more Playwright scenario IDs (e.g. `SC-*`) are referenced and a corresponding `tests/e2e/*.spec.js` file exists or is staged
   - The story is explicitly marked `E2E: N/A — visual-only AC` in the QA evidence or commit message (visual-only means no interaction, API call, or state-transition AC exists)
4. **FAIL if** neither condition is met — frontend code is being committed with no E2E declaration at all.

On FAIL, prompt the user to either:
- Identify which scenario IDs are covered and confirm the spec file exists, or
- Explicitly state `E2E: N/A — visual-only AC` if no testable interactions exist

This check is advisory for stories with `delegated_qa` status that have not yet had their E2E spec authored — flag it but do not block if the delegation log shows E2E authoring is a pending follow-up action.

---

### Check 9 — Diff verification for multi-file governance commits

This check fires when **2 or more** governance files (`claude/system/**`, `claude/charter/**`, `claude/agents/**`, `claude/roadmap/**`, `claude/backlog/**`) are staged together in the same commit.

1. Build the **intended file set** — the list of files the commit was actually meant to touch (from the task/story description, or from what was just edited in this session).
2. Compare against `git diff --cached --name-only` (the actual staged set).
3. **FAIL if:**
   - A file in the intended set is missing from staged (would silently drop a required change — e.g. a §6 checklist file left unstaged).
   - A file appears in staged that isn't in the intended set (would silently bundle an unrelated change into this commit — e.g. a leftover edit from earlier in the session).
4. **PASS if** the two sets match exactly.

This is the diff-verification step required by BLG-GOV-167 / `shared_standards.md §17` — multi-file governance commits are the highest-risk case for a partial or over-broad `git add`, since §6 compliance (version bump + OPERATIONAL_GUIDE.md + phase header + prompt_change_log.md) spans several files that must land together.

---

## Step 4 — Render the result

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMMIT CHECK — {branch} — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Staged files ({n}):
  {list each staged file}

  ✅ Check 1 — Branch matches EPIC
  ✅ Check 2 — Commit message format
     Suggested: [EPIC-03][ST-07] Update health_endpoints.md to v1.1
  ❌ Check 3 — OpenAPI drift detection
     REASON: docs/specs/api_contracts/alerts_endpoints.md staged with new ## POST /alerts/rules
     but docs/reference/openapi.yaml is NOT staged.
     ACTION: Stage openapi.yaml before committing.
  ✅ Check 4 — Governance §6 checklist (N/A — no governance files staged)
  ✅ Check 5 — No direct commits to main for sprint work
  ✅ Check 6 — No sealed artefacts modified
  ✅ Check 7 — E2E coverage declaration (N/A — no frontend files staged)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT: ❌ NOT READY — 1 check failed
Fix Check 3 before committing.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If all checks pass:
```
RESULT: ✅ READY TO COMMIT
Suggested message: [EPIC-03][ST-07] Update health_endpoints.md to v1.1
```

## Step 5 — On failure, help fix it

Don't just report failures — help resolve them:

- **Check 3 fail (OpenAPI):** Stage the openapi.yaml changes or prompt the user to add the missing path entry
- **Check 4 fail (§6):** Identify exactly which of the four steps is missing and action it
- **Check 2 fail (message):** Draft the correct commit message
- **Check 1 fail (branch):** Explain the correct branch and how to move the changes there
- **Check 7 fail (E2E):** Ask whether the story has interaction/API-call AC (if yes, identify which scenario IDs need spec coverage and whether a spec file exists or needs creating); if all AC is visual-only, add `E2E: N/A — visual-only AC` to the commit message body

Re-run the checklist after fixes are applied to confirm the commit is clean.

## Error handling and lessons learnt

If a check produced a false result (passed something it should have caught, or flagged something that was fine), append to `.claude/skills/lessons_learnt.md`:

```
| {YYYY-MM-DD} | commit-check | {check name} — {what was wrong with the check result} | {how to correctly evaluate this check} |
```

Common mistakes to watch for:
- Missing `##`-level vs `###`-level distinction when scanning api_contracts files for new endpoints
- Assuming openapi.yaml is already staged without actually checking `git diff --cached --name-only`
- Skipping Check 4 when governance files are staged alongside implementation files (both must pass)
