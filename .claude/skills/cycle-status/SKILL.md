---
name: cycle-status
description: Show a complete, one-screen status summary for the active sprint cycle. Use this skill at the start of any session, whenever the user asks "where are we?", "what's the sprint status?", "what's left?", "what's blocked?", "show me the cycle", or any variant. Also use after returning from a break mid-sprint to re-establish context before continuing work.
---

# Cycle Status

Produces a clean, one-screen summary of the current sprint — no digging through multiple files needed.

## Step 0 — Load lessons

Read `.claude/skills/lessons_learnt.md`. Look for entries tagged `[cycle-status]` and apply them. If the file doesn't exist, continue.

## Step 1 — Read state files

Read these files in parallel:

1. `.claude_current_state.json` — active cycle ID, status, engine, next release, open escalations
2. `claude/cycles/{cycle_id}/execution_state.json` — story statuses, EPIC statuses, PR numbers, deviations
3. `claude/cycles/{cycle_id}/sprint_backlog.md` — story titles and sprint assignment (Sprint 1 / 2 / 3)

Also run: `gh pr list --repo . --state open --json number,title,headRefName,mergeable,isDraft 2>/dev/null` to get live PR state.

The `cycle_id` comes from `.claude_current_state.json` → `active_cycle`.

## Step 2 — Compute counts

From execution_state.json, tally stories across all EPICs:

| Status key | Label |
|------------|-------|
| `done` | Done |
| `in_progress` | In progress |
| `blocked_frontend` / `blocked_backend` / `blocked` | Blocked |
| `delegated` | Delegated (awaiting human) |
| `not_started` | Not started |

Count total stories. Compute % complete (done / total).

## Step 3 — Render the report

Output exactly this structure. Keep it compact — the goal is one screen:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CYCLE STATUS — {cycle_id}
{today's date} | Engine: {engine} | Status: {status}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SPRINT PROGRESS  {done}/{total} stories complete ({pct}%)
{▓▓▓▓▓░░░░░}  (filled blocks = done, empty = remaining)

STORIES BY EPIC
{For each EPIC, one line per story:}
  EPIC-01  [STATUS_ICON] ST-01  {title} {SPRINT_BADGE}
  EPIC-01  [STATUS_ICON] ST-02  {title} {SPRINT_BADGE}
  ...

Status icons:
  ✅ done          🔄 in_progress    ⏳ delegated
  🚫 blocked       ⬜ not_started

Sprint badges: [S1] [S2] [S3]

OPEN PRs
{List each open PR: #NNN [EPIC-xx] {title} — {MERGEABLE|CONFLICTING|DRAFT}}
{If none: "No open PRs"}

BLOCKED ITEMS
{For each blocked/delegated story: ST-xx — {title} — {unblock_criteria (first 80 chars)}}
{If none: "No blocked items ✅"}

OPEN ESCALATIONS
{List from .claude_current_state.json → open_escalations}
{If none: "No open escalations ✅"}

DEVIATIONS THIS CYCLE
{Count DEV-* entries across all qa_evidence files for this cycle}
{List each: DEV-ID (Pn) — {one-line description}}
{If none: "No deviations filed ✅"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Counting deviations

To count deviations without reading every qa_evidence file in full, grep for the pattern:
```
grep -r "^### DEV-" claude/cycles/{cycle_id}/qa_evidence_*.md 2>/dev/null
```

Extract the ID and the priority marker (P1/P2/P3) from each match.

## Step 4 — Surface any action needed

After the report, if any of the following are true, add a one-line advisory:

- Any P0 or P1 deviation exists → `⚠️  P0/P1 deviation open — requires immediate attention before next PR merge`
- Any story is `blocked` (not delegated) → `⚠️  {N} story/stories blocked — see BLOCKED ITEMS above`
- Any PR is `CONFLICTING` → `⚠️  PR #{n} has merge conflicts — resolve before continuing`
- Cycle status is `Blocked` → `🛑  Cycle is BLOCKED — do not proceed with governed routines until escalation is resolved`

## Error handling and lessons learnt

If anything in this skill produces an inaccurate summary (wrong count, missed story, wrong PR state), append to `.claude/skills/lessons_learnt.md`:

```
| {YYYY-MM-DD} | cycle-status | {what was inaccurate} | {correct approach or file to check} |
```

Fix the output immediately in the same session.
