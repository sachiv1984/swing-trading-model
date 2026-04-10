# Skills — Lessons Learnt Log

This file is read at the start of every skill run. Each entry records a mistake that happened, what went wrong, and the correct approach — so the same mistake is never made twice.

**All skills append here when they catch or cause an error.**
**All skills read this before starting work.**

---

## Format

| Date | Skill | What went wrong | Correct approach |
|------|-------|-----------------|-----------------|
| *(entries added here as mistakes occur)* | | | |
| 2026-04-02 | commit-check | ST-06 schema reconciliation: accepted code inference (`reset_staging_db.sql` inserting `initial_cash`) as proof the column existed in the Supabase DB. Actual DB had no `initial_cash` — the script itself was stale. Signed off AC as Pass when schema was still wrong. | For any story whose AC requires `\d table` or schema confirmation, code inference is insufficient. Scripts referencing a column do not prove the column exists — the script may itself be wrong. Always require direct DB output (provided by the user) before signing off schema reconciliation AC-1. |
| 2026-03-31 | backlog-add | Assigned BLG-FEAT-12 to new item "Add gated feature rollout capability" without checking backlog_archive.md. BLG-FEAT-12 was already used by "Alert history table" (shipped v2.2, archived). Duplicate ID violation detected at roadmap rebalance STEP 3. | Step 1 ID scan must include BOTH backlog.md AND backlog_archive.md. Search `### BLG-{NAMESPACE}-` in both files and take the maximum across both. The SKILL.md Step 1 instruction has been updated to make this explicit. |

---

## How this works

When a skill encounters an error — whether caught by the skill itself, flagged by the user, or discovered after the fact — it appends a row to the table above.

At the start of every subsequent run, the skill reads this file and filters for rows matching its own name. It applies those lessons before taking any action.

The goal is a compounding improvement: each mistake makes the next run of that skill safer.

---

## Lessons by skill

*(This section is maintained automatically. Do not edit manually.)*

### backlog-add
| 2026-04-03 | backlog-add | Created new session sections (## N. New Backlog Items — Session YYYY-MM-DD) for each batch of new items instead of placing items under the correct existing type-based sections (§1–§8). This fragmented the backlog by date rather than organising it by type as intended. | New items must be appended to the correct existing type section (§1 Platform, §2 Features, §3 Frontend, §4 Backend, §5 QA, §6 Operations, §7 Spec Debt, §8 Governance). Never create a new numbered session section. The skill's default Step 4 behaviour is overridden by the backlog's Placement Rule (documented at the top of backlog.md). |

### cycle-status
*(No lessons recorded yet)*

### dev-file
*(No lessons recorded yet)*

### commit-check
*(No lessons recorded yet)*

### record-visual-qa
*(No lessons recorded yet)*

---

## Cross-skill lessons (general patterns)

| Date | Skill | What went wrong | Correct approach |
|------|-------|-----------------|-----------------|
| 2026-04-10 | general — commit format / governance_sync | ST-03 and ST-08 were implemented in the same commit as ST-02 but only `[ST-02]` appeared in the commit message. `governance_sync.yml` only scans for `[ST-xx]` in commit messages — omitting a story ID means the issue is never auto-closed and must be manually closed later. | When two stories land in the same commit, include all story IDs: `[EPIC-xx][ST-xx][ST-yy] <description>`. Also note: `governance_sync.yml` (pre-ST-10 fix) only reads `git log -1` (HEAD commit). In a multi-commit push, only the HEAD story is auto-closed. After ST-10 merges this improves to the full push range, but commit message discipline is still required. |
| 2026-03-25 | general — seed scripts | Seed script `DELETE FROM trade_reflections` caused silent transaction rollback on staging instances where that table doesn't exist. The entire seed was silently no-oped with no error visible to the caller. | Idempotency DELETE statements in seed scripts must only reference tables guaranteed to exist on all target environments. If the delete is guarded by a FK relationship that handles it via CASCADE on reset, omit the explicit DELETE entirely. |
| 2026-03-25 | general — Recharts cursor | Setting `cursor: grab/grabbing` on a div containing a Recharts chart only applies to the padding area. The Recharts `<svg>` element has `cursor: auto` by default, which overrides the inherited cursor and reverts to the browser default (arrow) inside the chart plot area. | When applying interactive cursor styles to Recharts charts, also set `style={{ cursor: "inherit" }}` on the chart component itself (e.g. `<AreaChart style={{ cursor: "inherit" }}>`). This makes the SVG and its overlay rect inherit the correct cursor from the parent div. |
