---
name: prompt-sync
description: Verify all governance prompts conform to the modular structure introduced in the 2026-05-09 refactor — governance_stack reference in §3, changelog reference in Change Log section, no inline history tables. Use after any session that adds or edits a governance prompt, when the user asks "are the prompts in sync?", "check prompt structure", or "verify prompt format". Also use as a one-time check after adding a new governance prompt to confirm it follows the canonical structure.
---

# Prompt Sync Check

Verifies that all Class 6 governance prompts in `claude/system/` follow the modular structure — no inline changelog tables, no copy-pasted canonical governance sources block.

## Step 0 — Load lessons

Read `.claude/skills/lessons_learnt.md`. Look for entries tagged `[prompt-sync]` and apply them. If the file doesn't exist, continue.

## Step 1 — Identify prompt files to check

Glob all `.md` files in `claude/system/` excluding:
- `claude/system/changelogs/` — these ARE the extracted changelogs
- `claude/system/shared/` — shared reference modules, different structure
- `claude/system/prompt_change_log.md` — append-only log, not a prompt

For each file, check whether it has a `**Version:**` header. Only check versioned files (governance prompts).

## Step 2 — Check governance stack reference (§3 pattern)

For each prompt file, search for the old inline canonical governance block. The old pattern is a section containing all four of:
- `claude/charter/team_charter.md`
- `claude/charter/document_lifecycle_guide.md`
- `claude/strategy/strategy_rules.md`
- role charters / `claude/agents/`

**FAIL** if: the file contains 3 or more of these four items listed inline (indicating the old copy-pasted block is still present).

**PASS** if: the file contains a reference to `claude/system/shared/governance_stack.md` instead.

**N/A** if: the file has none of the above (some prompts don't have a §3 canonical sources block).

## Step 3 — Check Change Log section structure

For each prompt file, find the `## Change Log` section (if present).

**FAIL** if: the section contains a Markdown table with columns like `| Version | Date | Change |` — this is an inline history table that should have been extracted.

**PASS** if: the section contains only a `See:` reference line pointing to `claude/system/changelogs/`.

**N/A** if: the file has no `## Change Log` section.

## Step 4 — Render report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROMPT SYNC CHECK — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checked {n} governance prompts.

GOVERNANCE STACK REFERENCE (§3)
  ✅ {file} — references shared/governance_stack.md
  ✅ {file} — N/A (no §3 block)
  ❌ {file} — inline canonical sources block still present

CHANGE LOG STRUCTURE
  ✅ {file} — references changelogs/
  ✅ {file} — N/A (no Change Log section)
  ❌ {file} — inline history table still present

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT: ✅ ALL IN SYNC | ❌ {n} VIOLATION(S)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 5 — Fix violations if instructed

For each inline governance stack block:
1. Replace the block content with: `Canonical governance stack: per \`claude/system/shared/governance_stack.md\`. This routine may not override any entry in that stack.`
2. Bump the file's `**Version:**` header (minor increment)
3. Update §14 in OPERATIONAL_GUIDE.md and the phase section source header
4. Append entry to `claude/system/prompt_change_log.md`

For each inline Change Log table:
1. Verify the content already exists in `claude/system/changelogs/<prompt>_changelog.md` (or create the file with that content)
2. Replace the inline table with: `See: [\`claude/system/changelogs/<name>_changelog.md\`](changelogs/<name>_changelog.md)`
3. Bump version, update §14, append to prompt_change_log.md

Apply all §6 checklist steps for every modified file before committing.

## Error handling and lessons learnt

If a false positive or false negative occurs (e.g. a shared/ file is incorrectly flagged), append to `.claude/skills/lessons_learnt.md`:

```
| {YYYY-MM-DD} | prompt-sync | {what was wrong} | {correct detection approach} |
```
