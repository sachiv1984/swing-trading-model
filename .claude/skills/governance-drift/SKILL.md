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

## Step 1b — OPERATIONAL_GUIDE.md self-consistency check (3-way)

`OPERATIONAL_GUIDE.md` is itself a Class 6 document and records its own version in three separate places that must all agree:

1. **Document header** (top of file): `**Version:**` / `**Last Updated:**`.
2. **§14 self-row** (inside the same metadata block read in Step 1): the table rows `| Version | X |` / `| Last Updated | Y |` — distinct from the per-engine rows below them.
3. **Change Log top row** (top row of the `| Version | Date | Change Summary |` table at the end of §14): the most recent entry's `Version`/`Date` columns.

These three have drifted out of sync repeatedly across this project's history (7+ recorded recurrences — 4.79/80/81/84/85, AUD-2026-06-10, AUD-2026-07-10-002, AUD-2026-07-14-001) because nothing mechanically checks them; the only guard has been a prose note (`shared_standards.md` §9.1) asking whoever edits the file to remember. Do not rely on that note — check directly:

Extract all three (version, date) pairs and compare pairwise. If all three match: `PASS — self-consistent`. If any pair differs, report `SELF-DRIFT` with the exact line number of each of the three locations and their values. Do not guess which one is correct — state that the Change Log top row is append-only and dated per-entry, so it is normally the most reliable source of truth, but flag it as a judgement call for the fixer to confirm (e.g. by checking `prompt_change_log.md`'s most recent `OPERATIONAL_GUIDE.md` row) rather than auto-selecting it.

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

OPERATIONAL_GUIDE.md SELF-CONSISTENCY (header vs §14 self-row vs Change Log top row)
  ✅ PASS — all three read v{x}/{date}
  ── or ──
  ❌ SELF-DRIFT FOUND
     Header (line {n}):        v{x} / {date}
     §14 self-row (line {n}):  v{y} / {date}
     Change Log top row (line {n}): v{z} / {date}
     Action: reconcile all three to the same value — do not assume the Change Log
     row is correct without confirming against prompt_change_log.md's latest
     OPERATIONAL_GUIDE.md entry.

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

If all versions match (including the Step 1b self-consistency check), no untracked/missing files: `✅ ALL IN SYNC — safe to commit`.

## Step 5 — Fix mismatches if instructed

If the user asks to fix drift, determine the correct version for each mismatch:

- If the file was recently edited and §14 was not updated: update §14 (and the phase section source prompt header per the standing rule in §14) and append to `claude/system/prompt_change_log.md`
- If §14 was updated but the file header was not bumped: bump the file header
- If Step 1b found SELF-DRIFT: confirm the true latest version via `prompt_change_log.md`'s most recent `OPERATIONAL_GUIDE.md` row, then write that single confirmed value to all three locations (header, §14 self-row, Change Log top row is presumably already correct — verify, don't just assume) in the same edit, so the fix doesn't itself go stale the next time any other §14 row is bumped
- Never silently pick one side — state which direction the fix goes and why

After fixing, re-run Steps 1–4 to confirm clean.

## Error handling and lessons learnt

If the §14 extraction logic misses a file or produces a false mismatch, append to `.claude/skills/lessons_learnt.md`:

```
| {YYYY-MM-DD} | governance-drift | {what was wrong} | {correct approach} |
```
