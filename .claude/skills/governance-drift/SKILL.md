---
name: governance-drift
description: Check that all Class 6 governance prompt versions match the §14 governance table in OPERATIONAL_GUIDE.md. Use before any governance commit, whenever the user asks "are the prompt versions in sync?", "check governance drift", or "do the prompts match the guide". Also use proactively after any session that modifies multiple governance files to catch missed updates before committing.
---

# Governance Drift Check

Detects version mismatches between Class 6 governance prompt files and the §14 governance table in `claude/system/OPERATIONAL_GUIDE.md`. Catches the "missed prompt" problem before it becomes a committed deviation.

## Step 0 — Load lessons

Read `.claude/skills/lessons_learnt.md`. Look for entries tagged `[governance-drift]` and apply them. If the file doesn't exist, continue.

## Step 1 — Extract §14 versions from OPERATIONAL_GUIDE

Read `claude/system/OPERATIONAL_GUIDE.md`.

Find the §14 metadata block — it's the table with rows like:
```
| Idea Intake Engine | `claude/system/idea_intake_prompt.md` v2.3 |
```

Extract every row that references a file in `claude/system/` or `claude/charter/` with a version number. Build a map:

```
file_path → version_in_guide
```

The metadata block is near the bottom of §14. Look for the pattern `| <label> | \`<path>\` v<version> |`.

## Step 2 — Extract actual versions from prompt files

For each file referenced in §14 that has a version number:

Read the file header (first 10 lines). Extract the `**Version:**` field.

Build a second map:
```
file_path → version_in_file
```

If a file referenced in §14 does not exist on disk: mark as `MISSING`.

If a file exists but has no `**Version:**` header: mark as `NO_HEADER`.

## Step 3 — Scan for unreferenced Class 6 files

Glob all files in `claude/system/` matching `*.md` that are NOT in `claude/system/changelogs/` and NOT in `claude/system/shared/`.

For each file found, check whether it appears in the §14 map from Step 1.

Files present on disk but absent from §14: mark as `UNTRACKED`.

Exclude files that are not governance prompts (e.g. `prompt_change_log.md`, `invariants.md` if not versioned, index files). A file is a governance prompt if it has a `**Version:**` header.

## Step 4 — Compare and render report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOVERNANCE DRIFT CHECK — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checked {n} files tracked in §14 + {m} untracked files found on disk.

VERSION MATCHES
  ✅ {file}  §14: v{x} | file: v{x}
  ...

VERSION MISMATCHES  ← these need fixing before committing
  ❌ {file}
     §14 says: v{x}
     File has: v{y}
     Action: bump file to v{y+1} or update §14 to match — determine which is correct

UNTRACKED FILES (on disk, not in §14)
  ⚠️  {file}  (v{x} in file header)
     Action: add to §14 governance table if this is a Class 6 prompt

MISSING FILES (in §14, not on disk)
  ❌ {file}
     Action: file has been deleted or moved — update §14

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT: ✅ ALL IN SYNC | ❌ {n} DRIFT(S) FOUND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If all versions match and no untracked/missing files: `✅ ALL IN SYNC — safe to commit`.

## Step 5 — Fix mismatches if instructed

If the user asks to fix drift, determine the correct version for each mismatch:

- If the file was recently edited and §14 was not updated: update §14 (and the phase section source prompt header per the standing rule in §14) and append to `claude/system/prompt_change_log.md`
- If §14 was updated but the file header was not bumped: bump the file header
- Never silently pick one side — state which direction the fix goes and why

After fixing, re-run Steps 1–4 to confirm clean.

## Error handling and lessons learnt

If the §14 extraction logic misses a file or produces a false mismatch, append to `.claude/skills/lessons_learnt.md`:

```
| {YYYY-MM-DD} | governance-drift | {what was wrong} | {correct approach} |
```
