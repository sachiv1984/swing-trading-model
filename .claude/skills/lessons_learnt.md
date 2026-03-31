# Skills — Lessons Learnt Log

This file is read at the start of every skill run. Each entry records a mistake that happened, what went wrong, and the correct approach — so the same mistake is never made twice.

**All skills append here when they catch or cause an error.**
**All skills read this before starting work.**

---

## Format

| Date | Skill | What went wrong | Correct approach |
|------|-------|-----------------|-----------------|
| *(entries added here as mistakes occur)* | | | |
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
*(No lessons recorded yet)*

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
| 2026-03-25 | general — seed scripts | Seed script `DELETE FROM trade_reflections` caused silent transaction rollback on staging instances where that table doesn't exist. The entire seed was silently no-oped with no error visible to the caller. | Idempotency DELETE statements in seed scripts must only reference tables guaranteed to exist on all target environments. If the delete is guarded by a FK relationship that handles it via CASCADE on reset, omit the explicit DELETE entirely. |
| 2026-03-25 | general — Recharts cursor | Setting `cursor: grab/grabbing` on a div containing a Recharts chart only applies to the padding area. The Recharts `<svg>` element has `cursor: auto` by default, which overrides the inherited cursor and reverts to the browser default (arrow) inside the chart plot area. | When applying interactive cursor styles to Recharts charts, also set `style={{ cursor: "inherit" }}` on the chart component itself (e.g. `<AreaChart style={{ cursor: "inherit" }}>`). This makes the SVG and its overlay rect inherit the correct cursor from the parent div. |
